# Existing Impulse patterns

Read-only inspection on September 8, 2026. These are facts about this installation and source checkout, followed by explicitly labeled design inferences. Runtime observations are snapshots, not permanent product properties.

Checkout revisions at inspection: Impulse `173691eba611c26d22fc7b8ea6b54a78e2e2ac46`; indexing `ec0264549db3f0cabafdcdc1d5212c776944fdb6`. Links reference the observed working-tree files, which may also contain uncommitted changes.

## What already exists

| Layer | Observed behavior | Primary source |
| --- | --- | --- |
| Impulse | Separates registered task, individual run, explicit agent outcome, and next run time. A reschedule persists independently of eventual outcome. | [Domain glossary](../../../impulse/CONTEXT.md) |
| Impulse | Supports calendar schedules, completion intervals, explicit next times, overlap policy, interruption handling, and command request IDs. Scheduling and outcome acknowledgments are durable after successful CLI calls. | [Installed skill](../../../../.agents/skills/impulse/SKILL.md), [CLI contract](../../../impulse/docs/cli-contract.md) |
| Indexing | Application-owned ledger, attempt budget, cooldown, and recovery marker survive runs. Ambiguous clicks still consume an attempt; successful recovery must supply structured verification. | [Coordinator](../../../biomogging-indexing/impulse-task.py), [Recovery instructions](../../../biomogging-indexing/recovery.md), [README](../../../biomogging-indexing/README.md) |
| Biomogging report | Stable action IDs carry evidence, confidence, effort, measure, and review window. Each new week must review prior actions and forecasts while distinguishing implementation from measured outcome. | [Assignment, output section](../../../biomogging-reports/AGENT_INSTRUCTIONS.md) |
| Both reports | Per-period evidence and publication receipts support continuation. An existing successful publication is verified; an uncertain publication attempt is reconciled before another publish. | [Biomogging assignment](../../../biomogging-reports/AGENT_INSTRUCTIONS.md), [HostPapa assignment](../../../hostpapa-reports/AGENT_INSTRUCTIONS.md) |
| HostPapa report | Reads the previous report to revisit open items, tracks coverage and source periods, and distinguishes last week's activity from current status. | [Assignment](../../../hostpapa-reports/AGENT_INSTRUCTIONS.md) |

`impulse task list --json` showed indexing disabled, and both weekly reports enabled, at inspection. Their actual schedules or state were not modified.

## Usage limits in the current foundation

Inspected September 8, 2026 at Impulse revision `173691eba611c26d22fc7b8ea6b54a78e2e2ac46`. Impulse has a global concurrent-agent limit, defaulting to 10, and documents no automatic execution cutoff. Its current settings, task, run, and agent types contain no model-token usage or monetary-spend fields. See [types](../../../impulse/src/types.ts), [capacity handling](../../../impulse/src/engine.ts), and [agent execution behavior](../../../impulse/README.md#from-scripts-and-agents).

This does not establish what an individual configured harness can report. It means a general per-responsibility cost meter or hard spending cap is not provided by the inspected Impulse model. The indexer's application-owned request-attempt budget is a different, countable resource. Any future limit should state its unit, source of usage evidence, and whether it is enforced by code or followed by the agent. The owner subsequently accepted [optional responsibility limits](../adr/0011-allow-optional-responsibility-limits.md), including a simultaneous-article cap. This inspection does not implement accounting or enforcement.

A monetary-cap example is “at most USD 50 per month on metered model API calls for this responsibility.” The amount is illustrative. Metered model calls can incur input/output-token charges; see [Anthropic's API pricing](https://platform.claude.com/docs/en/about-claude/pricing), checked September 8, 2026. A cap could bound the cost of repeated analysis and generation during an ongoing task. Its relevance depends on actual incremental charges, and enforcing it would require attributable usage plus control over spending actions; an estimated counter alone is not a guaranteed billing limit.

The user clarified that respecting these task-specific restrictions belongs to the working agent, with Impulse retaining scheduling responsibility. Two candidate information sources were checked against primary documentation on September 8, 2026:

- [ccusage](https://ccusage.com/guide/) reads local coding-agent usage and reports estimated costs; its [monthly-report documentation](https://ccusage.com/guide/monthly-reports) describes estimated usage-based cost and subscription comparisons. These figures must not be assumed to equal the provider's actual remaining daily, weekly, or monthly plan allowance. `command -v ccusage` did not find an executable in this shell's PATH; no package was installed or personal usage inspected.
- [Firecrawl's credit-usage endpoint](https://docs.firecrawl.dev/api-reference/endpoint/credit-usage) exposes remaining team credits, plan credits, and billing-period dates. This is provider account data. Attribution to a responsibility and its owner-approved budget still require task-level records, especially when multiple tasks share the account. No authenticated API call was made.

These are examples of possible information sources, not selected integrations or proof that an agent obeys every limit. The user subsequently clarified that cost restrictions and usage methods are supplied per project and may require custom setup; the skill must accommodate other methods and multiple sources. A future prototype should distinguish provider quota, shared project allowance, any task allocation, recorded consumption, and the freshness of each observation.

## Design inferences

1. **The useful reusable core is already distributed across these tasks.** It includes durable identity, evidence, attempts, conclusions, pending work, and next-run instructions. Indexing emphasizes operational continuity; reporting also begins an explicit learning loop.
2. **Run success and goal progress must remain separate.** A run can successfully gather evidence and schedule another observation without establishing that an experiment won or that the entire goal is complete.
3. **Impulse history is not the whole knowledge store.** Logs and outcomes explain execution; application records explain what was tried, why it mattered, and what changed. Impulse's retention policy explicitly differs from application data lifecycle.
4. **A skill can reuse Impulse without replacing it.** The question is how much application state and validation to standardize, not whether another scheduler is necessary.
5. **Publication and indexing uncertainty are relevant precedents for deployment uncertainty.** A missing acknowledgment does not establish that an external action failed. Durable intent plus external verification is a candidate pattern, not an exactly-once guarantee.

## Gaps requiring investigation

- These examples do not establish that an agent reliably retrieves a relevant failure from months of history.
- They do not establish that natural-language learnings remain evidence-backed after repeated summarization.
- They do not implement a general experiment-selection or stopping policy.
- A rule in assignment text is an instruction, not proof that every future agent obeys it.
- Observing errors after a deployment does not alone establish that the deployment caused them. Likewise, increased clicks do not establish increased purchases.

Local source links refer to neighboring projects on this machine. No private source datasets or credentials have been copied into this exploration.
