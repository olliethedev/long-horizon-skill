# Continuity prototype findings

Question: what distinctions must survive between sessions so the next run can recover work and revise conclusions without losing their evidence?

Status: initial mechanical walkthrough complete on September 8, 2026; user verdict and architecture decision pending. The prototype remains available for the active design interview. Delete it or absorb validated logic once that question is settled.

## What was exercised

Used Python 3.13.5. The first process recorded an attempt and an uncertain external outcome in the scratch directory, then exited. A second Python process loaded those records with no prior process memory and drove the remaining scenarios.

```sh
python3 prototypes/continuity/prototype.py --workspace prototypes/continuity/PROTOTYPE-WIPE-ME --steps try uncertain
python3 prototypes/continuity/prototype.py --workspace prototypes/continuity/PROTOTYPE-WIPE-ME --steps show try confirm week ack inconclusive ack week lose note try fresh drift try uncertain drift invalidate confirm invalidate
```

Run from an empty scratch directory to reproduce the initial sequence. All actions operated only on synthetic local records.

| Observed transition | Implication for the proposed records |
| --- | --- |
| Second process loaded attempt `a1` as uncertain and rejected a second attempt | The action identity and unresolved outcome must survive independently of session notes. |
| Deployment confirmation proposed day 7, while acknowledgment remained false | A planned observation time and confirmed future scheduling represent different facts. |
| Day 7 evidence was inconclusive; attempt stayed open until a day 14 loss | No observation, inconclusive evidence, and negative evidence must remain distinguishable. |
| A misleading universal-winner note did not alter the recorded loss or permit an identical repeat | A generated brief should not replace the underlying observations and decisions. This behavior was hard-coded, not learned. |
| A context change retained the old loss but allowed a new investigation | Learnings need applicability conditions; retaining history should not mean banning an idea forever. |
| Another context change did not resolve an uncertain deployment; confirmation came before invalidation | Changed evidence and execution uncertainty require separate handling. |

## Design inference

The candidate state model can express these distinctions with a small number of ordinary records. That supports investigating a skill with a durable workspace and optional helpers before choosing a larger runtime. It does not establish that this is the minimum schema, that arbitrary agents will follow it, or that it remains usable after thousands of attempts.

The hardest learning question is still open: will a fresh agent retrieve the relevant prior evidence and actually change its next decision? A deterministic reducer cannot answer that. The [candidate evaluation plan](../../docs/evaluation-plan.md) proposes fresh-agent, held-out scenarios to investigate it.

No real deployment, Impulse scheduling command, model invocation, statistical analysis, crash injection, or concurrent execution was tested. A successful state transition is not a successful business experiment. Actual runtime durability and semantic agent reliability require separate evidence.
