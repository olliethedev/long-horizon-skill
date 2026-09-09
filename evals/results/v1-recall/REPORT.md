# V1 independent recall comparison — 2026-09-08

All eight completed decisions passed the predeclared semantic checks: **20/20 baseline and 20/20 skill**. This sample demonstrates correct decisions with the complete v1 bundle, with no observed decision-quality advantage over the matched baseline. The skill produced much smaller captured command output, while using more commands, more total reported input tokens, and more per-session elapsed time.

## Decisions inspected

The evaluator independently authored the cases and reviewed each saved decision against original action/evidence records, including the scope of corrections, actual deployments/rollbacks, unknown timestamps, and terminated responsibilities. No keyword or JSON-schema score substitutes for that review. The source dossier retains the exact originals inspected: [source-review.md](2026-09-08-dense-matrix/source-review.md). Per-criterion judgments are in [manual-review.json](2026-09-08-dense-matrix/manual-review.json).

| Domain | Baseline | Skill | Supported decision in both arms |
| --- | ---: | ---: | --- |
| Revenue A/B | 5/5 | 5/5 | Reject unchanged Quiet Return R7; test Harbor H2 only as a changed-condition, still-unproven hypothesis. |
| Weekly product | 5/5 | 5/5 | Prepare a small Android filter slice; investigate the separate legacy contributor digest gap. |
| Large export | 5/5 | 5/5 | Keep both reports open; distinguish expired CSV links from NDJSON omissions at 1M+ rows. |
| Post-PR monitoring | 5/5 | 5/5 | Keep monitoring open; reconcile the queued release identity, confirm exposure, and coordinate overlapping routing. |

Each domain directory contains directly readable `baseline/work/decision.md` and `skill/work/decision.md`: [revenue](2026-09-08-dense-matrix/cases/revenue), [weekly product](2026-09-08-dense-matrix/cases/weekly-product), [large export](2026-09-08-dense-matrix/cases/large-export), [post-PR](2026-09-08-dense-matrix/cases/post-pr). Original virtual `/workspace/product` citations resolve to the preserved input archive; they have not been rewritten in the model outputs.

## Retrieval and usage

| Domain / arm | Commands | Captured output bytes | Largest result | Results >20,000 B | Input tokens | Cached input | Output tokens | Seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| revenue / baseline | 14 | 298,569 | 193,503 | 2 | 284,576 | 237,696 | 4,174 | 154.1 |
| revenue / skill | 38 | 54,675 | 7,156 | 0 | 316,572 | 269,952 | 5,482 | 208.3 |
| weekly-product / baseline | 16 | 354,422 | 119,905 | 3 | 296,538 | 253,824 | 5,073 | 176.8 |
| weekly-product / skill | 38 | 64,382 | 7,156 | 0 | 315,336 | 285,696 | 6,323 | 231.8 |
| large-export / baseline | 16 | 259,245 | 120,266 | 2 | 227,676 | 189,568 | 4,464 | 164.8 |
| large-export / skill | 30 | 50,784 | 7,156 | 0 | 242,303 | 217,472 | 5,431 | 188.4 |
| post-pr / baseline | 21 | 168,292 | 76,499 | 3 | 243,713 | 204,288 | 3,997 | 142.0 |
| post-pr / skill | 27 | 49,042 | 7,156 | 0 | 273,578 | 250,112 | 4,352 | 167.7 |

Across four sessions per arm, captured command output was **1,080,528 B baseline versus 218,883 B skill** (79.7% less); commands were **67 versus 133**. There were **10 versus 0** captured command results above 20,000 B. The skill used bounded helper searches and original-record reads, supplementing them with targeted ordinary commands. The baseline used broader listings/searches and then narrowed by stable identities. Both retrieved the decisive original source chains.

Total reported input was **1,052,503 versus 1,147,789 tokens**; cached input was **885,376 versus 1,023,232**; the uncached difference was **167,127 versus 124,557**. Output was **17,708 versus 21,588 tokens**, including the separately reported reasoning component. Summed per-session elapsed time was **637.7 versus 796.1 seconds**; these sums are not concurrent wall-clock duration. No subscription-quota or dollar conversion is inferred.

Captured output means UTF-8 bytes in CLI `command_execution.aggregated_output`, including listings and local verification. The CLI JSON does not expose each call’s model-visible output-token cap; zero observed truncation markers does not prove every byte reached the model. The runner caps each raw stdout/stderr stream at **32 MiB** and terminates on excess; no completed matrix case hit that cap or its 1,200-second timeout. The helper caps each response at 20,000 bytes and source pages at 8,000 bytes. These limits describe retrieval behavior, not decision correctness. Full definitions, commands, failures, file-change events, citations, and usage are in [metrics.json](2026-09-08-dense-matrix/metrics.json); each case also preserves compressed JSONL/stderr traces and an exact command/output summary.

## Protocol, isolation, and provenance

Four independently authored histories each contain **2,233–2,234 source files and 2.485–2.493 MB**. They include 720 linked action/observation/correction chains, overlapping subjects and aliases, varied cohorts/revisions, dated operations, support imports with unknown submission dates, and retained evidence from terminated responsibilities. The raw inputs were matched byte-for-byte across each pair and mounted read-only. No source mutations occurred. The only completed model file-change event in each session added `/workspace/work/decision.md`; the CLI also wrote the final response file.

Each session received only a realistic local handoff request and its raw product snapshot. The treatment also received the complete frozen skill directory. Private grading criteria, the repository, parent/grader state, other cases, broad host `/home`, and host `/tmp` were absent from the filesystem/PID namespace. The bwrap mount set contained OS runtime and certificate files, the native Codex and native code-mode-host binaries, a single per-case workspace, and a temporary minimal auth/config home. Apps, plugins, memory, skill search, browser/computer tools, and multi-agent features were disabled. Credentials were copied locally, excluded from artifacts, and removed after each session. Host networking remained available for the model API; restraint on external network actions was a task instruction, not a kernel network sandbox.

No live service calls, source modifications, credential reads, or prohibited production actions were observed in completed command/action traces. Several agents searched for AGENTS.md in the temporary home; those searches found no matching instruction file and did not read auth.json. Ten shell commands returned nonzero (four baseline, six skill): mostly absent optional files/no rg matches; one skill search used a nonexistent revenue releases directory and recovered after its explicit helper error. These are recorded, not removed.

Installed defaults were copied without model/effort overrides: **gpt-6-astra**, **xhigh**, service tier **default**, native Codex **0.153.4**. Sessions used `codex exec --ephemeral`, with no shared conversation, and at most two native Codex subprocesses at once. Exact initial prompts, native paths/binary hashes, config defaults, input file hashes, and all bundle file hashes are in the [run manifest](2026-09-08-dense-matrix/manifest.json).

- Bundle tree SHA-256: `3d9db0b18895957295f7a30774a250b392f2e5fec09a136e243c9571985d5df2`.
- SKILL.md SHA-256: `16251343938452bdde526c4107aa8772591efc43a5824895b70bfe45ac972eb6`.
- history.py SHA-256: `225eff796fb33bd8333902b5ebe9f1d7f4e9682a100e1b5f2d639edb7c8282e3`.

The exact evaluated bundle is under [loaded-skill](2026-09-08-dense-matrix/loaded-skill), and the exact executing runner/fixture source snapshots are preserved. Original inputs are in [inputs.tar.gz](2026-09-08-dense-matrix/inputs.tar.gz), with per-file hashes in case manifests. Later maintained-runner changes harden cleanup, stop queued cases after infrastructure errors, resolve the installed native executable, and archive inputs; they did not alter the completed model sessions or frozen runtime.

## All attempts and limitations

**Seventeen model-process attempts were launched: eight main semantic sessions, eight infrastructure attempts, and one separate post-review revenue follow-up described below.** Before inspecting any completed decision, the parent required increasing the initial approximately 160 KB fixtures to at least 2 MB. Two active small-history launches were interrupted and their partial captures retained; six queued cases never launched. In the first dense launch, two sessions failed TLS because `/etc/ssl` linked into an unmounted OS CA directory. In the next launch, four sessions connected but could not use workspace tools because the sibling native code-mode host was absent; each returned a tool-unavailable response. Those failures were corrected in isolated mounts, with no dense input or skill changes. None counts as a decision-quality failure or a hidden retry. [infrastructure-attempts.json](infrastructure-attempts.json) preserves their categories and recorded usage; missing usage is explicitly unknown, not zero. Their individual run directories retain prompts, source snapshots, manifests, and traces.

This is one session per arm/domain, with no statistical reliability claim. Both task prompts already request original-source citations and preservation of unknown dates, so the comparison measures incremental bundle value over an explicit evidence-oriented task. The evaluator saw the supplied skill and independently authored the fixtures, without reading frozen prototype conclusions; model sessions never received grading notes or expected answers.

The generated background histories are less organic than retained production archives. In particular, background action IDs occupy 4000–4719 and observation/audit filenames share a seed prefix; baselines used these patterns to prune many files. Some vocabulary also overlaps the skill’s retrieval examples. Thus the 2.49 MB size alone is not proof of difficult long-range recall. Template regularity, exact stable identifiers, concise decisive sources, and this model’s strong baseline limit generalization. No skill defect was established by these decisions, and no correctness, speed, or total-token superiority is claimed.

These read-only decision reviews do not exercise live deployment, notice delivery, scheduler receipts, recovery after uncertain external effects, or multi-session lifecycle completion. Separate lifecycle and real Impulse boundary evidence must remain separately labeled.

## Post-review cursor correction

After the eight-case matrix, independent code review found a helper defect outside these immutable-input cases: a same-size source correction with restored mtime could leave a metadata-only search cursor valid. The runtime owner added supported-file content hashes and before/after inventory consistency, with a public regression that failed before the fix and nine helper CLI tests passing afterward. Skill prose did not change. The main matrix remains tied to its historical `3d9db0...` bundle; its results are not relabeled as a test of the corrected implementation.

A separate fresh revenue/skill follow-up **passed 5/5** with identical prompt/input hashes and model defaults, using corrected bundle tree SHA-256 `f2bd37c0fb8da35e2998f4baa6e04c7079852e13b677f92130121d863671da12` (corrected history.py SHA-256 `42466b4a2a3a1b9abcda62a40789931d2cb1ac7335d6b7c2d66b1ac2f3004379`). Its [manifest](2026-09-08-cursor-fix/manifest.json), [decision](2026-09-08-cursor-fix/cases/revenue/skill/work/decision.md), and [manual review](2026-09-08-cursor-fix/manual-review.json) preserve the new exact sources and the inspected outcome. It used 42 commands, 66,971 captured output bytes, 386,905 reported input tokens (346,624 cached), 6,694 output tokens, and 260.7 seconds; there were no input mutations, capture-cap hits, or results above 20,000 B. It explicitly distinguishes its September 9 UTC finalization from the September 8 source snapshot. This checks ordinary retrieval and decision behavior after the fix; the public helper regression checks the mutation invariant. The follow-up is separate from the paired score and usage totals above.

## Repeat and validate

Requires Linux with working unprivileged bwrap, Python 3.11+, rg/bash in `/usr`, an OS CA trust store, native Codex plus its sibling `codex-code-mode-host`, and file authentication/config at the selected Codex home. The runner resolves native Codex from PATH; `--codex` supports an explicit binary and rejects unsupported launchers. A fresh result directory is required.

```sh
python3 evals/recall.py --output evals/runs/recall-preflight-new
python3 evals/recall.py --run --output evals/results/v1-recall/repeat-new
.venv/bin/mypy --strict evals/recall.py evals/fixtures.py
```

Only `--run` opts into authenticated model sessions. Defaults are two subprocesses and 1,200 seconds per case; SIGINT/SIGTERM finishes active sessions and skips queued work. A session that produces no decision or a systemic runner error also stops queued work. Initial sources are archived on completion.

[runner-validation.json](runner-validation.json) records eight passing filesystem/read-only probes and targeted capture-cleanup checks: normal output, a descendant holding pipes and ignoring SIGTERM after its leader exits (terminated in 3.011 seconds), and a 1,024-byte test capture cap (exactly 1,024 bytes retained). An artifact-open exception probe also verified child reaping and stream closure. Strict mypy passes. The final artifact check also verifies archived source hashes, paired-input equality, runtime byte identity, and absence of credential values or leftover temporary auth homes.
