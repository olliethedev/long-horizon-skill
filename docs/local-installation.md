# Local installation and starting a responsibility

On September 9, 2026, the published native-tools skill from commit `ba483280388ecf7a09aa0d514a05262f46683c5a` was installed on the owner's machine. After the README improvement, it was refreshed from the published repository through the Skills CLI for all three harnesses. The complete-workflow study has not changed this runtime bundle.

```sh
npx --yes skills add https://github.com/olliethedev/long-horizon-skill --skill long-horizon --agent codex claude-code antigravity-cli --global --yes
```

The CLI completed successfully and `skills list --global` listed Long Horizon for Codex, Claude Code and Antigravity CLI. It uses the universal `~/.agents/skills/long-horizon` location for Codex and Antigravity, and the existing shared Claude location. The additional Antigravity copy below is retained because the installed Antigravity customization guide explicitly documents that global root. No model prompt was submitted for installation or verification.

| Harness | Installed skill directory | Verification |
| --- | --- | --- |
| Codex | `/home/deck/.agents/skills/long-horizon` | Local `skills/list` returned `long-horizon`, user scope, enabled, for `better-stack-web`. No model turn was started. |
| Claude Code | `/home/deck/.claude/skills/long-horizon` | Existing `.claude/skills` symlink points to `.agents/skills`. Installed CLI documentation identifies this global discovery directory. |
| Antigravity CLI | `/home/deck/.gemini/config/skills/long-horizon` | Installed CLI's embedded customization documentation identifies `.gemini/config` as the global root and `skills/<name>/SKILL.md` as the skill layout. |

After the CLI refresh, all three locations contain the same 12 files as the repository bundle, with aggregate SHA256 `af8084aa46624ee25271c94ef14e1593f7adb6d325da156348132a8620ac4d26`. Initial installation used the skill-installer helper pinned to the published commit; the final refresh used the command above. Unrelated skills and existing customizations were preserved.

Codex discovery was checked through its local app-server API. Claude and Antigravity verification covers their documented discovery paths and exact installed contents; it does not claim an additional model activation test. An Antigravity interactive launch was closed at its project-trust screen without submitting a model prompt or changing that trust setting. Start a fresh harness session to load the installation; Codex can discover it on the next turn.

## Example: daily content work in better-stack-web

Start Codex in the project:

```sh
cd /home/deck/Projects/better-stack-web
codex
```

Then send:

```text
$long-horizon Take responsibility for growing qualified organic traffic to this site. Create useful new content and improve existing content, with daily actions. Inspect the project and available analytics, ask me for the missing details, and set up ongoing work using Impulse. Keep a record of what you tried and learned so future runs build on it.
```

The skill handles the initial interview; no separate grilling skill is required. Agree on audience and scope, useful success measures, authority to publish or open PRs, analytics and search data access, any project-specific limits or paid-service budgets, reporting destination and cadence, and when to pause or end. Reuse answers already present in the project. Daily activity need not mean declaring a content winner every day: choose observation windows that fit the available traffic and evidence.

This example does not register a task. The actual responsibility is created during that project setup conversation after consequential details are settled.
