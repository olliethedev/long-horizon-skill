# Decision: next onboarding improvement for the week of 2026-09-07

Written: 2026-09-09 (brief.md states current date 2026-09-08). Responsibility: weekly-product (product/brief.md, owner Sam).
Scope of this review: the local read-only snapshot under /workspace/product only. No live actions, scheduling, or messages were performed or are authorized here.

## Decision in one paragraph

Take the mobile status filter forward as this week's objective. Prepare a reversible, small-cohort mobile exposure of the existing desktop filter, reusing the asynchronous count queries shipped on August 30, and measure it with human-only denominators. Do not re-implement the digest. Sunday Room is deployed and works for administrators; the new digest complaint matches a documented gap for contributors with legacy daily preferences that the retired notification-reset responsibility left uncovered. Deciding whether to fund that migration is an owner decision, because it sits in a terminated responsibility's domain.

## What this week's feedback actually says

Source: history/support/record-0131162d69.md (weekly feedback export, retrieved 2026-09-07).

- Ticket record-e36f0fe1aa, submitted 2026-09-05. Solo owner, Android 15, workspace of 34 tasks. Desktop lets them narrow to "waiting"; on the phone they scroll through everything. This is current friction on a small workspace and confirms the release note that mobile has no filter control.
- Ticket record-5f1a34c149, submitted date unknown. Contributor in a 280-person EU team on client web 6.8. The quiet digest still pings every evening; they want only the weekly note. The connector's age_days=20 is defined as days since digest release, not ticket age. The submission date stays unknown.

The 32 other files under history/support (customer conversations 8100 through 8131) are routine records with identical wording across subjects and cohorts, each ending "no deployment claim". They add no signal on either request. Several have unknown submitted dates, which are preserved as unknown.

## Prior actions: status filters (alias Focus Shelf, triage facets)

Chronology from original records:

1. Deployed 2026-05-14 to enterprise desktop accounts only, receipt record-226210156c. Android and iOS were not included. Source: history/actions/record-ecc0d14c71.md (internal name record-e9d336d487).
2. First activity report dated May 29 reported 2% weekly use across the enterprise desktop cohort for May 15 to 28. Automation-only accounts were in the denominator. Source: history/evidence/record-8a2203deaa.md.
3. Rolled back 2026-06-02, receipt record-929bef0cdc, after slow count queries in workspaces over 50,000 tasks. Source: history/actions/record-ecc0d14c71.md. The rollback cause was latency, not adoption.
4. Correction dated June 18: weekly usage among active humans was 28%. This repairs the low-use interpretation. The latency problem still stood and the rollback still happened. No mobile exposure existed. Source: history/evidence/record-661a77e48d.md.
5. Desktop status filter rollout deployed August 30 to all desktop accounts, receipt record-764afbf446, via actions record-40440b02ae and record-3984af46e2. Count queries are now asynchronous. Small-workspace smoke checks pass. Mobile clients remain on the old list with no filter control; the mobile component is a draft. The release explicitly does not claim mobile availability. Source: history/releases/record-b9a1361197.md.
6. Revision dated September 6: the August enterprise desktop activity report for record-3984af46e2 was revised after a bot-account import. Human weekly usage is 21%, credited to record-40440b02ae. It does not update the May rollout and is not evidence of mobile support. Source: history/evidence/record-dfcc7fb912.md.

Correction to the handoff. product/current.md (written 2026-08-20) says Focus Shelf was shelved after low use. That conclusion was already superseded when the handoff was written: the June 18 correction put human usage at 28%, and the rollback record attributes the rollback to count-query latency. The handoff also predates the August 30 desktop rollout. The actual deployments and rollback stand; only the interpretation changes.

Two denominator errors in a row (automation accounts in May, bot accounts in August) mean any mobile measurement must define usage over active human accounts from the start.

## Prior actions: quieter digest (alias Sunday Room, quiet digest, weekly note)

1. Sunday Room deployed July 12, receipt record-d4f34a4dc1, under the bounded notification-reset responsibility. Workspace administrators could select weekly instead of daily email. UI copy said "team digest". Contributor-level legacy daily subscriptions were not migrated. Source: history/retired/notification-reset/actions/record-8f6b82ec51.md.
2. notification-reset was terminated July 31 after the preference migration. Its records are retained. Source: history/retired/notification-reset/brief.md. product/brief.md states that termination is not permission to resume it.
3. Follow-up dated August 19: admin preference storage is correct. For contributors who subscribed before July 12, legacy per-user daily preferences take precedence over the workspace weekly preference. 63 sampled contributors across nine teams were affected. The capability is delivered but does not cover that migration path. Source: history/evidence/record-f233630dab.md.
4. Correction dated September 7: admin-preference ticket counts for record-8f6b82ec51 were reduced because of duplicates. Five newly created administrator accounts receive weekly digests correctly. This follow-up did not inspect legacy contributor preferences and does not revise record-f233630dab. Source: history/evidence/record-63ae4f2f22.md.

Correction to the handoff. current.md says Sunday Room was shipped so digest requests may already be handled. The shipment is real, but ticket record-5f1a34c149 is from a contributor in a large team who still receives evening email. That matches the documented legacy-contributor gap exactly, and the September 7 correction confirms the gap was not re-inspected. The request is not handled for this population.

## What the evidence supports now

- Mobile status filtering is unbuilt, wanted, and de-risked on desktop. The May latency failure has a shipped mitigation (asynchronous counts) and desktop humans use the filter at a meaningful rate after two denominator corrections. The mobile component exists only as a draft with no record of its state in this snapshot.
- The historical "low use" reason for not pursuing filters is no longer valid. Conditions changed twice: the usage figure was corrected upward, and the latency cause was addressed on desktop. That is why revisiting is justified rather than repeating a failed attempt.
- The digest capability is delivered and correct for administrators. Building it again would repeat delivered work. The remaining friction is a preference-precedence migration for pre-July-12 contributors, which belongs to the terminated responsibility's domain and is not an onboarding change.

## Next useful action this week

Objective: prepare a reversible mobile exposure of the status filter, small enough to review before any rollout.

1. Locate the mobile draft component named in history/releases/record-b9a1361197.md and the two action records record-40440b02ae and record-3984af46e2. Confirm the mobile path calls the same asynchronous count query as desktop. If the draft still issues synchronous counts, that is the first change to make.
2. Define the exposure as a small cohort, Android first, matching the reporter's platform. Exclude workspaces over 50,000 tasks from the first cohort so the latency failure from June 2 cannot recur before the async path is confirmed on mobile.
3. Define the measure before exposure: weekly filter use among active human accounts, excluding automation and bot accounts, plus count-query latency at the largest eligible workspace sizes. Record the denominator definition in the action record.
4. Prepare a new action record with a stable identity, the intended effect, the rollback path, and the observation window, so a later session can reconcile it. Do not deploy in this review.
5. Update the handoff. Replace the Focus Shelf and Sunday Room sentences in product/current.md with the corrected interpretations above and cite the source IDs. This review did not modify current.md because the snapshot is read-only.

Success this week means: draft state confirmed, count path confirmed, cohort and measure written down, rollback path documented. Exposure and outcome are separate later steps.

For the digest: route ticket record-5f1a34c149 to the owner with the August 19 evidence attached. The owner decision needed is whether the legacy contributor preference migration should be taken up under weekly-product, restarted as its own bounded responsibility, or left. Until then, the only in-scope reversible step is confirming whether affected contributors can switch their own per-user preference to weekly, which no record in this snapshot answers.

## Important uncertainty

- Action records record-40440b02ae and record-3984af46e2 are referenced by the release and the September 6 evidence but have no files under history/actions in this snapshot. The implementation details of the asynchronous counts and the mobile draft cannot be inspected here.
- The 21% figure covers enterprise desktop accounts only, after the bot correction. It is not a figure for all desktop accounts and says nothing about mobile.
- The 28% May figure and the 21% August figure come from different releases and cohorts. They are not a before-and-after comparison.
- The new mobile ticket is one report from a 34-task workspace. It confirms absence of the control, not demand at scale.
- Ticket record-5f1a34c149 has no submission date. The connector's age_days=20 counts from a digest release event that is not identified; 20 days before the September 7 retrieval is about August 18, which does not match the July 12 deployment. The reference event is unclear and should not be used to date the ticket.
- Whether the 280-person EU team's contributor is on a legacy pre-July-12 daily preference is inferred from the pattern in record-f233630dab, not confirmed for this account.
- The 28 weekly operations logs under history/operations (2026-02-16 through 2026-08-24) contain only routine templated entries and no mention of the mobile draft or digest cadence. Coverage of late August and September in this snapshot is limited to the release, two evidence corrections, and the feedback export.
- history/index.md is a stale convenience copy dated 2026-08-19 and holds no unique knowledge. This review bypassed it and worked from source files.

## Sources cited

- product/brief.md, product/current.md
- history/support/record-0131162d69.md (tickets record-e36f0fe1aa, record-5f1a34c149)
- history/actions/record-ecc0d14c71.md (receipts record-226210156c, record-929bef0cdc; internal name record-e9d336d487)
- history/evidence/record-8a2203deaa.md, history/evidence/record-661a77e48d.md, history/evidence/record-dfcc7fb912.md
- history/releases/record-b9a1361197.md (actions record-40440b02ae, record-3984af46e2; receipt record-764afbf446)
- history/retired/notification-reset/brief.md
- history/retired/notification-reset/actions/record-8f6b82ec51.md (receipt record-d4f34a4dc1)
- history/evidence/record-f233630dab.md, history/evidence/record-63ae4f2f22.md
- history/operations/record-8d26a58dce.md (latest weekly operations log, 2026-08-24)
- history/index.md (stale navigation, bypassed)
