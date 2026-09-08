# Current decision

Keep the Cedar Ledger reliable-exports responsibility ongoing and prioritize a completeness investigation of organization exports (“Bulk archive download”). The useful next action is to retrieve the original final-page reproduction and release/rollback evidence, verify current routing and related work, and plan checks across both the retained streaming and restored buffered paths.

## Evidence

The supplied 2025-03-10 `support-investigation/ticket-bundle-31` reports deployment of streaming on March 2 (`release-ex22`), fewer timeouts for 20,000-row exports, and a reproduced loss of final-page records. On March 10, `rollback-ex23` disabled streaming only for exports over 10,000 rows; smaller exports retained it. Fewer timeouts do not establish successful or complete exports. The “Saved view CSV” complaint is a separate open stale-column-order issue.

The packet and its qualifications are durably preserved in [memory/evidence/2025-03-10-ticket-bundle-31.md](../memory/evidence/2025-03-10-ticket-bundle-31.md). The full rationale and investigation plan are in [Action 001](../memory/actions/001-completeness-follow-up.md).

## Material uncertainties

The original receipts and completeness reproduction were not available for direct inspection. The exact failure size, version, page shape, cohort, cause, and measured timeout/elapsed-time rates are unknown. The packet establishes reported historical routing, not current live state. Smaller-export streaming may or may not share the defect, and the restored buffered path lacks a supplied post-rollback verification. Related ongoing work and later corrections must be checked before product changes.

## Next action and intended observation

In a future authorized execution environment, retrieve the receipts and original reproduction; inspect current deployed routing/version and related export work. Verify exported IDs/counts and final-page records against a stable expected source, including 10,000/10,001/20,000 rows and full/partial final pages around the actual page size. Record completeness, duplicates, selected path, cohort/version, completion time, and timeouts separately.

A failure in retained streaming would support a scoped containment/fix proposal. A defect confined to disabled streaming would focus a tested final-page fix there. Passing current tests requires reconciliation with the original reproduction before closure. Propose restoration for larger streaming exports only with complete-record and completion-time evidence. Preserve the saved-view column-order issue as a separate open follow-up.

## Status and actual actions

Responsibility status: **ongoing, no owner pause**. Local evidence preservation and planning are complete; external investigation remains planned. No product was modified, test executed, external record retrieved, live task scheduled, or message sent. No owner decision or immediate notice is needed. No monthly report is due during this review session. The current handoff is [memory/handoff.md](../memory/handoff.md); all substantive conclusions and source observations survive independently of this outbox and the replaceable packet.
