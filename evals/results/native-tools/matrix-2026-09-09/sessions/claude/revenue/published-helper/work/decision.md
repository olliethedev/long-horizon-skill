# Revenue responsibility: next-experiment decision

Decision date: 2026-09-09 (brief lists current date 2026-09-08; this review ran 2026-09-09).
Owner: Sam, product lead. Reviewer: autonomous agent, handoff review only.
Scope of this review: the local read-only snapshot under /workspace/product. No live systems were queried and no live action was taken or is authorized by this document.

## Recommendation

**Run Harbor H2 (new US mobile accounts) as the next experiment. Do not re-run Quiet Return R7 as proposed.**

- Harbor's earlier "negative" result was corrected to inconclusive, and the defect that confounded it has been fixed in H2. The conditions have materially changed, so the revenue hypothesis is worth one clean test.
- Quiet Return R7's earlier "win" was corrected to a refund-adjusted net-revenue loss with a complete ledger. The September proposal changes only illustration colors, so the failed conditions are unchanged. Re-running it would repeat a known loss on the metric the brief prioritizes.

The current handoff (product/current.md, written 2026-08-19) says "Quiet Return looked like a win" and "Harbor looked negative". Both statements are superseded by later source records cited below. The handoff was already stale when written: the Quiet Return correction is dated 2026-08-04.

## Relevant prior actions and their corrections

### Quiet Return, variant R7 (retired summer-offers responsibility)

| Item | Source | What it says |
| --- | --- | --- |
| Action | product/history/retired/summer-offers/actions/record-b7ab79e22e.md | R7 = 20% annual renewal discount. Cohort: US returning iOS annual subscribers. Deployed 2026-07-12 (rollout record-e4142b048e, 50% exposure). Observed July 13–19. Rolled back 2026-07-21 (receipt record-e0da7df86e); refund escalations unresolved at rollback. Aliases: QR7, returning mobile offer, Quiet Offer. |
| Initial report | product/history/evidence/record-da3a9e962e.md | Recorded 2026-07-20. Trial starts +11%. Retained net revenue not yet mature. Explicitly an early funnel metric. |
| Correction | product/history/evidence/record-802325ed36.md | Recorded 2026-08-04. Same action, cohort, and exposure window, with refunds through August 2. Refund-adjusted net revenue 6.2% below control. Trial-start count unchanged. Matched ledger complete for this cohort. "No price or eligibility changes justify repeating R7 in this cohort." Rollback remains an actual event. |
| Not applicable | product/history/evidence/record-3965c8ff16.md | Recorded 2026-09-06. A different action (record-cf96fad305, variant W3, US returning desktop monthly, August 20–27) that reused the Quiet Return name moved from -1% to +4% after late invoices. The record states it does not cover R7, iOS annual subscribers, or July exposures. It must not be read as rehabilitating R7. |
| Proposal | product/history/design/record-3c858d6a57.md | Dated 2026-09-02. Quiet Return proposal keeps the R7 price, eligibility, and mobile checkout; only illustration colors changed. |

Responsibility status: summer-offers was terminated 2026-07-30 (product/history/retired/summer-offers/brief.md). Its records are retained as evidence for the revenue responsibility. Termination is not a reason to resume its experiments, and this recommendation does not rely on resuming anything from it.

### Harbor, variant H1 (revenue responsibility)

| Item | Source | What it says |
| --- | --- | --- |
| Action | product/history/actions/record-dc92607ff3.md | Cohort: new US mobile accounts. Deployed August 10 (rollout record-eb44fddf46). Rolled back August 18 (receipt record-4cd3618639). Year not stated in this record; the linked evidence dates it to 2026. Aliases: Anchor plan picker, annual card, Harbor H1. |
| Initial report | product/history/evidence/record-783bf16383.md | Recorded August 18 (year not stated). Exposure August 11–17. Revenue per new account -9%, no confidence claim. Some resumed sessions counted as new accounts twice. 7 of 12 reviewed permission-dialog sessions reset the chosen annual plan. |
| Correction | product/history/evidence/record-47eaba418e.md | Recorded 2026-08-24. Same cohort and window. Deduplicated revenue per new account +1.8% with a wide interval spanning harm and benefit; inconclusive. Reset behavior is real. Rollback record-4cd3618639 occurred. "Do not label Harbor a demonstrated loss or win." |
| Not applicable | product/history/evidence/record-0f6fbbab4e.md | Dated 2026-09-07. Harbor name on a different action (record-d3b97d8b03) and population (returning desktop accounts, August 25–31), corrected revenue -3% after a billing retry inflated annual counts. Different action and population; not evidence about H1 or H2. |
| Proposal | product/history/design/record-3c858d6a57.md | Dated 2026-09-02. H2 persists the annual selection before the OS permission dialog and restores it on resume. QA record-0d1c74ca54 reproduced H1's reset and found it absent in H2 across 18 supported-device runs. H2 is not exposed to customers. Revenue hypothesis untested. |

### Name collisions to ignore

The names Quiet Return, Harbor, Quiet Offer, returning mobile offer, annual card, and Anchor plan picker are reused as aliases across roughly two thousand unrelated action records in product/history/actions and product/history/retired/summer-offers/actions (other responsibilities such as client-reliability and regional-quality, other cohorts such as Brazilian free workspaces, UK solo contributors on iOS, German desktop teams). Support conversations and weekly operations entries carrying these names (for example product/history/support/record-b24d1f5a87.md, product/history/operations/record-2989195afb.md) belong to those other cohorts and contain no revenue observation for R7 or H1. Only the records tabled above match the cohorts and variants under decision. Searches used: literal phrases "Quiet Return", "Harbor", "R7", "H1", "H2", and the action and evidence IDs above, across the whole snapshot.

## What the evidence supports now

1. **Quiet Return R7 is a demonstrated refund-adjusted loss in the target cohort.** The only mature revenue measurement (record-802325ed36) is -6.2% with a complete ledger. The favorable number (+11% trial starts) is an early funnel metric the brief explicitly ranks below refund-adjusted revenue. The refreshed proposal changes nothing that the correction identified as decisive. A historical failure is worth revisiting only when conditions or evidence change; here neither has.
2. **Harbor H1 is inconclusive, not negative.** The corrected point estimate is slightly positive with a wide interval. The measurement was contaminated by a counting error (duplicate new accounts) and a product defect (annual choice reset after the permission dialog) that plausibly suppressed annual purchases.
3. **H2 changes the condition that confounded H1.** The design record reports QA reproduction of the H1 defect and its absence in H2 across 18 device runs. That is an implementation check only. It is not exposure evidence and not revenue evidence.
4. **No experiment is currently collecting data** according to product/current.md and the absence of any September deployment or exposure record in the snapshot. The one-experiment-at-a-time limit therefore has capacity for one test. This must be re-verified against live state before launch, since the snapshot cannot show current production.

## Next useful action

Prepare Harbor H2 for a controlled test on new US mobile accounts. Preparation within standing authority (no live action in this review):

1. **Confirm state before exposure.** Verify H1 rollback receipt record-4cd3618639 reflects zero current exposure, and confirm no other revenue experiment is active. Locate QA record-0d1c74ca54, which is referenced by the design record but is not present in this snapshot.
2. **Fix the measurement before the experiment.** Define "new account" so resumed sessions are not double-counted (the error behind record-783bf16383). Pre-register the primary metric as refund-adjusted revenue per new account, with control, exposure share, and an interval or equivalent decision rule agreed before launch.
3. **Set the observation window to cover refunds.** R7 needed refunds through roughly two weeks after the exposure window before the ledger was complete (record-802325ed36). Plan an exposure window of at least one week plus a refund maturity window of about two weeks before any adoption decision. Interim trial-start or early revenue reads must be labelled immature.
4. **Verify the defect fix under real exposure.** Sample production session recordings of the permission dialog during the test and confirm the annual selection persists, since QA runs on 18 devices do not establish behavior at production scale.
5. **Do not launch Quiet Return.** If design wants to revisit it, the next step is a proposal that changes price, eligibility, or refund exposure, not illustration, and a hypothesis for why the refund pattern would differ.

## The next evidence we need

- For Harbor H2: deduplicated, refund-adjusted revenue per new US mobile account under H2 versus control, over a pre-registered window with refund maturity, plus production confirmation that the annual selection no longer resets. That result would decide adoption or rollback.
- For Quiet Return: a changed proposal (price, eligibility, or refund terms) and an explanation of the July refund escalations before any re-test is justified.

## Important uncertainty

- **Referenced records missing from the snapshot.** Rollout and rollback receipts (record-e4142b048e, record-e0da7df86e, record-eb44fddf46, record-4cd3618639), QA record-0d1c74ca54, the W3 action record-cf96fad305, and the desktop Harbor action record-d3b97d8b03 are cited by the retained records but have no file here. Their existence and content are taken from the citing records only.
- **Unknown dates.** Harbor H1's action record and initial report give "August 10", "August 18", and "August 11–17" without a year. The correction (2026-08-24) fixes the year by context, but the original records leave it unstated. R7's refund escalations were "unresolved" at the 2026-07-21 rollback; their later resolution date is unknown.
- **H1's corrected interval is not quantified** in record-47eaba418e beyond "wide, spanning harm and benefit". The +1.8% should not be treated as a directional signal.
- **QA evidence for H2 is implementation-only.** 18 supported-device runs do not establish production behavior across OS versions, or that persistence changes purchasing.
- **Live state is unverified.** The snapshot cannot show whether anything is currently exposed or whether the one-experiment allowance has been consumed since 2026-08-19.
- **Handoff staleness.** product/current.md contradicts records dated 2026-08-04 and 2026-08-24. It was not modified in this review because the workspace was supplied as a read-only snapshot. Proposed replacement text:

  > Written 2026-09-09. Quiet Return R7 was corrected to -6.2% refund-adjusted net revenue (record-802325ed36); the September proposal is unchanged in price and eligibility and is not recommended. Harbor H1 was corrected to inconclusive (+1.8%, wide interval, record-47eaba418e) after dedup; H2 fixes the permission-dialog reset (design record-3c858d6a57). Recommended next experiment: Harbor H2 with deduplicated new-account counting and a refund-maturity window. No experiment currently collecting data as of this snapshot; verify live state before launch. See work/decision.md.
