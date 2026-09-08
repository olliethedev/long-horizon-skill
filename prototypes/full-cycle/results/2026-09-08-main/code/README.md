# THROWAWAY — complete responsibility cycles

Question: does the complete candidate improve useful autonomous work across fresh sessions when deployments, observations, schedules, and interruptions have independently recorded effects?

The candidate lives in `skill/long-horizon/`. It includes setup, standing authority, file-based continuity, evidence and corrections, impact-based coordination, project cost instructions, wait/pause/manual-resume/termination, and reporting. It is not installed or adopted as shared operating instructions.

The controlled service exposes deterministic product state, validation, deployment, metrics, operation lookup, coordination, scheduler, and local reporting operations. Its independent event log is the evidence for actual effects. Matching task facts and interfaces are compared with and without the candidate. Grader truth and service state stay outside agents' instructed workspace access.

Planned coverage: four domains, matching baseline and skill arms, six fresh sessions per chain, loss of an effect acknowledgment, loss of a scheduling acknowledgment, immature observations, changed evidence, and a later revisit with a growing archive. Additional focused probes cover setup, paused access restoration without owner resume, bounded completion/impossibility, and shared capacity. Record failures and incomplete chains with their denominators. Numerical acceptance is not claimed from one matrix.

These are simulated product configurations and fixture observations, not deployed real products. The service action trace is independently captured; filesystem reads and full harness/model isolation may still be unverified. Preserve those limits alongside results. A real elapsed-time Impulse pilot remains separate.

## Run

Prepare fixtures and calibrate deterministic checks without model calls:

```sh
python3 prototypes/full-cycle/evaluate.py
```

Run the full matrix with the installed, authenticated Codex CLI and its configured model defaults:

```sh
python3 prototypes/full-cycle/evaluate.py --agents
```

This runs 48 fresh sessions with up to three evaluating agents at once and consumes model allowance. It does not use a paid external product API. The command prints the temporary workspace root. Inspect its current state without changing it:

```sh
python3 prototypes/full-cycle/inspect.py ROOT
```

`run.py` can continue selected cases/epochs while preserving earlier completed epochs; it stops chains with a failed process for review. `grade.py` and `analyze.py` rescore preserved effects and captured traces without another model call. `archive.py` keeps readable case snapshots and compressed raw evidence. `focus.py` prepares separate setup/lifecycle probes, and `concurrency.py ROOT` checks simultaneous reservations and a fixture-specific cost guard against a running service.
