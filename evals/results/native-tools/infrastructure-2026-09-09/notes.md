# Infrastructure and pre-execution decisions

All main fixtures and criteria were frozen before the 36-session matrix. The
published treatment is the exact skill tree from commit
`be8d5901028abb11247664cea1e0f3af087e34fd`, extracted from `git archive`. The
candidate was released by the runtime owner and its copied tree hash verified as
`d2fc4f19934888d2b59fae0cbac46eb87b1b43c00033593be2563d5ba22b9b7e`.

Local interface discovery used native help, executable inspection, and isolated
file-access tracing. Codex 0.153.4 and Claude Code 2.1.266 expose fresh print/exec
sessions and JSON traces. Antigravity 1.1.27 exposes print, stream JSON, fresh
projects, and a native file-token fallback when no session bus is present.
Native binaries, versions, model settings, exact commands, and prompts are
recorded in the run manifests and preserved help output.

Antigravity's host auth lives in its unlocked Secret Service item. An attempted
`secret-tool lookup service gemini username antigravity` returned no value; a
read-only Secret Service query located the single matching item. A minimal
credential copy to the path discovered by isolated `strace` authenticated the
native `agy models` command. The adapter never mounts the host session bus or
copies existing projects, conversations, hooks, plugins, or MCP configuration.
Only credential shape/key names were inspected during discovery; values were
never printed or archived.

The initial Antigravity neutral preflight failed before generation because
`--print` consumed `--output-format` as its prompt. The exact stderr and failed
command remain in `../preflight-live-2026-09-09/antigravity`. After a no-model
preparation probe, `--print=<exact prompt>` passed a neutral tool-execution
preflight. Codex and Claude passed their first neutral preflights. There were
three successful neutral model sessions and one additional CLI parsing attempt
with no model generation. No evaluated history or grading material entered these
neutral sessions.

Installed model/effort defaults were retained: Codex selected `gpt-6-astra` with
`xhigh`; Claude selected `claude-fable-5-1[1m]` with no explicit effort setting;
Antigravity's global and CLI settings contained no model/effort preference. Its
native log resolved the fresh-session default to Gemini 3.8 Flash (High). The log's
internal wording “selected model override” describes native default selection;
the evaluator supplied no model or effort flag.

Before any main decision outcome, history density increased from 720 to 2400
linked chains per domain because the installed Claude configuration exposes a
million-token window. The resulting 7,273–7,274 files contain 8.21–8.24MB of raw
text per domain. Raw bytes are a difficulty proxy, not a measured tokenizer size.
Record IDs, record filenames, and receipt/support IDs share an opaque namespace;
brief/current/index names and meaningful subject/cohort cues remain. Calendar
dates were preserved, source paths were checked, and background chains were
interleaved in retained folders. The same five original decision criteria per
domain remained in force. Repeated templates and finite background cohorts are
still synthetic-history limitations.

The no-model matrix archive predates the final receipt-identity normalization;
it is an infrastructure attempt, not a treatment outcome. The live matrix
preserves the exact final fixtures and executed sources. Original preflight
summaries remain unchanged; `preflight-outcomes.json` supplements them using the
correct parser for Antigravity's nested events and usage.

The credential scanner samples installed Codex/Claude files and active temporary
native homes, keeping exact values only in process memory. At completion it
checks raw files, decompressed gzip content, and tar members. The scan report
contains counts and fingerprints only. SQLite conversations and full native
JSONL transcripts are also retained for Antigravity, beyond its concise stdout
tool summaries.


Claude OAuth interruption: the post-PR helper attempt failed before generation with an expired/unrefreshable session. A subsequent isolated native auth-status probe only confirmed local credential presence; expiresAt remained zero, and no supported noninteractive refresh command was advertised. Host auth/config was not modified. Future maintained adapters now copy only claudeAiOauth, excluding unrelated MCP OAuth entries. Earlier executed adapters are preserved; strict MCP isolation prevented their use, and observed credentials were scanned exactly with no matches.
