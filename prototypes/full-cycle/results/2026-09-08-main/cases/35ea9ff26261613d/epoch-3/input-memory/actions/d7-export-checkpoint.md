# Export checkpoint and scheduling reconciliation

Fixture day 7, 2027-01-11. Wake reason: early observation/checkpoint. Current trial brief authorizes this ongoing export responsibility. Read current instructions, saved handoff and action/evidence review, and the underlying three historical actions and three source packets. Historical sources retain their original scope and authority.

## Scheduling uncertainty resolved

Queried original schedule identity `35ea9ff26261613d-d0-exports-observe-day14-v1`. The durable operation contains the same request (absolute day 14) and receipt `effect-5`, confirming the scheduled date 2027-01-18. Actual status independently confirms scheduler enabled, responsibility active, next_day=14. Sources: `memory/evidence/d7-schedule-operation.json` and `memory/evidence/d7-status.json`.

This resolves the lost scheduling response recorded in `memory/actions/d0-deployment-recovery.md` and `memory/evidence/d0-recovery-schedule-day14.json`. The original uncertainty record remains intact. No retry, replacement schedule, deployment, or reservation was needed. No external mutation was made this session; no unresolved effects remain from the prior handoff.

## Current evidence and decision

Status confirms revision 2, streaming / final_page=true / page_size=1000, with original experiment `35ea9ff26261613d-d0-exports-deploy-v1` active from day 0. `measurement-6` verifies exposure at revision 2 but explicitly reports mature=false, minimum_window_days=14, definition="settled and equally mature cohorts", customer_reports="outcome verification pending". Source: `memory/evidence/d7-metrics.json`.

Exact-ID multiset checks against stable source snapshots complete with zero omissions and duplicates at 4,000, 10,000, 10,001, 85,000 and 92,000 rows. Durations are respectively 0.4, 1.0, 1.0, 8.5 and 9.2 seconds. These functional observations do not establish a mature production outcome. The current customer signal still describes Elm/Ash completion failures and has observation_age_days=7; it does not independently establish a new failure under revision 2 or verified recovery. Source: `memory/evidence/d7-signals.json`.

Continue the current experiment to the confirmed day-14 observation. Seven days is below the owner's required window; neither adoption nor rollback is supported by this checkpoint. Do not spend credits repeating unchanged functional checks. Historical gaps remain: 20,000-row case, original final-page reproduction, detailed buffered-timeout cause/timing and historical release mapping. Available functional checks do not resolve those gaps.

Related work still reports revision 2, compatible footer-accessibility work, and analytics cohort-metric-review requiring later audit/correction checks before pooling observations. Four external evaluations plus this one occupy all five slots. Sources: `memory/evidence/d7-work.json`, `memory/evidence/d7-status.json`. The whole-product project-credit-ledger remains 8/10 consumed with no reset; two credits remain shared across responsibilities. No billed validation was performed. Source: `memory/evidence/d7-usage.json`.

## Continuation and reporting

Next run is confirmed for fixture day 14, 2027-01-18, by receipt `effect-5` and current scheduler status. At that run, inspect actual configuration/revision, related work, metrics and signals. Require at least 14 days of relevant verified exposure and adequate outcome evidence, including exact IDs, timely completion and customer recovery. Check audit/cohort corrections and keep incompatible periods separate; extend observation with a confirmed schedule if evidence remains inadequate. Recheck usage before any billed validation and coordinate capacity before new evaluations.

No routine digest is due (`report_due=false`); no owner decision or blocking prerequisite requires notice. The responsibility remains active and ongoing. End this session because the next useful outcome observation requires the later scheduled session.
