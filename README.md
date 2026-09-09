# Long Horizon

A skill for agents that pursue responsibilities over days or months: improve a product from analytics, follow through on user feedback, evaluate revenue experiments, or monitor deployed changes. Agents choose useful objectives within the owner's standing brief, retain evidence from prior attempts, and use Impulse for future runs.

V1 runs on one machine. The distribution is a [skill bundle](skills/long-horizon/SKILL.md), editable workspace templates, and a small read-only file helper. There is no database or separate workflow server. The helper needs Python 3.11+ on a POSIX system; Linux is verified. The agent also needs an installed, configured Impulse CLI and the project's own tools/access.

## Install and start

Clone this repository and copy the whole `skills/long-horizon/` directory into your harness's skill directory. For a new installation using the skill directory on this machine:

```sh
git clone https://github.com/olliethedev/long-horizon-skill.git
cd long-horizon-skill
mkdir -p ~/.agents/skills
cp -R skills/long-horizon ~/.agents/skills/
```

Keep the scripts, references, and assets with SKILL.md. Review existing local modifications before updating an installed copy. Invoke `$long-horizon` with a responsibility, for example:

> Look after this product's onboarding. Investigate abandonment using our analytics and feedback, implement useful improvements within the permissions we agree, and check their effects after rollout.

The skill conducts a thorough setup interview one question at a time. It preserves prior answers and establishes the product/workspace, authority, evidence and access, coordination, optional limits and cost instructions, reporting, and continuation policy. A separate grill-me invocation is optional. The owner need not choose every future objective or supply a numeric KPI.

After agreement, adapt the [responsibility template](skills/long-horizon/assets/responsibility.md) and [Impulse definition](skills/long-horizon/assets/task.toml). Validate and preview the definition before registration. First-run timing is explicit. The example lets the agent schedule each next useful observation; other timing policies can be chosen at setup.

## How continuity works

Each fresh session reconstructs actual state from the brief, a concise current handoff, original actions, and decision evidence. The [history helper](skills/long-horizon/references/history.md) returns bounded source excerpts and paged reads, with source identities and explicit coverage limits. It searches ordinary files and writes nothing. An optional index is derived navigation, with no unique knowledge.

```sh
python3 skills/long-horizon/scripts/history.py search /path/to/product/history 'checkout offer' --limit 8
python3 skills/long-horizon/scripts/history.py read /path/to/product/history evidence/audit.json --bytes 6000
```

Agents follow aliases and action IDs through later corrections. [Evidence guidance](skills/long-horizon/references/evidence.md) separates request dates, deployment/exposure dates, observation windows, and retrieval time. Missing timestamps stay unknown. Source history informs decisions without transferring authority, and corrections preserve actual historical actions.

Consequential effects retain intent, stable request identity, and receipts. An uncertain response is reconciled before a repeat. Compatible development continues; material overlap changes the coordination or evaluation plan. Optional active-work limits include sleeping observation periods. Shared project budgets use the owner's usage source and accounting/reservation rules; Impulse is not a billing controller.

A planned observation waits with a confirmed schedule. An owner-resolvable blocker pauses, sends an actionable notice, and requires explicit owner resumption. A bounded responsibility can terminate when reached or impossible within its constraints. Completing one objective does not end an ongoing responsibility. History survives termination until explicit owner deletion. Routine reporting follows the agreed cadence; pause, termination, and owner decisions require immediate notices.

## Verification and limits

The [v1 implementation report](docs/v1-implementation.md) records current tests, independent review, and evaluation outcomes. [Evaluation commands](evals/README.md) separate ordinary checks from opt-in model sessions and the isolated real-clock Impulse exercise.

The preserved [55-session prototype study](prototypes/full-cycle/NOTES.md) found useful continuity and recovery in both skill and baseline arms, without demonstrating a skill advantage. It also exposed oversized retrieval, timestamp misinterpretation, and workspace-boundary violations. V1 addresses those mechanisms with a bounded helper, explicit evidence guidance, and more isolated evaluations. Historical records remain frozen; later findings are reported separately.

Selected simulated checkpoints do not establish reliable continuous work over months. A real product pilot still needs its own setup, access, authority, and outcome observation. The local Impulse exercise verifies scheduler behavior with real elapsed time and scripts; it is not a production customer experiment.

## Development

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m mypy
python3 -m unittest discover -s tests
```

CI runs typechecking and deterministic tests without model credentials or a live scheduler. See [CONTRIBUTING.md](CONTRIBUTING.md), the [v1 scope](docs/v1-spec.md), [domain terminology](CONTEXT.md), and [accepted decisions](docs/adr/). Research on [existing Impulse tasks](docs/research/pattern-transfer.md) and [Ponytail evaluation practices](docs/research/ponytail-evaluation-patterns.md) remains available alongside the [earlier project exploration](docs/design-session.md).
