# Historical-view comparison

Question: which historical action facts are reachable through a current row, the previous reporting week, or an index into dated records?

Exercised September 8, 2026 using Python 3.13.5. The comparison command and terminal view-switching both completed successfully. No model or live task ran.

```sh
python3 prototypes/history-views/prototype.py --compare
```

| History | Total records | Current-row action records | Previous-week action records | Indexed-archive action records | Records returned by index |
| --- | ---: | ---: | ---: | ---: | ---: |
| 26 weeks | 628 | 0 | 0 | 4 | 30 |
| 52 weeks | 1,252 | 0 | 0 | 4 | 56 |
| 104 weeks | 2,501 | 0 | 0 | 5 | 109 |

The four earlier action records contain deployment, a negative revenue observation, rollback, and a later qualification of the finding. At 104 weeks a fifth record contains a later recommendation with no deployment receipt. Current-row and previous-week views returned one recent routine observation for the subject, omitting those earlier action facts.

This is a deliberate comparison of restricted views. It does not imply that the full indexing task or report archive lost these kinds of facts. Source indexing logs and recovery evidence, and older report editions, can exist outside those views. The source [pattern-transfer note](../../docs/research/pattern-transfer.md) explains the correspondence and limits.

## What it establishes

For this synthetic history, dated records plus an explicit index preserve access to old actions and corrections that a current-state or previous-week-only view does not expose. The indexed query also returns increasing routine history: 109 records at two years. An index makes records addressable; it does not by itself solve relevance ranking or bounded-context recall.

## What remains untested

No agent created the index or selected the lookup subject; the generator supplied perfect subject labels. No semantic matching, interpretation of conflicting evidence, memory compaction, or downstream action choice was measured. These counts are data-view results, not agent recall scores.

Fresh-agent trials must include realistic task wording, imperfect agent-authored records, misleading summaries, changed names and conditions, and independent checks of whether historical evidence changes the next decision. The user-required [recall evaluation design](../../docs/recall-evaluation.md) specifies that work.

Status: available for the active design interview. The owner has since agreed to lifetime retention of action records and decision evidence; storage and retrieval architecture remain open. Delete this shell or absorb validated logic after the question is resolved.
