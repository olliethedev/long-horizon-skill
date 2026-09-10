# V1 recall comparison — September 8, 2026

Both arms passed all source-based criteria: **20/20 without the skill and 20/20 with the historical helper-based skill**. There was no observed decision-quality advantage.

Eight fresh Codex sessions compared matched histories across revenue, weekly product improvement, large-export feedback and post-PR monitoring. Each history contained roughly 2,233 files and 2.49 MB. Both arms found the decisive original records and corrections.

| Measure, four sessions per arm | No skill | Historical skill |
| --- | ---: | ---: |
| Criteria satisfied | 20/20 | 20/20 |
| Captured command output | 1,080,528 bytes | 218,883 bytes |
| Commands | 67 | 133 |
| Reported input tokens | 1,052,503 | 1,147,789 |
| Reported output tokens | 17,708 | 21,588 |
| Summed process time | 637.7 seconds | 796.1 seconds |

The helper reduced captured output by 79.7%, while increasing commands, total reported input and elapsed time. Captured bytes do not measure actual model-visible context; cached input is included in Codex's input total. No subscription-cost conversion is inferred.

A separate revenue follow-up after a helper cursor fix passed 5/5 criteria. There were 17 process attempts overall: eight main decisions, that follow-up and eight infrastructure attempts. Completed decisions were not silently replaced.

This tested the historical helper bundle, not the current instruction-only skill. Installed Codex defaults were `gpt-6-astra`, xhigh, CLI 0.153.4. Fixtures had predictable background patterns and the prompt already requested source-based reasoning. One trial per case cannot establish statistical reliability, selective recall over real months or a skill advantage. These read-only cases did not exercise deployments or scheduler effects.

Original evidence is retained locally. The later [native-tools comparison](../native-tools/REPORT.md) evaluates removing the helper.
