### Codex Pricing

Source: [Codex Pricing](https://developers.openai.com/codex/pricing.md)

## Plans

### Individual plans

#### Free ($0/month)

Explore Codex capabilities on quick coding tasks.

[Get Free](https://chatgpt.com/plans/free/)

#### Go ($8/month)

Use Codex for lightweight coding tasks.

[Get Go](https://chatgpt.com/plans/go)

#### Plus ($20/month)

Power a few focused coding sessions each week.

- Codex on the web, in the CLI, in the IDE extension, and on iOS
- Cloud-based integrations like automatic code review and Slack integration
- The latest models, including GPT-5.5, GPT-5.4, and GPT-5.3-Codex
- GPT-5.4-mini for higher usage limits on routine local messages
- Flexibly extend usage with [ChatGPT credits](#credits-overview)
- Other [ChatGPT features](https://chatgpt.com/pricing) as part of the Plus plan

[Get Plus](https://chatgpt.com/explore/plus?utm_internal_source=openai_developers_codex)

#### Pro (from $100/month)

Choose 5x or 20x higher rate limits than Plus.

Everything in Plus and:

- Access to GPT-5.3-Codex-Spark (research preview), a fast Codex model for day-to-day coding tasks
- 5x or 20x more Codex usage than Plus*
- Other [ChatGPT features](https://chatgpt.com/pricing) as part of the Pro plan

[Get Pro](https://chatgpt.com/explore/pro?utm_internal_source=openai_developers_codex)

[*Learn more about limits on both tiers.](https://help.openai.com/en/articles/9793128-about-chatgpt-pro-plans)

### Business and Enterprise plans

#### Business (pay as you go)

Bring Codex into your startup or growing business.

Everything in Plus and:

- Assign standard or usage-based Codex seats based on your team's needs. [Learn more](https://help.openai.com/en/articles/8792828-what-is-chatgpt-business)
- Larger virtual machines to run cloud tasks faster
- Flexibly extend usage with [ChatGPT credits](#credits-overview)
- A secure, dedicated workspace with essential admin controls, SAML SSO, and MFA
- No training on your business data by default. [Learn more](https://openai.com/business-data/)
- Other [ChatGPT features](https://chatgpt.com/pricing) as part of the Business plan

[Get Business](https://chatgpt.com/codex/team/start)

#### Enterprise & Edu

Unlock Codex for your entire organization with enterprise-grade functionality.

Everything in Business and:

- Priority request processing
- Enterprise-level security and controls, including SCIM, EKM, user analytics, domain verification, and role-based access control ([RBAC](https://help.openai.com/en/articles/11750701-rbac))
- Audit logs and usage monitoring via the [Compliance API](https://chatgpt.com/admin/api-reference#tag/Codex-Tasks)
- Data retention and data residency controls
- Other [ChatGPT features](https://chatgpt.com/pricing) as part of the Enterprise plan

[Contact sales](https://chatgpt.com/contact-sales?utm_internal_source=openai_developers_codex)

### API Key

Great for automation in shared environments like CI.

- Codex in the CLI, SDK, or IDE extension
- No cloud-based features (GitHub code review, Slack, etc.)
- Delayed access to new models like GPT-5.3-Codex and GPT-5.3-Codex-Spark
- Pay only for the tokens Codex uses, based on [API pricing](https://platform.openai.com/docs/pricing)

[Learn more](/codex/auth)

## Frequently asked questions

### How much does Sites cost?

[Sites](https://developers.openai.com/codex/sites) is free while in preview. Pricing information will be available soon.

### What are the usage limits for my plan?

The number of Codex messages you can send depends on the model used, size and complexity of your coding tasks and whether you run them locally or in the cloud. Small scripts or routine functions may consume only a fraction of your allowance, while larger codebases, long-running tasks, or extended sessions that require Codex to hold more context will use significantly more per message.

GPT-5.5 uses significantly fewer tokens to achieve results comparable to GPT-5.4. Its Codex setup runs faster and delivers higher-quality results for most users. These efficiency gains support generous usage limits despite GPT-5.5 being a significantly more capable model.

#### Plus

| Model | Local messages / 5h | Cloud tasks / 5h | Code reviews / 5h |
| --- | --- | --- | --- |
| GPT-5.5 | 15-80 | Not available | Not available |
| GPT-5.4 | 20-100 | Not available | Not available |
| GPT-5.4-mini | 60-350 | Not available | Not available |

#### Pro 5x

| Model | Local messages / 5h | Cloud tasks / 5h | Code reviews / 5h |
| --- | --- | --- | --- |
| GPT-5.5 | 80-400 | Not available | Not available |
| GPT-5.4 | 100-500 | Not available | Not available |
| GPT-5.4-mini | 300-1750 | Not available | Not available |

#### Pro 20x

| Model | Local messages / 5h | Cloud tasks / 5h | Code reviews / 5h |
| --- | --- | --- | --- |
| GPT-5.5 | 300-1600 | Not available | Not available |
| GPT-5.4 | 400-2000 | Not available | Not available |
| GPT-5.4-mini | 1200-7000 | Not available | Not available |

#### Business

| Model | Local messages / 5h | Cloud tasks / 5h | Code reviews / 5h |
| --- | --- | --- | --- |
| GPT-5.5 | 15-80 | Not available | Not available |
| GPT-5.4 | 20-100 | Not available | Not available |
| GPT-5.4-mini | 60-350 | Not available | Not available |

#### API Key

| Model | Local messages / 5h | Cloud tasks / 5h | Code reviews / 5h |
| --- | --- | --- | --- |
| GPT-5.5 | Not available | Not available | Not available |
| GPT-5.4 | [Usage-based](https://platform.openai.com/docs/pricing) | Not available | Not available |
| GPT-5.4-mini | [Usage-based](https://platform.openai.com/docs/pricing) | Not available | Not available |

Notes: local messages and cloud tasks share a five-hour window. Additional weekly limits may apply. For Enterprise/Edu users with flexible pricing, there are no fixed rate limits; usage scales with [credits](#credits-overview). Enterprise and Edu plans without flexible pricing have the same per-seat usage limits as Plus for most features.

Codex usage limits are shared with other agentic features once pricing for those features is effective. This currently includes [ChatGPT for Excel](https://help.openai.com/articles/20001063) on Plus and Pro.

Speed configurations increase credit consumption for all applicable models, so they also use included limits faster. Fast mode consumes credits at a higher rate for supported models. See [Speed](https://developers.openai.com/codex/speed) for supported models and rates. Image generations also use included limits ~3-5x faster on average, depending on image quality and size. GPT-5.3-Codex-Spark is in research preview for ChatGPT Pro users only, and isn't available in the API at launch. Because it runs on specialized low-latency hardware, usage is governed by a separate usage limit that may adjust based on demand.

### What happens when you hit usage limits?

ChatGPT Plus and Pro users who reach their usage limit can purchase additional credits to continue working without needing to upgrade their existing plan.

Business, Edu, and Enterprise plans with [flexible pricing](https://help.openai.com/en/articles/11487671-flexible-pricing-for-the-enterprise-edu-and-business-plans) can purchase additional workspace credits to continue using Codex.

If you are approaching usage limits, you can also switch to a smaller model to make your usage limits last longer.

All users may also run extra local tasks using an API key, with usage charged at [standard API rates](https://platform.openai.com/docs/pricing).

<a id="image-generation-usage-limits"></a>

### How does image generation count toward usage limits?

Image generation counts toward the same general Codex usage limits as local messages and cloud tasks. Image generations use included limits 3-5x faster on average than similar turns without image generation, depending on image quality and size. After you reach your included limits, image generation also draws from [credits](#credits-overview).

Image generation isn't available on the Free plan. When you use Codex with an API key, API pricing applies to image generation instead of included ChatGPT usage limits.

### Where can I see my current usage limits?

You can find your current limits in the [Codex usage dashboard](https://chatgpt.com/codex/settings/usage). If you want to see your remaining limits during an active Codex CLI session, you can use `/status`.

<a id="credits-overview"></a>

### How do credits work?

Credits let you continue using Codex after you reach your included usage limits. Usage draws down from your available credits based on the models and features you use, allowing you to extend work without interruption.

Codex credit usage is based on API token-based rates. Credits remain the core pricing unit that customers purchase and consume, but usage is calculated as credits per million input tokens, cached input tokens, and output tokens your workspace consumes. Read about tokens [here](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them).

The rate card below shows the credit cost per million tokens for Codex models and features.

A small subset of Enterprise customers should continue using the legacy rate card until we migrate you to the new token-based pricing for Codex. For more information, [contact OpenAI sales](https://chatgpt.com/contact-sales?utm_internal_source=openai_developers_codex).

| Credits per 1M tokens | Input tokens | Cached input tokens | Output tokens |
| --- | --- | --- | --- |
| GPT-5.5 | 125 credits | 12.50 credits | 750 credits |
| GPT-5.4 | 62.50 credits | 6.250 credits | 375 credits |
| GPT-5.4-mini | 18.75 credits | 1.875 credits | 113 credits |
| GPT-5.3-Codex-Spark | research preview | research preview | research preview |
| GPT-Image-2 (image) | 200 credits | 50 credits | 750 credits |
| GPT-Image-2 (text) | 125 credits | 31.25 credits | 250 credits |

GPT-5.5 usage averages 5-45 credits per message. Fast mode consumes credits at a higher rate for supported models. See [Speed](https://developers.openai.com/codex/speed) for rates.

Speed configurations will increase credit consumption for all models that apply. Fast mode consumes credits at a higher rate for supported models. See [Speed](https://developers.openai.com/codex/speed) for supported models and rates.

[Learn more about credits in ChatGPT Plus and Pro.](https://help.openai.com/en/articles/12642688)

[Learn more about credits in ChatGPT Business, Enterprise, and Edu.](https://help.openai.com/en/articles/11487671-flexible-pricing-for-the-enterprise-edu-and-business-plans)

### What counts as Code Review usage?

Code Review usage applies only when Codex runs reviews through GitHub, for example when you tag `@Codex` for review in a pull request or enable automatic reviews on your repository. Reviews run locally or outside of GitHub count toward your general usage limits.

### What can I do to make my usage limits last longer?

The usage limits and credits above are average rates. You can try the following tips to maximize your limits:

- **Control the size of your prompts.** Be precise with the instructions you give Codex, but remove unnecessary context.
- **Reduce the size of your AGENTS.md.** If you work on a larger project, you can control how much context you inject through AGENTS.md files by [nesting them within your repository](https://developers.openai.com/codex/guides/agents-md#layer-project-instructions).
- **Limit the number of MCP servers you use.** Every [MCP](https://developers.openai.com/codex/mcp) you add to Codex adds more context to your messages and uses more of your limit. Disable MCP servers when you do not need them.
- **Switch to a smaller model for routine tasks.** Using GPT-5.4 or GPT-5.4-mini can extend your local-message usage limits, depending on the model you switch from.

## Feature availability

### Access and surfaces

| Feature | Plus | Pro | Business | Enterprise/Edu | API Key |
| --- | --- | --- | --- | --- | --- |
| [Codex web](/codex/cloud) | Available | Available | Available | Available | Unavailable |
| [Codex app for local tasks](/codex/app) | Available | Available | Available | Available | Available |
| [Codex CLI](/codex/cli) | Available | Available | Available | Available | Available |
| [IDE extension](/codex/ide) | Available | Available | Available | Available | Available |
| [Codex SDK, `codex exec`, and scriptable workflows](/codex/sdk) | Available | Available | Available | Available | Available |
| [Codex access tokens for trusted automation](/codex/enterprise/access-tokens) | Unavailable | Unavailable | Available | Available | Unavailable |

### Models and multimodal

| Feature | Plus | Pro | Business | Enterprise/Edu | API Key |
| --- | --- | --- | --- | --- | --- |
| [Fast mode](/codex/speed) | Available | Available | Available | Available | Available |
| [Codex-Spark research preview](/codex/models) | Unavailable | Available | Unavailable | Unavailable | Unavailable |
| [Image generation and editing](/codex/app/features#image-generation) | Available | Available | Available | Available | Available |
| [Voice dictation](/codex/app/features#voice-dictation) | Available | Available | Available | Available | Unavailable |
| [Web search](/codex/app/features#web-search) | Available | Available | Available | Available | Available |

### Local features

| Feature | Plus | Pro | Business | Enterprise/Edu | API Key |
| --- | --- | --- | --- | --- | --- |
| [Local code review with `/review`](/codex/workflows#do-a-local-code-review) | Available | Available | Available | Available | Available |
| [Auto-review for approval requests](/codex/concepts/sandboxing/auto-review) | Available | Available | Available | Available | Available |
| [Sandboxing and permission controls](/codex/permissions) | Available | Available | Available | Available | Available |
| [Project and standalone app automations](/codex/app/automations) | Available | Available | Available | Available | Available |
| [Automations](/codex/app/automations) | Available | Available | Available | Available | Available |
| [Worktrees and built-in Git tools](/codex/app/worktrees) | Available | Available | Available | Available | Available |
| [Local environments and repeatable actions](/codex/app/local-environments) | Available | Available | Available | Available | Available |
| [Appshots](/codex/appshots) | Available | Available | Available | Unavailable | Available |

### Browser and remote control

| Feature | Plus | Pro | Business | Enterprise/Edu | API Key |
| --- | --- | --- | --- | --- | --- |
| [In-app browser previews and comments](/codex/app/browser) | Available | Available | Available | Available | Available |
| [Browser Use automation](/codex/app/browser#browser-use) | Limited* | Limited* | Limited* | Limited* | Limited* |
| [Chrome extension browser control](/codex/app/chrome-extension) | Limited* | Limited* | Limited* | Limited* | Limited* |
| [Computer Use](/codex/app/computer-use) | Limited* | Limited* | Limited* | Limited* | Limited* |
| [SSH remote connections](/codex/remote-connections#connect-to-an-ssh-host) | Available | Available | Available | Available | Available |
| [Mobile remote control](/codex/remote-connections) | Available | Available | Available | Available | Unavailable |

### Customization and extensions

| Feature | Plus | Pro | Business | Enterprise/Edu | API Key |
| --- | --- | --- | --- | --- | --- |
| [Custom instructions with `AGENTS.md`](/codex/guides/agents-md) | Available | Available | Available | Available | Available |
| [Skills](/codex/skills) | Available | Available | Available | Available | Available |
| [Plugins](/codex/plugins) | Available | Available | Available | Available | Limited† |
| [Plugin sharing](/codex/plugins/build#share-a-local-plugin-with-your-workspace) | Available | Available | Available | Available | Unavailable |
| [App connectors](/codex/plugins) | Available | Available | Available | Available | Unavailable |
| [MCP](/codex/mcp) | Available | Available | Available | Available | Available |
| [Subagents and custom agents](/codex/subagents) | Available | Available | Available | Available | Available |
| [Memories](/codex/memories) | Limited* | Limited* | Limited* | Limited* | Limited* |
| [Chronicle](/codex/memories/chronicle) | Unavailable | Limited* | Unavailable | Unavailable | Unavailable |

### Cloud and integrations

| Feature | Plus | Pro | Business | Enterprise/Edu | API Key |
| --- | --- | --- | --- | --- | --- |
| [Codex cloud tasks](/codex/cloud) | Available | Available | Available | Available | Unavailable |
| [Cloud environments and setup scripts](/codex/cloud/environments) | Available | Available | Available | Available | Unavailable |
| [Cloud agent internet access controls](/codex/cloud/internet-access) | Available | Available | Available | Available | Unavailable |
| [Sites](/codex/sites) | Unavailable | Unavailable | Available | Available | Unavailable |
| [GitHub issue and PR delegation with `@codex`](/codex/integrations/github#give-codex-other-tasks) | Available | Available | Available | Available | Unavailable |
| [GitHub code review and automatic PR reviews](/codex/integrations/github) | Available | Available | Available | Available | Unavailable |
| [Slack cloud integration](/codex/integrations/slack) | Available | Available | Available | Available | Unavailable |
| [Linear cloud integration](/codex/integrations/linear) | Available | Available | Available | Available | Unavailable |

### Admin, security, and analytics

| Feature | Plus | Pro | Business | Enterprise/Edu | API Key |
| --- | --- | --- | --- | --- | --- |
| [SAML SSO, MFA, and workspace user management](/codex/enterprise/admin-setup) | Unavailable | Unavailable | Available | Available | Unavailable |
| [`requirements.toml` managed config](/codex/enterprise/managed-configuration) | Available | Available | Available | Available | Available |
| [Cloud-managed config policies](/codex/enterprise/managed-configuration#cloud-managed-requirements) | Unavailable | Unavailable | Available | Available | Unavailable |
| [Codex RBAC and custom roles](/codex/enterprise/admin-setup#step-2-set-up-custom-roles-rbac) | Unavailable | Unavailable | Unavailable | Available | Unavailable |
| [SCIM, EKM, and domain verification](/codex/enterprise/admin-setup#enterprise-grade-security-and-privacy) | Unavailable | Unavailable | Unavailable | Available | Unavailable |
| [Enterprise retention and residency controls](/codex/enterprise/admin-setup#enterprise-grade-security-and-privacy) | Unavailable | Unavailable | Unavailable | Available | Unavailable |
| [No training on API or business data by default](https://openai.com/business-data/) | Unavailable | Unavailable | Available | Available | Available |
| [Analytics dashboard](/codex/enterprise/governance#analytics-dashboard) | Unavailable | Unavailable | Unavailable | Available | Unavailable |
| [Analytics API](/codex/enterprise/governance#analytics-api) | Unavailable | Unavailable | Unavailable | Available | Unavailable |
| [Compliance API and audit logs](/codex/enterprise/governance#compliance-api) | Unavailable | Unavailable | Unavailable | Available | Unavailable |
| [Codex Security for connected GitHub repositories](/codex/security) | Unavailable | Unavailable | Unavailable | Available | Unavailable |

* Limited means the feature is currently limited to specific regions. Check the individual feature documentation for geo restrictions.

† Some first-party plugins are not available.
