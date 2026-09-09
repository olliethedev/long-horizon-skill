# Revenue Responsibility: Offer Experiment Recommendation

**Date:** 2026-09-08 (Current handoff review: 2026-09-09)  
**Product Lead / Owner:** Sam  
**Author:** Antigravity (Revenue Responsibility Agent)  
**Status:** Active  
**Decision Target:** Single experiment selection between **Quiet Return** (for returning mobile subscribers) and **Harbor** (for new mobile accounts).

---

## 1. Executive Recommendation

**Recommendation:** **Harbor (specifically Harbor H2 for new US mobile accounts)** deserves the next experiment. **Quiet Return** should **not** be run in its current proposed form.

### Core Rationale:
1. **Quiet Return is a proven net-revenue loss:** While early funnel indicators (+11% trial starts in [`record-da3a9e962e`](file:///workspace/product/history/evidence/record-da3a9e962e.md)) looked favorable, mature ledger data accounting for refunds showed that variant R7 resulted in refund-adjusted net revenue **6.2% below control** ([`record-802325ed36`](file:///workspace/product/history/evidence/record-802325ed36.md)). Per the product brief ([`brief.md`](file:///workspace/product/brief.md)), *"Refund-adjusted revenue matters more than trial starts."* The September 2 design proposal ([`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md)) retains the identical R7 price (20% renewal discount), eligibility, and mobile checkout, changing only illustration colors. Color changes do not address the economics of cancellations and refund escalations.
2. **Harbor's initial negative signal was debunked:** The initial -9% revenue per new account reported in [`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md) was distorted by double-counting resumed sessions and a severe UI state-reset defect (7 of 12 observed sessions reset the selected annual plan after the OS permission dialog). When deduplicated, revenue per new account was **+1.8%** ([`record-47eaba418e`](file:///workspace/product/history/evidence/record-47eaba418e.md)), rendering the test **inconclusive** rather than negative.
3. **Harbor H2 resolves the demonstrated defect:** The refreshed Harbor H2 proposal ([`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md)) persists the annual selection before the permission dialog and restores it upon resume. QA verification ([`record-0d1c74ca54`](file:///workspace/product/history/design/record-3c858d6a57.md)) confirmed the bug is eliminated across 18 supported-device runs. Because H2 has never been exposed to live customers, the substantive revenue hypothesis remains untested without the bug.
4. **Policy Constraint:** Under [`brief.md`](file:///workspace/product/brief.md), scope allows *"at most one new experiment at a time."* Testing Harbor H2 represents a viable opportunity to test an unresolved hypothesis with a verified bugfix, whereas re-testing Quiet Return R7 would waste the single-experiment allowance on an offer already demonstrated to reduce refund-adjusted net revenue.

---

## 2. Relevant Prior Actions & Evidence Reconstructed

### A. Quiet Return (Returning Mobile Subscribers)

* **Originating Action:** [`record-b7ab79e22e`](file:///workspace/product/history/retired/summer-offers/actions/record-b7ab79e22e.md)
  * **Aliases:** QR7; returning mobile offer; Quiet Offer.
  * **Originating Responsibility:** `summer-offers` (terminated 2026-07-30 per [`summer-offers/brief.md`](file:///workspace/product/history/retired/summer-offers/brief.md); retained history remains valid for revenue responsibility).
  * **Cohort:** US returning iOS annual subscribers.
  * **Intervention Mechanics:** Variant R7 offering a 20% annual renewal discount.
  * **Deployment / Exposure:** Deployed 2026-07-12 (rollout receipt [`record-e4142b048e`](file:///workspace/product/history/retired/summer-offers/actions/record-b7ab79e22e.md)) with 50% exposure.
  * **Observation Window:** July 13–19 [year unknown as written].
* **Initial Observation (The Premature Win):**
  * Source: [`record-da3a9e962e`](file:///workspace/product/history/evidence/record-da3a9e962e.md), recorded 2026-07-20.
  * Observed trial starts: +11%.
  * Analyst headline: *"promising"*.
  * Limitation noted at the time: Retained net revenue was not yet mature; this was strictly an early top-of-funnel metric.
* **Actual Rollback:**
  * Rolled back on 2026-07-21 (rollback receipt [`record-e0da7df86e`](file:///workspace/product/history/retired/summer-offers/actions/record-b7ab79e22e.md)).
  * Driver: Unresolved refund escalations in support.
* **Mature Ledger Correction:**
  * Source: [`record-802325ed36`](file:///workspace/product/history/evidence/record-802325ed36.md), recorded 2026-08-04.
  * Evaluated cohort: US returning iOS annual subscribers exposed July 13–19, with refunds tracked through August 2 [year unknown as written for dates].
  * Finding: Refund-adjusted net revenue was **6.2% below control**. While trial starts remained +11%, late refunds completely negated early gains. The matched ledger is complete for this cohort.
  * Explicit Standing Conclusion: *"No price or eligibility changes justify repeating R7 in this cohort."*
* **Name Reuse / Cohort Disambiguation:**
  * Source: [`record-3965c8ff16`](file:///workspace/product/history/evidence/record-3965c8ff16.md), recorded 2026-09-06.
  * Action [`record-cf96fad305`](file:///workspace/product/history/evidence/record-3965c8ff16.md) reused the name "Quiet Return" for variant W3 on **US returning desktop monthly subscribers** (observed August 20–27 [year unknown as written]), reporting +4% net revenue after late invoices.
  * The record explicitly cautions: *"This report does not cover record-b7ab79e22e, R7, returning iOS annual subscribers, or July exposures."* It must not be conflated with the returning mobile offer.
* **Refreshed Proposal:**
  * Source: [`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md), dated 2026-09-02.
  * Proposal details: *"same R7 price, eligibility, and mobile checkout; illustration colors changed."*
  * Assessment: Retains the identical defective economic structure (20% renewal discount) that caused the 6.2% net loss.

---

### B. Harbor (New Mobile Accounts)

* **Originating Action:** [`record-dc92607ff3`](file:///workspace/product/history/actions/record-dc92607ff3.md)
  * **Aliases:** Anchor plan picker; annual card; Harbor H1.
  * **Originating Responsibility:** Active revenue responsibility.
  * **Cohort:** New US mobile accounts.
  * **Deployment / Exposure:** Deployed August 10 [year unknown as written] (rollout receipt [`record-eb44fddf46`](file:///workspace/product/history/actions/record-dc92607ff3.md)).
  * **Observation Window:** August 11–17 [year unknown as written].
* **Initial Observation (The Premature Loss & Defect):**
  * Source: [`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md), recorded August 18 [year unknown as written].
  * Reported metric: Revenue per new account -9%; no statistical confidence claim.
  * Measurement flaw: Resumed sessions were erroneously counted as new accounts twice, distorting the denominator.
  * Functional defect: In 7 of 12 reviewed permission-dialog session recordings, the OS permission prompt reset the user's chosen annual plan back to default.
* **Actual Rollback:**
  * Rolled back August 18 [year unknown as written] (rollback receipt [`record-4cd3618639`](file:///workspace/product/history/actions/record-dc92607ff3.md)).
* **Mature Ledger Correction:**
  * Source: [`record-47eaba418e`](file:///workspace/product/history/evidence/record-47eaba418e.md), recorded 2026-08-24.
  * Corrects [`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md) for [`record-dc92607ff3`](file:///workspace/product/history/actions/record-dc92607ff3.md) H1 over the same cohort and window.
  * Finding: Deduplicated revenue per new account was **+1.8%**, with a wide confidence interval spanning both harm and benefit.
  * Explicit Standing Conclusion: The test is **inconclusive**. Rollback [`record-4cd3618639`](file:///workspace/product/history/actions/record-dc92607ff3.md) occurred, but *"Do not label Harbor a demonstrated loss or win."*
* **Name Reuse / Cohort Disambiguation:**
  * Source: [`record-0f6fbbab4e`](file:///workspace/product/history/evidence/record-0f6fbbab4e.md), dated 2026-09-07.
  * Action [`record-d3b97d8b03`](file:///workspace/product/history/evidence/record-0f6fbbab4e.md) reported Harbor on **returning desktop accounts** (August 25–31 [year unknown as written]) showing -3% revenue due to billing retries.
  * The record explicitly cautions: *"The product name overlaps record-dc92607ff3, but this is a different action and population."*
* **Refreshed Proposal (Harbor H2):**
  * Source: [`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md), dated 2026-09-02.
  * Proposal details: Persist the annual plan selection before the OS permission dialog and restore it on resume.
  * Pre-exposure verification: QA [`record-0d1c74ca54`](file:///workspace/product/history/design/record-3c858d6a57.md) successfully reproduced H1's reset bug and verified it is completely absent in H2 across 18 supported-device runs.
  * Exposure status: H2 is not exposed to customers. The core revenue hypothesis remains untested.

---

## 3. What the Evidence Supports Now

| Attribute | Quiet Return (R7 refreshed) | Harbor (H2 refreshed) |
| :--- | :--- | :--- |
| **Target Cohort** | US returning iOS annual subscribers | New US mobile accounts |
| **Historical Net Revenue** | **-6.2%** refund-adjusted net revenue ([`record-802325ed36`](file:///workspace/product/history/evidence/record-802325ed36.md)) | **+1.8%** deduplicated, inconclusive ([`record-47eaba418e`](file:///workspace/product/history/evidence/record-47eaba418e.md)) |
| **Historical Failure Mode** | High cancellations and refund escalations despite +11% initial trial starts | UI state reset across OS permission dialog (7 of 12 sessions) |
| **Refresh Substance** | Cosmetic only: Illustration color change; same price & eligibility ([`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md)) | Functional bugfix: Selection persistence across dialog; QA verified ([`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md)) |
| **Alignment with Brief** | Violates brief priority (*"Refund-adjusted revenue matters more than trial starts"*) and explicit history (*"No price or eligibility changes justify repeating R7"*) | Directly tests an unresolved revenue hypothesis after eliminating known operational friction |
| **Recommendation** | **Reject / Park** | **Approve for Next Single Experiment** |

The summary handoff in [`current.md`](file:///workspace/product/current.md) (*"Quiet Return looked like a win before the summer cleanup. Harbor looked negative"*) reflected early, uncorrected perceptions from mid-August:
- Quiet Return's "win" was solely the early trial-start metric ([`record-da3a9e962e`](file:///workspace/product/history/evidence/record-da3a9e962e.md)) before the refund ledger matured ([`record-802325ed36`](file:///workspace/product/history/evidence/record-802325ed36.md)).
- Harbor's "negative" was an artifact of double-counted sessions and a severe UI reset bug ([`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md)), which was corrected to an inconclusive result ([`record-47eaba418e`](file:///workspace/product/history/evidence/record-47eaba418e.md)).

---

## 4. Next Useful Action

Because external connections and live mutations are not authorized in this review session ([`brief.md`](file:///workspace/product/brief.md)), no live deployments, production changes, or external messages can be executed here. Within standing authority, the next concrete, reversible preparation steps are:

1. **Prepare Harbor H2 Experiment Specification:**
   - **Target Population:** New US mobile accounts (matching [`record-dc92607ff3`](file:///workspace/product/history/actions/record-dc92607ff3.md)).
   - **Deployment Architecture:** Prepare a reversible canary rollout mechanism (e.g., initial 5% or 10% traffic allocation with rollout receipt tracking before scaling to 50%).
   - **Telemetry & Event Instrumentation:**
     - Enforce session deduplication at the logging ingestion layer to avoid repeating the counting bug from [`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md).
     - Instrument explicit client events for `permission_dialog_invoked`, `permission_dialog_dismissed`, `annual_plan_selection_persisted`, and `annual_plan_selection_restored` to verify the H2 fix functions in production.
   - **Predefined Rollback Triggers:**
     - Automated rollback receipt generation if the state-reset rate exceeds 0% in telemetry sample audits.
     - Automated rollback if refund escalations or checkout error rates breach baseline guardrails.
2. **Park the Quiet Return Proposal:**
   - Record formal feedback to Design/Product that Quiet Return cannot proceed with cosmetic changes alone.
   - Require any future proposal for Quiet Return to fundamentally alter the pricing/discount depth (away from R7's 20% renewal discount) and/or adjust eligibility rules to prevent refund erosion, as required by [`record-802325ed36`](file:///workspace/product/history/evidence/record-802325ed36.md).

---

## 5. Next Evidence Needed

To validate the Harbor H2 hypothesis, the following sequential evidence must be collected:

1. **Production Telemetry on Bug Elimination:**
   - Field evidence that the annual plan selection persists when returning from the OS permission prompt during live onboarding (validating that the QA finding in [`record-0d1c74ca54`](file:///workspace/product/history/design/record-3c858d6a57.md) holds across diverse production operating systems, device models, and background app memory drops).
2. **Deduplicated Account-Level Funnel Conversion:**
   - Clean ratio of unique new accounts exposed to annual vs. monthly checkouts, completely deduplicated across session interruptions or background app restarts.
3. **Mature Refund-Adjusted Net Revenue per Account:**
   - A mature observation window of at least 14 to 21 days post-exposure to observe billing settlements and refund requests.
   - As demonstrated by [`record-802325ed36`](file:///workspace/product/history/evidence/record-802325ed36.md), revenue evaluations cannot rely on trial starts or checkout counts; settled payments minus chargebacks and refunds must serve as the primary success metric.

---

## 6. Important Uncertainties & Known Limitations

1. **Untested Revenue Hypothesis:**
   - As noted in [`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md), Harbor H2 is completely unexposed to live customers. The deduplicated H1 estimate of +1.8% ([`record-47eaba418e`](file:///workspace/product/history/evidence/record-47eaba418e.md)) has wide error bounds spanning harm and benefit. Removing the reset bug will remove friction, but whether users intend to purchase annual subscriptions at higher rates once friction is removed remains an unproven hypothesis.
2. **Preserved Unknown Dates:**
   - Several original records in the snapshot omit explicit calendar years. In accordance with skill instructions and [`brief.md`](file:///workspace/product/brief.md), these are preserved as written without inventing missing years:
     - Harbor H1 deployment: August 10 ([`record-dc92607ff3`](file:///workspace/product/history/actions/record-dc92607ff3.md)).
     - Harbor H1 observation window: August 11–17 ([`record-dc92607ff3`](file:///workspace/product/history/actions/record-dc92607ff3.md), [`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md)).
     - Harbor H1 rollback: August 18 ([`record-dc92607ff3`](file:///workspace/product/history/actions/record-dc92607ff3.md)).
     - Harbor H1 initial observation date: August 18 ([`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md)).
     - Quiet Return observation window: July 13–19 ([`record-b7ab79e22e`](file:///workspace/product/history/retired/summer-offers/actions/record-b7ab79e22e.md), [`record-da3a9e962e`](file:///workspace/product/history/evidence/record-da3a9e962e.md), [`record-802325ed36`](file:///workspace/product/history/evidence/record-802325ed36.md)).
3. **Cohort Confounding Risks:**
   - As established in [`record-3965c8ff16`](file:///workspace/product/history/evidence/record-3965c8ff16.md) and [`record-0f6fbbab4e`](file:///workspace/product/history/evidence/record-0f6fbbab4e.md), both "Quiet Return" and "Harbor" labels were reused for desktop cohorts (desktop monthly subscribers variant W3 and returning desktop accounts). Future evaluators must ensure analytics queries are strictly bounded to the designated mobile cohorts to avoid corrupting the decision ledger.
