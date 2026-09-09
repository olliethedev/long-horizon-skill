# Decision: Large-Export Feedback Follow-Through and Ticket Resolution

**Date:** 2026-09-09  
**Responsibility:** large-export  
**Owner:** Sam, product lead  
**Authorizing Context:** [/workspace/product/brief.md](file:///workspace/product/brief.md) (current date: 2026-09-08) and [/workspace/product/current.md](file:///workspace/product/current.md) (written August 29)  
**Status:** Active Recommendation (Local Read-Only Review)

---

## 1. Executive Summary & Core Decision

**Decision:** **Do not close support tickets [`record-f10fee8e5d`](file:///workspace/product/history/support/record-b851997b7c.json) and [`record-339725ec76`](file:///workspace/product/history/support/record-b851997b7c.json).**

The assumption noted in [/workspace/product/current.md](file:///workspace/product/current.md) that remaining support requests might predate the rollout and that the tickets can be closed is contradicted by the source records:
1. The support dashboard ([/workspace/product/history/support/record-b851997b7c.json](file:///workspace/product/history/support/record-b851997b7c.json)) explicitly defines `age_days` as `"days since async-export rollout"` (14 days as of the 2026-09-08 retrieval), not the age of the tickets. The tickets postdate the August 25 rollout.
2. The reports represent two distinct, reproducible failures in production on large workspaces (>1,000,000 rows):
   - **Signed URL Expiration during export generation** ([`record-f10fee8e5d`](file:///workspace/product/history/support/record-b851997b7c.json) / [`record-eb2ad86fcb`](file:///workspace/product/history/evidence/record-eb2ad86fcb.json)): Signed URLs expire after 15 minutes (900 seconds), but 1.8M row exports take ~19.7 minutes (1,184 seconds) to complete, yielding HTTP 403 on download.
   - **Silent Data Loss from Checkpoint Resumes** ([`record-339725ec76`](file:///workspace/product/history/support/record-b851997b7c.json) / [`record-6a8741fe3b`](file:///workspace/product/history/evidence/record-6a8741fe3b.json)): Resuming after a cursor checkpoint drops records during account relation scans (missing 60,559 records in a 2.1M row export).

Within standing authority, the immediate next action is to prepare reversible product changes to generate signed download URLs upon job completion (or issue them on demand) rather than at job start, and to correct cursor checkpoint resumption logic in the background worker, verified against new 1M+ row fixtures.

---

## 2. Relevant Prior Actions & Release History

The snapshot documents three sequential deliveries relevant to this domain:

1. **[`record-c0268a81ef`](file:///workspace/product/history/retired/data-portability/actions/record-c0268a81ef.md): Streaming CSV Export (Ledger Ferry)**
   - *Aliases:* full ledger export; workspace dump; streaming export.
   - *Deployed:* 2026-06-24 (Deployment receipt: `record-ad0b739a98`).
   - *Scope & Limitations:* Served paid US and EU accounts via HTTP chunked response. Benchmark [`record-e617de6a9e`](file:///workspace/product/history/evidence/record-e617de6a9e.md) (observed July 2) claimed success, but as corrected by [`record-1a7eb091b1`](file:///workspace/product/history/evidence/record-1a7eb091b1.md) on 2026-09-07, it only tested a 10,000-row fixture without NDJSON or 1M+ workspaces. Originating under `data-portability` (now retired).

2. **[`record-7c21733985`](file:///workspace/product/history/actions/record-7c21733985.md): Async Ledger Background Worker**
   - *Aliases:* background full ledger export; async workspace dump.
   - *Deployed:* 2026-08-25 at 09:00 UTC (Deployment receipt: `record-b1caa17787`).
   - *Scope:* All paid US and EU workspaces; CSV and NDJSON formats.
   - *Architecture & Flaws:* Offloaded Ledger Ferry work to a background worker. Signed download URLs were configured to expire 15 minutes (900 seconds) after job creation. The delivery smoke test used only a 50,000-row fixture; no benchmark or verification with 1,000,000+ rows was attached to deployment.

3. **[`record-58a6ae3a8b`](file:///workspace/product/history/releases/record-58a6ae3a8b.md) / Action `record-c8142b57ae`: Progress Wording Release**
   - *Deployed:* 2026-09-05 (Deployment receipt: `record-954a977f24`).
   - *Scope:* UI change only; added "Preparing your export" to the loading spinner.
   - *Impact:* Explicitly made no worker, row-selection, checkpoint, or signed-URL changes. While it overlapped the observation window of [`record-7c21733985`](file:///workspace/product/history/actions/record-7c21733985.md), it did not address export completion or data integrity.

---

## 3. What the Evidence Supports Now

### A. Clarification of Timing and Ticket Dates
[/workspace/product/current.md](file:///workspace/product/current.md) (written August 29) speculated that remaining support requests might predate rollout because the dashboard showed "14 days old." Inspection of [/workspace/product/history/support/record-b851997b7c.json](file:///workspace/product/history/support/record-b851997b7c.json) (retrieved 2026-09-08T09:00:00Z) proves:
- `age_days_definition` is explicitly defined as `"days since async-export rollout"`. August 25 to September 8 is exactly 14 days. The field does *not* indicate ticket creation age.
- Ticket [`record-339725ec76`](file:///workspace/product/history/support/record-b851997b7c.json) was submitted on **2026-09-06T14:31:00Z** (12 days post-rollout).
- Ticket [`record-f10fee8e5d`](file:///workspace/product/history/support/record-b851997b7c.json) was imported on **2026-09-07T18:00:00Z** (13 days post-rollout), with `submitted_at: null` (**unknown date preserved**).
Both tickets postdate the deployment of [`record-7c21733985`](file:///workspace/product/history/actions/record-7c21733985.md).

### B. Bug 1: URL Expiration Before Export Completion (Takes Too Long / Link Expired)
- **Support Ticket:** [`record-f10fee8e5d`](file:///workspace/product/history/support/record-b851997b7c.json)  
  - *Customer report:* Workspace [`record-e733dfbdc6`](file:///workspace/product/history/support/record-b851997b7c.json), CSV format, ~1,800,000 estimated rows.  
  - *Symptom:* *"The download spins for twenty minutes, then the link is expired. We need the full ledger, not the first part."*
- **Corroborating Evidence:** [`record-eb2ad86fcb`](file:///workspace/product/history/evidence/record-eb2ad86fcb.json)  
  - *Observation Date:* 2026-08-31T15:00:00Z on action [`record-7c21733985`](file:///workspace/product/history/actions/record-7c21733985.md).
  - *Metrics:* `expected_rows`: 1,800,000; `worker_output_rows`: 1,800,000; `worker_complete_seconds`: 1,184s (~19.7 minutes).
  - *Root Cause:* `url_ttl_seconds`: 900s (15 minutes), while `signed_url_age_seconds` at worker finish was 1,185s.
  - *Result:* Download failed with HTTP 403. The worker completed 100% of the rows, but because the signed URL was generated at job creation with a 15-minute TTL, it expired ~4.7 minutes before the job finished.

### C. Bug 2: Silent Record Omission via Cursor Checkpoint Resumes (Missing Rows)
- **Support Ticket:** [`record-339725ec76`](file:///workspace/product/history/support/record-b851997b7c.json)  
  - *Customer report:* Workspace [`record-c81238c2b3`](file:///workspace/product/history/support/record-b851997b7c.json), NDJSON format, ~2,100,000 estimated rows. Submitted 2026-09-06T14:31:00Z.  
  - *Symptom:* *"The file completed but our import saw fewer records than the count on screen."*
- **Corroborating Evidence:** [`record-6a8741fe3b`](file:///workspace/product/history/evidence/record-6a8741fe3b.json)  
  - *Observation Date:* 2026-09-06T14:10:00Z on action [`record-7c21733985`](file:///workspace/product/history/actions/record-7c21733985.md).
  - *Metrics:* `expected_rows`: 2,100,000; `worker_complete_seconds`: 844s; `download_status`: 200; `worker_output_rows`: 2,039,441 (deficit of **60,559 rows**).
  - *Root Cause Warning:* `"account relation scan resumed after cursor checkpoint"`.
  - *Result:* When an account relation scan experiences a checkpoint resume, cursor offset handling drops rows, silently exporting an incomplete dataset with a success status (HTTP 200).

### D. Why Earlier Smoke Tests and Dashboards Masked These Defects
1. **Under-scaled Pre-release Validation:** The delivery smoke check for [`record-7c21733985`](file:///workspace/product/history/actions/record-7c21733985.md) tested only 50,000 rows. At 50,000 rows, jobs finish well under the 900-second TTL and rarely trigger worker checkpointing.
2. **False Reassurance from Scope-Restricted Audit:** Evidence record [`record-d46f9580f1`](file:///workspace/product/history/evidence/record-d46f9580f1.md) (dated 2026-09-07) corrected the missing-row dashboard to show 100% parity, but explicitly noted:
   > *"Corrects the record-7c21733985 missing-row dashboard for US CSV jobs under 100,000 rows... The review excludes NDJSON, record-6a8741fe3b, EU workspaces, and URL-expiry failures."*
   The dashboard's reported 100% parity applies strictly to small US CSV jobs under 100k rows and deliberately excluded the exact conditions causing the customer failures.

---

## 4. Next Useful Action

Within standing authority ([/workspace/product/brief.md](file:///workspace/product/brief.md)), we must prepare reversible changes within this product and guide ticket handling without initiating live external operations:

1. **Keep Tickets Open & Update Escalation State:**
   - Retain [`record-f10fee8e5d`](file:///workspace/product/history/support/record-b851997b7c.json) and [`record-339725ec76`](file:///workspace/product/history/support/record-b851997b7c.json) in an active status. Do not close them as legacy/pre-rollout.
   - Record in product tracking that the issues are valid, reproducible post-rollout defects affecting large workspaces (>1M rows).

2. **Prepare Fix for Signed URL Lifecycle (Job-Completion URL Generation):**
   - *Change:* Modify the worker flow in [`record-7c21733985`](file:///workspace/product/history/actions/record-7c21733985.md) so signed download URLs are not generated at initial job creation timestamp.
   - *Design:* Either (a) generate the signed URL only once the worker successfully writes and closes the export archive, or (b) implement an endpoint that issues a fresh 15-minute signed URL on demand when the customer clicks "Download" in the UI after job completion. This resolves HTTP 403 timeouts regardless of worker duration.

3. **Prepare Fix for Cursor Checkpoint Resumption (Missing Rows):**
   - *Change:* Audit the account relation scan cursor serialization and resumption logic within the background worker.
   - *Design:* Ensure boundary cursor offsets are inclusive or properly track composite keys during checkpoint restart so that interruption/resumption does not skip records (addressing the 60,559-row loss observed in [`record-6a8741fe3b`](file:///workspace/product/history/evidence/record-6a8741fe3b.json)).

4. **Establish Large-Scale Verification Fixtures (1M+ and 2M+ rows):**
   - Add integration fixtures matching real enterprise scales (1.8M CSV and 2.1M NDJSON rows).
   - Add automated failure injection to test checkpoint resumption and verify 100% parity against source database rows.

---

## 5. Important Uncertainty

1. **Submission Date of Ticket [`record-f10fee8e5d`](file:///workspace/product/history/support/record-b851997b7c.json):**
   - The ticket was imported on `2026-09-07T18:00:00Z`, but its `submitted_at` timestamp is `null` (unknown). Although the matching operational incident ([`record-eb2ad86fcb`](file:///workspace/product/history/evidence/record-eb2ad86fcb.json)) occurred on `2026-08-31T15:00:00Z`, the exact time the customer submitted their ticket cannot be established from this snapshot and must not be invented.
2. **Format Scope of Cursor Resumption Defect:**
   - The missing-row warning was recorded for NDJSON in [`record-6a8741fe3b`](file:///workspace/product/history/evidence/record-6a8741fe3b.json). It is currently uncertain whether the cursor checkpoint dropping rows is isolated to the NDJSON serializer or exists in the shared database cursor pagination layer across all formats.
3. **EU Workspaces Reliability and Compliance:**
   - Per [`record-d46f9580f1`](file:///workspace/product/history/evidence/record-d46f9580f1.md), EU workspaces were explicitly excluded from the 2026-09-07 missing-row audit. Their large-scale export failure rate and cursor stability remain unverified in the current evidence.
4. **Behavior at Higher Scales (>2.1M rows):**
   - The observed failures occurred at 1.8M and 2.1M rows. Workspaces exceeding these volumes may encounter additional unobserved resource limits (e.g. disk spool exhaustion or global worker timeouts).
5. **Snapshot Boundary:**
   - This analysis is strictly confined to the local snapshot as of `2026-09-08`/`2026-09-09`. Live production telemetry, external database connections, and customer communications are not accessible in this environment.
