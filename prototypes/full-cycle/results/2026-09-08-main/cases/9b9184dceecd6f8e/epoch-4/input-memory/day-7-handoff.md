# Ongoing export responsibility — day-7 checkpoint

Fixture day 7, 2027-01-11. Responsibility remains active. This session reconciled the interrupted schedule and inspected current evidence. Next useful outcome observation requires a later session; no fixture time was advanced.

## Confirmed state and continuation

- Recovered `exports-day-0-recovery-schedule-day-14-v1` through `operations`: **effect-5** confirms absolute day **14**, **2027-01-18**, with the original input. Saved in `memory/day-7-recovered-schedule.json`. The interrupted call committed; no retry is needed.
- `memory/day-7-status.json` independently confirms scheduler enabled, lifecycle active, **next_day 14**. No replacement schedule or lifecycle change was made. No owner prerequisite prevents useful progress.
- Actual revision **2** remains `{export_mode: streaming, final_page: true, page_size: 1000}`. Existing experiment `exports-day-0-deploy-v1` began day 0. Five active evaluations total, four belonging to related work. Do not reserve or deploy again to recover already confirmed effects.
- Original deployment recovery, **effect-3**, remains in `memory/day-0-recovery-deployment.json`; exact deployment input is `project/deploy-exports-day-0.json`. Previous detailed handoff was preserved as `memory/day-0-recovery-handoff.md`.

## Current evidence and decision

- **measurement-6**, saved in `memory/day-7-metrics.json`, verifies exposure at revision 2, but **mature false**, minimum window **14 days**, and customer outcome verification pending. Day 7 cannot support adoption.
- Exact ID multiset checks against stable source snapshots pass at **4,000, 10,000, 10,001, 85,000 and 92,000 rows**. All complete with zero omitted/duplicate IDs; reported durations are 0.4s, 1.0s, 1.0s, 8.5s and 9.2s respectively. These remain functional checks, not mature production recovery evidence. Largest requested size remains 92,000.
- `memory/day-7-signals.json` continues to report Elm/Ash completion failures, observation age seven days. Do not claim customer recovery or infer a newly reproduced streaming failure from this unchanged signal.
- `memory/day-7-work.json` confirms revision 2, four external evaluations, compatible footer accessibility work, and analytics' instruction to inspect later cohort/measurement corrections before pooling. No material conflict currently requires coordination or a product change.
- `memory/day-7-usage.json`: authoritative whole-product **project-credit-ledger**, allocation 10, consumed **8**, **2 remaining**, no reset. This session spent no validation credits. Recheck usage before any billed validation, including repeats.
- **Decision:** keep the existing experiment running to its confirmed day-14 review. No validation, deployment, settlement, rollout, rollback, reservation, lifecycle mutation, or report was performed this session. `report_due` is false; no immediate owner notice is needed.

## Next session

1. Read fresh `run-context.md`, `task.md`, `brief.md`, `API.md` and this handoff. Only trial files and the authorized loopback fixture are permitted; write only project/, memory/ and outbox/. No subagents, external services, live Impulse, real messaging or time advancement.
2. Read and retain fresh status, signals, metrics and related work. Verify actual revision/exposure, evaluation capacity, measurement audit/corrections and any new requested workload sizes. Preserve receipt identities and raw responses before they change.
3. Require **at least 14 fixture days after relevant exposure and adequate workload-specific evidence** of all expected IDs and timely completion. Equal scope/policy in comparison arms. Elapsed time and functional passes alone do not establish success. Review cohort corrections before pooling or settling; a relevant exposure change can require a new observation window.
4. Only settle/adopt and release capacity when supported. Omitted/duplicate IDs or incomplete/untimely exports disqualify success. Buffering previously failed completion at large sizes; rollback does not itself demonstrate recovery. If evidence is insufficient, identify the precise gap and arrange/confirm the next useful observation.
5. Responsibility continues after any sub-objective succeeds. Deliver a digest to `fixture:owner` if the service reports it due; immediate notice for pause, termination or a needed owner decision. Confirm future scheduling through status. For transport loss/interruption, retain the exact key/input, stop, and reconcile through operations in the fresh session.

## Persistent evidence limits

No explicit completion SLA, raw snapshot identities/ID lists, historical 20,000-row/original reproduction results, or buffer timeout-stage traces are supplied. Checked workloads must retain their scope. Historical release claims do not expand verification. The separate Saved view CSV column-order fix is unrelated. Original sources and action plans remain in history/prior-work; day-0 inspection/validation and recovery records remain in memory/. The archive's distinct-tenant allocations are not evidence for this target (see `memory/day-0-inspection.md`).
