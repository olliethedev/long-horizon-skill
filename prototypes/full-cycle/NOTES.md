# Complete-cycle findings

September 8, 2026. The complete skill candidate supported useful work across all four simulated domains, but this comparison does **not** demonstrate an advantage over the no-skill baseline. Both arms recovered interruptions, acted on changed evidence, and preserved continuation. Retrieval was frequently too broad, and the skill arm used more recorded tokens and commands.

At completion of this study, the packaged candidate was byte-identical to the frozen [tested candidate](skill/long-horizon/SKILL.md), including its references. That original state is retained in commit `62fec70`. The [current runtime skill](../../skills/long-horizon/SKILL.md) has since evolved in the separately reported [v1 implementation](../../docs/v1-implementation.md). The candidate is the transferable workflow; the Python service is evaluation infrastructure, not a proposed production workflow engine. This study did not install the skill or use a live product.

**55 fresh sessions completed:** 48 in the paired matrix, five candidate-only setup/lifecycle sessions, and two corrected-weekly final-session rechecks. All processes exited zero; that does not mean every interpretation was correct. Semantic errors and instructed directory-boundary violations are retained below.

## What ran

The main matrix completed **48/48 fresh Codex processes**, all with exit code zero: four domains × baseline/skill × six sessions. Distinct thread IDs were captured for all 48 sessions; no conversation was resumed. The checkpoints were days 0, 0, 7, 14, 240, and 540. Each next agent inherited the files its predecessor actually wrote, with no reviewer editing of their substantive content.

Each trial contained the same owner brief and service API for its domain, retained earlier handoff-prototype records, and 18,000 generated background records. Common initial input hashes matched across arms. The skill arm additionally received the candidate and an explicit invocation; its read command was observed in every main skill session. This tests explicit use, not automatic discovery.

The installed harness was `codex-cli 0.153.4`, authenticated through ChatGPT. No model or reasoning override was supplied. A nonsecret configuration snapshot records nominal `gpt-6-astra` / `xhigh`; actual provider routing was not independently established. Agents used workspace-write execution with network access for the authorized loopback service. Full isolation from global instructions/plugins and hard filesystem read isolation were not established.

The service recorded actual configuration effects, paid validation credits, atomic evaluation reservations, measurements, scheduler state, operation receipts, and delivery to a synthetic owner inbox. After the first deployment, then the first scheduling call, the effect committed but the response was lost and further service access closed for that session. The agents could preserve local uncertainty before stopping. This is an interrupted-service simulation, not an operating-system process kill.

The [review protocol](REVIEW.md) separates state checks, retained evidence, and semantic interpretation. Seven deterministic calibration groups passed before the paired model runs. Manual review was unblinded; the prose review guide was written during the early sessions before later outcomes. No numerical acceptance threshold or independently validated model judge is claimed.

## Observed decisions

| Domain | No-skill baseline | Complete candidate |
| --- | --- | --- |
| Revenue A/B | Deployed compact copy; waited at day 14 under its tighter precision criteria; rolled back after the later −4% audit; did not repeat the renamed losing offer. | Deployed and adopted under its saved positive-lower-bound rule; restored detailed copy after the audit; did not repeat the renamed losing offer. |
| Weekly product | Implemented resumable setup with explicit template choice retained; kept observing; withdrew the activation benefit claim after the eligibility correction; recognized the later feature request as already delivered. | Implemented and adopted the capability; withdrew the activation claim after correction, retaining the functionality provisionally; avoided duplicate implementation. |
| Feedback | Fixed streaming/final-page handling; observed Elm/Ash recovery; later detected failure at two million rows, validated a larger page size, deployed it, and left the new customer outcome pending. | Same substantive sequence, with explicit retained action/evidence records. |
| Post-PR bugs | Checked actual production exposure, repaired the dependency quota, repeated the repair after a new provider reset, then adopted verified recovery. | Same substantive sequence; did not blame or change a merged PR absent from production. |

All eight chains made useful actual fixture changes. All recovered the original deployment and scheduling receipts in later sessions without duplicating those effects. Early observations remained inconclusive. All ended active with a confirmed future run and two delivered due digests. No implemented service violation flag fired; this is narrower than general correctness, and the filesystem-boundary issues below still count.

The final feedback configurations completed all six supplied exact-ID cases, including two million rows in a simulated 20 seconds at page size 10,000. Both used the last shared validation credit and stopped at 10/10. That functional result did not establish mature recovery for the new customer. The other domains ended at 9/10 shared credits, including another responsibility's consumption. All respected four externally active evaluations and the fifth shared slot.

The earlier-adoption differences are not an automatic skill win. The baseline's revenue protocol requested a tighter confidence interval, and its weekly protocol sought stronger downstream evidence. Both arms followed their own preserved criteria. These small fixtures cannot establish which choice would maximize real revenue or product value.

## Recall and preserved history

Before the final session, each chain's available current handoff was restored from day 14. All eight agents recovered relevant later actions/corrections from the underlying records and actual state. Only the weekly baseline had a root-level index to remove; its missing-index injection also applied. None of the skill arms created that optional index, so this is **not** evidence of four successful skill-index rebuilds.

Changed historical Markdown records appended dated correction, recovery, or applicability annotations while retaining the original text. Review found no original evidence-file deletion. The bugs baseline overwrote some mutable pending/resolved JSON pointers; its dated evidence and session records retained the historical receipts. Different layouts worked without a universal schema.

| Domain | Final baseline memory | Final skill memory |
| --- | ---: | ---: |
| Revenue | 51,643 bytes | 74,345 bytes |
| Weekly product | 73,741 bytes | 64,245 bytes |
| Feedback | 71,239 bytes | 85,754 bytes |
| Post-PR bugs | 60,307 bytes | 83,365 bytes |

The background archive was roughly 8.83 MB per trial, but consisted of repetitive generated events for distinct allocations. Critical new agent-authored history grew over six sessions and remained much smaller. All eight initial sessions produced a command with more than one million captured output characters; subsequent sessions sometimes did too. Several commands attempted entire-archive reads. Capture limits truncated output, so neither full retrieval nor economical selection can be inferred. The candidate's bounded-search instruction did not reliably control this behavior.

Two commands searched the parent matrix directory for `AGENTS.md`: baseline revenue at epoch 5 and skill weekly at epoch 3. They returned no files, but violated the instructed trial read boundary. No grader content was observed in those results. Input/candidate hashes remained unchanged, and captured file-change events showed no paths outside the trial. These observations are not proof of complete OS isolation.

Both weekly arms also described the support request as 540 days old. The fixture's `observation_age_days` measures time since first deployment; it does not date the request. The already-delivered capability decision has independent configuration/receipt support, but this age assertion is unsupported and could wrongly discount new feedback. The baseline repeated it in the corrected-endpoint recheck. This is a semantic evidence error, documented in a [review addendum](results/2026-09-08-main/review-addendum.json), and prevents treating every reviewed decision as wholly correct.

## Fixture correction and rechecks

The original weekly endpoint unexpectedly returned the old 42%/49% activation aggregate again at day 540 after correcting it to 42%/43% at day 240. This was identified and recorded **before** the final weekly results. The active service was left unchanged and its exact source preserved. Both original arms recognized the unresolved contradiction and declined to restore the benefit claim.

The corrected endpoint now supplies current configuration and explicitly no new controlled comparison. Two additional fresh final-session rechecks forked the original day-240 memories and repeated the same stale-handoff injection. Both completed, retained the audit correction, avoided duplicate implementation, and confirmed another observation and digest. The baseline again assigned a 540-day age to the request; the skill handoff also called it old without a supplied timestamp. Neither recheck establishes a fully clean interpretation of request provenance. Their [results and review](results/2026-09-08-weekly-recheck/manual-review.json) are retained separately and do not replace the original trials. `recheck.py SOURCE_ROOT` prepares this fork for reproduction.

## Focused setup and lifecycle probes

| Probe | Observed behavior |
| --- | --- |
| Access restored, owner has not resumed | Retained paused/disabled state, no future run, no spending or mutation, no duplicate notice. |
| Later explicit owner resume | Verified current prerequisites and scope, enabled work, validated once, reserved/deployed a new experiment, confirmed day-14 observation; did not claim an immature revenue gain. |
| Bounded verified success | Inspected actual prior deployment receipt and mature exact-ID/customer outcomes, terminated, disabled scheduling, delivered completion notice, retained evidence. |
| Bounded impossibility | Used the accessible-source audit showing permanent purge and no backups; terminated within the permitted recovery scope and delivered the conclusion. |
| Sparse new setup request | Asked which website/product to improve first with a short recommendation; no invented answers, spending, activation, or messages. |

All five fresh processes completed. These are candidate-only probes, not comparative evidence of improvement. The setup case covers the first interview turn only. The bounded-success agent checked ancestor `AGENTS.md` paths outside its allowed trial; no contents returned, but this is a third instructed-boundary violation across the complete evaluation. [Focused observations](results/2026-09-08-focused/focused-observations.json) distinguish seeded effects from new work; [manual review](results/2026-09-08-focused/manual-review.json) records the limits.

## Shared capacity and costs

An additional deterministic test used simultaneous HTTP clients, separate from the model trials. Atomic reservation admitted exactly one claimant to the last evaluation slot. Forcing two clients to read a shared 9/10 ledger before spending produced 11/10: separate read-then-spend checks race. A fixture-specific `fcntl.flock` around the whole check/spend sequence admitted one spender and ended at 10/10.

That guard assumes every spender participates and the meter reflects completed calls synchronously. Delayed billing and uncertain calls need project-specific pending-consumption rules. This does not justify a universal billing integration or moving budget ownership into Impulse. The main LLM chains saw shared background work; they did not themselves race two simultaneously acting responsibilities on one real product.

## Recorded work and usage

| Main matrix, 24 sessions per arm | Baseline | Skill |
| --- | ---: | ---: |
| Aggregate process seconds | 5,005.72 | 5,812.33 |
| Captured shell commands | 413 | 526 |
| Commands with >1M captured output characters | 6 | 9 |
| CLI input tokens | 9,379,998 | 10,316,554 |
| CLI cached-input tokens | 8,517,248 | 9,319,680 |
| CLI output tokens | 134,286 | 160,965 |

These are the CLI's reported categories, summed across turns; do not add cached input on top of input as though it were a separate bill. Aggregate process seconds are not wall-clock duration because trials ran concurrently. This is one sample with different decisions, record sizes, and variable runtime. It shows no efficiency advantage for the candidate. Token telemetry is not actual billed dollars or remaining subscription allowance.

## Artifacts and next decision

- [Main manifest](results/2026-09-08-main/manifest.json), [state checks](results/2026-09-08-main/grades.json), [captured-trace analysis](results/2026-09-08-main/analysis.json), and [manual review](results/2026-09-08-main/manual-review.json).
- [Readable case snapshots](results/2026-09-08-main/cases/) retain input/output memories, project requests, decisions, and service state.
- [Raw evidence archive](results/2026-09-08-main/raw-evidence.tar.gz) retains JSONL harness/service traces, original controller/server versions, generated sources, and calibration state. [Provenance hashes](results/2026-09-08-main/provenance.json) cover all preserved files and raw entries.
- [Focused probe artifacts](results/2026-09-08-focused/) and [corrected-weekly rechecks](results/2026-09-08-weekly-recheck/) preserve separate manifests, snapshots, raw traces, hashes, and reviews.
- [Combined verification summary](results/summary.json): 55 distinct recorded thread IDs, 4,173 archive files and 212 compressed raw entries hash-verified. Candidate metadata and reference links validate. Eight deterministic calibration groups now pass, including the added weekly-endpoint regression check.

The evidence supports keeping the architecture small: a skill, readable files, and Impulse, with service-specific coordination/accounting mechanisms where required. It does not yet justify an additional general-purpose workflow engine or vector database. Before broad adoption, prioritize selective retrieval and stronger evaluation workspace boundaries, then repeated harder histories with diverse corrections. A narrowly scoped, real elapsed-time post-deployment monitoring pilot would cover actual Impulse continuation and deployment exposure; its product, access, actions, limits, and reporting destination still need the owner's setup interview.

Six checkpoints over a synthetic 18-month clock do not represent every weekly run for 18 months. The fixture implements scalar configuration choices, not arbitrary feature coding and deployment. There was no live Impulse mutation, real customer experiment, provider billing integration, external messaging, or full multi-turn setup interview. These operational uncertainties remain open.
