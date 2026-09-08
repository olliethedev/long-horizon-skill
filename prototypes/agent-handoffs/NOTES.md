# Agent-maintained handoffs: first exploration

Completed September 8, 2026. Four independent chains, three fresh agents per chain: **12 sessions total**. All four final decisions used retained history appropriately in manual review. This provides evidence for basic continuity through files chosen and written by agents; it does not establish reliable recall over large archives or demonstrate autonomous execution.

## What changed from the earlier probes

The earlier trials supplied a prepared historical archive. Here, each first agent received an empty memory directory and a dated observation packet. A second agent received the first agent's memory plus later evidence. A third received the second agent's memory and a new opportunity or problem. The reviewer replaced the packet and collected the outbox after each session; only `memory/` and static instructions passed forward. Agents chose their own filenames, layout, source retention, conclusions, and handoffs. No reviewer repairs or summaries were inserted between agents.

The packets span March 2025 to September 2026, compressed into three sessions. They are synthetic supplied observations, including reports of receipts; the agents did not perform those historical interventions or independently query their sources. The candidate skill was supplied explicitly to each fresh agent, using inherited harness defaults. Neither installed skill discovery nor full environment isolation was audited.

## Reviewed outcomes

| Domain | How history affected the final decision | Evidence |
| --- | --- | --- |
| Revenue A/B testing | Connected Quiet Offer to Spruce-47, replaced the incomplete-feed loss with the corrected +2% point estimate, retained the real rollback, and drafted a controlled evaluation without calling the correction a winner. | [Final decision](results/first-handoffs/cases/revenue/session-3/outbox/decision.md) |
| Weekly product improvement | Selected resumable setup as a still-unshipped opportunity, preserved the organization metric correction and current template choice, and kept solo retention unresolved. | [Final decision](results/first-handoffs/cases/weekly-product/session-3/outbox/decision.md) |
| User feedback | Recovered the partial export rollback and the later patch's 4k/10k verification boundary; proposed completeness and timing checks at 85k/92k before expanding streaming. It did not infer missing records from the new timeouts. | [Final decision](results/first-handoffs/cases/feedback/session-3/outbox/decision.md) |
| Bugs after PRs | Used the corrected historical quota cause to guide investigation, distinguished the unrelated 401 incident, and rejected reverting a PR absent from production without claiming the current cause was already proved. | [Final decision](results/first-handoffs/cases/post-pr-bugs/session-3/outbox/decision.md) |

All responsibilities remained ongoing. Reviewed decisions separated local analysis and saved plans from actual execution. These cases had no due digest or owner-decision trigger, so they do not validate immediate-notice delivery, pause/resume, termination, or report scheduling.

## Retention and size

| Domain | Memory after session 1 | After session 2 | After session 3 | Final files |
| --- | ---: | ---: | ---: | ---: |
| Revenue | 8,904 bytes | 19,576 bytes | 35,026 bytes | 9 |
| Weekly product | 10,020 bytes | 21,585 bytes | 33,766 bytes | 8 |
| Feedback | 9,517 bytes | 20,549 bytes | 32,579 bytes | 7 |
| Post-PR bugs | 8,254 bytes | 17,907 bytes | 26,819 bytes | 7 |

Each chain's three raw packets total approximately 1.9–2.3 KB. Saved memory also includes new interpretation, investigation plans, indexes, and current handoffs, so the size difference is not itself evidence of waste. It does identify memory growth as a useful dimension for longer trials. Final-session read reports enumerate all prior memory files in every case; these archives fit a full read and therefore do not test selective retrieval beyond context capacity. Some agents created indexes, while others continued through a handoff and source/action files. This run does not establish that an index or retrieval helper is necessary.

The final memories retain the complete original first-session source and action/review text, sometimes with appended correction links. All eight handoff boundaries match the preceding agent's saved memory byte for byte. Static inputs and observation packets remained unchanged, and all archived snapshot hashes were checked. First-session empty-memory snapshots were reconstructed from the generator's known initial state after three agents had started; source inputs were verified on collection. Later input snapshots were captured before the next agent started.

## What remains unproved

There is one chain per domain, no baseline arm, only three sessions per chain, no large competing archive, and no actions against a controlled service. Agents were told explicitly which files survive. Retaining copied evidence is useful but is easier than discovering and preserving evidence while doing the work. No index was removed or made stale in this run. Read/write reports are self-reports; full tool traces, token usage, cost, exact model identity, and enforced scope isolation are unavailable. The [manual rubric and calibration anchors](review-method.md) were written before reading outputs; review was unblinded and is not a validated model grader.

Next useful comparisons should combine these agent-maintained records with substantially longer sequences, competing relevant work and corrections, bounded retrieval, and missing/stale navigation. Test concise handoffs without losing source evidence. Separate full-cycle trials must exercise actual fixture actions, observation windows, interruption recovery, coordination, and lifecycle/reporting transitions.

## Reproducibility

The [archive manifest](results/first-handoffs/manifest.json) contains per-session input/memory/output hashes, agent identities, the invocation template, exact candidate skill and generator artifacts, and size statistics. Each archived `session-n` holds its input snapshot, resulting memory, and collected outbox; decision links resolve against that session's memory. Reviewer packets and criteria are outside each evaluated trial's permitted scope.

Run the project-local `prepare.py` to reproduce fixtures, then use `sessions.py` to collect and advance completed sessions and `archive.py` to verify and preserve a completed run. The archived generator is a provenance snapshot and retains its authoring-tree dependency on the earlier frozen skill; it is not a standalone installed package. No production skill or live Impulse task was modified.
