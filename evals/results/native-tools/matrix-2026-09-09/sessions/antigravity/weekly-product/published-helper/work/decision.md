# Product Decision: Mobile Status Filters as the Next Onboarding Improvement

**Date:** 2026-09-09  
**Responsibility:** weekly-product (Owner: Sam, product lead; brief current date: 2026-09-08)  
**Status:** Active  
**Scope:** Reduce recurring onboarding friction across mobile and desktop; prioritize observed problems, with ordinary investigation and reversible changes authorized.  
**Decision Target:** `/workspace/work/decision.md`  

---

## 1. Executive Summary & Selected Recommendation

Based on a thorough review of the product history, standing authority, and the weekly feedback export retrieved on 2026-09-07 ([history/support/record-0131162d69.md](file:///workspace/product/history/support/record-0131162d69.md)), the next useful onboarding improvement to pursue this week is **bringing the draft mobile status filter component to verification and preparing an initial reversible pilot**.

### Why Mobile Status Filters (Selected):
1. **Direct Alignment with Onboarding Scope:** Ticket [record-e36f0fe1aa](file:///workspace/product/history/support/record-0131162d69.md) (submitted 2026-09-05) identifies acute onboarding friction for solo owners on mobile (Android 15) who must scroll through all tasks rather than filtering to "waiting".
2. **Proven Value and Performance on Desktop:** The previous performance issue (slow count queries on workspaces over 50,000 tasks) was resolved by switching to asynchronous count queries in desktop release [record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md) (deployed 2026-08-30, receipt `record-764afbf446`). Desktop adoption is confirmed at **21% human weekly usage** ([history/evidence/record-dfcc7fb912.md](file:///workspace/product/history/evidence/record-dfcc7fb912.md)), decisively refuting the stale assumption that the feature suffered from low use.
3. **Draft Work Ready to Advance:** The mobile status filter component was already developed as a draft ([history/releases/record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md)). Completing smoke tests on small workspaces (like the 34 tasks reported in the Android ticket) and preparing a reversible pilot fits cleanly within standing authority and keeps the next objective small.

### Why Not Quieter Digest This Week:
1. **Out of Scope for New-User Onboarding:** Ticket [record-5f1a34c149](file:///workspace/product/history/support/record-0131162d69.md) comes from an existing contributor in a 280-person EU team on web client 6.8 regarding daily evening emails. This is an enterprise team member notification preference issue, not onboarding friction.
2. **Boundaries of Terminated Responsibility:** Sunday Room ([history/retired/notification-reset/actions/record-8f6b82ec51.md](file:///workspace/product/history/retired/notification-reset/actions/record-8f6b82ec51.md)) deployed on 2026-07-12 (receipt `record-d4f34a4dc1`) allowed workspace *administrators* to select weekly email, but intentionally did not migrate contributor-level legacy daily subscriptions. This was part of the bounded responsibility `notification-reset`, which terminated on 2026-07-31 ([history/retired/notification-reset/brief.md](file:///workspace/product/history/retired/notification-reset/brief.md)). Per [brief.md](file:///workspace/product/brief.md), termination of a finished responsibility does not grant permission to resume it. Reopening contributor email subscription migrations requires separate owner authority.
3. **Uncertain Timing:** Ticket [record-5f1a34c149](file:///workspace/product/history/support/record-0131162d69.md) has an **unknown** submission date. The connector field `age_days=20` indicates days elapsed since the digest release, not ticket age.

---

## 2. Reconstructing Prior Actions: What We Tried vs. What Actually Happened

The current handoff ([current.md](file:///workspace/product/current.md), written 2026-08-20) contained two critical summary claims that required verification against underlying records:
* *"Focus Shelf was shelved after low use."*
* *"Sunday Room was shipped, so digest requests may already be handled."*

Inspection of original action records, release notes, and evidence reveals that both claims are incomplete or misleading.

### A. Status Filters / "Focus Shelf" (Triage Facets)

| Milestone | Date / Receipt | Source Record | What Actually Happened |
| :--- | :--- | :--- | :--- |
| **Initial Desktop Pilot** | 2026-05-14<br>Receipt: `record-226210156c` | [history/actions/record-ecc0d14c71.md](file:///workspace/product/history/actions/record-ecc0d14c71.md) | Deployed under aliases "Focus Shelf" / "triage facets" / "status filters" (internal ID `record-e9d336d487`) to enterprise desktop accounts only. Mobile (Android/iOS) was not included. |
| **Initial Measurement (Flawed)** | 2026-05-29 (Window: May 15–28) | [history/evidence/record-8a2203deaa.md](file:///workspace/product/history/evidence/record-8a2203deaa.md) | Reported 2% weekly usage across all accounts. However, automation-only bot accounts were erroneously included in the denominator, artificially depressing the rate. |
| **Rollback** | 2026-06-02<br>Receipt: `record-929bef0cdc` | [history/actions/record-ecc0d14c71.md](file:///workspace/product/history/actions/record-ecc0d14c71.md) | Rolled back not because of fundamental lack of interest, but due to severe database performance bottlenecks: slow synchronous count queries in workspaces over 50,000 tasks. |
| **Architectural Fix & Desktop Release** | 2026-08-30<br>Receipt: `record-764afbf446` | [history/releases/record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md) | Action IDs `record-40440b02ae` and `record-3984af46e2` deployed to all desktop accounts. **Count queries were re-architected to be asynchronous**, solving the query bottleneck. Desktop smoke checks on small workspaces passed. However, mobile clients were omitted; mobile filter UI remained an unreleased draft component. |
| **Corrected Desktop Evidence** | 2026-09-06 | [history/evidence/record-dfcc7fb912.md](file:///workspace/product/history/evidence/record-dfcc7fb912.md) | Revised activity report for enterprise desktop accounts after bot accounts were removed: **human weekly usage was 21%**. Confirms that the feature has strong demand when performant, but notes that this does not constitute mobile support. |

### B. Quieter Digest / "Sunday Room" (Weekly Note / Team Digest)

| Milestone | Date / Receipt | Source Record | What Actually Happened |
| :--- | :--- | :--- | :--- |
| **Digest Setting Deployment** | 2026-07-12<br>Receipt: `record-d4f34a4dc1` | [history/retired/notification-reset/actions/record-8f6b82ec51.md](file:///workspace/product/history/retired/notification-reset/actions/record-8f6b82ec51.md) | Deployed under aliases "Sunday Room" / "quiet digest" / "weekly note". Allowed workspace **administrators** to select weekly instead of daily email (UI copy labeled "team digest"). |
| **Omission / Limitation** | 2026-07-12 | [history/retired/notification-reset/actions/record-8f6b82ec51.md](file:///workspace/product/history/retired/notification-reset/actions/record-8f6b82ec51.md) | **Contributor-level legacy daily subscriptions were NOT migrated.** Non-administrator team members continued receiving daily evening emails. |
| **Responsibility Termination** | 2026-07-31 | [history/retired/notification-reset/brief.md](file:///workspace/product/history/retired/notification-reset/brief.md) | The bounded responsibility `notification-reset` formally terminated. Records were retained for reference, but standing authority to alter user preferences expired. |

---

## 3. What the Evidence Supports Now

### Feedback Analysis ([history/support/record-0131162d69.md](file:///workspace/product/history/support/record-0131162d69.md), Retrieved 2026-09-07)

1. **Mobile Status Filter Request (Ticket `record-e36f0fe1aa`):**
   * **Submitted Date:** 2026-09-05
   * **Cohort:** Solo owner on Android 15; workspace with 34 tasks.
   * **Observation:** *"On desktop I can narrow to waiting, but on my phone I have to scroll through everything."*
   * **Significance:** This is a fresh, post-rollout observation following the 2026-08-30 desktop release. The user actively benefits from desktop status filtering, but experiences immediate friction on Android. Small-workspace solo owners represent the core onboarding funnel target.

2. **Quiet Digest Feedback (Ticket `record-5f1a34c149`):**
   * **Submitted Date:** Unknown (preserved as unknown per evidence guidelines).
   * **Cohort:** Contributor in a 280-person EU team; client web 6.8.
   * **Connector Metadata:** `age_days=20` (defined as days since the digest release, **not** ticket age).
   * **Observation:** *"The quiet digest still pings me every evening. I only need the weekly note."*
   * **Significance:** This user is an existing contributor in a large enterprise team on desktop web. Their issue directly stems from the unmigrated legacy daily subscriptions noted in `record-8f6b82ec51.md`. It does not reflect new user onboarding friction.

### Synthesis:
* The claim in [current.md](file:///workspace/product/current.md) that "Focus Shelf was shelved after low use" is invalidated by [history/releases/record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md) and [history/evidence/record-dfcc7fb912.md](file:///workspace/product/history/evidence/record-dfcc7fb912.md) (21% usage). The backend query issue is already resolved with async queries.
* The claim that "Sunday Room was shipped, so digest requests may already be handled" is factually incomplete: Sunday Room only solved digest settings for workspace administrators, leaving contributor legacy daily subscriptions active.
* However, because `notification-reset` is terminated, and ticket `record-5f1a34c149` reflects enterprise team contributor notification settings rather than onboarding flow, tackling email digests is both out of current responsibility authority and disconnected from onboarding friction.

---

## 4. Next Useful Action for This Week

**Objective:** Complete mobile client verification of the draft status filter component and prepare an initial reversible pilot on Android for small workspaces.

### Concrete Implementation Steps:
1. **Inspect Draft Component:**
   * Review the existing draft mobile status filter component referenced in [history/releases/record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md).
   * Confirm the mobile implementation hooks directly into the asynchronous query endpoints deployed in [record-40440b02ae](file:///workspace/product/history/releases/record-b9a1361197.md) rather than issuing synchronous count queries.
2. **Execute Small-Workspace Smoke Checks on Mobile:**
   * Validate filter behavior (specifically filtering to "waiting" and clearing filters) on mobile clients, matching the Android 15 environment and small workspace sizes (≤ 50 tasks, corresponding to the 34 tasks in `record-e36f0fe1aa`).
   * Verify UI layout responsiveness and ensure the filter bar does not obstruct task scrolling or drawer interactions.
3. **Prepare Reversible Rollout Artifact:**
   * Draft a scoped rollout specification for a reversible 10–20% mobile pilot or opt-in toggle within standing authority.
   * Define clear rollback criteria (e.g., query timeouts, mobile client crashes, or list render delays > 200ms).
4. **Digest Backlog Record:**
   * Log a note under weekly product records clarifying why contributor digest complaints persist (due to unmigrated legacy subscriptions from `record-8f6b82ec51.md`), so that if product lead Sam decides to charter a notification preference project, the root cause is documented. Do not initiate code changes or email migration work this week.

---

## 5. Important Uncertainties & Product Boundaries

1. **Mobile Performance on Large Workspaces:**
   * While asynchronous queries resolved database stalls on desktop ([history/releases/record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md)), mobile client rendering and network latency over cellular connections on larger workspaces (>1,000 tasks) have not been evaluated. Initial mobile testing should restrict exposure or benchmark small workspaces first.
2. **Draft Component Platform Coverage:**
   * [history/releases/record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md) notes that "the mobile component is a draft". It is uncertain whether the draft component is equally mature on Android and iOS, or if platform-specific UI adjustments will be required for Android 15 gesture navigation.
3. **Ticket `record-5f1a34c149` Timestamp & Breadth:**
   * The submission timestamp for ticket `record-5f1a34c149` is **unknown**. Because `age_days=20` indicates days since digest release rather than when the user contacted support, we cannot establish whether this complaint is an isolated legacy inquiry or part of an escalating volume.
4. **Authority over Terminated Responsibilities:**
   * The `notification-reset` responsibility terminated on 2026-07-31 ([history/retired/notification-reset/brief.md](file:///workspace/product/history/retired/notification-reset/brief.md)). Under [brief.md](file:///workspace/product/brief.md), standing authority does not permit resuming terminated responsibilities without explicit owner direction. Modifying subscriber email settings across enterprise accounts would exceed the standing remit of weekly onboarding friction reduction.

---

## 6. Citation Ledger

| Source Path | Source ID / Ref | Type / Subject | Key Content / Citation |
| :--- | :--- | :--- | :--- |
| `brief.md` | `weekly-product` | Responsibility Brief | Owner: Sam. Current date: 2026-09-08. Scope: onboarding friction across mobile and desktop. Finished responsibilities are not permission to resume them. |
| `current.md` | N/A | Handoff (2026-08-20) | Asserted Focus Shelf shelved after low use; Sunday Room shipped so digest requests handled. |
| `history/support/record-0131162d69.md` | `record-e36f0fe1aa` | Feedback Ticket | Submitted 2026-09-05. Solo owner on Android 15 (34 tasks): cannot filter to waiting on phone. |
| `history/support/record-0131162d69.md` | `record-5f1a34c149` | Feedback Ticket | Submitted unknown. Contributor in 280-person EU team (client web 6.8): still receives daily evening digest. `age_days=20` (days since release). |
| `history/actions/record-ecc0d14c71.md` | `record-e9d336d487`<br>`record-226210156c`<br>`record-929bef0cdc` | Action Record | Deployed May 14 to enterprise desktop only. Initial 2% report. Rolled back June 2 due to slow count queries (>50k tasks). |
| `history/evidence/record-8a2203deaa.md` | `record-8a2203deaa` | Evidence Record | Dated May 29. 2% usage included automation-only accounts in denominator. |
| `history/releases/record-b9a1361197.md` | `record-40440b02ae`<br>`record-3984af46e2`<br>`record-764afbf446` | Release Record | Deployed Aug 30 to all desktop accounts. Asynchronous count queries. Mobile is draft; not claimed. |
| `history/evidence/record-dfcc7fb912.md` | `record-dfcc7fb912` | Evidence Record | Dated Sept 6. Human weekly usage 21% on desktop. Does not evidence mobile support. |
| `history/retired/notification-reset/actions/record-8f6b82ec51.md` | `record-8f6b82ec51`<br>`record-d4f34a4dc1` | Retired Action | Deployed July 12. Allowed admins to select weekly email. Contributor legacy daily subscriptions not migrated. |
| `history/retired/notification-reset/brief.md` | `notification-reset` | Terminated Responsibility | Terminated July 31 after preference migration. Records retained for reference. |
