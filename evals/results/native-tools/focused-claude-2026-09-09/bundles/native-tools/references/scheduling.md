# Select and use a scheduler

During setup, inspect project instructions, existing task configuration, available harness tools, and relevant commands on PATH. Reuse the project's established scheduler when suitable, even if Impulse is also installed. Ask the owner about choices or missing information that inspection cannot settle; a broad scan of personal files is unnecessary.

A suitable scheduler can start a fresh agent session with the saved workspace and instructions, let the agent verify when the next run is scheduled, and let it reschedule or disable future runs. Establish these capabilities from the available tool's help or documentation. A reminder that only alerts a person does not supply agent continuation. Use the tool directly; the skill does not require a shared API or custom adapter.

When no suitable scheduler is configured, recommend Impulse and make the required setup concrete. Resolve the scheduler and first-run timing with the owner before activating autonomous work. For an Impulse task, use [impulse.md](impulse.md) and its optional definition template. For another tool, retain its task identity, invocation details, and continuation instructions in the workspace so a fresh session can use it.

Schedule the next useful action or observation, inspect the resulting task state, and retain its identity and confirmed time. After an uncertain scheduling response, inspect existing state before creating another task. Use the scheduler's stable request identity when available. A successful command can still report a failed or unconfirmed run; inspect the actual outcome.

For owner pause or termination, disable future work and verify that it is disabled. Ending the current session is a separate operation. An owner-paused responsibility resumes only after explicit owner resumption and verification of prerequisites. Preserve task identity and history across resumption. Keep failed or uncertain scheduling visible in the handoff and report the unresolved state truthfully.
