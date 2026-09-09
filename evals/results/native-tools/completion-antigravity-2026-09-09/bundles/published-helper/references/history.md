# Retrieve before choosing work

Run the helper by its path in this installed skill; it needs Python 3.11+ on Linux/macOS. PRODUCT is the explicit authorized product-history directory, not a parent containing multiple products. The helper reads existing UTF-8 Markdown, JSON/JSONL, text, CSV, YAML, and TOML. It writes no index or history.

```sh
python3 SKILL/scripts/history.py search PRODUCT 'returning mobile offer' 'Quiet Offer' --limit 8
python3 SKILL/scripts/history.py search PRODUCT 'action-731' 'audit-119' --limit 8
python3 SKILL/scripts/history.py read PRODUCT evidence/audit.json --offset 0 --bytes 6000
```

Search phrases match literally, case-insensitively, with OR semantics. Start with subject names and aliases; follow stable action/source IDs into their observations and corrections. Generic terms such as "metric" can return mostly unrelated history. Query concrete subject + condition as a phrase or narrow to an authorized subdirectory. Semantic similarity and missing aliases remain the agent's responsibility.

Each hit gives a relative source path, line, byte offset, and excerpt. Use `read` at that offset to inspect the original record; read its surrounding context as needed. `next_cursor` continues the same search with `--cursor TOKEN`; changed history/query invalidates it, so restart. A read page gives a content-hash `version` and `next_offset`; pass `--version HASH --offset OFFSET` on later pages to reject mixed file versions.

Responses are capped at 20,000 UTF-8 bytes. Search returns at most 20 hits (default 8); read pages contain at most 8,000 source bytes (default 6,000). Search skips lines larger than 65,536 bytes and returns bounded examples with offsets for explicit paged reading. Check `skipped`, examples, and continuation before claiming coverage. An exhausted search establishes only that the supplied phrases were exhausted in the supported files scanned. It does not establish that a renamed intervention never occurred.

Symlink entries and unsupported files are counted but not read. Version-control/environment directories are excluded. Helpers refuse absolute source paths and `..` traversal. A project with evidence in other formats needs an authorized extraction step. If this helper is unavailable, use equivalent bounded file searches and paged reads inside the supplied product workspace, preserving the same source and coverage checks.

Before a consequential decision, retain the relevant original attempt, actual outcome, latest applicable correction, and why their conditions match or differ today. Search the action/source IDs for later references even when the current handoff says the matter is settled. Cross-links in records are preferable to copying whole narratives into every handoff. Any optional index is derived navigation; rebuild or bypass it using the original files.
