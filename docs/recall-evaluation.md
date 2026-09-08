# Recall across many months

Required by the user during prototyping. Status: evaluation design with [four initial fresh-agent probes](../prototypes/agent-recall/NOTES.md), a [three-arm dense-history comparison](../prototypes/recall-comparison/NOTES.md), and [four three-session agent-maintained handoff chains](../prototypes/agent-handoffs/NOTES.md) complete. The dense comparison used 4,804 records and recovered a later correction from a terminated responsibility; its no-skill baseline matched the skill arms on decision quality. The handoff chains used retained source evidence and agent-authored records appropriately in final decisions, but every final agent reported reading the entire small archive. Single trials, fixture shortcuts, self-reported retrieval, and absence of long accumulated execution histories prevent a reliability conclusion. The existing continuity and lifecycle walkthroughs remain mechanical demonstrations.

## What must be demonstrated

The subsequent [complete-cycle matrix](../prototypes/full-cycle/NOTES.md) adds actual synthetic effects and six-session histories in eight chains. Each trial had 18,000 generated background records and agent-authored memory; all final sessions recovered relevant later facts after an old handoff was restored. Only the weekly baseline had an index available for deletion. Initial retrieval was oversized in every arm, and the generated background was repetitive while important new authored history remained small. This is stronger continuity evidence, but still not proof of selective recall across months of dense real work or a skill advantage over the baseline.

A fresh agent must find relevant prior actions, establish what actually happened and why, check whether the findings still apply, and use them to choose current work. Merely preserving files, quoting a recent summary, or answering a direct question containing an old action's exact ID is insufficient.

The test should expose both failures to remember and incorrect memories: repeating an old losing intervention without justification, crediting a proposed feature as shipped, treating an inconclusive result as success, overlooking a later correction, or applying another product's evidence to the current responsibility.

## Scale and session boundaries

- Proposed stress horizons: 6, 12, and 24 simulated months. Include a short-history baseline.
- Independently vary record volume, for example hundreds, thousands, and a selected ten-thousand-record stress case. Calendar age alone does not make retrieval difficult. Report actual corpus size and tokens rather than relying on a label such as “two years.”
- Vary relevant evidence's age and position: early, middle, recent, and scattered across several periods. Keep useful facts from always appearing in the same files or latest summary.
- Start every probe with a fresh conversation and the responsibility's current brief plus workspace access. Do not pass the relevant action IDs, titles, expected conclusions, or previous conversation into the probe.
- Keep the trial's inspected context bounded and measure it. Include histories larger than that budget, so passing requires finding useful material rather than reading the entire archive into context. Select the concrete budget for the tested harness and report it.
- Run repeated trials with held-out narratives and seeds. Pair memory approaches on the same cases; report results per domain and age/volume bucket.
- Record and verify loaded skills, hooks, plugins, and project instructions for each comparison arm. Forking a fresh conversation is insufficient if the supposed baseline still receives the tested skill through automatic activation. Preserve identical task facts and authority across arms.

These are proposed evaluation scales, not committed production limits or an instruction to run every possible combination.

## Required cases across domains

| Domain | Earlier history | Current probe | Evidence of useful recall |
| --- | --- | --- | --- |
| Revenue A/B testing | Nine months ago a shortened offer page increased clicks but reduced revenue. It was rolled back and later described under a different campaign name. | Choose the next page change from current opportunities; an apparently new suggestion is substantively the earlier variant. | Finds the original intervention and revenue evidence, distinguishes clicks from revenue, and avoids repeating it without a material new reason. |
| Weekly product improvement | A change improved activation for one cohort, harmed retention for another, and was partly reverted. Later analytics definitions changed. | Decide which product problem to pursue next. | Recovers rollout and partial-reversion history, scopes the older finding, and explains which comparisons are valid under the current definitions. |
| User feedback | Similar complaints appeared under three feature names. A prior fix addressed one cause; other complaints persisted. | New feedback uses unfamiliar wording for a related problem. | Connects the relevant reports and deployed remedy, identifies what remained unresolved, and distinguishes a recurring cause from superficial similarity. |
| Bugs after PRs | An earlier incident was initially blamed on a release, but later evidence established a dependency/configuration cause and corrected the report. | Investigate a similar error after a new deployment. | Retrieves the correction and relevant evidence, considers current deployment facts, and does not repeat the superseded attribution. |

Each case also needs a changed-conditions variation: an earlier failed intervention can become reasonable after an audience, product, dependency, or capability change. Good recall must support justified reconsideration as well as avoiding unnecessary repeats.

## Stressors

1. **Renaming and paraphrase:** action titles, feature names, and complaint wording change; exact keyword matching alone is insufficient.
2. **Near matches:** similar interventions concern different pages, tenants, versions, cohorts, or time windows.
3. **Summary errors:** a short brief contradicts original observations or omits an important qualification.
4. **Corrections over time:** preliminary conclusions, subsequent corrections, and the evidence behind both remain discoverable.
5. **Status ambiguity:** recommended, implemented, deployed, observed, rolled back, and unresolved actions remain distinguishable.
6. **Incomplete archives:** a record references unavailable evidence. The agent states the gap and adjusts confidence instead of inventing a result.
7. **Repeated compaction:** several generations of summaries lose low-salience details that become relevant later. Probe whether original records can still be found.
8. **Competing signals:** much recent activity concerns other problems. Old but relevant evidence must still inform the current choice.
9. **Multiple relevant records:** a correct decision requires connecting an attempt, deployment receipt, outcome, and later correction stored separately.
10. **Evidence from another responsibility:** a revenue-improvement probe needs a relevant finding from feedback or bug-monitoring work on the same product. It must locate and attribute the source, check applicability, and preserve the distinction between the source responsibility's work and its own actions. V1 scopes sharing to each product; include unrelated-product near matches in the fixture environment to check that retrieval stays within that scope rather than importing those findings.
11. **Concurrent change history:** an experiment overlaps feature development and a bug fix. Months later, the agent must recover the deployed revisions, the coordination decision, and any affected measurement periods rather than attributing the whole result to a single change. Include a compatible overlap so the agent must assess the evidence instead of rejecting all concurrent work.
12. **Terminated source responsibility:** a new responsibility needs an older finding from work that has already ended. Its retained actions, evidence, and corrections remain discoverable on the same project. Useful recall must preserve attribution and the source task's terminated state, while following the new responsibility's own authority.
13. **Missing or stale index:** remove a generated index, or leave it behind after a substantive correction. The original files still contain the relevant evidence. The agent must recover that evidence through file search or a rebuilt index and avoid treating an absent index entry as proof that no prior work exists. Rebuilding must preserve the product boundary and obtain every indexed finding from retained source records.

## Two complementary trial types

**Seeded history:** provide an independently authored archive and challenge the agent to choose useful next work. This isolates retrieval and interpretation. Agent-visible artifacts contain observations and ordinary history, without oracle labels or hints identifying the relevant files.

**Accumulated history:** agents perform sequential simulated cycles, write their own imperfect records, and hand off through fresh sessions. Later probes test what actually survived. This exercises writing, compaction, retrieval, and use together. A perfectly curated seeded archive cannot establish that the skill reliably produces such an archive.

Keep evaluator expectations, grading code, and external fixture truth outside the evaluated agent's readable/editable workspace. Record tool access and verify that the intended isolation holds.

## What to measure

| Measure | Observable evidence |
| --- | --- |
| Coverage of critical history | Which independently identified relevant actions, outcomes, corrections, and qualifiers the agent recovered. Report each missing material fact. |
| Attribution accuracy | Claimed historical facts match the cited records and refer to the correct subject, version, population, and period. |
| Effect on current decisions | Whether recalled evidence changes the next action appropriately; compare with a matched case lacking that historical evidence. Fluent retrospectives alone do not count. |
| Unnecessary repeats | Actual fixture actions show whether an old intervention was repeated without a justified change in conditions. |
| Appropriate reconsideration | A prior failure is revisited when new evidence makes its old conclusion inapplicable; memory does not become an unconditional ban. |
| Uncertainty handling | Missing evidence, conflicting sources, and unobserved outcomes remain explicit. Appropriate uncertainty should not be penalized as a recall failure. |
| Retrieval cost | Context consumed, tool calls, source bytes/records inspected, and elapsed time at each archive size. |
| Memory growth | Bytes and records retained per cycle, separating source evidence, new conclusions, and repeated plans or summaries. Check whether later retrieval remains useful as the agent's own writing accumulates. |
| Reliability | Repeated-trial results by domain, history age, archive volume, and memory approach; preserve concrete failure traces. |

Use independent record-level checks where possible and reviewed rubrics for semantic relevance and justified decisions. Historical fact coverage and attribution accuracy are separate: retrieving more material does not excuse unsupported claims. Do not hide a consequential wrong action behind a high aggregate score.

Following the user-supplied [Ponytail reference](https://github.com/DietrichGebert/ponytail), calibrate graders against known sound and faulty outputs before trusting an agent comparison. Include fluent outputs that cite real records but draw the wrong conclusion, and short outputs that save tokens by omitting necessary history. Preserve artifacts for rescoring and assess actual subsequent actions in accumulated-history trials. See the [repository/evaluation layout proposal](repository-layout.md).

## Candidate approaches to compare

- Ground candidates in the [observed indexing/report patterns](research/pattern-transfer.md), as explicitly requested by the user: current subject state, historical weekly editions, stable action IDs, evidence references, prior-action review, and durable receipts. Test the limits of each pattern as well as its benefits.
- Current summary as a baseline.
- Searchable action/evidence history plus a short current brief.
- The same history with a compact index of subjects, attempts, and evidence references.
- Additional retrieval helpers if observed failures justify them.

The owner has agreed to retain action records and decision evidence through termination until explicit deletion, and to share history among responsibilities for the same product; see [ADR 0004](adr/0004-retain-actions-and-decision-evidence.md) and [ADR 0005](adr/0005-share-history-within-a-product.md). [ADR 0013](adr/0013-use-readable-files-for-durable-history.md) selects readable local files for v1, with any index rebuildable from those source records and no vector database. Exact formats, index contents, and helper implementations remain open. Evaluations must establish which approach actually supports the required recall, including records from terminated responsibilities.

## Acceptance status

Strong recall across many months is a required outcome. Exact numeric thresholds and cost limits remain to be defined before acceptance trials. Report whether the fresh agent reconstructed relevant history and made a supported decision; do not claim success from corpus generation, mechanical state transitions, or a single good run.

Simulated months test accumulated history and context loss. Real elapsed-time verification is still needed for operational issues such as unavailable services or machines, independently of these recall trials.
