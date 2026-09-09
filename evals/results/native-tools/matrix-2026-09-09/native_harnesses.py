"""Native harness adapters; no direct model API calls or live configuration writes."""
from __future__ import annotations

from dataclasses import dataclass
import gzip
import json
import re
from pathlib import Path
import shutil
import subprocess
from typing import Any

from recall import configured_defaults, prepare_home


@dataclass(frozen=True)
class Harness:
    name: str
    binary: Path
    defaults: dict[str, Any]


def discover() -> tuple[Harness, ...]:
    home = Path.home()
    claude_config = json.loads((home / '.claude/settings.json').read_text())
    claude_defaults = {key: claude_config[key] for key in ('model', 'effortLevel') if key in claude_config}
    agy_settings = json.loads((home / '.gemini/antigravity-cli/settings.json').read_text())
    agy_global = json.loads((home / '.gemini/config/config.json').read_text())
    agy_defaults = {key: value for source in (agy_global.get('userSettings', {}), agy_settings)
                    for key, value in source.items() if key in ('model', 'effort', 'agent', 'defaultModel', 'defaultAgent', 'reasoningEffort')}
    def executable(name: str) -> Path:
        found = shutil.which(name)
        if found is None:
            raise ValueError(f'Required native CLI not found on PATH: {name}')
        path = Path(found).resolve()
        with path.open('rb') as stream:
            if stream.read(4) != b'\x7fELF':
                raise ValueError(f'{name} resolves to a launcher rather than the supported native Linux executable: {path}')
        return path
    return (
        Harness('codex', executable('codex'), configured_defaults(home / '.codex')),
        Harness('claude', executable('claude'), claude_defaults),
        Harness('antigravity', executable('agy'), agy_defaults),
    )


def setup_home(harness: Harness, destination: Path) -> None:
    destination.mkdir(mode=0o700)
    source = Path.home()
    if harness.name == 'codex':
        prepare_home(source / '.codex', destination, harness.defaults)
    elif harness.name == 'claude':
        config = destination / '.claude'
        config.mkdir(mode=0o700)
        shutil.copyfile(source / '.claude/.credentials.json', config / '.credentials.json')
        (config / '.credentials.json').chmod(0o600)
        (config / 'settings.json').write_text(json.dumps(harness.defaults))
        (destination / '.claude.json').write_text(json.dumps({'hasCompletedOnboarding': True}))
    elif harness.name == 'antigravity':
        config = destination / '.gemini/antigravity-cli'
        config.mkdir(parents=True)
        (config / 'settings.json').write_text(json.dumps(harness.defaults))
        # The native CLI uses Secret Service on the host and this documented-by-
        # trace file fallback when no D-Bus socket exists inside the sandbox.
        # Read just its unlocked item; never print or archive the credential.
        script = """import dbus, json, pathlib, sys
b=dbus.SessionBus();service='org.freedesktop.secrets'
i=dbus.Interface(b.get_object(service,'/org/freedesktop/secrets'),'org.freedesktop.Secret.Service')
unlocked,locked=i.SearchItems({'service':'gemini','username':'antigravity'})
if len(unlocked)!=1: raise SystemExit('Expected one unlocked Antigravity credential')
_,session=i.OpenSession('plain',dbus.String(''))
try:
 secret=dbus.Interface(b.get_object(service,unlocked[0]),'org.freedesktop.Secret.Item').GetSecret(session)
 data=bytes(secret[2]);value=json.loads(data)
 if not isinstance(value.get('token'),dict): raise SystemExit('Unexpected Antigravity credential shape')
 p=pathlib.Path(sys.argv[1]);p.write_bytes(data);p.chmod(0o600)
finally: dbus.Interface(b.get_object(service,session),'org.freedesktop.Secret.Session').Close()
"""
        subprocess.run(['/usr/bin/python3', '-c', script, str(config / 'antigravity-oauth-token')],
                       check=True, capture_output=True, timeout=20)


def bubble(workspace: Path, private_home: Path, harness: Harness, skill: Path | None = None) -> list[str]:
    cmd = ['bwrap', '--unshare-pid', '--die-with-parent', '--new-session', '--clearenv',
           '--ro-bind', '/usr', '/usr', '--symlink', 'usr/bin', '/bin',
           '--symlink', 'usr/lib', '/lib', '--symlink', 'usr/lib', '/lib64',
           '--dev', '/dev', '--proc', '/proc', '--tmpfs', '/tmp', '--dir', '/etc']
    for name in ('resolv.conf', 'hosts', 'nsswitch.conf', 'passwd', 'group', 'ssl', 'ca-certificates'):
        p = Path('/etc') / name
        if p.exists():
            cmd += ['--ro-bind', str(p.resolve()), f'/etc/{name}']
    cmd += ['--ro-bind', str(harness.binary), '/opt/harness',
            '--bind', str(private_home), '/eval-home', '--bind', str(workspace), '/workspace',
            '--ro-bind', str(workspace / 'product'), '/workspace/product']
    if harness.name == 'codex':
        cmd += ['--ro-bind', str(harness.binary.with_name('codex-code-mode-host')), '/opt/codex-code-mode-host']
    if skill is not None:
        cmd += ['--ro-bind', str(skill), '/workspace/skill']
    env = {'HOME': '/eval-home', 'CODEX_HOME': '/eval-home/.codex', 'CLAUDE_CONFIG_DIR': '/eval-home/.claude',
           'XDG_CONFIG_HOME': '/eval-home/.config', 'XDG_DATA_HOME': '/eval-home/.local/share',
           'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'TERM': 'dumb', 'USER': 'deck',
           'TMPDIR': '/tmp', 'SHELL': '/bin/bash', 'CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC': '1',
           'AGY_CLI_DISABLE_AUTO_UPDATE': '1'}
    for key, value in env.items():
        cmd += ['--setenv', key, value]
    return cmd + ['--chdir', '/workspace']


def invocation(harness: Harness, timeout: int, prompt: str) -> list[str]:
    if harness.name == 'codex':
        return ['/opt/harness', 'exec', '--skip-git-repo-check', '--ephemeral', '--ignore-rules',
                '--dangerously-bypass-approvals-and-sandbox', '--color', 'never', '--json',
                '--output-last-message', '/workspace/work/response.md', '-']
    if harness.name == 'claude':
        return ['/opt/harness', '--print', '--verbose', '--output-format', 'stream-json',
                '--safe-mode', '--strict-mcp-config', '--no-chrome', '--no-session-persistence',
                '--dangerously-skip-permissions', '--settings', '/eval-home/.claude/settings.json']
    return ['/opt/harness', '--print=' + prompt, '--output-format', 'stream-json', '--new-project',
            '--dangerously-skip-permissions', '--print-timeout', f'{timeout}s',
            '--log-file', '/workspace/work/antigravity.log']


def boundary(command: list[str], harness: Harness) -> dict[str, Any]:
    script = """import pathlib, json, ssl
p=pathlib.Path
checks={q:not p(q).exists() for q in ['/home/deck','/root','/grader','/workspace/evals','/workspace/criteria.json']}
try:
 (p('/workspace/product')/'probe').write_text('x');checks['inputs_read_only']=False
except OSError: checks['inputs_read_only']=True
checks['native_harness']=p('/opt/harness').is_file()
checks['python']=p('/usr/bin/python3').is_file()
checks['rg']=p('/usr/bin/rg').is_file()
checks['certificates']=bool(ssl.create_default_context().get_ca_certs())
print(json.dumps(checks));raise SystemExit(not all(checks.values()))
"""
    r = subprocess.run(command + ['/usr/bin/python3', '-c', script], capture_output=True, text=True, timeout=20)
    if r.returncode:
        raise RuntimeError(f'{harness.name} isolation failed: {r.stdout} {r.stderr}')
    result: dict[str, Any] = json.loads(r.stdout)
    return result


def summarize(path: Path, harness: Harness) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    with gzip.open(path, 'rt', encoding='utf-8', errors='replace') as stream:
        for n, line in enumerate(stream, 1):
            try:
                event = json.loads(line)
                if isinstance(event, dict):
                    events.append(event)
            except ValueError:
                events.append({'type': 'non_json', 'line': n, 'text': line[:1000]})
    usage: list[dict[str, Any]] = []
    for event in events:
        if event.get('event') == 'result':
            result = event.get('result', {})
            usage.append({'event': 'result', 'usage': result.get('usage'), 'status': result.get('status'),
                          'duration_seconds': result.get('duration_seconds'), 'num_turns': result.get('num_turns')})
        if event.get('event') == 'step_update' and 'usage' in event.get('step_update', {}):
            step = event['step_update']
            usage.append({'event': 'step_update', 'step_index': step.get('step_index'), 'usage': step['usage']})
        if 'usage' in event:
            usage.append({'type': event.get('type'), 'usage': event['usage']})
        if event.get('type') == 'result':
            usage.append({k: v for k, v in event.items() if k in ('type', 'modelUsage', 'total_cost_usd', 'duration_ms', 'num_turns')})
    return {'harness': harness.name, 'event_types': sorted({str(e.get('type', e.get('event'))) for e in events}),
            'usage_events': usage, 'event_count': len(events),
            'errors': [e for e in events if e.get('is_error') or e.get('type') in ('error', 'turn.failed', 'non_json')],
            'initialization': [e for e in events if (e.get('type') == 'system' and e.get('subtype') == 'init') or e.get('event') == 'init']}


def version_info(harness: Harness) -> dict[str, str]:
    if harness.name == 'antigravity':
        match = re.search(rb'(\d+\.\d+\.\d+)\n<SCRIPT', harness.binary.read_bytes())
        if match is None:
            raise ValueError('Cannot identify Antigravity embedded release version')
        return {'version': match.group(1).decode(), 'source': 'embedded release string; no advertised --version option'}
    result = subprocess.run([str(harness.binary), '--version'], capture_output=True, text=True, check=True, timeout=10)
    return {'version': result.stdout.strip(), 'source': 'native CLI --version'}
