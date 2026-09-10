# Long Horizon

**Give an AI agent a responsibility that lasts beyond one conversation.**

Some useful work takes longer than an agent session. Publishing an article is immediate; learning whether it attracts the right readers takes time. Shipping a fix is one step; checking whether it solves the customer's problem is another. Each follow-up needs the context of what was tried, what happened, and what changed since then.

Long Horizon is an agent skill for that cycle: agree on a responsibility, act, retain useful knowledge, arrange a follow-up, and use the results to choose the next useful action. It works with fresh sessions in harnesses such as Codex, Claude Code and Antigravity. The agent can choose objectives within the scope and permissions you establish.

The installed bundle is three Markdown files: the skill, setup guidance and scheduler guidance. The harness chooses how to investigate, implement and verify work. Useful knowledge lives in ordinary project files; retrievable facts stay in their source systems. V1 operates on one machine.

## Install

Use the [Skills CLI](https://www.skills.sh/docs/cli) from your project directory. It runs through npm's `npx` command:

```sh
npx skills add https://github.com/olliethedev/long-horizon-skill --skill long-horizon
```

Select the harnesses you want to use. The default installation is scoped to the project. To make the skill available across your projects, add `--global`:

```sh
npx skills add https://github.com/olliethedev/long-horizon-skill --skill long-horizon --global
```

The CLI also supports explicit agent selection and installed-skill management; see its [options and supported agents](https://github.com/vercel-labs/skills#options). Load a fresh harness session after installation. For a manual installation, copy the entire [`skills/long-horizon/`](skills/long-horizon/) directory into your harness's documented skill location, keeping its references together.

## Start with a responsibility

Open your agent inside the product repository. In Codex, invoke `$long-horizon`; in harnesses with slash-command skills, select `/long-horizon` from the skill picker. Give it an outcome and any constraints you already know:

```text
$long-horizon Grow qualified organic traffic to our developer documentation site, with daily actions.
```

The skill conducts its own setup conversation, one consequential question at a time. It inspects the project and reuses existing instructions and answers. Together you establish:

- The responsibility, audience, success measures and conditions for ending it.
- What the agent may change, publish, deploy or communicate without asking again.
- Which installed tools, skills and existing workflows can do the work, with essential access verified and the proposed toolset reviewed with you.
- How to coordinate with developers and other active responsibilities.
- Optional limits for autonomous runs, paid-service budgets and authoritative usage sources you supply.
- When to work and report, where requests for your help reach you, and how you reply and resume affected work.
- Where useful notes belong and how they are retained or committed.

You can start with a broad request. A separate interview skill, numerical target or monetary budget is optional. Setup investigation can proceed before settling limits for autonomous runs. Essential gaps must be resolved, with any adequate fallbacks explicitly agreed.

The agent prepares and validates the files, then shows the responsibility, first assignment and operating settings together. It asks **“Activate this responsibility with these settings?”** before enabling autonomous runs and verifies the resulting schedule. Standing permission then carries across ordinary follow-ups; an existing responsibility does not need onboarding again after a skill update.

## Why a scheduler is needed—and where Impulse fits

A skill file cannot start a new agent tomorrow. After the current session ends, something must launch the next session with the right project and instructions.

| Piece | Responsibility |
| --- | --- |
| Your agent harness | Reads files, reasons, edits code and uses your connected tools. |
| Long Horizon | Establishes the responsibility, preserves useful knowledge and guides continuation across runs. |
| A scheduler | Starts future sessions and lets the agent confirm, move or disable its next run. |

[Impulse](https://github.com/olliethedev/impulse) provides durable local scheduling for scripts and agent assignments. It can launch your configured harness, retain task/run identities, expose execution logs and let a running agent schedule its next observation or disable future work. Long Horizon includes [scheduler guidance](skills/long-horizon/references/scheduling.md); the agent uses the installed scheduler's tools and documentation.

To use it, follow [Impulse's installation and setup guide](https://github.com/olliethedev/impulse#build-and-install), configure your harness and terminal, and check the installation with `impulse doctor`. The machine, logged-in environment and configured harness must be available for scheduled execution. Installing Long Horizon alone does not install or configure Impulse.

During setup, the agent [discovers the project's scheduling tools](skills/long-horizon/references/scheduling.md). It reuses an existing suitable scheduler and recommends Impulse when none is configured. An alternative must launch fresh agent sessions with saved context, expose the next run, and support rescheduling and disabling work. Project-specific API budgets remain part of the agent's brief and accounting setup.

## Example responsibilities

Adapt these prompts to your product and available tools. Each begins a setup conversation; the agent resolves missing access, authority and operating details before setting up autonomous work.

### Improve content over time

```text
$long-horizon Grow qualified organic traffic to our API documentation and tutorials. Work daily on useful new articles and improvements to existing pages. Use our search and website analytics, coordinate with documentation changes, and send a weekly digest of actions and evidence. Open PRs for content changes; I will review and publish them.
```

Daily work can include research, writing and technical fixes. Traffic outcomes may need weeks of observation; the agent should choose measurement windows appropriate to the evidence.

### Run revenue experiments

```text
$long-horizon Improve net revenue from our subscription landing pages over the next six weeks. Run at most five page experiments at once, preserve checkout reliability, and account for refunds and cancellations. Ask me which analytics and experiment tools to use and what rollout authority you have. Retain failed and inconclusive attempts as well as wins.
```

### Improve a product from weekly analytics

```text
$long-horizon Take responsibility for reducing friction in our team's project-management app. Each week, review onboarding analytics and customer feedback, choose a useful improvement, implement it within our agreed permissions, and check its effect after rollout. Keep learning across iterations and send a fortnightly progress report.
```

### Follow customer feedback through to resolution

```text
$long-horizon Resolve the recurring incomplete-export complaints from our enterprise customers. Investigate their actual data sizes and failure conditions, implement and verify a fix, then follow up on deployed behavior and customer outcomes. End the assignment when the affected cases are resolved, and preserve the investigation for future regressions.
```

### Monitor a release for bugs

```text
$long-horizon Monitor our new billing release after it reaches production. Review errors and customer reports daily, investigate regressions, and open fixes as PRs. Coordinate with other deployments so we attribute problems to the right change. Finish after fourteen days of verified healthy production behavior, with a final report of fixes and remaining uncertainties.
```

## What carries between runs

The core rule is **persist knowledge that tools cannot readily reconstruct**. Keep the agreed responsibility and concise, searchable findings. Use Git, analytics, the CMS and scheduler for information they already retain.

| Information | Usual source |
| --- | --- |
| Code changes and their dates | Git history and relevant commit references |
| Historical traffic or revenue measurements | Analytics queries with the relevant periods and filters |
| What an experiment taught us, why it failed, or where its result applies | A concise learning note |
| A CMS change without revision history, or an experiment awaiting an outcome | Enough saved context to continue or evaluate it |

For example, a useful note might explain that a more practical article voice improved engagement among experienced developers over a particular observation window, while its effect on purchases remains unclear. It can point to the article, change and analytics query without copying the entire export. Later evidence can correct the finding. A pending experiment can become the eventual learning in the same note.

Each responsibility has an identifiable home for its agreement and notes; the agent chooses the layout and any task-specific recovery material. It references shared knowledge and discovers overlapping work before consequential changes, coordinating conflicting writes and reassessing affected observations. The skill does not require per-run narratives, raw exports, tool transcripts, receipt files, backup archives or record templates. A run with no new knowledge or pending context need not create an artifact. Useful learnings remain available after the responsibility ends.

The agent arranges and verifies the next useful follow-up. When owner input is needed, dependent work waits while independent useful work can continue. A fully paused responsibility requires explicit owner resumption. A bounded responsibility ends when achieved, impossible within its constraints, or no longer able to make useful progress; completing one objective can leave ongoing work active.

## Evidence and current limits

This is an experimental workflow. The [earlier full-cycle prototype](prototypes/full-cycle/NOTES.md) and [native-tools comparison](evals/results/native-tools/REPORT.md) exercised continuity, recovery and retrieval, but have **not demonstrated an overall advantage over a capable agent without the skill**. That is an open evaluation question, not a promised benefit.

The [prepared-workflow evaluation](evals/results/workflow-value/REPORT.md) compares fresh sessions with retained files and confirmed simulated follow-ups. Completed revenue pairs across all three harnesses show no outcome advantage, with higher native effort in the skill arms. Both arms received a setup-topic checklist, detailed owner answers and connected scheduling, deployment and reporting tools. This leaves the value of an adaptive setup conversation and real project integration unresolved. The report records executed coverage, interruptions and effort. Simulated weeks and dense history archives do not establish reliable real-world operation over months or actual revenue lift.

The current revision removes mandatory record templates and routine evidence retention. A [small Codex comparison](evals/results/lean/REPORT.md) used one short request and five fresh sessions per arm, including onboarding. The skill arm retained three project files versus 149 and used less measured follow-up effort; both reached the same final content choices. Both stopped at the final checkpoint, leaving ongoing continuation unresolved. Runner defects and differences in elicited owner answers limit the comparison. Subsequent wording and coordination refinements have local review only, with no further model evaluation. Earlier studies describe their original skill versions.

## Development

The distributed skill contains no evaluation programs. Python 3.11+ is needed only for repository development and evaluations:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m mypy
python3 -m unittest discover -s tests
```

CI runs deterministic tests and type checking without model credentials or a live scheduler. See [CONTRIBUTING.md](CONTRIBUTING.md), [evaluation commands](evals/README.md), [domain terminology](CONTEXT.md) and [design decisions](docs/adr/) for deeper implementation and research context.
