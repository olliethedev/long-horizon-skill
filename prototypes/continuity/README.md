# THROWAWAY — continuity state model

Question: can a fresh session reconstruct a useful next action from explicit attempt, observation, and learning records when a prior action is uncertain, a result is inconclusive, or conditions change? This explores the minimum distinctions the records need. It does not evaluate whether an LLM reliably creates or reads them.

Python follows the runtime of existing indexing/report helpers. It is an exploration choice, not a production language decision.

From the project root:

```sh
python3 prototypes/continuity/prototype.py
```

The terminal shows the full state after each action. Enter a shortcut and press Enter. State normally lives in memory. The pure state transitions are in `model.py`; the terminal and optional scratch-file I/O are in `prototype.py`.

For actual continuity across separate Python processes:

```sh
python3 prototypes/continuity/prototype.py --workspace prototypes/continuity/PROTOTYPE-WIPE-ME
```

Quit and run the same command again. The scratch folder contains only synthetic prototype state and is ignored by Git. Remove it to reset. The model is deliberately small; enough repeated attempts will exceed one terminal screen.

## Scenarios to drive

1. `try`, `uncertain`; exit and restart. The saved record must still require reconciliation, not a blind repeat. `confirm` injects a fixture that says the deployment was observed.
2. `confirm`, `week`. A planned date is separate from the simulated scheduler acknowledgment (`ack`). Seven days passing cannot create a result.
3. `ack`, `inconclusive`. The attempt stays open, another observation is proposed, and the new wake needs its own acknowledgment. After another `week`, inject `lose`.
4. `note`, `try`. A misleading session note cannot replace the recorded loss. `fresh` reloads durable records and discards the note.
5. `drift`, `try`. The same variant is now eligible for investigation in changed conditions. The historical loss remains visible with its old scope.
6. `confirm`, `drift`, `invalidate`. Close a confounded comparison without calling it a win or loss. An uncertain external action must be reconciled before it can be invalidated.

For a noninteractive transcript, supply names after `--steps`, for example `--steps try uncertain show`.

## Limits

All external effects, evidence verdicts, context changes, and scheduler acknowledgments are injected fixtures. There is no analytics/statistics engine, LLM, real scheduling, authorization model, concurrency control, rollout, or goal-completion policy. The seven-day window is a scenario device, not an A/B-testing recommendation. Scratch-file replacement is not a tested crash-durability protocol.

The fixed `short-copy` candidate makes repeats easy to see; this is not a general candidate-selection algorithm. A material context change is an explicit input, not automatic proof that every previous finding has expired.

Capture the verdict in [NOTES.md](NOTES.md). Keep this prototype only while the interview is actively using it; delete it or absorb validated logic after the question is settled.
