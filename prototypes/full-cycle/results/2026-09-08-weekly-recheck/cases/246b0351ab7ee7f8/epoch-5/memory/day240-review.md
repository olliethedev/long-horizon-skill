# Day-240 source-audit review — 2027-09-01

The responsibility remains active. Keep the revision-2 resumable-setup experiment open for a later corrected-evidence review; neither adoption nor rollback is supported by the available outcome evidence. No configuration change, new evaluation, or billed validation is needed today.

## Correction and decision

Current metrics receipt **measurement-9** corrects **measurement-1, measurement-4, measurement-6 and measurement-7**. The audit says earlier exposure assignment included existing customers; restricting the analysis to original eligible new users revises activation. Completed-project activation still excludes drafts. Corrected control/variant activation is **42%/43%**, difference +1 percentage point, reported 95% CI **[-2,+4] points**. Retained use separately is **31%/32%**, difference +1 point, CI **[-1,+3] points**. Neither benefit, material harm nor equivalence is established for either outcome. No commercial benefit is established.

The day-14 conclusion that activation improved is **superseded**. Preserve its original evidence as historical; use measurement-9 for current conclusions and do not pool corrected and superseded estimates. This is a correction of the existing experiment's eligible population, not a fresh experiment, new deployment, or proof of recovery. Status still shows experiment start day 0; the audit provides no replacement exposure start date. Its arrival on day 240 does not itself restart the minimum window. Metrics verifies exposure and mature=true, minimum_window_days=14; elapsed time and that flag do not overcome inadequate evidence.

Missing information remains: sample sizes, assignment design and integrity after the restriction, exact enrollment/observation windows, retention horizon, coverage and guardrails. The audit describes original eligibility, not a policy change across arms; keep scope and accepted policy identical across arms. Do not infer newly collected historical solo retention or conflate these users with historical Quickstart cohorts.

## Verified state and constraints

- evidence/day240-status.json: day 240, revision 2, save_setup=true, explicit_template=true; original experiment active, five active evaluations, scheduler enabled/active with next_day=null; monthly report due. The prior day-28 registration is historical and no longer establishes pending continuation. No intervening review outcome is supplied.
- evidence/day240-work.json: revision 2, four external evaluations; footer accessibility remains compatible. Measurement review specifically requires attending to cohort corrections, which this review does. No material implementation conflict is reported.
- evidence/day240-signals.json: a new audit pointer accompanies a **240-day-old** unsaved-draft statement. Verified deployed configuration and original successful functional checks contradict treating that old statement as a new failure.
- evidence/day240-usage.json: project-credit-ledger reports **9/10 credits consumed, 1 remaining, no reset**, including other responsibilities. No validation called this session; functional revalidation would not resolve cohort or outcome uncertainty.

## Next observation and reporting

Request a review on **day 254 (2027-09-15)** to look for additional eligible-new-user observations, audit clarification and separate retained-use evidence. The date is an observation checkpoint, not a claim that more time will produce adequate data or a 30-day retention measure. Do not repeat current metrics within this session hoping for a changed result. If another review provides no additional information, reassess the measurement path and usefulness of retaining the evaluation slot instead of treating another elapsed interval as progress. If an owner-resolvable measurement prerequisite is evidenced and blocks useful work, pause and notify under the brief; none is established today.

Adoption still requires valid mature activation and retained-use benefit with acceptable guardrails. Credible harm can support rollback. Before a future product change recheck work and actual revision; consult usage before any billed validation, obey capacity, and preserve stable mutation keys. Historical organization metric correction and uncollected solo retention remain separate unresolved history in history/prior-work/.

The monthly digest is due and should be delivered to fixture:owner with this correction and the verified continuation. Scheduling and reporting outcomes will be recorded in the current handoff and appended here. Recover any ambiguous mutation using operations in a fresh session; stop immediately on service interruption.

## Confirmed action outcomes

Schedule **effect-10**, key weekly-resumable-setup-review-day254-v1, registers day 254 (2027-09-15). Independent after-schedule and final status both verify enabled/active next_day=254. Monthly digest **effect-11**, key weekly-product-monthly-digest-day240-v1, was delivered to fixture:owner as message 1; final status confirms report_due=false. No unresolved mutation remains. Requests are retained under project/ and full receipts under memory/evidence/day240-*.json. No deployment, settlement, lifecycle change, reservation or validation occurred. Current handoff is finalized; end this session for the later observation.
