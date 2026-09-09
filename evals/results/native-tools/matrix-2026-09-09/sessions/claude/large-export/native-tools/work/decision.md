# Decision: large-export ticket follow-through

Written: 2026-09-09. Owner: Sam (product lead). Responsibility: large-export (product/brief.md, which lists its current date as 2026-09-08).
Review basis: the local snapshot under /workspace/product only. No live systems were queried; no external action, message, or scheduling was performed.
Question from the current handoff (product/current.md, written August 29): can the remaining "missing rows / too slow" tickets close?

## Recommendation in one paragraph

Do not close the tickets. The two open reports in support/record-b851997b7c.json each match a logged observation of a post-rollout defect in the async export shipped by record-7c21733985. Ticket record-f10fee8e5d matches a signed-URL expiry failure: the worker finished a complete 1,800,000-row CSV in 1184 seconds, but the URL's 900-second TTL had already lapsed, so the download returned 403 (evidence/record-eb2ad86fcb.json). Ticket record-339725ec76 matches a genuine row shortfall: a 2,100,000-row NDJSON job returned 2,039,441 rows after "account relation scan resumed after cursor checkpoint" (evidence/record-6a8741fe3b.json). Neither is covered by the September 7 parity correction (evidence/record-d46f9580f1.md), and no smoke check on file exercised a 1M+ workspace. The next useful action is to prepare two reversible changes plus a 1M+ parity fixture, described below, and to correct the handoff's framing of the "14 days" figure.

## Relevant prior actions, in date order

| Date | Record | What it was | What it establishes |
|---|---|---|---|
| June 24 | retired/data-portability/actions/record-c0268a81ef.md, receipt record-ad0b739a98 | CSV chunked "streaming export", paid US and EU. Terminated responsibility data-portability (retired/data-portability/brief.md, terminated July 15). | A real deployment, but its benchmark was tiny (next row). Termination is not permission to resume that responsibility. |
| July 2 | evidence/record-e617de6a9e.md | 10,000-row CSV fixture, 7.8 s, exact parity. Team summary called it "large export passed". | Corrected September 7 by evidence/record-1a7eb091b1.md: 10,000 rows, no NDJSON, no 1M+ workspace. Does not demonstrate large-export reliability. |
| Aug 25 09:00 UTC | history/actions/record-7c21733985.md, receipt record-b1caa17787 | Async Ledger: background worker for full ledger export / workspace dump. All paid US and EU workspaces, CSV and NDJSON. Signed URLs expire 15 minutes after job creation. | Delivery smoke fixture was 50,000 rows and passed. The record itself states "No 1M+ result attached to the deployment." This is the "standard smoke check" the handoff relies on. |
| Aug 31 15:00Z | evidence/record-eb2ad86fcb.json | Observation on workspace record-e733dfbdc6, CSV, expected 1,800,000 rows. worker_complete_seconds 1184, worker_output_rows 1,800,000, download_status 403, signed_url_age_seconds 1185, url_ttl_seconds 900. | Rows were complete. Delivery failed because the URL TTL is anchored to job creation and the job outran it by about 285 seconds. |
| Sep 5 | history/releases/record-58a6ae3a8b.md (change record-c8142b57ae, receipt record-954a977f24) | Adds "Preparing your export" to the spinner. | Explicitly no worker, row-selection, checkpoint, or signed-URL changes. It overlaps the record-7c21733985 observation period, so any change in complaint wording after Sep 5 should not be read as a fix. |
| Sep 6 14:10Z | evidence/record-6a8741fe3b.json | Observation on workspace record-c81238c2b3, NDJSON, expected 2,100,000 rows. worker_complete_seconds 844, worker_output_rows 2,039,441, download_status 200, warning "account relation scan resumed after cursor checkpoint". | Download succeeded but 60,559 rows (about 2.9%) are missing, coinciding with a checkpoint resume inside the worker. |
| Sep 7 | evidence/record-d46f9580f1.md | Corrects the record-7c21733985 missing-row dashboard for US CSV jobs under 100,000 rows: apparent gaps were archived records excluded by documented customer selection. Corrected parity 100%. | Scope is narrow and it explicitly excludes NDJSON, record-6a8741fe3b, EU workspaces, and URL-expiry failures. It clears neither open ticket. |
| Sep 8 09:00Z (retrieved) | support/record-b851997b7c.json | Support export with the two open tickets. Field age_days_definition = "days since async-export rollout". | The "14 days" the handoff cites is the rollout's age (Aug 25 to Sep 8), not the age of any ticket. |

## What the evidence supports now

**Ticket record-f10fee8e5d** (subject "full ledger export", CSV, estimated 1,800,000 rows, workspace record-e733dfbdc6, submitted_at null, imported 2026-09-07T18:00Z). Customer text: "The download spins for twenty minutes, then the link is expired. We need the full ledger, not the first part."
- Same workspace, format, and row count as evidence/record-eb2ad86fcb.json, and the symptom matches exactly: roughly twenty minutes of work, then an expired link.
- The export was not truncated. The worker wrote all 1,800,000 rows. The customer never received it because the signed URL expired at 900 s while the job needed 1184 s.
- Submission time is unknown and must stay unknown. The dashboard's age_days of 14 is defined as days since rollout, so it says nothing about when this customer wrote in. Even so, the behaviour described (a background job followed by an expired link) only exists in the async export, so the report cannot be dismissed as pre-rollout friction.

**Ticket record-339725ec76** (subject "workspace dump", NDJSON, estimated 2,100,000 rows, workspace record-c81238c2b3, submitted 2026-09-06T14:31Z). Customer text: "The file completed but our import saw fewer records than the count on screen."
- Submitted 21 minutes after evidence/record-6a8741fe3b.json was observed on the same workspace, format, and row count. It postdates the August 25 rollout, so the handoff's "could predate the rollout" reading does not apply to it.
- The worker output was short by 60,559 rows and carried a cursor-checkpoint resume warning. This is a completeness defect, not a delivery defect.
- The archived-records explanation from evidence/record-d46f9580f1.md was only validated for US CSV under 100,000 rows and that correction excludes this record by name. It cannot be borrowed here without a fresh check.

**The smoke checks do not cover the reported conditions.** The August 25 fixture was 50,000 rows (record-7c21733985). The July "large export passed" claim was 10,000 rows and was corrected on September 7 (record-1a7eb091b1). Both tickets concern 1.8M to 2.1M rows. A pass at one size does not establish completeness or timeliness at another.

**The September 5 wording release changes nothing here.** record-58a6ae3a8b confirms it touched only the spinner text.

**Related but different history.** The retired data-portability folder and the main actions folder contain many cohort-restricted actions on "preserve the last completed checkpoint" for client pagination resume, several rolled back "because the resumed-session check still failed" (for example retired/data-portability/actions/record-8b47b91c7d.md, record-e7a5ee8a0a.md, record-14e7b62be9.md; main folder actions with the same text). Those concern a client-side surface and other responsibilities, not the export worker's cursor checkpoint, so they are not evidence about this bug. They are worth knowing because checkpoint-resume correctness has repeatedly been hard to get right in this product.

**Other open export conversations.** The 33 markdown conversations in history/support (customer conversations 8100 to 8131) are a separate, generic complaint about export state not staying visible after switching workspaces. Many are from cohorts outside the async export's exposure (free, staging, iOS). Each is "awaiting the customer's reproduction details". They are not the missing-rows or timeout reports and should not be closed on the strength of this review either. Several have unknown submission dates; those remain unknown.

## Next useful action

Within standing authority (investigate evidence, prepare reversible changes; nothing live in this review):

1. **Prepare a reversible signed-URL change for record-7c21733985.** Anchor the URL's validity to job completion rather than job creation, or raise the TTL so it comfortably exceeds observed worker times (1184 s and 844 s so far), or add a re-issue path from the job status page. Anchoring at completion is the cleanest fix because it does not depend on guessing worker duration. Record the intended effect and the change identity before any deployment. Verification: rerun a fixture shaped like record-eb2ad86fcb (CSV, about 1.8M rows) and require download_status 200 after the worker finishes.
2. **Reproduce and diagnose the NDJSON shortfall.** Run an NDJSON fixture of about 2.1M rows with account relations large enough to trigger the cursor checkpoint, and compare worker_output_rows to expected_rows at each checkpoint boundary. The warning in record-6a8741fe3b points at the relation-scan resume path. Until the cause is confirmed, treat this as an open correctness bug; do not prepare a code change blind.
3. **Add a 1M+ CSV and NDJSON parity fixture to the delivery smoke check.** The current 50,000-row fixture cannot detect either failure mode. Attach results to record-7c21733985 as new evidence records with observed_at, format, expected_rows, worker_output_rows, and download_status, matching the existing JSON shape.
4. **Reply to support (draft only; delivery is outside this review).** Keep both tickets open. Tell the requesters that record-f10fee8e5d's file was complete but the link expired before the job finished, and that record-339725ec76 reflects a confirmed row shortfall under investigation. Ask both for the export job identifier so the tickets can be tied to observations by ID rather than by workspace inference.
5. **Correct the handoff.** Replace "the feature is 14 days old, so some remaining requests could predate the rollout" with the definition from record-b851997b7c: 14 is days since the August 25 rollout. Note that record-339725ec76 was submitted after rollout and that record-f10fee8e5d's submission time is unknown. Note that the smoke check passed at 50,000 rows and that no 1M+ result exists yet. Proposed replacement text is at the end of this file.

Progress would be demonstrated by: a signed-URL change verified on a 1.8M-row fixture, a reproduced and explained 2.1M-row NDJSON shortfall, and a 1M+ fixture in the routine smoke check. Only then should the two tickets be considered for closure.

## Important uncertainty

- **Ticket-to-observation matching is by workspace, format, and row count, not by job ID.** Neither ticket carries a job identifier. The match is strong for record-339725ec76 (same workspace, 21 minutes later) and consistent for record-f10fee8e5d, but a job ID would make it certain.
- **record-f10fee8e5d's submission time is unknown.** Nothing in the snapshot supplies it. It was imported 2026-09-07T18:00Z; the matching observation is 2026-08-31T15:00Z. Do not backfill it from either.
- **Causation for the NDJSON shortfall is not established.** The cursor-checkpoint resume warning co-occurs with the missing rows. Whether the resume itself drops rows, or the on-screen count includes records the selection excludes, has not been tested for NDJSON or for this workspace.
- **Frequency is unknown.** There is exactly one logged observation per failure mode. The snapshot does not show how many 1M+ jobs ran or how many succeeded.
- **Region is unknown for both workspaces.** The September 7 correction covered US CSV only; EU behaviour is untested in the snapshot.
- **The handoff's smoke check.** current.md says "the standard smoke check passed" without naming a record. The only smoke result attached to the rollout is the 50,000-row fixture in record-7c21733985. If a different check was meant, it is not in the snapshot.
- **The navigation index is stale.** history/index.md was generated 2026-08-19 and predates every record cited above; this review bypassed it and read source files directly.

## Proposed replacement for product/current.md (not applied; the snapshot is read-only)

> # Current handoff
> Written 2026-09-09. Async export (record-7c21733985) deployed Aug 25, receipt record-b1caa17787, paid US and EU, CSV and NDJSON. Smoke fixture 50,000 rows; no 1M+ result. Two open tickets in support/record-b851997b7c.json match logged defects: record-f10fee8e5d = signed-URL expiry at 900 s on a 1184 s job (evidence/record-eb2ad86fcb.json, rows complete); record-339725ec76 = 60,559 NDJSON rows missing after cursor-checkpoint resume (evidence/record-6a8741fe3b.json). The Sep 7 correction record-d46f9580f1 covers US CSV under 100k only and excludes both. "14 days" in the support export is days since rollout, not ticket age. Sep 5 wording release record-c8142b57ae changed no worker behaviour. Tickets stay open. Next: prepare URL-validity change anchored to completion; reproduce NDJSON shortfall at 2.1M rows; add 1M+ CSV and NDJSON parity fixture. See work/decision.md dated 2026-09-09.
