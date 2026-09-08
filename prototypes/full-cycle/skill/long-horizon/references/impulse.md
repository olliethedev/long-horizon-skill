# Impulse continuation

Use the installed Impulse CLI and its current help for the exact task-definition format and command options. Check the existing task identity before registering or changing anything. A project-supplied scheduler replaces live Impulse during isolated evaluations.

The inspected installation supports file-based task definitions. `impulse task register FILE --json` registers the definition; registration is idempotent by canonical source path. Editing it requires `impulse task update TASK --json` to apply the change. Inspect `impulse task show TASK --json` for applied configuration and drift. Preserve the task identity and workspace across updates.

Within an authorized run, arrange continuation with the CLI's task-next operation. Outside the run supply the task identity, for example `impulse task next TASK --after 24h --json`. Inspect the structured result and retain its receipt. For uncertain durable mutations, use `--request-id KEY` with the identical input; look up current state before creating a second effect.

For owner pause or termination, disable future automatic work using the current task-disable command and verify the result. Stopping a run alone does not disable future runs. A paused task requires explicit owner resumption; changing its next date alone does not re-enable it. On an authorized resume, verify prerequisites and use the installed enable operation, such as `impulse task enable TASK --now --json`.

The CLI can return a structured `ok:true` while waited work has failed, is unconfirmed, or was interrupted. Read the outcome status, not just process success. Current task-definition updates can fence scheduling callbacks from old runs; recheck current authority when a scheduling mutation is rejected. Keep unresolved scheduling evidence visible.
