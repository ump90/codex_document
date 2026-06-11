### Codex 定价

Source: [Codex Pricing](https://developers.openai.com/codex/pricing.md)

## 计划

### 个人计划

#### Free（$0/月）

在快速编码任务中探索 Codex 能力。

[获取 Free](https://chatgpt.com/plans/free/)

#### Go（$8/月）

将 Codex 用于轻量级编码任务。

[获取 Go](https://chatgpt.com/plans/go)

#### Plus（$20/月）

每周支持几次专注的编码会话。

- Web、CLI、IDE 扩展和 iOS 上的 Codex
- 基于云的集成，例如自动代码审查和 Slack 集成
- 最新模型，包括 GPT-5.5、GPT-5.4 和 GPT-5.3-Codex
- GPT-5.4-mini，用于提高常规本地消息的使用上限
- 使用 [ChatGPT 点数](#credits-overview) 灵活扩展用量
- Plus 计划包含的其他 [ChatGPT 功能](https://chatgpt.com/pricing)

[获取 Plus](https://chatgpt.com/explore/plus?utm_internal_source=openai_developers_codex)

#### Pro（$100/月起）

选择比 Plus 高 5 倍或 20 倍的速率限制。

包含 Plus 的全部内容，并且：

- 访问 GPT-5.3-Codex-Spark（研究预览版），这是一个用于日常编码任务的快速 Codex 模型
- 比 Plus 多 5 倍或 20 倍的 Codex 用量*
- Pro 计划包含的其他 [ChatGPT 功能](https://chatgpt.com/pricing)

[获取 Pro](https://chatgpt.com/explore/pro?utm_internal_source=openai_developers_codex)

[*了解两个档位限制的更多信息。](https://help.openai.com/en/articles/9793128-about-chatgpt-pro-plans)

### Business 和 Enterprise 计划

#### Business（按量付费）

将 Codex 带入你的初创公司或成长型企业。

包含 Plus 的全部内容，并且：

- 根据团队需要分配标准或基于用量的 Codex 席位。[了解更多](https://help.openai.com/en/articles/8792828-what-is-chatgpt-business)
- 更大的虚拟机，用于更快运行云任务
- 使用 [ChatGPT 点数](#credits-overview) 灵活扩展用量
- 安全的专用工作区，具备必要的管理员控制、SAML SSO 和 MFA
- 默认不会使用你的业务数据进行训练。[了解更多](https://openai.com/business-data/)
- Business 计划包含的其他 [ChatGPT 功能](https://chatgpt.com/pricing)

[获取 Business](https://chatgpt.com/codex/team/start)

#### Enterprise & Edu

用企业级功能为整个组织启用 Codex。

包含 Business 的全部内容，并且：

- 优先请求处理
- 企业级安全与控制，包括 SCIM、EKM、用户分析、域名验证和基于角色的访问控制（[RBAC](https://help.openai.com/en/articles/11750701-rbac)）
- 通过 [Compliance API](https://chatgpt.com/admin/api-reference#tag/Codex-Tasks) 提供审计日志和用量监控
- 数据保留和数据驻留控制
- Enterprise 计划包含的其他 [ChatGPT 功能](https://chatgpt.com/pricing)

[联系销售](https://chatgpt.com/contact-sales?utm_internal_source=openai_developers_codex)

### API Key

非常适合 CI 等共享环境中的自动化。

- CLI、SDK 或 IDE 扩展中的 Codex
- 不包含基于云的功能（GitHub 代码审查、Slack 等）
- 对 GPT-5.3-Codex 和 GPT-5.3-Codex-Spark 等新模型的访问会延迟
- 仅按 Codex 使用的 tokens 付费，基于 [API 定价](https://platform.openai.com/docs/pricing)

[了解更多](18-authentication-and-sessions.md)

## 常见问题

### Sites 的费用是多少？

[Sites](80-sites.md) 在预览期间免费。定价信息会稍后公布。

### 我的计划有哪些使用限制？

你可以发送的 Codex 消息数量取决于所用模型、编码任务的规模和复杂度，以及任务是在本地还是云端运行。小脚本或常规函数可能只消耗额度的一小部分；大型代码库、长时间运行的任务，或需要 Codex 保留更多上下文的长会话，则每条消息会消耗更多额度。

GPT-5.5 使用明显更少的 tokens 即可达到与 GPT-5.4 相当的结果。它的 Codex 设置运行更快，并能为多数用户提供更高质量的结果。尽管 GPT-5.5 能力更强，这些效率提升也支持更宽裕的使用限制。

#### Plus

| 模型 | 本地消息 / 5 小时 | 云任务 / 5 小时 | 代码审查 / 5 小时 |
| --- | --- | --- | --- |
| GPT-5.5 | 15-80 | 不可用 | 不可用 |
| GPT-5.4 | 20-100 | 不可用 | 不可用 |
| GPT-5.4-mini | 60-350 | 不可用 | 不可用 |

#### Pro 5x

| 模型 | 本地消息 / 5 小时 | 云任务 / 5 小时 | 代码审查 / 5 小时 |
| --- | --- | --- | --- |
| GPT-5.5 | 80-400 | 不可用 | 不可用 |
| GPT-5.4 | 100-500 | 不可用 | 不可用 |
| GPT-5.4-mini | 300-1750 | 不可用 | 不可用 |

#### Pro 20x

| 模型 | 本地消息 / 5 小时 | 云任务 / 5 小时 | 代码审查 / 5 小时 |
| --- | --- | --- | --- |
| GPT-5.5 | 300-1600 | 不可用 | 不可用 |
| GPT-5.4 | 400-2000 | 不可用 | 不可用 |
| GPT-5.4-mini | 1200-7000 | 不可用 | 不可用 |

#### Business

| 模型 | 本地消息 / 5 小时 | 云任务 / 5 小时 | 代码审查 / 5 小时 |
| --- | --- | --- | --- |
| GPT-5.5 | 15-80 | 不可用 | 不可用 |
| GPT-5.4 | 20-100 | 不可用 | 不可用 |
| GPT-5.4-mini | 60-350 | 不可用 | 不可用 |

#### API Key

| 模型 | 本地消息 / 5 小时 | 云任务 / 5 小时 | 代码审查 / 5 小时 |
| --- | --- | --- | --- |
| GPT-5.5 | 不可用 | 不可用 | 不可用 |
| GPT-5.4 | [按用量计费](https://platform.openai.com/docs/pricing) | 不可用 | 不可用 |
| GPT-5.4-mini | [按用量计费](https://platform.openai.com/docs/pricing) | 不可用 | 不可用 |

说明：本地消息和云任务共享同一个五小时窗口，可能还会有额外的每周限制。对于启用 flexible pricing 的 Enterprise/Edu 用户，没有固定速率限制；用量会随 [credits](#credits-overview) 扩展。未启用 flexible pricing 的 Enterprise 和 Edu 计划在多数功能上拥有与 Plus 相同的每席位使用限制。

当其他 agentic 功能的定价生效后，Codex 使用限制会与这些功能共享。目前这包括 Plus 和 Pro 上的 [ChatGPT for Excel](https://help.openai.com/articles/20001063)。

Speed 配置会提高所有适用模型的点数消耗，因此也会更快使用包含的额度。Fast mode 对受支持模型会以更高速率消耗点数。请参阅 [Speed](08-speed.md) 了解受支持模型和速率。图像生成也会更快使用包含的额度，平均约为 3-5 倍，具体取决于图像质量和尺寸。GPT-5.3-Codex-Spark 仅面向 ChatGPT Pro 用户研究预览，发布时不在 API 中提供。由于它运行在专用低延迟硬件上，用量受单独的使用限制约束，并可能根据需求调整。

### 达到使用限制后会怎样？

达到使用限制的 ChatGPT Plus 和 Pro 用户可以购买额外点数继续工作，而无需升级现有计划。

启用 [flexible pricing](https://help.openai.com/en/articles/11487671-flexible-pricing-for-the-enterprise-edu-and-business-plans) 的 Business、Edu 和 Enterprise 计划可以购买额外 workspace 点数继续使用 Codex。

如果你接近使用限制，也可以切换到更小的模型，让使用限制持续更久。

所有用户还可以使用 API key 运行额外的本地任务，用量按 [标准 API 费率](https://platform.openai.com/docs/pricing) 计费。

<a id="image-generation-usage-limits"></a>

### 图像生成如何计入使用限制？

图像生成计入与本地消息和云任务相同的 Codex 通用使用限制。根据图像质量和尺寸，带图像生成的回合平均会比类似的非图像生成回合快 3-5 倍消耗包含额度。达到包含额度后，图像生成也会从 [credits](#credits-overview) 中扣除。

Free 计划不提供图像生成。使用 API key 调用 Codex 时，图像生成按 API 定价计费，而不是使用包含的 ChatGPT 使用限制。

### 在哪里查看当前使用限制？

你可以在 [Codex 使用情况仪表板](https://chatgpt.com/codex/settings/usage) 查看当前限制。如果想在活跃的 Codex CLI 会话中查看剩余额度，可以使用 `/status`。

<a id="credits-overview"></a>

### credits 如何工作？

credits 可让你在达到包含的使用限制后继续使用 Codex。用量会根据你使用的模型和功能从可用 credits 中扣减，让你不中断地继续工作。

Codex credit 用量基于 API token 费率。Credits 仍是客户购买和消耗的核心定价单位，但用量会按 workspace 消耗的每百万输入 tokens、缓存输入 tokens 和输出 tokens 计算。请在[这里](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)了解 tokens。

下方费率卡展示了 Codex 模型和功能每百万 tokens 的 credit 成本。

少数 Enterprise 客户在迁移到新的 Codex token-based pricing 前，应继续使用旧版费率卡。如需更多信息，请[联系 OpenAI 销售](https://chatgpt.com/contact-sales?utm_internal_source=openai_developers_codex)。

| 每 100 万 tokens 的点数 | 输入 tokens | 缓存输入 tokens | 输出 tokens |
| --- | --- | --- | --- |
| GPT-5.5 | 125 点数 | 12.50 点数 | 750 点数 |
| GPT-5.4 | 62.50 点数 | 6.250 点数 | 375 点数 |
| GPT-5.4-mini | 18.75 点数 | 1.875 点数 | 113 点数 |
| GPT-5.3-Codex-Spark | 研究预览 | 研究预览 | 研究预览 |
| GPT-Image-2 (image) | 200 点数 | 50 点数 | 750 点数 |
| GPT-Image-2 (text) | 125 点数 | 31.25 点数 | 250 点数 |

GPT-5.5 每条消息平均消耗 5-45 点数。Fast mode 对受支持模型会以更高速率消耗点数。请参阅 [Speed](08-speed.md) 了解费率。

Speed 配置会提高所有适用模型的点数消耗。Fast mode 对受支持模型会以更高速率消耗点数。请参阅 [Speed](08-speed.md) 了解受支持模型和费率。

[进一步了解 ChatGPT Plus 和 Pro 中的 credits。](https://help.openai.com/en/articles/12642688)

[进一步了解 ChatGPT Business、Enterprise 和 Edu 中的 credits。](https://help.openai.com/en/articles/11487671-flexible-pricing-for-the-enterprise-edu-and-business-plans)

### 哪些情况算作 Code Review 用量？

Code Review 用量只适用于 Codex 通过 GitHub 运行审查的情况，例如你在 pull request 中标记 `@Codex` 请求审查，或在仓库上启用自动审查。在本地或 GitHub 之外运行的审查会计入通用使用限制。

### 如何让使用限制持续更久？

上面的使用限制和 credits 是平均费率。你可以尝试以下做法最大化额度：

- **控制提示规模。** 给 Codex 的指令要精确，但移除不必要的上下文。
- **减少 AGENTS.md 的大小。** 如果在较大项目中工作，可以通过[在仓库内嵌套 AGENTS.md](50-custom-instructions-with-agents-md.md#layer-project-instructions) 控制注入多少上下文。
- **限制使用的 MCP 服务器数量。** 添加到 Codex 的每个 [MCP](53-model-context-protocol.md) 都会给消息增加更多上下文，并消耗更多额度。不需要时请禁用 MCP 服务器。
- **为常规任务切换到更小的模型。** 根据你从哪个模型切换，使用 GPT-5.4 或 GPT-5.4-mini 可以延长本地消息使用限制。

## 功能可用性

### 访问入口与使用界面

| 功能 | Plus | Pro | Business | Enterprise/Edu | API Key |
| --- | --- | --- | --- | --- | --- |
| [Codex web](47-codex-web.md) | 可用 | 可用 | 可用 | 可用 | 不可用 |
| [用于本地任务的 Codex app](44-codex-app.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [Codex CLI](45-codex-cli.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [IDE 扩展](46-codex-ide-extension.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [Codex SDK、`codex exec` 和可脚本化工作流](59-codex-sdk.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [用于可信自动化的 Codex access token](63-access-tokens.md) | 不可用 | 不可用 | 可用 | 可用 | 不可用 |

### 模型与多模态

| 功能 | Plus | Pro | Business | Enterprise/Edu | API Key |
| --- | --- | --- | --- | --- | --- |
| [Fast mode](08-speed.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [Codex-Spark 研究预览](20-model-selection.md) | 不可用 | 可用 | 不可用 | 不可用 | 不可用 |
| [图像生成与编辑](27-codex-app-features.md#image-generation) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [语音听写](27-codex-app-features.md#voice-dictation) | 可用 | 可用 | 可用 | 可用 | 不可用 |
| [网页搜索](27-codex-app-features.md#web-search) | 可用 | 可用 | 可用 | 可用 | 可用 |

### 本地功能

| 功能 | Plus | Pro | Business | Enterprise/Edu | API Key |
| --- | --- | --- | --- | --- | --- |
| [使用 `/review` 进行本地代码审查](06-example-workflows.md#do-a-local-code-review) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [审批请求的自动审查](65-auto-review.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [沙箱和权限控制](77-permissions.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [项目和独立 app 自动化](24-automations.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [自动化](24-automations.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [Worktree 和内置 Git 工具](42-worktrees.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [本地环境和可重复操作](37-local-environments.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [Appshots](43-appshots.md) | 可用 | 可用 | 可用 | 不可用 | 可用 |

### 浏览器与远程控制

| 功能 | Plus | Pro | Business | Enterprise/Edu | API Key |
| --- | --- | --- | --- | --- | --- |
| [App 内浏览器预览与评论](36-in-app-browser.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [Browser Use 自动化](36-in-app-browser.md#browser-use) | 有限开放* | 有限开放* | 有限开放* | 有限开放* | 有限开放* |
| [Chrome 扩展浏览器控制](29-codex-chrome-extension.md) | 有限开放* | 有限开放* | 有限开放* | 有限开放* | 有限开放* |
| [Computer Use](35-computer-use.md) | 有限开放* | 有限开放* | 有限开放* | 有限开放* | 有限开放* |
| [SSH 远程连接](79-remote-connections.md#connect-to-an-ssh-host) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [移动端远程控制](79-remote-connections.md) | 可用 | 可用 | 可用 | 可用 | 不可用 |

### 自定义与扩展

| 功能 | Plus | Pro | Business | Enterprise/Edu | API Key |
| --- | --- | --- | --- | --- | --- |
| [使用 `AGENTS.md` 编写自定义指令](50-custom-instructions-with-agents-md.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [Skills](48-agent-skills.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [Plugins](78-plugins.md) | 可用 | 可用 | 可用 | 可用 | 部分可用† |
| [Plugin 共享](69-build-plugins.md#share-a-local-plugin-with-your-workspace) | 可用 | 可用 | 可用 | 可用 | 不可用 |
| [App connectors](78-plugins.md) | 可用 | 可用 | 可用 | 可用 | 不可用 |
| [MCP](53-model-context-protocol.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [Subagents 和自定义 agents](81-subagents-2.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [Memories](74-memories.md) | 有限开放* | 有限开放* | 有限开放* | 有限开放* | 有限开放* |
| [Chronicle](70-chronicle.md) | 不可用 | 有限开放* | 不可用 | 不可用 | 不可用 |

### 云端与集成

| 功能 | Plus | Pro | Business | Enterprise/Edu | API Key |
| --- | --- | --- | --- | --- | --- |
| [Codex 云任务](47-codex-web.md) | 可用 | 可用 | 可用 | 可用 | 不可用 |
| [云环境和 setup scripts](25-cloud-environments.md) | 可用 | 可用 | 可用 | 可用 | 不可用 |
| [云端 agent 互联网访问控制](23-agent-internet-access.md) | 可用 | 可用 | 可用 | 可用 | 不可用 |
| [Sites](80-sites.md) | 不可用 | 不可用 | 可用 | 可用 | 不可用 |
| [使用 `@codex` 委派 GitHub issue 和 PR](49-codex-code-review-in-github.md#give-codex-other-tasks) | 可用 | 可用 | 可用 | 可用 | 不可用 |
| [GitHub 代码审查和自动 PR 审查](49-codex-code-review-in-github.md) | 可用 | 可用 | 可用 | 可用 | 不可用 |
| [Slack 云集成](56-use-codex-in-slack.md) | 可用 | 可用 | 可用 | 可用 | 不可用 |
| [Linear 云集成](55-use-codex-in-linear.md) | 可用 | 可用 | 可用 | 可用 | 不可用 |

### 管理、安全与分析

| 功能 | Plus | Pro | Business | Enterprise/Edu | API Key |
| --- | --- | --- | --- | --- | --- |
| [SAML SSO、MFA 和 workspace 用户管理](64-admin-setup.md) | 不可用 | 不可用 | 可用 | 可用 | 不可用 |
| [`requirements.toml` 托管配置](67-managed-configuration.md) | 可用 | 可用 | 可用 | 可用 | 可用 |
| [云端托管配置策略](67-managed-configuration.md#cloud-managed-requirements) | 不可用 | 不可用 | 可用 | 可用 | 不可用 |
| [Codex RBAC 和自定义角色](64-admin-setup.md#step-2-set-up-custom-roles-rbac) | 不可用 | 不可用 | 不可用 | 可用 | 不可用 |
| [SCIM、EKM 和域名验证](64-admin-setup.md#enterprise-grade-security-and-privacy) | 不可用 | 不可用 | 不可用 | 可用 | 不可用 |
| [企业级保留和驻留控制](64-admin-setup.md#enterprise-grade-security-and-privacy) | 不可用 | 不可用 | 不可用 | 可用 | 不可用 |
| [默认不使用 API 或业务数据训练](https://openai.com/business-data/) | 不可用 | 不可用 | 可用 | 可用 | 可用 |
| [分析仪表板](66-governance.md#analytics-dashboard) | 不可用 | 不可用 | 不可用 | 可用 | 不可用 |
| [Analytics API](66-governance.md#analytics-api) | 不可用 | 不可用 | 不可用 | 可用 | 不可用 |
| [Compliance API 和审计日志](66-governance.md#compliance-api) | 不可用 | 不可用 | 不可用 | 可用 | 不可用 |
| [用于已连接 GitHub 仓库的 Codex Security](71-codex-security.md) | 不可用 | 不可用 | 不可用 | 可用 | 不可用 |

* 有限开放表示该功能目前只在特定地区可用。请查看对应功能文档了解地理限制。

† 部分第一方 plugins 不可用。
