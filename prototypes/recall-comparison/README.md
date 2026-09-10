# THROWAWAY — dense recall comparison

Question: does the draft skill, or a narrow instruction about bounded retrieval, improve a fresh agent's decision compared with the same task without that skill?

```sh
python3 prototypes/recall-comparison/prepare.py
```

The generator prepares three matching temporary workspaces with synthetic records from March 2025 through July 2026, interpreted from a September 2026 current brief. Each contains 1,200 intervention sequences plus a separated historical correction, current signals, retained responsibilities, and a stale summary. Subject indexes aid navigation; relevant evidence shares its directory with 1,200 other evidence files. All three arms receive the same user brief, authority, current signals, and history. The original skill is frozen; the revised arm adds only a bounded-retrieval paragraph.

Use a fresh fork-free evaluator for each trial, with only its opaque trial path and `task.md`. Keep this generator, manifest, and reviewer criteria outside its permitted scope. The manifest maps paths to arms; graders must inspect evidence and decisions rather than prefer the presence of a skill.

This is an exploratory comparison: one case and one trial per arm, with instructed access boundaries, self-reported retrieval, and no external effects. It does not establish reliable recall, hard context limits, or independently verified harness isolation. Preserve those limitations when reporting ties or differences. The first-pass skill does not contain all later accepted setup and retention decisions; the common brief supplies current authority and history scope for every arm.

Preparation review found one additional fixture limitation: only one record has phase `corrected`. Although the surrounding history is substantially denser than the first probe, filtering for that phase can expose the critical correction. Future held-out cases need competing corrections; keep this limitation visible rather than modifying inputs while evaluated agents are running.

Generated archives are temporary. Preserve a reproducibility manifest, outputs, and the evidence needed for reviewed findings, while keeping the earlier evaluation artifacts unchanged.

The [first comparison findings](NOTES.md) and [preserved manifest](https://github.com/olliethedev/long-horizon-skill/blob/be91b6929b4910042e71ddf704c0801b4d611d39/prototypes/recall-comparison/results/first-comparison/manifest.json) are available. All three arms made a supported decision; the baseline matched the skill arms. The bounded-retrieval revision avoided reported history-output truncation in its single trial, while all arms exposed the same startup discovery weakness.
