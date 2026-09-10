# Dense recall comparison findings

Run and reviewed September 8, 2026. All three arms made a supported decision, including the arm without the candidate skill. This case therefore provides no demonstrated improvement in decision quality from the skill. The narrow retrieval revision produced bounded history searches without reported content-output truncation, while the other two arms recovered after truncated content searches. All three began with an overly broad filename listing before reading the product scope and any skill.

## Case and method

The current Cedar Shop responsibility considers removing explanatory offer text. A stale summary calls a prior attempt a revenue failure and forbids retrying it. The retained history contains a real deployment, an initial apparent loss, and a real rollback. A later correction from a different, terminated responsibility establishes that wallet orders were omitted from the original revenue feed. Corrected totals do not establish a winner.

Each arm received the same current brief, authority, product boundary, registry, history, and evidence. The archive contains 4,804 action records, 1,438,969 bytes of JSONL, and 1,204 supporting evidence files. Records range from March 1, 2025 to July 9, 2026; the current brief is dated September 8, 2026. This is dated synthetic history, not elapsed execution time or agent-authored memory.

One fresh fork-free subagent ran per arm, with inherited model defaults and no overrides. Arms were: no candidate skill; the frozen first-pass skill; and that same skill with one added paragraph about bounded retrieval. The factual task and authorization were identical. Exact loaded global harness instructions and model identity were not independently audited; “no-skill” means this candidate skill was absent from the trial workspace.

[Review criteria](review-criteria.json) were written before output review. The parent reviewed the decisions against source evidence and those criteria, with arm identity visible. Executable checks verified original input hashes, cited action IDs, and evidence paths. The [manifest](https://github.com/olliethedev/long-horizon-skill/blob/be91b6929b4910042e71ddf704c0801b4d611d39/prototypes/recall-comparison/results/first-comparison/manifest.json) preserves provenance and output hashes. Identical case files are archived once under [inputs](https://github.com/olliethedev/long-horizon-skill/blob/be91b6929b4910042e71ddf704c0801b4d611d39/prototypes/recall-comparison/results/first-comparison/inputs/task.md); each arm's skill and outputs are under its own directory. Interpret decision evidence paths relative to the common input root, except `SKILL.md`, which belongs to that arm.

## Observed decisions and retrieval

| Arm | Decision | Reported retrieval behavior |
| --- | --- | --- |
| [No skill](https://github.com/olliethedev/long-horizon-skill/blob/be91b6929b4910042e71ddf704c0801b4d611d39/prototypes/recall-comparison/results/first-comparison/arms/no-skill/outputs/decision.md) | Proposed a controlled retest. Correctly treated the apparent loss as superseded and corrected +2% as inconclusive. | Initial filename listing and a 220-row filtered projection were truncated. Later semantic and action-link searches recovered the four critical records. |
| [Frozen skill](https://github.com/olliethedev/long-horizon-skill/blob/be91b6929b4910042e71ddf704c0801b4d611d39/prototypes/recall-comparison/results/first-comparison/arms/frozen-skill/outputs/decision.md) | Same supported choice and historical interpretation. | Initial filename listing and a broad content query were truncated. A structured filter excluding the common archive responsibility then isolated the four critical records. |
| [Bounded retrieval revision](https://github.com/olliethedev/long-horizon-skill/blob/be91b6929b4910042e71ddf704c0801b4d611d39/prototypes/recall-comparison/results/first-comparison/arms/bounded-retrieval/outputs/decision.md) | Same supported choice and historical interpretation. | Initial filename listing was truncated. History queries used explicit match limits and refinement; no later content-output truncation was reported. An intentional result limit was recognized as a reason to refine the query. |

All three recovered the same four historical actions and supporting evidence:

- `1cc8f2628484`: compact presentation was actually deployed.
- `6e2407d39843`: the original feed reported USD 50,000 control versus USD 30,000 treatment across 10,000 sessions per arm.
- `12667552afc5`: detailed presentation was actually restored following that observation.
- `23d81f52f86d`: later reconciliation corrected treatment revenue to USD 51,000, versus the unchanged USD 50,000 control, with equal session counts and insufficient evidence of a winner.

Their proposals preserve the active responsibility, leave terminated source responsibilities terminated, correct the stale summary through output evidence, and distinguish a historical rollback from its superseded rationale. All identify current measurement checks and experiment criteria needed before a future authorized launch. These are local proposals; no experiment, resumption, schedule, or product change was executed.

Each retrieval log discloses that initial trial-wide filename discovery exposed another product's path before the responsibility scope was read. None reports reading that product's contents or uses its results as evidence. This is a startup discovery weakness; it is not evidence of fully scoped retrieval or an enforced product boundary. The revised paragraph was read only after that initial discovery, so this trial does not test activation of the skill before the first tool call.

## Limits exposed by the comparison

- All 4,800 surrounding records share one `growth-archive` responsibility and a regular four-stage pattern. The frozen-skill agent exploited that distinction. There is only one `corrected` phase record. More archive bytes and substantive-looking records still leave simple fixture shortcuts.
- Both the basic task and the summary name the earlier intervention clearly enough to guide search. Product identity is explicit and the other-product near match is simple. There are no missing supporting documents or conflicting corrections.
- Some decisive rows lack the cohort field present in surrounding records. The baseline's initial exact cohort filter missed them; semantic retrieval and evidence inspection recovered them. This is a useful warning against assuming that every record has complete index metadata.
- All arms scanned the whole scoped index programmatically at some point. This is different from placing the entire archive into model context. No complete, independently captured tool trace or token/cost measurement is available; retrieval claims rely on agent-reported commands and warnings.
- One trial per arm cannot establish reliability or isolate a wording effect from sampling variation. The bounded revision's narrower outputs are encouraging process evidence, not a measured cost reduction or a production acceptance result.
- Input preservation and valid references were checked, but read boundaries were instructions, not an OS sandbox. Manual review was not blinded. No installed-skill startup, multiwake execution, or history written by agents was tested.

## Consequences for the next prototype

Keep the no-skill baseline: this run shows why supported skill outputs alone cannot establish added value. The bounded-retrieval paragraph is a candidate for further evaluation; no shared skill has been changed or installed.

Next use histories with several substantive responsibilities and competing corrections, and let agents write the history across fresh sessions. Verify the actual skill-loading path and scope-aware startup before interpreting initial discovery behavior. Preserve independently captured tool outputs and use matched, repeated trials when drawing efficiency conclusions.

This comparison does not justify a database, embeddings, or a mandatory retrieval helper. It narrows the remaining questions to archive construction, initialization, and reliable continuation through actual agent-written records.
