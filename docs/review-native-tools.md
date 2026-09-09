# Native tools revision review

Two independent reviewers inspected the staged revision against the published base `be8d5901028abb11247664cea1e0f3af087e34fd` using `git diff --cached be8d590`. The maintained-file review excluded frozen results from code-style changes, then inspected the central report and relevant archive identities separately. Sources were CONTRIBUTING.md, CONTEXT.md, accepted ADRs, and [the current revision specification](native-tools-revision.md).

## Standards

One documented-standard mismatch: CONTRIBUTING required Python’s standard library, while the Antigravity host-auth adapter uses the installed system Python D-Bus binding. The dependency was already described in the evaluation guide. The policy now explicitly permits this narrow host-auth prerequisite and distinguishes it from the distributed skill, which remains instructions and templates only. The reviewer verified the correction and reported no remaining Standards findings.

The setup guide also incorrectly described sequential execution after its runner adopted two workers. It now documents at most two concurrent sessions. No runtime or evaluator behavior changed to resolve these documentation findings.

## Spec

No additional implementation findings. The runtime preserves the accepted authority, evidence, chronology, retention, lifecycle and scheduler requirements. The evaluation tooling uses actual harnesses, freezes matched inputs/prompts/bundles, separates completion attempts from selected refinement probes, and retains original failures. The reviewer checked all 40 reviewed decisions against their recorded SHA256 values.

Known incomplete validation remains separate: the requirement to “Run the matched 36-session comparison” currently has 34 initial decisions. Two initial Claude post-PR cells, the preselected Claude weekly follow-up, and the reminder-only setup case need renewed native authentication. The [results report](../evals/results/native-tools/REPORT.md) marks them pending and leaves publication pending. Remaining semantic failures are disclosed; they were not rescored as successes.

## Verification

- Official skill metadata validation passes for the final runtime tree `af8084aa46624ee25271c94ef14e1593f7adb6d325da156348132a8620ac4d26`.
- All four deterministic tests pass; strict mypy passes for all 14 maintained evaluation modules.
- Maintained-file whitespace checks and current documentation links pass. Frozen native outputs retain their original line endings and whitespace.
- Initial, completion, focused and setup provenance checks preserve exact candidate/input/prompt identities and cleanup; the initial audit explicitly retains the known operational interruption.
- Exact observed-credential scans and the [generic credential-pattern scan](../evals/results/native-tools/credential-pattern-scan.json) found no matches. The latter checked 147,721 raw/decompressed artifact streams.
- Historical prototype, v1 recall, and Impulse integration archives are unchanged. No owned temporary evaluation authentication homes remain.

Standards: one documented mismatch resolved, zero open findings. Spec: zero additional implementation findings; one known validation requirement remains incomplete pending four Claude decisions.
