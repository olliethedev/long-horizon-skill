# Setup interview

Design guidance for the accepted [built-in setup interview](adr/0012-build-thorough-setup-into-the-skill.md). This is not an installed skill or a completed behavioral evaluation.

## Purpose and depth

Establish a shared understanding sufficient for autonomous work across fresh sessions. The owner wants thorough grilling of the task details, not merely collecting a title and schedule. Explore meaningful ambiguities, failure scenarios, and trade-offs one question at a time, with a recommendation when a choice is needed.

Read the supplied request, existing project instructions, relevant workspaces, and available evidence first. Resolve facts through authorized inspection; ask the owner for missing decisions. Preserve prior answers, including decisions from a separate `grill-me` conversation. Thoroughness is coverage of the responsibility's actual details, not a fixed questionnaire or repetition of information already supplied.

## Details to establish

| Area | What the durable brief needs to establish |
| --- | --- |
| Responsibility | What the owner wants improved or monitored, the relevant product and subjects, and whether the brief is ongoing or bounded. The agent may select objectives within that scope. |
| Evidence and useful progress | Relevant signals, data access, how changes and their effects can be verified, and how the agent should judge worthwhile progress. Match the method to the task; qualitative feedback and quiet monitoring can be valid evidence. |
| Authority | Which actions the agent may take autonomously, including applicable implementation, deployment, rollback, or communication permissions, and decisions reserved for the owner. |
| Optional limits | Applicable bounds such as five articles under active tests, any project budget or task allocation, and how the agent should act as the bound becomes relevant. Limits remain optional. |
| Project cost instructions | If cost restrictions apply, obtain the user's project-specific instructions for measuring and respecting them. Resolve units, relevant allowance periods, source access, and the scope shared with other responsibilities when needed to interpret those instructions. |
| Coordination | Related work for the same product, how actual changes are discovered, and what interactions require coordination. Compatible work can proceed. Establish the product boundary for shared history; cross-product learning is outside v1. |
| Continuation and interruption | An initial observation cadence or trigger, the evidence needed before another action, and applicable wait, pause, explicit owner-resume, and termination behavior. |
| Owner reporting | Agree the routine report cadence, destination, and authority to use it. Send immediate notices when the task pauses, terminates, or needs an owner decision; other runs update the saved history. A weekly digest is an example, not a required cadence. See [ADR 0014](adr/0014-agree-reporting-at-setup.md). |
| Continuity | Where the agreed brief, actions, observations, corrections, pending work, and related history will be kept so a fresh agent can continue. History remains searchable after termination until the owner explicitly deletes it. |

These are areas to cover through inspection and discussion, not a fixed questionnaire to present together or a mandatory numerical policy for every task. Use concrete scenarios to find consequential gaps. Where a future choice properly belongs to the agent, record that discretion instead of asking the owner to preselect every experiment or feature.

## Project-specific costs

The user supplies the project's cost restrictions and the ways to obtain relevant usage information. A project may use a custom script, one or several tools, service reports, existing instructions, or another method. `ccusage` and Firecrawl MCP are examples raised during design; the skill does not require either, invent a standard replacement, or assume that those examples cover other projects.

When a budget covers the project, responsibilities using it must respect that shared scope. Starting another responsibility or waking a fresh session does not create another copy of the allowance. Task-specific allocations may be used when the owner supplies them. A cost estimate, a subscription allowance, and service credits remain distinct quantities unless the supplied accounting method establishes a valid relationship.

The working agent interprets and follows these instructions. Impulse handles scheduling. Any local helper must be justified by prototype evidence; a universal cost-provider interface or central billing system has not been selected.

## Completing setup

Keep the emerging brief current as answers arrive. Before autonomous operation, make the responsibility, authorization, evidence approach, applicable project instructions, unresolved prerequisites, and initial continuation plan concrete and reviewable. Conclude the interview when the owner and agent have established shared understanding and the necessary authorization; carry that authorization into scheduling and later runs.

Treat known consequential gaps explicitly instead of silently inventing defaults. New facts can still require a later owner decision. Preserve the accepted distinction between ordinary scheduled waits and a task paused until explicit owner resumption.

## Proposed behavioral probes

Use complete and incomplete briefs across the four required domains. Inspect the actual questions, saved brief, and any attempted task registration. Include a prior interview, a custom cost source unrelated to the named examples, multiple responsibilities sharing a project budget, and a task with no requested budget. Check that reporting setup obtains or reuses the cadence and authorized destination rather than inventing a channel or forcing weekly reports.

Check that the agent uncovers important missing details before autonomous work, asks one question at a time, preserves supplied decisions, and leaves agent-selected objectives flexible within the brief. These probes have not run; the earlier four recall probes began with established responsibilities and did not test setup.
