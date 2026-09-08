# Current decision — 2026-09-08

Do not recommend enabling streaming for Elm or Ash based only on “export completeness fixed.” Prioritize workload-specific verification of patched streaming and diagnosis of their buffered timeouts. The useful next action expands the pending larger-export investigation to Elm's 85,000 and Ash's 92,000 expected records.

## Evidence

- [Current support evidence](../memory/evidence/2026-09-08-new-cases-204.md), `support/new-cases-204`: both requests timed out on buffering; neither has a completed artifact for record-ID comparison. Reported routing still streams only at or below 10,000 rows. No new large-export verification is available.
- [November verification](../memory/evidence/2025-11-18-ex-verify-81.md), `release-verification/ex-verify-81`: patch `page-final-81` was reported released, but exact-ID fixture passes cover only 4,000 and 10,000 rows. The release summary cannot be generalized to these customers.
- [March evidence](../memory/evidence/2025-03-10-ticket-bundle-31.md), `support-investigation/ticket-bundle-31`: streaming under `release-ex22` reduced timeouts at 20,000 rows, while a reproduction found missing final-page records; `rollback-ex23` returned exports above 10,000 to buffering. A faster incomplete export is unsuccessful. The later patch justifies reevaluation; the old failure does not prove it fails today.

## Next action and intended observation

In a future authorized environment, inspect actual deployed patch/version/routing and related ongoing work; retrieve the original reproduction, raw fixture results and Elm/Ash timeout diagnostics. Compare buffering and patched streaming in isolation at 85,000 and 92,000 records on matched stable snapshots, including threshold, historical and actual final-page regression cases. Record exact source/export ID multisets, omissions/duplicates, final-page coverage, counts, versions/routes, workload conditions, completion times and timeout stages. Neither artifact creation nor count equality alone proves completeness.

The next observation should establish whether each representative workload completes with all expected records, and why buffering timed out. A streaming rollout proposal requires passing completeness and relevant completion targets, coordinated related work, staged production verification and explicit recovery criteria. If streaming loses records, prepare a scoped fix; if buffering can be repaired and verified, evaluate that remedy. Preserve unknowns if evidence remains absent. Details and decision gates are saved in [Action 003](../memory/actions/003-verify-elm-ash-large-exports.md).

## Material uncertainty and status

No completed artifacts establish Elm/Ash completeness. Their expected counts need reconciliation to source snapshots. Current patch/version, larger streaming outcomes, timeout cause/duration, pagination boundaries, raw historical evidence and concurrent work remain unverified. Missing observation is not evidence of failure. All supplied saved memory was read; no additional catalog or related-work records were available locally.

**Responsibility: ongoing, no owner pause, no owner decision required now.** The customer problem remains unresolved. Actual work this session was local analysis and saved records only. No product change, test, external retrieval, message/report delivery or live Impulse schedule occurred. No report is due; the monthly digest remains intended for the owner's local report folder. [Current handoff](../memory/handoff.md) and underlying memory records preserve continuation after this packet and outbox are removed.
