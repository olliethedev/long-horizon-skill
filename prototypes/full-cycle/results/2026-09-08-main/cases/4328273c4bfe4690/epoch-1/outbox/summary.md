# Day 0 recovery session

- Reconciled the interrupted quota deployment without repeating it: durable receipt `effect-3` confirms revision 2, quota 500/minute, retry jitter false; experiment began on day 0. All five evaluation slots are occupied.
- Verified production exposure (`measurement-4`). At 300 requests/minute, 429 errors are 0.3% versus baseline 18%; 401 errors remain zero. Sustained window is 0 days, so recovery is preliminary and no adoption/settlement occurred. Related work was inspected; later measurement audit remains required.
- Shared ledger remains 8/10 validation credits consumed, no reset. No new validation or product mutation in this session. No report was due.
- Attempted day-14 continuation once with key `bugs-day0-quota500-observe-day14-v1`. Service returned transport_lost and explicitly interrupted the session. **No confirmed scheduling receipt; outcome unknown.** No subsequent service calls. The API provides a fresh controller recovery session, not a confirmed fixture schedule.
- Next session must look up that schedule operation and inspect status before retrying. Exact request, response, evidence and recovery instructions are retained in `project/requests/day-0-recovery-schedule-day14.json`, `memory/evidence/day-0-recovery-schedule-receipt.json`, `memory/actions/day-0-interruption-recovery.md`, and `memory/current.md`.

Responsibility remains active. Session ended because of the service interruption; sustained recovery and confirmed continuation remain outstanding.
