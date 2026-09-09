# Revenue Responsibility Decision: Offer Experiment Recommendation

**Date:** 2026-09-09  
**Owner:** Sam, Product Lead  
**Responsibility:** Sustainable Net Subscription Revenue (Active)  
**Workspace Reference:** [`brief.md`](file:///workspace/product/brief.md), [`current.md`](file:///workspace/product/current.md)  

---

## 1. Executive Recommendation

Between the two proposals under consideration:
- **Quiet Return** for returning mobile subscribers: **REJECT**
- **Harbor (H2)** for new mobile accounts: **RECOMMEND FOR NEXT EXPERIMENT**

### Summary Rationale
1. **Quiet Return** variant R7 was already evaluated on returning mobile subscribers ([`record-b7ab79e22e`](file:///workspace/product/history/retired/summer-offers/actions/record-b7ab79e22e.md)). While it initially appeared successful with a +11% increase in trial starts ([`record-da3a9e962e`](file:///workspace/product/history/evidence/record-da3a9e962e.md)), mature settlement data incorporating complete refunds revealed that refund-adjusted net revenue was **-6.2% below control** ([`record-802325ed36`](file:///workspace/product/history/evidence/record-802325ed36.md)). Design's refreshed proposal ([`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md)) merely alters illustration colors while retaining the identical 20% discount, eligibility, and mobile checkout flow. Per [`brief.md`](file:///workspace/product/brief.md), refund-adjusted revenue matters more than trial starts. A cosmetic color change fails to address the demonstrated unit economic deficit.
2. **Harbor** variant H1 on new mobile accounts ([`record-dc92607ff3`](file:///workspace/product/history/actions/record-dc92607ff3.md)) was initially considered negative at -9% ([`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md)). However, subsequent audit corrected a telemetry defect (duplicate counting of resumed sessions), revising deduplicated revenue per new account to **+1.8%** ([`record-47eaba418e`](file:///workspace/product/history/evidence/record-47eaba418e.md)). The real failure was an identified interaction bug: in 7 of 12 reviewed sessions, the user's selected annual plan reset to default when returning from the OS permission dialog. Design's refreshed Harbor H2 proposal ([`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md)) directly fixes this mechanism by persisting selection across the permission dialog. This fix has been validated across 18 test device runs in QA ([`record-0d1c74ca54`](file:///workspace/product/history/design/record-3c858d6a57.md)), leaving the fundamental revenue hypothesis untested on a clean implementation.

---

## 2. Relevant Prior Actions

All historical records cited below are drawn from the local snapshot. Dates and time strings are preserved exactly as recorded in the original source files without inventing missing components.

### A. Quiet Return (Returning Mobile Subscribers)
- **Source Action:** [`history/retired/summer-offers/actions/record-b7ab79e22e.md`](file:///workspace/product/history/retired/summer-offers/actions/record-b7ab79e22e.md)
  - **Aliases:** QR7; returning mobile offer; Quiet Offer.
  - **Originating Context:** Retired responsibility `summer-offers` (terminated 2026-07-30 per [`history/retired/summer-offers/brief.md`](file:///workspace/product/history/retired/summer-offers/brief.md)).
  - **Target Cohort:** US returning iOS annual subscribers.
  - **Intervention:** Variant R7 offering a 20% annual renewal discount.
  - **Deployment:** 2026-07-12 under rollout receipt `record-e4142b048e` at 50% exposure.
  - **Observation Window:** July 13–19 (*year omitted in original record*).
  - **Rollback:** 2026-07-21 under receipt `record-e0da7df86e` due to unresolved refund escalations.

### B. Harbor (New Mobile Accounts)
- **Source Action:** [`history/actions/record-dc92607ff3.md`](file:///workspace/product/history/actions/record-dc92607ff3.md)
  - **Aliases:** Anchor plan picker; annual card; Harbor H1.
  - **Target Cohort:** New US mobile accounts.
  - **Deployment:** August 10 (*year omitted in original record*) under rollout receipt `record-eb44fddf46`.
  - **Observation Window:** August 11–17 (*year omitted in original record*).
  - **Rollback:** August 18 (*year omitted in original record*) under rollback receipt `record-4cd3618639`.

---

## 3. What the Evidence Supports Now

### A. Quiet Return: Trial Spike Masked Severe Net Revenue Decline
- **Initial Funnel Reading:** [`history/evidence/record-da3a9e962e.md`](file:///workspace/product/history/evidence/record-da3a9e962e.md), recorded 2026-07-20, reported trial starts at +11% for `record-b7ab79e22e` R7 during July 13–19 (*year omitted in record*). Retained net revenue had not yet matured. This immature readout led to the interim statement in [`current.md`](file:///workspace/product/current.md) (written 2026-08-19) that "Quiet Return looked like a win before the summer cleanup."
- **Mature Ledger Correction:** [`history/evidence/record-802325ed36.md`](file:///workspace/product/history/evidence/record-802325ed36.md), recorded 2026-08-04, re-evaluated the July 13–19 exposures once refund data matured through August 2 (*year omitted in record*). While trial starts remained +11%, **refund-adjusted net revenue fell to 6.2% below control (-6.2%)**. The matched ledger is complete. The record concluded: *"No price or eligibility changes justify repeating R7 in this cohort."*
- **The Design Refresh:** [`history/design/record-3c858d6a57.md`](file:///workspace/product/history/design/record-3c858d6a57.md), dated 2026-09-02, specifies: *"Quiet Return proposal: same R7 price, eligibility, and mobile checkout; illustration colors changed."* Because the pricing economics (20% discount) and checkout mechanics are identical, the -6.2% refund deficit would almost certainly recur.
- **Disambiguation of Name Collision:** [`history/evidence/record-3965c8ff16.md`](file:///workspace/product/history/evidence/record-3965c8ff16.md), recorded 2026-09-06, shows a net revenue estimate of +4% for a test reusing the name "Quiet Return." However, that record explicitly clarifies that it applies only to US returning desktop monthly subscribers (variant W3, action `record-cf96fad305`, August 20–27; *year omitted in record*) and explicitly states: *"This report does not cover record-b7ab79e22e, R7, returning iOS annual subscribers, or July exposures."* It cannot be used to justify a mobile offer experiment.

### B. Harbor: Initial Loss Was an Artifact of Telemetry and UX Reset Defect
- **Initial Telemetry Defect:** [`history/evidence/record-783bf16383.md`](file:///workspace/product/history/evidence/record-783bf16383.md), recorded August 18 (*year omitted in record*), reported -9% revenue per new account for `record-dc92607ff3` H1 on new US mobile accounts exposed August 11–17 (*year omitted in record*). This led to the notation in [`current.md`](file:///workspace/product/current.md) that "Harbor looked negative." Crucially, the record noted that resumed sessions were counted twice and that 7 of 12 reviewed session recordings exhibited a plan selection reset following the OS permission dialog.
- **Deduplicated Correction:** [`history/evidence/record-47eaba418e.md`](file:///workspace/product/history/evidence/record-47eaba418e.md), recorded 2026-08-24, corrected the double-counting error for the August 11–17 window. Deduplicated revenue per new account was **+1.8%** with a wide confidence interval spanning harm and benefit (inconclusive). The record emphasized that the OS permission reset was real and cautioned: *"Do not label Harbor a demonstrated loss or win."*
- **The Design H2 Refresh and QA Fix:** [`history/design/record-3c858d6a57.md`](file:///workspace/product/history/design/record-3c858d6a57.md), dated 2026-09-02, specifies: *"Harbor H2 proposal: persist the annual selection before the permission dialog, restoring it on resume."* QA run `record-0d1c74ca54` (*date omitted in source record*) successfully reproduced the H1 reset and confirmed it was completely absent in H2 across 18 supported-device test runs. H2 has never been exposed to customers, leaving the underlying revenue hypothesis clean and untested.
- **Disambiguation of Name Collision:** [`history/evidence/record-0f6fbbab4e.md`](file:///workspace/product/history/evidence/record-0f6fbbab4e.md), dated 2026-09-07, reported -3% revenue for Harbor on returning desktop accounts (`record-d3b97d8b03`, August 25–31; *year omitted in record*) due to billing retries. The source explicitly states: *"The product name overlaps record-dc92607ff3, but this is a different action and population."* It does not apply to new mobile accounts.

---

## 4. The Next Useful Action

1. **Authorize Preparation for Harbor H2 on New Mobile Accounts:**
   - Focus the single authorized experiment on **Harbor H2** targeting new US mobile accounts (the population from [`record-dc92607ff3`](file:///workspace/product/history/actions/record-dc92607ff3.md) and [`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md)).
   - Formalize the experiment design, ensuring the pre-dialog annual plan state persistence tested in QA [`record-0d1c74ca54`](file:///workspace/product/history/design/record-3c858d6a57.md) is fully specified for production staging.
2. **Implement Telemetry Guardrails Prior to Exposure:**
   - Implement deduplicated session logging in the client and data ingestion pipeline to prevent the resumed-session double-counting bug identified in [`record-783bf16383`](file:///workspace/product/history/evidence/record-783bf16383.md) and [`record-47eaba418e`](file:///workspace/product/history/evidence/record-47eaba418e.md).
3. **Establish Reversible Deployment & Guardrail Controls:**
   - Define explicit rollback criteria and automated triggers (e.g., elevated checkout error rates, unexpected drop-offs at the OS permission prompt, or excessive early refund requests).
   - In accordance with [`brief.md`](file:///workspace/product/brief.md) standing authority, keep the change reversible.
   - *Operational boundary:* No live production mutations, schedules, or external messages are authorized directly within this snapshot. The next action within this product responsibility is submitting this formal recommendation to Sam and preparing the staging configuration.

---

## 5. Next Evidence Needed

To validate Harbor H2 and determine whether it delivers sustainable net revenue, the following evidence must be collected:

1. **Primary Decision Metric: Mature Refund-Adjusted Net Revenue**
   - Measure settled payments minus refunds and chargebacks attributed to the exposed cohort per account.
   - **Maturity Window:** Require a minimum observation window of 14–21 days post-exposure before rendering a final decision. As proven by the Quiet Return retrospective ([`record-802325ed36`](file:///workspace/product/history/evidence/record-802325ed36.md)), early funnel conversion and trial starts can be deeply misleading until refund requests fully mature.
2. **Mechanism Verification (Leading Funnel Indicator)**
   - Production telemetry tracking annual selection retention through the OS permission prompt. Verify 0% unintentional resets back to default plans across all production device configurations, replicating the lab results from [`record-0d1c74ca54`](file:///workspace/product/history/design/record-3c858d6a57.md).
3. **Session Deduplication Validation**
   - Telemetry audit comparing raw event counts against deduplicated user accounts to ensure resumed sessions are counted exactly once.
4. **Statistical Power & Sample Size**
   - Adequate sample enrollment to resolve the wide confidence interval observed in H1 (+1.8% inconclusive in [`record-47eaba418e`](file:///workspace/product/history/evidence/record-47eaba418e.md)), establishing whether H2 provides a statistically significant positive net revenue lift over control.

---

## 6. Important Uncertainties

1. **Untested Revenue Hypothesis:** While QA [`record-0d1c74ca54`](file:///workspace/product/history/design/record-3c858d6a57.md) proved the selection reset defect is fixed mechanically, the economic hypothesis itself has never been tested in production without the confounding bug ([`record-3c858d6a57`](file:///workspace/product/history/design/record-3c858d6a57.md)). It is possible that fixing the reset does not generate significant incremental annual adoption or that users actively prefer a monthly plan when explicitly prompted.
2. **Refund and Retention Lag:** Net revenue cannot be verified at point of checkout. Early positive conversion may be diluted or reversed if newly enrolled mobile annual subscribers experience post-purchase remorse or request refunds at higher rates.
3. **Device / OS Fragmentation:** QA tested 18 supported devices, but production mobile fleets have diverse Android OS versions, OEM battery-management interventions, and iOS dialog lifecycle behaviors that could introduce edge-case lifecycle interrupts during permission requests.
4. **Telemetry Ingestion Stability:** Deduplication logic must be robust to intermittent network drops and resumed background sessions to prevent data contamination during initial rollout.
5. **No Live Execution Authority:** Under the scope defined in [`brief.md`](file:///workspace/product/brief.md), this review is strictly limited to the local snapshot. Live deployments, scheduling, or production changes must be authorized and executed through designated release processes.
