# Long Horizon

A skill for agents that pursue responsibilities over days or months: improve a product from analytics, follow through on user feedback, evaluate revenue experiments, or monitor deployed changes. Agents choose useful objectives within the owner's standing brief, retain evidence from prior attempts, and arrange future runs with the project's scheduling tools.

V1 runs on one machine. The distribution contains [skill instructions](skills/long-horizon/SKILL.md), supporting references, and editable workspace templates. Agents use their harness and available system tools to find and read files. There is no bundled retrieval program, database, or separate workflow server. The agent needs the project's tools/access and a suitable scheduler; setup recommends Impulse when none is configured.

## Install and start

Clone this repository and copy the whole `skills/long-horizon/` directory into your harness's skill directory. For a new installation using the skill directory on this machine:

```sh
git clone https://github.com/olliethedev/long-horizon-skill.git
cd long-horizon-skill
mkdir -p ~/.agents/skills
cp -R skills/long-horizon ~/.agents/skills/
```

Keep the references and assets with SKILL.md. When updating, preserve any local modifications and replace the installed bundle with the new one; copying over an older installation can leave removed files such as the former history helper. Invoke `$long-horizon` with a responsibility, for example:

> Look after this product's onboarding. Investigate abandonment using our analytics and feedback, implement useful improvements within the permissions we agree, and check their effects after rollout.

The skill conducts a thorough setup interview one question at a time. It preserves prior answers and establishes the product/workspace, authority, evidence and access, coordination, optional limits and cost instructions, reporting, and continuation policy. A separate grill-me invocation is optional. The owner need not choose every future objective or supply a numeric KPI.

Setup [discovers available scheduling tools](skills/long-horizon/references/scheduling.md) and reuses the project's established scheduler when suitable. It must launch a fresh agent with the saved workspace and instructions, expose the next scheduled run, and allow rescheduling or disabling future runs. Tool help and documentation establish those capabilities.

After agreement, adapt the [responsibility template](skills/long-horizon/assets/responsibility.md). If Impulse is selected, the [example definition](skills/long-horizon/assets/task.toml) can be validated and previewed before registration. First-run timing is explicit. Other schedulers use their own interfaces, with continuation instructions saved in the workspace.

## How continuity works

Each fresh session reconstructs actual state from the brief, a concise current handoff, original actions, and decision evidence. [Retrieval guidance](skills/long-horizon/references/history.md) explains how to follow subjects, aliases, source IDs, and dated corrections using native file tools. Agents choose search scope and read sizes appropriate to the archive, account for truncated or incomplete results, and recheck evidence that changes during investigation. An optional index is derived navigation, with no unique knowledge.

Agents follow aliases and action IDs through later corrections. [Evidence guidance](skills/long-horizon/references/evidence.md) separates request dates, deployment/exposure dates, observation windows, and retrieval time. Missing timestamps stay unknown. Source history informs decisions without transferring authority, and corrections preserve actual historical actions.

Consequential effects retain intent, stable request identity, and receipts. An uncertain response is reconciled before a repeat. Compatible development continues; material overlap changes the coordination or evaluation plan. Optional active-work limits include sleeping observation periods. Shared project budgets use the owner's usage source and accounting/reservation rules; Impulse is not a billing controller.

A planned observation waits with a confirmed schedule. An owner-resolvable blocker pauses, sends an actionable notice, and requires explicit owner resumption. A bounded responsibility can terminate when reached or impossible within its constraints. Completing one objective does not end an ongoing responsibility. History survives termination until explicit owner deletion. Routine reporting follows the agreed cadence; pause, termination, and owner decisions require immediate notices.

## Verification and limits

The [native-tools revision](docs/native-tools-revision.md) records the current scope, and the [native harness report](evals/results/native-tools/REPORT.md) preserves the comparison, reasoning failures, usage, and focused verification. The [original v1 implementation report](docs/v1-implementation.md) records the previously published helper-based bundle. [Evaluation commands](evals/README.md) separate ordinary checks from opt-in model sessions and the isolated real-clock Impulse exercise.

The preserved [55-session prototype study](prototypes/full-cycle/NOTES.md) found useful continuity and recovery in both skill and baseline arms, without demonstrating a skill advantage. The [subsequent helper comparison](evals/results/v1-recall/REPORT.md) reduced captured retrieval output but showed no decision-quality improvement and used more total input tokens and time. The owner chose native tools for the revised skill; the published helper bundle remains a frozen evaluation arm. Historical records remain unchanged. The new comparison uses Codex, Claude Code, and Antigravity with more than 7,000 files per case. Its [report](evals/results/native-tools/REPORT.md) separates source retrieval from supported decisions and marks incomplete coverage explicitly; it does not demonstrate a consistent helper advantage.

Selected simulated checkpoints do not establish reliable continuous work over months. A real product pilot still needs its own setup, access, authority, and outcome observation. The local Impulse exercise verifies scheduler behavior with real elapsed time and scripts; it is not a production customer experiment.

## Development

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m mypy
python3 -m unittest discover -s tests
```

Python 3.11+ is needed for development and evaluations, not to install the skill. CI runs typechecking and deterministic tests without model credentials or a live scheduler. See [CONTRIBUTING.md](CONTRIBUTING.md), the [current revision scope](docs/native-tools-revision.md), [domain terminology](CONTEXT.md), and [accepted decisions](docs/adr/). Research on [existing Impulse tasks](docs/research/pattern-transfer.md) and [Ponytail evaluation practices](docs/research/ponytail-evaluation-patterns.md) remains available alongside the [earlier project exploration](docs/design-session.md).
