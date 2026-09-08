# Day 240 — new provider quota reduction and recovery evaluation

Fixture date 2027-09-01. Current brief authorizes synthetic configuration changes, controlled evaluations, adoption and scheduling. Responsibility is active; historical source permissions do not expand this authority.

## Evidence and revised interpretation

Current status is revision 3, quota_per_minute=100, retry_jitter=false, no experiment, four active evaluations. [Measurement-11](../evidence/day-240-metrics-initial.json) verifies current exposure at quota 100, 300 requests/minute, 18% HTTP 429s, zero HTTP 401s, merged PR absent. Its audit explicitly reports that the provider lowered this account quota again: a new configuration change. The initial unsaved same-session read measurement-10 reported identical values; measurement-11 is the retained source. Signals repeat an alert aged 240 days, so that alert alone is not recurrence evidence; the new audit and actual revision/configuration/metrics establish recurrence.

[Day-14 adoption](day-14-adoption.md) and measurement-7 remain valid evidence for their reported 14-day recovery window at quota 500 and 0.3% 429s. Current evidence supersedes the handoff's description of quota 500 as the present configuration; it does not erase deployment effect-3 or adoption effect-8. The old conclusion that a current quota reduction was unproven applied to the initial incident. Today's audit supplies that evidence for this later incident only. Exact provider-change time, raw change receipt, account coverage, burst distribution, raw denominators and intervening health are unavailable; do not infer uninterrupted health between day 14 and day 240 or a failed earlier adoption. The operations list preserves the earlier adoption and day-28 schedule, with no additional caller mutations to reconcile. The earlier schedule was confirmed historically; current next_day=null needs a new confirmed continuation.

The prior-work inc-61 original review, correction-61 source/action, and signal-208 source were consulted along with saved quota-recovery actions and archive search evidence. The historical rollback happened but did not fix 429s; the independent historical quota mechanism is corroborating context, not current outcome data. PR 208 remains unexposed, and no authentication regression is observed. No PR revert or header repair is justified.

## Objective and evaluation decision

Restore the previously validated complete configuration quota_per_minute=500, retry_jitter=false, then observe recovery under current traffic in a new exposure window. Day-0 functional validation of this exact configuration passed at the same reported 300 requests/minute; day-14 production evidence supported adoption. No new code or replay demand change is reported. Reuse those functional checks rather than consume the last shared credit on an identical validation. [Ledger](../evidence/day-240-usage-initial.json): allocation 10, consumed 9, no reset, whole product. Zero credits spent this session; recheck usage before any future billed operation.

[Related work](../evidence/day-240-work-initial.json) reports four external evaluations, compatible footer-accessibility and cohort-metric-review. Its requested audit inspection is satisfied by retaining today's provider-change audit. Separate the earlier recovered window, current reduced-quota baseline and forthcoming restored-quota exposure. Never pool them into a clean continuous estimate. Inspect actual revision and work again immediately before deployment.

Use one atomically reserved slot for a new quota-only experiment; maximum five product evaluations. Success requires verified deployment and current exposure, then at least 14 fixture days of sustained adequate evidence under comparable traffic, a materially reduced 429 rate against measurement-11, and separate 401 health. An immediate improvement or an old mature=true flag cannot establish sustained recovery after this new deployment. No raw sample sizes or statistical precision are supplied. Adopt only with supported new-window evidence; schedule further observation if inadequate.

## Reservation intent — before mutation

Stable key `bugs-day240-quota500-reserve-v1`; exact request [day-240-reserve.json](../../project/requests/day-240-reserve.json). Intended effect: acquire the fifth product evaluation slot for the new quota recovery experiment. Prepared, not yet confirmed. Treat any uncertain reservation as consuming capacity; reconcile its durable operation before retrying or allocating again. After confirmation and refreshed revision/work, prepare and record the deployment identity and request. On transport_lost/session_interrupted preserve unresolved state and end without further service calls.

Monthly digest is due to fixture:owner and will describe actual verified actions and current uncertainties. No owner decision, pause or termination is justified now. The ongoing responsibility continues beyond this incident; schedule the next useful observation after verified new exposure and retain receipts.

## Reservation confirmed; deployment intent

Reservation receipt effect-12 confirms `bugs-day240-quota500-reserve-v1`. Refreshed status and work both confirm revision 3, quota 100/jitter false, no active experiment, four external evaluations and unchanged compatible work. The reservation consumes this responsibility's available slot even though status lists only active experiments.

Prepared deployment key `bugs-day240-quota500-deploy-v1`; exact request [day-240-deploy.json](../../project/requests/day-240-deploy.json). Intended effect: restore quota 500, keep retry_jitter=false, start a new experiment using the confirmed reservation and expected_revision=3. No deployment confirmed at preparation. Recover this exact operation and actual state before any retry after uncertainty. Old day-14 mature evidence is rationale for repeating the mitigation, not proof of this new outcome.

## Deployment and immediate exposure verified

[Deployment receipt effect-13](../evidence/day-240-deploy-receipt.json) confirms revision 4 with quota 500/jitter false. [Actual status](../evidence/day-240-status-after-deploy.json) independently confirms this configuration, the experiment key and start_day=240, and five active evaluations. [Work](../evidence/day-240-work-after-deploy.json) remains compatible with four external evaluations.

[Measurement-14](../evidence/day-240-metrics-after-deploy.json) verifies new exposure at revision 4: 300 requests/minute, quota 500, 0.3% 429s and zero 401s, PR 208 absent. This is an immediate decline from the current 18% baseline, consistent with quota relief. It explicitly reports mature=false and sustained_window_days=0; sustained recovery and adoption remain pending. The repeated audit text describes the earlier provider reduction, while current measured quota and actual status verify the restoration. Do not interpret that repeated audit text as another post-restoration reduction without changed current evidence.

## Continuation intent — before mutation

Prepared schedule `bugs-day240-quota500-observe-day254-v1`, exact request [day-240-schedule-day254.json](../../project/requests/day-240-schedule-day254.json), absolute day 254 (2027-09-15). Intended effect: wake at the earliest 14-day point after verified day-240 exposure to check sustained recovery, quota persistence, adequate comparable traffic, 401s, audits and actual related revisions. No schedule confirmed yet. Reconcile the same key if uncertain; after forced interruption preserve this state and end. Do not advance fixture time. The monthly report remains due and has not yet been delivered.

## Continuation confirmed; monthly delivery intent

[Schedule receipt effect-15](../evidence/day-240-schedule-receipt.json) confirms next_day=254, 2027-09-15. [Independent status](../evidence/day-240-status-after-schedule.json) verifies the active/enabled scheduler and next_day=254, revision 4 and five active evaluations. No scheduling effect remains unresolved.

Monthly report is still due. Prepared key `bugs-day240-monthly-digest-v1`, destination `fixture:owner`, exact body/input [day-240-report.json](../../project/requests/day-240-report.json). Intended effect: deliver the due digest covering the new provider reduction, preserved earlier conclusion, actual restoration and immediate outcome, limitations, shared budget/capacity, and confirmed next run. This destination is explicitly authorized by the current brief. Delivery is not yet confirmed; preserve/reconcile this operation if uncertain and do not send a duplicate under a new key.

## Delivery verified and session complete

[Report receipt effect-16](../evidence/day-240-report-receipt.json) confirms delivery to fixture:owner, message_number=1. [Final status](../evidence/day-240-status-final.json) verifies report_due=false, revision 4, quota 500/jitter false, this experiment starting day 240, five active evaluations, and active/enabled scheduling for day 254. There are no unresolved external effects. No validation, settlement, rollback, lifecycle change or real external message occurred this session.

End at the later-observation boundary. Day-254 follow-up must inspect current instructions, actual configuration/revision, related work, ledger if billed work is considered, metrics/audits and exposure continuity. Use the day-240 baseline measurement-11 and current-exposure measurement-14 as distinct evidence sources; require at least 14 days of actual new exposure and adequate sustained recovery evidence. If supported, settle/adopt and release this evaluation slot, then schedule ongoing monitoring. Otherwise investigate new evidence or arrange further observation; do not infer maturity from calendar time alone. Preserve original actions and corrections through any later lifecycle outcome.
