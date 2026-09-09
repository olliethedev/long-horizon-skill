# Skill repository and evaluation layout

Historical research proposal and v1 implementation notes. The [native-tools revision](native-tools-revision.md) removes runtime helpers and adds a comparison across three native harnesses; the distributed bundle now contains instructions and templates only.

Research-informed proposal, September 8, 2026. The user supplied [Ponytail](https://github.com/DietrichGebert/ponytail) as a reference. Inspected revision: `356918eba965ee1eac64bd3a7f0dd02108350de5`. Framework and runtime remain open; [ADR 0013](adr/0013-use-readable-files-for-durable-history.md) selects readable files for durable history, with exact formats still to be prototyped.

The [source review](research/ponytail-evaluation-patterns.md) checks what the runner and graders actually measure. It identifies gaps in treatment-version pinning, judge input selection, and open-feature completion checks; those limitations accompany the useful patterns below.

## What to carry over

Ponytail separates installable instructions in `skills/`, deterministic checks in `tests/`, and model evaluations and reports in `benchmarks/`. Its package manifest lists runtime files; ordinary CI runs package/helper checks and consistency checks. See [package.json](https://github.com/DietrichGebert/ponytail/blob/356918eba965ee1eac64bd3a7f0dd02108350de5/package.json), [test workflow](https://github.com/DietrichGebert/ponytail/blob/356918eba965ee1eac64bd3a7f0dd02108350de5/.github/workflows/test.yml), and [benchmark configuration](https://github.com/DietrichGebert/ponytail/blob/356918eba965ee1eac64bd3a7f0dd02108350de5/benchmarks/promptfooconfig.yaml).

Its [agentic benchmark](https://github.com/DietrichGebert/ponytail/blob/356918eba965ee1eac64bd3a7f0dd02108350de5/benchmarks/agentic/README.md) preserves workspaces for later scoring. Its [.gitignore](https://github.com/DietrichGebert/ponytail/blob/356918eba965ee1eac64bd3a7f0dd02108350de5/.gitignore) excludes routine generated runs, while selected findings live in tracked reports. Retaining reviewable evidence deliberately is useful here too.

Ponytail's many platform wrappers serve its distribution needs. This one-machine Impulse project does not yet need them. Its [copy checker](https://github.com/DietrichGebert/ponytail/blob/356918eba965ee1eac64bd3a7f0dd02108350de5/scripts/check-rule-copies.js) checks compact copies and selected shared phrases; the skill-to-compact-rule comparison is explicitly a canary, not full equivalence. Prefer one maintained runtime skill source here; introduce generated or copied forms only for an actual target.

## Proposed layout

```text
skills/long-horizon/
  SKILL.md                 runtime instructions, including thorough setup
  references/              supporting detail when needed
  scripts/                 helpers justified by prototype evidence
evals/
  cases/                   task requests and case definitions
  fixtures/                synthetic projects, histories, services, user answers
  graders/                 artifact checks and published judgment rubrics
  calibration/             known sound and faulty outcomes to check graders
  runs/                    generated workspaces and traces, normally ignored
  results/                 reviewed findings and retained evidence
tests/                     deterministic tests for implemented helpers and graders
docs/                      design, ADRs, research, evaluation plans
prototypes/                disposable explorations with recorded findings
```

Create paths as they acquire a purpose; this proposal is not an instruction to scaffold empty directories. The existing four-probe archive stays where its report and hashes reference it. Absorb useful prototype code deliberately while preserving evidence provenance.

The complete-cycle exploration packaged its exact evaluated candidate in `skills/long-horizon/` at commit `62fec70`. That runtime folder is now the maintained v1 source. The original copy under `prototypes/full-cycle/skill/` is frozen experimental evidence, not a second runtime implementation. V1's maintained evaluations live in `evals/`, public CLI/installation checks in `tests/`, and historical prototype fixtures/results remain under `prototypes/`. No empty framework directories or distribution wrappers were added. The runner uses the installed Codex CLI and Python's standard library; adopting Promptfoo is not necessary for these stateful comparisons.

Product workspaces and real project cost configuration belong outside the skill distribution. Synthetic fixtures can model any user-provided cost method. Authoring instructions and grader answers must remain outside evaluated workspaces; directory layout alone does not enforce read isolation.

## Verification layers

1. **Ordinary checks:** metadata, references, actual helper behavior, grader calibration, and relevant packaging contracts. Matching skill wording cannot establish agent behavior.
2. **Focused behavioral probes:** setup interviewing, evidence interpretation, history retrieval, and custom project-limit handling. Compare matched inputs with and without the candidate skill; disclose when a trial ends at a proposed decision.
3. **Several-session execution:** agents act against synthetic services, write their own history, arrange continuation through isolated Impulse or a controlled substitute, and resume in fresh sessions. Inspect effects, uncertain receipts, concurrent work, shared budgets, and termination. A later real elapsed-time pilot covers separate operational uncertainty.

Promptfoo, used in Ponytail's focused benchmarks, remains a candidate. We need fresh sessions, a controllable clock, captured tool traces, and repeatable external-state fixtures. Assess framework fit against those requirements before selecting dependencies.

## Evidence and comparison integrity

Record case/fixture versions, exact tested skill bytes or hash, model and harness settings, loaded instruction/plugin sources, allowed tools, grading version and rubric, workspace artifacts, action/retrieval traces, and measured usage or explicit telemetry gaps. Keep the factual brief and authorization identical across arms. Self-reported access logs supplement captured traces; they do not replace them.

Separate preparation, agent execution, and scoring so deterministic checks can be rerun on preserved artifacts. Label LLM regrading that incurs new usage. Calibrate each grader with a justified outcome and a plausible failure for the same task; calibration demonstrates those cases, not general grading accuracy.

Judge useful completion and constraints before rewarding low cost, few calls, short memory, or fast execution. Doing nothing, dropping history, or prematurely ending ongoing work cannot count as an efficiency improvement merely because it uses fewer tokens.
