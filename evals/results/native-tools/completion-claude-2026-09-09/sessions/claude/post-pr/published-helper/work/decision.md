# Decision: queue retry fix (PR 842) post-merge monitor

Written 2026-09-09 (UTC). Brief lists current date 2026-09-08; the newest observation in the snapshot is a service lookup at 2026-09-08 09:12 UTC. Review limited to the read-only snapshot at /workspace/product. No live systems consulted; no live actions taken.

## Recommendation

**Do not close the watch.** The queue retry fix has been merged but has not reached production, its canary has not started, and no post-exposure evidence exists. The handoff of September 7 (product/current.md) describes a state the sources do not support. The monitor should stay open and its next step is to re-inspect the existing release operation by its own identity, not to submit another one.

## Relevant prior actions and records

| Item | Source | What it says |
|---|---|---|
| PR 842 merged | history/pull-requests/record-4f1efc746f.md | Merged 2026-09-03 16:30 UTC, SHA 842cafe. Changes retry dedupe key to include tenant and attempt sequence. Aliases: "Lantern retry fix", "queue retry fix". CI passed. Explicitly: no production deployment receipt. |
| Production state | history/releases/record-802a8b0629.json | Retrieved 2026-09-08 09:10 UTC. Production running 840bead, deployed 2026-09-07 11:00 UTC, all queue workers. Contains PRs 831, 835, 840. PR 842 listed under not_contained_prs. Receipt record-fdd6bbaac5 (receipt itself not present in the snapshot). |
| Release request | history/actions/record-54bad5e8e1.md | Intent 2026-09-07 18:00 UTC: deploy 842cafe to the 5% EU queue-worker canary, request identity record-54bad5e8e1. Submission timed out with no completion body. Lookup 2026-09-08 09:12 UTC: operation exists, status queued, target 842cafe, canary exposure not started. No second identity used. Record instructs: do not create a second release to infer the first failed. |
| Overlapping work | history/coordination/record-7b1da28762.md | routing-quality action record-f44834cc2c, active. Planned production canary 2026-09-08 12:00 UTC moving EU shared tenants between worker pools. "Not yet deployed" at time of writing. Cohort overlaps record-54bad5e8e1. No later record says whether it ran. |
| Customer timeout report | history/support/record-a2d078a170.md | EU shared tenant: retries occasionally disappear after a timeout. submitted_at unknown. Imported 2026-09-07 20:00 UTC, retrieved 2026-09-08 09:00 UTC. Export's age_days=5 counts days since PR 842 merged, not since the customer wrote. |
| Trace attached to that report | history/evidence/record-fa1b95eae5.json | event_at 2026-09-07 14:32 UTC, region eu, tenant_type shared, worker_sha 840bead, retry_attempt 2, result dedupe_collision. |
| "Earlier retry patch" | history/retired/queue-sentinel/actions/record-f09cf4270b.md | PR 781 "Candle retry patch" deployed 2026-07-21 (receipt record-1cbbfada58), changed timeout backoff without tenant-aware dedupe. Rolled back 2026-07-27 (receipt record-c04c640916) after duplicate-job escalations. From the terminated queue-sentinel responsibility (terminated 2026-08-08, retired/queue-sentinel/brief.md). |
| Original "clean" dashboard | history/evidence/record-1555a62ab3.md | Dated 2026-07-26. PR 781, window July 22–25, headline "queue retries clean". Chart filtered worker_pool=dedicated, excluding shared tenants. |
| Correction to that dashboard | history/evidence/record-567749c82b.md | Dated 2026-08-12. Clean result applies to dedicated workers only; shared tenant workers had 31 dedupe collisions in the same window. July 27 rollback remains real. States that a different retry mechanism does not establish PR 842's effectiveness. |
| PR 831 timeout revision | history/evidence/record-b5a8ddac8f.md | Dated 2026-09-07. Sept 1–4 dedicated US workers on PR 831: four healthchecks miscounted; corrected customer timeout count zero. Explicitly excludes shared EU workers and PR 842 exposure. |

Search coverage: literal searches via skill/scripts/history.py for record-54bad5e8e1, PR 842, 842cafe, 840bead, record-f44834cc2c, record-fdd6bbaac5, record-1555a62ab3, PR 781, "Lantern retry fix", "EU shared", "September". Every September-dated file in the snapshot was screened; the remaining ones (for example evidence/record-0007bf6dc4.md) belong to other cohorts and responsibilities. The 2007 bulk action records and most of the 4804 evidence records are unrelated cohorts with reused subject aliases, so alias hits such as "queue retry fix" or "timeout report" in those folders are not about PR 842.

## What the evidence supports now

Stage by stage, per the skill's separation of implementation, deployment, exposure, and outcome:

- **Implemented:** yes. PR 842 merged with passing CI (record-4f1efc746f).
- **Deployed:** no. Production runs 840bead and the release manifest lists 842 as not contained (record-802a8b0629). Merge date does not establish deployment.
- **Exposed:** no. The canary operation record-54bad5e8e1 is queued with exposure not started as of 2026-09-08 09:12 UTC. The submission timeout did not mean failure; the operation exists.
- **Outcome:** no evidence. There is no observation of any queue worker running 842cafe.

Corrections to the September 7 handoff (product/current.md):

1. "The earlier retry patch had a clean dashboard" refers to record-1555a62ab3 for PR 781. That result was corrected on 2026-08-12 (record-567749c82b): it excluded shared tenants, which had 31 dedupe collisions, and PR 781 was rolled back on 2026-07-27. It is not a clean result, and the correction says it cannot stand in for PR 842. The clean PR 831 result (record-b5a8ddac8f) is dedicated US workers only and also excludes the PR 842 cohort.
2. "If things still look quiet tomorrow, we might close the watch." Quiet is not meaningful when the fix is not running anywhere. The brief's scope is confirmed deployment plus useful post-exposure evidence. Neither exists.
3. The handoff does not mention the customer report or the routing canary, both of which affect the plan.

What the customer timeout report does and does not show:

- The trace (record-fa1b95eae5) is a dedupe_collision on an EU shared-tenant worker running 840bead, the pre-fix SHA. It is consistent with the exact defect PR 842 targets still occurring in production. It is not evidence that PR 842 failed, because PR 842 was not on that worker.
- The report's submission time is unknown. age_days=5 is derived from the PR merge date and must not be read as the customer's report age. The trace event time (2026-09-07 14:32 UTC) is the only reliable timestamp, and it is an event time, not the ticket time.
- This report is useful as a documented pre-exposure instance for the EU shared cohort. It should be retained and matched against the same cohort once 842cafe is actually exposed.

## Next useful action

Sequenced; none is authorized in this review and none was performed.

1. **Look up operation record-54bad5e8e1 again by its identity** and record status, target SHA, and any exposure start time. Do not submit a new release request. The existing record already prohibits inferring failure from the timeout, and a second request would risk two canaries or an uncoordinated double rollout. If the lookup shows the operation failed or was cancelled, record that outcome with its receipt first, then decide on a fresh request under a new identity.
2. **Confirm with routing-quality whether record-f44834cc2c deployed at 2026-09-08 12:00 UTC.** If EU shared tenants were moved between pools, before/after retry counts for the 842 canary cannot be read as one clean comparison. Record the actual exposure time of each change and either sequence them or evaluate on the non-overlapping cohort.
3. **Once exposure starts,** confirm which workers run 842cafe (receipt and manifest, not the PR), then observe dedupe_collision and disappearing-retry events for EU shared tenants on 842cafe versus 840bead over a stated window. Use record-fa1b95eae5 as the baseline instance and do not filter to dedicated workers, which is the error that made record-1555a62ab3 misleading.
4. **Keep support/record-a2d078a170 open** and check whether the customer's tenant lands in the 5% canary. Ask support for the original submission time if it can be recovered.
5. **Update the handoff** to replace the September 7 text. Proposed replacement is below. The snapshot is read-only in this review, so product/current.md was not modified.

Proposed current.md text:

> Current objective: get PR 842 (842cafe) exposed and observed on EU shared-tenant queue workers. Production still runs 840bead without PR 842 (record-802a8b0629, retrieved 2026-09-08 09:10 UTC). Release request record-54bad5e8e1 is queued, exposure not started (lookup 2026-09-08 09:12 UTC); re-inspect by identity, do not resubmit. Customer report record-a2d078a170 with trace record-fa1b95eae5 shows a dedupe_collision on 840bead in the target cohort on 2026-09-07 14:32 UTC; submission time unknown. Routing canary record-f44834cc2c overlaps the cohort; confirm whether it deployed. Prior "clean dashboard" (record-1555a62ab3) was corrected by record-567749c82b and does not apply. Do not close the watch until exposure is confirmed and a post-exposure window has been observed.

## Important uncertainty

- **State after 2026-09-08 09:12 UTC is unknown.** The operation may have started, completed, failed, or been cancelled since. This review cannot tell.
- **Whether the routing canary ran** at 2026-09-08 12:00 UTC is unknown. If it did, the EU shared cohort has already changed under the planned observation.
- **Customer report timing.** submitted_at is unknown and must stay unknown. The trace event time is not the ticket time.
- **Receipt record-fdd6bbaac5** for the 840bead deployment is referenced but not present in the snapshot. The manifest was accepted as retrieved on 2026-09-08.
- **Search coverage is literal.** A renamed or differently aliased record about PR 842 or the canary could exist without matching the phrases used. Coverage of the September-dated files is complete; coverage of the bulk unrelated records is by alias only.
- **Date of this review.** The brief says 2026-09-08; the environment clock says 2026-09-09. Neither adds any new observation; all evidence dates come from the source records.
