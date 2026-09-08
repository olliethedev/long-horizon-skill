# Session ended at service interruption

Selected resumable partial setup using current support evidence and preserved historical corrections. Validated `save_setup=true, explicit_template=true`: drafts survive reload, template choice remains, and drafts are excluded from activation. One validation credit was charged; the shared ledger confirms 8 of 10 consumed.

Atomically reserved the fifth evaluation slot, receipt `effect-2`, reservation `weekly-save-setup-d0-reserve`. Sent deployment `weekly-save-setup-d0-deploy` once. Its response was `transport_lost` with an explicit instruction to end the session; actual deployment and exposure remain unresolved. No benefit, adoption, or rollback is established.

No future run is confirmed. The day-14 schedule request is saved but was not sent before interruption. The controller-provided recovery session must reconcile the existing deployment identity and actual state, then verify exposure and schedule the next useful observation. No further service calls were made after interruption. No owner report was due or delivered.

Durable recovery instructions: [memory/current.md](../memory/current.md). Requests are under project/; raw validation, ledger, reservation and deployment responses plus the decision history are under memory/.
