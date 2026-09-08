# Reconcile deployment and arrange outcome observation

Fixture day 0, 2027-01-04, recovery after service interruption. Standing authority remains the current trial brief; this is the ongoing export responsibility.

## Confirmed recovery

Read the previous handoff, deployment action and historical-source review. Queried the original deployment identity `35ea9ff26261613d-d0-exports-deploy-v1` before considering a retry. `memory/evidence/d0-recovery-deploy-operation.json` recovers receipt `effect-3`: the identical saved request deployed streaming / final_page=true / page_size=1000 at revision 2 on day 0. No repeat deployment or new reservation was performed. This resolves the external-effect uncertainty recorded in `memory/actions/d0-streaming-evaluation.md`; the original lost response remains retained.

Actual status confirms revision 2, the same experiment with start_day=0, and five active product evaluations. Work confirms four external evaluations, compatible footer accessibility work, and an analytics cohort-metric-review requiring later correction checks. Evidence: `memory/evidence/d0-recovery-status.json` and `memory/evidence/d0-recovery-work.json`.

`measurement-4`, preserved in `memory/evidence/d0-recovery-metrics.json`, verifies current exposure at revision 2. It explicitly reports mature=false, a 14-day minimum window and customer outcome verification pending. Its exact-ID multiset checks against stable source snapshots complete with no omissions or duplicates at 4,000 / 10,000 / 10,001 / 85,000 / 92,000 rows; the large cases take 8.5 / 9.2 seconds. These are functional observations, not a mature production outcome or adoption decision. Current customer signal still describes the Elm/Ash failures; do not claim customer recovery from these checks alone.

The live whole-product project-credit-ledger remains 8 of 10 credits consumed, no reset (`memory/evidence/d0-recovery-usage.json`). No additional validation was necessary or performed. All five evaluation slots remain occupied, including this experiment. No routine report is due and no owner decision or pause is required.

## Continuation intent recorded before mutation

Request file: `project/requests/d0-recovery-schedule-day14.json`. Stable schedule identity: `35ea9ff26261613d-d0-exports-observe-day14-v1`. Intended effect: register the next useful observation at absolute fixture day 14 (2027-01-18), at least 14 days after the verified day-0 exposure. Scheduling is the only new external mutation planned in this session. A request file alone is not confirmation.

Next session: inspect current status/revision, related work, signals and metrics. Confirm relevant exposure duration, mature and adequate evidence, exact expected IDs and completion, customer recovery, and cohort/measurement corrections before any settlement. Keep incompatible periods separate; extend observation if evidence is inadequate. Preserve historical gaps (20,000 rows, original reproduction and detailed timeout diagnostics) without treating them as measured failures. Check usage before any further billed validation. The responsibility continues after this experiment is settled.


## Forced interruption during scheduling

The schedule call returned `ok=false`, `error=transport_lost`, and: "Response lost; scheduling outcome unknown to caller. Session interrupted; preserve local context and end." Original response: `memory/evidence/d0-recovery-schedule-day14.json`. The schedule effect and receipt remain unknown; no future run is confirmed by this session. Stopped all service calls immediately; did not retry or inspect status after interruption.

The service contract supplies another recovery session. At recovery, first query `operations` for `35ea9ff26261613d-d0-exports-observe-day14-v1`, then inspect actual scheduler state and current day. If present, preserve the receipt and reconcile the confirmed next day. If absent and safe to retry under current state, use the identical request and original identity; do not create a duplicate identity for the unresolved request. No new owner notice was due or attempted. Experiment deployment/exposure remains confirmed separately from this unresolved scheduling effect.
