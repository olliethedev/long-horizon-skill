# Patterns to transfer from existing Impulse tasks

Source inspection: September 8, 2026. The user explicitly requested using the Google indexing and Biomogging report tasks as prototype references. Sources were read; existing tasks, their ledgers, and publications were not changed. Prototype inputs are synthetic.

## Observed patterns and candidate trials

| Existing pattern | What the source establishes | Candidate trial |
| --- | --- | --- |
| Reserve an indexing attempt before an external click | The worker persists the attempt counter and `submitting` status before invoking the browser. An ambiguous click keeps the reservation. | Interrupt after the simulated effect, restart with an unresolved receipt, and check that the next agent reconciles rather than repeats the action or refunds the budget. |
| Separate current state and recovery evidence | The coordinator supplies window identity, used attempts, cooldown, ledger paths, and run identity to recovery work. | A fresh run reconstructs what remains permitted and which action is unresolved, even if its conversational summary is missing. |
| Ledger rows identify subjects but are mutable | `set_status` updates a URL's status, attempted timestamp, and result in the existing row; later index verification updates status/result again. The ledger alone therefore does not retain every historical transition. Other logs and recovery files exist. | Replay a year or more of activity through a current-row view and a historical archive; inspect which earlier attempts and explanations remain reachable. Do not claim this comparison models the entire indexing system. |
| Per-edition evidence and stable action IDs | Report instructions require stable action IDs, evidence, review windows, and immutable previous reports. The inspected generated action register also has separate `implementationStatus` and `outcomeStatus` fields. | Follow a recommendation across months and renames, including proposed-but-never-shipped work and later revisions. |
| Revisit the previous distinct week | Report instructions explicitly ask each run to review prior actions and compare forecasts with actual outcomes; another edition of the same week is not a new observation interval. | Insert a same-week rerun and check that it does not manufacture a new result. Compare previous-week-only retrieval with access to older indexed evidence. |
| Publication intent and receipt | A publication attempt precedes publishing; an existing successful receipt is verified, and uncertain outcomes require reconciliation. | Lose the local acknowledgment after a synthetic publication, then verify that the new run finds the existing effect without producing another copy. |
| Versioned measurement assumptions | New reports use the current owner-supplied click-to-estimated-revenue assumption, while historical editions retain the assumption used then. The source has no actual orders/commission feed. | Change a measurement assumption midway through the history. The agent must interpret old evidence under its original definition and avoid presenting a proxy estimate as verified purchase revenue. |

Primary sources: [indexing worker](../../../biomogging-indexing/process-queue.sh), [index verification](../../../biomogging-indexing/audit-requested-index-status.sh), [indexing coordinator](../../../biomogging-indexing/impulse-task.py), [recovery instructions](../../../biomogging-indexing/recovery.md), [report assignment](../../../biomogging-reports/AGENT_INSTRUCTIONS.md), [report template](../../../biomogging-reports/REPORT_TEMPLATE.md), [generated action register](../../../biomogging-reports/weeks/2026-09-06/impulse-20260907/actions.json).

## What must be established rather than assumed

The inspected report editions all concern the same completed week, September 6, 2026. Their existence is not evidence of months of successful follow-up or of stable IDs surviving months of agent-generated work. The instructions provide a useful candidate method; the evaluations must measure whether agents obey it.

Likewise, a current ledger row is useful for deciding what is pending now, but full recall may require finding the corresponding logs or snapshots. A prototype should measure how those references survive and remain discoverable, rather than declaring either task already solves general memory.

The proposed comparison is: current state for resumption, dated records and evidence for historical reconstruction, and an optional compact index to connect them. The owner has since agreed to retain action records and decision evidence for the responsibility's lifetime. Indexing and retrieval remain candidates to evaluate with fresh agents.

## Relation to current prototypes

- The [continuity prototype](../../prototypes/continuity/README.md) already illustrates uncertain operations, scoped outcomes, and separate scheduling acknowledgment. These match indexing/publication concerns, but its simulated transitions do not establish the installed tasks' crash guarantees.
- The [lifecycle prototype](../../prototypes/lifecycle/README.md) separates a completed improvement from a broader ongoing brief across four domains.
- The [history-view prototype](../../prototypes/history-views/README.md) compares what older facts are reachable through current rows, the previous reporting week, and a subject index into archived records. It is a data-retention/retrieval-view experiment, not an LLM recall evaluation.
- The [recall evaluation design](../recall-evaluation.md) requires actual fresh-agent trials on both curated and agent-authored history, including all the patterns above.
