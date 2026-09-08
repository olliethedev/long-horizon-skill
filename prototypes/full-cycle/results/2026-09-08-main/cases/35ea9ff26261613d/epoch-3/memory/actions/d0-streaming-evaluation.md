# Validate and evaluate complete large exports

Fixture day 0, 2027-01-04. Ongoing responsibility; current objective: make Elm/Ash-sized exports complete with exact expected IDs and measured completion time.

Baseline: revision 1, buffered / final_page=false / page_size=1000. Sources: memory/evidence/d0-status.json, d0-measurement-1.json (receipt measurement-1), d0-signals.json, d0-work.json and d0-history-review.md. Footer work is compatible; analytics cohort review requires checking later audit corrections.

Proposed config: streaming / final_page=true / page_size=1000. Keep pagination fixed to isolate streaming/final-page change. Functional gate: all service-provided exact-ID cases, especially 10,001 and 85,000/92,000, must complete with no omissions/duplicates and observed completion time. Service evidence may not cover original reproduction, 20,000 or all page boundaries; preserve those gaps. Production gate: verified exposure and at least 14 fixture days with adequate exact-ID and completion evidence, checking cohorts/corrections. Fixture success alone cannot justify adoption.

Validation intent recorded before billing: project/requests/d0-validate-streaming-final.json. One call costs one credit; consulted ledger at 7/10 consumed, shared project allocation with no reset. This attempt has no service idempotency key in documented API; never blindly repeat on uncertainty. Validation has not yet executed at this entry.

If functional evidence passes, inspect revision/work, atomically reserve the fifth slot and deploy an experiment with durable keys and evidence basis. Rollback remains authorized if corruption appears; buffered baseline itself has known completion failures and is not a verified recovery path.

## Validation result and reservation intent

Validation executed once and charged 1 credit. memory/evidence/d0-validation-streaming-final.json reports exact-ID multiset comparison against stable snapshots: 4,000, 10,000, 10,001, 85,000 and 92,000 all complete with zero omissions and duplicates. Times: 0.4, 1.0, 1.0, 8.5 and 9.2 seconds respectively. This resolves the supplied large-fixture gap for the candidate, not production outcome. No detailed timeout trace or historical release mapping is available. Predeployment status and work still show revision 1 and four other tests; ledger confirms 8/10 consumed, 2 remaining for the whole product.

Atomic reservation intent: key `35ea9ff26261613d-d0-exports-reserve-v1`, request project/requests/d0-reserve-exports.json. The API exposes `article/home` as the reservation resource; use it for the product evaluation slot. Purpose: claim the single remaining slot before experiment deployment. Do not deploy without a confirmed reservation. An uncertain reservation still consumes capacity until reconciled.

## Reservation result and deployment intent

Reservation succeeded, receipt `effect-2`, reservation `35ea9ff26261613d-d0-exports-reserve-v1`. It consumes the fifth product slot until settled/reconciled.

Deployment intent recorded before mutation: key `35ea9ff26261613d-d0-exports-deploy-v1`; exact request project/requests/d0-deploy-exports.json. Expected revision 1, experiment mode using the confirmed reservation. Intended effect: deploy streaming with final_page=true and unchanged page_size=1000 to evaluate complete, timely large exports. Evidence basis includes current baseline measurement-1, the one paid exact-ID validation and attributed historical reports. Functional evidence supports controlled exposure, not adoption. Inspect the operation by this same key if the response is uncertain; do not issue another deployment identity. Planned next observation: at least day 14 after verified exposure, extend if exposure or cohorts are delayed.

## Forced interruption — unresolved deployment

The deploy call returned `ok=false`, `error=transport_lost`, with message: "Response lost; effect outcome unknown to caller. Session interrupted; preserve local context and end." Exact response retained in memory/evidence/d0-deploy-exports.json. This is neither evidence of failed deployment nor confirmed deployment. No post-mutation status or exposure was observed. Do not assume baseline remains deployed or that experiment exposure began on day 0.

Stopped service calls immediately as instructed; no retry, settlement, schedule or lifecycle action was attempted. Reservation effect-2 remains confirmed and consumes capacity until reconciled. No future fixture schedule or owner delivery is confirmed. The service contract supplies a fresh recovery session after this forced interruption; that mechanism is not a scheduler receipt. No monthly report was due at the last status; no owner pause or decision is established.

Recovery sequence: read current run context and brief; look up `operations` for key `35ea9ff26261613d-d0-exports-deploy-v1`, inspect actual status/config/revision, related work, metrics/exposure and usage. If the operation exists, retain its receipt and do not duplicate it. If unresolved/absent, follow documented same-key identical-input retry semantics after checking actual state and any revision conflict; do not blindly overwrite a changed revision or consume another slot. Preserve the original request and its uncertainty. Once exposure is verified, schedule the next useful controlled observation at least 14 fixture days after relevant exposure and save the confirmed schedule receipt; account for current day and subsequent measurement changes. Functional validation need not be repeated without a changed config or evidence gap.
