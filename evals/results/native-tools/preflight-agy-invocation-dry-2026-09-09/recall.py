#!/usr/bin/env python3
"""Opt-in, isolated, matched fresh-session recall evaluation (Python 3.11+).

Run: python3 evals/recall.py --run --output evals/results/v1-recall/RUN_NAME
Without --run, validates/materializes cases and the bwrap boundary without an LLM.
The runner records evidence; a human reviews decisions against private criteria.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import selectors
import shutil
import signal
import subprocess
import tarfile
import tempfile
import threading
import time
import tomllib
from typing import Any

from fixtures import Case, cases, materialize

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_CAP = 32 * 1024 * 1024  # per stdout/stderr stream; excess terminates the case
STOP_BETWEEN_CASES = threading.Event()


def request_stop(signum: int, _frame: Any) -> None:
    """Finish active sessions and skip queued sessions after SIGINT/SIGTERM."""
    STOP_BETWEEN_CASES.set()
    print(f"Received signal {signum}; active cases will finish and queued cases will be skipped.", flush=True)


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def hashes(directory: Path) -> dict[str, str]:
    return {
        str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(directory.rglob("*")) if p.is_file() and not p.is_symlink()
    }


def aggregate_hash(values: dict[str, str]) -> str:
    return hashlib.sha256(json.dumps(values, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def archive_inputs(output: Path) -> dict[str, str]:
    """Preserve exact original source files without thousands of loose artifacts."""
    source = output / "inputs"
    destination = output / "inputs.tar.gz"
    with tarfile.open(destination, "w:gz") as archive:
        archive.add(source, arcname="inputs")
    result = {"path": destination.name, "sha256": hashlib.sha256(destination.read_bytes()).hexdigest()}
    shutil.rmtree(source)
    return result


def configured_defaults(home: Path) -> dict[str, Any]:
    config = tomllib.loads((home / "config.toml").read_text(encoding="utf-8"))
    # Only harmless model defaults survive. No hooks, plugins, MCPs, projects,
    # instructions, shared sessions, environment providers, or shell snapshots.
    result = {k: config[k] for k in ("model", "model_reasoning_effort", "service_tier") if k in config}
    if config.get("model_provider", "openai") != "openai":
        raise ValueError("Custom model providers require a separately reviewed minimal auth/config adapter.")
    if not (home / "auth.json").is_file():
        raise ValueError("This runner requires native Codex file authentication; no credentials are printed.")
    return result


def prepare_home(source: Path, target: Path, defaults: dict[str, Any]) -> None:
    codex_home = target / ".codex"
    codex_home.mkdir(parents=True, mode=0o700)
    shutil.copyfile(source / "auth.json", codex_home / "auth.json")
    (codex_home / "auth.json").chmod(0o600)
    lines = [f"{key} = {json.dumps(value)}" for key, value in defaults.items()]
    lines += [
        'approval_policy = "never"',
        'sandbox_mode = "danger-full-access"',
        'web_search = "disabled"',
        '[features]',
        'apps = false',
        'plugins = false',
        'remote_plugin = false',
        'multi_agent = false',
        'browser_use = false',
        'computer_use = false',
        'shell_snapshot = false',
        'skill_search = false',
        'memories = false',
    ]
    (codex_home / "config.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def bubble_command(workspace: Path, auth_home: Path, codex: Path, skill: Path | None) -> list[str]:
    cmd = [
        "bwrap", "--unshare-pid", "--die-with-parent", "--new-session", "--clearenv",
        "--ro-bind", "/usr", "/usr", "--symlink", "usr/bin", "/bin",
        "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
        "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp", "--dir", "/etc",
    ]
    for filename in ("resolv.conf", "hosts", "nsswitch.conf", "passwd", "group", "ssl", "ca-certificates"):
        source = Path("/etc") / filename
        if source.exists():
            cmd += ["--ro-bind", str(source.resolve()), f"/etc/{filename}"]
    cmd += [
        "--ro-bind", str(codex), "/opt/codex",
        "--ro-bind", str(codex.with_name("codex-code-mode-host")), "/opt/codex-code-mode-host",
        "--bind", str(auth_home), "/eval-home",
        "--bind", str(workspace), "/workspace",
        "--ro-bind", str(workspace / "product"), "/workspace/product",
    ]
    if skill is not None:
        cmd += ["--ro-bind", str(skill), "/workspace/skill"]
    cmd += [
        "--setenv", "HOME", "/eval-home", "--setenv", "CODEX_HOME", "/eval-home/.codex",
        "--setenv", "PATH", "/usr/bin:/bin", "--setenv", "LANG", "C.UTF-8",
        "--setenv", "TERM", "dumb", "--setenv", "USER", "deck",
        "--setenv", "TMPDIR", "/tmp", "--chdir", "/workspace",
    ]
    return cmd


def probe_boundary(command: list[str]) -> dict[str, Any]:
    # Executed by the runner before starting Codex, not sent as a model task.
    script = """import json, pathlib, os, ssl
root=pathlib.Path('/workspace/product')
hidden=['/home/deck/Projects','/home/deck/.codex','/root','/grader','/workspace/fixtures.py']
checks={p:not pathlib.Path(p).exists() for p in hidden}
try:
 (root/'__write_probe__').write_text('mutation')
 checks['input_read_only']=False
except OSError:
 checks['input_read_only']=True
checks['python']=pathlib.Path('/usr/bin/python3').is_file()
checks['rg']=pathlib.Path('/usr/bin/rg').is_file()
checks['native_codex']=pathlib.Path('/opt/codex').is_file()
checks['code_mode_host']=pathlib.Path('/opt/codex-code-mode-host').is_file()
checks['os_certificate_store']=len(ssl.create_default_context().get_ca_certs()) > 0
checks['no_parent_processes']=all(not (pathlib.Path('/proc')/p/'cmdline').read_bytes().startswith(b'python3 evals/recall.py') for p in os.listdir('/proc') if p.isdigit() and (pathlib.Path('/proc')/p/'cmdline').exists())
print(json.dumps(checks))
raise SystemExit(0 if all(checks.values()) else 1)
"""
    result = subprocess.run(command + ["/usr/bin/python3", "-c", script], capture_output=True, text=True, timeout=20)
    if result.returncode:
        raise RuntimeError(f"Isolation probe failed: {result.stdout} {result.stderr}")
    parsed: dict[str, Any] = json.loads(result.stdout)
    return parsed


def prompt_for(case: Case, arm: str) -> str:
    activation = "Use $long-horizon at /workspace/skill/SKILL.md for this handoff review.\n\n" if arm == "skill" else ""
    return (
        activation + case.request + "\n\n"
        "The product workspace is /workspace/product. Start with brief.md and current.md. "
        "The attached source archive is a read-only snapshot; you may search it and inspect original records. "
        "Use only this local snapshot for the review. No external systems are connected and no live actions are authorized here. "
        "Write your dated recommendation to /workspace/work/decision.md, including the relevant prior actions, "
        "what the evidence supports now, the next useful action, and important uncertainty. Cite specific source paths and source IDs "
        "so the product owner can inspect your reasoning. Preserve unknown dates. Finish with a brief response pointing to your decision.\n"
    )


def signal_group(process: subprocess.Popen[bytes], signum: int) -> None:
    try:
        os.killpg(process.pid, signum)
    except ProcessLookupError:
        pass


def capture(command: list[str], prompt: str, destination: Path, timeout: int) -> dict[str, Any]:
    """Capture bounded streams and clean up even when an exited leader leaves pipes open."""
    started = time.monotonic()
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    assert process.stdin is not None and process.stdout is not None and process.stderr is not None
    selector = selectors.DefaultSelector()
    counts = {"stdout": 0, "stderr": 0}
    reason: str | None = None
    terminated_at: float | None = None
    killed_at: float | None = None
    forced_pipe_close = False
    try:
        process.stdin.write(prompt.encode())
        process.stdin.close()
        selector.register(process.stdout, selectors.EVENT_READ, "stdout")
        selector.register(process.stderr, selectors.EVENT_READ, "stderr")
        with gzip.open(destination / "trace.jsonl.gz", "wb") as stdout_file, gzip.open(destination / "stderr.txt.gz", "wb") as stderr_file:
            files = {"stdout": stdout_file, "stderr": stderr_file}
            while selector.get_map():
                now = time.monotonic()
                if reason is None and now - started > timeout:
                    reason = "wall_timeout"
                if reason is not None and terminated_at is None:
                    signal_group(process, signal.SIGTERM)
                    terminated_at = now
                # Descendants may retain pipe FDs after the leader exits. Escalate
                # for the whole owned group regardless of process.poll().
                if terminated_at is not None and killed_at is None and now - terminated_at >= 2:
                    signal_group(process, signal.SIGKILL)
                    killed_at = now
                if killed_at is not None and now - killed_at >= 2:
                    forced_pipe_close = True
                    break
                for key, _ in selector.select(timeout=0.25):
                    chunk = os.read(key.fd, 65536)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    stream = str(key.data)
                    remaining = max(0, OUTPUT_CAP - counts[stream])
                    files[stream].write(chunk[:remaining])
                    files[stream].flush()
                    counts[stream] += len(chunk)
                    if reason is None and counts[stream] > OUTPUT_CAP:
                        reason = f"{stream}_capture_cap"
            try:
                code = process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                reason = reason or "leader_did_not_exit_after_streams_closed"
                signal_group(process, signal.SIGKILL)
                code = process.wait(timeout=10)
    finally:
        selector.close()
        signal_group(process, signal.SIGKILL)
        for stream_file in (process.stdin, process.stdout, process.stderr):
            try:
                stream_file.close()
            except OSError:
                pass
        if process.poll() is None:
            process.kill()
        process.wait(timeout=10)
    return {"exit_code": code, "termination_reason": reason, "raw_stream_bytes": counts,
            "capture_cap_per_stream_bytes": OUTPUT_CAP, "forced_pipe_close": forced_pipe_close,
            "elapsed_seconds": round(time.monotonic() - started, 3)}


def summarize_trace(path: Path) -> dict[str, Any]:
    commands: list[dict[str, Any]] = []
    usage: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    messages: list[str] = []
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as trace:
        for number, line in enumerate(trace, 1):
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                errors.append({"line": number, "type": "invalid_jsonl", "text": line[:1000]})
                continue
            if event.get("type") == "turn.completed":
                usage.append(event.get("usage", {}))
            if event.get("type") in {"error", "turn.failed"}:
                errors.append(event)
            item = event.get("item", {})
            if event.get("type") == "item.completed" and item.get("type") == "error":
                errors.append(event)
            if event.get("type") == "item.completed" and item.get("type") == "command_execution":
                commands.append(item)
            if event.get("type") == "item.completed" and item.get("type") == "agent_message":
                messages.append(str(item.get("text", "")))
    # These are inspection aids, not automatic correctness judgments. Full command
    # output is retained because a suspicious string or failed command is ambiguous.
    possible_boundary_attempts = [item for item in commands if any(
        needle in str(item.get("command", "")) for needle in
        ("/home/", "/eval-home", "/grader", "curl ", "wget ", "https://", "http://", "auth.json", "rm ", "chmod ", "../")
    )]
    return {
        "usage_events": usage, "command_count": len(commands), "commands": commands,
        "failed_commands": [item for item in commands if item.get("exit_code", 0) != 0],
        "possible_boundary_attempts_for_manual_review": possible_boundary_attempts,
        "cli_output_truncation_markers": sum("truncat" in str(item.get("aggregated_output", "")).lower() for item in commands),
        "errors": errors, "agent_messages": messages,
    }


def _evaluate(case: Case, arm: str, output: Path, frozen_skill: Path, native: Path,
             auth_source: Path, defaults: dict[str, Any], run: bool, timeout: int) -> dict[str, Any]:
    if STOP_BETWEEN_CASES.is_set():
        return {"case": case.name, "arm": arm, "not_launched": "operator_stop_between_cases"}
    destination = output / "cases" / case.name / arm
    destination.mkdir(parents=True)
    prompt = prompt_for(case, arm)
    (destination / "prompt.txt").write_text(prompt, encoding="utf-8")
    input_root = output / "inputs" / case.name
    initial_hashes = hashes(input_root)
    with tempfile.TemporaryDirectory(prefix=f"recall-{case.name}-{arm}-", dir=ROOT / "evals" / "runs") as temporary:
        temporary_root = Path(temporary)
        workspace = temporary_root / "workspace"
        shutil.copytree(input_root, workspace / "product")
        (workspace / "work").mkdir()
        auth_home = temporary_root / "auth-home"
        prepare_home(auth_source, auth_home, defaults)
        bubble = bubble_command(workspace, auth_home, native, frozen_skill if arm == "skill" else None)
        boundary = probe_boundary(bubble)
        command = bubble + [
            "/opt/codex", "exec", "--skip-git-repo-check", "--ephemeral", "--ignore-rules",
            "--dangerously-bypass-approvals-and-sandbox", "--color", "never", "--json",
            "--output-last-message", "/workspace/work/response.md", "-",
        ]
        metadata: dict[str, Any] = {
            "case": case.name, "arm": arm, "started_at": utc_now(), "model_defaults": defaults,
            "command": command, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "input_tree_sha256": aggregate_hash(initial_hashes), "input_hashes": initial_hashes,
            "skill_hashes": hashes(frozen_skill) if arm == "skill" else {},
            "isolation_probe": boundary, "fresh_session": True, "shared_conversation": False,
            "network_boundary": "Host network retained for Codex API; task forbids external calls. This is filesystem/PID isolation, not a network sandbox.",
            "private_credential_home": "Temporary local copy; omitted from artifacts and removed on exit.",
        }
        dump(destination / "manifest.json", metadata)
        print(f"{utc_now()} {'RUN' if run else 'PREPARED'} {case.name}/{arm}", flush=True)
        if run:
            metadata.update(capture(command, prompt, destination, timeout))
            summary = summarize_trace(destination / "trace.jsonl.gz")
            dump(destination / "trace-summary.json", summary)
            shutil.copytree(workspace / "work", destination / "work")
            metadata["decision_present"] = (destination / "work" / "decision.md").is_file()
            if not metadata["decision_present"] or metadata["exit_code"] != 0:
                STOP_BETWEEN_CASES.set()
        actual_hashes = hashes(workspace / "product")
        metadata["input_mutations"] = {
            key: {"before": initial_hashes.get(key), "after": actual_hashes.get(key)}
            for key in sorted(initial_hashes.keys() | actual_hashes.keys())
            if initial_hashes.get(key) != actual_hashes.get(key)
        }
        metadata["finished_at"] = utc_now()
        dump(destination / "manifest.json", metadata)
        print(f"{utc_now()} DONE {case.name}/{arm}: exit={metadata.get('exit_code')} decision={metadata.get('decision_present')}", flush=True)
    return {k: metadata.get(k) for k in ("case", "arm", "exit_code", "termination_reason", "decision_present", "elapsed_seconds", "input_mutations")}


def evaluate(case: Case, arm: str, output: Path, frozen_skill: Path, native: Path,
             auth_source: Path, defaults: dict[str, Any], run: bool, timeout: int) -> dict[str, Any]:
    try:
        return _evaluate(case, arm, output, frozen_skill, native, auth_source, defaults, run, timeout)
    except Exception:
        # Set this in the worker before the executor can start its next queued job.
        STOP_BETWEEN_CASES.set()
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="Explicitly opt into eight paid/authenticated fresh Codex sessions.")
    parser.add_argument("--output", type=Path, required=True, help="New output directory; existing runs are never overwritten.")
    parser.add_argument("--codex", type=Path, help="Native Codex executable; defaults to the resolved executable on PATH.")
    parser.add_argument("--auth-source", type=Path, default=Path.home() / ".codex")
    parser.add_argument("--timeout", type=int, default=1200, help="Wall timeout per case in seconds.")
    parser.add_argument("--jobs", type=int, choices=(1, 2), default=2)
    args = parser.parse_args()
    output: Path = args.output.resolve()
    candidate = args.codex or shutil.which("codex")
    if candidate is None:
        parser.error("Codex was not found on PATH; pass --codex /path/to/native/codex.")
    native = Path(candidate).resolve()
    auth_source: Path = args.auth_source.resolve()
    if output.exists():
        parser.error("Output directory already exists; choose a new run path.")
    if shutil.which("bwrap") is None or not native.is_file():
        parser.error("bwrap and the native Codex executable are required.")
    host_binary = native.with_name("codex-code-mode-host")
    if not host_binary.is_file():
        parser.error("The native Codex code-mode host must exist beside the native executable.")
    with native.open("rb") as binary:
        if binary.read(4) != b"\x7fELF":
            parser.error("The resolved Codex executable is a launcher, not a native ELF binary. Pass --codex /path/to/native/codex.")
    if args.timeout < 60:
        parser.error("Use a timeout of at least 60 seconds.")
    defaults = configured_defaults(auth_source)
    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    selected_cases = cases()
    output.mkdir(parents=True)
    (ROOT / "evals" / "runs").mkdir(parents=True, exist_ok=True)
    frozen_skill = output / "loaded-skill"
    shutil.copytree(ROOT / "skills" / "long-horizon", frozen_skill,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for case in selected_cases:
        materialize(case, output / "inputs" / case.name)
    dump(output / "grading-private.json", {case.name: [asdict(c) for c in case.criteria] for case in selected_cases})
    shutil.copyfile(Path(__file__), output / "runner-source.py")
    shutil.copyfile(Path(__file__).with_name("fixtures.py"), output / "fixtures-source.py")
    skill_hashes = hashes(frozen_skill)
    manifest: dict[str, Any] = {
        "started_at": utc_now(), "run_models": args.run, "jobs": args.jobs, "model_defaults": defaults,
        "native_codex_path": str(native), "native_codex_sha256": hashlib.sha256(native.read_bytes()).hexdigest(),
        "native_code_mode_host_sha256": hashlib.sha256(host_binary.read_bytes()).hexdigest(),
        "native_codex_version": subprocess.run([str(native), "--version"], capture_output=True, text=True, check=True).stdout.strip(),
        "skill_tree_sha256": aggregate_hash(skill_hashes), "skill_hashes": skill_hashes,
        "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "fixtures_sha256": hashlib.sha256(Path(__file__).with_name("fixtures.py").read_bytes()).hexdigest(),
        "cases": [{"name": case.name, "input_files": len(case.files), "input_bytes": sum(len(s.encode()) for s in case.files.values())} for case in selected_cases],
        "limitations": ["One session per arm/domain; no significance or reliability estimate.",
                        "Fixture-author criteria guide manual inspection; JSON validity and bounded output do not establish correct decisions.",
                        "Offline decision review cannot validate production mutations, scheduling, or actual customer outcomes.",
                        "The OS /usr runtime is visible; repository, grader, other cases, broad /home and host /tmp are not mounted.",
                        "Host networking is retained for model API access; external network restraint is task-level, not kernel-enforced."],
    }
    dump(output / "manifest.json", manifest)
    print(f"Frozen skill tree SHA-256: {manifest['skill_tree_sha256']}", flush=True)
    futures = []
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        for case in selected_cases:
            for arm in ("baseline", "skill"):
                futures.append(executor.submit(evaluate, case, arm, output, frozen_skill, native, auth_source, defaults, args.run, args.timeout))
        results: list[dict[str, Any]] = []
        for future in futures:
            try:
                results.append(future.result())
            except Exception as exc:
                results.append({"runner_error": f"{type(exc).__name__}: {exc}"})
    manifest["finished_at"] = utc_now()
    manifest["results"] = results
    manifest["initial_inputs_archive"] = archive_inputs(output)
    dump(output / "manifest.json", manifest)
    return 1 if any(r.get("runner_error") or r.get("exit_code", 0) not in (0, None) or r.get("input_mutations")
                    or (args.run and (r.get("not_launched") or not r.get("decision_present"))) for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
