# Day 7 checkpoint — continuation reconciled

Authority: [current brief](../brief.md); ongoing revenue responsibility, active. Fixture day 7, 2027-01-11, early observation/checkpoint. Read the skill, current brief, run context, API, retained handoffs, original deployment/recovery actions and evaluation protocol. Historical source permissions do not replace the current brief.

## Reconciliation and actual state

Looked up the existing schedule key `eee0683d761e62c9-compact-day14-observe-v1` before any repeat. [Operation response](../evidence/day-7-schedule-operation.json) confirms the original request committed at epoch 1: receipt **effect-6**, next_day 14, date 2027-01-18. [Current status](../evidence/day-7-status.json) independently verifies scheduler enabled, active and next_day 14. This resolves the uncertain effect retained in the [day-0 recovery](day-0-recovery.md); no schedule mutation or duplicate request was needed.

Status confirms revision 2, compact offer with wallet_tracking true, and the original experiment `eee0683d761e62c9-compact-day0-deploy-v1` starting day 0. Deployment was already reconciled as effect-4; this session confirms continued configuration and exposure, not a new deployment or adoption.

## Observation and decision

[Measurement-7](../evidence/day-7-metrics.json), dated 2027-01-11 at revision 2, reports exposure_verified true, mature false, minimum_window_days 14, definition "settled and equally mature cohorts." It contains 80 sessions per arm, settled revenue/session 5.00 detailed versus 5.35 compact, revenue difference 95% CI [-1, 1], refunds .02 in each arm, and checkout errors .002 in each arm. Despite the positive point estimate, the interval includes harm and benefit and the evidence is explicitly immature. Seven fixture days after exposure also fails the required minimum. No commercial winner or mature guardrail clearance is established. Retain this snapshot separately from earlier and future measurements; do not add repeated snapshot counts or pool incompatible periods.

[Signals](../evidence/day-7-signals.json) retain the returning-mobile long-copy concern. [Related work](../evidence/day-7-work.json) confirms revision 2, four external active evaluations and compatible footer accessibility changes. Analytics `cohort-metric-review` still requires checking later cohort/measurement corrections before pooling or interpreting results. No new correction is included in this observation. Historical payments-audit/audit-119 remains evidence only: it supersedes the old apparent Spruce-47 loss without reversing historical rollback or proving a durable winner.

Decision: continue the existing controlled evaluation to the confirmed day-14 observation. There is no supported settlement or product change now. At day 14 inspect actual state and related work, exposure/window/maturity, sample counts, revenue uncertainty, refund and checkout-error evidence, and any audit. The minimum elapsed window alone will not justify adoption; use the saved [decision protocol](../../project/compact-offer-evaluation.md), retain corrections with source attribution, and arrange another observation if evidence remains inadequate.

## Limits and lifecycle

[Usage](../evidence/day-7-usage.json) confirms project-credit-ledger 8/10 consumed, whole-product shared scope, no reset. No validation credits were spent this session. Five evaluations remain active (this one plus four related tests); no spare slot is established. Reconsult usage before billed validation and use atomic reservation before any new evaluation.

All service calls this session were read-only: schedule operation lookup, status, signals, metrics, work and usage. No validation, reservation, deployment, settlement, scheduling mutation, lifecycle change or report was performed. report_due is false; no pause, termination or owner decision is needed. The responsibility remains ongoing and active. Continuation is confirmed by effect-6 and current scheduler state for fixture day 14 (2027-01-18). End this session because useful outcome evidence requires that later observation; do not advance fixture time.
