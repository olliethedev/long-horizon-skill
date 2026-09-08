# THROWAWAY — complete responsibility cycles

Question: does the complete candidate improve useful autonomous work across fresh sessions when deployments, observations, schedules, and interruptions have independently recorded effects?

The candidate lives in `skill/long-horizon/`. It includes setup, standing authority, file-based continuity, evidence and corrections, impact-based coordination, project cost instructions, wait/pause/manual-resume/termination, and reporting. It is not installed or adopted as shared operating instructions.

The controlled service exposes deterministic product state, validation, deployment, metrics, operation lookup, coordination, scheduler, and local reporting operations. Its independent event log is the evidence for actual effects. Matching task facts and interfaces are compared with and without the candidate. Grader truth and service state stay outside agents' instructed workspace access.

The [reviewed main matrix](NOTES.md) completed 48 fresh sessions: four domains, matching baseline and skill arms, six sessions per chain, lost effect and scheduling acknowledgments, immature observations, changed evidence, and a later revisit with a growing archive. Additional focused probes cover setup, pause/manual resume, bounded completion/impossibility, and shared capacity. Original outputs and failures remain preserved. Numerical acceptance is not claimed from one matrix.

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

For the focused probes, `python3 prototypes/full-cycle/focus.py` prints a new root. Start `service.py ROOT` in a separate terminal, then run:

```sh
python3 prototypes/full-cycle/run.py ROOT --epochs 0 --concurrency 3
python3 prototypes/full-cycle/resume.py ROOT
python3 prototypes/full-cycle/run.py ROOT --cases 7202704d67026be1 --epochs 1 --concurrency 1
```

The first command consumes four fresh model sessions; the last consumes one. `resume.py` supplies the explicit synthetic owner instruction only after the first batch ends. It does not enable the task itself. Review lifecycle results against `REVIEW.md`; the main grader's useful-configuration predicate is not appropriate for bounded impossibility or unapproved setup.

`recheck.py SOURCE_ROOT` prepares a separate weekly final-session fork from original day-240 records. Start a new service for the printed root, then `run.py ROOT --epochs 5 --concurrency 2` executes two fresh sessions. This was used to separate an original fixture inconsistency from the stale-handoff test. The original main outcomes remain in the archive. Current calibration includes a regression check for the corrected endpoint, added after the original seven calibration groups.

Keep total evaluating processes across simultaneous runs within the intended concurrency. Stop each local fixture server when its run ends. No command here installs the skill or modifies real Impulse tasks.
