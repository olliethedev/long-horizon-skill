# Native tools and scheduler discovery

Design interview completed September 9, 2026, following the owner's review of the published v1 implementation (`be8d590`). The owner accepted the plan with “sounds good”; implementation and evaluation are authorized. Review this revision against that published commit. Previously accepted continuity, authority, retention, and lifecycle decisions remain in force except where this document explicitly revises runtime packaging and scheduler selection.

## Owner-directed changes

- Remove `history.py` from the distributed skill. Teach the agent to locate and inspect retained records using its harness and available system tools, including search and appropriate date ordering. The owner wants the skill to explain the working method without shipping a custom retrieval program.
- Keep using readable files, source attribution, historical actions, applicable corrections, and product-scoped history. The underlying continuity and retention requirements remain in force.
- During setup, inspect relevant available tools and existing project configuration for a suitable scheduler. Impulse is the owner's expected tool and a recommendation when no suitable existing tool is available; it should not be assumed to be the only possible scheduler.
- Evaluate removal of the helper using the existing retrieval evaluation infrastructure and large-file-history cases. Evaluation programs belong to the development repository; removing runtime helper code does not imply removing evaluation tooling or historical evidence.

## Accepted revision decisions

1. **Reuse the project's established scheduler when suitable.** Accepted September 9, 2026. An existing project scheduler takes precedence over Impulse merely being installed. Recommend Impulse when no suitable scheduler is configured. Discover available tools and project choices before asking the owner to supply facts the agent can inspect.
2. **Check scheduling capabilities through the available tool.** Accepted September 9, 2026. A suitable scheduler can start a fresh agent session with the saved workspace and instructions, let the agent verify when the next run is scheduled, and let it reschedule or disable future runs. The agent can establish these capabilities from the tool's help or documentation; the skill does not require custom integrations for each scheduler. These capabilities preserve the existing wait, pause/manual-resume, and termination behavior.
3. **Evaluate Codex, Claude Code, and Antigravity.** Explicitly selected by the owner September 9, 2026. Exercise each actual harness and report results separately. A model API substituted for a harness would not test that harness's file tools. Installation alone does not establish that authentication, isolated sessions, and trace capture work; inspect and verify these before the evaluation matrix.
4. **Run the matched 36-session comparison.** Accepted September 9, 2026. Within each harness, compare no skill, the frozen published skill with its helper, and the revised skill using native tools across the four existing domains. Match inputs, task prompts, and model settings within each harness. Remove the easy filename clues from generated background histories. Assess actual evidence retrieval and supported decisions alongside time and token usage; lower output volume alone is not success. Preserve failures and original loaded bytes. Additional repeats should address observed failures or meaningful differences; one session per condition is exploratory evidence.

## Inspected implementation and evidence

At the start of this revision, the published skill directed retrieval through the bundled helper, and its scheduling reference and assignment template were Impulse-specific. The existing fresh-agent runner executed Codex, with matched baseline/skill arms across revenue, weekly product improvement, export feedback, and post-PR monitoring. That earlier study did not compare several harness products.

Local discovery on September 9 found `codex`, `claude`, and Antigravity's `agy` CLI on PATH, as well as Impulse and ripgrep. Installed `agy` reports version `1.1.27`; its local help documents noninteractive `--print`, structured JSON/stream-JSON output, and session/project options. This establishes an available CLI interface, not authenticated or isolated execution. No model session was launched during this discovery.

The published comparison found correct decisions in both arms. The helper reduced captured command output while increasing commands, total reported input tokens, and elapsed time; it did not demonstrate a decision-quality advantage. Original histories, prompts, loaded bundle bytes, and results are retained in [the evaluation archive](../evals/results/v1-recall/REPORT.md). They remain historical evidence when the active bundle changes.

The prior generated histories exposed easy-to-prune background naming patterns. A new evaluation should distinguish reproducing the existing comparison from testing more realistic retrieval difficulty. Sorting by a source's event or observation date also differs from sorting by filesystem modification time; the existing evidence-time distinctions remain relevant with native tools.

## Implementation and verification

The [native harness evaluation report](../evals/results/native-tools/REPORT.md) contains the current per-case outcomes, usage, infrastructure status, and preserved limitations.

The runtime bundle now contains only instructions and editable templates. Native retrieval guidance keeps original-source, chronology, correction, coverage, and workspace-scope checks without requiring a particular utility, read-size limit, or index. Scheduler selection lives in a general reference, while the existing Impulse reference and task definition remain conditional examples. Setup preserves already-granted authority and existing project choices.

The helper-specific CLI tests are retired with the runtime helper; their exact code and results remain in the published commit and archives. The copied-bundle test verifies that references and the optional Impulse template travel together without executable runtime code. Python typechecking applies to evaluation tooling. Metadata validation and the copied-bundle check pass for the initial revised candidate.

All three harnesses passed isolated native tool-use preflights. An initial Antigravity invocation failed before generation because its `--print` option consumed the next flag; that attempt is preserved, and the corrected invocation passed. The 36-session matrix uses the frozen published commit and candidate tree `d2fc4f19934888d2b59fae0cbac46eb87b1b43c00033593be2563d5ba22b9b7e`. Each matched domain has 7,273–7,274 files and approximately 8.2 MB of source text, with opaque IDs shared by original and generated evidence. Raw bytes do not establish exact token counts, and repeated templates remain a limitation.

Three separate offline scheduler-choice probes cover setup reasoning: an established suitable scheduler in Codex, a reminder-only scheduler in Claude Code, and no scheduler in Antigravity. They use captured target-machine inspection results and supplied owner answers. They do not test actual discovery, installation, or registration, and they are not a matched comparison across harnesses. No live product task or global skill installation is part of this revision.

The existing Impulse-specific ADR and implementation report describe the shipped v1. Record the resolved revision alongside that history rather than rewriting old evaluation results.

## Interpretation checks from the initial comparison

Source retrieval and decision accuracy are reviewed separately. Some completed decisions locate the required records but infer a restriction from an ended responsibility, assign a before/after relationship to an unknown request time, or turn a diagnostic association into a proven cause. The original decisions and criterion-level reviews remain in the archive, including failures. The final candidate adds three general clarifications: derive related-work authority from the active brief, preserve unknown relative request ordering, and distinguish observations from causal hypotheses when recording decisions and learnings. Its tree is `af8084aa46624ee25271c94ef14e1593f7adb6d325da156348132a8620ac4d26`. The [fixed five-session follow-up plan](../evals/results/native-tools/refinement-plan-2026-09-09.json) was recorded before the edit and launches; its selected failure cases and passing control are separate from the original comparison and cannot retroactively improve its scores.

## Current completion status

The final runtime candidate passes metadata validation and the copied-bundle check. All four deterministic development tests and strict typechecking of the 14 maintained evaluation modules pass. The [results report](../evals/results/native-tools/REPORT.md) records 34 completed initial decisions, four focused decisions, and two setup decisions with mixed semantic outcomes. Four required Claude decisions remain pending renewed native authentication; no completed decision is being repeated. Publication is pending those checks unless the owner revises the agreed evaluation scope.
