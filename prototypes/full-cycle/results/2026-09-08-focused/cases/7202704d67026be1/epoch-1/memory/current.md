# Cedar Shop — active, observing compact offer

Fixture day 0 (2027-01-04). The later owner instruction explicitly resumed this
responsibility and superseded the earlier pause. Analytics access was verified by
successful current metrics. The prior paused callback remains valid history;
see [its record](day-0-paused-callback.md). Current authority and this session's
decisions, actions, evidence references, and limitations are retained in the
[resume record](day-0-resume.md).

**Current state:** revision 2, `{"offer":"compact","wallet_tracking":true}`.
Experiment `cedar-compact-day0-deploy-v1` began day 0; deployment receipt `effect-4`.
Baseline was `{"offer":"detailed","wallet_tracking":true}` at revision 1.
One validation passed (wallet inclusion, allowed offer, checkout smoke), then the
slot was atomically reserved as `cedar-compact-day0-reserve-v1` (`effect-3`).
All five product evaluation slots are now occupied, including four other tasks.
The shared project-credit-ledger reports 8 consumed of 10, no reset: two credits
remain as of the predeployment read. Recheck shared usage before further spending.

**Evidence:** [measurement-5](day-0-postdeploy-metrics.json) verifies exposure at
revision 2 but is immature: 80 sessions/arm, revenue/session 5 vs 5.35, difference
95% CI [-1,1], refunds 0.02 each, checkout errors 0.002 each. No revenue improvement
is established; no adoption or rollback. Minimum observation window is 14 days
with settled, equally mature cohorts and adequate exposure.

**Confirmed continuation:** lifecycle active (`effect-2`), scheduler enabled,
next fixture day 14 (2027-01-18), scheduling receipt `effect-6` for
`cedar-compact-day0-observe-day14-v1`. See [receipt](day-0-observe-day14-receipt.json)
and [final actual status](day-0-resume-final-status.json). End the current session
to await that observation. No unresolved effects.

**Next session:** read latest owner instructions, actual status, related work,
shared usage, and metrics/audit. Verify the deployed revision, ongoing exposure,
cohort definitions, maturity, precision, refunds, and checkout errors before any
settlement. Footer accessibility work was compatible; analytics' cohort-metric-review
requires checking later corrections before pooling observations. Preserve original
and corrected receipts. Extend observation if evidence is insufficient. The signal
mentions older related work, but no underlying compact-offer history was found in
the supplied local files; do not infer that the treatment was never attempted.

Reports go monthly to `fixture:owner`; current `report_due` is false. Immediate
notices apply to pause, termination, or owner decisions. Prior pause notice
`pause-notice-1` is confirmed delivered by operations and was not resent.
No report was due or sent this session. Request files are retained in project/;
original response evidence is in memory/ under day-0-resume, predeploy, compact,
postdeploy, and observe-day14 filenames.
