# Contributing

Runtime instructions live in `skills/long-horizon/`. Keep the entrypoint concise and put conditional detail in linked references. Preserve the scope and lifecycle decisions in CONTEXT.md and docs/adr/. Frozen prototypes/results are evidence, not another maintained runtime implementation.

The distributed skill contains instructions and editable templates; agents use their harness and available tools for retrieval and scheduling. Keep executable evaluation tooling in the repository, using Python 3.11+ and the standard library. The Antigravity host authentication adapter additionally uses the installed system Python D-Bus binding to read its unlocked Secret Service credential; this is an evaluation-host prerequisite, not a distributed skill dependency. Test public boundaries with real temporary files or subprocesses; avoid tests coupled to internal functions or wording. Typecheck maintained evaluation tooling. Preserve original evidence and explicit incomplete coverage; native tool use does not establish exhaustive or atomic retrieval by itself.

Run `python3 -m unittest discover -s tests` for the deterministic suite. Model evaluations and real Impulse integration are explicit opt-in commands described in evals/README.md; ordinary CI must not consume model allowance or operate a user's scheduler.

Every behavioral skill revision needs focused evaluations and review. Preserve actual loaded bytes, source/version provenance, raw traces, model configuration, observed decisions, failures, and limitations. Claims of reliable recall require evidence use, not just valid output. Never edit archived agent outputs to improve a score.

Frozen results retain their original whitespace and line endings. Scope whitespace checks to maintained changes with `git diff --cached --check -- . ':(exclude)evals/results/**'`; do not reformat evidence to satisfy a style check.
