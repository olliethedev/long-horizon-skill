# Repository layout

The installable skill has one maintained source in `skills/long-horizon/`. It contains instructions, references and templates; runtime retrieval uses the harness's existing file tools.

| Path | Purpose |
| --- | --- |
| `skills/long-horizon/` | Distributed skill bundle |
| `evals/` | Reusable fixtures, native harness adapters, runners and scoring rubrics |
| `evals/results/<study>/REPORT.md` | Concise reviewed results |
| `evals/runs/` | Ignored workspaces, raw traces, snapshots and local analysis |
| `tests/` | Deterministic checks; no model usage in CI |
| `docs/` | Design decisions, research and evaluation methods |
| `prototypes/` | Historical exploration code and findings; generated results are ignored |

Do not commit generated histories, copied source trees, binary trace archives, long per-session review dumps or one-off campaign scripts. Keep full evidence locally so results can be checked without making the skill repository an archive of every run. Historical evidence links can point to the commit that originally recorded them.

The structure follows useful patterns from [Ponytail](research/ponytail-evaluation-patterns.md): separate runtime instructions, ordinary checks and model evaluations; keep routine generated runs out of Git. This project uses Python's standard library for its stateful evaluation services and native harness sessions.

A behavioral comparison should preserve matched facts and permissions, identify the tested skill and harness, and inspect actual effects and retained claims. Evaluate useful outcomes and constraints before comparing cost or speed. Report incomplete cases and uncertainty explicitly. Static checks and correct file formatting cannot establish autonomous task performance.
