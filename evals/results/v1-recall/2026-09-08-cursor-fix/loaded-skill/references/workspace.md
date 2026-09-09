# Durable workspace

Keep the owner's current brief, a short current handoff, and searchable original action/evidence records in readable local files. Choose a layout appropriate to the project; the following is a starting point, not a required schema:

Copy and adapt [responsibility](../assets/responsibility.md), [current handoff](../assets/current.md), [action](../assets/action.md), and [evidence](../assets/evidence.md) templates when creating a workspace. Resolve the brief in conversation before activating it; empty template fields do not supply authority or defaults.

```text
brief.md
current.md
actions/<stable-id>.md
evidence/<source-id>.<format>
index.md                    # optional, generated navigation
```

The handoff identifies the current objective/status, unresolved effects, active observations, relevant limits, confirmed continuation, and links needed for the next decision. Keep old detail in the underlying records; avoid repeatedly copying every plan and historical narrative into the handoff.

For a consequential action, retain its stable identity, subject and conditions, intended effect and rationale, actual service request/receipt, observed result or unresolved status, relevant evidence, and next observation. Distinguish proposed, implemented, deployed, observed, adopted, and rolled-back work without forcing every task through all these stages. Include source identities, periods, measurement definitions, and important missing coverage in retained evidence.

Link a correction to its earlier claim and source. Preserve the original observation and action history; date the revised interpretation and applicability. Related findings retain their originating responsibility and product. A terminated source remains terminated.

Write enough before an external effect that a fresh agent can reconcile it after interruption. Store atomic current-state updates where practical; retain original evidence separately so a damaged summary can be recovered. No unique finding may live solely in an index. Rebuild or bypass stale navigation using source files. Retain history through termination until owner deletion.
