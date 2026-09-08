# Long Horizon

Working name for agents that pursue outcomes over days or months, learning from earlier attempts. The reviewable [skill candidate](skills/long-horizon/SKILL.md) includes setup, durable-workspace guidance, and Impulse continuation instructions. Impulse owns scheduling. Durable history lives in readable local files, with any index rebuildable from those records. Small local helpers belong in the bundle only where prototype results justify them.

Version one targets one machine running Impulse, with multiple coordinated responsibilities. Cross-machine coordination is outside this version.

Examples include improving website content through experiments, implementing features and checking subsequent feedback, and investigating errors after deployment. A/B testing is one demanding example, not the project's whole scope.

The design covers ongoing responsibilities without a single fixed success metric. Agents choose objectives within their responsibility; ongoing work continues across individual improvements while useful work remains. Bounded assignments can terminate when reached or impossible, and owner-resolvable blockers pause until manual resumption. Strong recall of relevant actions across many months is a required prototype outcome.

Agents may revise their own plans and learnings within scope. Changes to the shared skill require evaluations and owner review before adoption.

History remains searchable after a responsibility terminates, so future responsibilities on the product can use it. Records and decision evidence are retained until the owner explicitly deletes them. Shared history is scoped to each product in v1; cross-product learning is deferred.

Owners may specify optional responsibility limits, including domain constraints such as testing at most five articles simultaneously. Project cost instructions and usage sources come from the user and may require custom setup. The working agent follows those instructions across runs; Impulse owns scheduling. Accounting and supporting helpers remain to be prototyped.

The skill will conduct a thorough setup interview before autonomous operation, exploring the task details and preserving the agreed brief. A separate `grill-me` invocation is optional; prior answers carry forward.

Setup also establishes a reporting cadence and destination. Routine runs preserve their work in the history; scheduled digests report progress, with immediate notices for pauses, termination, or decisions needing the owner.

This project contains research, interview notes, disposable state-model explorations, and fresh-session behavioral evaluations. The latest [complete-cycle evaluation](prototypes/full-cycle/README.md) compares actual configuration changes, observations, recovery, reporting, and continuation with and without the skill. Earlier [dense-history comparisons](prototypes/recall-comparison/NOTES.md) and [agent-maintained handoffs](prototypes/agent-handoffs/NOTES.md) remain preserved. The skill is a local review candidate; it has not been installed or used on a live product.

The latest evaluation completed 55 fresh sessions: 48 paired domain sessions, five focused setup/lifecycle probes, and two corrected-fixture rechecks. Both arms performed useful work and recovered saved history; the skill did not demonstrate a quality or efficiency advantage. Oversized retrieval, request-age interpretation errors, and instructed directory-boundary violations remain documented in the [findings](prototypes/full-cycle/NOTES.md). These are selected simulated checkpoints, not proof of continuous operation for 18 months.

- [Interview and open decisions](docs/design-session.md)
- [Task setup interview](docs/setup-interview.md)
- [Repository and evaluation layout proposal](docs/repository-layout.md)
- [Domain glossary](CONTEXT.md)
- [Readable files and rebuildable indexes](docs/adr/0013-use-readable-files-for-durable-history.md)
- [Existing Impulse patterns](docs/research/existing-impulse-patterns.md)
- [Patterns to transfer from indexing and reporting](docs/research/pattern-transfer.md)
- [External research](docs/research/long-running-agent-patterns.md)
- [Ponytail repository and evaluation research](docs/research/ponytail-evaluation-patterns.md)
- [Prototype](prototypes/continuity/README.md)
- [Lifecycle prototype across four domains](prototypes/lifecycle/README.md)
- [Candidate evaluation scenarios](docs/evaluation-plan.md)
- [Recall evaluation across many months](docs/recall-evaluation.md)
- [History-view prototype](prototypes/history-views/README.md)
- [Independent agent recall prototype](prototypes/agent-recall/README.md)
- [Dense recall comparison with a no-skill baseline](prototypes/recall-comparison/README.md)
- [Agent-maintained history across fresh sessions](prototypes/agent-handoffs/README.md)
- [Complete-cycle evaluation and commands](prototypes/full-cycle/README.md)
- [Full-cycle findings](prototypes/full-cycle/NOTES.md)

Created September 8, 2026. Existing scheduled tasks are sources of evidence for this exploration.
