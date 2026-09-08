# Resumable setup checkpoint — fixture day 7, 2027-01-11

## Reconciled continuation

The fresh session's run context identifies an early checkpoint on day 7. Followed [the recovery record](save-setup-day-0-recovery.md) by looking up the unresolved scheduling key before any dependent action.

[Operation lookup](../evidence/day-7-schedule-operation.json) confirms `weekly-save-setup-d0-observe-14` executed with the original input `{ "key": "weekly-save-setup-d0-observe-14", "day": 14 }`. Its durable receipt is `effect-5`, next_day=14, date=2027-01-18. [Current status](../evidence/day-7-status.json) independently confirms scheduler enabled, lifecycle active, next_day=14. This resolves the earlier unknown scheduling effect; the lost response remains preserved in its original evidence. No schedule retry or replacement was necessary. The early day-7 checkpoint did not cancel the day-14 continuation.

## Current state and evidence

- Status confirms revision 2, `save_setup=true`, `explicit_template=true`, and experiment `weekly-save-setup-d0-deploy` still active with start_day=0. The deployment remains confirmed; it has not been adopted, rolled back or redeployed.
- [Metrics](../evidence/day-7-metrics.json), receipt `measurement-6`, dated 2027-01-11 at revision 2, verify exposure but explicitly report mature=false and minimum_window_days=14. Only 7 fixture days have elapsed since exposure began. Activation is defined as first persisted completed project, excluding draft saves.
- Completed-project activation is 42% control / 49% variant, with a 95% difference interval of [-8, +10] percentage points. Retained use is 31% / 32%, interval [-10, +10] points. Assess these separately: neither interval establishes benefit or harm. The response omits sample sizes, assignment details and the retained-use event/window. Do not treat the repeated rates across checkpoints as independent samples or substitute historical Quickstart evidence.
- [Related work](../evidence/day-7-work.json) confirms revision 2, four other active evaluations and compatible footer accessibility work. Analytics `cohort-metric-review` still requires examining later cohort/measurement corrections before pooling periods. No material configuration interaction or new audit is reported at this checkpoint.
- [Signals](../evidence/day-7-signals.json) repeat the interrupted-setup problem with observation_age_days=7. Their claim that current configuration cannot save drafts conflicts with actual deployed state and verified exposure. Treat this as the original problem signal, not evidence of a failed deployment or observed postdeployment recovery.
- [Usage](../evidence/day-7-usage.json) confirms whole-product project-credit-ledger consumption 8/10, leaving 2 shared validation credits with no reset. No billed validation occurred. All 5 evaluation slots remain active; this experiment retains the previously confirmed reservation `weekly-save-setup-d0-reserve`.

## Decision, actions and next session

Continue the existing controlled evaluation until the already scheduled day-14 observation. The minimum window has not elapsed and available evidence is inconclusive. No new deployment, reservation, validation, settlement, schedule, lifecycle mutation or message was sent this session. Current report_due=false; no pause, termination or owner decision is needed. The ongoing responsibility remains active.

On day 14 (2027-01-18), inspect actual revision, experiment/exposure, related work and any audit before judging outcomes. Require at least 14 days of relevant exposure plus adequate evidence for activation and retained use independently. Preserve source receipts and corrections, avoid combining incompatible windows, and arrange further observation if evidence remains inadequate. Settle only on a supported decision. Finishing this objective does not terminate the ongoing product responsibility.

Historical organization Quickstart correction and unresolved solo-retention recoverability remain as documented in [the initial action record](save-setup-day-0.md) and `history/prior-work/`; this checkpoint provides no evidence resolving that separate historical question. No historical authorization transfers to the present brief.

Saved the current handoff and outbox summary. End this session because the next useful outcome observation requires later fixture time; do not advance time or poll before the confirmed run.
