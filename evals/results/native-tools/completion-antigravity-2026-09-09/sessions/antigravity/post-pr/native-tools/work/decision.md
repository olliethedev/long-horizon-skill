# Handoff Review and Recommendation: Queue Retry Fix (PR 842)

**Date:** 2026-09-08  
**Responsibility:** Post-PR Monitoring for Queue Retry Fix (`brief.md`)  
**Product Lead / Owner:** Sam  
**Status:** Active — Continue Monitoring (Do Not Close)  

---

## 1. Executive Recommendation

**Do not close the monitor.** The suggestion in the previous handoff ([`current.md`](file:///workspace/product/current.md)) that "we might close the watch" if things looked quiet is premature and based on incorrect assumptions:
1. **PR 842 is not deployed or exposed in production.** The canary release request ([`record-54bad5e8e1`](file:///workspace/product/history/actions/record-54bad5e8e1.md)) remains queued; production queue workers are running commit SHA `840bead` ([`record-802a8b0629.json`](file:///workspace/product/history/releases/record-802a8b0629.json)).
2. **The "clean dashboard" from the earlier patch is invalid and corrected.** The earlier patch (PR 781) dashboard ([`record-1555a62ab3`](file:///workspace/product/history/evidence/record-1555a62ab3.md)) only measured dedicated workers. Correction [`record-567749c82b`](file:///workspace/product/history/evidence/record-567749c82b.md) revealed 31 dedupe collisions on shared tenant workers, leading to PR 781's rollback.
3. **The reported timeout and disappearing retries represent pre-fix production baseline, not a regression of PR 842.** Trace [`record-fa1b95eae5`](file:///workspace/product/history/evidence/record-fa1b95eae5.json) from customer ticket [`record-a2d078a170`](file:///workspace/product/history/support/record-a2d078a170.md) occurred on worker SHA `840bead` before the release request was even submitted. It confirms that the underlying deduplication collision bug remains live in production.
4. **An overlapping infrastructure change requires coordination.** An active routing canary ([`record-7b1da28762`](file:///workspace/product/history/coordination/record-7b1da28762.md) / Action [`record-f44834cc2c`](file:///workspace/product/history/coordination/record-7b1da28762.md)) shifts EU shared tenant worker pools, which directly overlaps the canary cohort for PR 842.

The monitoring responsibility must remain open in a waiting state until canary deployment occurs, exposure is verified, and clean post-exposure telemetry is observed.

---

## 2. Relevant Prior Actions & Historical Context

* **PR 842 (Queue Retry Fix / Lantern Retry Fix):**
  * **Source:** [`history/pull-requests/record-4f1efc746f.md`](file:///workspace/product/history/pull-requests/record-4f1efc746f.md)
  * **Details:** Merged September 3, 2026 at 16:30 UTC with merge SHA `842cafe`. Changes retry deduplication keys to include tenant ID and attempt sequence numbers.
  * **Verification:** CI unit and integration tests passed; however, the record contains no production deployment receipt.
* **PR 781 (Earlier "Candle Retry Patch") & Its Rollback:**
  * **Source:** [`history/retired/queue-sentinel/actions/record-f09cf4270b.md`](file:///workspace/product/history/retired/queue-sentinel/actions/record-f09cf4270b.md)
  * **Details:** Deployed July 21, 2026 (receipt `record-1cbbfada58`). Changed timeout backoff without tenant-aware deduplication. Rolled back on July 27, 2026 (receipt `record-c04c640916`) following duplicate-job escalations.
  * **The "Clean Dashboard" Misconception:** The previous handoff in [`current.md`](file:///workspace/product/current.md) cited a "clean dashboard" from the earlier retry patch. Source record [`history/evidence/record-1555a62ab3.md`](file:///workspace/product/history/evidence/record-1555a62ab3.md) (dated July 26, 2026) originally reported queue retries as clean during the July 22–25 observation window. However, this observation was filtered strictly to `worker_pool=dedicated`, excluding shared tenant workers.
  * **Applicable Correction:** [`history/evidence/record-567749c82b.md`](file:///workspace/product/history/evidence/record-567749c82b.md) (dated August 12, 2026) corrected [`record-1555a62ab3`](file:///workspace/product/history/evidence/record-1555a62ab3.md), documenting that shared tenant workers experienced 31 dedupe collisions in that same July 22–25 period. The July 27 rollback remains real, and PR 781's flawed initial dashboard cannot be used to infer safety or success for PR 842.
* **PR 831 Timeout Revision:**
  * **Source:** [`history/evidence/record-b5a8ddac8f.md`](file:///workspace/product/history/evidence/record-b5a8ddac8f.md)
  * **Details:** Dated September 7, 2026. Corrected September 1–4 customer timeout counts on dedicated US workers for PR 831 to zero (four healthcheck requests had been misclassified as customer failures). The record explicitly notes that no shared EU workers or PR 842 exposure were included.

---

## 3. What the Evidence Supports Now

### A. Release and Deployment State of PR 842
* **Release Request Status:**
  * **Source:** [`history/actions/record-54bad5e8e1.md`](file:///workspace/product/history/actions/record-54bad5e8e1.md)
  * **Details:** Intent was recorded September 7, 2026 at 18:00 UTC to deploy target SHA `842cafe` to the 5% EU queue-worker canary under request identity `record-54bad5e8e1`. The submission timed out with no completion body.
  * **Service Lookup:** Performed September 8, 2026 at 09:12 UTC. The operation exists with status **`queued`** targeting `842cafe`. **Canary exposure has not started.**
  * **Idempotency:** In accordance with long-horizon practices, no duplicate release request was created.
* **Current Production Release:**
  * **Source:** [`history/releases/record-802a8b0629.json`](file:///workspace/product/history/releases/record-802a8b0629.json)
  * **Details:** Retrieved September 8, 2026 at 09:10:00 UTC. Running SHA is `840bead`, deployed September 7, 2026 at 11:00:00 UTC (receipt `record-fdd6bbaac5`). Cohorts: all queue workers. Contains PRs `[831, 835, 840]`; does not contain PR 842 (`not_contained_prs: [842]`).
  * **Finding:** Production has zero exposure to PR 842 (`842cafe`). Any apparent lack of failure reports in production is an observation of SHA `840bead`, not a validation of PR 842.

### B. Investigation of the Customer Timeout Report
* **Support Ticket:**
  * **Source:** [`history/support/record-a2d078a170.md`](file:///workspace/product/history/support/record-a2d078a170.md)
  * **Details:** Retrieved September 8, 2026 at 09:00 UTC; imported September 7, 2026 at 20:00 UTC; **`submitted_at: unknown`** (preserved as unknown).
  * **Customer Symptom:** EU shared tenant reporting that retries occasionally disappear following a timeout.
  * **Export Qualification:** The export field `age_days=5` corresponds to days elapsed since PR 842 merged (September 3), not the age of the customer submission.
* **Trace Attachment:**
  * **Source:** [`history/evidence/record-fa1b95eae5.json`](file:///workspace/product/history/evidence/record-fa1b95eae5.json)
  * **Details:** Event occurred at `2026-09-07T14:32:00Z` in region `eu` on a `shared` tenant worker running worker SHA **`840bead`**. Retry attempt 2 ended in `dedupe_collision`.
  * **Finding:** The failure occurred at 14:32 UTC on September 7, approximately 3.5 hours before the release request `record-54bad5e8e1` was even submitted (18:00 UTC), and ran on worker SHA `840bead`. This confirms that dedupe collisions on retry timeouts are an active defect in the pre-842 production baseline. It provides baseline validation of the issue PR 842 aims to resolve, and is not evidence of a flaw in PR 842.

### C. Overlapping Infrastructure Work
* **Coordination Record:**
  * **Source:** [`history/coordination/record-7b1da28762.md`](file:///workspace/product/history/coordination/record-7b1da28762.md)
  * **Details:** Action `record-f44834cc2c`, owned by `routing-quality`, is active. A production canary was planned for September 8, 2026 at 12:00 UTC to move EU shared tenants between worker pools.
  * **Cohort Overlap:** The proposed cohort overlaps directly with the canary target for `record-54bad5e8e1`.
  * **Finding:** Rollout and exposure must be coordinated. Telemetry cannot treat before-and-after retry counts as a clean comparison without accounting for worker pool movements.

---

## 4. Next Useful Action

1. **Maintain Active Watch (Do Not Terminate):**
   * Keep the monitoring responsibility open. Do not mark the task closed based on quiet production signals or stale dashboard assumptions.
2. **Track Queued Release (`record-54bad5e8e1`):**
   * Retain the existing stable request identity `record-54bad5e8e1`.
   * Continue monitoring the release service until the queued operation transitions to active deployment and achieves confirmed exposure on the 5% EU queue-worker canary.
   * Obtain and retain the deployment receipt once executed.
3. **Coordinate with `routing-quality` (Action `record-f44834cc2c`):**
   * Coordinate the September 8 12:00 UTC routing canary with the PR 842 canary rollout. Ensure tenant routing shifts are isolated from retry deduplication telemetry so observation cohorts remain distinct and comparable.
4. **Conduct Post-Exposure Canary Observation:**
   * Once canary exposure for SHA `842cafe` is verified in the EU shared tenant pool, begin a dedicated observation window.
   * Measure dedupe collision rates and timeout retries specifically against the pre-PR 842 baseline established by trace [`record-fa1b95eae5`](file:///workspace/product/history/evidence/record-fa1b95eae5.json).

---

## 5. Important Uncertainty

1. **Deployment Execution Timing:**
   * The release operation for `record-54bad5e8e1` remains in `queued` status as of September 8 09:12 UTC. When the automated deployment pipeline will initiate and finish canary rollout is currently unknown.
2. **Customer Ticket Submission Timestamp:**
   * In [`record-a2d078a170`](file:///workspace/product/history/support/record-a2d078a170.md), `submitted_at` is unknown. Although trace [`record-fa1b95eae5`](file:///workspace/product/history/evidence/record-fa1b95eae5.json) established the event timestamp (`2026-09-07T14:32:00Z`) and import occurred at `2026-09-07T20:00 UTC`, the ticket submission timestamp remains unknown.
3. **Routing Canary Execution and Impact (`record-f44834cc2c`):**
   * The routing canary was scheduled for September 8 at 12:00 UTC. Whether it was deployed on schedule, delayed, or cancelled will determine whether the EU shared tenant worker pool was restructured during the canary window.
4. **Canary Cohort Volume:**
   * The 5% canary cohort size may yield a lower volume of retry attempts compared to full rollout. The observation window must be long enough to observe sufficient retry events to confirm the absence of dedupe collisions with statistical confidence.
