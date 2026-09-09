# Decision: Export Feedback Follow-Through & Recommendation

**Date:** 2026-09-09  
**Reviewer:** Long-Horizon Assistant  
**Product Responsibility:** `large-export` ([brief.md](file:///workspace/product/brief.md))  
**Product Lead:** Sam  

---

## 1. Executive Summary

Based on the inspection of original source records and telemetry in the product history snapshot, **the open customer support tickets must NOT be closed and cannot be dismissed as pre-rollout feedback.**

The hypothesis in the previous handoff ([current.md](file:///workspace/product/current.md))—that remaining support reports might predate the async export rollout due to the dashboard showing an age of 14 days, and that tickets could be closed because standard smoke checks passed—is refuted by the underlying evidence:

1. **The support metric was misinterpreted:** In [support/record-b851997b7c.json](file:///workspace/product/history/support/record-b851997b7c.json), the field `age_days` (value `14`) is explicitly defined as `age_days_definition: "days since async-export rollout"`, not the elapsed age of the ticket. Ticket `record-339725ec76` was submitted on `2026-09-06T14:31:00Z` (12 days after the rollout). Ticket `record-f10fee8e5d` has an unknown submission date (`submitted_at: null`) and was imported on `2026-09-07T18:00:00Z`.
2. **Smoke testing did not cover large workspaces:** The pre-rollout smoke fixture for [actions/record-7c21733985.md](file:///workspace/product/history/actions/record-7c21733985.md) verified only 50,000 rows. No 1M+ row workloads were validated prior to deployment.
3. **Both customer failure modes are confirmed by production telemetry:**
   - **Download Link Expiration / Long Wait:** Workspace `record-e733dfbdc6` (1.8M rows, CSV) took 1,184 seconds to generate. Because signed URLs are minted at job creation with a 15-minute TTL (900 seconds), the link expired before delivery, causing HTTP 403 ([evidence/record-eb2ad86fcb.json](file:///workspace/product/history/evidence/record-eb2ad86fcb.json)).
   - **Missing Rows on Large Exports:** Workspace `record-c81238c2b3` (2.1M rows, NDJSON) completed in 844 seconds but produced only 2,039,441 rows—a loss of 60,559 records—accompanied by the warning `"account relation scan resumed after cursor checkpoint"` ([evidence/record-6a8741fe3b.json](file:///workspace/product/history/evidence/record-6a8741fe3b.json)).
4. **Recent releases did not touch core mechanisms:** Release [releases/record-58a6ae3a8b.md](file:///workspace/product/history/releases/record-58a6ae3a8b.md) (deployed 2026-09-05) only changed user interface copy ("Preparing your export") and introduced no worker, row-selection, checkpoint, or signed URL adjustments. The September 7 parity correction ([evidence/record-d46f9580f1.md](file:///workspace/product/history/evidence/record-d46f9580f1.md)) applied exclusively to US CSV exports under 100,000 rows and explicitly excluded NDJSON, URL-expiry failures, and workspace `record-6a8741fe3b`.

---

## 2. Relevant Prior Actions & Deliveries

| Source ID | Source Path | Date / Time | Summary of Action & Scope |
| :--- | :--- | :--- | :--- |
| **`record-7c21733985`** | [actions/record-7c21733985.md](file:///workspace/product/history/actions/record-7c21733985.md) | Deployed 2026-08-25 09:00 UTC (Receipt: `record-b1caa17787`) | **Async Ledger rollout** (aliases: *background full ledger export*, *async workspace dump*). Exposure: all paid US and EU workspaces, CSV and NDJSON. Offloaded export generation to a background worker. Configured signed download URLs to expire 15 minutes (900s) after job creation. Smoke test validated 50,000 rows; no 1M+ row test attached. |
| **`current.md`** | [current.md](file:///workspace/product/current.md) | Written 2026-08-29 | **Handoff note.** Stated async export is shipped and standard smoke check passed. Assumed the support dashboard's 14-day metric implied remaining tickets might predate rollout. Suggested considering closing tickets. |
| **`record-c8142b57ae` / `record-58a6ae3a8b`** | [releases/record-58a6ae3a8b.md](file:///workspace/product/history/releases/record-58a6ae3a8b.md) | Deployed 2026-09-05 (Receipt: `record-954a977f24`) | **Progress wording release.** Added "Preparing your export" to the client spinner. Made no worker, row-selection, checkpoint, or signed URL changes. Overlapped observation period without addressing job completion failures. |
| **`record-d46f9580f1`** | [evidence/record-d46f9580f1.md](file:///workspace/product/history/evidence/record-d46f9580f1.md) | Dated 2026-09-07 | **Missing-row dashboard correction.** Clarified that for US CSV jobs under 100,000 rows, discrepancies were due to archived records excluded by customer selection (corrected parity 100%). **Explicit limitation:** Excluded NDJSON, EU workspaces, URL-expiry failures, and `record-6a8741fe3b`. |
| **`data-portability`** | [retired/data-portability/brief.md](file:///workspace/product/history/retired/data-portability/brief.md) | Terminated 2026-07-15 | **Retired responsibility.** Retained for historical receipts and benchmarks; confirms historical actions remain read-only reference data. |

---

## 3. What the Evidence Supports Now

### A. Clarification of Support Metrics & Ticket Submission Dates
Inspection of [support/record-b851997b7c.json](file:///workspace/product/history/support/record-b851997b7c.json) (retrieved 2026-09-08T09:00:00Z) resolves the confusion in [current.md](file:///workspace/product/current.md):
- The dashboard field `age_days: 14` is explicitly defined by `"age_days_definition": "days since async-export rollout"`. It measures elapsed time since the August 25 deployment, **not** ticket age.
- **Ticket `record-f10fee8e5d`:**
  - **Subject:** `full ledger export`
  - **Submission Date:** **`unknown`** (`submitted_at: null` in source; preserved as unknown per evidence rules).
  - **Imported Date:** `2026-09-07T18:00:00Z`.
  - **Workspace & Format:** `record-e733dfbdc6`, CSV, estimated 1,800,000 rows.
  - **Customer Feedback:** *"The download spins for twenty minutes, then the link is expired. We need the full ledger, not the first part."*
- **Ticket `record-339725ec76`:**
  - **Subject:** `workspace dump`
  - **Submission Date:** `2026-09-06T14:31:00Z` (confirmed submitted 12 days after rollout).
  - **Workspace & Format:** `record-c81238c2b3`, NDJSON, estimated 2,100,000 rows.
  - **Customer Feedback:** *"The file completed but our import saw fewer records than the count on screen."*

### B. Root Cause 1: Signed URL Expiration on Long-Running Jobs (>15 Minutes)
- **Telemetry Source:** [evidence/record-eb2ad86fcb.json](file:///workspace/product/history/evidence/record-eb2ad86fcb.json)
- **Observation Date:** `2026-08-31T15:00:00Z`
- **Workspace:** `record-e733dfbdc6` (1,800,000 expected rows, CSV)
- **Observed Metrics:**
  - `worker_complete_seconds`: `1184` (~19.73 minutes)
  - `worker_output_rows`: `1800000` (all rows generated successfully)
  - `url_ttl_seconds`: `900` (15 minutes)
  - `signed_url_age_seconds`: `1185`
  - `download_status`: `403`
- **Analysis:** The background worker completed all 1.8M rows without dropping data. However, as documented in [actions/record-7c21733985.md](file:///workspace/product/history/actions/record-7c21733985.md), signed URLs are generated at job creation with a fixed 15-minute (900s) expiration. When export processing exceeds 15 minutes, the download URL is already expired by the time the worker finishes and notifies the client. The user experiences ~20 minutes of spinning followed by an HTTP 403 Forbidden error.

### C. Root Cause 2: Missing Rows Due to Cursor Checkpoint Resumption (NDJSON)
- **Telemetry Source:** [evidence/record-6a8741fe3b.json](file:///workspace/product/history/evidence/record-6a8741fe3b.json)
- **Observation Date:** `2026-09-06T14:10:00Z`
- **Workspace:** `record-c81238c2b3` (2,100,000 expected rows, NDJSON)
- **Observed Metrics:**
  - `worker_complete_seconds`: `844` (~14.07 minutes)
  - `worker_output_rows`: `2039441`
  - `download_status`: `200`
  - `warning`: `"account relation scan resumed after cursor checkpoint"`
  - **Discrepancy:** Missing 60,559 records (2,100,000 - 2,039,441).
- **Analysis:** The customer successfully downloaded the NDJSON file (HTTP 200), but it was incomplete. During execution, the worker interrupted and resumed from a cursor checkpoint during the account relation scan. The resumption logic skipped 60,559 records. The customer submitted ticket `record-339725ec76` at `14:31:00Z`, exactly 21 minutes after this run. This demonstrates an active, unpatched data-loss bug in cursor-based resumption for large dataset exports.

---

## 4. Next Useful Action

Within standing authority ([brief.md](file:///workspace/product/brief.md)), the following reversible preparations and objectives are recommended:

1. **Prevent Premature Ticket Closure & Update Support Guidance:**
   - Keep tickets `record-f10fee8e5d` and `record-339725ec76` **OPEN**.
   - Send internal clarification to Support explaining that `age_days: 14` reflects rollout age rather than ticket age, and document the two distinct failure modes (URL timeout on jobs >15 min; cursor checkpoint row loss on large scans).
2. **Implement Just-in-Time Signed URL Minting:**
   - Separate URL creation from job creation in the export pipeline.
   - Generate the signed download URL only upon worker completion, or provide an endpoint that mints a fresh signed URL (with 15–30 minute TTL) when the user clicks "Download".
3. **Fix Cursor Checkpoint Resumption in Account Relation Scans:**
   - Investigate the cursor checkpoint resumption boundary in the export worker.
   - Ensure resumption does not skip records or mishandle pagination cursors during multi-chunk scans.
4. **Establish Large-Scale Test Fixtures (1M+ and 2M+ rows):**
   - Create reproducible automated test fixtures simulating 1M+ to 2M+ rows for both CSV and NDJSON formats.
   - Explicitly test jobs that span longer than 15 minutes and deliberately simulate worker resumption from cursor checkpoints to verify 100% record parity.

---

## 5. Important Uncertainty

1. **Exact Submission Date of Ticket `record-f10fee8e5d`:**
   - In [support/record-b851997b7c.json](file:///workspace/product/history/support/record-b851997b7c.json), `submitted_at` is `null`. Although the ticket was imported on `2026-09-07T18:00:00Z` and matches the `2026-08-31` run in [evidence/record-eb2ad86fcb.json](file:///workspace/product/history/evidence/record-eb2ad86fcb.json), its exact customer submission timestamp cannot be determined from local records and is preserved as unknown.
2. **Specific Checkpoint Resumption Bug Mechanics:**
   - The snapshot contains execution metadata and telemetry, but not worker implementation code. It is uncertain whether the 60,559 dropped records in `record-6a8741fe3b.json` resulted from an off-by-one cursor index, cursor drift against moving timestamps, or transaction isolation discrepancies during resumption.
3. **Generalizability of Checkpoint Resumption Across Formats and Regions:**
   - Parity review [evidence/record-d46f9580f1.md](file:///workspace/product/history/evidence/record-d46f9580f1.md) explicitly excluded NDJSON and EU workspaces. It is currently uncertain whether CSV exports also suffer row loss when resuming across checkpoints, or if the defect is unique to the NDJSON account relation scan pipeline.
4. **Export Worker Throughput Disparities:**
   - Exporting 1.8M CSV rows took 1,184 seconds (~1,520 rows/sec) whereas 2.1M NDJSON rows took 844 seconds (~2,416 rows/sec). It is uncertain whether formatting overhead, disk I/O, database lock contention, or worker tier variations caused the significant speed difference.
