# Evaluations

Ordinary CI runs the public helper/installation tests and strict mypy checks. It never runs model sessions, needs credentials, or starts a scheduler. Historical research fixtures and their preserved outputs remain under `prototypes/`.

## Real Impulse boundary

```sh
python3 evals/impulse_integration.py --output evals/results/impulse-local
```

Requires the installed Impulse CLI. The command creates a separate `IMPULSE_HOME`, clears any inherited assignment context for operator calls, and uses only a local script assignment. It confirms that a scheduled continuation survives a deliberately failed run and a daemon restart; a fresh process recovers the files, then disables future work. It also checks identical request-ID replay. The fixture waits about twelve real seconds and stops its own daemon afterward. No model, production task, startup configuration, or external notice is used.

Supply a new output directory for each run. Public CLI responses, run identities, source, cleanup diagnostics, and results are preserved. Private scheduler context/database files are excluded from publication. Both the [initial v1 result](results/impulse-v1/result.json) and [final result](results/impulse-v1-final/result.json) passed. Each archive includes the exact executed source; the final run includes independent cleanup attempts and daemon-status verification.

## Fresh-agent recall

The maintained recall runner and independent case definitions compare matched no-skill and full-bundle arms in isolated workspaces. These opt-in sessions consume the installed model harness's allowance. Each domain has roughly 2.5 MB of seeded history, including related actions, observations, corrections, and competing cohorts. This is an offline decision review, not a continuous product rollout.

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
