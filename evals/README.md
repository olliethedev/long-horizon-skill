# Evaluations

Ordinary CI runs bundle installation and exported-evidence checks, plus strict mypy. It never runs model sessions, needs credentials, or starts a scheduler. Historical research fixtures and their preserved outputs remain under `prototypes/`.

## Complete-workflow value study

The [study protocol](../docs/workflow-value-study.md) declares a comparison beginning with an ordinary owner request, empty agent-authored memory, actual service effects and confirmed scheduling across fresh native sessions. The [capped study report](results/workflow-value/REPORT.md) retains the 50-attempt allowance, completed revenue pairs, partial weekly-product coverage and interruption evidence. No outcome advantage is demonstrated in the complete pairs. The runtime skill remains unchanged; earlier studies remain separate evidence.

`workflow_continue.py` is the one-time four-slot continuation of the interrupted 46-attempt campaign, not a general scheduler or runtime dependency. Its recorded recovery consumes only unspent slots and never repeats the interrupted decision. `workflow_summary.py` derives session counts and native effort from the linked archives; `workflow_publish.py` scans and verifies the published evidence. None assigns semantic grades automatically. Do not rerun archived generated decisions or treat the original 192-attempt plan below as the final allowance.

```sh
# Mechanical fixture calibration only; no models, credentials or live services.
python3 evals/workflow_calibrate.py

# Isolated preparation for 24 trajectories; reads native authentication for setup but launches no models.
python3 evals/workflow_runner.py --output evals/runs/workflow-preflight-NEW
```

After choosing the evaluation-session allowance and freezing the protocol, add `--run` for the model comparison. The full scope is four domains, three harnesses and two treatments, with at most eight fresh launches per trajectory (192 total). Add `--harness codex` for eight trajectories (64 total). At most two native processes run concurrently. Use a new output directory; preserve failures and do not repeat completed decisions for a better score. Read the protocol and `workflow_rubric.json` before reviewing results: deterministic calibration establishes fixture reachability, not agent performance or semantic success.

## Native harness comparison

The [native harness guide](NATIVE_TOOLS.md) describes the current 36-session comparison: Codex, Claude Code, and Antigravity; no skill, the frozen published helper bundle, and the revised native-tools bundle; four domains with over 7,200 files each. It includes opt-in commands, authentication requirements, isolation boundaries, preserved artifacts, and grading rules. The distributed skill contains no evaluation programs.

Three separate setup smoke probes exercise an established suitable scheduler (Codex), a reminder-only tool (Claude), and a missing scheduler (Antigravity), using the revised skill:

```sh
# Prepare offline source snapshots and check isolation without model calls.
python3 evals/setup_probes.py --output evals/results/native-tools/setup-dry-RUN

# Run three fresh sessions, at most two concurrently.
python3 evals/setup_probes.py --run --output evals/results/native-tools/setup-live-RUN
# If one login is unavailable, run only the other assigned cases; complete it later in a new output.
python3 evals/setup_probes.py --run --harness codex --harness antigravity --output evals/results/native-tools/setup-available-RUN
```

These probes supply captured tool inventories and help text. They test setup reasoning, preserve existing owner answers, and prohibit installation or registration. Each scenario is exercised by one harness; this is neither a matched harness comparison nor a test of live scheduler discovery. The same native harness requirements and artifact isolation apply. Use a new output path; the default per-session timeout is 600 seconds, adjustable with `--timeout 30..3600`.

## Real Impulse boundary

```sh
python3 evals/impulse_integration.py --output evals/results/impulse-local
```

Requires the installed Impulse CLI. The command creates a separate `IMPULSE_HOME`, clears any inherited assignment context for operator calls, and uses only a local script assignment. It confirms that a scheduled continuation survives a deliberately failed run and a daemon restart; a fresh process recovers the files, then disables future work. It also checks identical request-ID replay. The fixture waits about twelve real seconds and stops its own daemon afterward. No model, production task, startup configuration, or external notice is used.

Supply a new output directory for each run. Public CLI responses, run identities, source, cleanup diagnostics, and results are preserved. Private scheduler context/database files are excluded from publication. Both the [initial v1 result](results/impulse-v1/result.json) and [final result](results/impulse-v1-final/result.json) passed. Each archive includes the exact executed source; the final run includes independent cleanup attempts and daemon-status verification.

## Earlier Codex recall runner

The earlier recall runner and independent case definitions compare matched no-skill and current full-bundle arms in isolated Codex workspaces. These opt-in sessions consume the installed model harness's allowance. Each domain has roughly 2.5 MB of seeded history, including related actions, observations, corrections, and competing cohorts. This is an offline decision review, not a continuous product rollout. A new run loads the current bundle; the original helper comparison's exact loaded bytes remain in its result archive.

```sh
# Materialize cases and check isolation without model calls.
python3 evals/recall.py --output evals/results/recall-preflight

# Explicitly run eight fresh sessions, at most two concurrently.
python3 evals/recall.py --run --output evals/results/recall-local --jobs 2
```

The runner requires Linux, `bwrap`, Python 3.11+, `rg`, native Codex with its sibling `codex-code-mode-host`, and an existing Codex file-authenticated home. It resolves `codex` on PATH; if that is a launcher, supply `--codex /path/to/native/codex`. `--auth-source` selects the existing configuration/authentication directory. Even the no-model preflight checks this setup. The recorded model and reasoning defaults come from that configuration. Other hooks, integrations, memory, and agents are disabled for isolation.

Use a new output directory for each attempt. Each session has a temporary credential home that is excluded from artifacts and removed afterward. Product inputs and the candidate skill are mounted read-only; the repository, grader, other cases, and host home are absent. Host networking remains available for the model API, so external-network restraint is an instruction, not kernel enforcement. Raw source snapshots, exact prompts, loaded skill bytes, executed runner/fixture sources, model configuration, traces, decisions, and boundary checks are retained. Read `grading-private.json` outside the evaluated session to manually inspect each decision against its source evidence; the runner's exit status reports execution, not semantic success.

The default per-case wall limit is 1,200 seconds, with 32 MB retained per stdout/stderr stream. An execution failure or missing decision stops queued cases; active cases finish. SIGINT/SIGTERM also stop between cases. Interrupted and infrastructure-failed attempts remain part of the record.

The [v1 results and manual review](results/v1-recall/REPORT.md) retain the four-domain comparison, usage and retrieval measurements, infrastructure attempts, and the separate follow-up after the cursor-integrity fix. The original comparison's loaded bundle remains unchanged; the follow-up records the final bundle separately.

Scores must distinguish original actions from corrected interpretations, relevant conditions from similarly named cohorts, and unknown request dates from known deployment dates. Bounded output, correct JSON, or a process exit code is not a semantic success criterion. Preserve failed and incomplete sessions, oversized retrieval, and unsupported conclusions.
