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

Keep records proportional to useful work: ordinary checks can update the handoff or append dated observations to an existing record; a no-change run does not need a new collection of boilerplate files. Retain consequential actions and original decision evidence. Reports and related responsibilities should link to the same retained source where access permits, instead of copying exports into each folder. An independently distributed report may need its own supporting copy.

As history grows, partition records by responsibility and, when useful, time period. Keep a small product-level directory of responsibility briefs and relevant shared work; retrieve underlying records selectively through [history.md](history.md). A directory or index is optional navigation, not another copy of every history. Preserve stable identities and resolve links when moving records; accumulated file count alone is not a reason to discard evidence.

## Artifact policy

Resolve this during setup, following existing project instructions and the owner's choice. Recommend committing concise durable briefs, handoffs, action/outcome/learning records, and portable task definitions. Keep bulky or sensitive evidence in ignored, backed-up storage accessible to future authorized sessions. Fuller versioning of non-sensitive evidence is a valid project choice.

Record which paths are tracked or ignored, the repository's audience, automatic commit and push authority, target branch, checkpoint cadence, and the location, access, backup and retention policy for evidence outside Git. Retained records must link to that evidence. An unavailable backup or future-session access path is a readiness gap, not an assumed service. Keep credentials and private runtime data out of shared Git history.

At agreed checkpoints, inspect changes and include only authorized responsibility artifacts in commits; unrelated developer work can coexist. Retention and Git tracking are separate decisions: ignoring evidence does not authorize deletion. Portable scheduler definitions do not reproduce registered tasks, runtime state, authentication, or backups.

## Action and evidence records

For a consequential action, retain its stable identity, subject and conditions, intended effect and rationale, actual service request/receipt, observed result or unresolved status, relevant evidence, and next observation. Distinguish proposed, implemented, deployed, observed, adopted, and rolled-back work without forcing every task through all these stages. Include source identities, periods, measurement definitions, and important missing coverage in retained evidence.

Link a correction to its earlier claim and source. Preserve the original observation and action history; date the revised interpretation and applicability. Related findings retain their originating responsibility and product. A terminated source remains terminated.

Write enough before an external effect that a fresh agent can reconcile it after interruption. Store atomic current-state updates where practical; retain original evidence separately so a damaged summary can be recovered. No unique finding may live solely in an index. Rebuild or bypass stale navigation using source files. Retain history through termination until owner deletion.
