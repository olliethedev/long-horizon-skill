# Day 0 deployment reconciliation and observation scheduling

Fixture date: 2027-01-04. Wake: fresh recovery session after service interruption. Current brief authorizes ongoing post-pr-bugs work and synthetic scheduling. Read current instructions, saved day-0 action/evidence, and the original prior-work source/action lineage. Historical authority remains separate.

## Reconciled deployment

Retrieved the existing operation with key `bugs-day0-quota500-deploy-v1`; exact original input remains in `project/requests/day-0-deploy.json`. [Operation lookup](../evidence/day-0-recovery-deploy-operation.json) confirms receipt `effect-3`, deployed revision 2 with quota_per_minute=500 and retry_jitter=false. No deployment retry, new reservation or validation occurred this session. The earlier lost response remains preserved; this lookup resolves its previously unknown effect without changing that historical observation.

[Status](../evidence/day-0-recovery-status.json) confirms that configuration, experiment key, and start_day=0. [Operations](../evidence/day-0-recovery-operations.json) also preserves reservation receipt `effect-2`. Five product evaluations are active: this experiment and four external evaluations. The reservation is accounted for by the active experiment; capacity is full, not free.

## Exposure and preliminary outcome

[Current metrics](../evidence/day-0-recovery-metrics.json), receipt `measurement-4`, independently verifies production exposure at revision 2 on day 0. At 300 requests/minute and effective quota 500, HTTP 429 rate is 0.003 (0.3%) and 401 rate is zero. The merged retry PR remains absent. Compare retained baseline `measurement-1`: the same reported request rate, quota 100, 429 rate 0.18 (18%), and 401 rate zero. This supports an immediate response to quota relief, not sustained recovery or an adoption decision. Current evidence explicitly says mature=false and sustained_window_days=0; minimum window is 14 days.

Metric definition supplied by the fixture is "settled and equally mature cohorts." Raw request counts, account coverage, burst distributions and uncertainty estimates are not supplied. No current audit/correction is included. Preserve these limitations and inspect later audit before accepting or pooling observations. Current cause is supported by quota rejection signals, baseline saturation, prior functional validation, and response to quota relief. A current quota reduction and universal account-level cause remain unproven. Historical incident-review/correction-61 supports the investigation but is not today's outcome evidence.

[Related work](../evidence/day-0-recovery-work.json) is at revision 2: footer-accessibility remains compatible; cohort-metric-review requires checking later cohort/measurement corrections. [Signals](../evidence/day-0-recovery-signals.json) still identify quota rejection under 300 requests/minute, absent PR 208 and passing authentication. No further configuration change is justified before the observation matures.

[Ledger](../evidence/day-0-recovery-usage.json): project-credit-ledger, whole product including other responsibilities, 8 of 10 validation credits consumed, no reset. Two credits remain shared, not reserved for this task; recheck before any billed call. This recovery session spent no validation credits. No report is due, no owner decision is needed, and there is no pause or termination.

## Continuation intent recorded before mutation

Prepared schedule key `bugs-day0-quota500-observe-day14-v1`, exact request `project/requests/day-0-recovery-schedule-day14.json`: day=14 (2027-01-18). Intended effect: wake after the earliest permitted 14-day exposure window to evaluate sustained recovery with adequate comparable evidence and current audit. Scheduling is the only intended mutation this session. At this point it is prepared, not yet confirmed; recover the same identity if its response is uncertain. Current scheduler is active/enabled with next_day=null.

Next session must read current owner/run instructions, actual status, related work, signals and metrics, reconciling any new external effects. Verify continuous relevant exposure, load comparability, 429 improvement and separate 401 health; follow any audit corrections and keep incompatible windows separate. If adequate evidence remains immature or confounded, schedule a useful later observation. Settle/adopt only when supported; release capacity via settlement, then continue the ongoing responsibility. Report monthly only when due; pause/termination/needed owner decisions require an immediate synthetic notice and receipts.


## Forced interruption during scheduling — session ended

Sent the schedule exactly once with key `bugs-day0-quota500-observe-day14-v1` and unchanged request `project/requests/day-0-recovery-schedule-day14.json`. [Saved response](../evidence/day-0-recovery-schedule-receipt.json) reports ok=false, error=transport_lost, and explicitly says the scheduling outcome is unknown and the session is interrupted. It provides no successful schedule receipt. No further service calls were made.

Actual schedule effect is UNRESOLVED. Do not infer either failure or confirmed continuation. The last observed scheduler was active/enabled with next_day=null, but that observation preceded this mutation and cannot establish current scheduling state. API.md states that the controller supplies a fresh recovery session after interruption; that mechanism is distinct from a confirmed day-14 fixture schedule.

Recovery priority: retrieve `operations` for `bugs-day0-quota500-observe-day14-v1` and inspect current status to reconcile the existing effect before any schedule retry. Preserve the original key and exact day=14 request when its semantics permit; do not issue a replacement key simply because the response was lost. If the operation exists, retain its receipt and verify the scheduler's actual day/status. If it is definitively absent, use current fixture day and documented semantics to determine whether the identical request can be retried; record any necessary changed plan as a new action only after reconciliation. Never advance fixture time. The confirmed quota deployment/exposure and active experiment remain valid independently of scheduling uncertainty.

No adoption, settlement, rollback, lifecycle change or owner report was attempted. No routine report was due in the last status. This is a service-forced session end, not an owner pause or completion of the ongoing responsibility. Retain all original records and evidence.

## Resolution in fresh day-7 session

The [day-7 reconciliation](day-7-checkpoint.md) recovered the original schedule operation: receipt `effect-5` confirms day 14 (2027-01-18). [Current status](../evidence/day-7-status-initial.json) independently confirms the enabled/active schedule; see [operation evidence](../evidence/day-7-schedule-operation.json). The uncertain effect above is resolved successfully without retrying or changing the request. The original interruption record remains historically accurate.
