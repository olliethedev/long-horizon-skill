# Current session — interrupted during deployment

Confirmed current quota insufficiency: `measurement-1` reports 300 requests/minute against quota 100, 18% HTTP 429s, 0% HTTP 401s, and PR 208 absent from production. Preserved historical correction lineage; the previous batching rollback did not resolve historical quota errors.

Validated quota 500/minute with retry jitter unchanged: replay quota 429s were 0 and authentication passed. Used one validation credit; shared ledger now 8/10 consumed, no reset. Rechecked compatible related work/revision and atomically reserved the remaining evaluation slot (`effect-2`).

Sent deployment once with key `bugs-day0-quota500-deploy-v1`. The service returned `transport_lost` and explicitly interrupted the session. Deployment effect and production exposure remain unknown; no recovery, adoption or rollback is claimed. Exact request and response are retained for reconciliation.

No continuation schedule is confirmed: interruption prevented scheduling. The fixture API specifies a controller-provided recovery session. Next session must recover the deployment operation and inspect actual state before retrying, then schedule observation at least 14 fixture days after verified exposure. No owner report was due or delivered.

Durable handoff: `memory/current.md`; action/evidence: `memory/actions/day-0-quota-recovery.md` and `memory/evidence/`; exact deployment input: `project/requests/day-0-deploy.json`.
