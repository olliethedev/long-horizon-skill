# THROWAWAY — lifecycle across four domains

Question: can the same small lifecycle express page revenue experiments, weekly product improvement, feedback work, and monitoring bugs after PRs, including reached objectives and impossible objectives? The user has now selected continuation across objectives for ongoing responsibilities; bounded briefs can terminate when complete or impossible.

From the project root:

```sh
python3 prototypes/lifecycle/prototype.py
```

Advance events, switch cases, and inspect the retained evidence and objectives. Everything lives in memory. The pure reducer is in `model.py`, fixture narratives are in `scenarios.py`, and this terminal shell owns all I/O. No extra dependencies are required.

Inspect final states across all four cases:

```sh
python3 prototypes/lifecycle/prototype.py --compare
```

Print every state in one case:

```sh
python3 prototypes/lifecycle/prototype.py --case revenue --walkthrough
```

Cases: `revenue`, `weekly-product`, `feedback`, `post-pr-bugs`.

## Selected lifecycle

- Completing an individual improvement leaves an ongoing responsibility active.
- An impossible sub-objective permits another useful objective within the broader responsibility.
- Completing a bounded responsibility, or establishing that its entire brief is impossible, terminates the task.

The weekly product case now includes an impossible investigation route followed by an alternative objective. The feedback case represents an impossible full brief. The earlier terminate-after-any-objective comparison is preserved in the findings, and its rejected branch has been removed from the executable prototype.

## Limits

The narratives provide both observations and scripted interpretations. This exercises the shape of records and transitions; it does not test an agent's reasoning, prove statistical significance, or evaluate a real product. Revenue figures are fictional, and the later revenue-analysis verdict is supplied rather than calculated. The monitoring window and sample sizes belong to the fixture, not universal sufficiency rules.

No Impulse task is registered, changed, stopped, or scheduled. The next-action text expresses intent only; the earlier continuity prototype explores the separate scheduling acknowledgment. JSON round-tripping in the TUI is not a fresh-agent evaluation or a crash-durability test. The prototype's fixed narrative length keeps state small enough to inspect.

Agent-driven trials across all four domains remain required. They need raw fixture evidence, fresh sessions between observations, independent grading, and no supplied answer labels. See the [evaluation plan](../../docs/evaluation-plan.md).

Capture findings in [NOTES.md](NOTES.md). Delete this shell or absorb validated logic when the active interview has resolved its question.
