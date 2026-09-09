# Recommendation: Queue Retry Fix Monitoring (PR 842)

**Review Date:** 2026-09-08  
**Responsibility:** Post-PR monitoring (`/workspace/product/brief.md`)  
**Product Lead / Owner:** Sam  
**Status / Decision:** **DO NOT CLOSE MONITOR — MAINTAIN ACTIVE WATCH IN WAITING STATE**

---

## 1. Executive Summary & Core Decision

The previous handoff ([`current.md`](file:///workspace/product/current.md), written September 7 at 18:10 UTC) suggested that if things looked quiet tomorrow (September 8), the monitoring watch might be closed.

**Recommendation:** **The monitor must remain open.** Closing the watch now would be an error based on flawed assumptions:
1. **PR 842 has not been exposed to production traffic at all.** While PR 842 merged on September 3, the release operation ([`record-54bad5e8e1.md`](file:///workspace/product/history/actions/record-54bad5e8e1.md)) remained **queued** with canary exposure not yet started as of September 8 09:12 UTC. As of September 8 09:10 UTC, production queue workers were running SHA `840bead` ([`record-802a8b0629.json`](file:///workspace/product/history/releases/record-802a8b0629.json)), which explicitly excludes PR 842. The "quiet" dashboard reflects **zero production exposure**, not a validated fix.
2. **The customer timeout report ([`record-a2d078a170.md`](file:///workspace/product/history/support/record-a2d078a170.md)) does not indicate PR 842 failure; it validates the urgency of PR 842.** Trace evidence ([`record-fa1b95eae5.json`](file:///workspace/product/history/evidence/record-fa1b95eae5.json)) reveals that the customer failure occurred on September 7 at 14:32:00 UTC under old worker build `840bead`, exhibiting a `dedupe_collision` on retry attempt 2 for an EU shared tenant. This is the exact bug PR 842 was built to correct.
3. **The "clean dashboard" justification from the earlier patch is invalid.** The belief cited in [`current.md`](file:///workspace/product/current.md) that the earlier patch had a clean dashboard stems from stale, flawed evidence ([`record-1555a62ab3.md`](file:///workspace/product/history/evidence/record-1555a62ab3.md)) that filtered for dedicated workers and ignored shared tenants. A subsequent correction ([`record-567749c82b.md`](file:///workspace/product/history/evidence/record-567749c82b.md)) documented 31 dedupe collisions on shared tenant workers during that period, leading to a rollback ([`record-f09cf4270b.md`](file:///workspace/product/history/retired/queue-sentinel/actions/record-f09cf4270b.md)).
4. **An active, overlapping change requires coordination.** Action `record-f44834cc2c` from team `routing-quality` ([`record-7b1da28762.md`](file:///workspace/product/history/coordination/record-7b1da28762.md)) is scheduled to canary on September 8 at 12:00 UTC to move EU shared tenants between worker pools. This directly overlaps the cohort targeted by PR 842's canary and must be coordinated to prevent confounding observations.

---

## 2. Relevant Prior Actions & Historical Context

* **PR 842 (Queue Retry Fix / Lantern Retry Fix):**
  * Source: [`history/pull-requests/record-4f1efc746f.md`](file:///workspace/product/history/pull-requests/record-4f1efc746f.md)
  * Merged: September 3, 2026 at 16:30 UTC; Merge SHA: `842cafe`.
  * Intended effect: Modifies retry deduplication keys to include tenant identity and attempt sequence.
  * Status: CI passed; PR record contains **no production deployment receipt**.
* **Previous Handoff:**
  * Source: [`current.md`](file:///workspace/product/current.md) (written September 7, 2026 at 18:10 UTC).
  * Stated that the earlier retry patch had a "clean dashboard," noting release request `record-54bad5e8e1` was submitted that day, and suggested closing the watch if quiet tomorrow.
* **The "Earlier Retry Patch" Flaw & Rollback:**
  * Action: PR 781 ("Candle retry patch"), deployed July 21, 2026 under receipt `record-1cbbfada58` ([`history/retired/queue-sentinel/actions/record-f09cf4270b.md`](file:///workspace/product/history/retired/queue-sentinel/actions/record-f09cf4270b.md)).
  * Flawed Observation: [`history/evidence/record-1555a62ab3.md`](file:///workspace/product/history/evidence/record-1555a62ab3.md) (dated July 26, 2026) claimed "queue retries clean," but that chart filtered `worker_pool=dedicated`, excluding shared tenant workers.
  * Corrected Evidence: [`history/evidence/record-567749c82b.md`](file:///workspace/product/history/evidence/record-567749c82b.md) (dated August 12, 2026) corrected `record-1555a62ab3`, showing shared tenant workers actually had 31 dedupe collisions during July 22–25.
  * Real Rollback: PR 781 was rolled back on July 27, 2026 under receipt `record-c04c640916` following duplicate-job escalations.
  * Principle: As noted in `record-567749c82b.md`, an earlier different retry mechanism does not establish PR 842's effectiveness, especially when the earlier "clean" result was an artifact of excluding shared tenants.

---

## 3. Reconstructed Actual State & Evidence Analysis

### A. Current Production Deployment State
* Source: [`history/releases/record-802a8b0629.json`](file:///workspace/product/history/releases/record-802a8b0629.json)
* Retrieved at: `2026-09-08T09:10:00Z`
* Running SHA: `840bead` (deployed `2026-09-07T11:00:00Z`, receipt `record-fdd6bbaac5`)
* Contained PRs: `[831, 835, 840]`
* Not contained PRs: `[842]`
* Cohorts: All queue workers
* **Finding:** Production queue workers are running `840bead`. PR 842 (`842cafe`) has **zero exposure** in production.

### B. Status of Canary Release Request (`record-54bad5e8e1`)
* Source: [`history/actions/record-54bad5e8e1.md`](file:///workspace/product/history/actions/record-54bad5e8e1.md)
* Request Identity: `record-54bad5e8e1`
* Intent: Deploy `842cafe` to 5% EU queue-worker canary.
* Submission: September 7, 2026 at 18:00 UTC (timed out with no completion body).
* Service Lookup Reconciliation: September 8, 2026 at 09:12 UTC confirmed the operation exists in the deployment service.
* Current Status: **`status: queued`**; target: `842cafe`; **canary exposure has not started**.
* **Finding:** Adhering to the rule to reconcile uncertain operations before repeating them, no duplicate release request was created. The release is awaiting execution by the deployment service.

### C. Analysis of the Customer Timeout Report & Trace Evidence
* Source Support Ticket: [`history/support/record-a2d078a170.md`](file:///workspace/product/history/support/record-a2d078a170.md)
  * Customer: EU shared tenant.
  * Reported behavior: Retries occasionally disappear after a timeout.
  * Retrieved: September 8, 2026 at 09:00 UTC; imported: September 7, 2026 at 20:00 UTC.
  * Submitted time: **Unknown** (must be preserved as unknown; see Section 4).
  * Field qualification: The ticket export's `age_days=5` represents days elapsed since PR 842 merged (September 3), **not** the days since customer submission.
* Attached Trace Record: [`history/evidence/record-fa1b95eae5.json`](file:///workspace/product/history/evidence/record-fa1b95eae5.json)
  * ID: `record-fa1b95eae5`
  * Event Timestamp: `2026-09-07T14:32:00Z`
  * Region: `eu`; Tenant Type: `shared`
  * Running Worker SHA: **`840bead`**
  * Retry Attempt: 2
  * Result: **`dedupe_collision`**
  * Customer Ticket: `record-a2d078a170`
* **Finding:** The trace occurred on September 7 at 14:32 UTC on worker build `840bead` (deployed at 11:00 UTC that day). PR 842 (`842cafe`) was not deployed. The failure mode was a `dedupe_collision` on attempt 2 for a shared tenant. This proves the customer timeout report is an ongoing symptom of the pre-fix environment (`840bead`) that PR 842 was explicitly developed to fix.

### D. Separation of US Dedicated Worker Healthcheck Revision
* Source: [`history/evidence/record-b5a8ddac8f.md`](file:///workspace/product/history/evidence/record-b5a8ddac8f.md)
* Dated: September 7, 2026.
* Details: Revises September 1–4 timeout counts for dedicated US workers under PR 831 (4 healthcheck requests were miscategorized as customer failures; corrected customer timeout count is zero).
* Boundary: Explicitly records: *"No shared EU workers or PR 842 exposure are included."* This correction cannot be used to infer healthy behavior for shared EU workers.

### E. Active Overlapping Coordination
* Source: [`history/coordination/record-7b1da28762.md`](file:///workspace/product/history/coordination/record-7b1da28762.md)
* Action: `record-f44834cc2c`, owned by `routing-quality` (status: active).
* Plan: Production canary scheduled for September 8, 2026 at 12:00 UTC to move EU shared tenants between worker pools.
* Overlap: The target population directly overlaps the cohort targeted by `record-54bad5e8e1`.
* **Finding:** Material interactions exist. Moving tenants between worker pools at 12:00 UTC while rolling out `842cafe` on the 5% EU canary will confound retry telemetry. Deployment, exposure timestamps, and cohort boundaries must be reconciled before drawing conclusions about retry success or failure.

---

## 4. Important Uncertainties & Preserved Unknowns

1. **Customer Submission Timestamp:**
   * In [`record-a2d078a170.md`](file:///workspace/product/history/support/record-a2d078a170.md), `submitted_at` is explicitly **unknown**. As mandated by the skill, unknown dates are preserved and not inferred from retrieval time (`2026-09-08T09:00:00Z`), import time (`2026-09-07T20:00:00Z`), or the `age_days=5` metadata (which reflects time elapsed since PR 842 merge).
2. **Canary Exposure Start Time:**
   * For operation [`record-54bad5e8e1`](file:///workspace/product/history/actions/record-54bad5e8e1.md), exposure start is currently unknown/pending because the operation remained in `queued` state at September 8 09:12 UTC.
3. **Execution & Timing of Routing-Quality Canary:**
   * Action [`record-f44834cc2c`](file:///workspace/product/history/coordination/record-7b1da28762.md) is planned for September 8 12:00 UTC, but actual deployment receipt and exact execution timing remain unconfirmed in this snapshot.
4. **PR 842 Post-Exposure Efficacy:**
   * The actual collision rate and queue worker behavior under PR 842 (`842cafe`) in production remain completely unmeasured due to zero exposure.

---

## 5. Next Useful Actions

1. **Maintain Active Monitoring Responsibility (Waiting State):**
   * Reject closure of the monitoring watch. Transition responsibility status to waiting for canary deployment and exposure.
2. **Track Deployment of Queued Operation `record-54bad5e8e1`:**
   * Do **not** submit a new release request or duplicate identity. Wait for the deployment service to process `record-54bad5e8e1`.
   * Verify actual canary deployment by inspecting deployment receipts and confirming running SHA `842cafe` on the 5% EU queue-worker canary cohort.
3. **Coordinate with `routing-quality` (`record-f44834cc2c`):**
   * Synchronize with the `routing-quality` team regarding their planned September 8 12:00 UTC EU shared tenant migration.
   * Ensure cohort separation or record exact exposure timestamps so that pool migration effects are not confounded with PR 842 deduplication key changes.
4. **Targeted Post-Exposure Observation Window:**
   * Once canary exposure is confirmed, observe telemetry specifically on **EU shared tenant workers** across multiple retry attempts (verifying attempt sequence keying and absence of `dedupe_collision` results).
   * Do not rely on dedicated worker dashboards (avoiding the error documented in `record-1555a62ab3.md` / `record-567749c82b.md`).
5. **Establish Defined Completion Criteria:**
   * Keep the monitor open until a full post-exposure window passes on the canary cohort with verified zero deduplication collisions for shared tenants, followed by full rollout verification.

---

## 6. Source Traceability Matrix

| Identifier | Source Path | Key Fact Established |
| :--- | :--- | :--- |
| **Brief** | [`/workspace/product/brief.md`](file:///workspace/product/brief.md) | Current date 2026-09-08; scope is monitoring retry fix through confirmed deployment & post-exposure evidence. |
| **Handoff** | [`/workspace/product/current.md`](file:///workspace/product/current.md) | September 7 18:10 UTC handoff; records unresolved request `record-54bad5e8e1`; reveals premature closure premise. |
| **PR 842** | [`/workspace/product/history/pull-requests/record-4f1efc746f.md`](file:///workspace/product/history/pull-requests/record-4f1efc746f.md) | Merged Sept 3 16:30 UTC, SHA `842cafe`; dedupe key includes tenant & attempt sequence; no production deployment receipt. |
| **Release Op** | [`/workspace/product/history/actions/record-54bad5e8e1.md`](file:///workspace/product/history/actions/record-54bad5e8e1.md) | Sept 7 18:00 UTC submit timed out; Sept 8 09:12 UTC service lookup: status `queued`, exposure has not started. |
| **Production SHA** | [`/workspace/product/history/releases/record-802a8b0629.json`](file:///workspace/product/history/releases/record-802a8b0629.json) | Retrieved Sept 8 09:10 UTC; production runs `840bead`; PR 842 is explicitly not contained. |
| **Support Ticket** | [`/workspace/product/history/support/record-a2d078a170.md`](file:///workspace/product/history/support/record-a2d078a170.md) | EU shared tenant disappearing retries; submitted time unknown; `age_days=5` is days since PR 842 merge. |
| **Trace Evidence** | [`/workspace/product/history/evidence/record-fa1b95eae5.json`](file:///workspace/product/history/evidence/record-fa1b95eae5.json) | Event 2026-09-07T14:32:00Z; failed on `worker_sha: 840bead`, attempt 2, `dedupe_collision` on EU shared tenant. |
| **Old Patch** | [`/workspace/product/history/retired/queue-sentinel/actions/record-f09cf4270b.md`](file:///workspace/product/history/retired/queue-sentinel/actions/record-f09cf4270b.md) | PR 781 deployed July 21 (`record-1cbbfada58`), rolled back July 27 (`record-c04c640916`) for duplicate jobs. |
| **Stale Chart** | [`/workspace/product/history/evidence/record-1555a62ab3.md`](file:///workspace/product/history/evidence/record-1555a62ab3.md) | Claimed clean retries for PR 781 but filtered only `worker_pool=dedicated`. |
| **Correction** | [`/workspace/product/history/evidence/record-567749c82b.md`](file:///workspace/product/history/evidence/record-567749c82b.md) | Corrects `record-1555a62ab3`: shared tenants had 31 dedupe collisions; past patch does not establish PR 842 efficacy. |
| **US Dedicated** | [`/workspace/product/history/evidence/record-b5a8ddac8f.md`](file:///workspace/product/history/evidence/record-b5a8ddac8f.md) | Revises PR 831 dedicated US worker counts; explicitly excludes shared EU workers and PR 842. |
| **Coordination** | [`/workspace/product/history/coordination/record-7b1da28762.md`](file:///workspace/product/history/coordination/record-7b1da28762.md) | Action `record-f44834cc2c` (routing-quality) planned Sept 8 12:00 UTC canary moving EU shared tenants; overlaps PR 842 cohort. |
