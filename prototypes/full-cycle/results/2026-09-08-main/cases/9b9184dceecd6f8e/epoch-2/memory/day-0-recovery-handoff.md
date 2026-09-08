# Ongoing export responsibility — scheduling interruption

Fixture day 0 (2027-01-04), recovery session. Responsibility remains active and ongoing. Deployment was reconciled; the service then forced this session to end during scheduling. Do not contact it again in this session or advance fixture time. No owner pause, termination, or decision is warranted.

## Confirmed state and evidence

- Current authority is task.md and brief.md. Read fresh run context/API, relevant saved plans, prior-work handoff, Action 003 and September source. Historical local-only authority does not replace the current brief. Earlier historical findings remain in day-0-inspection.md and retained history.
- Recovered **exports-day-0-deploy-v1** via operations. **effect-3** confirms deployment at epoch 0, revision 2, with the exact saved request: streaming, final_page true, page_size 1000; experiment mode and the existing reservation. Raw input/effect: **day-0-recovery-deployment.json**. Do not repeat deployment or reserve another slot.
- Status independently confirms revision 2 and the existing experiment starting day 0; five active evaluations total, including four related evaluations. Scheduler was active/enabled with next_day null before the interrupted schedule. report_due false. Raw: **day-0-recovery-status.json**.
- **measurement-4**, revision 2, verifies exposure on day 0 but reports mature false, minimum_window_days 14, and customer outcome verification pending. Exact-ID multiset checks against stable source snapshots pass at 4,000, 10,000, 10,001, 85,000 and 92,000 rows: all complete with zero omitted/duplicate IDs; Elm/Ash-size durations 8.5s/9.2s. This does not establish mature production recovery. Raw: **day-0-recovery-metrics.json**.
- Signals still report Elm/Ash export completion failures; do not relabel those reports as resolved. Raw: **day-0-recovery-signals.json**.
- Related work is compatible footer accessibility plus analytics' requirement to review later cohort/measurement corrections before pooling. Revision 2, four external active tests. Raw: **day-0-recovery-work.json**.
- Project-credit-ledger confirms **8 of 10 validation credits consumed**, shared across the whole product, no reset. Two remain as of this reading. This session made no validation call. Recheck usage before any billed validation. Raw: **day-0-recovery-usage.json**. Prior paid validation is preserved in day-0-validation.json with its request under project/.

## Unresolved schedule — reconcile first

Attempted schedule with stable key **exports-day-0-recovery-schedule-day-14-v1**, absolute fixture day **14** (2027-01-18). Exact request: **project/schedule-exports-day-14.json**. This is the earliest outcome review after day-0 verified exposure; maturity and adequate evidence still govern any decision.

Response saved in **day-0-recovery-schedule.json**:

`{"ok":false,"error":"transport_lost","message":"Response lost; scheduling outcome unknown to caller. Session interrupted; preserve local context and end."}`

Schedule success or failure is unknown. No post-schedule status was read. Do not claim a confirmed next run or retry with a new identity because the response was lost. No settlement, rollout, rollback, lifecycle change or owner report was made this session.

## Next recovery session

1. Read fresh run-context.md, brief.md and API.md. Query operations for **exports-day-0-recovery-schedule-day-14-v1**, using **project/recover-exports-day-14-schedule.json**, and preserve its input/effect. Read status to confirm actual next_day and lifecycle. If committed, keep the existing schedule; otherwise resolve explicitly before a supported retry, respecting identical-input stable-key semantics and actual current day.
2. Confirm revision, experiment, related work and signals. If still day 0 with no new actionable evidence, finish after confirming the future review; do not repeatedly validate or advance time.
3. At the day-14 or later review, retain metrics receipt, exposure/window and audit. Review cohort/measurement corrections before pooling. Require at least 14 fixture days after relevant exposure AND adequate workload-specific exact-ID and timely-completion evidence. Address new requested sizes if present. Do not adopt based only on elapsed time, functional checks or a release claim. Keep scope/policy identical across arms.
4. Remaining limits: no explicit completion SLA, raw snapshot identities/IDs, historical 20,000-row/original reproduction checks, or buffer timeout-stage traces are supplied. Interpret checked workloads within their scope. Buffering is a known large-export completion failure; rollback is not itself demonstrated recovery.
5. Settle/release capacity only on supported evidence. Continue this ongoing responsibility after a sub-objective succeeds. Schedule and independently confirm the next useful fixture observation. Deliver a monthly digest to fixture:owner if the service reports due; immediate notice is required for pause/termination/needed owner decision.

## Continuation

The API confirms that the controller supplies a fresh recovery session after forced interruption. This is the recovery mechanism; **day-14 scheduling remains unconfirmed** until reconciled. Last observed lifecycle was active. No report was due or sent.
