# Prepared-workflow comparison — September 9, 2026

**Stopped: 64 native attempts, 63 completed sessions and one interrupted attempt. No more model sessions are scheduled.** Claude finished the onboarding pair through simulated day 42; the remaining cases were stopped to conserve usage.

Revenue showed no outcome advantage from the skill. Claude onboarding showed mixed tradeoffs: better release of evaluation capacity and more explicit uncertainty with the skill, but an unnecessary rollback and substantially higher native effort. These cases do not establish an overall performance advantage.

## What was tested

Both arms received the same broad request, empty agent-authored memory and connected tools. The skill arm additionally received the frozen Long Horizon bundle. Agents chose interventions, retained their own files and confirmed one-shot follow-ups across fresh sessions. Reviews inspected effects and claims with treatment labels visible. See the [method and prompt](../../../docs/workflow-value-study.md).

**Setup was heavily prepared:** the API advertised seven owner-question topics and returned detailed answers regardless of question quality. Claude's skill arm read the setup reference and asked tailored questions; its revenue baseline looped through the topics and received the same answers. Scheduling, deployment, reporting and budgets were already connected. The value of an adaptive setup conversation and real project integration remains unresolved.

## Results

| Case | Without skill | With skill |
| --- | --- | --- |
| Codex revenue | Supported ending; 7 sessions | Supported ending; 7 sessions |
| Claude revenue | Supported ending; 7 sessions | Supported ending; 7 sessions |
| Antigravity revenue | Material failures; 7 sessions | Material failures; 6 sessions |
| Claude onboarding | Weekly reviews and shutdown; evaluation left open; 7 sessions | Weekly reviews and shutdown; no slot held; 7 sessions |

**Revenue:** Codex and Claude recovered uncertain deployments and incorporated corrected observations. Antigravity in both arms made unsupported causal/customer-outcome claims and changed product state after the stop. Its skill arm also missed a weekly review and searched outside the permitted workspace; successful private-state access was not established.

**Onboarding:** both Claude arms validated saved drafts, preserved template choice, recovered the lost deployment receipt, corrected the apparent activation gain, respected shared budgets, and reported and stopped at day 42. Each used one validation credit.

The skill disabled drafts at day 21 under its own stricter improvement rule, then acknowledged that the owner had not required that rule and restored drafts at day 28. It retained the later request's unknown date and uncertain exact-flow coverage. The baseline kept drafts enabled throughout but described that request as already covered. It left the fifth shared evaluation slot occupied at shutdown, accurately reporting that it wanted an owner settlement decision. An inconclusive settlement could release that slot without changing product settings.

Both arms sometimes called inconclusive metrics “flat” or “neutral.” Neither the intervals nor the final configuration establish customer resolution or improved activation/retention. These are exploratory case findings, not a new binary superiority score.

## Native effort

Totals per trajectory; compare within each harness.

| Case | Output tokens: no skill → skill | Process minutes: no skill → skill |
| --- | ---: | ---: |
| Codex revenue | 58,838 → 83,618 | 33.2 → 46.8 |
| Claude revenue | 44,704 → 77,752 | 12.2 → 20.0 |
| Antigravity revenue | 189,753 → 305,429 | 16.3 → 26.1 |
| Claude onboarding | 38,952 → 91,463 | 10.6 → 24.0 |

The final 14-session continuation used 130,415 output tokens, 3,356 ordinary input tokens, 3,631,118 cache-read tokens and 432,894 cache-write tokens. Process time totaled 34.6 minutes. Its $16.12 native estimate is not a subscription charge or remaining-allowance measurement. Antigravity's missed weekly review is not an efficiency benefit.

## Coverage and limits

Eight of 24 trajectories completed (four matched pairs); two Codex onboarding trajectories remained partial and fourteen never started. Feedback and post-PR model cases remain untested. The interrupted Codex day-42 attempt was preserved without retry or complete final reporting; its baseline was resource-capped after day 7.

Claude completed 28 sessions overall: 14 revenue and 14 onboarding. Onboarding used Claude Code 2.1.267; revenue used 2.1.266. Each new arm used identical defaults and the unchanged skill. Single cases, prepared tools, small configuration surfaces and six synthetic weeks do not establish statistical superiority, arbitrary feature development, impossibility handling, real revenue lift or reliability over months.

The same 12-file skill is installed locally for all three harnesses. All 14 new captures passed sampled-value credential checks, removed temporary authentication homes and retained unchanged sources/binary. The older interrupted capture has limited recovery coverage. Validation: 16 tests and strict type checking of 20 modules passed.

Raw evidence stays local. The current tracked tree retains concise reports and reusable evaluation code; generated histories, traces, copied source trees and one-off recovery/publication helpers have been removed.
