# Long-running agents: memory, recovery, and evaluation

Research date: 2026-09-08. Status: design input, not an architecture decision.

Question: What should a reusable skill contribute above a scheduler such as Impulse so that fresh agent runs can pursue an objective, wait for real-world evidence, and improve their decisions over weeks or months?

The evidence supports treating continuity of knowledge and recovery of execution as separate problems. A skill can define the working method and carry scripts; a workflow runtime can preserve execution state. Neither automatically makes the agent's conclusions true. The most useful next comparison is a skill with a durable workspace against the same skill with a few enforced state operations. This is a proposed experiment, not a conclusion that a new runtime is necessary.

Local Impulse behavior and existing indexing/report tasks are being investigated separately. This report makes no claims about their guarantees.

## What the primary sources establish

### 1. A skill may already contain deterministic code

**Fact.** The Agent Skills specification requires `SKILL.md` and explicitly permits executable `scripts/`, reference documents, assets, and additional directories. Instructions and resources are loaded progressively. Its reference validator checks frontmatter and naming conventions; this is different from measuring agent behavior. [Agent Skills specification](https://agentskills.io/specification)

**Implication.** Choosing a skill as the distribution format does not require putting locking, record validation, or fixture setup into prose. Those can be bundled helpers. This remains compatible with the user's preference for a skill with evals.

### 2. Fresh sessions need explicit handoff artifacts

**Fact.** Anthropic's long-running coding harness used an initializer, a structured feature list, progress notes, Git history, and incremental work in subsequent sessions. Compaction alone did not prevent undocumented partial work or premature completion. The authors explicitly limit the demonstrated system to full-stack application development and describe broader generalization as future work. [Effective harnesses for long-running agents, November 2025](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

**Implication.** This is evidence for explicit recovery context, not evidence that the same instructions will autonomously optimize a business over months. A new run should establish current state before selecting more work; previous output is something to verify.

### 3. Compaction and persistent knowledge serve different purposes

**Fact.** Anthropic distinguishes conversation compaction from structured notes stored outside the context window. It warns that aggressive summarization can discard details whose relevance appears later. It also describes retrieving data through lightweight references instead of loading every raw result into the prompt. [Effective context engineering for AI agents, September 2025](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

**Design inference.** Keep a short current brief, source evidence, and a history of decisions separately. A brief should point to evidence; it should not become the only surviving evidence. For an old losing page variant, preserve what was tested, when, against what baseline, and why its result may or may not transfer to today's page.

### 4. Session state and cross-session memory are distinct primitives

**Fact.** LangGraph differentiates checkpointers, which persist a thread's graph state, from stores, which persist application-defined data across threads. Its in-memory checkpoint implementations lose state on process restart. [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

**Design inference.** A long-lived effort should have an identity independent of an agent conversation or scheduler invocation. Resuming a conversation is an optional convenience; reconstructing the effort from durable records is the actual continuity requirement. Stored knowledge is supplied to later inference; none of these mechanisms implies model weight training.

### 5. Durable execution has explicit checkpoint boundaries

**Fact.** LangGraph checkpoints graph state at super-step boundaries and can preserve successful sibling writes when another node fails. Its durability modes trade performance against crash recovery: `exit` does not save intermediate state, `async` can lose an in-flight checkpoint, and `sync` writes checkpoints before continuing. [LangGraph checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers)

**Implication.** “Uses persistence” is insufficient as a reliability claim. The design must say which operations are durable and what will be replayed after interruption. A persisted note and a persisted execution checkpoint are useful for different reasons.

### 6. A runtime cannot erase an ambiguous external effect

**Fact.** Temporal documents the case where an Activity completes an external operation, then its worker crashes before reporting completion. The Activity may execute again. Completed Activities are not re-executed during ordinary replay, but safe retries require idempotency; request keys are enforced by the service being called. [Temporal Activity Definition: idempotency](https://docs.temporal.io/activity-definition#idempotency)

**Design inference.** A page deployment whose acknowledgement was lost needs an “outcome unknown” state. The next run should inspect the deployment using its identity or retry with an externally supported idempotency key. A local success flag, lock, or workflow engine alone cannot prove the remote action occurred exactly once. Where reconciliation cannot determine the outcome, keep it unresolved instead of inventing success or failure.

### 7. Fast-forwarded time is practical, with a limited claim

**Fact.** Temporal's Python SDK exposes workflow timers, cancellation, and workers. Its test environment supports automatically advancing to scheduled events or manually advancing time; it also supports mocked Activities. The README explicitly describes the current source branch rather than necessarily the released package. [Temporal Python SDK: workflows and testing](https://github.com/temporalio/sdk-python/blob/main/README.md#testing)

**Design inference.** A local evaluator can advance a fixture clock by seven days and provide the next observation immediately. This tests temporal decisions and recovery without waiting seven days. It does not simulate genuine user behavior, prove causal attribution, or validate production scheduler uptime.

### 8. Evaluate environmental outcomes and repeated trials

**Fact.** Anthropic's evaluation guidance distinguishes a trace from the resulting state of the environment. It recommends matching graders to the question, isolating trials, and measuring variability across multiple runs. Code, model, and human graders have different strengths; model graders need calibration. Reliability across repeated successes differs from obtaining one success across several attempts. [Demystifying evals for AI agents, January 2026](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

**Implication.** A final message saying “the winner is live” is not sufficient. The evaluator should inspect the fixture's deployed variant, saved evidence, pending work, and stop state. Report complete-chain success as well as individual checkpoint success: a system can look good at each step and still fail during a long sequence.

### 9. Skill evaluation has an existing baseline pattern

**Fact.** Anthropic's public skill-creator source stores realistic prompts and fixture files in `evals/evals.json`, compares runs with and without a skill or against an earlier skill version, and records assertion results, timing, and token usage. Its description-trigger evaluation is a separate loop from task-output evaluation. [Anthropic skill-creator source](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)

**Implication.** Reuse the with-skill/baseline comparison idea, while adding a fresh-session sequence runner for this problem. A skill that triggers correctly may still lose history, act twice, or reach an unsupported conclusion. The source is a Claude-oriented implementation, not a portable standard guaranteeing identical behavior in every host.

## Candidate comparison

This table is an architectural interpretation of the sources above, not measured benchmark results.

| Candidate | What it contributes | Unresolved responsibility | Evidence that would justify it |
| --- | --- | --- | --- |
| Skill plus workspace files | Portable procedure, readable evidence and decisions, low setup cost | Agent adherence, concurrent writes, partial records, recovery order | Fresh runs consistently recover and act correctly in bounded single-writer fixtures |
| Skill plus small helpers | Same method, with validated records, atomic local updates, stable operation identities, and ownership checks | Remote effects still need reconciliation; helper semantics must be maintained | Prose-only failures cluster around mechanical state operations and helpers eliminate them |
| Skill on a durable workflow runtime | Checkpointed execution and explicit recovery boundaries; richer timer/retry/signal orchestration | Application memory, sound judgments, effect idempotency, runtime operation | Requirements demand many coordinated branches, distributed workers, or recovery behavior that exceeds a small helper |

The duration alone does not choose the architecture. A monthly read-and-report effort may need less execution machinery than a ten-minute task with several irreversible external effects. The number of interacting operations and recovery requirements is a more useful discriminator.

## Three recommendations to test

1. **Give each effort a reconstructable working record.** Candidate records: objective and evaluation policy; current state and next observation due; evidence references; attempts and outcomes; provisional conclusions with applicability conditions; pending operations. Give observations timestamps and subject versions. Keep “no evidence yet,” “evidence inconclusive,” and “negative outcome” distinguishable. This structure is a proposed local model, not a schema mandated by any source.

2. **Put judgment in the skill and measure which mechanics need enforcement.** Compare identical tasks using files alone and files plus narrowly scoped operations such as claim work, record an observation, and finish a run. Include crash boundaries and duplicate wakeups. Add a helper only when it enforces a requirement we can name; adopt a broader runtime when requirements exceed those operations. This experiment preserves a skill-first packaging choice without committing to a prose-only implementation.

3. **Make time and context loss explicit evaluation inputs.** An evaluator should own the simulated clock, event stream, remote fixture state, and independent expected outcomes. Each wakeup starts a fresh session with the effort path and wakeup reason. Only persisted artifacts cross that boundary. Keep multiple held-out narratives so the skill cannot pass merely by reproducing one demonstration. Treat model, host, tools, and skill version as part of the evaluated configuration.

## Prototype and evaluation scenarios

These are proposed scenarios, not completed experiments. They should initially use an in-memory simulator with visible state, then durable scratch fixtures when specifically testing process loss. A logic prototype can establish whether states make sense; agent evals must establish whether models actually use them correctly.

| Scenario | Fixture event sequence | Observable success |
| --- | --- | --- |
| Fresh-session recovery | Day 0 creates variants; day 7 provides observations; day 35 asks for the next attempt with no conversation history | Agent identifies previous versions, retrieves their evidence, and explains how history affects the next choice |
| Early or delayed evidence | Wake before the observation window; later receive partial results or no new data | No fabricated outcome; an explicit reason and appropriate next observation time remain recorded |
| Lost acknowledgement | Deployment takes effect; runner is killed before local success is recorded | Next run reconciles the same operation identity and does not create an extra deployment |
| Duplicate wakeup | Two invocations see the same pending step | One action is committed, or a conflict is explicitly surfaced; no silent overwrite of history |
| Changed conditions | Earlier evidence favors a variant; later observations use a different audience or page version | Earlier conclusion remains traceable, and its applicability is reconsidered instead of silently reused |
| Misleading summary | Brief says “B won”; referenced evidence marks the experiment inconclusive | Agent corrects the brief and refrains from treating it as established evidence |
| Repeated losing idea | Months of attempts contain the proposed variant under a different label | Agent detects substantive similarity or states what material change justifies retesting |
| Stop and restart | Fixture policy says gains are below the useful threshold; later a relevant condition changes | Agent stops as specified, retains the reason, and resumes only under the policy's reopening condition |
| Cross-domain transfer | Same mechanics applied to a feedback-led feature release or error monitoring | Agent uses domain evidence and actions without inventing page-variant concepts or forcing every effort into an experiment |

Start with the fresh-session, lost-acknowledgement, and changed-conditions cases: together they distinguish remembering history, recovering execution, and revising beliefs. Record actual side-effect count and durable state using deterministic checks; use reviewed rubrics for whether a conclusion is supported. Compare baseline, skill-only, and helper-assisted configurations over repeated independent trials. Keep fixture setup and grading outside agent-editable files.

## Limits and decisions still needed

This research does not establish a general-purpose system that autonomously improves arbitrary outcomes forever. The cited harness demonstrations cover bounded work; product documentation specifies mechanisms rather than business effectiveness. No primary source here demonstrates months of safe, adaptive A/B optimization.

“Marginal improvement” requires a domain policy. An A/B-testing application needs its own measurement design, decision method, observation requirements, and treatment of changing audiences. A generic skill should carry that policy and evidence, not invent statistical certainty. Stopping under a configured policy also does not prove that a global optimum has been reached.

The interview should settle the initial effort's observable outcome, the intended authority for real actions, whether efforts can overlap on the same resource, and what should reopen a stopped effort. Those answers determine which prototype failures matter enough to enforce mechanically.
