# V1 implementation scope

This is the original published v1 scope. The subsequently accepted [native-tools revision](native-tools-revision.md) changes runtime packaging and scheduler selection while retaining the underlying responsibility and evidence requirements.

The owner authorized implementation and publication to `olliethedev/long-horizon-skill` after the design interview and 55-session prototype evaluation. The accepted ADRs and CONTEXT.md remain the product requirements. This document makes the implementation and its review boundary concrete.

Deliver an installable `skills/long-horizon/` bundle with the complete setup/continuation workflow, copyable responsibility/action/evidence/handoff templates, and a small bounded file-reading helper. Impulse owns scheduling. The helper supports existing Markdown and text records, requires no database/index, and never changes source history. An optional derived index carries no unique knowledge.

The helper searches within an explicit product directory, returns bounded source excerpts with file/line identities and pagination, reports incomplete coverage, rejects stale continuation cursors, and refuses symlink/path traversal reads. Paged source reading identifies its version. An exhausted search supports absence only within its reported coverage; missing aliases or skipped formats remain retrieval limitations.

The skill must check relevant original attempts and later corrections before deciding, preserve historical actions when interpretations change, and explicitly distinguish request/event time, deployment/exposure time, observation window, and retrieval time. Unknown timestamps remain unknown. Related product history conveys evidence rather than authority. Standing authority, optional shared limits/cost instructions, pause/manual resume, wait, termination, and reporting remain as agreed.

Setup establishes the product, responsibility, useful outcomes, authority, evidence/access, related work, limits/cost sources, reporting, and scheduling without forcing every future objective or a numeric KPI. Templates are editable starting points; they cannot grant authority. Install instructions copy only the runtime bundle. No automatic global installation or live product registration occurs as part of publication.

## Agreed verification seams

The owner's go-ahead follows the three proposed gates: file-backed recall, evidence-linked decisions, and actual scheduler continuation. Verify these through public interfaces:

1. The helper CLI returns bounded, traceable history while preserving source bytes and scope. Test each behavior with a failing CLI test before implementing it.
2. Fresh agents receive realistic requests, raw history, and the skill; evaluate their actual retrieved sources and decisions. Compare with a matched baseline. Include dense histories, competing corrections, renamed interventions, unknown request dates, and retained terminated-work evidence. Preserve failures and raw traces.
3. An isolated `IMPULSE_HOME` executes a local elapsed-time continuation/restart/termination exercise using the real CLI. Record actual runs and scheduling outcomes. This establishes the scheduler integration boundary; production access and a real product pilot remain task-specific setup work.

Ship deterministic checks, typechecking, repeatable opt-in model evaluations, CI for ordinary checks, and reviewed evidence. Keep historical prototypes frozen. A zero exit code or bounded response alone does not prove correct recall. Do not claim months of continuous reliability from selected checkpoints.

## Review baseline

`62fec70` preserves the starting research and prototype repository. Review the v1 implementation against that commit along Standards and Spec axes. The new GitHub repository was empty when inspected; publishing the completed current branch is explicitly authorized.
