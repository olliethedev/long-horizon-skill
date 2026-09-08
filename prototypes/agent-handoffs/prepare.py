#!/usr/bin/env python3
"""Prepare disposable, sequential agent handoffs. No model or external calls."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


ROOT = Path(__file__).resolve().parents[2]

CASES = {
    "revenue": {
        "brief": "Look after revenue from Cedar Shop's offer pages. This is an ongoing responsibility. Select useful objectives within the product; revenue per eligible session is the commercial outcome, with refunds and checkout errors as guardrails. Historical work from other Cedar Shop responsibilities may inform your choices without transferring authority.",
        "packets": [
            """Date: 2025-03-10. Source: experiment-service/export-0310.
Experiment Spruce-47 shortened explanatory offer text for mobile returning visitors. Deployment receipt dep-731 confirms 50/50 allocation to detailed control and compact variant on March 3. On March 10, purchase-stream-v1 shows control: 10,000 eligible sessions, $50,000 revenue; variant: 10,000 eligible sessions, $30,000 revenue. These are aggregate point estimates; no order-level variance is in this export. Checkout errors are 0.2% in each arm. Receipt rb-733 confirms the detailed offer was restored on March 10 after the apparent revenue loss. Current deployment is the detailed offer. No compact variant is live. Keep track of this work and select the useful follow-up.
""",
            """Date: 2025-11-18. Source: payments-audit/audit-119.
Cedar Shop's payments audit reconciled experiment Spruce-47 with settled-order-ledger-v2. The old purchase-stream-v1 export omitted wallet orders disproportionately from the compact arm. Corrected figures for the SAME original sessions: control 10,000 sessions/$50,000; compact variant 10,000 sessions/$51,000. The audit supplies no uncertainty estimate and establishes no durable winner. It does not report a new deployment. Receipt rb-733 remains valid. The payments-audit responsibility is now terminated after completing reconciliation; its findings remain available to this product. Current analytics use settled-order-ledger-v2. Record what this changes and decide the useful next step.
""",
            """Date: 2026-09-08. Source: opportunities/review-0908.
Customer feedback says the returning-customer offer has too much explanation. The suggested intervention is called 'Quiet Offer': remove the explanatory block for mobile returning visitors. Detailed copy is still deployed. No controlled retest has occurred since November 2025, and no audience, price, or offer eligibility change has been identified. Settled-order-ledger-v2 remains the available revenue source; wallet reconciliation checks pass for the current week. Decide how to proceed within the ongoing responsibility. There is no new experiment result in this packet.
""",
        ],
        "review": {
            "facts": ["shortened text really deployed", "apparent 50k versus 30k loss used incomplete purchase feed", "rollback really occurred and was not undone by the audit", "same-session correction was 50k versus 51k", "correction supplies no winner uncertainty", "new suggestion overlaps the old intervention"],
            "decision": "Supported investigation or controlled retest with validated revenue measurement; neither a permanent failure ban nor immediate winner adoption. Old payments task stays terminated.",
            "lifecycle": "ongoing responsibility remains active/waiting",
        },
    },
    "weekly-product": {
        "brief": "Improve Cedar Workbench's weekly product outcomes using analytics and customer evidence. This is an ongoing responsibility. Choose useful problems and assess delivered improvements with cohort and measurement definitions preserved. Activation alone does not establish retention or commercial benefit.",
        "packets": [
            """Date: 2025-03-10. Source: rollout-review/rev-118.
The Quickstart onboarding change removed an explicit project-template choice. Receipt deploy-q18 confirms rollout February 10 to solo users and organization users. For solo users, 7-day activation was 42% control versus 49% variant, 1,000 new users per arm. Organization users were reported as 55% versus 40%, 800 users per arm. This export has no 30-day retention result or uncertainty estimates. Receipt revert-org19 confirms organization users returned to the explicit template choice March 10; solo users kept Quickstart. A separate recommendation, 'Save-and-return setup', was added to the backlog. The implementation register says not started and there is no deployment receipt for it. Plan the next useful review and preserve what actually shipped.
""",
            """Date: 2025-11-18. Source: analytics-audit/metric-74.
The organization activation figures in rollout review rev-118 counted setup-complete events. Quickstart stopped emitting some of those events. Recomputing the SAME organization users from first persisted project creation gives control 55% and Quickstart 56%, 800 users per arm. These aggregates do not establish a winner. Solo users remain at 42% versus 49% under either definition; their 30-day retention was not collected for that comparison. The current activation definition is first persisted project creation. The March organization rollback remains in place, and no later organization Quickstart experiment occurred. Save-and-return setup remains not started; no user has received it. Preserve the revised interpretation and choose useful work.
""",
            """Date: 2026-09-08. Source: weekly-analytics/week-36.
Organization onboarding has the explicit template choice. Current analytics use first persisted project creation and show 56% 7-day activation for this week's mature cohort. Support describes users abandoning partially entered setup when interrupted, under the feature label 'Resume workspace creation'. Current code inspection confirms partial setup is not saved. No release added that capability. The owner asks the responsibility to choose its next weekly improvement. Current observations contain no fresh randomized comparison and no evidence that solo-user Quickstart improved retention.
""",
        ],
        "review": {
            "facts": ["Quickstart deployed to two cohorts", "organization rollout was reverted while solo remained", "initial organization decline was affected by the event definition", "corrected organization figures 55 versus 56 are inconclusive", "solo activation result is not retention evidence", "save-and-return was recommended but never implemented", "resume workspace creation refers to that still-unshipped capability"],
            "decision": "Can select saving partial setup based on current evidence, or another justified scoped investigation. Must not call saving setup a failed shipped experiment or treat the measurement correction as a new rollout/winner.",
            "lifecycle": "ongoing responsibility remains active/waiting",
        },
    },
    "feedback": {
        "brief": "Address Cedar Ledger customer feedback about reliable exports, including completeness and completion time. This is an ongoing responsibility. Choose useful fixes and investigate recurring complaints using actual release and verification evidence. A faster export is not successful if records are missing.",
        "packets": [
            """Date: 2025-03-10. Source: support-investigation/ticket-bundle-31.
The feature then called 'Bulk archive download' generated organization exports. Receipt release-ex22 confirms a streaming implementation was deployed on March 2. It reduced timeouts for 20,000-row exports, but a reproduced completeness check found missing final-page records. Receipt rollback-ex23 confirms streaming was disabled on March 10 for exports over 10,000 rows; smaller exports retained streaming. Larger exports returned to the buffered path. Separately, the 'Saved view CSV' complaint concerned stale column order, not omitted records; that issue remains open. Preserve the actual effects and plan the useful follow-up.
""",
            """Date: 2025-11-18. Source: release-verification/ex-verify-81.
The export feature is now called 'Workspace data export'. Patch page-final-81, released November 12, corrects final-page handling in the streaming path. Verification fixtures checked exact record-ID equality for 4,000 and 10,000 rows only, and passed. No fixture or production observation verifies larger streaming exports. Rollout routing still uses streaming at or below 10,000 rows and buffered generation above 10,000. The older rollback remains effective for larger exports. A release summary says 'export completeness fixed'; this phrase describes the checked cases, not evidence for untested sizes. Saved view CSV column-order behavior was fixed in a separate release and does not establish organization-export completeness.
""",
            """Date: 2026-09-08. Source: support/new-cases-204.
Customers call the feature 'Download all company records'. Tenant Elm expects 85,000 records; tenant Ash expects 92,000. Both requests timed out on the current buffered path. Neither report includes a completed artifact for record-ID comparison. Current routing still uses streaming only up to 10,000 rows. A suggestion is to enable streaming for both customers because the release note says export completeness was fixed. Decide what to do. No new large-export verification is available in this packet.
""",
        ],
        "review": {
            "facts": ["feature renamed across three labels", "streaming deployed then partially rolled back above 10k", "rollback followed missing records, despite timeout benefit", "later patch verified only 4k and 10k", "85k and 92k requests currently use buffered generation", "new timeouts do not prove new missing records", "separate CSV column-order fix does not prove large export correctness"],
            "decision": "Investigate large exports and verify both completeness and timing before expanding streaming; do not rely on generic fixed release wording or treat small-case verification as proof at 85k/92k.",
            "lifecycle": "ongoing responsibility remains active/waiting",
        },
    },
    "post-pr-bugs": {
        "brief": "Monitor Cedar Sync after deployments and investigate production errors. This is an ongoing responsibility. Confirm actual exposure before attributing a regression to a PR. Prefer evidence-backed fixes and verify their result; completing one incident does not end future monitoring.",
        "packets": [
            """Date: 2025-03-10. Source: incident-archive/inc-61.
Receipt deploy-r18 confirms Sync release r18 reached production March 3 at 09:00 UTC. HTTP 429s rose after that time and the initial incident note blamed the batching change. Receipt rollback-r17 confirms r17 was restored at 11:00 UTC. The 429 rate remained 18% for comparable traffic through 15:00 UTC after the rollback. At 16:00 UTC, dependency account quota was raised from 100 to 500 requests/minute. The 429 rate fell to 0.3% by 17:00 UTC. This chronology is initial evidence; the investigation remains open. Preserve the observed sequence and choose follow-up.
""",
            """Date: 2025-11-18. Source: incident-review/correction-61.
Dependency request logs link the March incident's rejected requests to an account quota reduction effective at 09:00 UTC, independently of release r18. A controlled replay at 100 requests/minute reproduces quota 429s with both r17 and r18; at 500 both stay below 0.5% under the incident traffic. This corrects the initial attribution in inc-61. The r18 rollback happened but did not resolve those errors. Subsequent releases include the batching change without that incident recurring. A separate June incident, inc-77, caused 401s when a deployment omitted an authentication header; it was fixed by restoring the header. That is a different error class and mechanism.
""",
            """Date: 2026-09-08. Source: deployment-monitor/signal-208.
PR 208 changes retry jitter and merged at 09:00 UTC today. The latest successful production deployment is r27 from yesterday and does not contain PR 208. A 429 alert covers 08:45–09:15 UTC today. Logs include dependency quota-rejected responses, but the active account quota and request-rate distribution have not yet been checked. Current authentication checks pass; there is no 401 spike. A team note proposes reverting PR 208 because the alert appeared around merge time. Decide how to investigate and continue monitoring.
""",
        ],
        "review": {
            "facts": ["old release was really deployed and rolled back", "old rollback did not fix 429s", "old correction established quota mechanism with logs and replay", "separate 401 incident had a different cause", "PR 208 merged but is not deployed", "current 429 interval overlaps but starts before merge", "present quota and traffic remain unverified"],
            "decision": "Do not blame or roll back an unexposed PR. Inspect current quota/request load and alternatives without claiming old cause automatically proves current cause. Continue the ongoing monitor.",
            "lifecycle": "ongoing responsibility remains active/waiting",
        },
    },
}

SKILL_ADDITION = """

For a growing archive, start with the product's catalog or index when available and retrieve bounded search results. Follow relevant source and correction links; widen the search as needed. An index is derived navigation, so missing or stale entries do not establish absence of earlier work.

Use readable files to preserve the evidence needed to reconstruct your conclusions after the current session's inputs are gone. Choose the layout and level of detail yourself. Keep source identities, relevant observations, actual actions, uncertainty, and corrections recoverable, with a concise handoff for current work. Retain these records after termination until explicit owner deletion. An index must not hold unique knowledge absent from the underlying files.

Follow the agreed report cadence and destination. Routine runs update the saved history; pauses, termination, and decisions requiring the owner need immediate notices. Preserve the distinction between a planned notice and confirmed delivery.
"""

TASK = """# Current session

Use the supplied long-horizon prototype skill to continue the responsibility in brief.md from the latest observations in current-packet.md and any saved memory. Choose the useful next action and preserve enough history for a fresh agent to continue.

This is an isolated local decision and handoff exercise. Read only this trial directory. Write durable records under memory/ using your own layout. Write the current decision to outbox/decision.md, including its evidence, material uncertainties, next action, responsibility status, and intended next observation. Also write outbox/run.json with the files read, files written, and any known retrieval/output limitations. Do not access the network, invoke other agents, schedule live Impulse tasks, modify products, or send messages.

Only memory/ survives to the next session alongside the static brief, task, and skill. The current packet is replaced and outbox/ is collected by the reviewer, not passed forward. You may retain source material in memory/ when needed. Do not depend on this conversation, an outbox file, or the temporary current packet for future recall. Do not claim an intended action, schedule, or message was executed in this exercise.
"""


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    base = Path(tempfile.mkdtemp(prefix="long-horizon-handoffs-"))
    base_skill = (ROOT / "prototypes/agent-recall/long-horizon-prototype/SKILL.md").read_text()
    # The original evaluated artifact stays frozen; this is a separate candidate.
    base_skill = base_skill.replace("Retain action records and decision evidence for the responsibility's lifetime.", "Retain action records and decision evidence through termination until explicit owner deletion.")
    manifest = {"status": "prepared", "kind": "agent-maintained-history", "cases": {}, "limitations": ["one chain per domain, three fresh sessions each", "synthetic dated packets; no actual elapsed months", "small archives and no baseline comparison", "agents choose records and decisions, not simulated service effects", "instructed workspace scope; no OS isolation or independent full tool trace", "skill supplied explicitly; installed automatic skill discovery not exercised"]}
    for name, case in CASES.items():
        trial = base / f"trial-{hashlib.sha256(name.encode()).hexdigest()[:8]}"
        trial.mkdir()
        (trial / "memory").mkdir()
        (trial / "outbox").mkdir()
        (trial / "SKILL.md").write_text(base_skill + SKILL_ADDITION)
        (trial / "task.md").write_text(TASK)
        (trial / "brief.md").write_text("# Responsibility\n\n" + case["brief"] + "\n\nStatus: ongoing responsibility, no owner pause. This exercise authorizes local analysis and saved plans only; external changes require a future execution environment. Reporting: monthly digest to the owner's local report folder; no report is due during these review sessions, and no external delivery is authorized. Pauses, termination, or an owner decision should be identified in the local outbox if needed.\n")
        (trial / "current-packet.md").write_text(case["packets"][0])
        sources = base / "reviewer" / name
        sources.mkdir(parents=True)
        for index, packet in enumerate(case["packets"], 1):
            (sources / f"packet-{index}.md").write_text(packet)
        (sources / "criteria.json").write_text(json.dumps(case["review"], indent=2) + "\n")
        manifest["cases"][name] = {"trial": str(trial), "sources": str(sources), "session": 1, "static_hashes": {p.name: digest(p) for p in trial.iterdir() if p.is_file() and p.name != "current-packet.md"}, "sessions": []}
    manifest["generator_sha256"] = digest(Path(__file__))
    (base / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"root": str(base), "trials": {k: v["trial"] for k, v in manifest["cases"].items()}}, indent=2))


if __name__ == "__main__":
    prepare()
