# Evaluations

CI runs deterministic tests and strict mypy. Model evaluations are explicit opt-ins and consume the selected harness's allowance.

## Results

- [Complete workflow](results/workflow-value/REPORT.md): autonomous follow-ups with agent-created history and a simulated product service.
- [Native file tools](results/native-tools/REPORT.md): matched decisions over large histories, with and without the history helper.
- [Historical v1 recall](results/v1-recall/REPORT.md): the earlier helper-based comparison.
- [Local Impulse integration](results/impulse/REPORT.md): real scheduling, recovery and shutdown without model calls.
- [Workflow preparation](results/workflow-preparation/REPORT.md): fixture reachability and isolation checks.

Publish concise findings only. Raw workspaces, transcripts, copied sources, detailed reviews and one-off analysis belong in ignored `evals/runs/` or a local backup.

## Ordinary checks

```sh
.venv/bin/python -m mypy
python3 -m unittest discover -s tests
python3 evals/workflow_calibrate.py
```

## Workflow comparison

Read [the method](../docs/workflow-value-study.md) and `workflow_rubric.json` before running or grading. The service models revenue, weekly product improvement, customer feedback and post-PR monitoring. Each session starts fresh; retained files and confirmed schedules provide continuity.

```sh
# Preflight only: checks native setup and isolation, with no model launches.
python3 evals/workflow_runner.py --output evals/runs/workflow-preflight-NEW
```

Adding `--run` launches the selected model matrix. The full default is 24 trajectories with up to eight sessions each (192 attempts), at most two concurrent processes; `--harness codex` selects eight trajectories (64 attempts). Agree the scope and allowance before using it. Use a new output directory, retain failed attempts and never rerun a generated decision to improve its score.

The [native harness guide](NATIVE_TOOLS.md) documents the separate retrieval and setup evaluations. They use installed Codex, Claude Code and Antigravity defaults with isolated temporary authentication homes. No production product or live owner task belongs in an evaluation workspace.

## Impulse boundary

```sh
python3 evals/impulse_integration.py --output evals/runs/impulse-NEW
```

This uses a separate `IMPULSE_HOME` and script assignment, waits about twelve real seconds, checks recovery and request replay, and stops its own daemon. It launches no model session.

## Grading

Inspect useful work, actual effects, constraints, original evidence, corrections, continuity and final claims. Correct formatting, process exit status and low token usage are not semantic success. Report incomplete cases separately; sessions in one trajectory are not independent experiments. Preserve unknown dates and causal uncertainty, and distinguish synthetic evidence from real production outcomes.
