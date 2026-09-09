# Native tools revision review

Two independent reviewers inspected the staged revision against the published base `be8d5901028abb11247664cea1e0f3af087e34fd` using `git diff --cached be8d590`. The maintained-file review excluded frozen results from code-style changes, then inspected the central report and relevant archive identities separately. Sources were CONTRIBUTING.md, CONTEXT.md, accepted ADRs, and [the current revision specification](native-tools-revision.md).

## Initial implementation — Standards

One documented-standard mismatch: CONTRIBUTING required Python’s standard library, while the Antigravity host-auth adapter uses the installed system Python D-Bus binding. The dependency was already described in the evaluation guide. The policy now explicitly permits this narrow host-auth prerequisite and distinguishes it from the distributed skill, which remains instructions and templates only. The reviewer verified the correction and reported no remaining Standards findings.

The setup guide also incorrectly described sequential execution after its runner adopted two workers. It now documents at most two concurrent sessions. No runtime or evaluator behavior changed to resolve these documentation findings.

## Initial implementation — Spec

No additional implementation findings. The runtime preserves the accepted authority, evidence, chronology, retention, lifecycle and scheduler requirements. The evaluation tooling uses actual harnesses, freezes matched inputs/prompts/bundles, separates completion attempts from selected refinement probes, and retains original failures. The reviewer checked all 40 reviewed decisions against their recorded SHA256 values.

At this first review, the matched comparison had 34 initial decisions and four Claude decisions remained ungenerated across the initial, focused and setup work. The owner subsequently renewed authentication and all four completed. That validation gap is resolved; the initial interruption and remaining semantic failures remain disclosed in the [results report](../evals/results/native-tools/REPORT.md).

## Verification

- Official skill metadata validation passes for the final runtime tree `af8084aa46624ee25271c94ef14e1593f7adb6d325da156348132a8620ac4d26`.
- All six deterministic tests pass, including recovery from a truncated gzip and visible failure for persistent corruption; strict mypy passes for all 14 maintained evaluation modules using the repository development environment.
- Maintained-file whitespace checks and current documentation links pass. Frozen native outputs retain their original line endings and whitespace.
- Initial, completion, focused and setup provenance checks preserve exact candidate/input/prompt identities and cleanup; the initial audit explicitly retains the known operational interruption.
- Exact observed-credential scans and the [generic credential-pattern scan](../evals/results/native-tools/credential-pattern-scan.json) found no matches. The original pattern scan checked 147,721 raw/decompressed artifact streams; the [resumed scan](../evals/results/native-tools/credential-pattern-scan-resumed-2026-09-09.json) checked 162,492 with zero matches. Two failed watchers lost their in-memory credential sets; later successful scans cannot establish coverage of temporary-only values that disappeared before another watcher observed them. Exact executed sources, failure evidence and coverage limits are retained in [scanner provenance](../evals/results/native-tools/credential-scan-claude-provenance.json).
- Historical prototype, v1 recall, and Impulse integration archives are unchanged. No owned temporary evaluation authentication homes remain.

## Authentication resumption and scanner correction

The resumed work adds four previously ungenerated Claude decisions, completing 36 initial, five focused and three setup decisions. All 44 reviewed decision files match their recorded SHA256 values. The runtime remains the same final candidate; the initial completion uses the original frozen d2 candidate. Historical prototype and v1 evidence remain unchanged.

Credential scanning encountered incomplete gzip files written by another evaluation batch. The maintained scanner now retains its sampled values while retrying incomplete archives, samples again on retries, and reports an explicit incomplete scan with a nonzero exit if bounded retries are exhausted. It never treats an unreadable archive as clean. Real-file regression tests exercise both recovery and persistent failure; failed watcher evidence and credential coverage limits remain preserved.

## Final resumption review — Standards

The independent reviewer found one scanner edge case: malformed DEFLATE data raises `zlib.error`, which initially bypassed the bounded retry and incomplete-report path. The documented explicit-failure contract required handling it. The correction now catches that exception, and the real-file persistent-corruption regression covers both truncated gzip and malformed DEFLATE bodies. The reviewer inspected the staged correction and confirmed the finding resolved. All three scanner tests and strict typechecking pass after the fix. No remaining documented-standard violations or actionable heuristic smells were found.

The reviewer independently checked the four resumed decision hashes, d2 versus af808 bundle identities, original-manifest links and exact scanner-source provenance. The report preserves semantic failures and the temporary-credential coverage limitation.

## Final resumption review — Spec

The independent reviewer found the same malformed-DEFLATE failure-report gap, then inspected the staged correction and confirmed it resolved. The agreed evaluation requirement is complete: 36 initial, five focused and three setup decisions, using the correct frozen candidates and unchanged criteria. No missing requirements, scope creep or additional implementation findings remain.

Standards: one resumed-delta finding resolved, zero open. Spec: one resumed-delta finding resolved, zero open. All agreed model sessions and required repository checks are complete; mixed semantic outcomes remain recorded as failures.
