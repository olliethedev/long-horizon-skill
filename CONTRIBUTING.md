# Contributing

Runtime instructions live in `skills/long-horizon/`. Keep the entrypoint concise and put conditional detail in linked references. Preserve the scope and lifecycle decisions in CONTEXT.md and docs/adr/.

The distributed skill contains instructions and supporting references; agents use their harness and available tools for retrieval and scheduling. Keep executable evaluation tooling in the repository, using Python 3.11+ and the standard library. The Antigravity host authentication adapter additionally uses the installed system Python D-Bus binding to read its unlocked Secret Service credential; this is an evaluation-host prerequisite, not a distributed skill dependency. Test public boundaries with real temporary files or subprocesses; avoid tests coupled to internal functions or wording. Typecheck maintained evaluation tooling. Preserve original evidence and explicit incomplete coverage; native tool use does not establish exhaustive or atomic retrieval by itself.

Run `python3 -m unittest discover -s tests` for the deterministic suite. Model evaluations and real Impulse integration are explicit opt-in commands described in evals/README.md; ordinary CI must not consume model allowance or operate a user's scheduler.

Every behavioral skill revision needs focused evaluations and review. Preserve actual loaded bytes, source/version provenance, raw traces, observed decisions and failures locally under ignored `evals/runs/` or a local evidence backup. Never edit original outputs to improve a score. Claims of reliable recall require evidence use, not just valid output.

Publish only concise reviewed results under `evals/results/<study>/REPORT.md`: what was compared, outcomes, relevant usage and material limitations. Do not commit raw traces, generated histories, copied source trees, large review dumps or campaign-specific publishing/recovery scripts. Keep reusable fixtures, runners, rubrics and tests in their maintained directories. Run `git diff --cached --check` before committing.
