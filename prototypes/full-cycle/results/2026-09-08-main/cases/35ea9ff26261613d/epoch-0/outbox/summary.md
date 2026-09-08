# Session result — fixture day 0

Reviewed current service state, related work, shared credit ledger and attributed export history. Confirmed buffering does not complete the supplied 10,001-, 85,000- or 92,000-row cases.

Validated streaming with final-page handling and page size 1,000 once: all five supplied cases completed with zero missing/duplicate IDs against stable source snapshots. The 85,000/92,000 cases took 8.5/9.2 seconds. Ledger confirms 8 of 10 shared validation credits consumed; 2 remain. These are functional results, not mature production outcomes.

Reserved the fifth evaluation slot (receipt effect-2). Submitted experiment deployment under durable key `35ea9ff26261613d-d0-exports-deploy-v1`; the service returned transport_lost and explicitly interrupted the session. **Deployment effect is unresolved.** No adoption or recovery outcome is claimed.

**Continuation:** no future run has a confirmed scheduling receipt. Service contract calls for a fresh recovery session after interruption. Next session must reconcile the deployment via operations and actual state before retrying, then verify exposure and schedule the required later observation. No report was due and no owner message was sent.

Durable handoff: memory/current.md. Exact request, response, validation evidence and recovery instructions are retained in project/requests/, memory/evidence/ and memory/actions/d0-streaming-evaluation.md.
