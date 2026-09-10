# Use readable files for durable history

The [simplified persistence decision](0016-persist-knowledge-tools-cannot-reconstruct.md) supersedes the broad retention scope below; this document records the earlier decision.

V1 stores the responsibility's durable brief, actions, evidence, and learnings in readable local files. Use ordinary file search and, where useful, an index generated from those files. The original records remain authoritative: an index must not contain the only copy of a finding, qualification, or correction, and can be rebuilt if missing or stale. The user accepted this approach September 8, 2026, preferring to work with modern harnesses' file capabilities without adding a vector database.

This keeps history inspectable and portable while accepting the need to maintain useful records and evaluate retrieval as the archive grows. The existing seeded-history probes support further exploration with files; they do not establish reliable recall across months of agent-authored history or prove an index is necessary. Exact file formats, index contents, and any helper commands remain prototype choices. Index generation must respect the accepted product boundary and retention policy.
