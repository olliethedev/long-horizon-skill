# Long Horizon

**Give an AI agent a responsibility that lasts beyond one conversation.**

Long Horizon is a Markdown skill for work that takes days or months: improving a product, testing content, following up on feedback or monitoring a release. It helps agents carry useful learning into fresh sessions and arrange their next action or observation.

The harness chooses how to do the work using the project's tools. The skill provides onboarding and continuity.

## Install

From your project directory, use the [Skills CLI](https://www.skills.sh/docs/cli):

```sh
npx skills add https://github.com/olliethedev/long-horizon-skill --skill long-horizon
```

Select your harness, such as Codex, Claude Code or Antigravity. Add `--global` to install across projects, then start a fresh session.

## Get started

Open your agent in the project and invoke the skill with a simple request. These examples use Codex's `$long-horizon` syntax; use your harness's skill picker where applicable.

```text
$long-horizon Grow useful organic traffic to this website. Work daily on new content and improvements to existing pages.
```

```text
$long-horizon Improve this product each week using analytics and customer feedback. Follow up after changes to see whether they helped.
```

The agent inspects the project and asks about missing details: outcomes, tools and access, permissions, timing, reporting, optional limits and where notes belong. It shows the proposed responsibility and asks for final confirmation before activating autonomous work.

## What carries between runs

Each responsibility has a home for its agreement, concise findings and pending context. Agents retain useful discoveries, failed approaches and reasoning that tools cannot readily reconstruct. Git, analytics and other source systems supply facts they already hold; routine exports and per-run logs are not required.

Before consequential changes, agents are instructed to discover overlapping work and coordinate through the project's workflow. They arrange useful follow-ups and can end a responsibility when it is achieved, impossible or has no useful work remaining.

## Scheduling with Impulse

A skill cannot start tomorrow's agent session by itself. [Impulse](https://github.com/olliethedev/impulse) is a separate CLI that schedules local agent assignments and lets agents arrange, reschedule or stop future runs. Install and configure it separately; the machine and harness must be available when work is due.

Setup reuses another suitable scheduler if you already have one, or recommends Impulse otherwise.

---

This workflow is experimental. Read the [skill](skills/long-horizon/SKILL.md), [evaluation results and limitations](evals/results/lean/REPORT.md), or [contributing guide](CONTRIBUTING.md).
