# Contributing

Runtime instructions live in `skills/long-horizon/`. Keep the entrypoint concise and put conditional detail in linked references. Preserve the scope and lifecycle decisions in CONTEXT.md and docs/adr/. Frozen prototypes/results are evidence, not another maintained runtime implementation.

Python runtime helpers use Python 3.11+ and the standard library. Test the public CLI with real temporary files; avoid tests coupled to internal functions or wording. Typecheck runtime helpers and maintained evaluation tooling. Keep bounded output, original evidence, and explicit incomplete coverage as behavioral contracts. Helpers never infer authority from history or replace Impulse scheduling.

Run `python3 -m unittest discover -s tests` for the deterministic suite. Model evaluations and real Impulse integration are explicit opt-in commands described in evals/README.md; ordinary CI must not consume model allowance or operate a user's scheduler.

Every behavioral skill revision needs focused evaluations and review. Preserve actual loaded bytes, source/version provenance, raw traces, model configuration, observed decisions, failures, and limitations. Claims of reliable recall require evidence use, not just valid output. Never edit archived agent outputs to improve a score.
