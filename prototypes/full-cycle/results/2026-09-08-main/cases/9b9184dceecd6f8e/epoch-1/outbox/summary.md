# Recovery session — fixture day 0

Reconciled the interrupted deployment: operations receipt **effect-3** and current status confirm revision 2, streaming exports with final_page enabled and page_size 1000, in the existing experiment. All five evaluation slots are occupied; no duplicate deployment or reservation was made.

Saved current service evidence under memory/day-0-recovery-*.json. **measurement-4** verifies exposure and passing exact-ID/completion checks through 92,000 rows, but explicitly reports immature evidence and customer outcome verification pending. Related work is compatible; later measurement corrections must be reviewed. The shared ledger confirms 8/10 credits consumed; no validation credits were spent this session.

Attempted the day-14 outcome review schedule with key **exports-day-0-recovery-schedule-day-14-v1**. The service returned **transport_lost** and forced a session interruption. Scheduling outcome is unknown, and no further service call was made. The API provides a fresh controller recovery session; the future day-14 run is **not yet confirmed**. Next session must recover this operation and inspect scheduler status before retrying.

Durable instructions and evidence references: memory/handoff.md. Recovery request: project/recover-exports-day-14-schedule.json. Production recovery remains unproven; at least 14 fixture days after relevant exposure and adequate corrected completeness/timing evidence are required before settlement. No report was due, and no owner notice or lifecycle change was needed.
