# Evidence and time

Retain source identity and the actual observation before summarizing it. The [evidence template](../assets/evidence.md) keeps time and scope separate:

- **Event/request time:** when the underlying event occurred or feedback was submitted, if supplied.
- **Deployment/exposure time:** when the relevant version reached the population, established by actual rollout evidence.
- **Observation window:** the interval and cohort measured; a minimum-duration assertion is different from exact start/end timestamps.
- **Retrieved time:** when this agent obtained the source.

Store an unavailable field as unknown. An `age_days` field needs a documented reference event; inspect its definition or qualify it. Retrieval time, a file modification date, and time since deployment cannot supply a missing request timestamp.

An unknown request time also leaves whether it preceded or followed a rollout unknown unless separate evidence establishes that relationship.

Link a correction to the precise earlier source/claim, its subject and measurement definition. A newer record for a different cohort or version does not supersede the relevant observation. Retain conflicting sources and identify what would reconcile them. Corrected conclusions do not erase actual deployments, rollbacks, or previously delivered reports.

Separate implementation checks, actual deployment/exposure, and observed user outcomes. Feature availability can coexist with current user friction. A merged PR may be absent from production. A functional export check at one size cannot establish completeness and timeliness at another. Use the domain's evidence method; the skill does not impose a statistical test or universal success threshold.

Distinguish observations, plausible explanations, and established causes. Before persisting a decision or learning, check its explanatory claims against the sources, including the summary. A diagnostic warning alongside a failure supports a hypothesis, not a proven mechanism. An inconclusive result remains compatible with harm and benefit.
