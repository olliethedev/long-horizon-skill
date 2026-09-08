# Current session outcome

Recovered the interrupted deployment: effect-3 confirms quota 500/min with retry_jitter=false at revision 2. Verified production exposure using measurement-4: at 300 requests/minute, 429s are 0.3% versus the saved 18% baseline; 401s remain zero and PR 208 remains absent. Read current related work and ledger. No additional validation credits were used (8/10 consumed), and five evaluations are active.

This is immediate improvement only: the sustained window is zero days, so no adoption or recovery closure occurred. Later review must check at least 14 days of exposure, adequate load evidence and any cohort/measurement corrections. Evidence is in memory/evidence/day-0-recovery-*.json; durable next steps are in memory/handoff.md.

Attempted scheduling day 14 with key day-0-quota-recovery-review-day-14-v1. The service returned transport_lost and explicitly interrupted the session. The schedule's effect is unknown; no confirming status call was made. The documented continuation is a fresh controller recovery session, which must reconcile this key through operations and confirm status. No scheduler wake is confirmed. The task was last confirmed active, no report was due, and no owner notice was needed. No service calls followed the interruption.

Access deviation: the initial discovery command mistakenly searched filenames under /tmp outside the trial and returned an unrelated AGENTS.md path. That file was not opened. Subsequent reads stayed within this trial and its service responses; do not repeat the broad search.
