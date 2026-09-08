# Allow optional responsibility limits

Owners may set optional limits on a responsibility, including domain-specific limits such as A/B testing at most five articles at a time. The agent chooses work within those limits; they can constrain simultaneous active work as well as run frequency or resource consumption. In the article example, experiments continue to occupy capacity while collecting observations between agent runs, and a finished experiment frees capacity for another article.

Limits are optional and their scope belongs in the owner's brief. Cost restrictions and ways of obtaining usage information are supplied by the user on a per-project basis and may require custom setup. The agent working on a responsibility follows those instructions and preserves relevant accounting across runs; Impulse continues to own scheduling. When a budget is shared across a project, separate responsibilities do not each receive a fresh copy of that allowance.

Examples include a paid crawling-service budget and constraints on use of the harness's subscription allowance. `ccusage` and Firecrawl MCP are illustrative, not required integrations or an exhaustive set of cost sources. Any supporting helpers remain to be prototyped; an instruction to respect a budget is not a guarantee of runtime or provider billing enforcement.

No particular spending allowance is established by this decision. A subscription's remaining usage allowance, an estimated API-equivalent dollar cost, and the budget assigned to an individual responsibility are distinct quantities.
