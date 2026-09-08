# Evidence: organization export streaming and scoped rollback

Source identity: `support-investigation/ticket-bundle-31`, dated 2025-03-10; supplied via this session's `current-packet.md`. The source packet is preserved verbatim below because the temporary packet will be replaced.

Evidence level: the packet reports receipt-backed deployment and rollback plus a reproduced completeness defect. The underlying receipts, reproduction data, row counts, page size, and current live deployment state were not supplied or independently inspected. Treat this as the reported state as of the packet date, not a fresh live verification.

## Preserved source packet

Date: 2025-03-10. Source: support-investigation/ticket-bundle-31.
The feature then called 'Bulk archive download' generated organization exports. Receipt release-ex22 confirms a streaming implementation was deployed on March 2. It reduced timeouts for 20,000-row exports, but a reproduced completeness check found missing final-page records. Receipt rollback-ex23 confirms streaming was disabled on March 10 for exports over 10,000 rows; smaller exports retained streaming. Larger exports returned to the buffered path. Separately, the 'Saved view CSV' complaint concerned stale column order, not omitted records; that issue remains open. Preserve the actual effects and plan the useful follow-up.

## Interpretation and limits

- “Bulk archive download” means organization exports. Preserve both names for later retrieval.
- `release-ex22`: streaming reportedly deployed on March 2, 2025. Fewer timeouts were observed for 20,000-row exports; no timeout rate or elapsed-time distribution was supplied. This does not establish a complete or successful export, nor quantify completion-time improvement.
- A reproduced completeness check found missing final-page records. The affected reproduction's exact size, cohort, software version, and root cause are unspecified. Do not assume all sizes are affected or that exports of 10,000 rows or fewer are safe.
- `rollback-ex23`: streaming reportedly disabled on March 10 for exports **over** 10,000 rows, which returned to the buffered path. Streaming remained for exports of 10,000 rows or fewer. This was a scoped rollback, not removal of streaming from every export.
- Buffered-path completeness and performance after rollback are not verified by the packet. Restoring that path is not evidence that all reliability problems are resolved.
- “Saved view CSV” has an open stale-column-order issue. This is a separate failure mode; the packet does not attribute omitted records to it.
- No later corrections, related-responsibility findings, or implementation details were available in the supplied files. Future evidence should be added with links to this record, preserving the original observations.

## Later evidence, 2025-11-18

[release-verification/ex-verify-81](2025-11-18-ex-verify-81.md) reports the rename to Workspace data export, release of final-page patch `page-final-81`, passing exact-ID fixtures at 4,000 and 10,000 rows, and continued buffering above 10,000 rows. This adds scoped verification without establishing larger streaming completeness. The separate Saved view CSV column-order issue is now reported fixed. These later observations update the corresponding status uncertainties above; the original March evidence remains intact. See [Action 002](../actions/002-verify-larger-patched-exports.md) for the resulting plan.
