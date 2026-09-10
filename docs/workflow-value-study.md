# Prepared-workflow evaluation method

The [results report](../evals/results/workflow-value/REPORT.md) records completed comparisons, partial cases, interruptions and usage. This method tests autonomous follow-through in a prepared environment. It does not fully evaluate the skill's conversational setup or integration discovery.

## Comparison

Each matched pair receives the same broad owner request, synthetic product facts, tools, owner answers and event timeline. Both start with empty agent-authored memory. The skill arm additionally receives the frozen Long Horizon bundle; the baseline receives normal factual tool documentation without the skill's process instructions.

The revenue request is: “Look after revenue from returning mobile visitors for the next six weeks. Try useful changes to our offer pages and follow through on what happens.” Both prompts identify the persistent workspace and tool documentation. The skill prompt adds only `Use $long-horizon at /workspace/skill/SKILL.md for this responsibility.` See the exact [prompt construction](../evals/workflow_runner.py) and [owner requests and answers](../evals/workflow_world.py).

The shared API advertises seven setup topics and returns prepared answers by topic, irrespective of question quality. Claude's revenue skill arm read the setup reference and asked tailored questions; its baseline looped through the advertised topics with generic questions and obtained the same answers. Both created their own durable records. This tests asking for and retaining supplied facts, but largely removes the challenge of discovering consequential questions. Scheduling, reporting, deployment and budget interfaces are already connected. Conclusions must not generalize this comparison to unstructured interviews or establishing those integrations in a real project.

The four scenarios cover revenue experiments, weekly product improvement, customer-feedback resolution and post-PR monitoring. Agents can inspect evidence, choose supported product settings, validate and deploy changes, coordinate with developer work, report findings and schedule fresh follow-ups. Product changes are small configuration surfaces, not arbitrary application development.

Each trajectory has an independent clock and a 42-day horizon, with at most eight sessions. A confirmed schedule or explicit owner instruction is required to wake the agent; the evaluator does not rescue missing schedules. Product events happen before owner instructions and scheduled work at the same timestamp. Only the agent's files and the independent service state carry forward.

The full design has 24 trajectories: four domains, three harnesses and two arms. Actual executed scope and any smaller owner-set usage cap belong in the results. Completing or stopping a responsibility can legitimately require fewer sessions. Never extend work past the owner's stop merely to reach an evaluation day or session count.

## Outcome review

The primary unit is the whole trajectory. Review useful fulfillment, actual effects, material constraint violations, evidence interpretation and unassisted continuity. The [rubric](../evals/workflow_rubric.json) covers setup, useful work, continuity, evidence, coordination, recovery, limits, lifecycle and reporting.

Preserve failed and interrupted attempts. A resource-censored trajectory is neither a completed success nor automatically a task failure. A correct next action does not excuse consequential false claims. Missing facts remain unknown. Finishing an individual feature need not end an ongoing responsibility.

Do not score directory layout, file count, verbosity or preferred interview wording. Compare native effort within a harness, keeping cache categories and missing telemetry explicit. Synthetic project credits and subscription model allowance are different resources. Native dollar estimates are not actual subscription charges.

## Controls and limits

Freeze the tested skill, service fixtures, rubric, evaluator sources and native settings before each declared comparison. Preserve earlier decisions when the scope or installed harness version changes. Calibrate deterministic controls and review examples before model trials. Never repeat generated decisions to obtain a better result.

Temporary homes isolate native authentication; the product workspace and service socket are scoped to one trajectory. Verify boundaries before launch and remove temporary credentials afterward. Network access remains available for model transport, so this is not a general network allowlist. Record credential-scan gaps and incomplete capture honestly.

A finite owner-answer API supplies vocabulary, developer overlap is scripted, and the initial cases are feasible. One synthetic scenario per domain cannot establish statistical superiority, arbitrary objective selection, impossibility handling, real revenue lift or reliable operation over months. Dense-history retrieval tests and real Impulse integration remain separate evidence.

Keep raw sources, traces and detailed reviews locally. Publish a concise account of the method, outcomes, relevant effort and limitations, without committing every generated artifact. The distributed skill contains none of the evaluation programs.
