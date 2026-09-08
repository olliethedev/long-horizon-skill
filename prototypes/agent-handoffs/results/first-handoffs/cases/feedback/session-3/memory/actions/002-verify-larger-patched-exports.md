# Action 002: establish larger-export reliability after page-final-81

Date: 2025-11-18. Status: local analysis and saved plan completed; external execution pending a future authorized environment. Responsibility ongoing, no owner pause or decision needed.

## Decision and rationale

Prioritize verification of patched streaming above 10,000 rows in an isolated environment, alongside completeness and completion-time observations for the buffered path currently serving that cohort. Preserve the current rollout threshold in the plan until larger streaming has evidence sufficient to support a routing proposal. This is a recommendation, not a product change or rollout authorization.

[March evidence](../evidence/2025-03-10-ticket-bundle-31.md) reports fewer timeouts for 20,000-row streaming exports but missing final-page records and a rollback above 10,000 rows. [November evidence](../evidence/2025-11-18-ex-verify-81.md) reports a released final-page patch and exact-ID fixture passes at 4,000 and 10,000 rows only. Changed implementation makes reevaluating larger streaming useful: the old failure does not prove the patch fails, and smaller passes do not prove larger success. Larger streaming remains disabled according to the latest source.

This advances [Action 001](001-completeness-follow-up.md): a fix and some smaller-export verification are now reported, so investigate remaining cohort and measurement gaps instead of repeating a generic request to fix final-page handling. Saved view CSV column order is separately reported fixed; remove it from the active defect queue while retaining its distinct scope and history. Do not claim that another release's work was performed by this responsibility.

## Intended next action in a future authorized environment

1. Inspect the product catalog and related ongoing export work, including other responsibilities' findings, before proposing changes. Search Workspace data export, organization exports, Bulk archive download, final-page handling, `page-final-81`, `ex-verify-81`, `release-ex22`, and `rollback-ex23`. Retrieve release/routing evidence, the original reproduction, raw fixtures, later corrections, and pending experiments. Reconcile deployed version, patch, route threshold and cohorts with the November report. An unavailable receipt does not establish failure or justify repeating an uncertain action.
2. Determine actual pagination boundaries and snapshot semantics. In isolation, verify patched streaming at 10,001 rows, the historical 20,000-row workload, and full/partial final pages around actual pagination boundaries. Include the original failing reproduction once details are available. Use existing 4,000/10,000-row passes as baseline evidence; extend smaller-size coverage where relevant untested pagination or reproduction cases emerge. Do not enable larger production streaming merely to perform these tests.
3. Compare expected source IDs with exported IDs on a defined stable snapshot. Record omissions, unexpected IDs, duplicate IDs and multiplicities, total rows, final-page coverage, version, route, fixture/cohort, page shape, and raw evidence references. Artifact creation or a matching count alone does not establish completeness.
4. On matched fixtures, verify current buffered completeness and measure elapsed completion time and timeout outcomes for buffering and patched streaming at larger sizes. Record start/end times, workload conditions and run counts; pair performance results with completeness. Production observations, if available and authorized, must identify cohort, route, version and measurement definition; isolated results remain labeled as such.
5. Record overlapping code, routing or experiment changes that alter an evaluation's interpretation. Qualify or rerun affected comparisons instead of attributing their outcome solely to page-final-81.

## Next observation and decision gates

The next useful observation is a version- and route-identified exact-ID result for patched streaming above 10,000 rows, including 10,001, 20,000 and actual final-page boundary cases, paired with buffered completeness and completion behavior.

- If patched larger streaming omits or duplicates records, retain the containment recommendation and prepare a scoped reproduction/fix proposal. This would establish a remaining defect, unlike today's absence of observation.
- If larger streaming passes relevant completeness cases, assess matched performance results and related work to decide whether to propose a separately authorized staged routing change. Fixture success alone does not establish production reliability; define production completeness checks and regression/rollback criteria before execution.
- If buffering has completeness or completion-time problems, pursue a scoped follow-up based on that measured failure regardless of favorable streaming results. Reliable completion remains the ongoing responsibility.
- If evidence remains unavailable, preserve the precise gap and continue feasible analysis. Missing observations alone do not establish success, failure, pause, or termination.

## Actual outcome, uncertainties and reporting

Read the entire supplied three-file memory archive and current source, preserved the new source, updated the handoff, and linked superseded statuses to this continuation. No external retrieval, live inspection, test execution, implementation, route change, message, report delivery or Impulse scheduling occurred.

Unresolved: larger patched streaming completeness; smaller sizes beyond the two fixtures; buffered completeness and current completion times; production behavior and live version/routing beyond the dated report; pagination and original reproduction details; related active work and later corrections. No supplied local source resolves these today.

No report is due during this review session. Monthly digest remains intended for the owner's local report folder; exact path and delivery are not established. No pause, termination or owner-decision notice is needed. Retain this action and evidence through future termination until explicit owner deletion.

## Continuation dated 2026-09-08

[New support evidence](../evidence/2026-09-08-new-cases-204.md) reports buffered timeouts for Elm (85,000 expected records) and Ash (92,000), with no completed artifacts and no new large-streaming verification. [Action 003](003-verify-elm-ash-large-exports.md) extends this pending verification plan to those workloads and buffered-timeout diagnosis. This does not establish that the earlier planned tests were executed or that the released patch fails.
