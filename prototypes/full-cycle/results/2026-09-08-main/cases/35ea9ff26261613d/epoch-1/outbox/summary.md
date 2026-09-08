# Session summary — fixture day 0 recovery

Recovered the interrupted deployment using its original operation key. Receipt `effect-3` and live status confirm revision 2, streaming with final-page handling enabled, and the active experiment. No duplicate deployment, reservation or paid validation was performed.

`measurement-4` verifies exposure and complete exact-ID checks at all supplied sizes, including 85,000 and 92,000 rows in 8.5 and 9.2 seconds. The required 14-day outcome window is immature; customer recovery and adoption remain unconfirmed. Five evaluation slots are occupied; shared validation usage remains 8/10 credits.

Requested a follow-up on fixture day 14 (2027-01-18), but the service returned transport_lost and explicitly interrupted the session. **No future schedule is confirmed.** The service contract supplies a recovery session; it must reconcile key `35ea9ff26261613d-d0-exports-observe-day14-v1` through operations and actual scheduler state before any retry. All service calls stopped after interruption.

Evidence: `memory/evidence/d0-recovery-deploy-operation.json`, `memory/evidence/d0-recovery-status.json`, `memory/evidence/d0-recovery-metrics.json`, and `memory/evidence/d0-recovery-schedule-day14.json`. Exact scheduling input is retained in `project/requests/d0-recovery-schedule-day14.json`. Durable handoff: `memory/current.md`; action record: `memory/actions/d0-deployment-recovery.md`. No routine report was due or owner notice required.
