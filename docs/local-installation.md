# Local installation

The September 9 Eastern / September 10 UTC onboarding revision was installed for all three owner harnesses from the reviewed local repository using the Skills CLI:

```sh
npx --yes skills add /home/deck/Projects/long-horizon --skill long-horizon --agent codex claude-code antigravity-cli --global --yes
```

For installation from the published project, replace the local path with `https://github.com/olliethedev/long-horizon-skill`.

| Harness | Verified installed directory |
| --- | --- |
| Codex | `/home/deck/.agents/skills/long-horizon` |
| Claude Code | `/home/deck/.claude/skills/long-horizon` (shared `.agents/skills` location) |
| Antigravity CLI | `/home/deck/.gemini/config/skills/long-horizon` (also available at the universal `.agents/skills` location) |

The CLI installed the universal bundle and Claude link. The additional Antigravity directory, documented by this host's installed customization guide, was refreshed with the entire bundle. All three locations contain the same 13 files, byte-for-byte, with aggregate SHA256 `c125e3a1fa68352680011105a75cf9eb273136e70ba08f95cda9ce9bd57f56bb`. Exact hashes and local review evidence are retained under ignored `evals/runs/onboarding-2026-09-10-local/`.

Verification used file contents and installation paths; no model session was launched. Start a fresh harness session to load the revised skill. Established responsibilities keep their standing authority; installing the revision does not activate, pause or re-onboard them.

For a new responsibility, start your harness in the product repository and invoke `$long-horizon` or select the skill from its picker. A simple request such as “Grow qualified organic traffic with daily content work” begins the built-in setup conversation. See the [README examples](../README.md#example-responsibilities). The agent prepares a concrete summary and asks for final activation confirmation before scheduling autonomous work.
