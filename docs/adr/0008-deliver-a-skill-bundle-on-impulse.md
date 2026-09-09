# Deliver a skill bundle on top of Impulse

The runtime-helper and Impulse-only choices below were revised by [ADR 0015](0015-use-native-tools-and-discover-scheduling.md) after the owner's review of the published bundle. This record describes the original v1 choice.

Deliver v1 as a skill bundle containing SKILL.md, templates, evaluations, and small local helper commands where prototype results demonstrate a need. The skill describes the working method; helpers can support memory and coordination mechanics, while Impulse continues to own scheduling. This preserves the user's preferred skill distribution model while allowing executable support for requirements that prose alone does not reliably satisfy. [ADR 0013](0013-use-readable-files-for-durable-history.md) subsequently selects readable files for durable history; language and exact helper interfaces remain open.
