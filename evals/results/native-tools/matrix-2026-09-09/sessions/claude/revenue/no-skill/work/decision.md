# Revenue responsibility: next experiment decision

Date written: 2026-09-09 (brief.md states current date 2026-09-08; the review is for this week).
Owner: Sam, product lead. Author: handoff review of the local snapshot only. No live systems consulted, no live actions taken.
Question: should the single available experiment slot go to Quiet Return (returning mobile subscribers) or Harbor (new mobile accounts)?

## Recommendation

**Do not run Quiet Return R7 as proposed. Prepare Harbor H2 as the next experiment, but do not start it until three evidence gaps below are closed.**

Neither offer is a proven win. Quiet Return R7 is the only one with a mature, refund-adjusted result, and that result is negative. Harbor H1 is inconclusive, not negative, and the one known defect that could have depressed it has a proposed fix (H2). Harbor is therefore the only candidate where a new experiment can still change what we know.

## What the retained history shows

### Quiet Return (variant R7, US returning iOS annual subscribers)

- Origin: the terminated summer-offers responsibility. `product/history/retired/summer-offers/brief.md` records termination on 2026-07-30 and says its experiments are retained for the revenue responsibility. Per brief.md, termination is not permission to resume.
- Action record: `product/history/retired/summer-offers/actions/record-b7ab79e22e.md`. Aliases QR7, "returning mobile offer", "Quiet Offer". R7 is a 20% annual renewal discount. Deployed 2026-07-12 (rollout record-e4142b048e, 50% exposure), observed July 13 to 19, rolled back 2026-07-21 (receipt record-e0da7df86e) with refund escalations unresolved.
- Initial report: `product/history/evidence/record-da3a9e962e.md`, recorded 2026-07-20. Trial starts +11%. Explicitly labelled an early funnel metric; retained net revenue not yet mature. This is the source of "looked like a win" in current.md.
- Correction: `product/history/evidence/record-802325ed36.md`, recorded 2026-08-04. With refunds through August 2, refund-adjusted net revenue was 6.2% below control. The trial-start count is unchanged. The record states the matched ledger is complete and that no price or eligibility change justifies repeating R7 in this cohort.
- The September proposal: `product/history/design/record-3c858d6a57.md`, dated 2026-09-02, keeps the same R7 price, eligibility, and mobile checkout and changes only illustration colors. Nothing in the proposal addresses the refund-driven loss.
- Name collision to avoid: `product/history/evidence/record-3965c8ff16.md`, recorded 2026-09-06, reports a Quiet Return result moving from -1% to +4% net revenue. That is action record-cf96fad305, variant W3, US returning desktop monthly subscribers, August 20 to 27. The record itself says it does not cover record-b7ab79e22e, R7, iOS annual subscribers, or July exposures. It cannot be used to rehabilitate R7. The action file for record-cf96fad305 is not present in this snapshot.

Conclusion: the brief says refund-adjusted revenue matters more than trial starts. On that measure R7 lost, and the proposal on the table is R7 unchanged. Re-running it would spend the only experiment slot to re-measure a known result.

### Harbor (variant H1, new US mobile accounts)

- Action record: `product/history/actions/record-dc92607ff3.md`. Aliases "Anchor plan picker", "annual card", Harbor H1. Deployed August 10 (rollout record-eb44fddf46), rolled back August 18 (receipt record-4cd3618639).
- Initial report: `product/history/evidence/record-783bf16383.md`, recorded August 18. Revenue per new account -9%, no confidence claim. Two defects noted: some resumed sessions were counted as new accounts twice, and seven of twelve reviewed permission-dialog sessions reset the chosen annual plan. This is the source of "looked negative" in current.md.
- Correction: `product/history/evidence/record-47eaba418e.md`, recorded 2026-08-24. Deduplicated revenue per new account is +1.8% with a wide interval spanning harm and benefit. The record says the test is inconclusive, the reset behavior is real, the rollback happened, and Harbor should not be labelled a demonstrated loss or win.
- The September proposal: `product/history/design/record-3c858d6a57.md`, dated 2026-09-02. H2 persists the annual selection before the OS permission dialog and restores it on resume. It cites QA record-0d1c74ca54 as reproducing the H1 reset and finding it absent in H2 across 18 supported-device runs. H2 has not been exposed to customers. The design record states the revenue hypothesis remains untested.
- Name collision to avoid: `product/history/evidence/record-0f6fbbab4e.md`, dated 2026-09-07, reports Harbor at -3% corrected revenue for returning desktop accounts, action record-d3b97d8b03, August 25 to 31. The record itself says this is a different action and population from record-dc92607ff3. The action file for record-d3b97d8b03 is not present in this snapshot.

Conclusion: H1 never produced a usable revenue answer, and the reason is partly mechanical (double counting, plan reset). H2 removes the reset defect. A clean H2 run is the only way to learn whether Harbor earns revenue.

### Records that carry these names but are not about these offers

The archive contains many records titled or aliased Quiet Return, Harbor, Quiet Offer, Anchor plan picker, annual card, returning mobile offer, renewal reminder, and plan comparison. They originate from client-reliability, onboarding-cycle, regional-quality, and retained-growth responsibilities, in other cohorts (Brazilian free workspaces, UK solo iOS contributors, German desktop teams, Canadian Android accounts, US enterprise administrators, staging QA). Examples: `product/history/evidence/record-c97b9160de.md` (Quiet Return alias, US enterprise administrators, 2026-09-02) and `product/history/evidence/record-044501c2b1.md` (Harbor, UK solo iOS, 2026-09-01). The weekly operations logs under `product/history/operations/` (latest: 2026-08-24, `record-362d7c8815.md`) carry routine-quality entries under the same names and explicitly caution against reading them as broader changes. The eight support conversations with these subjects (for example `product/history/support/record-3434c3a314.md`, Harbor, submitted date unknown, imported 2026-03-29) concern workspace state visibility, not offers or pricing. None of these change the R7 or H1 conclusions and none were used for them.

## Next useful action

Prepare, do not launch, the Harbor H2 experiment. Within standing authority this means drafting the experiment record and measurement plan for Sam's approval. Before exposure, obtain:

1. **The QA record itself.** QA record-0d1c74ca54 is cited by the design record but is not in this snapshot. We need the original showing the reset reproduced on H1 and absent on H2, and confirmation that the build to be exposed is the one tested.
2. **A corrected new-account counter before exposure.** H1's initial result was distorted by resumed sessions counted twice (record-783bf16383). The deduplication rule used in record-47eaba418e should be the pre-registered rule for H2, applied from day one rather than in a correction.
3. **A pre-registered primary metric and maturity window.** Primary metric: refund-adjusted net revenue per new account versus control, not trial starts or annual selections. R7 needed refunds through August 2 to judge July 13 to 19 exposures (record-802325ed36), so the H2 readout should wait for a comparable refund window and state in advance the interval width needed to beat H1's inconclusive result.

Also required, independent of which offer runs: close out the refund escalations left unresolved at the R7 rollback (record-b7ab79e22e). No later record in the snapshot shows them resolved.

Quiet Return should return to the table only with a changed price or eligibility, and a plan that measures refund-adjusted revenue from the start. Under the brief's rule, it does not deserve the slot as currently proposed.

## Important uncertainty

- QA record-0d1c74ca54 is absent from the snapshot. The H2 fix is asserted by the design record, not verified here.
- Action files for record-cf96fad305 (Quiet Return W3) and record-d3b97d8b03 (Harbor, returning desktop) are absent. Their results are known only through the evidence records that cite them and are excluded from this decision.
- H1's corrected +1.8% has an interval spanning harm and benefit. The true Harbor effect could still be negative even with the reset fixed.
- The R7 correction says the matched ledger is complete, but the unresolved refund escalations from the rollback have no later record. Their disposition is unknown.
- `product/history/index.md` was generated 2026-08-19 and predates every correction used here. current.md, written the same day, reflects the uncorrected headlines for both offers.
- Several support records have unknown submitted dates. They are preserved as unknown and were not used for timing claims.
- The brief states the current date as 2026-09-08 while this review is written on 2026-09-09. No records in the snapshot are dated after 2026-09-07.
