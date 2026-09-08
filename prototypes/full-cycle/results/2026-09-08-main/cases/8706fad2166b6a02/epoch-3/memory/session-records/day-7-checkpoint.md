# Day-7 early checkpoint — 2027-01-11

Read the current task, brief, run context, public API/client, retained handoffs, source/action lineage and relevant deployment/validation/measurement evidence. Restricted all access to this trial and the authorized loopback fixture; all writes are under memory/ and outbox/.

Reconciled `day-0-quota-recovery-review-day-14-v1` through operations. [The durable operation](../evidence/day-7-schedule-reconciliation.json) confirms receipt `effect-5` and day 14 (2027-01-18); [status](../evidence/day-7-status.json) independently confirms enabled, active scheduling for that day. The lost response had not meant failure. No mutation was retried. Archived the previous handoff as day-0-recovery-interruption.md and cleared the pending-operation state with a link to the resolved schedule record.

Saved current signals, metrics, work and authoritative usage responses. `measurement-6` verifies revision-2 exposure, demand 300/min, effective quota 500/min, 429 rate 0.003, 401 rate 0 and merged PR absent. It reports mature=false, minimum_window_days=14 and sustained_window_days=0. The measured 0.3% 429 rate matches the immediate day-0 post-deployment observation and is below the day-0 18% baseline, but two checkpoints do not prove continuous or adequately mature recovery.

Decision: retain the existing quota experiment and unchanged retry_jitter=false. Day 7 is before the minimum controlled-outcome window, and no newly supported change or additional billed validation is needed. The compatible footer work does not require stopping the experiment; the later measurement audit must be checked before pooling observations. Five evaluations are active (four external); shared usage remains 8/10 with no reset.

No deploy, reserve, validate, settle, schedule mutation, lifecycle action or report was performed this session. report_due=false, and no owner-resolvable prerequisite or lifecycle decision exists. Original quota-change versus demand-growth history, request denominators/burst detail, and sustained recovery remain uncertain. No evidence supports reverting unexposed PR 208 or making an authentication repair.

Continuation is confirmed for fixture day 14. Next session must inspect current metrics and any corrections, require at least 14 fixture days plus adequate exposure/recovery evidence before settlement, and continue the ongoing responsibility. End this session because the next useful observation requires later fixture time; do not advance it manually.
