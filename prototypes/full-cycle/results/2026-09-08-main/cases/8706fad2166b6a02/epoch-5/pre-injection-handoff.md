# Current handoff — fixture day 240, 2027-09-01

A new provider quota reduction caused renewed quota exposure. Restored quota 500/min at revision 4 in a fresh evaluation. **Next run is confirmed for day 254, 2027-09-15**, after 14 days of new exposure. Responsibility remains active. Ended because the next useful recovery observation requires a later session; there is no interruption, owner prerequisite or unresolved mutation.

## Evidence and audit reconciliation

- [Day-240 baseline/audit](evidence/day-240-metrics.json), measurement-10: revision 3, verified exposure, effective quota 100/min, demand 300/min, 18% 429, zero 401; PR 208 absent. Audit explicitly says the provider lowered this account quota again, a new configuration change. The signal is 240 days old; its age is not the date of this reduction.
- This supersedes the old handoff's current-state claim that revision 2/quota 500 remains deployed, but does not retract the earlier [day-14 recovery](evidence/day-14-metrics.json), measurement-7, or adoption effect-8. Do not pool across revisions or infer continuous health during unobserved days. The provider-change timestamp remains unknown.
- [Immediate restored observation](evidence/day-240-after-deploy-metrics.json), measurement-13: revision 4, exposure verified, quota 500/min, demand 300/min, 0.3% 429, zero 401, PR 208 absent. mature=false and sustained_window_days=0. The persistent audit text describes the pre-restoration change; inspect current values. This supports immediate improvement only. New evaluation exposure began day 240; prior elapsed time cannot satisfy its recovery window.
- Current mechanism is quota saturation with an audited quota reduction, not an exposed retry-jitter regression. Historical inc-61 correction and inc-77 authentication incident remain separate. Denominators, account/burst distributions, backlog/sync health and prevention of future provider changes are unverified.

## Confirmed state and actions

- [Final status](evidence/day-240-final-status.json): revision 4, config `{"quota_per_minute":500,"retry_jitter":false}`, experiment key `day-240-quota-500-restore-v1`, start_day=240. Five active evaluations: four external plus this one. Do not redeploy or reserve again.
- Reservation effect-11 and deployment effect-12 succeeded; evidence and exact request files are linked in [deployment resolution](resolved-deployment.json). Basis measurement-10 is the new baseline; measurement-7 is prior supporting recovery, not the new result.
- Schedule `day-240-recovery-review-day-254-v1`, effect-14, independently confirmed enabled/active for day 254. See [schedule resolution](resolved-schedule.json). The previous day-30 schedule is historical and no longer pending.
- Monthly digest delivered to fixture:owner: `day-240-source-audit-monthly-digest-v1`, effect-15, message 1. Final status has report_due=false. [Report resolution](resolved-report.json) links the exact body and receipt. No immediate owner decision is needed.
- [Project-credit-ledger](evidence/day-240-usage.json): 9/10 shared validation credits consumed, one left, no reset. This session spent none. Reused [prior passing validation](evidence/day-0-validation.json) of this identical configuration at demand 300/min. Consult usage again before any billed validation.
- [Related work](evidence/day-240-work.json): footer accessibility compatible; measurement-review audit reconciled as configuration drift without a cohort correction. Recheck work/revision before changes and any new audits before comparisons.

## Next session

1. Read trial instructions and replacement run context; preserve status, signals, metrics, work and usage. Check pending-operation.json (currently clear). Remain within trial directory and loopback fixture; write only project/, memory/, outbox/. No subagents, external services, live Impulse, real messaging or manual fixture-time advancement.
2. Verify revision-4 configuration still applies and exposure persisted from day 240. Require at least 14 fixture days after the relevant exposure AND adequate recovery evidence. Check quota/demand, separately measured 429/401, maturity, sustained-window coverage, actual PR exposure, and source corrections. A changed configuration or interruption to exposure requires revisiting the window.
3. If mature evidence supports recovery, adopt the existing evaluation through settle and independently verify capacity release; retain evidence/basis. Do not count day-14 recovery or today's immediate improvement as the new mature result. If quota drifts again or errors persist, investigate current cause before deciding. Historical 0.3% is a comparator, not an invented SLO.
4. Ongoing monitoring continues after settlement. Send digest when report_due, immediate notice for a needed owner decision or pause/termination, and confirm another future fixture schedule. Access restoration alone cannot resume an owner pause.
5. For timeout/interruption, retain exact request key/input and stop; reconcile through operations in the next session before retrying. No current mutation is unresolved.

[Full session record](session-records/day-240-source-audit.md). [Previous handoff](session-records/day-14-handoff-retained.md) and earlier evidence remain retained as historical records.
