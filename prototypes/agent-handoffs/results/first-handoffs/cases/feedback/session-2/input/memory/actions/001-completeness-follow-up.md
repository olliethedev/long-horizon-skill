# Action 001: establish completeness before changing export streaming

Status: local analysis and saved plan completed; external investigation and implementation **not executed**. Responsibility remains ongoing, with no owner pause or decision needed.

## Decision and rationale

Prioritize a completeness investigation of organization exports (“Bulk archive download”), covering the streaming path still reported active at 10,000 rows or fewer and the buffered path restored above that threshold. Do not recommend reenabling streaming for larger exports on the strength of fewer timeouts alone. The final-page loss requires reproduction and an explanation before a proposed fix can be assessed.

Evidence: [preserved ticket bundle and scope qualifications](../evidence/2025-03-10-ticket-bundle-31.md). The smaller streaming cohort deserves explicit inspection because the rollback left it enabled, although the supplied evidence does not establish that smaller exports lose records. The larger buffered cohort also needs verification; rollback alone establishes no measured outcome.

## Intended next action in an authorized future execution environment

1. Retrieve `support-investigation/ticket-bundle-31`, `release-ex22`, `rollback-ex23`, and the original completeness reproduction. Search the relevant product catalog or history using organization exports, Bulk archive download, streaming, final-page records, and the receipt IDs; follow later corrections and linked evidence. Inspect related ongoing export work and the actual deployed code/version, routing threshold, and cohort behavior before proposing product changes.
2. Compare expected source record IDs and counts against exported IDs and counts on a stable fixture or defined snapshot. Check omissions and duplicates, with explicit inspection of final-page records. Exercise 10,000 and 10,001 rows, the reported 20,000-row workload, and full/partial final pages around the implementation's actual pagination boundaries. Page size and exact original failure size must first be retrieved. Verify which path serves each case. Reproduce disabled streaming only in an appropriate isolated test environment, if authorized; this plan does not authorize live reenabling.
3. Record version, organization/cohort, source snapshot, selected path, expected and actual IDs/counts, page shape, start/end timestamps, elapsed completion time, timeout behavior, and the relevant raw evidence. Separate successful artifact creation from verified completeness.
4. If retained streaming loses records, prioritize a scoped containment/fix proposal using the observed affected cohort and a verified alternative path. If the defect is confined to the disabled cohort, develop and validate a final-page fix there. If current tests pass, explain the discrepancy with the original reproduction and versions before concluding the defect is resolved. Evaluate completion-time improvements only alongside a passing completeness check.

## Separate unfinished issue

Retrieve the “Saved view CSV” stale-column-order reproduction and expected saved-view column sequence for a separate follow-up. It remains open; do not count it as evidence of missing organization-export records or describe it as fixed by the streaming rollback. Check whether another responsibility owns related work before proposing changes.

## Next observation and decision gate

The next useful observation is receipt/reproduction evidence plus a current route-and-version check, followed by a recorded completeness result across the threshold and actual pagination boundaries. This should determine whether retained streaming needs a containment proposal and where a final-page fix belongs. A larger-export streaming restoration proposal requires both complete records and measured completion behavior after a validated fix; no restoration is approved by this record.

## Actual outcome and reporting

Only local evidence preservation, analysis, and this plan were performed. No product change, test execution, receipt retrieval, live inspection, external message, or Impulse schedule occurred. No report is due in these review sessions. Follow the monthly digest cadence to the owner's local report folder when due; no destination path or delivery is established here. Preserve this action and its evidence even if the responsibility later terminates, until explicit owner deletion.
