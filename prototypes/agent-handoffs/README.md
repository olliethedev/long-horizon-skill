# THROWAWAY — agent-maintained history across fresh sessions

Question: when agents choose what to save, can later fresh sessions recover actual actions, evidence, and corrections and use them to choose current work?

Run `python3 prototypes/agent-handoffs/prepare.py` to create four temporary trials. Each domain receives three dated observation packets sequentially. Only the static brief/instructions and the agent's own `memory/` files pass forward. The reviewer archives each session's inputs, memory, and outbox before replacing the current packet and clearing the outbox. Agents choose their own memory layout and may preserve source excerpts or files. Earlier evaluated skills stay frozen; this trial uses a separate candidate adding bounded retrieval, durable source preservation, retention, and reporting instructions.

Use a new independent agent for every session, supplying only the trial path and the explicit skill invocation. The reviewer criteria and future packets stay outside its instructed scope. No live services, scheduling, or messages are authorized. These are handoff and decision probes; agents do not execute interventions against a simulated service.

The packets span March 2025 to September 2026, but each chain has only three sessions and a small archive. This tests continuity through agent-maintained files, not reliable recall under months of accumulated volume. There is one chain per domain, no control arm, no enforced filesystem sandbox, and no independent full tool trace or cost telemetry. Disclosure of these limits is part of the result.

The [first findings](NOTES.md) and [preserved archive](https://github.com/olliethedev/long-horizon-skill/blob/be91b6929b4910042e71ddf704c0801b4d611d39/prototypes/agent-handoffs/results/first-handoffs/manifest.json) are available. Four chains completed twelve fresh sessions; final decisions used retained history appropriately in manual review. All eight handoff boundaries were verified without reviewer edits to memory. All final agents reported reading their entire small history, so larger selective-retrieval trials remain necessary.
