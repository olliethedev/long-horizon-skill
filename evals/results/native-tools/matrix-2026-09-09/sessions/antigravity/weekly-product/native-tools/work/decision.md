# Product Handoff Review & Decision

- **Responsibility:** `weekly-product` ([brief.md](file:///workspace/product/brief.md))
- **Product Lead / Owner:** Sam
- **Decision Date:** 2026-09-09 (Evaluating snapshot state as of 2026-09-08 / 2026-09-09)
- **Review Scope:** Reduce recurring onboarding friction across mobile and desktop; prioritize observed problems with reversible changes. Read-only local snapshot review; no external tools, live actions, scheduling, or production mutations authorized.

---

## 1. Executive Recommendation

**Next Useful Onboarding Improvement:** **Mobile Status Filter Component for Onboarding Workspaces** (advancing the unreleased draft component).

### Rationale
This week’s feedback export ([support/record-0131162d69.md](file:///workspace/product/history/support/record-0131162d69.md)) contained two customer requests:
1. **Status filters on phone:** Ticket `record-e36f0fe1aa` (submitted 2026-09-05) from a solo owner on Android 15 onboarding with 34 tasks: *"On desktop I can narrow to waiting, but on my phone I have to scroll through everything."*
2. **Quieter digest:** Ticket `record-5f1a34c149` (submitted **unknown**; `age_days=20` indicates days since digest release, not ticket age) from a contributor in a 280-person EU team on web client 6.8: *"The quiet digest still pings me every evening. I only need the weekly note."*

Between these two:
- **Mobile Status Filters** directly falls under the `weekly-product` onboarding mandate ([brief.md](file:///workspace/product/brief.md): *"Reduce recurring onboarding friction across mobile and desktop"*). The technical risk (query latency on large workspaces) was already resolved on desktop using asynchronous count queries ([releases/record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md)), and desktop adoption is confirmed at 21% human weekly use ([evidence/record-dfcc7fb912.md](file:///workspace/product/history/evidence/record-dfcc7fb912.md)). However, mobile clients remain on the old list with no filter controls because the mobile component was left in draft form.
- **Quieter Digest** is **not** an onboarding issue, but rather an unmigrated preference precedence issue affecting established contributors in mature teams. Furthermore, it belongs to `notification-reset`, a bounded responsibility that was explicitly terminated on July 31, 2026 ([retired/notification-reset/brief.md](file:///workspace/product/history/retired/notification-reset/brief.md)). Under project standing authority ([brief.md](file:///workspace/product/brief.md)), terminated responsibilities must not be resumed without owner authorization.

---

## 2. Analysis of Feedback Items

| Dimension | Feedback Item 1: Mobile Status Filters | Feedback Item 2: Quieter Digest |
| :--- | :--- | :--- |
| **Source Record** | [support/record-0131162d69.md](file:///workspace/product/history/support/record-0131162d69.md) | [support/record-0131162d69.md](file:///workspace/product/history/support/record-0131162d69.md) |
| **Ticket ID** | `record-e36f0fe1aa` | `record-5f1a34c149` |
| **Submission Date** | **2026-09-05** | **unknown** *(Connector reports `age_days=20`, defined as days since digest release, not ticket age. Date preserved as unknown per [evidence.md](file:///workspace/skill/references/evidence.md))* |
| **Retrieval Date** | 2026-09-07 | 2026-09-07 |
| **User & Cohort** | Solo owner on Android 15; workspace with 34 tasks | Contributor in a 280-person EU team; client web 6.8 |
| **Customer Problem** | Has desktop filtering ("waiting"), but cannot filter on phone, forcing manual scrolling through all tasks during onboarding task management. | Still receives daily evening digest emails despite expecting only a weekly note. |
| **Applicability to Onboarding** | **Directly applicable:** Core onboarding workflow for new workspace owners managing task setup on mobile. | **Not onboarding:** Post-onboarding notification volume for existing team members in large organizations. |

---

## 3. Relevant Prior Actions & What Actually Happened

Our current handoff ([current.md](file:///workspace/product/current.md), written 2026-08-20) made two assertions that original records show were inaccurate or outdated:

### A. Status Filters & "Focus Shelf"
*Current handoff claim: "Focus Shelf was shelved after low use."*

#### 1. Initial Attempt & Flawed Evaluation
- **Action:** `record-ecc0d14c71` ([actions/record-ecc0d14c71.md](file:///workspace/product/history/actions/record-ecc0d14c71.md)), internal ID `record-e9d336d487`, aliases: "triage facets", "status filters".
- **Deployment:** Deployed on May 14, 2026 (receipt `record-226210156c`) to enterprise desktop accounts only. Android and iOS were explicitly excluded.
- **Flawed Metric:** Report `record-8a2203deaa` ([evidence/record-8a2203deaa.md](file:///workspace/product/history/evidence/record-8a2203deaa.md), dated May 29, 2026) reported only 2% weekly use. However, automation-only bot accounts were mistakenly included in the denominator.
- **Rollback:** Rolled back June 2, 2026 (receipt `record-929bef0cdc`) due to severe count-query latency on workspaces exceeding 50,000 tasks.

#### 2. Evidence Correction
- **Correction:** `record-661a77e48d` ([evidence/record-661a77e48d.md](file:///workspace/product/history/evidence/record-661a77e48d.md), dated June 18, 2026) audited active human usage and revealed it was actually **28%**, debunking the "low-use" conclusion. Count-query latency was the only valid technical reason for the rollback. The audit noted no mobile exposure existed.

#### 3. Desktop Re-rollout & Current Mobile State
- **Release:** `record-b9a1361197` ([releases/record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md)), actions `record-40440b02ae` and `record-3984af46e2`, deployed August 30, 2026 to all desktop accounts (receipt `record-764afbf446`).
- **Technical Fix:** Count queries were re-architected as **asynchronous**, successfully passing small-workspace smoke checks.
- **Desktop Usage:** `record-dfcc7fb912` ([evidence/record-dfcc7fb912.md](file:///workspace/product/history/evidence/record-dfcc7fb912.md), dated September 6, 2026) confirmed human weekly desktop usage is **21%** (revising after bot-account import).
- **Mobile Gap:** `releases/record-b9a1361197.md` explicitly states: *"Mobile clients remain on the old list and have no filter control; the mobile component is a draft. This release does not claim mobile availability."* Mobile was never released, explaining ticket `record-e36f0fe1aa`.

---

### B. Quieter Digest & "Sunday Room"
*Current handoff claim: "Sunday Room was shipped, so digest requests may already be handled."*

#### 1. Implementation in Retired Responsibility
- **Action:** `record-8f6b82ec51` ([retired/notification-reset/actions/record-8f6b82ec51.md](file:///workspace/product/history/retired/notification-reset/actions/record-8f6b82ec51.md)), aliases: "quiet digest", "weekly note".
- **Deployment:** Deployed July 12, 2026 (receipt `record-d4f34a4dc1`) by `notification-reset`, a bounded responsibility that terminated July 31, 2026 ([retired/notification-reset/brief.md](file:///workspace/product/history/retired/notification-reset/brief.md)).
- **Functionality:** Allowed workspace administrators to select weekly instead of daily email ("team digest"). Contributor-level legacy daily subscriptions were not migrated.

#### 2. What Actually Happened to Contributors
- **Evidence:** `record-f233630dab` ([evidence/record-f233630dab.md](file:///workspace/product/history/evidence/record-f233630dab.md), dated August 19, 2026) showed that for contributors who subscribed prior to July 12, 2026, legacy per-user daily preferences take precedence over workspace weekly preferences (affecting 63 sampled contributors across 9 teams). The capability was delivered for admin settings but omitted this migration path.
- **Subsequent Audit:** `record-63ae4f2f22` ([evidence/record-63ae4f2f22.md](file:///workspace/product/history/evidence/record-63ae4f2f22.md), dated September 7, 2026) confirmed that 5 new administrator accounts receive weekly digests correctly, but explicitly noted it did not inspect legacy contributor preferences and did not revise `record-f233630dab`.
- **Outcome:** The assertion in `current.md` that Sunday Room handled digest requests was mistaken for contributors. Ticket `record-5f1a34c149` reflects this known unmigrated legacy preference bug.

---

## 4. What the Evidence Supports Now

1. **Focus Shelf was not shelved due to lack of user demand:** Active human desktop adoption was 28% in May ([evidence/record-661a77e48d.md](file:///workspace/product/history/evidence/record-661a77e48d.md)) and is 21% in September ([evidence/record-dfcc7fb912.md](file:///workspace/product/history/evidence/record-dfcc7fb912.md)). The rollback was caused by synchronous query latency on >50k tasks, which was resolved on desktop by making count queries asynchronous ([releases/record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md)).
2. **Mobile status filtering was never deployed:** Mobile clients have no filter controls and remain on the old list because the mobile component was left in draft ([releases/record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md)). Solo onboarding mobile users are currently experiencing avoidable task-triage friction ([support/record-0131162d69.md](file:///workspace/product/history/support/record-0131162d69.md)).
3. **Digest requests are not handled for legacy contributors:** Sunday Room only provided workspace-level admin options; legacy contributor daily preferences override workspace settings ([evidence/record-f233630dab.md](file:///workspace/product/history/evidence/record-f233630dab.md)). However, this is an email notification preference migration issue for existing team members, belonging to a terminated responsibility (`notification-reset`), rather than an onboarding product issue.

---

## 5. Next Useful Action (This Week)

Pursuant to standing authority in [brief.md](file:///workspace/product/brief.md) (*"investigate evidence, choose ordinary objectives, and prepare reversible changes within this product"*):

1. **Advance the Draft Mobile Status Filter Component:**
   - Inspect and complete the draft mobile filter component referenced in [releases/record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md).
   - Ensure the mobile component uses the asynchronous count query pattern established in desktop actions `record-40440b02ae` and `record-3984af46e2` to prevent UI thread blocking.
2. **Define Small-Workspace Smoke Checks on Mobile:**
   - Create smoke check criteria for small mobile accounts (<100 tasks, directly matching the solo owner profile on Android 15 in ticket `record-e36f0fe1aa`).
3. **Prepare a Staged, Reversible Rollout Plan:**
   - Plan a limited initial rollout cohort (e.g., new solo Android accounts) with feature flagging to permit immediate rollback if query latency or layout regressions occur.
4. **Digest Follow-up for Product Lead:**
   - Retain evidence [record-f233630dab.md](file:///workspace/product/history/evidence/record-f233630dab.md) and [record-63ae4f2f22.md](file:///workspace/product/history/evidence/record-63ae4f2f22.md) in records. Advise Sam (product lead) of the contributor preference precedence gap so they can decide whether to charter a dedicated notification migration task, keeping it separate from the weekly onboarding sprint.

---

## 6. Important Uncertainty

1. **Mobile Network Conditions & Async State Handling:** While asynchronous queries resolved desktop performance ([releases/record-b9a1361197.md](file:///workspace/product/history/releases/record-b9a1361197.md)), high-latency or fluctuating mobile cellular connections may cause delayed badge counts or list-flicker on mobile devices. Loading and error states must be verified.
2. **Platform & OS Scope:** Ticket `record-e36f0fe1aa` specifically documents Android 15. The draft mobile component's readiness across iOS vs. Android remains unverified in this snapshot.
3. **Digest Ticket Submission Freshness:** Ticket `record-5f1a34c149` has an **unknown** submission date; `age_days=20` represents elapsed days since the digest release, not ticket submission time. Its submission recency relative to other feedback cannot be established from this export alone.
4. **Metric Denominators:** Prior analyses repeatedly misclassified bot/automation accounts as human users ([evidence/record-8a2203deaa.md](file:///workspace/product/history/evidence/record-8a2203deaa.md) vs. [evidence/record-661a77e48d.md](file:///workspace/product/history/evidence/record-661a77e48d.md), and [evidence/record-dfcc7fb912.md](file:///workspace/product/history/evidence/record-dfcc7fb912.md)). Any future mobile adoption measurement must explicitly filter for human interactive sessions.
