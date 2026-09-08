# First independent recall probes

Run and reviewed September 8, 2026. Four fresh agents made supported local decisions using older evidence in four synthetic archives. This establishes that the candidate workflow can work on these particular inputs. It does not establish reliable recall over months or demonstrate that the skill improves performance over an unassisted agent.

## Method and preserved evidence

Each agent received one case directory, its current decision task, and the same [disposable skill](long-horizon-prototype/SKILL.md). Agents started without the parent conversation (`fork_turns: none`); model settings were inherited without overrides. The fixtures contained dated history spanning September 2025 to September 2026. No real year elapsed.

Each archive contained 832 routine observations plus three or four substantive action records. Agents had access to a subject index, current signals, a misleading summary, and evidence linked from action records. The [review criteria](review-criteria.json) were written before output review and kept outside the agents' permitted case directories. The generator was also outside their permitted scope. Access boundaries were instructions, not an OS-enforced sandbox.

All original case inputs and agent outputs are preserved under [results/first-pass](results/first-pass/manifest.json). The manifest records input/output hashes, actual record counts and archive bytes. Each case includes `outputs/decision.json`, `outputs/decision.md`, and an agent-reported `outputs/retrieval.json`. The parent manually compared decisions with source evidence and the prewritten criteria, then checked that all cited action IDs and paths resolve within the corresponding case. Those checks establish reference validity; semantic conclusions below come from the manual review.

| Case | Archive size | Observed decision | Review |
| --- | --- | --- | --- |
| [Revenue](results/first-pass/revenue/outputs/decision.md) | 835 records; 192,924 bytes | Recovered deployment, randomized observation, and rollback. Distinguished higher clicks from lower revenue: USD 5 versus USD 3 per recorded session. Rejected an unqualified repeat of the text-removal intervention and proposed a different layout hypothesis while retaining explanatory content. | Meets this case's decision criteria. It did not claim statistical significance from insufficient distribution data or execute an experiment. |
| [Weekly product improvement](results/first-pass/weekly-product/outputs/decision.md) | 835 records; 192,974 bytes | Recovered that saving unfinished setup was recommended, deferred before implementation, and absent from the verified release. Selected it for further work instead of treating it as a measured failure. | Meets this case's decision criteria. Historical verification and current flags were considered together; no improvement was claimed before implementation or measurement. |
| [User feedback](results/first-pass/feedback/outputs/decision.md) | 836 records; 193,163 bytes | Connected the old and renamed export feature, recovered a partial rollback, and found that later tests covered only exports up to 10,000 rows. Proposed investigating current large exports and verifying both completion and record completeness. | Meets this case's decision criteria. It did not blindly restore the old background-job implementation, which had omitted records. |
| [Bugs after a PR](results/first-pass/post-pr-bugs/outputs/decision.md) | 835 records; 193,005 bytes | Recovered the preliminary release attribution, unsuccessful rollback, and later upstream-quota correction. Prioritized checking current quota pressure and whether the new PR contributed, while keeping the observation assignment active. | Meets this case's decision criteria. It caught that the current request-volume interval was unspecified and did not present the old cause as proof of the current cause. |

All four corrected the misleading summary in their output with supporting references, preserved source history, and kept the responsibility active. Their output artifacts propose subsequent work; this trial did not execute fixes, experiments, rollbacks, schedules, or owner notifications. Statements about permitted access and absence of external actions rely on the instructed task and agent reports; full tool traces were not archived.

## A concrete retrieval weakness

All four retrieval logs report an initial whole-file read of `memory/actions.jsonl` that produced truncated tool output. They then recovered the relevant records through targeted searches and read their evidence files. The final decisions were supported, but the initial retrieval behavior was wasteful and would become more problematic as archives grow.

All four also used a search excluding the `routine_review` phase. Because almost everything irrelevant in this fixture has that phase, this provides an unusually easy way to isolate the substantive history. Subject tags are consistently assigned, and the evidence directory contains only the relevant supporting documents. A year of dates and roughly 193 KB of JSONL should therefore not be confused with a difficult many-month recall workload.

The frozen candidate already says to use indexes and search. A justified next candidate is a narrow clarification: use the current brief and index to select bounded portions of a growing archive; widen the search when needed; follow evidence and correction links. Measure whether that changes retrieval behavior before adding a storage or retrieval helper. This is a proposed experiment, not an accepted production mechanism.

## What remains unresolved

- No comparison with the same task without the skill, or with summaries alone. The outcome cannot be attributed to the skill, index, or any individual instruction.
- One fresh decision session per domain, with no repetitions or held-out variations. Do not infer a success rate from four decisions.
- Histories were authored by the fixture generator, not accumulated by agents. Writing, summarizing, subsequent correction discovery, and repeated waking remain untested as a combined workflow.
- No hard context budget or independently measured retrieval cost. Corpus bytes are known; model tokens, complete tool traces, and reliable elapsed-time measurements are unavailable.
- No missing evidence, dense competing interventions, inconsistent indexing, changed-conditions reconsideration, or unrelated-product near matches. The weekly case tested unshipped work, not the cohort/metric-definition changes in the broader evaluation plan.
- The bug case consumed another responsibility's records already present in its archive. It did not discover a separate workspace or coordinate live concurrent actions.
- No external effects, Impulse scheduling integration, uncertain-action reconciliation, pause/resume execution, crash recovery, or actual multi-day operation. Lifecycle prose in a decision is not an execution test.

## Next bounded experiments

First compare the frozen skill, a narrowly revised retrieval instruction, and a no-skill baseline on a held-out archive containing many substantive interventions, plausible near matches, and imperfect indexing. Capture actual retrieval outputs under a bounded context budget. Include changed conditions so correct recall can justify retrying an old idea.

Then run a short sequence of fresh agent sessions against synthetic services. Let agents write the records themselves, advance fixture time, introduce a later correction and an overlapping product change, and inspect what the next fresh agent actually does. This distinguishes keeping records from producing records that another agent can use.

The result supports continuing a skill-first exploration. It does not yet justify choosing a database, embedding service, mandatory retrieval helper, or production schema. The [full recall plan](../../docs/recall-evaluation.md) remains the acceptance target.
