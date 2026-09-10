# Native tools comparison

`native_matrix.py` compares three actual harnesses (Codex, Claude Code, and
Antigravity), three treatments (no skill, published helper bundle, and revised
native-tools bundle), and four matched handoff domains. It does not call model
APIs directly. The original `recall.py` evaluation remains usable unchanged;
`fixtures.py` retains its original 720-chain default.

From the repository root:

```sh
python3 evals/native_preflight.py --output evals/runs/native-tools/preflight-dry-RUN
python3 evals/native_preflight.py --run --output evals/runs/native-tools/preflight-live-RUN
python3 evals/native_matrix.py --output evals/runs/native-tools/matrix-dry-RUN
python3 evals/native_matrix.py --run --output evals/runs/native-tools/matrix-live-RUN
```

Every output path must be new. `--run` explicitly enables authenticated model
sessions; without it, the runner freezes artifacts and executes local isolation
probes. The matrix defaults to two native processes, accepts `--jobs 1|2`, and
bounds each session with `--timeout 30..3600` seconds (default 1200). A
SIGINT/SIGTERM lets active sessions finish and skips queued sessions. A missing
decision, nonzero native exit, infrastructure exception, or input mutation is a
run failure. Inspect preserved failures before starting any investigation.

The runner requires Python 3.11+, Linux bubblewrap, native ELF versions of
`codex`, `claude`, and `agy` discoverable through PATH, `rg`, and the system
certificate store. It copies only harmless installed model/effort defaults,
never chooses a different model, and records the native versions and executable
hashes. Codex also needs its sibling `codex-code-mode-host`. Claude uses its
native file authentication. Antigravity's adapter uses the installed system
Python D-Bus binding to read only its unlocked Secret Service item and copies it
into the native CLI's file fallback. No host D-Bus socket, live project, session,
hook, plugin, integration, or broad home directory is mounted. All temporary
credential copies are removed when their sessions finish.

Each session gets a fresh writable work directory and the same read-only raw
input snapshot for its domain. Both skill treatments receive the same activation
sentence and `/workspace/skill` path; the no-skill treatment omits only that
activation and mount. The published bundle is frozen using `git archive` of the
pinned commit, and the candidate is copied only if its declared tree hash
matches. Updating the pinned comparison requires an intentional evaluator edit.

`native_fixtures.py` retains the original four decision/evidence chains but uses
2,400 linked background chains per domain. Individual history record filenames and receipt, action, evidence, and
support identities share an opaque namespace. Briefs, current state, and
navigation/index files keep their descriptive names; subject and cohort cues
remain available. Some
background chains are retained beside actions from terminated responsibilities.
The 7,273–7,274 files per domain contain about 8.2 MB of text. This is a raw-byte
difficulty measure, not a tokenizer count or proof about a model's context use.
Template repetition and the finite set of background cohorts remain limitations.
The frozen large-export snapshot also obscures the individual job regions that
were encoded only in the original names. A separate clarification, recorded
before any export session launched, excludes inferred geography from grading;
job identity, format, scale, failure, and correction exclusions remain observable.
The delivered action's explicit paid US/EU scope remains available.

The run archive contains exact evaluator sources, input archives and file
hashes, both skill bundles, the declared criteria, per-session prompts,
commands/settings, native traces, decisions, usage, and failures. The criteria
and evaluator sources are never mounted into native sessions. Antigravity's
stream records concise tool summaries, so its native conversation artifacts are
also retained. Its resolved model is recorded from the native log.

Semantic success requires all five source-backed criteria for a domain and no
material contradictory decision. Exit codes, artifact presence, valid JSON, and
retrieval size do not prove success. Review source records and actual decisions,
then record criterion-level judgments with reasons. Report each harness and
treatment separately: one initial session per cell supports descriptive case
outcomes, not significance or reliability estimates. These offline handoffs do
not evaluate live scheduling, production changes, or customer outcomes.

The isolation boundary covers files and processes. Host networking remains
available for each native harness's model transport; external-service restraint
is part of the task instruction rather than an enforced network allowlist.

After source review, the following local commands regenerate diagnostics,
reviewed outcomes, and provenance checks without model calls:

```sh
python3 evals/native_diagnostics.py evals/runs/native-tools/matrix-live-RUN
python3 evals/native_report.py evals/runs/native-tools/matrix-live-RUN
python3 evals/native_audit.py evals/runs/native-tools/matrix-live-RUN
```

Store each independent review in the session's `manual-review.json`, with the
decision's SHA256, criterion verdicts and reasons, sources checked, material
contradictions, and accuracy caveats. The report rejects changed decisions and
preserves missing telemetry as unknown. Group sums include reporting-session
counts. Native token accounting differs between harnesses; compare treatment
usage within one harness. Claude's dollar values are native reported estimates,
not actual subscription charges.

Captured tool output sizes are diagnostics rather than semantic gates or a
measurement of context exposure. Full reference text matches show that a tool
made the source available; they cannot establish comprehension. Antigravity
diagnostics use its full native transcript because stdout tool events summarize
file reads.

Start the credential scanner while authenticated sessions are running, so it
can observe short-lived refreshed credential copies without archiving values:

```sh
python3 evals/native_credentials_check.py \
  --matrix evals/runs/native-tools/matrix-live-RUN \
  --artifacts evals/runs/native-tools \
  --output evals/runs/native-tools/credential-scan-RUN.json
```

It waits for the matrix's completion marker, scans exact observed values in
raw artifacts, decompressed gzip, and tar members, and then discards its in-memory
values. A scan started only after cleanup cannot cover temporary refreshed
values that are no longer available. If another batch is still writing archives,
the scanner retains its observed values and samples active homes while retrying
an incomplete scan. It permits at most 60 full scans and 59 one-second pauses
(scan time is additional); persistent corruption exits 2 with
`scan_complete = false`, never a clean result. Startup file paths and total
credential-sampling calls are recorded without storing credential values.

`native_replay.py` preserves infrastructure interruptions in separate archives.
Completion mode selects only initial cells without a generated decision and
reuses the initial archived skill bundles, even if the working runtime changed:

```sh
python3 evals/native_replay.py --run --mode complete --harness antigravity \
  --source-matrix evals/runs/native-tools/matrix-live-RUN \
  --output evals/runs/native-tools/completion-RUN
python3 evals/native_report.py evals/runs/native-tools/matrix-live-RUN \
  --completion evals/runs/native-tools/completion-RUN
```

The original failure and skipped-cell manifest remain unchanged. The aggregate
records attempts separately from intended semantic cells and refuses to replace
a generated decision with a completion. Frozen criteria, original prompts,
published bundle, input archive, candidate, installed defaults and executable
identities are checked before reuse.
Keep replay archives beside the original matrix: the runner scans adjacent
linked archives for generated or active cells and excludes them before any
authentication setup or model launch. This also prevents repeating a focused
failure merely to obtain a passing result.

Focused mode implements the five preselected failure/control probes described
in the archived refinement plan. It requires `--candidate-hash` with the exact
revised tree SHA256. Repeatable `--harness` flags allow pending authentication to
leave some of that fixed selection unrun; the complete selection remains in
each manifest. Omit `--run` for no-model isolation preparation. Report focused
outcomes separately from the original comparison, and never repeat successful
probes merely to obtain a favorable result.
