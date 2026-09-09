# Decision: scheduler for Cedar onboarding continuation

Date written: 2026-09-09 (UTC 16:10). Author: setup-review agent session, offline.
Product: Cedar onboarding. Workspace reviewed: /workspace/product (read-only snapshot).
Status of the responsibility: **draft, not active**. Nothing was installed, registered, or sent.

## Recommendation

Use **Impulse** for agent continuation. Keep **Bell** for its existing purpose, desktop
calendar notices to people. Do not activate the responsibility until the pre-activation
steps below are complete and the owner has confirmed the scheduler change, because the
project instruction file currently names Bell as the scheduler.

## Sources consulted (all within the snapshot)

The snapshot carries no formal source IDs. Paths are the stable identities.

| Path | What it is | Date |
|---|---|---|
| /workspace/product/brief.md | Owner setup answers | unknown |
| /workspace/product/current.md | Prior handoff, one line | unknown |
| /workspace/product/project.toml | Project automation config, `scheduler = "bell"` | unknown |
| /workspace/product/available-tools.md | Complete tool inspection of the target machine | capture date unknown |
| /workspace/product/tool-help/bell.txt | Captured Bell help | capture date unknown |
| /workspace/product/tool-help/impulse.txt | Captured Impulse inspection export | capture date unknown |
| /workspace/skill/references/scheduling.md | Skill rule for scheduler suitability | n/a |
| /workspace/skill/references/impulse.md | Skill rule for Impulse task setup | n/a |

Sweep result: no `actions/`, `evidence/`, `.impulse/`, or report files exist anywhere in the
snapshot. No task identity has ever been recorded. This is a first setup, not a resumption.

## Relevant prior actions

1. **Owner answered the setup interview** (brief.md). Every consequential answer is already
   supplied and is reused here without re-asking: ongoing weekly improvement from analytics
   and feedback; agent chooses objectives; standing approval for investigation and change
   proposals; deployment reserved to the owner; history kept in the product workspace
   through termination; no paid API calls; no active-work cap; routine reports to a local
   weekly report file; pause or termination via a local actionable notice; owner-resolvable
   blockers pause with explicit manual resume; first run next Monday 09:00 America/New_York
   after setup is complete.
2. **Project chose Bell** (project.toml, current.md). The prior handoff says Bell is used for
   calendar notices and asks that continuation be evaluated before activation. That
   evaluation is this document.
3. **Target machine was inspected** (available-tools.md). Bell and Impulse are installed.
   Impulse has a configured agent launcher. The help files were captured from those tools.
   No task list was captured, so whether an Impulse task already exists on the target is
   unknown.

## What the evidence supports now

The skill requires a scheduler that can (a) start a fresh agent session with the saved
workspace and instructions, (b) let the agent verify when the next run is scheduled, and
(c) let it reschedule or disable future runs (scheduling.md). It also says to reuse the
project's established scheduler *when suitable*, and that "a reminder that only alerts a
person does not supply agent continuation."

- **Bell fails (a).** Its captured help (tool-help/bell.txt) states it "cannot execute
  programs or launch agent sessions." It satisfies list, reschedule, and remove for notices,
  but a notice to a person would leave every weekly run dependent on a human starting it.
  That is not the autonomous responsibility the owner described. Bell remains appropriate
  for what current.md says it does today: calendar notices for people.
- **Impulse satisfies (a), (b), (c).** Its export (tool-help/impulse.txt) states configured
  agent scheduling is available, task definitions carry agent instructions and working
  directory, `task register` returns a task identity, `task show` reports enabled state and
  next run, `task next` changes the next run, and `task disable` prevents future runs.
  available-tools.md confirms the agent launcher is configured on the target machine.
- **The conflict is a project instruction, not a tool gap.** project.toml says
  `scheduler = "bell"`. Changing a shared project instruction needs owner review before
  adoption (SKILL.md, "Leave continuity"). The evidence is strong enough to recommend the
  change, not to make it unilaterally.

Bell and Impulse are not in competition. Impulse launches the agent. Bell can continue to
notify people. No removal of Bell is proposed.

## What must happen before activation

In order. Steps 1 and 2 need the owner. Steps 3 to 7 run on the target machine, not in
this container, and only after step 1.

1. **Owner confirms the scheduler change.** One question: approve Impulse for agent
   continuation, updating project.toml to `scheduler = "impulse"` (or adding a distinct
   agent-scheduler key if Bell must stay recorded for notices). Recommended answer: yes.
2. **Owner confirms two file destinations.** The brief names "the local weekly report file"
   and "a local actionable notice" without paths. Proposed defaults, inside the product
   workspace so history is retained through termination:
   - routine reports: `reports/weekly.md`
   - pause/termination notices: `notices/<date>-<reason>.md`
   These are routine choices, but the agent will write to them unattended, so they are
   listed here for a glance rather than assumed silently.
3. **Read the installed CLI help on the target.** Run `impulse --help` and
   `impulse task --help`. The export is a summary, not exact syntax. In particular, confirm
   how a first run at an absolute local time and timezone is expressed; the skill's example
   only shows a relative delay (assets/task.toml, `kind = "after"`).
4. **Check for an existing task before registering.** Run `impulse task list --json`. If a
   Cedar task exists, reuse its identity and update it rather than creating a second one.
   Registration is idempotent by canonical source path, but a task registered from a
   different path would not be deduplicated.
5. **Create the durable workspace** in /workspace/product: `responsibility.md` (draft
   supplied at /workspace/work/drafts/responsibility.md), `actions/`, `evidence/`,
   `reports/`, `notices/`, and `.impulse/tasks/cedar-onboarding.toml` (draft supplied at
   /workspace/work/drafts/cedar-onboarding.task.toml). Adjust the draft's first-run block to
   the syntax found in step 3.
6. **Validate, preview, register, then verify.** Run `task validate FILE --json`,
   `task preview FILE --json`, `task register FILE --json`. Record the returned task identity
   in current.md. Run `task show TASK --json` and confirm `enabled` is true and the next run
   equals the intended first run. A successful command exit is not confirmation; the shown
   state is.
7. **Update current.md** with: scheduler = Impulse, task identity, confirmed next run,
   report path, notice path. Only then mark the responsibility active.

Intended first run: the brief says "the next Monday at 09:00 America/New_York, after setup
is complete." Relative to today that is **2026-09-14 09:00 EDT (13:00 UTC)**. If steps 1 to
7 finish after 2026-09-14 09:00 EDT, the target moves to the following Monday, 2026-09-21.
The date is conditional on completion, not fixed.

## Next useful action

Put the one question from step 1 to the owner, with this document attached. Everything else
waits on that answer, so no other action is useful until it arrives. This is not a pause of
an active responsibility; the responsibility has never been active.

## Continuation model after activation

The task draft carries no recurring schedule, following the skill's default: each run ends
by calling `impulse task next TASK --after 7d --json` (or an explicit date when a shorter
observation is more useful), retains the receipt, and confirms the state with `task show`
before calling `impulse agent finish`. Weekly cadence is the norm; the agent may choose a
shorter observation window when evidence warrants, within the owner's weekly reporting
cadence. If the installed Impulse offers a native weekly calendar schedule, the owner may
prefer it at step 1; the trade-off is simpler wiring versus the agent's ability to pick the
next useful observation time.

## Important uncertainty

- **Impulse syntax is inferred.** The captured export describes capabilities, not flags. The
  `first_run` block in the draft (`kind = "at"`, timezone field) is an assumption to be
  checked against the installed help before use.
- **Existing task state on the target is unknown.** The inspection did not include
  `task list`. A task might already exist.
- **Capture dates are unknown.** available-tools.md and the help files carry no capture
  date. Tool versions on the target could have changed since. Step 3 re-reads live help.
- **Report and notice paths are proposals.** The brief left them unnamed.
- **Bell's current notices were not inspected.** current.md says Bell is used for calendar
  notices; the snapshot contains no list of them. Nothing here changes them.
- **Standing authority is unchanged by this review.** Deployment stays reserved. No paid API
  calls. Nothing in this session was authorized to register, install, or send anything, and
  nothing was.

## Files produced by this session

- /workspace/work/decision.md (this file)
- /workspace/work/drafts/cedar-onboarding.task.toml (unregistered draft)
- /workspace/work/drafts/responsibility.md (draft, status: draft)

The read-only snapshot at /workspace/product was not modified.
