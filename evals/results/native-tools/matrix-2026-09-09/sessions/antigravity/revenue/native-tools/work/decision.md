# Revenue Responsibility: Offer Experiment Decision

**Date:** 2026-09-08  
**Author:** Revenue Responsibility Autonomous Agent  
**Owner:** Sam, Product Lead  
**Scope Reference:** [/workspace/product/brief.md](file:///workspace/product/brief.md)  
**Status Reference:** [/workspace/product/current.md](file:///workspace/product/current.md)  

---

## 1. Recommendation Summary

Between the two proposals under review—**Quiet Return** (for returning mobile subscribers) and **Harbor** (for new mobile accounts)—**Harbor (Variant H2) deserves the next experiment**. **Quiet Return does not deserve an experiment**.

- **Quiet Return (Variant R7)** appeared successful initially (+11% trial starts in [`record-da3a9e962e`](file:///workspace/product/history/evidence/record-da3a9e962e.md)), but mature ledger analysis proved it was net-revenue destructive (**-6.2% refund-adjusted net revenue** in [`record-802325ed36`](file:///workspace/product/history/evidence/record-802325ed36.md)). The refreshed proposal in [`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md) retains the identical R7 discount pricing, eligibility rules, and checkout flow—altering only illustration colors. Because the economic drivers of customer dissatisfaction and refunds remain unchanged, running Quiet Return again risks predictable revenue loss.
- **Harbor (Variant H1)** was prematurely branded a loss (-9% in [`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md)) due to double-counting resumed sessions in the denominator and a confirmed UX defect where annual selections reset during the OS permission dialog. When telemetry was deduplicated in [`record-47eaba418e`](file:///workspace/product/history/evidence/record-47eaba418e.md), revenue per new account was actually **+1.8%** (inconclusive), even while handicapped by the reset bug. Harbor H2 ([`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md)) directly resolves the permission-dialog reset (verified in QA [`record-0d1c74ca54`](file:///workspace/product/history/design/record-3c858d6a57.md)), leaving the fundamental revenue hypothesis viable and ready for an unbiased test.

Per [`brief.md`](file:///workspace/product/brief.md), standing policy permits at most one new experiment at a time, prioritizing refund-adjusted net revenue over trial starts. Harbor H2 is the sole candidate with a sound, untested revenue hypothesis and targeted defect remediation.

---

## 2. Relevant Prior Actions & Reconstructed Chronology

### A. Quiet Return for Returning Mobile Subscribers

1. **Origin & Baseline Action ([`record-b7ab79e22e`](file:///workspace/product/history/retired/summer-offers/actions/record-b7ab79e22e.md)):**
   - **Origin:** Originating in the `summer-offers` campaign ([`/workspace/product/history/retired/summer-offers/brief.md`](file:///workspace/product/history/retired/summer-offers/brief.md), terminated 2026-07-30; historical records retained under standing revenue authority).
   - **Aliases:** `QR7`, `returning mobile offer`, `Quiet Offer`.
   - **Target Cohort:** US returning iOS annual subscribers.
   - **Intervention (Variant R7):** Offered a 20% annual renewal discount upon return.
   - **Deployment & Exposure:** Deployed on 2026-07-12 via rollout receipt `record-e4142b048e` at 50% traffic exposure. The observation period spanned July 13–19, 2026.
   - **Rollback:** Rolled back on 2026-07-21 (receipt `record-e0da7df86e`) due to mounting customer support escalations regarding refunds.

2. **Early Observation ([`record-da3a9e962e`](file:///workspace/product/history/evidence/record-da3a9e962e.md)):**
   - **Recorded:** 2026-07-20.
   - **Initial Finding:** Trial starts increased by **+11%**, leading an analyst to headline the trial as "promising." However, the record noted explicitly that retained net revenue was not yet mature.

3. **Mature Ledger Correction ([`record-802325ed36`](file:///workspace/product/history/evidence/record-802325ed36.md)):**
   - **Recorded:** 2026-08-04.
   - **Corrected Finding:** Followed the July 13–19 exposure cohort with matched refund ledger data through August 2, 2026. While the +11% trial-start volume was real, **refund-adjusted net revenue was 6.2% below control (-6.2%)**. 
   - **Applicability & Conclusion:** The matched ledger was confirmed complete for this cohort. The record stated definitively: *"No price or eligibility changes justify repeating R7 in this cohort."*

4. **Irrelevant Name Reuse Warning ([`record-3965c8ff16`](file:///workspace/product/history/evidence/record-3965c8ff16.md)):**
   - **Recorded:** 2026-09-06.
   - **Context:** A recent correction noted a +4% net revenue lift under the name "Quiet Return" for action `record-cf96fad305`.
   - **Separation:** This report tested variant W3 on **US returning desktop monthly subscribers** exposed August 20–27, 2026. The record explicitly cautions: *"This report does not cover record-b7ab79e22e, R7, returning iOS annual subscribers, or July exposures."*

5. **September Design Proposal ([`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md)):**
   - **Dated:** 2026-09-02.
   - **Change Proposed:** Maintains identical R7 pricing (20% discount), identical eligibility, and identical mobile checkout flow; only illustration colors were updated.

---

### B. Harbor for New Mobile Accounts

1. **Baseline Action ([`record-dc92607ff3`](file:///workspace/product/history/actions/record-dc92607ff3.md)):**
   - **Aliases:** `Anchor plan picker`, `annual card`, `Harbor H1`.
   - **Target Cohort:** New US mobile accounts.
   - **Intervention (Harbor H1):** Presented an annual subscription selection card / anchor plan picker during initial mobile onboarding.
   - **Deployment & Rollout:** Deployed August 10 [year not stated in record; preserved as August 10], rollout record `record-eb44fddf46`.
   - **Rollback:** Rolled back August 18 [year not stated in record; preserved as August 18], receipt `record-4cd3618639`.

2. **Initial Inaccurate Evidence ([`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md)):**
   - **Recorded:** August 18 [year not stated in record; preserved as August 18].
   - **Observation Window:** August 11–17 [year not stated in record; preserved as August 11–17].
   - **Initial Metric:** Revenue per new account reported at **-9%** (with no confidence claim).
   - **Telemetry & UX Failures Identified:**
     1. Resumed app sessions were double-counted as new accounts in telemetry, artificially inflating the denominator.
     2. In session recordings, 7 of 12 reviewed user sessions that encountered the OS permission dialog had their chosen annual plan selection reset to default.
   - This flawed initial report was the source of [`current.md`](file:///workspace/product/current.md)'s note that "Harbor looked negative."

3. **Telemetry Deduplication & Correction ([`record-47eaba418e`](file:///workspace/product/history/evidence/record-47eaba418e.md)):**
   - **Recorded:** 2026-08-24.
   - **Correction:** Corrected `record-783bf16383` for `record-dc92607ff3` H1 on the identical August 11–17 cohort.
   - **Corrected Metric:** Deduplicated revenue per new account was **+1.8%** with a wide interval spanning harm and benefit (inconclusive).
   - **Finding:** Rollback receipt `record-4cd3618639` remained an actual historical event, and the permission reset bug in recordings was confirmed genuine. The record cautioned: *"Do not label Harbor a demonstrated loss or win."*

4. **Irrelevant Name Overlap Warning ([`record-0f6fbbab4e`](file:///workspace/product/history/evidence/record-0f6fbbab4e.md)):**
   - **Dated:** 2026-09-07.
   - **Context:** Action `record-d3b97d8b03` labeled "Harbor" on **returning desktop accounts** (exposed August 25–31, 2026) showed -3% corrected revenue after billing retry inflation.
   - **Separation:** The record explicitly states: *"The product name overlaps record-dc92607ff3, but this is a different action and population."*

5. **September Design & Defect Fix Proposal ([`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md)):**
   - **Dated:** 2026-09-02.
   - **Change Proposed (Harbor H2):** Persist the user's annual plan selection before the OS permission dialog and restore it upon resume.
   - **QA Verification:** QA record `record-0d1c74ca54` reproduced H1's reset bug and verified it was completely eliminated in H2 across 18 supported-device runs.
   - **Current State:** H2 has not yet been exposed to customers; the underlying revenue hypothesis remains untested.

---

## 3. What the Evidence Supports Now

| Evaluation Dimension | Quiet Return (R7 refreshed) | Harbor (H2 refreshed) | Evidence Sources |
| :--- | :--- | :--- | :--- |
| **Historical Net Revenue** | **-6.2% refund-adjusted revenue** below control (matured ledger complete). | **+1.8% deduplicated revenue per account** (inconclusive; wide confidence interval). | [`record-802325ed36`](file:///workspace/product/history/evidence/record-802325ed36.md), [`record-47eaba418e`](file:///workspace/product/history/evidence/record-47eaba418e.md) |
| **Top-of-Funnel Metric** | +11% trial starts (transient, misleading). | Flawed initial -9% report caused by double-counted resumed sessions in denominator. | [`record-da3a9e962e`](file:///workspace/product/history/evidence/record-da3a9e962e.md), [`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md) |
| **Root Cause of Past Defect** | Structural: 20% renewal discount caused refund requests and post-trial cancellations. | Technical/UX: App reset user plan choice back to default upon OS permission dialog (7/12 sessions). | [`record-b7ab79e22e`](file:///workspace/product/history/retired/summer-offers/actions/record-b7ab79e22e.md), [`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md) |
| **Substance of Refresh** | Superficial: same price, eligibility, and checkout flow; changed only illustration colors. | Functional: persists plan selection across OS permission dialogs; validated in QA (`record-0d1c74ca54`). | [`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md) |
| **Hypothesis Viability** | **Invalidated:** Mature evidence demonstrates economic harm under R7 terms. | **Untested & Promising:** Core hypothesis of annual plan presentation has never been run without the UX defect. | [`record-802325ed36`](file:///workspace/product/history/evidence/record-802325ed36.md), [`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md) |

### Key Analytical Conclusions:
1. **Quiet Return R7 must not be repeated:** The standing scope mandate in [`brief.md`](file:///workspace/product/brief.md) explicitly establishes that *"Refund-adjusted revenue matters more than trial starts."* R7 generated a high volume of signups that subsequently refunded or escalated, reducing net revenue by 6.2%. Because the September proposal makes no changes to pricing, discounting, or eligibility, cosmetic illustration changes cannot overcome this structural deficit.
2. **Harbor's negative reputation in `current.md` was based on obsolete data:** As of the 2026-08-19 handoff, Harbor appeared negative because only `record-783bf16383` was known. The subsequent 2026-08-24 correction ([`record-47eaba418e`](file:///workspace/product/history/evidence/record-47eaba418e.md)) proved Harbor was not a loser, while the design documentation ([`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md)) confirmed the existence and resolution of the critical permission-dialog bug.
3. **Desktop cohort outcomes do not translate to mobile cohorts:** Neither the +4% desktop result for Quiet Return W3 ([`record-3965c8ff16`](file:///workspace/product/history/evidence/record-3965c8ff16.md)) nor the -3% desktop result for Harbor (`record-0f6fbbab4e`) should influence the decision for mobile cohorts.

---

## 4. Next Useful Action

In accordance with standing authority under [`brief.md`](file:///workspace/product/brief.md) (investigate evidence, choose ordinary objectives, and prepare reversible changes within this product, with no live external actions or production mutations authorized in this review snapshot):

1. **Select Objective:** Authorize the preparation of an experiment for **Harbor H2** targeting **new US mobile accounts**.
2. **Instrumentation Specifications Required for H2:**
   - **Telemetry Deduplication Guard:** Implement a persistent account/device token in the experiment analytics harness to prevent resumed application sessions from being logged as new accounts in the denominator (remedying the flaw in [`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md)).
   - **Permission Flow State Telemetry:** Emit explicit telemetry events logging plan selection prior to permission dialog display and verify plan restoration upon app resume to monitor whether the QA fix ([`record-0d1c74ca54`](file:///workspace/product/history/design/record-3c858d6a57.md)) holds under live operating conditions.
   - **Cohort Isolation:** Ensure routing filters strictly target new US mobile accounts, isolating the variant from desktop cohorts or returning subscriber tests.
3. **Required Evidence for Decision:**
   - **Mature Refund-Adjusted Revenue Window:** Run the experiment for a minimum duration that covers the initial billing cycle plus refund maturation (minimum 14–21 days post-exposure), avoiding premature declarations based on trial starts.
   - **Confidence Intervals on Net Revenue:** Pre-specify a sample size capable of distinguishing whether deduplicated revenue per new account exceeds control with statistical precision, resolving the inconclusive wide interval from H1.

---

## 5. Important Uncertainty

1. **Net Revenue Effect of Removing the Reset Friction:** While Harbor H1 achieved +1.8% deduplicated revenue despite the bug, its confidence interval spanned both negative and positive territory. While H2 ensures users who select annual plans actually check out with annual plans, whether new mobile accounts retain these subscriptions or request refunds upon billing is untested.
2. **Live Device / OS Fragmentation:** QA tested H2 across 18 supported devices ([`record-0d1c74ca54`](file:///workspace/product/history/design/record-3c858d6a57.md)). However, edge-case Android memory reclamation or unusual iOS permission dialog lifecycle interruptions under low-memory conditions could still cause unhandled state drops in the wild.
3. **Refund Lag & Ledger Maturation:** Early funnel gains can hide late refunds (as happened with Quiet Return in [`record-802325ed36`](file:///workspace/product/history/evidence/record-802325ed36.md)). Any rollout must retain a rollback safeguard if early chargebacks or refund escalations exceed control thresholds.
4. **Historical Unknown Dates:** In accordance with evidence preservation standards, source records [`record-dc92607ff3`](file:///workspace/product/history/actions/record-dc92607ff3.md) and [`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md) lack year stamps on certain deployment, exposure, and recording dates (e.g., "August 10", "August 18", "August 11–17"). They have been preserved as recorded without inventing missing timestamps.
