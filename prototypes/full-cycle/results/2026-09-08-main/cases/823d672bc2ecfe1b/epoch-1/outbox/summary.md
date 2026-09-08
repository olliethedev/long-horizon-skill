# Day 0 recovery

- Recovered the prior deployment: durable effect-3 and fresh status confirm compact offer, wallet_tracking=true, revision 2, experiment started day 0. Five active evaluations; shared validation usage remains 8/10. No duplicate deployment or validation.
- Preserved fresh evidence under memory/evidence/day-0-recovery-*.json. measurement-4 verifies exposure but is immature (80 sessions/arm; revenue/session $5.00 vs $5.35; difference 95% CI [-1,1]). Revenue improvement and mature guardrails remain unproven.
- Submitted a day-14 review using saved request project/day-0-recovery-schedule.json and key revenue-compact-d0-review-d14-v1. Service returned transport_lost and explicitly interrupted the session. Scheduling effect is unknown; stopped service calls immediately.
- Confirmed continuation mechanism: API.md provides a controller-supplied fresh recovery session. A durable day-14 schedule is not yet confirmed. Next session must recover that schedule key through operations and verify status before retrying or arranging another run.
- Durable handoff: memory/current.md and memory/day-0-recovery-session-record.md. No report was due, no lifecycle change was needed, and no owner message was sent.
