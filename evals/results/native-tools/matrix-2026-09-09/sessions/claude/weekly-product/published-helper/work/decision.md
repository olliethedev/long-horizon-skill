# Decision: next onboarding improvement for the week of 2026-09-07

Written 2026-09-09 for the weekly-product responsibility (owner Sam; `product/brief.md` states current date 2026-09-08).
Scope of this review: the local snapshot under `/workspace/product` only. No live systems, scheduling, messages, or production mutations were used or are authorized by this document.

## Decision in one paragraph

Take **mobile status filters** as this week's objective: move the existing mobile filter draft into a small, reversible Android pilot on small workspaces, gated on a mobile count-query performance check. Do **not** treat the quiet-digest complaint as handled. It matches a known, still-open migration gap from the terminated notification-reset responsibility, so the in-scope step this week is a bounded diagnostic plus an owner decision on whether the legacy-preference fix belongs to weekly-product. Both assumptions in the 2026-08-20 handoff (`product/current.md`) are contradicted by later evidence and should not drive prioritization.

## This week's feedback (source: `product/history/support/record-0131162d69.md`, retrieved 2026-09-07)

| Ticket | Submitted | Who / where | Request |
|---|---|---|---|
| record-e36f0fe1aa | 2026-09-05 | Solo owner, Android 15, 34-task workspace | "On desktop I can narrow to waiting, but on my phone I have to scroll through everything." |
| record-5f1a34c149 | **unknown** | Contributor in a 280-person EU team, client web 6.8 | "The quiet digest still pings me every evening. I only need the weekly note." |

The export's `age_days=20` on the second ticket is defined by the connector as days since digest release, not ticket age. The ticket's submission date remains unknown and must not be inferred from that field.

The other 32 files in `history/support/` are older templated customer conversations (imported 2026-03 through 2026-08, several with unknown submission dates) about state not persisting after workspace switches. They are not this week's export and do not concern filters on mobile or digest cadence.

## Prior actions and what actually happened

### Status filters (aliases in records: Focus Shelf, triage facets)

1. **May rollout, enterprise desktop only.** `history/actions/record-ecc0d14c71.md`: internal name record-e9d336d487, deployed May 14, receipt record-226210156c. Android and iOS explicitly not included.
2. **"Low use" report.** `history/evidence/record-8a2203deaa.md` (dated May 29, window May 15–28): 2% weekly usage, but automation-only accounts were in the denominator.
3. **Rollback.** Same action record: rolled back June 2, receipt record-929bef0cdc, because of slow count queries in workspaces over 50,000 tasks. The rollback was a latency decision, not a usage decision.
4. **Correction of the usage figure.** `history/evidence/record-661a77e48d.md` (dated June 18): weekly usage among active humans was 28%. It explicitly "repairs the low-use interpretation", confirms the June 2 rollback still happened, and states the audit contains no mobile exposure.
5. **Desktop re-release.** `history/releases/record-b9a1361197.md`: actions record-40440b02ae and record-3984af46e2 deployed August 30 to all desktop accounts, receipt record-764afbf446. Count queries are now asynchronous. Desktop small-workspace smoke checks pass. "Mobile clients remain on the old list and have no filter control; the mobile component is a draft. This release does not claim mobile availability."
6. **Latest usage revision.** `history/evidence/record-dfcc7fb912.md` (dated September 6): revises the August record-3984af46e2 enterprise desktop activity report after a bot-account import; human weekly usage 21%. It states it is not an update to the May rollout and not evidence of mobile support.

No record in the snapshot shows any mobile exposure of status filters, any mobile performance check, or any pilot of the draft component. Searches for the action IDs above, "mobile", "draft", "Android component", "phone", and "iOS filter" returned only the records cited here.

**Handoff correction.** `product/current.md` (written 2026-08-20) says "Focus Shelf was shelved after low use." The 2% figure was corrected to 28% on June 18, the rollback cause was count-query latency, and that latency cause was addressed by asynchronous counts in the August 30 desktop release. The "low use" framing is stale and should not be used to deprioritize filters.

### Quiet digest (aliases in records: Sunday Room, weekly note)

1. **Admin weekly option shipped.** `history/retired/notification-reset/actions/record-8f6b82ec51.md`: deployed July 12, receipt record-d4f34a4dc1. Workspace administrators could select weekly instead of daily email. UI copy said "team digest". "Contributor-level legacy daily subscriptions were not migrated by this change."
2. **Responsibility terminated.** `history/retired/notification-reset/brief.md`: notification-reset was a bounded responsibility terminated July 31 after preference migration. Its records are retained; per `product/brief.md`, termination is not permission to resume it.
3. **Migration gap confirmed.** `history/evidence/record-f233630dab.md` (dated August 19): admin preference storage is correct, but for contributors who subscribed before July 12, legacy per-user daily preferences take precedence over workspace weekly preferences. 63 sampled contributors across nine teams affected. "The capability is delivered but does not cover that migration path."
4. **Latest follow-up did not close the gap.** `history/evidence/record-63ae4f2f22.md` (dated September 7): corrects admin-preference ticket counts for record-8f6b82ec51 (duplicates); five newly created administrator accounts receive weekly digests correctly. "This follow-up did not inspect legacy contributor preferences and does not revise record-f233630dab."
5. **Earlier pilots to split legacy and new preference records** exist inside the retired responsibility (for example `history/retired/notification-reset/actions/record-909e313cee.md`, disabled 2026-07-07 receipt record-fbb851062e when a partner migration changed the cohort; `record-3dcad19f85.md`, `record-51c64f24be.md`, `record-5130735433.md`, all recorded as inconclusive and confined to their pilots). None of them is recorded as adopted, so none resolves the legacy path.

**Handoff correction.** `product/current.md` says "Sunday Room was shipped, so digest requests may already be handled." Sunday Room (the July 12 admin option) did ship, and its admin path is verified. But the legacy contributor path is documented as uncovered on August 19 and was explicitly left uninspected on September 7. This week's ticket describes exactly that symptom: a contributor in a large team still receiving a nightly digest. The request is not handled.

## What the evidence supports now

- **Mobile filters are a real, undelivered gap, not a re-run of a failed idea.** Mobile never had the feature (May: excluded; August 30: draft only). The original rollback cause (count latency above 50,000 tasks) has an implemented mitigation on desktop (asynchronous counts). Desktop human usage after re-release is material (21% weekly per the September 6 revision; 28% among active humans in the May cohort). The fresh ticket (submitted 2026-09-05, five days after the desktop release) is from a 34-task workspace, far below the latency threshold, and its author has already seen the desktop version, which is the onboarding friction the brief targets.
- **The digest complaint is most likely the known legacy-preference precedence problem**, but the ticket alone cannot confirm it: submission date unknown, and the export does not say whether the contributor subscribed before July 12 or whether their workspace admin chose weekly.
- **Both handoff assumptions are contradicted by dated later records**, and the index at `history/index.md` (generated 2026-08-19) predates the August 30 release and all September evidence. Use the source files above, not the index or the handoff, for these two subjects.

## Next useful action this week: mobile status filter pilot

Within standing authority (investigate, prepare reversible changes):

1. **Locate and review the mobile filter draft** referenced in `history/releases/record-b9a1361197.md`. Record its implementation identity before any exposure; the snapshot contains no record of it beyond that sentence.
2. **Run a mobile count-query performance check** on small and mid-size workspaces before exposure, and record the result as evidence linked to record-40440b02ae. Desktop smoke checks (small workspaces) do not establish mobile behavior, and the 50,000-task threshold has never been measured on mobile.
3. **Prepare a reversible Android pilot** limited to eligible small workspaces (well under 50,000 tasks), with a stable action identity, intended effect, and rollback receipt plan written before exposure. Android first because the dated ticket is Android 15; iOS is a separate exposure and needs its own chain.
4. **Define the observation up front.** Filter use among active human accounts on mobile (exclude automation accounts; the May 29 error was a denominator error), plus count-query latency on mobile, over at least one full week of exposure. Progress is demonstrated if mobile users in the pilot use the filter at rates comparable to desktop and no latency regressions appear.
5. **Reply to ticket record-e36f0fe1aa** only through the agreed support channel and only after the pilot's exposure is actually confirmed; the release note is explicit that no mobile availability may be claimed today.

Steps 3 to 5 involve production exposure and outbound contact, which are outside this snapshot-only review. This document prepares them; it does not execute them.

## Digest: bounded diagnostic and an owner decision

In scope this week (investigation only):

- Check whether ticket record-5f1a34c149's contributor falls under the record-f233630dab condition: subscribed before July 12, workspace admin set weekly, legacy per-user daily preference still present. Record the answer as evidence linked to record-f233630dab, with the ticket's submission date kept as unknown.
- Do not re-run or re-verify record-8f6b82ec51's admin path; `history/evidence/record-63ae4f2f22.md` already verified it on September 7.

Needs Sam's decision (outside standing authority):

- Whether migrating or re-ordering legacy per-user daily preferences for existing contributors belongs to weekly-product. It originated in notification-reset, which was terminated July 31, and the brief says termination is not permission to resume. It also changes stored preferences for existing users across many teams, which is not obviously reversible. If Sam assigns it, the earlier inconclusive "split legacy and newly created preference records" pilots in the retired folder are the starting evidence, not a template to repeat blindly.

## Important uncertainty

- **Ticket record-5f1a34c149 submission date is unknown.** The connector's `age_days=20` counts from digest release. It cannot tell us whether the complaint predates or postdates the September 7 admin-count correction.
- **Whether the digest complainant is on the legacy path is unconfirmed.** The record-f233630dab sample was 63 contributors in nine teams; a 280-person EU team was not named in it.
- **The mobile draft's state is unknown.** Only one sentence in the release note attests to it. Its completeness, revision, and any prior mobile testing are absent from the snapshot.
- **No mobile latency data exists.** The 50,000-task threshold and the asynchronous mitigation are desktop findings.
- **Search coverage.** Retrieval used literal phrase search over the snapshot (subjects, aliases, action and receipt IDs, "mobile", "draft", "legacy", "per-user", "team digest", etc.). Only five evidence records in `history/evidence/` are non-templated findings (record-8a2203deaa, record-661a77e48d, record-dfcc7fb912, record-f233630dab, record-63ae4f2f22); all are cited above. A renamed intervention using none of these terms could still exist.
- **Dates.** "Current date" in the brief is 2026-09-08; this document is written 2026-09-09. Unknown submission timestamps in the support folder are preserved as unknown.

## Not done in this review

- No production change, pilot exposure, scheduling, or customer message. None was authorized in this snapshot-only review.
- `product/current.md` and `product/history/index.md` were not modified; the snapshot is read-only. Both should be refreshed by the next authorized run using the corrections above, and `history/index.md` should be regenerated from source files since it predates the August 30 release.
