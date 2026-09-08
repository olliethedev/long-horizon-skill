# THROWAWAY — independent agent recall probes

Question: can a fresh agent using the candidate skill find and use relevant older actions in a year of synthetic history across the four required domains?

Prepare isolated case directories:

```sh
python3 prototypes/agent-recall/prepare.py
```

The command prints temporary workspace paths. Each contains a disposable SKILL.md, responsibility, current signals, summary, subject index, 832 routine history records plus domain actions, and supporting evidence. A `task.md` supplies the same decision/output contract. Run a fresh evaluator with only that case path and task; it must not receive this generator, prior findings, or expected answers.

Independent forward-testing follows the skill-creator guidance. Evaluators are instructed to read only their own case directory, use no network or live systems, and write only case outputs. These are instructed scope boundaries; no OS-enforced read sandbox is claimed. Case generators and reviewer expectations remain outside that allowed scope.

This first pass uses one fresh agent per domain with the same draft skill and seeded history. It does not compare a baseline, repeat seeds, test agent-authored history, execute external effects, or simulate several full agent cycles. An archive spanning a year is a data horizon, not elapsed execution time. The [recall evaluation design](../../docs/recall-evaluation.md) requires those further comparisons before acceptance.

The [first-pass findings](NOTES.md) and [complete synthetic inputs and outputs](results/first-pass/manifest.json) are preserved. All four agents made supported decisions on these inputs. All four also reported truncated whole-archive reads before switching to targeted retrieval. The fixtures are deliberately an initial probe and have substantial limitations documented in the findings.

The skill is not installed. Its evaluated version remains frozen alongside the results. Discard the draft or absorb justified changes after comparison. Do not claim skill reliability from four probes or frontmatter validation.
