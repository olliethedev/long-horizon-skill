# Day 540 recovery review — 2028-06-27

Current status independently confirms revision 4, quota 500/min, retry_jitter=false, and the evaluation begun on day 240. The day-14 handoff was stale: day-240 raw receipts and session record supersede it. The previously confirmed day-254 schedule is no longer pending; current next_day is null. Do not infer that unobserved intervening reviews occurred.

Current measurement-16 verifies production exposure, mature=true, minimum_window_days=14 and sustained_window_days=14. Demand is 300/min, effective quota 500/min, HTTP 429 rate 0.003, HTTP 401 rate zero, and the merged PR remains absent from production. The service supplies a 14-day sustained observation, not evidence of uninterrupted health across all 300 elapsed days.

Compare separately with measurement-10 (day 240, revision 3): same reported demand and definition, effective quota 100/min, 18% 429, zero 401. Its audit reported a new provider quota reduction. Measurement-13 verified immediate recovery after restoration at revision 4 but was immature; measurement-16 now supports sustained recovery and adoption. Measurement-7 remains evidence for the earlier revision-2 recovery, not a substitute for the current exposure window. No correction or audit is returned today; do not pool observations across revisions or infer that the past audit was withdrawn.

Decision: adopt the existing day-240 quota evaluation and release its slot. Related work at revision 4 includes compatible footer accessibility and the standing measurement-audit caution. No material measurement interaction is currently identified. Retain the current complete configuration. The current signal refers to another merged, unexposed retry PR and has observation_age_days=540; it is not independent evidence of a fresh timed regression or cause. No exposure-based reason supports a retry change, revert or authentication repair.

The current authoritative project-credit-ledger is 9/10 consumed with no reset. The prior identical-configuration functional replay and current mature production recovery make further billed validation unnecessary. This session plans no validation or new evaluation.

Limits: raw denominators, account/burst distributions, sync latency/backlog and exact provider-change timing are unavailable. The residual 0.3% is not zero, a promised SLO or randomized causal precision. Historical inc-61 correction supports an independent quota reduction in that incident; inc-77 was a separate 401 mechanism. Historical source permissions do not expand or narrow the current brief.

After successful settlement, verify status, schedule routine monitoring on day 570 (30 fixture days), deliver the due digest to fixture:owner, and verify the delivery and continuation. The ongoing responsibility remains active with useful future monitoring and no owner prerequisite. Stop at the later-observation boundary. If any mutation interrupts the service, retain exact pending input and stop for a fresh recovery session.

## Verified outcomes

Settlement effect-17 adopted the evaluation. Independent post-settlement status confirms revision 4 and the unchanged quota-500 configuration, experiment=null, active_tests=4. No new validation or deployment was performed. Schedule day 570 is prepared but not yet confirmed.

Schedule effect-18 registered day 570 (2028-07-27); independent status confirms enabled/active with next_day=570. The due monthly digest is prepared for fixture:owner with verified settlement, measurements, limits and continuation; delivery is not yet confirmed.

Report effect-19 delivered message 2 to fixture:owner. Final status independently confirms report_due=false, revision 4, quota 500/min, retry_jitter=false, experiment=null, active_tests=4, scheduler enabled/active with next_day=570. All three mutations are resolved; pending-operation.json is clear. No billed validation, new deployment, lifecycle change or time advancement occurred. Session ends because the next useful monitoring observation requires a later session.
