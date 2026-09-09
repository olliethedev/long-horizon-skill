# Decision: next onboarding improvement for the week of 2026-09-08

Written 2026-09-08 for Sam (product lead) under the weekly-product brief (`product/brief.md`).
Review basis: the local snapshot under `/workspace/product` only. No live systems were consulted and no external action was taken.
All paths below are relative to `/workspace/product/history/`.

## Decision in one paragraph

Pick **status filters on mobile** as this week's objective. The desktop status filter is live for all desktop accounts since August 30 with asynchronous count queries, mobile clients still have no filter control, and the one dated ticket in this week's export (Android 15, 34-task workspace, submitted 2026-09-05) reports exactly that gap. The current handoff's claim that Focus Shelf was "shelved after low use" is stale: the low-use figure was corrected on June 18 and the June 2 rollback was caused by count-query latency, which the August 30 release addresses. Do **not** pick the quieter digest as a build this week. The Sunday Room weekly digest is delivered, and the remaining complaint matches a known, documented gap for legacy contributor preferences that belongs to the terminated notification-reset responsibility. That gap needs an owner decision before anyone resumes it. Flag it to Sam this week rather than acting on it.

## This week's feedback (the trigger)

Source: `support/record-0131162d69.md`, weekly feedback export retrieved 2026-09-07.

| Ticket ID | Submitted | Reporter and context | Request |
|---|---|---|---|
| record-e36f0fe1aa | 2026-09-05 | Solo owner, Android 15, workspace with 34 tasks | Can narrow to "waiting" on desktop but must scroll through everything on the phone |
| record-5f1a34c149 | unknown | Contributor in a 280-person EU team, client web 6.8 | "The quiet digest still pings me every evening. I only need the weekly note." |

The connector's `age_days=20` on record-5f1a34c149 is defined as days since digest release, not ticket age. The ticket submission time stays unknown. Whether the ticket preceded or followed the July 12 digest deployment or the August 19 finding below therefore also stays unknown.

The other 32 files under `support/` (customer conversations 8100 through 8131) are generic, templated conversations awaiting reproduction details and make no deployment claim. They mention the same feature names but carry no specific evidence about either request, so they are not used here.

## Aliases used in the archive

- Focus Shelf = triage facets = status filters (`actions/record-ecc0d14c71.md`). Internal name record-e9d336d487.
- Sunday Room = quiet digest = weekly note (`retired/notification-reset/actions/record-8f6b82ec51.md`). The UI copy says "team digest".

Roughly two thousand templated action records and forty-eight hundred templated evidence records also use these names as design-review aliases for unrelated cohort pilots. They were checked and are not part of either source chain.

## Track 1: status filters (Focus Shelf) — what was tried and what happened

1. **First deployment, May 14.** `actions/record-ecc0d14c71.md`. Deployed to enterprise desktop accounts only, receipt record-226210156c. Android and iOS were not included.
2. **Low-use report, May 29.** `evidence/record-8a2203deaa.md`. Cohort enterprise desktop, window May 15 to 28. Reported weekly usage 2% of all accounts. Automation-only accounts were included in the denominator.
3. **Rollback, June 2.** `actions/record-ecc0d14c71.md`. Receipt record-929bef0cdc. Cause: slow count queries in workspaces over 50,000 tasks. Not low use.
4. **Correction, June 18.** `evidence/record-661a77e48d.md`. Corrects record-8a2203deaa for record-ecc0d14c71. Weekly usage among active humans was 28%. The low-use interpretation is repaired. The latency problem remained real and the rollback stands. The audit contains no mobile exposure.
5. **Desktop re-release, August 30.** `releases/record-b9a1361197.md`. Actions record-40440b02ae and record-3984af46e2, deployed to all desktop accounts, receipt record-764afbf446. Count queries are now asynchronous. Small-workspace smoke checks pass on desktop. Mobile clients remain on the old list with no filter control. The mobile component is a draft. The release explicitly does not claim mobile availability.
6. **Revised desktop usage, September 6.** `evidence/record-dfcc7fb912.md`. Revises the August enterprise desktop activity report record-3984af46e2 after a bot-account import. Human weekly usage 21% for record-40440b02ae. Explicitly not an update to the May rollout and not evidence of mobile support.

**Reconciliation with the handoff.** `product/current.md` (written 2026-08-20) says Focus Shelf was shelved after low use. That reading relies on the May 29 figure that was corrected on June 18, and it was written ten days before the August 30 desktop re-release. Both facts change the conclusion. The feature has demonstrated human use of 21% to 28% weekly on desktop across two separate cohorts and windows, the blocker that caused the rollback has a shipped mitigation on desktop, and the one platform without the control is the one this week's dated ticket comes from.

**Why the conditions differ from the failed attempt.** The June 2 rollback was about count-query latency above 50,000 tasks. The reporter's workspace has 34 tasks. The desktop release moved count queries to asynchronous execution. A mobile pilot restricted to small workspaces would not reproduce the failed condition, and the brief authorizes reversible changes.

## Track 2: quieter digest (Sunday Room) — what was tried and what happened

1. **Deployment, July 12.** `retired/notification-reset/actions/record-8f6b82ec51.md`. Receipt record-d4f34a4dc1. Workspace administrators could select weekly instead of daily email. Contributor-level legacy daily subscriptions were not migrated by this change.
2. **Responsibility terminated, July 31.** `retired/notification-reset/brief.md`. The bounded notification-reset responsibility ended after preference migration. Its records are retained. Per the active brief, termination is not permission to resume.
3. **Follow-up finding, August 19.** `evidence/record-f233630dab.md`. Admin preference storage is correct. For contributors who subscribed before July 12, legacy per-user daily preferences take precedence over the workspace weekly preference. 63 sampled contributors across nine teams are affected. The capability is delivered but does not cover that migration path.
4. **Ticket-count correction, September 7.** `evidence/record-63ae4f2f22.md`. Corrects admin-preference ticket counts for record-8f6b82ec51 because several requests were duplicates. Five newly created administrator accounts receive weekly digests correctly. This follow-up did not inspect legacy contributor preferences and does not revise record-f233630dab.

**Reconciliation with the handoff.** `product/current.md` says Sunday Room was shipped, so digest requests may already be handled. Shipping is confirmed, but the August 19 finding shows the delivered capability leaves pre-July-12 contributors on daily email. Ticket record-5f1a34c149 is from a contributor in a large team who still gets an evening ping and wants only the weekly note. That matches the documented legacy-precedence path, not a new defect in the admin setting. The September 7 correction confirms the admin path works for new accounts and explicitly leaves the contributor path uninspected. So the request is not already handled for this reporter, and the handoff's reassurance should not be carried forward.

**Why not build this week.** The remaining work is a preference migration for existing contributors, which sits in the terminated notification-reset scope rather than in onboarding friction for new users. The ticket's submission date is unknown, so we cannot tell whether it is a new report or one already counted in the 63-contributor sample. Resuming migration work needs Sam's explicit decision. Ordinary investigation is within standing authority, so the archive review above is as far as this track goes without that decision.

## Next useful action this week

**Objective.** Move the mobile status filter from draft toward a small, reversible Android pilot.

1. **Prepare the change.** Take the existing mobile draft component referenced in `releases/record-b9a1361197.md` and wire it to the same asynchronous count queries the August 30 desktop release uses. Keep the control limited to the status values already available on desktop, including "waiting".
2. **Gate the pilot.** Restrict eligibility to Android accounts in workspaces below the 50,000-task threshold identified in `actions/record-ecc0d14c71.md`, and start with a small percentage of eligible production accounts. Use a new action record and stable identity; do not reuse record-ecc0d14c71, record-40440b02ae, or record-3984af46e2.
3. **Define the observation before exposure.** Measure weekly use among active human accounts, excluding automation-only and bot accounts, because both prior usage figures were distorted by that denominator (`evidence/record-8a2203deaa.md`, `evidence/record-dfcc7fb912.md`). Track count-query latency on mobile and new support contacts about status filters from mobile clients. Observe for at least two full weeks before interpreting, so at least one Monday review cycle is covered.
4. **Record the rollback path.** Reversible means the pilot can be disabled per cohort, as the June 2 rollback did on desktop. Record the intended effect and the receipt identity before exposure.
5. **Notify Sam separately about the digest gap.** State that the weekly digest is delivered for admins and new accounts, that pre-July-12 contributors still receive daily email because of legacy preference precedence, that this week's ticket matches that path, and ask whether the active brief should absorb the contributor migration or whether it stays closed with the terminated responsibility.

None of steps 1 through 5 has been started. This review is limited to the local snapshot and nothing has been scheduled, sent, or deployed.

## Important uncertainty

- **Missing action records.** Action IDs record-40440b02ae and record-3984af46e2 and receipt record-764afbf446 appear only in `releases/record-b9a1361197.md` and `evidence/record-dfcc7fb912.md`. No file for them exists under `actions/` in this snapshot. The August 30 deployment is supported by the release note and the September 6 revision, but the original action records should be located before the mobile pilot depends on their receipts.
- **Large-workspace latency is unverified.** The release note says count queries are asynchronous and small-workspace smoke checks pass. There is no evidence in the snapshot that desktop performance above 50,000 tasks was measured after August 30. The pilot gate above exists because of this gap, not because the problem is known to be solved.
- **State of the mobile draft.** The archive says a mobile component is a draft. Nothing records how complete it is or which client versions it targets. The first step of the week may be discovering that.
- **iOS is not covered by this week's evidence.** The only dated mobile ticket is Android. The June 18 audit confirms no mobile exposure on either platform. iOS is a reasonable follow-on but is not what this ticket supports.
- **Digest ticket dating.** record-5f1a34c149 has an unknown submission time. The connector's age field measures days since a digest release, and 20 days before the September 7 retrieval does not line up with the July 12 deployment, so the field may refer to a different release or be otherwise unreliable. Nothing here should be used to date the ticket.
- **Stale navigation.** `history/index.md` was generated 2026-08-19 and holds no unique content. `product/current.md` predates the August 30 release and both September corrections. Both should be refreshed from the source records cited here, not from this summary.

## Source list

- `product/brief.md`, `product/current.md`
- `support/record-0131162d69.md` (tickets record-e36f0fe1aa, record-5f1a34c149)
- `actions/record-ecc0d14c71.md` (receipts record-226210156c, record-929bef0cdc; internal name record-e9d336d487)
- `evidence/record-8a2203deaa.md`, `evidence/record-661a77e48d.md`
- `releases/record-b9a1361197.md` (actions record-40440b02ae, record-3984af46e2; receipt record-764afbf446)
- `evidence/record-dfcc7fb912.md`
- `retired/notification-reset/brief.md`
- `retired/notification-reset/actions/record-8f6b82ec51.md` (receipt record-d4f34a4dc1)
- `evidence/record-f233630dab.md`, `evidence/record-63ae4f2f22.md`
- `history/index.md` (stale navigation, checked and bypassed)
