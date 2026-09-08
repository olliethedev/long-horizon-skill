# Lifecycle walkthrough findings

Question: do the same records express four domains with reached or impossible objectives, and what does each completion policy do to an ongoing brief?

Status: scripted walkthroughs exercised September 8, 2026. The user subsequently selected continuation across objectives for ongoing responsibilities. User-driven inspection is still available. These are not LLM evaluations. The table below records the original comparison before that decision.

Executed with Python 3.13.5:

```sh
python3 prototypes/lifecycle/prototype.py --compare
python3 prototypes/lifecycle/prototype.py --case feedback --walkthrough
```

The comparison drove four synthetic cases under two candidate policies, for eight deterministic walkthroughs. Both commands completed successfully. Observations below describe the implemented models, not measured agent judgment.

| Case | End after an individual objective | Continue within the broader brief |
| --- | --- | --- |
| Page revenue | Terminates day 28 after supported variant C rollout; later observations are not consumed. | Retains losing B and successful C evidence; waits for post-rollout evidence on day 35. |
| Weekly product improvement | Terminates day 14 after the onboarding fix; never considers the day 21 search evidence. | Retains the verified onboarding outcome, selects the search objective, and awaits a representative sample. |
| Feedback | Terminates day 8 because the requested historical data cannot be obtained within the entire brief's permitted sources. | Same result, since the impossible objective is the full bounded brief. |
| Bugs after PRs | Terminates day 8 after the deployed observation window and verified regression fix. | Same result, since the bounded responsibility is complete. |

The feedback walkthrough remained waiting during the temporary provider outage on day 3. It terminated only after later fixture evidence established the unavailable historical data and ruled out permitted alternative sources. That distinction is supplied by the fixture; testing whether a fresh agent discovers and respects it remains outstanding.

## What this suggests

The general records need responsibility, current and prior objectives, evidence, reasons, next work, and a distinct terminal reason. Domain-specific interpretation can be supplied without introducing variants into feedback work or forcing a numerical KPI onto every responsibility.

Automatically terminating after every selected objective is too coarse for the example weekly brief if the owner expects ongoing improvement. The user is deciding how much discretion the agent should have at that boundary. This comparison does not evaluate a nuanced agent deciding to stop; it only exposes the consequences of two explicit policies.

## Limits and next evidence

- Revenue verdicts, priority choices, and conclusions about impossibility are scripted. No statistical analysis, live analytics, model reasoning, or causal inference was evaluated.
- No Impulse task was created or altered. This model expresses future-work intent, not scheduler acknowledgment.
- A failed sub-objective within an otherwise feasible broad responsibility needs an additional case after the termination policy is resolved.
- Required next-stage evidence is fresh-agent trials across all four domains, with raw fixture observations and independent grading rather than supplied decision labels. See [the evaluation plan](../../docs/evaluation-plan.md).

The rejected terminate-after-any-objective branch has now been removed. A subsequent walkthrough of all four cases confirmed that revenue and weekly-product responsibilities remain waiting/active, while the bounded feedback and monitoring cases terminate for impossible/reached respectively. The weekly case also retained an impossible investigation route and selected a useful alternative. These are still scripted transitions; the shell remains available for the active cross-domain exploration.
