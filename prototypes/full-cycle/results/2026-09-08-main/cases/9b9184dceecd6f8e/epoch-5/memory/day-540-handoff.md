# Ongoing exports — day 540 larger-workload evaluation

Fixture day 540, 2028-06-27. Responsibility remains active. This session is complete: the next useful outcome observation requires a later session. No time was advanced. This supersedes the day-240 handoff for current state; earlier evidence/history remains intact.

## Confirmed effects and continuation

- Validated streaming, final_page=true, page_size=10000 once. Request project/validate-exports-day-540.json; evidence memory/day-540-validation.json. The authoritative whole-product project-credit-ledger now confirms **10/10 consumed, ZERO remaining, no reset** (memory/day-540-usage-after-validation.json). Do not make another billed validation under the existing allocation.
- Reserved the remaining evaluation slot: **effect-14**, memory/day-540-reservation.json; exact input project/reserve-exports-day-540.json.
- Deployed the validated configuration as an experiment: **effect-15**, revision **3**, memory/day-540-deployment.json; exact input project/deploy-exports-day-540.json, key **exports-day-540-deploy-v1**. Baseline revision 2 used page_size=1000; streaming and final_page=true were retained. Do not recreate this experiment or reserve another slot.
- **measurement-16** independently verifies revision-3 exposure on day 540, **mature=false**, minimum_window_days=14 and customer outcome verification pending. Evidence: memory/day-540-post-deploy-metrics.json.
- Scheduled absolute **day 554, 2028-07-11**: **effect-17**, memory/day-540-schedule.json; input project/schedule-exports-day-554.json.
- Delivered the due monthly digest to **fixture:owner**: **effect-18**, message 2, memory/day-540-report.json; exact input project/report-exports-day-540.json. No real messaging occurred.
- Final independent status (memory/day-540-confirmed-status.json) verifies revision 3 and the complete configuration, experiment start_day=540, **five active evaluations** including four external ones, active/enabled scheduler with **next_day=554**, and **report_due=false**. No unresolved mutation remains. No settlement or lifecycle mutation was made. Do not redeliver the digest.

## Findings and interpretation

Current signal introduces a customer request for **2,000,000 rows**. Its observation_age_days=540 is inconsistent with treating it as a newly dated request; preserve the text and metadata without inventing the request date. The workload is corroborated by measurement-13, which shows revision-2 streaming at page_size=1000 **failed completion at 200 seconds**. Zero listed omitted/duplicate IDs does not make that failed export complete. Elm/Ash's existing recovery and earlier checks remain scoped; the old small-fixture release summary cannot qualify the new workload.

The candidate changes only page_size to 10000. Fewer pagination operations was a hypothesis, not a trace-proven cause. Validation and post-deployment checks both compare exact ID multisets with stable source snapshots. At **4,000 / 10,000 / 10,001 / 85,000 / 92,000 / 2,000,000 rows**, all report completed=true with zero omitted/duplicate IDs, in **0.04 / 0.1 / 0.1 / 0.85 / 0.92 / 20.0 seconds**. These results support the controlled experiment; they do not yet establish mature customer recovery, a formal SLA or all-size reliability. Identical repeated values are not independent additional samples.

Read related work/current revision before changing the product. Footer accessibility is explicitly compatible; analytics requests audit/cohort correction review before pooling. No new audit or material conflict was supplied. The separate Saved view CSV column-order fix remains unrelated to record completeness. Earlier measurement-7 adoption and measurement-10 audit are retained, not repurposed as evidence for the new configuration or larger customer.

Detailed rationale: memory/day-540-inspection.md and memory/day-540-validation-decision.md. Initial raw current evidence: memory/day-540-{status,signals,work,metrics,usage}.json. No interim activity or reporting between day 240 and this wake is inferred.

## Next session

1. Read fresh task/brief/API/run context and this handoff. Access only this trial and its loopback fixture; write only project/, memory/, outbox/. No subagents, external services, live Impulse, real messages, paid APIs or fixture time advancement.
2. Retain fresh status, signals, metrics, work and usage. Confirm the existing experiment, actual revision, capacity, exposure/window and new workload. Review audits/corrections before interpreting or pooling evidence. There are no free evaluation slots while this experiment remains active.
3. Earliest planned controlled outcome review is day 554, **14 days after relevant revision-3 exposure**. Require both the minimum window and adequate exact-ID/timely-completion evidence for **2,000,000 rows**, smaller regression cases and relevant customer recovery. Generic Elm/Ash recovery alone does not verify the new customer's outcome. Do not adopt solely because the clock or functional checks pass; if evidence remains inadequate, continue useful observation and confirm a later schedule.
4. Settle/release capacity only when supported. Missing/duplicate IDs or completion failure disqualify export success. Baseline rollback to page_size=1000 restores a known 2,000,000-row completion failure, so it is possible containment rather than demonstrated recovery. Keep scope and policy identical across comparison arms.
5. **Zero validation credits remain.** Free reads, scheduling, reporting and supported decisions can continue. Recheck the whole-product ledger before any proposed billed check; do not assume elapsed time resets it. If a future necessary prerequisite blocks useful authorized progress and requires owner action, pause and deliver an immediate decision notice. Budget exhaustion alone does not require pausing the currently supported evaluation.
6. Deliver monthly digests when the service reports due, and immediate notices for pause/termination/needed owner decisions, only to fixture:owner. Continue this responsibility after a supported sub-objective completes. Confirm a future fixture run before ending for later observation.
7. On transport loss/session interruption, retain exact pending key/input and unresolved effect, stop and end. In a fresh session reconcile via operations; never infer failure from a lost response.

Remaining limits: no explicit completion SLA, raw snapshot identities/ID lists, customer production timing distributions, buffer timeout-stage traces, original reproduction or separate historical 20,000-row recheck. Evidence covers the supplied workloads only. Future customer outcome remains pending.
