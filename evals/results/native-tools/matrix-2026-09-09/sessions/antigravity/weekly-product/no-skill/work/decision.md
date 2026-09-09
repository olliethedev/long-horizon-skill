# Product Decision: Next Onboarding Improvement

**Date:** 2026-09-08  
**Author:** Product Lead Review (Sam / Antigravity)  
**Status:** Decided  
**Active Brief:** [brief.md](file:///workspace/product/brief.md)  
**Current Handoff:** [current.md](file:///workspace/product/current.md)  

---

## 1. Executive Recommendation

Between the two requests in this week's feedback export ([record-0131162d69.md](file:///workspace/product/history/support/record-0131162d69.md)), **mobile status filters** is selected as the next onboarding improvement to advance this week.

* **Selected Action:** Advance the existing draft mobile status filter component ([record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md)) into a reversible, small-workspace rollout focused on mobile onboarding friction (e.g., filtering tasks by "waiting" on phone).
* **Rejected Alternative:** Do not undertake the quieter digest request. The underlying initiative ([Sunday Room](file:///workspace/product/history/retired/notification-reset/actions/record-8f6b82ec51.md)) belonged to the bounded responsibility `notification-reset` ([brief.md](file:///workspace/product/history/retired/notification-reset/brief.md)), which was officially terminated on July 31. Under standing product authority ([brief.md](file:///workspace/product/brief.md)), terminated responsibilities must not be resumed. Furthermore, the feedback ticket reflects legacy contributor preference overrides in an established 280-person organization, not onboarding friction, and its submission date is unknown.

---

## 2. Review of This Week's Feedback

Source file: [history/support/record-0131162d69.md](file:///workspace/product/history/support/record-0131162d69.md) (Retrieved 2026-09-07)

1. **Ticket record-e36f0fe1aa**
   * **Submitted:** 2026-09-05
   * **User/Cohort:** Solo owner on Android 15, workspace with 34 tasks.
   * **Reported Problem:** *"On desktop I can narrow to waiting, but on my phone I have to scroll through everything."*
   * **Onboarding Relevance:** Directly in scope. A newly onboarded solo workspace owner managing 34 tasks faces immediate friction transitioning between desktop and mobile.
2. **Ticket record-5f1a34c149**
   * **Submitted:** `unknown` *(date preserved as unknown)*
   * **User/Cohort:** Contributor in a 280-person EU team, client web 6.8.
   * **Reported Problem:** *"The quiet digest still pings me every evening. I only need the weekly note."*
   * **Metadata Note:** The connector supplies `age_days=20`, which is defined as days since the digest release, not ticket age.
   * **Onboarding Relevance:** Out of scope. The user is an established contributor in a large enterprise team using web 6.8, not an onboarding user.

---

## 3. Relevant Prior Actions: What We Have Already Tried

### Track A: Status Filters / Focus Shelf
* **May 14, 2026 — Initial Focus Shelf Rollout:**
  * Source: [history/actions/record-ecc0d14c71.md](file:///workspace/product/history/actions/record-ecc0d14c71.md)
  * Action ID: `record-ecc0d14c71` (internal name `record-e9d336d487`; aliases: triage facets, status filters).
  * Deployment receipt: `record-226210156c`.
  * Scope: Deployed to enterprise desktop accounts only. Android and iOS were excluded.
* **June 2, 2026 — Desktop Rollback:**
  * Source: [history/actions/record-ecc0d14c71.md](file:///workspace/product/history/actions/record-ecc0d14c71.md)
  * Rollback receipt: `record-929bef0cdc`.
  * Trigger: Severe count-query latency in workspaces exceeding 50,000 tasks.
* **August 30, 2026 — Desktop Status Filter Rollout:**
  * Source: [history/releases/record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md)
  * Action IDs: `record-40440b02ae`, `record-3984af46e2`.
  * Deployment receipt: `record-764afbf446`.
  * Architecture change: Count queries were rebuilt to be asynchronous, resolving the latency bottleneck. Desktop small-workspace smoke checks passed.
  * Mobile state: Mobile clients remained on the legacy unfiltered list with no filter control; the mobile component was left in draft form.

### Track B: Quieter Digest / Sunday Room
* **July 12, 2026 — Sunday Room Deployment:**
  * Source: [history/retired/notification-reset/actions/record-8f6b82ec51.md](file:///workspace/product/history/retired/notification-reset/actions/record-8f6b82ec51.md)
  * Action ID: `record-8f6b82ec51` (aliases: quiet digest, weekly note).
  * Deployment receipt: `record-d4f34a4dc1`.
  * Scope: Workspace administrators were enabled to configure weekly instead of daily email digests ("team digest"). Contributor-level legacy daily subscriptions were deliberately not migrated.
* **July 31, 2026 — Responsibility Termination:**
  * Source: [history/retired/notification-reset/brief.md](file:///workspace/product/history/retired/notification-reset/brief.md)
  * The bounded responsibility `notification-reset` was officially terminated after preference migration.

---

## 4. What Actually Happened & What the Evidence Supports Now

### A. Correction of Assumptions in current.md
The handoff note in [current.md](file:///workspace/product/current.md) (written 2026-08-20) made two assumptions that the evidence disproves or clarifies:

1. **Assumption:** *"Focus Shelf was shelved after low use."*
   * **Reality:** The initial May 29 report ([record-8a2203deaa.md](file:///workspace/product/history/evidence/record-8a2203deaa.md)) reported 2% weekly usage because automation-only accounts were mistakenly included in the denominator.
   * **Evidence correction:** On June 18 ([record-661a77e48d.md](file:///workspace/product/history/evidence/record-661a77e48d.md)), usage was audited and corrected to **28% weekly usage among active humans**. The feature was rolled back on June 2 strictly due to count-query latency at scale (>50k tasks), not user disinterest.
   * **Current adoption:** Following the August 30 async query redesign ([record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md)), an audit on September 6 ([record-dfcc7fb912.md](file:///workspace/product/history/evidence/record-dfcc7fb912.md)) revised human weekly desktop usage to **21%** (`record-40440b02ae`). Status filtering is actively used on desktop, but mobile users remain completely unserved because the mobile component remained a draft.

2. **Assumption:** *"Sunday Room was shipped, so digest requests may already be handled."*
   * **Reality:** Sunday Room shipped workspace-level admin preferences ([record-8f6b82ec51.md](file:///workspace/product/history/retired/notification-reset/actions/record-8f6b82ec51.md)), but contributor-level subscriptions were never migrated.
   * **Evidence audit:** On August 19 ([record-f233630dab.md](file:///workspace/product/history/evidence/record-f233630dab.md)), an investigation revealed that for contributors subscribed prior to July 12, legacy per-user daily preferences take precedence over workspace weekly preferences (affecting 63 sampled contributors across 9 teams). On September 7 ([record-63ae4f2f22.md](file:///workspace/product/history/evidence/record-63ae4f2f22.md)), admin ticket counts were corrected, but legacy contributor preferences were explicitly left uninspected and unrevised.
   * **Why it is out of scope:** 
     1. Per [brief.md](file:///workspace/product/brief.md): *"Keep original evidence and activity from finished responsibilities. Their termination is not permission to resume them."* `notification-reset` ended July 31; reopening contributor notification migration exceeds standing authority.
     2. Ticket `record-5f1a34c149` represents legacy enterprise contributor notification settings, not onboarding friction.

---

## 5. Next Useful Action This Week

**Objective:** Bring the draft mobile status filter component ([record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md)) to mobile onboarding accounts as a small, reversible change.

1. **Focus on Small Onboarding Workspaces:**
   * Target new solo/small accounts (workspaces with <50 tasks, such as the 34-task Android workspace in `record-e36f0fe1aa`). Desktop small-workspace smoke checks already passed ([record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md)).
2. **Implement Asynchronous Status Filtering on Mobile:**
   * Implement the filter control on the mobile client using the proven asynchronous count queries deployed in desktop action `record-40440b02ae`.
   * Specifically verify the "waiting" status facet requested in ticket `record-e36f0fe1aa`.
3. **Ensure Reversibility:**
   * Guard the mobile filter control component behind a client-side feature flag so it can be enabled incrementally or rolled back instantly without touching the desktop deployment ([receipt record-764afbf446](file:///workspace/product/history/releases/record-b9a1361197.md)).
4. **Maintain Boundaries:**
   * Do not restart work on contributor email preference migrations from the terminated `notification-reset` responsibility.

---

## 6. Important Uncertainty

1. **Mobile Query Latency and Client UI Thread:**
   * While asynchronous count queries resolved performance on desktop browsers ([record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md)), performance on lower-tier mobile hardware or constrained cellular networks has not yet been benchmarked.
2. **Unknown Feedback Date on Digest Ticket:**
   * The submission date for ticket `record-5f1a34c149` is recorded as `unknown` ([record-0131162d69.md](file:///workspace/product/history/support/record-0131162d69.md)). The metadata field `age_days=20` reflects time elapsed since digest rollout, not when the user reported the issue, leaving the recency of this request uncertain.
3. **Mobile OS and Version Compatibility:**
   * Ticket `record-e36f0fe1aa` was submitted from Android 15. The draft mobile component's behavior on iOS and older Android releases remains unverified.
4. **Large-Workspace Degradation on Mobile:**
   * Prior Focus Shelf history showed count degradation above 50,000 tasks ([record-ecc0d14c71.md](file:///workspace/product/history/actions/record-ecc0d14c71.md)). While small onboarding workspaces are safe, mobile-specific query limits or pagination boundaries must be validated before expanding beyond small workspaces.
