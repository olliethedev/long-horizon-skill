# Native tools evaluation — 2026-09-09

<!-- BEGIN INITIAL MATRIX -->
The initial comparison currently has **34 of 36 intended decisions**, independently reviewed against original sources: **22 semantic passes and 162/170 observable criterion components**. Removing the helper did not produce a consistent success or efficiency advantage. Codex passed every completed cell; Claude and Antigravity often retrieved the right records but made material authority, chronology, or causal claims that contradicted those records.

Two Claude post-PR cells remain pending native authentication renewal. They are **ungraded**, not semantic failures. The published-helper attempt failed before generation with `OAuth session expired and could not be refreshed`; native telemetry reported zero API duration, tokens, and estimated cost. No completed decision was repeated.

## Design and preserved identities

The predeclared matrix is three actual native harnesses × three treatments × four domains, one initial decision per cell. Every treatment receives identical raw inputs and task text except skill activation. Both skill arms use the same activation sentence and `/workspace/skill` location. Grading material, evaluator code, other cases, repository instructions, and live projects are outside the isolated sessions.

- Published helper: exact `skills/long-horizon` from commit `be8d5901028abb11247664cea1e0f3af087e34fd`, frozen by `git archive`; tree SHA256 `f2bd37c0fb8da35e2998f4baa6e04c7079852e13b677f92130121d863671da12`.
- Initial native-tools candidate: tree SHA256 `d2fc4f19934888d2b59fae0cbac46eb87b1b43c00033593be2563d5ba22b9b7e`. Both frozen bundles contain 12 files.
- Codex CLI 0.153.4: installed `gpt-6-astra`, `xhigh`, service tier `default`.
- Claude Code 2.1.266: installed `claude-fable-5-1[1m]`; native traces resolve `claude-fable-5-1` with the 1M context configuration. No effort override was configured.
- Antigravity 1.1.27: no installed model/effort override; fresh native logs resolve Gemini 3.8 Flash (High). The evaluator supplied no model/effort flag.

Each domain contains 7,273–7,274 files and 8,212,441–8,239,173 raw text bytes. Before any main outcomes, the evaluator increased linked background chains from 720 to 2,400 per domain because Claude's installed configuration exposes a 1M context. Raw bytes are an approximate difficulty measure, not a tokenizer measurement. Individual history record filenames, action/evidence IDs, and receipts share an opaque namespace; briefs, current state, navigation files, and legitimate subject/cohort cues remain descriptive. Background actions also occur beside retained terminated work. Repeated templates and a finite background cohort vocabulary remain limitations.

The opaque transformation removed geography encoded only in individual export job/workspace names. A [separate clarification](matrix-2026-09-09/large-export-observability-clarification.json), recorded before any export session launched, treats that geography as unobservable for all nine export cells. Grading still checks exact job/workspace identity, format, row scale, failure, and explicit correction exclusion. The delivered action's stated paid-US/EU scope remains observable. These results do not demonstrate individual regional recall.

## Initial outcomes

Semantic success requires all five declared source-backed criteria **and no material contradictory decision**. A correct next action does not erase contradictory reasoning elsewhere in the decision or proposed persisted handoff. Full decisions, criterion sources, and material claims were manually reviewed. Incidental errors are retained in each review's notes and the aggregate output.

| Harness | Treatment | Revenue | Weekly product | Large export | Post-PR | Semantic passes | Criteria satisfied |
|---|---|---|---|---|---|---:|---:|
| Codex | No skill | Pass | Pass | Pass | Pass | 4/4 | 20/20 |
| Codex | Published helper | Pass | Pass | Pass | Pass | 4/4 | 20/20 |
| Codex | Native tools | Pass | Pass | Pass | Pass | 4/4 | 20/20 |
| Claude | No skill | Pass | Fail | Fail | Pass | 2/4 | 19/20 |
| Claude | Published helper | Pass | Fail | Pass | Pending auth | 2/3 | 15/15 |
| Claude | Native tools | Pass | Fail | Pass | Pending auth | 2/3 | 15/15 |
| Antigravity | No skill | Pass | Fail | Fail | Pass | 2/4 | 19/20 |
| Antigravity | Published helper | Fail | Fail | Fail | Pass | 1/4 | 16/20 |
| Antigravity | Native tools | Fail | Fail | Fail | Pass | 1/4 | 18/20 |

The export counts cover only observable portions of the unchanged criteria. Denominators exclude the two ungenerated Claude decisions.

The consequential failures were:

- **Authority:** all Claude and Antigravity weekly decisions invented an owner-approval or domain restriction because related digest work originated in a terminated responsibility, despite the active brief authorizing ordinary work on that requested product concern. Both no-skill baselines made this error too.
- **Missing source chains:** Antigravity helper weekly omitted the original 28% usage correction and contributor/admin digest audits, satisfying 3/5 criteria. Its export decision omitted the retired streaming deployment and original 10k benchmark/correction chain, also satisfying 3/5. Native tools recovered those chains, but other contradictions still prevented semantic success.
- **Unknown relative time:** Claude no-skill and Antigravity no-skill/native export explicitly claimed both tickets postdated rollout although one submission time was unknown. Preserving `null` elsewhere did not repair the contradiction.
- **Unsupported causes and conclusions:** Antigravity helper/native revenue invented cancellation/refund causality; native additionally said the inconclusive Harbor result “proved Harbor was not a loser.” All Antigravity export treatments asserted an unproved cursor-resume mechanism. Claude no-skill export explicitly ruled out selection/count explanations without evidence.

Passing decisions still had caveats. Examples include Claude's false claim that an August index predates every cited correction, overconfident compressed ticket-to-job handoffs, Antigravity's unsupported minimum observation windows and “18 devices” paraphrase of 18 QA runs, and post-PR summaries implying a later correction caused an earlier rollback. The manual reviews distinguish these from contradictions that materially change the evidence interpretation or authorized next decision.

## Native usage and retrieval

These are native reported totals for completed decisions plus the zero-use Claude infrastructure attempt. **Compare treatments within a harness.** Codex input includes cached input as a subset; Claude reports cache reads/writes separately from input; Antigravity reports cache reads separately and its reported total equals input plus output. Missing fields remain unknown. Dollar values are Claude's **reported estimates, not actual subscription charges**.

| Harness / treatment | Decisions | Input tokens | Cache read | Cache write | Output tokens | Reported estimate USD |
|---|---:|---:|---:|---:|---:|---:|
| Codex / no skill | 4 | 1,447,589 | 1,238,400 | 0 | 19,120 | Unreported |
| Codex / helper | 4 | 1,672,600 | 1,507,456 | 0 | 24,102 | Unreported |
| Codex / native | 4 | 2,326,761 | 2,041,984 | 0 | 25,111 | Unreported |
| Claude / no skill | 4 | 1,448 | 1,395,913 | 165,270 | 55,705 | 6.45410825 |
| Claude / helper | 3 | 1,254 | 1,436,527 | 162,673 | 45,479 | 5.89908175 |
| Claude / native | 3 | 838 | 1,107,054 | 167,754 | 45,404 | 5.91042350 |
| Antigravity / no skill | 4 | 1,083,963 | 8,549,433 | Unreported | 120,036 | Unreported |
| Antigravity / helper | 4 | 1,214,123 | 9,809,743 | Unreported | 125,551 | Unreported |
| Antigravity / native | 4 | 1,213,598 | 9,632,655 | Unreported | 124,450 | Unreported |

| Harness / treatment | Elapsed seconds | Tool calls | Reported failed tools | Captured tool-output bytes |
|---|---:|---:|---:|---:|
| Codex / no skill | 698.689 | 72 | 6 | 4,277,051 |
| Codex / helper | 903.500 | 158 | 5 | 609,109 |
| Codex / native | 921.793 | 92 | 4 | 9,296,014 |
| Claude / no skill | 901.750 | 66 | 0 | 246,386 |
| Claude / helper | 753.463 | 63 | 1 | 280,374 |
| Claude / native | 706.931 | 62 | 1 | 315,972 |
| Antigravity / no skill | 694.992 | 220 | 4 | 570,933 |
| Antigravity / helper | 770.385 | 229 | 5 | 604,523 |
| Antigravity / native | 713.904 | 237 | 6 | 655,201 |

Elapsed seconds sum recorded native-process durations, including the 0.459-second pre-generation Claude failure; overlapping execution means these sums are not wall-clock matrix duration. Claude helper/native still have fewer generated decisions.

Native guidance did not guarantee smaller retrieval: Codex native captured substantially more output and reported more input than helper while both passed. Captured output bytes are **not measured model-context exposure**; native tools can retain full output while presenting bounded views. Truncation markers and the descriptive 20 kB threshold are diagnostics, not semantic gates. Antigravity diagnostics use its preserved full native transcript because stdout file-read events contain concise summaries.

The failing skill sessions received the full entrypoint and relevant history/evidence/workspace references in captured tool outputs, rather than reading only the entrypoint. Exact source-text matches establish availability, not comprehension. Full per-session usage, reasoning counts, elapsed time, tool inputs, failures, citation diagnostics, reference matches, and review caveats are in [reviewed-results.json](matrix-2026-09-09/reviewed-results.json) and the [initial](matrix-2026-09-09/tool-diagnostics.json) / [completion](completion-antigravity-2026-09-09/tool-diagnostics.json) diagnostics.

## Infrastructure, interruption, and limits

All three neutral native tool preflights passed. The first Antigravity preflight attempt failed in CLI parsing before generation; using `--print=<prompt>` corrected the invocation. No-model isolation/auth-discovery attempts and executed sources are retained in [infrastructure evidence](infrastructure-2026-09-09/notes.md).

The initial runner launched 32 attempts: 31 decisions and one Claude pre-generation authentication failure. It stopped the remaining four cells and cleaned all 32 temporary homes. The [separate Antigravity completion](completion-antigravity-2026-09-09/manifest.json) added the three untouched post-PR cells using the original d2 bundle, exact archived inputs/prompts, and unchanged defaults. Thus there are **35 attempts, 34 generated decisions, and two pending intended cells**. The original manifest, failure trace, and skipped-cell records remain unchanged.

The [initial provenance audit](matrix-2026-09-09/provenance-audit.json) passes all identity/default/prompt/input/cleanup checks and retains three expected operational failures: the failed Claude cell, its absent semantic review, and the incomplete launched set. The [completion audit](completion-antigravity-2026-09-09/provenance-audit.json) passes 41/41 checks. Exact credential scans found zero matches in [59,171 initial streams](credential-scan.json) and [74,005 completion-time streams](credential-scan-completion-antigravity.json), including decompressed gzip and tar members. The scanner kept observed credential values in memory and never printed or archived them. Owned temporary authentication copies and initial/completion processes were cleaned.

No external-service, scheduling, or delegation tools were observed in those decision traces. Flagged home-directory commands only searched isolated `AGENTS.md` filenames or read native spilled tool-result files. Filesystem and PID isolation are enforced; host networking remains available for native model transport, so external restraint is also a task instruction, not a network allowlist.

This is a synthetic, explicitly activated skill comparison with one decision per cell. It does not establish statistical reliability, automatic skill discovery, live scheduler execution, production mutation safety, or customer outcomes. Different models and native accounting prevent cross-harness efficiency ranking. Authentication interruption also leaves the Claude treatment comparison incomplete.
<!-- END INITIAL MATRIX -->

<!-- BEGIN FOCUSED -->
## Focused refinement verification

The [predeclared refinement plan](refinement-plan-2026-09-09.json) selected five post hoc probes before changing the runtime: Claude weekly; Antigravity revenue, weekly, and export; plus the previously passing Codex export control. The refined candidate is `af8084aa46624ee25271c94ef14e1593f7adb6d325da156348132a8620ac4d26`. It clarifies active-brief authority, unknown relative time, and the distinction between observations and causal hypotheses before persisting explanatory claims. Original failures and the d2 candidate remain preserved.

Four available probes completed once each with unchanged original snapshots, prompts, criteria, native binaries and installed defaults. **Two passed semantic review; all four satisfied the five explicit observable criteria.** Claude weekly remains pending authentication. No successful decision was repeated in response to these outcomes, and no additional repetitions of these generated focused decisions are planned.

| Harness / domain | Semantic result | Criteria | Interpretation |
|---|---|---:|---|
| Claude / weekly product | Pending auth | Ungraded | Preselected probe remains unrun. |
| Antigravity / revenue | Fail | 5/5 | H1 is now consistently inconclusive, but invented cancellation/refund economics and discount causality remain. |
| Antigravity / weekly product | Fail | 5/5 | Still invents a retired-domain authority ban and claims desktop latency was solved without supporting large-workspace evidence. |
| Antigravity / large export | Pass, with caveats | 5/5 | Preserves unknown request time and explicitly labels cursor causality as a hypothesis requiring inspection/reproduction. Compressed handoff wording remains too categorical. |
| Codex / large export control | Pass | 5/5 | Preserves unknown relative ordering, conditional causality, source scale/format limits, and active authority. |

Full revised entrypoint/history/evidence/workspace text was present in the failing Antigravity sessions' captured tool outputs. Thus the remaining failures occurred despite availability of the new guidance. The export pass supports only this focused instance: its summary's “cursor loss” wording and unvalidated 1–2-hour TTL proposal remain recorded caveats, just as analogous uncertainty compression was retained in passing initial Claude export decisions. Materially unqualified causal assertions and explicit both-tickets-postdate claims were failures under the same standard.

| Focused cell | Elapsed seconds | Input tokens | Cache read | Output tokens | Tool calls | Captured tool-output bytes |
|---|---:|---:|---:|---:|---:|---:|
| Antigravity / revenue | 183.963 | 338,113 | 1,982,440 | 32,807 | 59 | 176,522 |
| Antigravity / weekly product | 217.984 | 331,166 | 3,433,350 | 40,210 | 62 | 202,567 |
| Antigravity / large export | 198.123 | 306,749 | 2,952,805 | 33,168 | 64 | 161,948 |
| Codex / large export | 244.070 | 583,826 | 511,616 | 6,353 | 22 | 2,575,278 |

Native accounting and captured-output limitations are the same as above; no dollar estimate was supplied by either harness. These selected probes cannot replace the initial matrix or establish a balanced treatment effect. See [focused outcomes and complete usage](focused-available-2026-09-09/reviewed-results.json), [tool diagnostics](focused-available-2026-09-09/tool-diagnostics.json), and [51/51 passing provenance checks](focused-available-2026-09-09/provenance-audit.json). The [focused credential scan](credential-scan-focused-available.json) found zero exact-value matches across 118,005 raw/decompressed streams. All four temporary homes and native processes were cleaned; no external, scheduling, or delegation tool use was observed.
<!-- END FOCUSED -->

<!-- BEGIN SETUP -->
## Offline setup probes

Two of the three separately assigned setup cases ran on the final `af8084aa…` candidate. Both produced decisions with unchanged inputs and satisfied their three explicit setup-choice criteria. Full source-backed review passed Codex and failed Antigravity; the Claude reminder-only case remains pending login.

| Harness | Captured target case | Recommended scheduler | Full decision review |
|---|---|---|---|
| Codex | Suitable Relay already configured, Impulse also available | Preserve Relay | Pass |
| Claude | Bell sends reminders but cannot launch agents; Impulse available | Untested | Pending auth |
| Antigravity | No scheduler installed | Propose Impulse | Fail: activation/timing plan |

Codex reused the settled owner answers, established Relay's capabilities from captured help, kept first-run timing conditional on completed setup, and required authorization before a live registration. Antigravity correctly recognized the missing scheduler and recommended Impulse, but its ordered plan placed registration and a confirmed configuration before final owner go-ahead. It also converted “next Monday after setup completes” into an already agreed fixed date without a fallback. These defects matter even though the offline session performed no registration.

Antigravity's concrete TOML draft also used unsupported `first_run.time`. A [supplemental reviewer check](setup-available-2026-09-09/supplemental-setup-check/result.json) with the installed Impulse CLI and a disposable `IMPULSE_HOME` rejected that exact draft field. Its proposed validation step would expose the error before registration; this check is separate from the captured-inventory model evaluation. The runtime skill's own template was unchanged and does not contain that field. The decision also overstated scheduler history retention as a guarantee for product evidence files.

The [setup archive](setup-available-2026-09-09/manifest.json) preserves exact sources, prompts, inputs, final skill bytes, traces, and decisions. [Reviewed results](setup-available-2026-09-09/reviewed-results.json) include native usage and time. [Provenance checks](setup-available-2026-09-09/provenance-audit.json) passed 31/31. The [credential scan](credential-scan-setup-available.json) found zero exact-value matches across 147,693 raw/decompressed artifact streams. Both temporary credential homes were removed and no owned model process remained.

These cases test reasoning over supplied inspection exports, not actual target-machine discovery, installation, scheduling or customer outcomes. Each harness received a different case, so these probes cannot compare harness quality statistically. No new live product task or global skill installation was performed.

## Remaining authenticated validation

Four Claude decisions remain pending `claude auth login`: the original helper/native post-PR cells on the frozen d2 candidate, the preselected weekly-product follow-up on the final candidate, and the reminder-only setup case. Completed decisions will not be repeated. Publication remains pending this required validation unless the owner changes the agreed scope.
<!-- END SETUP -->

## Repository review and deterministic checks

The [two-axis review](../../../docs/review-native-tools.md) found no remaining implementation findings after documentation corrections; it preserves the pending Claude validation separately. All four deterministic tests, strict typechecking of 14 maintained modules, official skill metadata validation, current documentation links, and maintained-file whitespace checks pass. Original trace whitespace is retained. The [generic credential-pattern scan](credential-pattern-scan.json) found no matches across 147,721 raw/decompressed streams, supplementing the exact observed-value scans above. Historical prototype and v1 archives are unchanged.
