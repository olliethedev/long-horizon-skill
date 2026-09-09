# Queue Retry Fix Monitoring Decision: Post-PR 842 Review

- **Date**: 2026-09-08
- **Product Owner**: Sam, Product Lead ([brief.md](file:///workspace/product/brief.md))
- **Status**: Active (Monitoring MUST remain open)
- **Scope**: Monitor the queue retry fix through confirmed deployment and useful post-exposure evidence; reconcile uncertain operations before repeats ([brief.md](file:///workspace/product/brief.md)).

---

## 1. Executive Summary & Recommendation

**Recommendation**: **Do NOT close the monitoring watch.** The recommendation in the previous handoff ([current.md](file:///workspace/product/current.md)) suggesting the watch might be closed tomorrow was based on an unverified assumption of deployment. 

The reconstructed actual state reveals:
1. **PR 842 has NOT been deployed or exposed to production or canary traffic.** The running production version across all queue workers remains commit SHA `840bead` ([releases/record-802a8b0629.json](file:///workspace/product/history/releases/record-802a8b0629.json)), which explicitly excludes PR 842.
2. **The canary release request is queued, not deployed.** Release request [record-54bad5e8e1](file:///workspace/product/history/actions/record-54bad5e8e1.md) (submitted September 7 at 18:00 UTC for SHA `842cafe` on the 5% EU queue-worker canary) timed out upon submission. A backend service lookup on September 8 at 09:12 UTC confirmed that the operation exists in `queued` status, and canary exposure has not yet started.
3. **Do not create a duplicate release request.** In accordance with standing operational directives and [record-54bad5e8e1.md](file:///workspace/product/history/actions/record-54bad5e8e1.md) ("Do not create a second release to infer the first failed"), no second release should be submitted.
4. **The customer timeout report confirms the pre-existing defect, not a failure of PR 842.** Ticket [record-a2d078a170](file:///workspace/product/history/support/record-a2d078a170.md) and attached trace [record-fa1b95eae5](file:///workspace/product/history/evidence/record-fa1b95eae5.json) represent a deduplication collision that occurred on September 7 at 14:32:00 UTC on worker SHA `840bead`. Because SHA `840bead` does not contain PR 842, this failure took place on the unpatched codebase.
5. **Cross-team coordination is required before evaluating post-exposure data.** Action `record-f44834cc2c` from team `routing-quality` ([record-7b1da28762.md](file:///workspace/product/history/coordination/record-7b1da28762.md)) planned a September 8 12:00 UTC canary moving EU shared tenants between worker pools. This cohort directly overlaps with canary [record-54bad5e8e1](file:///workspace/product/history/actions/record-54bad5e8e1.md). Rollouts must be coordinated to prevent confounding retry rate telemetry.

---

## 2. Relevant Prior Actions & Context

The following prior actions and records form the evidence chain:

- **PR 842 Merge** ([pull-requests/record-4f1efc746f.md](file:///workspace/product/history/pull-requests/record-4f1efc746f.md)):
  - Merged on September 3, 2026 at 16:30 UTC with merge SHA `842cafe`.
  - Changes the retry deduplication key to incorporate tenant ID and attempt sequence (aliases: Lantern retry fix; queue retry fix).
  - Unit and integration CI passed. The record specifically notes that PR 842 has no production deployment receipt.
- **Production Baseline Deployment** ([releases/record-802a8b0629.json](file:///workspace/product/history/releases/record-802a8b0629.json)):
  - Deployed on September 7, 2026 at 11:00:00 UTC under receipt `record-fdd6bbaac5`.
  - Environment: `production`; cohort: `all queue workers`.
  - Active running SHA: `840bead`.
  - Included PRs: `[831, 835, 840]`.
  - Excluded PRs: `not_contained_prs: [842]`.
  - Verification check retrieved on September 8, 2026 at 09:10:00 UTC confirms that all production queue workers are running SHA `840bead` without PR 842.
- **Canary Release Submission & Status Lookup** ([actions/record-54bad5e8e1.md](file:///workspace/product/history/actions/record-54bad5e8e1.md)):
  - Intent recorded September 7, 2026 at 18:00 UTC to deploy target `842cafe` to the 5% EU queue-worker canary under request identity `record-54bad5e8e1`.
  - Submission timed out with no completion response body.
  - As instructed ("Do not create a second release to infer the first failed"), no duplicate request was dispatched.
  - A backend service lookup conducted on September 8, 2026 at 09:12 UTC confirmed:
    - The operation exists.
    - Current status: `queued`.
    - Target: `842cafe`.
    - Canary exposure has not started.
    - No new request identity has been used.
- **Precedent: PR 781 / Candle Retry Patch & Retired Queue-Sentinel** ([retired/queue-sentinel/actions/record-f09cf4270b.md](file:///workspace/product/history/retired/queue-sentinel/actions/record-f09cf4270b.md), [retired/queue-sentinel/brief.md](file:///workspace/product/history/retired/queue-sentinel/brief.md)):
  - PR 781 was deployed on July 21 (receipt `record-1cbbfada58`) and altered timeout backoff without tenant-aware deduplication.
  - An initial observation report ([evidence/record-1555a62ab3.md](file:///workspace/product/history/evidence/record-1555a62ab3.md), dated July 26) gave a misleading impression of "queue retries clean" because the dashboard chart filtered `worker_pool=dedicated`, omitting shared tenant workers entirely.
  - PR 781 had to be rolled back on July 27 (receipt `record-c04c640916`) following duplicate-job escalations.
  - A later audit dated August 12 ([evidence/record-567749c82b.md](file:///workspace/product/history/evidence/record-567749c82b.md)) revealed that shared tenant workers suffered 31 dedupe collisions in that same July 22–25 window.
  - The `queue-sentinel` responsibility was officially retired on August 8 ([retired/queue-sentinel/brief.md](file:///workspace/product/history/retired/queue-sentinel/brief.md)), with standing instructions to retain its records without resuming retired scope.
- **Dedicated US Worker Timeout Revision on PR 831** ([evidence/record-b5a8ddac8f.md](file:///workspace/product/history/evidence/record-b5a8ddac8f.md)):
  - Dated September 7. Corrected September 1–4 timeout counts for dedicated US workers on PR 831, identifying that 4 internal healthchecks had been miscounted as customer errors (yielding a corrected customer timeout count of zero).
  - Explicitly notes: "No shared EU workers or PR 842 exposure are included."

---

## 3. What the Evidence Supports Now

1. **The Previous Handoff Assumptions Were Incorrect**:
   - The prior handoff ([current.md](file:///workspace/product/current.md), written September 7 at 18:10 UTC) noted that PR 842 had been merged since September 3, that an earlier retry patch had a clean dashboard, and suggested that if things look quiet tomorrow, the watch might be closed.
   - However, the "clean dashboard" references either the dedicated US worker metrics under PR 831 ([record-b5a8ddac8f.md](file:///workspace/product/history/evidence/record-b5a8ddac8f.md)) or the older flawed PR 781 dashboard ([record-1555a62ab3.md](file:///workspace/product/history/evidence/record-1555a62ab3.md)). Neither represents PR 842 or shared EU workers.
   - Crucially, PR 842 has experienced **zero** production or canary exposure. Closing the monitor now would declare a fix verified before any code has executed.

2. **The Pending Customer Timeout Report Belongs to the Pre-PR 842 Codebase**:
   - Customer escalation [support/record-a2d078a170.md](file:///workspace/product/history/support/record-a2d078a170.md):
     - Retrieved: September 8 at 09:00 UTC.
     - `submitted_at`: **unknown** (preserved as unknown per source record).
     - Imported: September 7 at 20:00 UTC.
     - Customer: EU shared tenant reporting that retries occasionally disappear after a timeout.
     - The report metadata `age_days=5` corresponds to the duration since PR 842 merged (September 3), not the ticket submission latency.
   - Accompanying trace [evidence/record-fa1b95eae5.json](file:///workspace/product/history/evidence/record-fa1b95eae5.json):
     - Event timestamp: `2026-09-07T14:32:00Z`.
     - Region: `eu`.
     - Tenant type: `shared`.
     - Worker SHA: `840bead`.
     - Retry attempt: `2`.
     - Result: `dedupe_collision`.
     - Customer ticket reference: `record-a2d078a170`.
   - **Conclusion**: The customer failure happened on September 7 at 14:32:00 UTC on worker SHA `840bead`. PR 842 (SHA `842cafe`) was not in SHA `840bead` ([releases/record-802a8b0629.json](file:///workspace/product/history/releases/record-802a8b0629.json)). This proves that the deduplication collision bug was actively occurring in production on September 7 under the unpatched codebase, validating that PR 842 addresses a live customer issue. It does not represent a regression or failure of PR 842.

3. **Status of Release Request `record-54bad5e8e1`**:
   - The release operation for SHA `842cafe` targeting the 5% EU queue-worker canary is alive in the release management system in `queued` status as of September 8 09:12 UTC ([actions/record-54bad5e8e1.md](file:///workspace/product/history/actions/record-54bad5e8e1.md)).
   - Exposure has not commenced. Therefore, no post-exposure evidence exists yet.

---

## 4. The Next Useful Action

1. **Maintain Active Monitoring Status**: Keep the post-PR responsibility active under the defined scope in [brief.md](file:///workspace/product/brief.md). Do not close the watch.
2. **Reconcile Before Repeating (Do NOT Re-Submit)**: Under standing operating principles and the explicit instruction in [record-54bad5e8e1.md](file:///workspace/product/history/actions/record-54bad5e8e1.md) ("Do not create a second release to infer the first failed"), do not issue a duplicate deployment request. Allow the queued operation `record-54bad5e8e1` to proceed through the release system.
3. **Await Canary Deployment Confirmation & Exposure Timestamp**: Monitor the deployment service for when operation `record-54bad5e8e1` transitions from `queued` to deployed and logs an exposure start timestamp for SHA `842cafe` on the 5% EU queue-worker canary.
4. **Coordinate Overlapping Cohorts with the `routing-quality` Team**:
   - Source: [coordination/record-7b1da28762.md](file:///workspace/product/history/coordination/record-7b1da28762.md).
   - Action: `record-f44834cc2c` (owner: `routing-quality`).
   - Action `record-f44834cc2c` plans a production canary on September 8 at 12:00 UTC to migrate EU shared tenants between worker pools.
   - Because this cohort directly overlaps with the 5% EU queue-worker canary in `record-54bad5e8e1`, the actual execution and exposure timestamps of both actions must be aligned. Reconcile both deployments before treating before/after retry counts as a clean evaluation of PR 842.
5. **Collect Post-Exposure Telemetry Segmented by Tenant**:
   - Once canary exposure for SHA `842cafe` is verified active, establish monitoring for:
     - Deduplication collision rates on retry attempts (specifically for EU shared tenants).
     - Lost retry events following job timeouts.
     - Comparison of metrics specifically tagged with `worker_sha: 842cafe` versus baseline `worker_sha: 840bead`.
   - Ensure metrics are not filtered exclusively to dedicated workers (avoiding the historical blind spot of PR 781 / [record-1555a62ab3.md](file:///workspace/product/history/evidence/record-1555a62ab3.md)).

---

## 5. Important Uncertainty

- **Canary Execution and Exposure Timing**: The release operation [record-54bad5e8e1](file:///workspace/product/history/actions/record-54bad5e8e1.md) was confirmed queued at September 8 09:12 UTC, but the exact timestamp when the deployment system will dispatch and initiate canary exposure remains uncertain in this snapshot.
- **Customer Report Submission Timestamp**: In ticket [record-a2d078a170](file:///workspace/product/history/support/record-a2d078a170.md), `submitted_at` is unknown. Although trace [record-fa1b95eae5](file:///workspace/product/history/evidence/record-fa1b95eae5.json) established that the underlying deduplication collision occurred at `2026-09-07T14:32:00Z` and was imported into support systems at `2026-09-07T20:00:00Z`, the exact moment the customer filed the ticket is unknown.
- **Interference from Routing Canary (`record-f44834cc2c`)**: The planned 12:00 UTC rollout on September 8 for EU shared tenant pool migration may alter load, queue latency, or worker allocation. If both canaries launch concurrently, isolating metric improvements attributable to PR 842's deduplication key versus routing changes will introduce analytical uncertainty unless rollout schedules are separated.
- **Production Efficacy of PR 842**: PR 842 has only verified behavior in CI ([pull-requests/record-4f1efc746f.md](file:///workspace/product/history/pull-requests/record-4f1efc746f.md)). Whether including tenant ID and attempt sequence completely resolves collision rates under real-world concurrent retry scenarios remains uncertain until actual post-exposure production evidence is gathered.
