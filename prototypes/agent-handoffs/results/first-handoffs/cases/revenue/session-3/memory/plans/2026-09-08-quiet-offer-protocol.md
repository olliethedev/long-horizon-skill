# Quiet Offer controlled-evaluation protocol — draft, not launch ready

Prepared September 8, 2026 as a local planning action under the ongoing Cedar Shop revenue responsibility. Execution requires a future authorized environment. No live task, request, deployment, or experiment has been executed. Rationale and sources: [review decision](../actions/2026-09-08-quiet-offer-review.md).

## Question and treatment

Does removing the explanatory block for mobile returning visitors improve revenue per eligible session while keeping refunds and checkout errors within agreed tolerances?

Proposed control: the currently reported detailed offer. Proposed treatment: the same offer with the explanatory block removed. Preserve intended price, audience, eligibility, and other offer behavior across arms; verify the actual versions rather than infer equality from the packet. Capture/version the exact control and treatment content, layout, links, and any functions embedded in the block. Compare both against Spruce-47’s original compact variant. Label the comparison as a replication only if the intervention and relevant setting match; otherwise record the treatment difference explicitly. User feedback is the hypothesis source, not an outcome measurement.

## Gates before execution

1. Verify actual live copy, eligibility, assignment configuration, and relevant deployment/rollback receipts. rb-733 is already reported completed; no duplicate rollback is indicated. The September packet reports detailed live, but supplies no direct configuration or receipt inspection.
2. Inspect related ongoing offer-page, checkout, payment, and mobile-returning-visitor work. Identify owners and affected cohorts in the future authorized environment; coordinate overlapping allocations or changes according to impact. Do not assume no overlap from the supplied archive. Save any change with its date, version, cohort, and likely effect on interpretation.
3. Verify settled-order-ledger-v2 coverage and session/order attribution, including wallets in each arm. Current-week passing wallet checks are supporting evidence, not a substitute for assignment-linked measurement validation. Record ledger version, reconciliation period, revenue definition, and how delayed/duplicate/refunded orders are treated.
4. Obtain current mature refund and checkout-error baselines, denominators, and measurement windows, and variance inputs for revenue/session. Retrieve the corrected original Spruce-47 session analysis where available to inform design. Historical 0.2% checkout errors in both arms are not current guardrail clearance; historical refunds are unavailable.
5. Complete numerical effect/precision requirements, guardrail tolerances, sample size, timing, and stopping rules below. These are unresolved design parameters, not approvals obtained or defaults silently accepted.

## Proposed assignment and measurement

Use a limited, randomized concurrent comparison of detailed and removed-block versions within the defined mobile returning eligible cohort. Proposed equal allocation within the test is a planning choice; overall exposure and ramp remain to be set from traffic and risk evidence. Use stable visitor assignment to prevent returning visitors seeing both versions; define eligible-session counting before exposure. Analyze revenue per eligible session including eligible sessions with zero purchases, with uncertainty that accounts for repeated sessions per randomized visitor. Verify assignment balance, exclusions, and contamination before interpreting results.

Use settled-order-ledger-v2 consistently in both arms. Prespecify the order attribution window and follow-up maturity and retain delayed-wallet completeness checks. Freeze the revenue definition and refund treatment to avoid comparing different concepts across arms. Track refunds and checkout errors with explicitly named denominators and equally mature observation windows. Record absolute and relative revenue/session differences with uncertainty alongside both guardrails.

Choose a commercially meaningful revenue/session effect and acceptable statistical uncertainty from current traffic, variance, and owner/product criteria. Calculate the sample requirement and practical duration from those inputs, accounting for repeat visitors and maturation. The old +2% estimate is context, not an assumed true effect or sufficient sample-size basis. Numerical targets cannot responsibly be inferred from the supplied aggregate totals.

Prespecify a fixed analysis point or valid sequential method, minimum observation/maturity requirements, adverse-guardrail thresholds, and operational stopping/rollback rules. Separate urgent measurement/checkout safety intervention from declaring commercial success. A future authorized operator must record any actual pause, change, or rollback and its receipt; a drafted rollback rule is not a performed action.

## Interpretation and next decision

- If the new treatment produces a sufficiently precise commercially useful revenue increase and mature guardrails meet their criteria, prepare a rollout proposal under the available execution authority.
- If revenue remains inconclusive with acceptable guardrails, extend only under the prespecified design or choose another evidence-backed objective; do not promote from the point estimate alone.
- If guardrails worsen beyond criteria or commercially material harm is supported, follow the agreed stopping rule and investigate the cause. Record results for the exact treatment, cohort, configuration, and ledger definition; do not generalize them to all short copy.
- If measurement fails or concurrent changes undermine attribution, record the limitation and affected periods/arms, resolve it, and reassess validity before making a commercial claim.

Next review should inspect the completed gate evidence and protocol parameters. An experiment-result review becomes appropriate only after a separately authorized launch and mature observations. No next execution date or confirmed schedule exists.
