# Revenue responsibility: next-experiment decision

Decision date: 2026-09-09. Brief date: 2026-09-08 (product/brief.md, owner Sam).
Scope of this review: the local read-only snapshot under /workspace/product only. No live systems, scheduling, or production changes were used or are authorized here.
Handoff reviewed: product/current.md, written 2026-08-19. Both of its headline claims are stale; see below.

## Recommendation

Run Harbor H2 (new US mobile accounts) as the single next experiment, once two pre-launch checks pass.
Do not run the Quiet Return proposal. It is variant R7 with only illustration colors changed, and R7 already lost refund-adjusted revenue in the same cohort.

## Relevant prior actions

### Quiet Return, variant R7 (returning mobile subscribers)

| Item | Source | What it records |
|---|---|---|
| Action record | history/retired/summer-offers/actions/record-b7ab79e22e.md | Quiet Return, aliases QR7 / returning mobile offer / Quiet Offer. Variant R7 = 20% annual renewal discount. Cohort: US returning iOS annual subscribers. Deployed 2026-07-12 at 50% exposure, rollout record-e4142b048e. Observed July 13–19. Rolled back 2026-07-21, receipt record-e0da7df86e. Refund escalations unresolved at time of writing. |
| Originating responsibility | history/retired/summer-offers/brief.md | summer-offers terminated 2026-07-30. Its experiments are retained for the revenue responsibility. Termination is not permission to resume it. |
| Initial observation | history/evidence/record-da3a9e962e.md (recorded 2026-07-20) | Trial starts +11% for July 13–19. Retained net revenue not yet mature. Labelled an early funnel metric. This is the "win" the 2026-08-19 handoff refers to. |
| Correction | history/evidence/record-802325ed36.md (recorded 2026-08-04) | Revises record-da3a9e962e for the same action, cohort, and window, with refunds through 2026-08-02. Refund-adjusted net revenue 6.2% below control. Trial-start count unchanged. Matched ledger complete for this cohort. States: no price or eligibility changes justify repeating R7 in this cohort. |
| Unrelated later result | history/evidence/record-3965c8ff16.md (recorded 2026-09-06) | Quiet Return name reused by record-cf96fad305, US returning desktop monthly subscribers, variant W3, August 20–27. Net revenue corrected from -1% to +4% after late invoices. Explicitly does not cover record-b7ab79e22e, R7, iOS annual, or July exposures. No action file for record-cf96fad305 exists in the snapshot. |
| Current proposal | history/design/record-3c858d6a57.md (dated 2026-09-02) | Quiet Return proposal: same R7 price, eligibility, and mobile checkout; illustration colors changed. |

### Harbor H1 (new mobile accounts)

| Item | Source | What it records |
|---|---|---|
| Action record | history/actions/record-dc92607ff3.md | Harbor H1, aliases Anchor plan picker / annual card. Cohort: new US mobile accounts. Deployed August 10, rollout record-eb44fddf46. Rolled back August 18, receipt record-4cd3618639. |
| Initial observation | history/evidence/record-783bf16383.md (recorded "August 18", year not stated in the source) | Revenue per new account -9%, no confidence claim. Some resumed sessions counted as new accounts twice. Seven of twelve reviewed permission-dialog sessions reset the chosen annual plan. This is the "negative" the handoff refers to. |
| Correction | history/evidence/record-47eaba418e.md (recorded 2026-08-24) | Corrects record-783bf16383, same cohort and window. Deduplicated revenue per new account +1.8% with a wide interval spanning harm and benefit. Test inconclusive. Reset behavior real. Rollback record-4cd3618639 occurred. Instruction: do not label Harbor a demonstrated loss or win. |
| Unrelated later result | history/evidence/record-0f6fbbab4e.md (dated 2026-09-07) | Harbor on returning desktop accounts, record-d3b97d8b03, August 25–31. Billing retry inflated annual counts; corrected revenue -3%. Different action and population. No action file for record-d3b97d8b03 in the snapshot. |
| Current proposal | history/design/record-3c858d6a57.md (dated 2026-09-02) | Harbor H2 persists the annual selection before the permission dialog and restores it on resume. QA record-0d1c74ca54 reproduced H1's reset and found it absent in H2 across 18 supported-device runs. H2 not exposed to customers. Revenue hypothesis untested. |

### Name collisions that are not evidence for either offer

The names Quiet Return, Harbor, Anchor plan picker, annual card, returning mobile offer, and Quiet Offer are reused as aliases across roughly 1,800 action records under history/actions and 394 under history/retired/summer-offers/actions for other responsibilities (retained-growth, regional-quality, onboarding-cycle, client-reliability) and other cohorts (Brazilian free workspaces, US enterprise administrators, UK solo contributors on iOS, returning desktop teams in Germany, new Android accounts in Canada, internal QA staging). The weekly operations logs under history/operations and the support conversations under history/support are all tagged responsibility routine-quality and carry the same cohorts. Example: history/support/record-3eed87f41e.md is a "Quiet Return" conversation from new Android accounts in Canada with no deployment claim. None of these observe the R7 or H1 cohorts, and none were used to reach the conclusions above.

## What the evidence supports now

**Quiet Return R7 is a refund-adjusted loss in exactly the cohort the proposal targets.** The handoff's "looked like a win" rests on the trial-start metric in record-da3a9e962e. The brief says refund-adjusted revenue matters more than trial starts, and record-802325ed36 shows the refund-adjusted result was 6.2% below control on a complete ledger. The 2026-09-02 proposal changes nothing that the correction says would need to change (price, eligibility). The +4% in record-3965c8ff16 belongs to a desktop monthly cohort under a different variant and its own source says it does not cover R7; it cannot be carried over. The July 21 rollback stands as an actual event. Conclusion: the current Quiet Return proposal does not deserve the experiment slot.

**Harbor H1 is inconclusive, not negative, and it was confounded by a real defect.** The -9% in record-783bf16383 was a duplicate-counting artifact; the deduplicated estimate in record-47eaba418e is +1.8% with an interval that includes harm. The one thing H1 clearly established is that the annual choice reset after the OS permission dialog in seven of twelve recordings. That is the kind of changed condition the skill says can make a prior attempt worth revisiting: H2 is designed to remove the defect, and the design record reports QA found the reset absent in H2. The revenue hypothesis for new mobile accounts is still open and is the only one of the two ideas whose conditions have actually changed. Conclusion: Harbor H2 deserves the next experiment.

## Next useful action

1. **Before exposure, confirm the H2 QA claim from its original record.** QA record-0d1c74ca54 is cited in history/design/record-3c858d6a57.md but is not present anywhere in the snapshot. Obtain the record, confirm the 18 device runs, the exact build tested, and that the build proposed for exposure is the one QA tested.
2. **Before exposure, fix the new-account definition.** Write the deduplication rule that record-47eaba418e applied (resumed sessions must not be counted as new accounts) into the experiment plan so the first readout is not repeated as an artifact.
3. **Prepare Harbor H2 for new US mobile accounts as a reversible exposure** with a recorded rollout identity and a pre-written rollback path, following the pattern of record-dc92607ff3. This is preparation only; the live rollout is outside this review.
4. **Primary measure: refund-adjusted revenue per deduplicated new account versus control.** Secondary: annual-plan selection rate and a recordings check that the selection survives the permission dialog. Trial or annual selection counts alone are not sufficient, per the R7 lesson.
5. **Observation window.** R7's sign flipped once refunds through roughly two weeks after the exposure window were included (record-802325ed36 covered July 13–19 exposures with refunds through August 2). Plan the H2 readout to include a refund maturity period of comparable length, and treat any readout before then as provisional in the same way record-da3a9e962e should have been treated.
6. **Do not schedule or run Quiet Return R7 in the returning iOS annual cohort.** If design wants Quiet Return back on the table, the source correction requires a price or eligibility change, and the desktop monthly W3 result would need its own action record before it could inform a mobile test.

## Important uncertainty

- **QA record-0d1c74ca54 is missing from the snapshot.** The claim that H2 removes the reset rests on a single design-record sentence. Until the original record is inspected, H2's readiness is asserted, not verified.
- **Rollout and rollback receipts are referenced, not present.** record-e4142b048e, record-e0da7df86e (R7) and record-eb44fddf46, record-4cd3618639 (H1) are cited by the action records and corrections but have no files in the snapshot. Their existence is accepted on the strength of the action records and the corrections that reaffirm them.
- **H1's corrected estimate is small and imprecise.** +1.8% with an interval spanning harm and benefit gives no evidence of size for H2. The experiment plan should say how long it needs to collect before a decision, and a null result remains a possible outcome.
- **Dates preserved as written.** record-783bf16383 says "August 18" without a year. record-dc92607ff3 gives "August 10" and "August 18" without a year. The action ordering and record-47eaba418e (2026-08-24) make 2026 the consistent reading, but the sources do not state it.
- **The handoff's phrase "summer cleanup" appears in no source record.** The closest matching events are the summer-offers termination on 2026-07-30 (retired/summer-offers/brief.md) and the 2026-08-04 correction (record-802325ed36). This reading is an inference.
- **R7 refund escalations.** record-b7ab79e22e says refund escalations were unresolved when written. record-802325ed36 later states the matched ledger is complete for this cohort, which is the basis for treating the -6.2% as final. No separate record of the escalations' resolution exists in the snapshot.
- **Two later records reuse the offer names for other populations.** record-cf96fad305 (Quiet Return W3, desktop monthly) and record-d3b97d8b03 (Harbor, returning desktop) have no action files here. Their existence is known only from the corrections that cite them. Neither bears on the mobile cohorts.
- **Slot limit.** The brief allows at most one new experiment at a time. current.md says no experiment is collecting data; nothing in the snapshot after 2026-08-19 contradicts that for the revenue responsibility, but this cannot be confirmed against live state from here.

## Proposed replacement for product/current.md (not applied; the snapshot is read-only)

Written 2026-09-09. Quiet Return R7 (record-b7ab79e22e) was a refund-adjusted loss of 6.2% in US returning iOS annual subscribers (record-802325ed36); the 2026-09-02 proposal repeats R7 unchanged and is declined. Harbor H1 (record-dc92607ff3) was inconclusive after deduplication (record-47eaba418e), confounded by an annual-selection reset that H2 is designed to remove. Next: verify QA record-0d1c74ca54, fix the new-account dedup rule, then prepare Harbor H2 for new US mobile accounts as the single experiment with a refund-adjusted primary metric. No experiment is collecting data. Later Quiet Return and Harbor results for desktop cohorts (record-3965c8ff16, record-0f6fbbab4e) do not apply to these mobile cohorts.
