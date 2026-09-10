# Native file-tool comparison — September 9, 2026

Removing the runtime history helper did **not reduce the overall initial decision score**, but neither skill variant demonstrated an overall advantage over no skill.

Three harnesses compared no skill, the published helper bundle and the native-tools revision across four domains. Each case contained about 7,273 files (8.2 MB), with matched source facts and independently reviewed decisions.

| Harness | No skill | Helper skill | Native-tools skill |
| --- | ---: | ---: | ---: |
| Codex | 4/4 | 4/4 | 4/4 |
| Claude Code | 2/4 | 3/4 | 3/4 |
| Antigravity | 2/4 | 1/4 | 1/4 |
| Total semantic passes | 8/12 | 8/12 | 8/12 |

All 36 initial decisions completed; 24 passed semantic review and 172/180 observable criteria were satisfied. Common failures involved inventing permission restrictions, ordering events with unknown dates, and treating plausible causes as established facts. Finding the right records did not guarantee correct interpretation.

Five separately declared refinement probes produced two semantic passes and 25/25 observable criteria. Three setup probes produced two semantic passes and 9/9 explicit setup-choice criteria. These selected probes do not replace the initial comparison. In total, 44 decisions completed in 45 attempts, including one authentication failure before generation.

There was no consistent efficiency advantage. For Codex, native tools used more reported input and captured output than the helper despite equal decision scores. Captured tool output is not the same as model-visible context, and native accounting differs between harnesses.

The study used installed defaults: Codex 0.153.4 (`gpt-6-astra`, xhigh), Claude 2.1.266 (`claude-fable-5-1[1m]`), and Antigravity 1.1.27 (Gemini 3.8 Flash, High). The final skill tree was `af8084aa46624ee25271c94ef14e1593f7adb6d325da156348132a8620ac4d26`.

These were synthetic, one-session decisions with one trial per cell. Repetitive fixtures, a strong baseline, supplied setup inventories and visible treatment labels limit generalization. The tests do not establish real months-long operation, exhaustive recall or production outcomes. Authentication recovery did not repeat completed decisions. Historical credential-scanning gaps remain documented in the local evidence backup.

Raw inputs, traces, reviews and exact source snapshots are retained locally rather than committed. See [evaluation instructions](../../README.md) for the reusable runners.
