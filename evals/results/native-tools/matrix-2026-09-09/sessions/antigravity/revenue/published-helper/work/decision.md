# Revenue Experiment Recommendation: Harbor (H2) vs. Quiet Return

**Date:** 2026-09-09  
**Reviewing Context:** Product Lead Brief dated 2026-09-08 (`brief.md`)  
**Handoff Reference:** `current.md` (written 2026-08-19)  
**Target Product / Responsibility:** Revenue responsibility (/workspace/product)  
**Status / Decision:** Recommended: Harbor H2 for new mobile accounts; Rejected: Quiet Return R7 for returning mobile subscribers.

---

## 1. Executive Summary & Recommendation

In accordance with the product brief (`brief.md`) to improve sustainable net subscription revenue while running at most one experiment at a time, this review evaluates the two proposed offer concepts:
1. **Quiet Return** for returning mobile subscribers
2. **Harbor** for new mobile accounts

**Recommendation:** **Harbor (specifically variant H2)** deserves the next experiment. **Quiet Return does not.**

### Rationale Summary
- **Quiet Return for mobile subscribers** has already been tested as variant R7 (`record-b7ab79e22e`). While initial funnel metrics appeared positive (+11% trial starts in `record-da3a9e962e`), mature ledger evidence accounting for refund escalations revealed that net revenue was **6.2% below control** (`record-802325ed36`). The September design proposal (`record-3c858d6a57`) keeps the exact same R7 price, eligibility, and mobile checkout, changing only illustration colors. Because refund-adjusted revenue matters more than trial starts (`brief.md`), cosmetic artwork changes do not justify repeating an economically negative offer. (A recent +4% win in `record-3965c8ff16` pertained strictly to desktop monthly subscribers on variant W3 and explicitly excluded mobile iOS annual R7).
- **Harbor for new mobile accounts** was initially perceived as negative (-9% revenue per new account in `record-783bf16383`), which prompted its rollback. However, a subsequent correction (`record-47eaba418e`) demonstrated that the -9% figure was distorted by a double-counting telemetry error; deduplicated revenue per new account was **+1.8% (inconclusive)**. Crucially, session recordings confirmed that 7 of 12 permission-dialog sessions accidentally reset the user's selected annual plan (`record-783bf16383`). The Harbor H2 proposal (`record-3c858d6a57`) directly fixes this defect by persisting the annual selection across the OS dialog, verified in QA across 18 device runs (`record-0d1c74ca54`). With the root-cause bug resolved and the core revenue hypothesis untested under clean conditions, Harbor H2 is the only proposal with a viable path to sustainable net revenue.

---

## 2. Relevant Prior Actions & Evidence Analysis

### A. Quiet Return (Returning Mobile Subscribers)

1. **Prior Action & Cohort:**
   - **Source Path:** `history/retired/summer-offers/actions/record-b7ab79e22e.md`
   - **Source ID:** `record-b7ab79e22e`
   - **Aliases:** QR7, returning mobile offer, Quiet Offer.
   - **Originating Responsibility:** `summer-offers` (terminated 2026-07-30 per `history/retired/summer-offers/brief.md`; history retained for revenue responsibility).
   - **Target Cohort:** US returning iOS annual subscribers.
   - **Intervention:** Variant R7 offering a 20% annual renewal discount.
   - **Deployment & Exposure:** Deployed 2026-07-12 via rollout `record-e4142b048e` at 50% exposure. Observation window: July 13–19 *(year unstated in record)*.
   - **Rollback:** Rolled back 2026-07-21, receipt `record-e0da7df86e`, due to unresolved refund escalations.

2. **Early Observation:**
   - **Source Path:** `history/evidence/record-da3a9e962e.md`
   - **Source ID:** `record-da3a9e962e` (recorded 2026-07-20).
   - **Reported Metric:** Trial starts +11%; retained-net-revenue not yet mature. Headline labeled "promising".
   - **Analysis:** This early funnel metric created the initial perception recorded in `current.md` that "Quiet Return looked like a win before the summer cleanup."

3. **Subsequent Correction & Mature Evidence:**
   - **Source Path:** `history/evidence/record-802325ed36.md`
   - **Source ID:** `record-802325ed36` (recorded 2026-08-04).
   - **Scope & Ledger:** Revises `record-da3a9e962e` for `record-b7ab79e22e` R7 (US returning iOS annual subscribers, July 13–19 exposures *(year unstated)* with refunds tracked through August 2 *(year unstated)*). Matched ledger complete.
   - **Observed Result:** Refund-adjusted net revenue was **6.2% below control**. While trial starts remained +11%, post-trial cancellations and refund escalations erased all initial gains.
   - **Historical Disposition:** Explicitly concludes: *"No price or eligibility changes justify repeating R7 in this cohort."*

4. **Name Reuse / Cohort Distinction:**
   - **Source Path:** `history/evidence/record-3965c8ff16.md`
   - **Source ID:** `record-3965c8ff16` (recorded 2026-09-06).
   - **Scope:** Corrects a test under the reused name "Quiet Return" by action `record-cf96fad305` for US returning desktop monthly subscribers (variant W3, August 20–27 *(year unstated)*), showing +4% net revenue after late invoices.
   - **Limitation:** The record explicitly states: *"This report does not cover record-b7ab79e22e, R7, returning iOS annual subscribers, or July exposures."* This positive result cannot be applied to mobile subscribers.

5. **Current Proposal Evaluation:**
   - **Source Path:** `history/design/record-3c858d6a57.md`
   - **Source ID:** `record-3c858d6a57` (dated 2026-09-02).
   - **Design Content:** *"Quiet Return proposal: same R7 price, eligibility, and mobile checkout; illustration colors changed."*
   - **Assessment:** Changing illustration colors does not alter offer economics, discount rate (20%), or checkout friction. It does nothing to mitigate the refund escalations that caused the -6.2% net revenue deficit.

---

### B. Harbor (New Mobile Accounts)

1. **Prior Action & Cohort:**
   - **Source Path:** `history/actions/record-dc92607ff3.md`
   - **Source ID:** `record-dc92607ff3`
   - **Aliases:** Anchor plan picker, annual card, Harbor H1.
   - **Target Cohort:** New US mobile accounts.
   - **Deployment & Exposure:** Deployed August 10 *(year unstated in record)*, rollout `record-eb44fddf46`. Observed August 11–17 *(year unstated)*.
   - **Rollback:** Rolled back August 18 *(year unstated)*, receipt `record-4cd3618639`.

2. **Early Observation:**
   - **Source Path:** `history/evidence/record-783bf16383.md`
   - **Source ID:** `record-783bf16383` (recorded August 18 *(year unstated)*).
   - **Reported Metric:** Revenue per new account initially reported at -9% (no confidence claim).
   - **Identified Defects:**
     1. *Instrumentation flaw:* Resumed sessions were counted as new accounts twice, artificially deflating per-account revenue.
     2. *User experience bug:* 7 of 12 reviewed permission-dialog sessions reset the user's chosen annual plan back to default.
   - **Analysis:** This preliminary report created the negative impression cited in `current.md` ("Harbor looked negative").

3. **Subsequent Correction & Re-analysis:**
   - **Source Path:** `history/evidence/record-47eaba418e.md`
   - **Source ID:** `record-47eaba418e` (recorded 2026-08-24).
   - **Scope:** Corrects `record-783bf16383` for `record-dc92607ff3` H1 on the same cohort and exposure window.
   - **Observed Result:** Deduplicated revenue per new account was **+1.8%**, with a wide confidence interval spanning both harm and benefit (inconclusive).
   - **Key Finding:** The test was not a confirmed negative. The plan reset behavior in session recordings was real and severely compromised annual plan conversions. Guidance specifies: *"Do not label Harbor a demonstrated loss or win."*

4. **Current Proposal & Verification:**
   - **Source Path:** `history/design/record-3c858d6a57.md`
   - **Source ID:** `record-3c858d6a57` (dated 2026-09-02).
   - **Proposal Details:** Harbor H2 persists the user's annual plan selection before the OS permission dialog and restores it upon resume.
   - **Pre-deployment Verification:** QA `record-0d1c74ca54` reproduced H1's plan reset and confirmed it is completely absent in H2 across 18 supported-device test runs.
   - **Current State:** H2 has not yet been exposed to live customers; the revenue hypothesis remains untested under bug-free conditions.

---

## 3. What the Evidence Supports Now

| Evaluation Dimension | Quiet Return (R7 refreshed) | Harbor (H2) |
| :--- | :--- | :--- |
| **Target Population** | US returning mobile (iOS) annual subscribers | New US mobile accounts |
| **Historical Net Revenue** | **-6.2% below control** (`record-802325ed36`, mature refund ledger) | **+1.8%** (`record-47eaba418e`, inconclusive wide interval) |
| **Flaw in Prior Run** | Refund escalations and cancellations post-trial | UI plan reset bug (7 of 12 sessions) + telemetry double counting |
| **Nature of Design Refresh** | Superficial (illustration colors changed only; identical R7 price/terms) | Structural bug fix (persists plan choice across OS permission dialog) |
| **Verification of Refresh** | None (cosmetic only; underlying economics unchanged) | Verified in QA across 18 device runs (`record-0d1c74ca54`) |
| **Alignment with Brief** | Violates mandate (prior run had -6.2% refund-adjusted revenue) | Aligns with mandate (tests clean revenue hypothesis for new accounts) |
| **Recommendation** | **Reject** | **Approve for Next Experiment** |

The evidence clearly establishes that:
1. Quiet Return R7 was not a true win. The perception in `current.md` was based on early trial start counts (`record-da3a9e962e`), which were overturned once refund ledgers matured (`record-802325ed36`). Repackaging R7 with new illustration colors without altering pricing, eligibility, or terms cannot reasonably be expected to fix customer refund escalations.
2. Harbor H1 was never proven to be a loss. The -9% decline was an un-deduplicated artifact, and H1 suffered from a severe friction point where more than half of reviewed users had their annual selection wiped out during onboarding.
3. Harbor H2 removes that friction point, has passed device QA, and represents a legitimate, unconfounded test of the annual card / anchor plan picker hypothesis.

---

## 4. Next Useful Action

Within the standing authority granted in `brief.md` (investigating evidence, choosing ordinary objectives, and preparing reversible changes within the product, with live mutations reserved), the recommended next action is:

**Prepare a reversible, controlled A/B experiment for Harbor H2 on New US Mobile Accounts.**

### Next Evidence Required
Before and during the rollout of Harbor H2, the following specific evidence must be collected:
1. **Telemetry & Deduplication Verification (Pre-Flight):**
   - Verify that the analytics event pipeline correctly deduplicates resumed onboarding sessions so that accounts are not double-counted (preventing recurrence of the error in `record-783bf16383`).
2. **In-Flight Plan Persistence Telemetry (Production Exposure):**
   - Instrument an explicit metric tracking whether the annual plan selection remains active following the OS permission dialog in production sessions to confirm the QA result (`record-0d1c74ca54`) holds across real customer devices.
3. **Controlled Rollout & Receipts:**
   - Define a controlled exposure split (e.g., 50% exposure to new US mobile accounts) with recorded rollout and rollback receipts.
4. **Matured Metric Observation Window:**
   - Observe the experiment for a minimum 7–14 day exposure window, followed by a dedicated observation window for billing and refund maturation (at least 14–21 days post-exposure) before declaring success, guarding against premature conclusions as seen in `record-802325ed36`.
   - Measure: Deduplicated revenue per new account, annual plan conversion rate, 30-day refund rate, and net subscription revenue.
5. **Customer Support Escalation Monitoring:**
   - Track incoming support tags (`history/support`) to identify any permission dialog lockups, unexpected plan toggles, or checkout confusion.

---

## 5. Important Uncertainty & Risk Considerations

1. **Customer Exposure Uncertainty:**
   - Harbor H2 has never been exposed to live customers (`record-3c858d6a57`). While QA `record-0d1c74ca54` validated the fix on 18 test devices, real-world Android and iOS device fragmentation could introduce unforeseen edge cases with the permission dialog.
2. **Revenue Hypothesis Uncertainty:**
   - Because the deduplicated H1 result (+1.8%) had a wide interval spanning harm and benefit (`record-47eaba418e`), it is uncertain whether persisting the annual plan picker will drive a statistically significant increase in net revenue or whether user resistance to annual commitments on mobile will dominate.
3. **Refund and Retention Maturation Lag:**
   - Upfront subscription commitments carry refund risk. As demonstrated by Quiet Return R7, initial signups do not equal sustainable net revenue. The true net revenue outcome of Harbor H2 cannot be determined until refund windows close.
4. **Preservation of Unknown Dates:**
   - Historical records `history/actions/record-dc92607ff3.md`, `history/evidence/record-783bf16383.md`, and others omit calendar years for certain deployment and observation dates (e.g., "August 10", "August 18", "August 11–17", "July 13–19", "August 2"). In accordance with standing instructions, these dates must be treated as having unknown years and not assumed.

---

## 6. Primary Evidence Index

| Source ID | Source Path | Date as Recorded | Subject / Cohort | Key Finding |
| :--- | :--- | :--- | :--- | :--- |
| `brief.md` | `brief.md` | 2026-09-08 | Revenue responsibility | Net subscription revenue scope; refund-adjusted revenue > trial starts; max 1 experiment. |
| `current.md` | `current.md` | 2026-08-19 | Handoff summary | Stale summary noting Quiet Return looked like a win and Harbor looked negative. |
| `record-b7ab79e22e` | `history/retired/summer-offers/actions/record-b7ab79e22e.md` | Deployed 2026-07-12; rolled back 2026-07-21 | Quiet Return R7 (US returning iOS annual) | 50% exposure July 13–19 *(year unstated)*; rolled back due to unresolved refund escalations. |
| `record-da3a9e962e` | `history/evidence/record-da3a9e962e.md` | Recorded 2026-07-20 | Quiet Return R7 (July 13–19) | Initial funnel metric: trial starts +11%; net revenue immature. |
| `record-802325ed36` | `history/evidence/record-802325ed36.md` | Recorded 2026-08-04 | Quiet Return R7 correction | Refund-adjusted net revenue was -6.2% below control; repeating R7 unjustified. |
| `record-3965c8ff16` | `history/evidence/record-3965c8ff16.md` | Recorded 2026-09-06 | Quiet Return W3 name reuse | Desktop monthly cohort +4% net revenue; explicitly does not cover mobile R7. |
| `record-dc92607ff3` | `history/actions/record-dc92607ff3.md` | Deployed Aug 10; rolled back Aug 18 *(years unstated)* | Harbor H1 (New US mobile accounts) | Deployed Aug 10, rolled back Aug 18; initial -9% revenue report and permission reset bug. |
| `record-783bf16383` | `history/evidence/record-783bf16383.md` | Recorded August 18 *(year unstated)* | Harbor H1 observation | Reported -9% revenue; double-counted resumed sessions; 7 of 12 sessions reset annual choice. |
| `record-47eaba418e` | `history/evidence/record-47eaba418e.md` | Recorded 2026-08-24 | Harbor H1 correction | Deduplicated revenue is +1.8% (inconclusive); reset bug confirmed real; neither loss nor win. |
| `record-3c858d6a57` | `history/design/record-3c858d6a57.md` | Dated 2026-09-02 | Offer proposals (Quiet Return & Harbor H2) | Quiet Return only changed colors (same R7); Harbor H2 fixes reset bug (tested in QA record-0d1c74ca54). |
| `record-0d1c74ca54` | Cited in `record-3c858d6a57.md` | Unknown *(prior to 2026-09-02)* | Harbor H2 QA | Confirmed absence of permission dialog reset across 18 test device runs. |
