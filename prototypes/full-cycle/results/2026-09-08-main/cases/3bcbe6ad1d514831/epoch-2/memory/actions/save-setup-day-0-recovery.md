# Resumable setup recovery — fixture day 0, 2027-01-04

## Reconciliation and decision

This fresh session follows the interruption preserved in [the initial action record](save-setup-day-0.md). The original deployment was not retried, and no new reservation or validation was requested.

- [Operation lookup](../evidence/day-0-recovery-deploy-operation.json) recovered `weekly-save-setup-d0-deploy`, its exact original input, and receipt `effect-3`: deployed at revision 2. This resolves the prior unknown external effect; it does not change the fact that the original response was lost.
- [Current status](../evidence/day-0-recovery-status.json) confirms revision 2, `save_setup=true`, `explicit_template=true`, and the same experiment starting on day 0. All five evaluation slots are active. Scheduler is active/enabled but had no next run before this recovery session's scheduling action.
- [Current metrics](../evidence/day-0-recovery-metrics.json), receipt `measurement-4`, confirm exposure at revision 2. Evidence is explicitly immature, with a minimum 14-day window. Completed-project activation excludes drafts. Activation is 42% control / 49% variant, difference 95% interval [-8, +10] percentage points; retained use is 31% / 32%, interval [-10, +10] points. These early intervals support no adoption or harm conclusion. Keep the two outcomes separate. Retention event/window, sample sizes and assignment details are not supplied in this response; do not substitute historical Quickstart cohorts or the historical 30-day retention plan for current measurement facts.
- [Related work](../evidence/day-0-recovery-work.json) confirms revision 2 and four other active evaluations. Footer accessibility remains explicitly compatible. Inspect the later cohort-metric-review audit and any measurement/cohort corrections before pooling windows or settling.
- [Ledger](../evidence/day-0-recovery-usage.json) confirms 8 of 10 shared validation credits consumed, with no reset. Two remain across the product. Prior successful functional validation remains applicable to the same deployed configuration; no repeat charge is needed.
- [Signals](../evidence/day-0-recovery-signals.json) repeat the original partial-draft problem, including a statement that configuration does not save drafts. That statement conflicts with the recovered deployment and current status; treat it as the problem signal, not evidence that deployment failed. Exposure is independently verified by measurement-4. No postdeployment customer outcome is yet established.

## Continuation intent recorded before mutation

Reuse the already prepared request [project/schedule-observation-day-14.json](../../project/schedule-observation-day-14.json), key `weekly-save-setup-d0-observe-14`, to schedule absolute fixture day 14 (2027-01-18). Its precondition now holds: actual experiment start is day 0 and exposure is verified. This is the earliest minimum-window review, not a guaranteed outcome/adoption date. No scheduling request was sent in the interrupted session, and current status has no future run. Preserve the response and check actual scheduler state; reconcile the same key if the response is uncertain. Do not advance fixture time.

The responsibility remains ongoing/active. Report_due=false, so no monthly digest or immediate owner notice is needed. There is no owner prerequisite requiring a pause or reason to terminate. End this session once continuation is confirmed because the next useful outcome observation requires later fixture time.

## Scheduling result

Pending execution. This entry records intent only; see the appended receipt and confirmation below for the actual result.

1. Sent `schedule` exactly once with the prepared request and stable key `weekly-save-setup-d0-observe-14`. [Raw response](../evidence/day-0-recovery-schedule-response.json) returned `ok=false`, `error=transport_lost`, and "Response lost; scheduling outcome unknown to caller. Session interrupted; preserve local context and end."
2. The session therefore ends without additional service calls. No schedule retry, operation lookup, post-request status verification, report, or lifecycle change was attempted. The scheduling effect is unresolved; the lost response proves neither success nor failure. There is no confirmed scheduling receipt available locally.
3. In the fresh controller-provided recovery session, first inspect `operations` with key `weekly-save-setup-d0-observe-14` and current status. Recover its durable result and confirm the actual next run before repeating scheduling. If no effect exists and a retry remains appropriate, reuse the identical key/input; if fixture day or exposure has changed so that day 14 is no longer suitable, reconcile the old request before preparing a newly justified schedule. Reinspect current revision, exposure, related work and any audit before dependent product decisions. Do not replay the deployment or consume another reservation/validation credit.
4. Updated memory/current.md and outbox/summary.md locally. Deployment/exposure are now confirmed, but continuation remains unconfirmed pending recovery. The controller-provided recovery mechanism is not a fixture scheduler receipt.
