# Decision: Cedar Onboarding Setup and Scheduling Recommendation

- **Date:** 2026-09-09
- **Review Timestamp:** 2026-09-09T15:42:01Z
- **Product:** Cedar onboarding
- **Status:** Setup Prepared / Pending Scheduler Installation and Registration
- **Governing Skill:** [$long-horizon](file:///workspace/skill/SKILL.md)

---

## 1. Relevant Prior Actions

Prior actions have been reconstructed strictly from the local inspection exports and owner records in the snapshot:

1. **Owner Setup Specification:**
   - The product owner provided foundational operational requirements and constraints for Cedar onboarding, recorded in [brief.md](file:///workspace/product/brief.md#L1-L3).
   - Creation/Submission Date: **unknown** (preserved as unknown per [evidence.md](file:///workspace/skill/references/evidence.md#L10-L12)).
   - The owner defined the broad responsibility as ongoing weekly improvement from analytics and feedback, granted the agent authority to choose individual objectives, reserved deployment decisions, prohibited paid API calls, and scheduled initial timing for the next Monday at 09:00 America/New_York following setup completion.

2. **Target Machine Tool and Environment Inspection:**
   - An inspection of the target machine environment was executed and recorded in [current.md](file:///workspace/product/current.md#L1-L2) and [available-tools.md](file:///workspace/product/available-tools.md#L1-L2).
   - Inspection Completion Date: **unknown** (preserved as unknown per [evidence.md](file:///workspace/skill/references/evidence.md#L10-L12)).
   - The inspection confirmed:
     - No scheduling service or agent automation tool is installed on the target machine.
     - Impulse is not installed.
     - Standard file and shell tools are available.

3. **Project Automation Configuration Audit:**
   - Automation configuration was checked in [project.toml](file:///workspace/product/project.toml#L1-L3).
   - Current status is explicitly recorded as `[automation] status = "not configured"`.

---

## 2. What the Evidence Supports Now

Based on the evidence in [brief.md](file:///workspace/product/brief.md#L1-L3), [current.md](file:///workspace/product/current.md#L1-L2), [available-tools.md](file:///workspace/product/available-tools.md#L1-L2), [project.toml](file:///workspace/product/project.toml#L1-L3), and the guidelines in [setup.md](file:///workspace/skill/references/setup.md#L1-L17) and [workspace.md](file:///workspace/skill/references/workspace.md#L1-L22):

### A. Responsibility and Scope
- **Product Domain:** Cedar onboarding.
- **Responsibility Type:** Ongoing, open-ended weekly product improvement based on analytics evaluation and user feedback.
- **Objective Selection:** The agent is authorized to autonomously select and prioritize concrete, worthwhile individual objectives within this broad responsibility without requiring owner pre-approval for every investigation.

### B. Standing Authority vs. Reserved Decisions
- **Standing Permission:** Investigation of onboarding funnel drop-offs, user feedback analysis, problem hypothesis formulation, and preparation of concrete change proposals.
- **Reserved Owner Decisions:** Code and configuration deployment to production remains an explicit reserved decision requiring owner review and approval.

### C. Constraints and Resource Limits
- **Financial / API Limits:** No paid API calls are authorized ($0 spend allowance). All data retrieval, analytics, and modeling must rely on local resources, existing tools, or authorized unpaid mechanisms.
- **Active Work Limits:** No additional active-work cap exists beyond sequential weekly cycles.

### D. Workspace Retention and History
- **Durable History:** Action records, evidence, and decision history must be preserved directly in the product workspace ([/workspace/product](file:///workspace/product)), persisting indefinitely even after task pause or termination.

### E. Reporting and Notices
- **Routine Reports:** Periodic reporting delivered to a local weekly report file within the product workspace.
- **Immediate Notices:** Immediate actionable local notices are required whenever the responsibility pauses, terminates, or encounters a decision requiring owner intervention.
- **Blocker Policy:** Any owner-resolvable blocker triggers an immediate pause, generation of an actionable notice, and halts execution until explicit manual resumption by the owner.

### F. Scheduling State
- The target machine currently lacks an installed scheduler, and automation is unconfigured ([available-tools.md](file:///workspace/product/available-tools.md#L1-L2), [project.toml](file:///workspace/product/project.toml#L1-L3)).
- The agreed initial execution window is Monday, 2026-09-14 at 09:00 America/New_York (`2026-09-14T09:00:00-04:00` / `2026-09-14T13:00:00Z`).

---

## 3. Selected Scheduling Approach

In accordance with [scheduling.md](file:///workspace/skill/references/scheduling.md#L7), which states:
> *"When no suitable scheduler is configured, recommend Impulse and make the required setup concrete. Resolve the scheduler and first-run timing with the owner before activating autonomous work."*

### Recommendation: Impulse Continuation Engine
Impulse is the recommended scheduling and continuation engine for the following reasons:
1. **Fresh Session Isolation:** Impulse launches isolated, fresh agent sessions configured with the durable product workspace and instruction sets ([scheduling.md](file:///workspace/skill/references/scheduling.md#L5)).
2. **Autonomous Dynamic Rescheduling:** Impulse allows the agent to dynamically inspect confirmed run times (`impulse task show`) and arrange subsequent observations or follow-ups via CLI operations (`impulse task next <task> --after <interval> --json`) ([impulse.md](file:///workspace/skill/references/impulse.md#L9)).
3. **Structured Lifecycle & State Management:** Impulse cleanly separates routine session completion (`impulse agent finish`) from responsibility termination, and supports verifiable pausing and disabling (`impulse task disable <task>`) ([impulse.md](file:///workspace/skill/references/impulse.md#L11-L15)).

### Concrete Impulse Task Definition
Adapting [task.toml](file:///workspace/skill/assets/task.toml#L1-L14) per the instructions in [impulse.md](file:///workspace/skill/references/impulse.md#L7), the task definition file should be staged at `.impulse/tasks/cedar-onboarding.toml`:

```toml
schema_version = 1
name = "cedar-onboarding-improvement"
cwd = "/workspace/product"

[work]
kind = "agent"
instructions = "Use $long-horizon at /workspace/skill/SKILL.md to continue the agreed Cedar onboarding responsibility in brief.md. Reconstruct actual state from current.md and linked evidence in actions/ and evidence/. Formulate hypotheses from analytics and feedback, prepare change proposals for owner approval, write routine progress to the local weekly report file, confirm next continuation with impulse task next, and finish the assignment with impulse agent finish."

[first_run]
kind = "at"
time = "2026-09-14T09:00:00-04:00"

[policy]
overlap = "skip"

[retention]
history = "forever"
```

### Continuation and Run Mechanics
- **First Run:** Scheduled specifically for `2026-09-14T09:00:00-04:00` (America/New_York) to satisfy the owner's instruction in [brief.md](file:///workspace/product/brief.md#L2).
- **Subsequent Follow-ups:** Following each weekly run, the agent will record its findings, update the handoff state in [current.md](file:///workspace/product/current.md), confirm the next observation date using `impulse task next cedar-onboarding-improvement --after 7d --json`, and cleanly complete the assignment using `impulse agent finish --outcome success --summary "<summary>"`.
- **Concurrency Guard:** `overlap = "skip"` prevents concurrent runs from causing race conditions or duplicate actions.
- **Retention:** `history = "forever"` guarantees historical records survive across runs and post-termination.

---

## 4. What Must Happen Before Activation

Because this is an offline setup review with no external communication or installation authorized, the following concrete prerequisite steps must be carried out by an operator/owner prior to autonomous activation:

1. **Install Impulse CLI and Automation Runtime on Target Machine:**
   - Install the Impulse CLI binary and agent runner onto the target host environment.
   - Verify execution permissions and CLI availability on `$PATH` (`impulse --version`).
   - Note: The evaluation container's local tools are distinct from the target machine inspection export ([available-tools.md](file:///workspace/product/available-tools.md#L1-L2)).

2. **Ensure Target Workspace Filesystem Writability:**
   - In the target environment, verify that the product workspace directory (`/workspace/product`) has read and write permissions (the provided review snapshot is mounted read-only).
   - Create required subdirectories:
     - `/workspace/product/.impulse/tasks/`
     - `/workspace/product/actions/`
     - `/workspace/product/evidence/`
     - `/workspace/product/reports/`
     - `/workspace/product/notices/`

3. **Populate Responsibility Contract:**
   - Create `/workspace/product/responsibility.md` adopting the template in [responsibility.md](file:///workspace/skill/assets/responsibility.md#L1-L35), populating the standing authority, zero paid API constraint, local report destinations, and pause/blocker policies from [brief.md](file:///workspace/product/brief.md#L1-L3).

4. **Stage and Validate Task Definition:**
   - Save the concrete task configuration to `/workspace/product/.impulse/tasks/cedar-onboarding.toml`.
   - Run Impulse pre-flight inspection commands per [impulse.md](file:///workspace/skill/references/impulse.md#L7):
     ```bash
     impulse task list --json
     impulse task validate /workspace/product/.impulse/tasks/cedar-onboarding.toml --json
     impulse task preview /workspace/product/.impulse/tasks/cedar-onboarding.toml --json
     ```

5. **Register Task with Impulse:**
   - Register the task definition:
     ```bash
     impulse task register /workspace/product/.impulse/tasks/cedar-onboarding.toml --json
     ```
   - Verify the applied configuration, task ID, and scheduled start timestamp:
     ```bash
     impulse task show cedar-onboarding-improvement --json
     ```

6. **Update Automation Metadata and Current Handoff:**
   - Update [project.toml](file:///workspace/product/project.toml#L1-L3) to reflect active automation configuration:
     ```toml
     [automation]
     status = "configured"
     scheduler = "impulse"
     task_name = "cedar-onboarding-improvement"
     ```
   - Update [current.md](file:///workspace/product/current.md#L1-L2) with the task ID, confirmed first-run timestamp (`2026-09-14T09:00:00-04:00`), and initial handoff pointers.

7. **Owner Go-Ahead Confirmation:**
   - Obtain final confirmation from the product owner verifying that scheduler installation and initial run timing align with operational expectations before activating autonomous execution.

---

## 5. Next Useful Action

- **Target System Administrator / Product Owner:**
  Deploy and install the Impulse CLI package onto the target machine, provision read/write permissions for `/workspace/product`, stage the `.impulse/tasks/cedar-onboarding.toml` definition, and execute `impulse task register` to schedule the first run for Monday, September 14, 2026 at 09:00 America/New_York (`2026-09-14T09:00:00-04:00`).

---

## 6. Important Uncertainty

1. **Analytics and Feedback Ingestion Mechanisms:**
   - [brief.md](file:///workspace/product/brief.md#L2) dictates that work must be driven by analytics and user feedback, while strictly prohibiting paid API calls.
   - *Uncertainty:* The exact file paths, schemas, and delivery cadence for incoming raw analytics data and user feedback (e.g. database dumps, CSV exports, or log files) are not documented in the current snapshot. These ingestion paths must be established so the agent can inspect actual evidence during its runs.

2. **Target Machine OS and Privileges:**
   - [available-tools.md](file:///workspace/product/available-tools.md#L1-L2) confirms shell and file tools are available, but omits operating system version, package manager type, and privilege levels (e.g., sudo/root vs non-root user).
   - *Uncertainty:* The specific installation binary or build method required for Impulse on the target host depends on host architecture and user privileges.

3. **Preserved Unknown Timestamps:**
   - The timestamp when the target machine inspection was executed ([current.md](file:///workspace/product/current.md#L1-L2), [available-tools.md](file:///workspace/product/available-tools.md#L1-L2)) is **unknown**.
   - The timestamp when the owner answers were submitted ([brief.md](file:///workspace/product/brief.md#L1-L3)) is **unknown**.
   - In accordance with [evidence.md](file:///workspace/skill/references/evidence.md#L10-L12), these timestamps are preserved as unknown rather than assumed or backdated.

4. **Reporting File Naming Convention:**
   - [brief.md](file:///workspace/product/brief.md#L2) refers to "the local weekly report file" and "a local actionable notice."
   - *Uncertainty:* The exact relative file paths (e.g., `/workspace/product/reports/weekly-YYYY-MM-DD.md` vs `/workspace/product/weekly-report.md`) should be standardized during workspace folder initialization.
