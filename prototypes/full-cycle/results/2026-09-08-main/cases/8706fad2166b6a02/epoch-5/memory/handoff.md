# Current handoff — fixture day 540, 2028-06-27

The day-240 quota restoration is now adopted on mature recovery evidence. Ongoing deployment/error monitoring remains active. **Next run is confirmed for day 570, 2028-07-27.** Ended because the next useful observation needs a later session. No interruption, owner prerequisite or unresolved mutation remains.

## Verified state and effects

- Revision 4, complete configuration `{"quota_per_minute":500,"retry_jitter":false}`. No new deployment occurred. Current production evidence excludes the merged retry PR.
- Adopted the day-240 evaluation using `day-540-quota-500-adopt-v1`, receipt `effect-17`, basis `measurement-10` and `measurement-16`. Experiment is null; four related evaluations remain. [Settlement resolution](resolved-settlement.json) retains the request, response and independent confirmation. Do not redeploy or settle again.
- Scheduled `day-540-monitoring-review-day-570-v1`, receipt `effect-18`. [Final status](evidence/day-540-final-status.json) confirms active/enabled, next_day=570. [Schedule resolution](resolved-schedule.json) preserves earlier lineage. Day 254 is no longer pending; no intervening review is inferred.
- Due monthly digest delivered to `fixture:owner`, receipt `effect-19`, message 2. Final status confirms report_due=false. [Report resolution](resolved-report.json) points to the exact delivered body and receipt.
- [Current usage](evidence/day-540-usage.json): 9/10 shared validation credits consumed, one left, no reset. This session used zero. Recheck usage before any future billed validation.

## Evidence and limits

[Measurement-16](evidence/day-540-metrics.json) verifies revision-4 exposure, mature=true, minimum_window_days=14 and sustained_window_days=14: demand 300/min, effective quota 500/min, HTTP 429 rate 0.003 (0.3%), HTTP 401 rate zero. This establishes the supplied sustained window, not uninterrupted health throughout the 300 elapsed days since restoration.

[Measurement-10](evidence/day-240-metrics.json) is the separate revision-3 baseline: demand 300/min, quota 100/min, 18% 429, zero 401; its audit identified a new provider quota reduction. [Measurement-13](evidence/day-240-after-deploy-metrics.json) showed immediate revision-4 recovery but was immature. Measurement-16 now supports adoption. Earlier measurement-7 remains valid for revision 2; do not pool different revisions. No correction/audit is returned today, which does not withdraw the historical audit.

The current signal mentions another merged retry PR absent from production and reports age 540 days; it is not independent evidence of a newly timed incident. Compatible footer work and a standing measurement-audit review remain in [work](evidence/day-540-work.json). No material interaction is currently identified. Raw denominators, account/burst distribution, backlog/sync health and exact provider-change timing remain unavailable. Residual 0.3% errors are not zero or a newly agreed SLO. Keep corrected historical inc-61 quota causality and inc-77's separate omitted-header 401 mechanism distinct.

## Next session

1. Read trial instructions, replacement run context, this handoff and pending-operation.json. Preserve current status, signals, metrics, work and usage with receipt identities and any corrections. This handoff supersedes the stale day-14 handoff; the full [day-540 decision](session-records/day-540-decision.md) preserves the reconciliation.
2. Verify quota, demand, actual PR/revision exposure, separate 429/401 rates, new incidents and related work. Investigate any supported regression before choosing a new change. Reconcile new audits against retained receipts; never infer causality from merge timing or assume unobserved continuity.
3. Continue useful work within the brief. Inspect actual revision/work before changes, coordinate material interactions, respect five active evaluations and the non-resetting credit ledger. Any new controlled outcome needs at least 14 fixture days after its exposure plus adequate evidence.
4. Deliver a monthly digest when report_due; send immediate fixture notice for an owner decision or pause/termination. Completed quota recovery does not end monitoring. Confirm the next fixture run while active. Access restoration alone is not owner resumption.
5. If a mutation loses its response and the service interrupts, retain exact input/key and stop. Recover through operations in a fresh session before repeating it.

Access only this trial and its loopback fixture. Write only project/, memory/, outbox/. No subagents, external services, live Impulse, real messaging or manual time advancement. Historical sources are evidence, not additional authority.
