# V1 implementation review

Two independent reviewers inspected the staged implementation against baseline `62fec7085a63ab0749fa9c8d7b701dff9006138f` using `git diff --cached 62fec70`. The baseline was the only commit; implementation commits follow review. Standards sources were CONTRIBUTING.md, CONTEXT.md, and accepted ADRs. The specification was docs/v1-spec.md plus those domain decisions. The original helper reviewed is retained in the [main evaluation's loaded bundle](https://github.com/olliethedev/long-horizon-skill/blob/be91b6929b4910042e71ddf704c0801b4d611d39/evals/results/v1-recall/2026-09-08-dense-matrix/loaded-skill/scripts/history.py).

## Standards

**One documented-standard violation, P2: stale cursors can silently omit corrected evidence.** The original helper's inventory recorded only path, size, and modification time and hashed that metadata as its search version. The spec requires the helper to “reject stale continuation cursors”; CONTRIBUTING.md makes explicit incomplete coverage a behavioral contract. A CLI probe retrieved page one, changed `offer good` to equal-length `offer fail`, restored the original modification time, then resumed. The helper accepted the cursor, reported the same version, omitted the corrected first line, and returned no continuation. Timestamp-preserving replacement therefore defeated the contract. The reviewer recommended content identity and search consistency validation.

No material baseline code-smell findings warranted changes. The reviewer's probe touched temporary files only.

## Spec

**One finding, P2: stale search cursors can silently omit corrected evidence.** The spec requires the helper to “reject[] stale continuation cursors.” Replacing a previously returned line with a same-length correction and preserving its original modification time left the search version unchanged. An independent CLI reproduction changed `offer failed` to `offer passed`, restored the timestamp, and resumed the old cursor: exit zero, corrected line skipped, no continuation. The reviewer recommended source-content identity and a regression for timestamp-preserving replacements.

No additional missing/partial requirements or scope creep were found. Setup, authority, lifecycle, retained evidence, coordination, optional limits, reporting, and stated evaluation boundaries aligned with the accepted requirements.

## Resolution and verification

A public CLI regression reproduced the defect before the change. The helper now includes SHA-256 source-content identities in the search inventory and compares inventories again after retrieval. Hashing uses bounded chunks, and paged reads share the same hashing function. All nine helper CLI tests and strict typechecking passed after the fix. The skill's behavioral prose was unchanged; the final bundle receives a separate fresh-agent check because its helper bytes changed.

Both reviewers independently repeated their original reproduction against the corrected helper: the stale cursor now exits with code 2 and requests a restarted search. Both confirmed their finding resolved and reported no remaining material findings. The final deterministic suite passed all ten tests; strict mypy passed for all four maintained Python source files.

Standards: one P2 finding, resolved, zero open. Spec: one P2 finding, resolved, zero open. Both findings concerned the same cursor-integrity defect.
