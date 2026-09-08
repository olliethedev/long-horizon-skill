# Long Horizon

Long Horizon concerns agents carrying out broad responsibilities over time, choosing concrete objectives, and using earlier work to inform later decisions.

## Language

**Responsibility**:
The broad brief describing what the owner wants the agent to look after or improve. The agent can select concrete objectives within this brief.
_Avoid_: Run, individual improvement

**Objective**:
A concrete outcome the agent pursues within its responsibility, selected by the owner or by the agent. The agent may choose another objective as its understanding develops.
_Avoid_: Goal, run, scheduled task

**Authorization**:
The owner's standing permission to act within an agreed responsibility, scope, and limits. It continues across runs, so actions within those limits do not need repeated approval.
_Avoid_: Per-run approval, unrestricted permission

**Responsibility limit**:
An optional owner-defined bound on a responsibility's active work or resource use, such as how many articles may be under experiment simultaneously. It constrains the agent's choices within its authorization.
_Avoid_: Objective, agent concurrency alone

**Project cost instructions**:
The owner's project-specific rules for permitted resource spending and how relevant usage or remaining allowance is established. Responsibilities in the project follow the applicable shared rules and any allocations the owner supplies.
_Avoid_: Fixed provider integration, automatic budget per responsibility

**Workspace**:
The durable collection of objectives, attempts, evidence, learnings, and pending work, sufficient for a fresh agent to continue independently of a particular conversation or agent. V1 keeps this collection in readable local files. It remains available after termination until the owner explicitly deletes it.
_Avoid_: Conversation history, run log

**Shared learning**:
A finding that other responsibilities for the same product can consult, with its original supporting evidence and the conditions where it applies. V1 limits this sharing to that product and preserves attribution to the work that established the finding.
_Avoid_: Universal rule, unattributed summary

**Shared operating instructions**:
The reusable guidance governing how agents pursue responsibilities across sessions. A revision changes the common working method, rather than an individual responsibility's plan or evidence-backed learning.
_Avoid_: Task plan, shared learning

**Coordination**:
How responsibilities agree on overlapping work so compatible changes can proceed and interference with other work or its evaluation is addressed.
_Avoid_: Blanket development freeze, assuming every overlap is a conflict

**Pause**:
A suspension of the task's work while a resolvable prerequisite is missing, with its context and pending work preserved until the owner explicitly resumes it.
_Avoid_: Impossible objective, termination

**Wait**:
A planned interval before the task's next useful observation or action, with future continuation scheduled.
_Avoid_: Pause requiring owner intervention, termination

**Termination**:
Ending the task's future work when its brief is satisfied, impossible within its constraints, or has no useful work remaining within scope. Completing one objective in an ongoing responsibility does not by itself terminate the task.
_Avoid_: Sleeping until the next run, deleting history
