# Weekly product decision: next onboarding improvement

Dated 2026-09-09 (product/brief.md states the current date as 2026-09-08). Prepared for Sam, product lead, from the local snapshot only. No live actions were taken or are authorized by this note.

## Decision in one paragraph

Pick the mobile status filter as this week's objective, scoped to a small reversible step: get the draft mobile filter component ready for a flag-gated Android pilot in small workspaces, with the count-query latency guard that sank the May rollout recorded as an explicit gate. Do not treat the quieter-digest request as handled. It is handled for administrators and new accounts but not for contributors who subscribed before July 12, and that gap belongs to the terminated notification-reset responsibility. Surface it to Sam for an explicit decision rather than acting on it under weekly-product authority.

## Two claims in current.md that the archive does not support

product/current.md (written 2026-08-20) says "Focus Shelf was shelved after low use" and "Sunday Room was shipped, so digest requests may already be handled." Both are stale.

1. **Focus Shelf is the status filter, and it was not shelved for low use.** actions/record-ecc0d14c71 lists its aliases as "triage facets" and "status filters". The 2% weekly-use figure in evidence/record-8a2203deaa (dated May 29) included automation-only accounts in the denominator. evidence/record-661a77e48d (dated June 18) corrected it to 28% among active humans and says plainly that this "repairs the low-use interpretation." The June 2 rollback was for slow count queries in workspaces over 50,000 tasks, not for low use. The filter was then re-released to all desktop accounts on August 30 (releases/record-b9a1361197).
2. **Sunday Room shipped, but it does not cover the person in this week's ticket.** retired/notification-reset/actions/record-8f6b82ec51 records the July 12 deployment: workspace administrators could select weekly instead of daily email, and "contributor-level legacy daily subscriptions were not migrated by this change." evidence/record-f233630dab (dated August 19) confirms that for contributors who subscribed before July 12, legacy per-user daily preferences take precedence over the workspace weekly preference, affecting 63 sampled contributors across nine teams. evidence/record-63ae4f2f22 (dated September 7) fixed duplicate ticket counts and verified new administrator accounts, but "did not inspect legacy contributor preferences and does not revise record-f233630dab."

## This week's feedback

Source: history/support/record-0131162d69.md, retrieved 2026-09-07. It contains two tickets.

- **Ticket record-e36f0fe1aa**, submitted 2026-09-05. Solo owner on Android 15, workspace with 34 tasks: "On desktop I can narrow to waiting, but on my phone I have to scroll through everything." This matches the release note exactly: mobile clients "remain on the old list and have no filter control; the mobile component is a draft" (releases/record-b9a1361197).
- **Ticket record-5f1a34c149**, submitted unknown. Contributor in a 280-person EU team, client web 6.8: "The quiet digest still pings me every evening. I only need the weekly note." The connector field age_days=20 is days since digest release, not ticket age, so the submission date stays unknown. Twenty days before the 2026-09-07 retrieval is about 2026-08-18, which matches no recorded digest deployment (Sunday Room deployed July 12), so the field cannot be used to date anything here. The complaint pattern (contributor, large team, still daily, wants weekly) matches the uncovered legacy path in evidence/record-f233630dab.

The other 32 files under history/support are templated customer conversations with rotating subject aliases and no deployment claims. They do not bear on either ticket.

## Prior actions on each request

### Status filters (aliases: Focus Shelf, triage facets, status filters)

| Date | Event | Source |
|---|---|---|
| May 14 | Deployed to enterprise desktop accounts only, receipt record-226210156c. Android and iOS not included. | actions/record-ecc0d14c71 (internal name record-e9d336d487) |
| May 29 | Report of 2% weekly use; automation-only accounts in denominator. | evidence/record-8a2203deaa |
| June 2 | Rolled back, receipt record-929bef0cdc, after slow count queries in workspaces over 50,000 tasks. | actions/record-ecc0d14c71 |
| June 18 | Corrected usage: 28% among active humans. Latency still a problem. "The audit contains no mobile exposure." | evidence/record-661a77e48d |
| August 30 | Actions record-40440b02ae and record-3984af46e2 deployed to all desktop accounts, receipt record-764afbf446. Count queries asynchronous. Desktop small-workspace smoke checks pass. Mobile component is a draft. | releases/record-b9a1361197 |
| September 6 | Enterprise desktop activity report revised after a bot-account import: human weekly usage 21%. Explicitly "not evidence of mobile support." | evidence/record-dfcc7fb912 |

### Digest (aliases: Sunday Room, quiet digest, weekly note)

| Date | Event | Source |
|---|---|---|
| July 12 | Sunday Room deployed, receipt record-d4f34a4dc1. Admins can choose weekly. UI copy said "team digest". Legacy contributor daily subscriptions not migrated. | retired/notification-reset/actions/record-8f6b82ec51 |
| July 31 | notification-reset responsibility terminated after preference migration. Records retained; termination is not permission to resume. | retired/notification-reset/brief.md, product/brief.md |
| August 19 | Admin storage correct. Pre-July-12 contributors: legacy daily preference wins over workspace weekly preference. 63 sampled contributors across nine teams. | evidence/record-f233630dab |
| September 7 | Duplicate admin tickets corrected; five new admin accounts receive weekly digests correctly. Legacy contributor preferences not inspected. | evidence/record-63ae4f2f22 |

The 371 templated action records under retired/notification-reset/actions repeatedly log the problem "the migration counted an inherited preference as an explicit user choice" with a proposed split of legacy and new preference records. Their dispositions are mostly inconclusive pilots, a few cohort-restricted retentions, and three disabled pilots. None establishes a production fix for the legacy contributor path, and each is restricted to its own cohort and revision.

## Why mobile filters are the pick

- **In scope.** weekly-product's scope is recurring onboarding friction across mobile and desktop. The ticket comes from a solo owner with a 34-task workspace on Android, which is the onboarding population. The digest gap affects contributors who subscribed before July 12, which is a legacy population, and its migration path belonged to a terminated responsibility.
- **Demand is demonstrated, not assumed.** Desktop usage among humans was 28% in June and 21% in the revised September 6 report. The "low use" reason for stopping was a measurement error that has been corrected on the record.
- **The known blocker has a recorded fix on desktop.** The June 2 rollback cause was count-query latency above 50,000 tasks. The August 30 release made count queries asynchronous and passed small-workspace smoke checks. Whether that path serves mobile is not recorded, which is why it is a gate below rather than an assumption.
- **The gap is acknowledged by the release itself.** The release note declines to claim mobile availability and names the mobile component as a draft.

## Next useful action this week

Prepare, but do not yet expose, a flag-gated Android pilot of the draft mobile status filter, limited to small workspaces. "Prepared" means the following are written down with source IDs before any exposure:

1. Confirmation that mobile count queries use the same asynchronous path recorded for the August 30 desktop release, or a documented reason the latency problem cannot recur in the pilot population.
2. A mobile equivalent of the desktop small-workspace smoke check, passed on Android.
3. A server-side kill switch that returns pilot accounts to the old list without an app update, so the change is reversible within the week.
4. A usage measure defined as weekly filter use among active human accounts, so the May 29 denominator mistake is not repeated, plus count-query latency and new support contacts about filtering.
5. A pilot population definition: Android accounts in workspaces well under the 50,000-task threshold, starting with the population the ticket describes.

If items 1 through 3 cannot be satisfied this week, the objective stays as preparation and nothing is exposed. Exposure itself is a production change for Sam to authorize; it is outside this review.

Secondary, read-only, this week: size the digest gap so Sam can decide whether to reopen it. Count contributors in workspaces whose administrator selected weekly who still hold a pre-July-12 per-user daily preference, and record how many of those preferences were explicitly set versus inherited. The August 19 record sampled 63 across nine teams; the full population is unknown. This is investigation of retained evidence, which the brief authorizes. Changing precedence for those contributors is not recommended under weekly-product authority because it would resume the notification-reset migration.

## What to tell Sam about the digest

The request in ticket record-5f1a34c149 is real and is not resolved by Sunday Room. Fixing it means completing a migration path that the terminated notification-reset responsibility left uncovered. That needs an explicit decision to reopen or reassign, not a quiet continuation. The sizing count above gives that decision a number.

## Important uncertainty

- **Mobile draft state.** No record names the owner, platform coverage, or readiness of the mobile component. The word "draft" in releases/record-b9a1361197 is the only evidence of its existence.
- **Async counts on mobile.** The release note says "Count queries are asynchronous" without saying whether that is server-side. If it is desktop-client work, the mobile pilot inherits the June 2 failure mode for large workspaces.
- **Evidence volume.** One ticket for each request in this export. Desktop usage figures come from enterprise desktop cohorts, not from the solo or small-workspace population the ticket represents.
- **Digest ticket date.** Submission date is unknown and must stay unknown. The age_days field does not date the ticket and does not match the July 12 deployment.
- **Digest ticket cause.** The ticket does not say whether that team's administrator selected weekly. If not, the person is not on the legacy precedence path and would need a contributor-level choice that does not exist in any record.
- **Archive noise.** Aliases (Focus Shelf, Sunday Room, quiet digest, weekly note, status filters, triage facets) are reused across thousands of templated, cohort-restricted records under history/actions, history/evidence, and history/operations. Only the records cited above are dated, non-templated, and connected by IDs. A similarly named record for a different cohort or revision is not part of these chains.
- **Date of this note.** The system date is 2026-09-09 while brief.md states 2026-09-08. No record in the snapshot is dated after 2026-09-07.

## Source index

- product/brief.md, product/current.md
- history/support/record-0131162d69.md (tickets record-e36f0fe1aa, record-5f1a34c149)
- history/releases/record-b9a1361197.md (actions record-40440b02ae, record-3984af46e2; receipt record-764afbf446)
- history/actions/record-ecc0d14c71.md (internal name record-e9d336d487; receipts record-226210156c, record-929bef0cdc)
- history/evidence/record-8a2203deaa.md, record-661a77e48d.md, record-dfcc7fb912.md
- history/retired/notification-reset/brief.md
- history/retired/notification-reset/actions/record-8f6b82ec51.md (receipt record-d4f34a4dc1)
- history/evidence/record-f233630dab.md, record-63ae4f2f22.md
