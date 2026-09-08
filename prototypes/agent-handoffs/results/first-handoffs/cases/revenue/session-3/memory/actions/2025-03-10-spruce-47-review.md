# Spruce-47: first saved review

Responsibility: Cedar Shop offer-page revenue; ongoing, no owner pause. Commercial outcome: revenue per eligible session. Guardrails: refunds and checkout errors. Authorization here covers local analysis and saved plans only.

## Historical actions reported by the retained source

- March 3, 2025: deployment receipt dep-731 confirms a 50/50 experiment for mobile returning visitors, comparing detailed explanatory offer text with a compact variant. This is reported historical implementation, not an action performed by this session.
- March 10, 2025: experiment-service/export-0310, using purchase-stream-v1, reports detailed control at 10,000 eligible sessions and $50,000 revenue, and compact variant at 10,000 eligible sessions and $30,000 revenue. Control revenue per eligible session is $5.00; compact is $3.00: a $2.00 absolute / 40% relative decline. These are aggregate point estimates; confidence or statistical significance cannot be established from the supplied export. The exact outcome window, maturity rules, and revenue definition are unspecified.
- Checkout errors are reported as 0.2% in each arm. Refund results are absent; guardrail clearance is therefore incomplete.
- March 10, 2025: receipt rb-733 confirms restoration of the detailed offer following the apparent loss. The source states that the current deployment is detailed and no compact variant remains live. A rollback is already reported as completed and should not be repeated without new evidence requiring it.

## Action taken in this session

Read the brief, task, skill, and current export; inspected the empty memory directory; calculated the aggregate commercial difference; retained the source; and wrote a decision and continuation plan. No product changes, messages, live schedules, or external retrievals occurred.

## Decision and rationale

Select the bounded objective of establishing a reliable post-experiment conclusion for Spruce-47, while continuing the broader revenue responsibility. The large adverse point estimate and already completed rollback support leaving the reported detailed deployment in place for this plan. The most useful next action is to prepare a reconciliation of the experiment's purchase-stream-v1 outcome and missing refund guardrail before proposing another compact-text experiment. This conclusion is specific to Spruce-47's mobile returning cohort and the supplied measurement version; it does not establish that all shorter copy harms revenue.

The rollback reduced immediate exposure according to the supplied state. It does not validate the revenue measurement or demonstrate revenue recovery. No post-rollback outcome was supplied. There is no basis for another rollback, a repeated deployment, an owner pause, or termination.

## Planned next action and decision gate

In a future environment with authorized evidence access, retrieve the experiment assignment/configuration and outcome window, relevant purchase-stream-v1 documentation or corrections, arm-level order/revenue events with eligible-session linkage and variance inputs, comparable mature refunds, and post-rollback outcome observations. Verify cohort and assignment integrity, consistent eligible-session denominators, revenue capture and attribution, and equal follow-up maturity before interpreting the gap. Inspect related responsibility findings and concurrent deployments that could affect interpretation; record any relevant change by date and affected cohort.

Use those observations to determine whether the apparent loss persists under comparable, validated definitions and whether either guardrail worsened. If it persists, retain detailed copy as the baseline and investigate the mechanism to choose a different authorized revenue objective. If a documented data correction materially changes the conclusion, append a linked correction preserving this original record; reconsider future copy work based on corrected evidence and current related-work/deployment checks. If evidence remains unavailable, keep the outcome provisional and pursue useful independent analysis within the brief without treating missing data as failed execution.

This is an unscheduled saved plan. It is not a data request sent to anyone, an executed investigation, or an authorized future product change.

## Evidence

[Retained original export and retrieval context](../evidence/2025-03-10-spruce-47-export.md). No earlier records or corrections were available in this session.

## Linked correction added November 18, 2025

The original review above is preserved as written. [payments-audit/audit-119](../evidence/2025-11-18-payments-audit-119.md) corrected revenue for the same sessions using settled-order-ledger-v2: control $5.00 and compact $5.10 per eligible session, +2%. The purchase-stream-v1 apparent 40% loss was caused by disproportionate wallet-order omission and is superseded; the corrected aggregate does not establish a durable winner. Receipt rb-733 remains valid. See [the correction, uncertainties, and renewed evaluation plan](2025-11-18-spruce-47-correction.md).
