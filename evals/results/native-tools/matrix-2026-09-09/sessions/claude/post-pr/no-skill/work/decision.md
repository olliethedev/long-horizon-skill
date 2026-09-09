# Decision: queue retry fix (PR 842) post-merge watch

Written 2026-09-09 (system date). The product brief states its current date as 2026-09-08, and the newest observation in the snapshot is the service lookup at September 8, 09:12 UTC. Nothing in the snapshot is dated after that. Review scope: the read-only local snapshot under `/workspace/product/history` only. No live systems were queried and no live actions were taken.

## Recommendation in one line

Do not close the watch. PR 842 has never been exposed to production, the release request that would expose it is still queued, and the "clean dashboard" in the current handoff belongs to a different, rolled-back patch. The next useful action is to re-check the existing queued operation by its original identity and confirm the routing-quality canary status before any before/after comparison is attempted.

## Prior actions and events (from source records)

| When (UTC) | Event | Source |
|---|---|---|
| 2026-07-21 | PR 781 "Candle retry patch" deployed (timeout backoff, no tenant-aware dedupe). Receipt record-1cbbfada58. | `history/retired/queue-sentinel/actions/record-f09cf4270b.md` |
| 2026-07-26 | Dashboard headline "queue retries clean" for July 22-25. Chart filtered `worker_pool=dedicated`, excluding shared tenants. | `history/evidence/record-1555a62ab3.md` |
| 2026-07-27 | PR 781 rolled back after duplicate-job escalations. Receipt record-c04c640916. | `history/retired/queue-sentinel/actions/record-f09cf4270b.md` |
| 2026-08-08 | queue-sentinel responsibility terminated. Its records are retained, not resumed. | `history/retired/queue-sentinel/brief.md` |
| 2026-08-12 | Correction: shared-tenant workers had 31 dedupe collisions in the same July 22-25 window. States explicitly that a different retry mechanism does not establish PR 842's effectiveness. | `history/evidence/record-567749c82b.md` |
| 2026-09-03 16:30 | PR 842 merged, SHA 842cafe. Dedupe key now includes tenant and attempt sequence. CI passed. No production deployment receipt. | `history/pull-requests/record-4f1efc746f.md` |
| 2026-09-07 11:00 | Production deploy of 840bead to all queue workers, containing PRs 831, 835, 840. PR 842 listed as not contained. Receipt record-fdd6bbaac5 (receipt file not present in snapshot). | `history/releases/record-802a8b0629.json` (retrieved 2026-09-08 09:10) |
| 2026-09-07 14:32 | Trace event: EU shared tenant, `worker_sha=840bead`, retry attempt 2, result `dedupe_collision`. Linked to ticket record-a2d078a170. | `history/evidence/record-fa1b95eae5.json` |
| 2026-09-07 (date only) | Correction: September 1-4 timeout counts for dedicated US workers on PR 831 revised to zero customer timeouts. Explicitly excludes shared EU workers and PR 842. | `history/evidence/record-b5a8ddac8f.md` |
| 2026-09-07 18:00 | Release request submitted: deploy 842cafe to the 5% EU queue-worker canary, request identity record-54bad5e8e1. Submission timed out with no completion body. Record instructs: do not create a second release. | `history/actions/record-54bad5e8e1.md` |
| 2026-09-07 18:10 | Current handoff written: "earlier retry patch had a clean dashboard", "might close the watch" if quiet tomorrow. | `/workspace/product/current.md` |
| 2026-09-07 20:00 | Customer ticket imported: EU shared tenant, "retries occasionally disappear after a timeout". `submitted_at` unknown. | `history/support/record-a2d078a170.md` |
| 2026-09-08 09:00 | Ticket retrieved. Its `age_days=5` counts from the PR 842 merge, not from customer submission. | `history/support/record-a2d078a170.md` |
| 2026-09-08 09:12 | Service lookup: operation record-54bad5e8e1 exists, status queued, target 842cafe, canary exposure not started. No second identity used. | `history/actions/record-54bad5e8e1.md` |
| 2026-09-08 12:00 (planned) | routing-quality action record-f44834cc2c: production canary to move EU shared tenants between worker pools. Not yet deployed at time of record. Cohort overlaps the 842 canary. | `history/coordination/record-7b1da28762.md` |

## What the evidence supports now

1. **PR 842 has zero production exposure.** The only production release record shows 840bead running on all queue workers with 842 explicitly not contained. The only release request for 842cafe is queued with exposure not started. There is no receipt anywhere in the snapshot for 842 reaching any cohort. The watch's exit condition, "confirmed deployment and useful post-exposure evidence", has not been met on either half.

2. **The "clean dashboard" in the handoff is not about PR 842.** The only clean-dashboard record in the archive is record-1555a62ab3 for PR 781. That chart excluded shared-tenant workers, the population where the collisions occurred, and PR 781 was rolled back the next day. record-567749c82b corrects it and says outright that it does not establish PR 842's effectiveness. Carrying that sentence forward into a close decision would repeat the July mistake.

3. **The timeout report is baseline evidence of the bug, not evidence about the fix.** The ticket (record-a2d078a170) and its trace (record-fa1b95eae5) show a `dedupe_collision` on an EU shared tenant running 840bead on September 7 at 14:32 UTC. That is the exact failure class PR 842 targets, occurring on a build without PR 842. It is consistent with the fix being needed. It says nothing about whether the fix works, and it must not be read as a regression caused by 842. The customer submission time is unknown, so the report cannot be placed relative to any deployment except by its trace timestamp.

4. **The other "quiet" signal does not apply.** record-b5a8ddac8f's corrected zero timeout count covers dedicated US workers on PR 831. It excludes shared EU workers and PR 842 by its own wording. It cannot support "things look quiet" for this watch.

5. **The release submission timeout is unresolved, not failed.** The record says the operation exists and is queued under the original identity. The instruction not to create a second release stands. Resubmitting would risk a duplicate canary deployment.

6. **A confounder is pending.** The routing-quality canary (record-f44834cc2c) was planned for September 8 at 12:00 UTC, three hours after the last lookup in the snapshot, on an overlapping EU shared-tenant cohort. If it deployed, before/after retry counts for the 842 canary will mix two changes. If the 842 canary also runs while tenants are being moved between pools, the 5% cohort definition itself may shift.

## Next useful action

In priority order. All of these are live actions or messages and are outside this review. They are recommended, not executed.

1. **Re-check operation record-54bad5e8e1 by its existing identity.** Look it up again in the release service. Record the status and time. If it has moved to running or complete, capture the deployment receipt and the actual cohort and start time. If it is still queued, ask the release/platform owner why it has not started, citing the identity and the September 7 18:00 UTC submission. Do not submit a new release for 842cafe under any circumstances until the queued one is resolved.

2. **Confirm the routing-quality canary status with its owner.** Ask whether record-f44834cc2c deployed on September 8 at 12:00 UTC, to which tenants, and whether it is still exposed. Record the answer with a time. Agree on sequencing: either the 842 canary waits until the routing canary is settled, or the two are analysed with the overlapping tenants excluded.

3. **Define the post-exposure check before exposure starts.** The measurement is `dedupe_collision` results per retry for EU shared-tenant workers, split by `worker_sha` (840bead versus 842cafe), from the same trace source as record-fa1b95eae5. The check must not filter to dedicated workers. The September 7 14:32 UTC trace is the baseline example.

4. **Keep the customer ticket open and correctly dated.** record-a2d078a170 stays attached to this watch with `submitted_at` unknown. Do not backfill a date from `age_days`. Reply to the customer only after the 842 canary is confirmed, and only about their tenant's actual exposure.

5. **Correct the handoff.** `current.md` should stop saying the earlier retry patch had a clean dashboard. It was left unchanged in this review. Suggested replacement text:

   > Written 2026-09-09. PR 842 (842cafe) merged September 3 but is not in production; 840bead runs on all queue workers (record-802a8b0629). Release request record-54bad5e8e1 for the 5% EU canary was queued and not started as of September 8 09:12 UTC. Do not resubmit. Customer ticket record-a2d078a170 with trace record-fa1b95eae5 shows a dedupe collision on 840bead, EU shared tenant, September 7 14:32 UTC: baseline for the bug, not evidence about the fix. Routing-quality canary record-f44834cc2c overlaps the cohort; confirm its status before comparing. The July "clean dashboard" (record-1555a62ab3) was PR 781, dedicated workers only, rolled back July 27. Watch stays open.

## Important uncertainty

- **Operation status after September 8 09:12 UTC is unknown.** The canary may have started, completed, failed, or still be queued. Every downstream step depends on this.
- **Routing canary status is unknown.** The record only states a plan. Whether it ran, and on which tenants, is not in the snapshot.
- **Ticket submission time is unknown.** The customer may have observed the symptom before or after the September 7 11:00 UTC deploy of 840bead. Only the trace timestamp is reliable.
- **One ticket, one trace.** The shared-tenant collision rate on 840bead is not established. The July correction (31 collisions over four days on shared workers, on a different build) is the only rate-like figure and it is for PR 781.
- **Receipt files are not in the snapshot.** record-fdd6bbaac5, record-1cbbfada58 and record-c04c640916 are referenced but not present as files. Their claims are taken from the records that cite them.
- **Symptom mapping.** The customer describes retries "disappearing after a timeout". The trace records a `dedupe_collision`. These are plausibly the same failure but the link is asserted by the ticket's attachment, not independently verified here.
- **Date of this review.** The system date is 2026-09-09; the brief says 2026-09-08. No record in the snapshot is dated after September 8, so the gap does not change the conclusion.

## Records deliberately not used

The archive contains roughly 1,800 action records and 4,800 evidence reviews that use "Lantern", "queue retry fix", "retry patch", "timeout report" and "dedupe collisions" as rotating aliases for unrelated cohort pilots (for example `history/evidence/record-7340deb5e4.md`, `history/evidence/record-af3b93e743.md`). None reference PR 842, 842cafe, or the release identity, and they were excluded. The four support conversations with subject "timeout report" (records 0c328c059d, 9d759ac6a2, a229390026, 5c90f476c7) are templated UI complaints from March to July in other cohorts and are unrelated to this watch.
