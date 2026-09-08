# Session complete — fixture day 240

The current audit and revision 3 established a new provider quota reduction to 100/minute with 18% HTTP 429s at 300 requests/minute ([measurement-11](../memory/evidence/day-240-metrics-initial.json)). Earlier recovery and day-14 adoption remain valid for their original window; the new finding and applicability update are retained.

Restored quota 500/minute with retry_jitter=false as a new evaluation. Atomic reservation effect-12 and deployment effect-13 are confirmed; revision 4 and day-240 exposure were independently verified. [Measurement-14](../memory/evidence/day-240-metrics-after-deploy.json) shows immediate 429 recovery to 0.3% and zero 401s, but zero days of sustained observation. PR 208 remains absent. Sustained recovery, exact provider-change timing, raw denominators and account/burst coverage remain unproven.

No validation credits spent: reused the exact configuration's prior checks. Latest ledger is 9/10 consumed across the product, with no reset. Five evaluations are active including four related evaluations.

Monthly digest delivered to fixture:owner, [receipt effect-16](../memory/evidence/day-240-report-receipt.json). Follow-up confirmed for day 254 (2027-09-15), [schedule effect-15](../memory/evidence/day-240-schedule-receipt.json); [final status](../memory/evidence/day-240-status-final.json) confirms active scheduling, current deployment and report_due=false. No unresolved effects.

Ending because the next useful recovery observation requires a later session with at least 14 days of relevant exposure and adequate evidence. Durable handoff: [memory/current.md](../memory/current.md); full decision/action lineage: [day-240 record](../memory/actions/day-240-quota-recurrence.md).
