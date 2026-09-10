# Install and verify

Use the Skills CLI from the product repository, adding `--global` for availability across projects:

```sh
npx skills add https://github.com/olliethedev/long-horizon-skill --skill long-horizon --global
```

Select the intended harnesses. For development, the same command accepts a local repository path. Copy the complete bundle, including linked references, when installing manually through a harness's documented skill directory.

After updating, verify that each intended installation contains the current bundle and no retired templates or references. Start a fresh harness session to load it. Installation does not activate a responsibility or replace its existing owner instructions. Keep host paths, hashes and installation receipts in local development records rather than shared project guidance.

See the [README](../README.md) for starting a responsibility and example prompts.
