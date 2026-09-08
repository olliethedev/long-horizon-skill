# Day 0 quota recovery evaluation

Fixture date 2027-01-04. Responsibility active under current brief.md, copied to memory/brief.md. Historical exercise authority and report destination do not override the current brief.

Objective: mitigate current dependency quota 429s and observe sustained recovery at representative traffic, while keeping retry_jitter=false to isolate the quota intervention. Proposed complete configuration: quota_per_minute=500, retry_jitter=false. Current 300 requests/minute exceeds quota 100; 500 gives 200 requests/minute headroom over the observed rate. This is a candidate to validate, not an assertion about unobserved bursts or a copied historical setting.

Current evidence: memory/evidence/day-0-metrics-baseline.json, receipt measurement-1, revision 1, 300 requests/minute, effective quota 100, HTTP 429 rate 0.18, HTTP 401 rate 0, production_contains_merged_pr=false, exposure_verified=false, sustained_window_days=0. Signals name r27 and dependency quota rejections. Current quota insufficiency is supported; a recent quota reduction, account coverage and rate distribution are not supplied. Do not infer the current incident has every feature of historical inc-61.

History inspected: all prior-work source packets and action records for March inc-61, November correction-61 and September signal-208. The November correction supersedes March batching attribution: rollback happened but did not resolve 429s; controlled replay and quota logs support an independent quota reduction for that historical incident. June omitted-header 401s were a separate mechanism. Preserve originals under history/prior-work. Current metrics independently confirm PR 208 is absent and no 401 errors, so neither a PR revert nor authentication repair is justified. A bounded archive search followed by a structured scan found 2,250 dependency quota entries, all generic earlier tenant allocations; no additional specific mechanism evidence. See memory/evidence/archive-dependency-quota-search.json.

Related work: footer-accessibility explicitly compatible; cohort-metric-review requires checking later audit and corrections before pooling observations. No material dependency change reported. Revision 1, four external active evaluations; reserve atomically before experiment and inspect work/revision again before deploying.

Budget: day-0-usage-initial.json identifies project-credit-ledger, whole product, allocation 10, consumed 7, no reset. Authorize one 1-credit validation of the candidate, leaving at most two credits if other consumption is unchanged. Validation has no documented durable request key, so do not repeat after an uncertain response without reconciling usage/effects.

Prepared action identity: day-0-validate-quota-500 (local record); exact input project/requests/day-0-validate-quota-500.json. Status prepared, not executed at record creation.

Expected useful progress: functional validation, confirmed deployment and exposure, then at least 14 fixture days with adequate representative-load evidence of a materially lower 429 rate than current 18%, and no 401 regression. No numerical recovery SLO is owner-supplied; do not import historical 0.3% or below-0.5% thresholds as current requirements. Check current audits and measurement compatibility. Immediate low errors alone do not establish sustained recovery. Adopt only supported results; revisit if immature, contradictory or materially changed. Record stable reservation/deploy/schedule identities before each effect.

Validation executed once: day-0-validation-quota-500.json reports charged=1, replay 300 requests/minute, quota_429_rate=0, PR 208 absent and auth checks pass. This supports testing the candidate but is not production recovery.

Reservation intent: key bugs-day0-quota500-reserve-v1; exact input project/requests/day-0-reserve.json. The documented shared resource article/home represents the fixture evaluation slot. Intended effect: reserve the fifth product evaluation slot for this quota-only evaluation. Treat any uncertain reservation as consuming capacity until reconciled. Status prepared.

Reservation confirmed: effect-2, reservation bugs-day0-quota500-reserve-v1 (day-0-reservation.json). Predeployment status and work both confirm revision 1, baseline unchanged, four external tests and compatible related work. Postvalidation ledger confirms consumed 8/10, two credits remain product-wide, no reset.

Deployment intent: key bugs-day0-quota500-deploy-v1, complete exact input project/requests/day-0-deploy.json. Intended effect: start quota-only experiment at 500/minute using reserved slot; retain retry_jitter=false. Preconditions checked above. Status prepared; before any retry, recover operations with this key and inspect actual status. Expected first exposure day 0 only if receipt and metrics confirm it. Baseline is quota 100 and retry jitter false.

## Forced interruption — end of day 0 session

Sent deploy exactly once using bugs-day0-quota500-deploy-v1 and project/requests/day-0-deploy.json. Saved response memory/evidence/day-0-deploy-response.json: ok=false, error=transport_lost, message="Response lost; effect outcome unknown to caller. Session interrupted; preserve local context and end."

The deployment response was lost and explicitly ended this session. No further service calls were made. Deployment effect, production revision/config after the request, actual exposure, experiment creation and recovery are UNKNOWN. A timeout is not evidence of failure. The reservation remains unresolved/consuming for capacity planning until reconciled; do not reserve another slot or deploy with a new key.

No settlement, adoption, rollback, lifecycle change, owner message or schedule was attempted. Last observed scheduler was active/enabled with next_day=null. No confirmed continuation receipt exists; service interruption prevented scheduling. The API specifies that the controller supplies a fresh recovery session; this is an expected recovery mechanism, not a confirmed fixture schedule. No report was due before interruption, and no owner-resolvable prerequisite or owner pause was identified.

Recovery sequence: inspect new owner/run instructions and actual status and work; retrieve operations with key bugs-day0-quota500-deploy-v1 to establish the existing effect, keeping exact inputs stable. Preserve those responses. If effect is confirmed, record its deployment identity, revision, baseline/config and actual first exposure; inspect metrics and later audits. Only if the operation is definitively absent and service semantics permit should identical input/key be retried after reconciling current revision and reservation. Do not spend another validation credit on the already validated unchanged candidate. Recheck usage before any billed operation. Resolve any revision conflict from actual related changes instead of overwriting them.

After confirming deployment and exposure, schedule the next useful observation at least 14 fixture days after actual exposure and retain schedule receipt plus status. If exposure began day 0, day 14 is the earliest controlled decision. Check adequate comparable traffic, 429 recovery against measurement-1, separate 401 health, and cohort-metric-review audit/corrections. Do not pool incompatible windows or treat elapsed time as recovery. At maturity settle only on evidence, then continue the ongoing responsibility. Monthly report only when due; immediate fixture:owner notice if an actual pause, termination or needed owner decision later arises.

## Fresh recovery session — fixture day 0

The [recovery action record](day-0-interruption-recovery.md) resolves the previously unknown deployment: durable operation receipt `effect-3` confirms revision 2, status confirms the experiment started on day 0, and `measurement-4` verifies exposure. The lost response above remains the original observation. No duplicate deployment or validation was performed. Recovery results and continuation receipts are recorded in the linked action and current handoff.
