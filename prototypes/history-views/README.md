# THROWAWAY — historical views inspired by existing tasks

Question: after months of activity, which prior action facts are reachable through a current subject row, a previous-week report, or a subject index into dated records? This isolates information availability before testing whether an agent retrieves and uses it well.

From the project root:

```sh
python3 prototypes/history-views/prototype.py
```

Switch views and horizons in the terminal. The selected subject, archive size, retrieved record count, action history, corrections, and evidence references are shown. Routine observations are counted to keep the frame compact. Everything lives in memory, with no dependencies beyond Python.

For a comparison at 26, 52, and 104 weeks:

```sh
python3 prototypes/history-views/prototype.py --compare
```

## Patterns being tested

The indexing worker's ledger updates the current state of each URL. This prototype's `current` view similarly holds one latest record per subject. The actual indexing task also has logs and recovery artifacts; this view does not represent its entire memory system.

The Biomogging report asks the agent to review the previous distinct week's actions and forecasts. The `previous-week` view represents stopping after that one report. Actual historical editions remain available, and an agent could read further back.

The `indexed-archive` candidate retains dated records and maps a stable subject identity to them. This is a proposed addition to test, not a claim that it is already implemented by either source task. The pure functions in `model.py` are separate from the terminal shell.

## Synthetic history

There are 24 routine observations per week. A mobile checkout trial is deployed in week 3, produces a negative revenue observation in week 4, is rolled back in week 5, and receives a qualifying correction in week 17. A similarly themed intervention is only proposed in week 70; it has no deployment receipt.

These fictional records illustrate distinct action states, corrections, and temporal scope. They do not use private data or make statistical claims. The source patterns and local citations are recorded in [pattern transfer](../../docs/research/pattern-transfer.md).

## Limits and disposition

The lookup subject is supplied, so this is not a semantic search benchmark. The index is perfect because the fixture generator assigns it; actual agent-created metadata may be missing or wrong. No agent wrote, searched, summarized, or interpreted these records. A larger archive in memory is not proof of many-month agent recall, and this experiment does not choose a production retention policy or database.

The next required evidence is fresh-agent trials described in the [recall evaluation design](../../docs/recall-evaluation.md). Keep this prototype only while the interview is exploring the question; capture findings in [NOTES.md](NOTES.md), then delete it or absorb validated logic.
