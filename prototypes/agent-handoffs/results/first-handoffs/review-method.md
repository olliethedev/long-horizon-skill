# Review method fixed before reading outputs

Review the three sessions for each domain against its preserved raw packets and `criteria.json`. Do not reward a particular memory layout or the presence of a skill. All domains use the same candidate, so this is not a skill-versus-baseline comparison.

For each session, assess whether material observations, actual actions, uncertainty, and the chosen continuation are faithfully recorded. In the final session, assess every listed historical fact as supported, omitted, or contradicted, with artifact references. A fact left in memory but not considered in the decision establishes retention only; inspect whether the relevant history actually informs the next action.

Calibrate the distinctions against these examples before scoring outputs:

| Domain | Supported reasoning | Plausible failure |
| --- | --- | --- |
| Revenue | The corrected point estimate supports reconsideration under a valid measurement plan; the old rollback is still a real event. | The old 40% loss permanently rules out shortened text, or the corrected 2% estimate proves it should be adopted immediately. |
| Weekly product | Saving partial setup remains an unshipped opportunity; organization activation changed definition and solo activation is not retention. | The saved-setup feature already failed, the metric correction redeployed Quickstart, or solo retention is claimed from activation. |
| Feedback | Preserve the partial rollback and small verification sizes; investigate 85k/92k completeness and timeouts before expanding streaming. | A generic release note establishes large-export safety, or new timeouts are described as newly observed missing records. |
| Post-PR bugs | The older corrected quota cause informs current investigation; establish today's cause separately and do not roll back an unexposed PR. | Treat the old release as the established cause, blame today's merged-but-undeployed PR, or claim current quota is confirmed from old evidence. |

A supported final decision may choose a different next objective from the examples when it respects the brief and evidence. Record material errors separately rather than hiding them in an aggregate score. Distinguish authored conclusions, copied raw observations, and missing evidence; copying a packet is legitimate evidence retention but does not itself establish useful recall.

Check static inputs and packet hashes, preserve every generation of memory and outbox, and confirm that the prior memory snapshot matches the next input memory exactly. No reviewer repairs, summaries, or added indexes pass between sessions. Review read/write reports as self-reports, not proof of enforced access boundaries. Model identity, token usage, and full harness/tool traces are not independently captured.

This is a manual, unblinded exploratory review, with one three-session chain per domain. These illustrative calibration anchors are not an independently validated model grader. More sessions, larger archives, competing cases, repeat trials, and actual actions against controlled services remain necessary.
