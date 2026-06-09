### 管理员设置

Source: [Admin Setup](https://developers.openai.com/codex/enterprise/admin-setup.md)

本指南面向希望为其工作区设置 Codex 的 ChatGPT Enterprise 管理员。

请将本页用作逐步推出指南。有关详细的策略、配置、自动化和监控信息，请使用链接页面：[Authentication](https://developers.openai.com/codex/auth)、[Agent approvals & security](https://developers.openai.com/codex/agent-approvals-security)、[Access tokens](https://developers.openai.com/codex/enterprise/access-tokens)、[Managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration) 和 [Governance](https://developers.openai.com/codex/enterprise/governance)。

#### 企业级安全和隐私

Codex 支持 ChatGPT Enterprise 安全功能，包括：

- 不使用企业数据进行训练
- App、CLI 和 IDE 的零数据保留（代码保留在开发者环境中）
- 遵循 ChatGPT Enterprise 策略的数据驻留和保留
- 细粒度用户访问控制
- 静态数据加密 (AES-256) 和传输中加密 (TLS 1.2+)
- 通过 ChatGPT Compliance API 进行审计日志记录

安全控制和运行时保护请参阅 [Agent approvals & security](https://developers.openai.com/codex/agent-approvals-security)。更多详情请参考 [Zero Data Retention (ZDR)](https://platform.openai.com/docs/guides/your-data#zero-data-retention)。
更广泛的企业安全概览请参阅 [Codex security white paper](https://trust.openai.com/?itemUid=382f924d-54f3-43a8-a9df-c39e6c959958&source=click)。

#### 前提条件：确定负责人和推出策略

在推出期间，团队成员可能会支持将 Codex 集成到组织中的不同方面。请确保你具备以下负责人：

- **ChatGPT Enterprise 工作区所有者：** 需要由其在工作区中配置 Codex 设置。
- **安全负责人：** 决定 Codex 的代理权限设置。
- **分析负责人：** 将分析和合规 API 集成到你的数据流水线。

决定你将使用哪些 Codex 使用界面：

- **Codex local:** 包括 Codex app、CLI 和 IDE extension。代理在开发者电脑上的沙箱中运行。
- **Codex cloud:** 包括托管 Codex 功能（包括 Codex cloud、iOS、Code Review，以及由 [Slack integration](https://developers.openai.com/codex/integrations/slack) 或 [Linear integration](https://developers.openai.com/codex/integrations/linear) 创建的任务）。代理在托管容器中远程运行，并访问你的代码库。
- **Both:** 同时使用 local + cloud。

你可以启用 local、cloud 或两者，并通过工作区设置和基于角色的访问控制 (RBAC) 控制访问。

#### 步骤 1：在你的工作区中启用 Codex

你可以在 ChatGPT Enterprise 工作区设置中配置 Codex 访问权限。

前往 [Workspace Settings > Settings and Permissions](https://chatgpt.com/admin/settings)。

#### Codex 本地

对于新的 ChatGPT Enterprise 工作区，Codex local 默认启用。如果
你不是 ChatGPT 工作区所有者，可以通过
[安装 Codex](https://developers.openai.com/codex/quickstart) 并使用工作邮箱登录来测试自己是否有访问权限。

开启 **Allow members to use Codex Local**。

这将为允许的用户启用 Codex app、CLI 和 IDE extension。

如果成员需要程序化的 Codex local 工作流，也请开启 **Allow members to use Codex access tokens**，或通过自定义角色授予访问令牌权限。工作区所有者和管理员可以使用 **Access token expiration limit** 设置成员为新令牌可选择的最长过期时间。设置和权限详情请参阅 [Access tokens](https://developers.openai.com/codex/enterprise/access-tokens)。

如果 Codex Local 开关关闭，尝试使用 Codex app、CLI 或 IDE 的用户会看到以下错误：“403 - Unauthorized. Contact your ChatGPT administrator for access.”

#### 为 Codex CLI 启用设备码身份验证

允许开发者在非交互环境中使用 Codex CLI 时通过设备码登录（例如远程开发机器）。更多详情见 [authentication](https://developers.openai.com/codex/auth/)。

#### Codex 云

#### 前提条件

Codex cloud 需要 **GitHub (cloud-hosted) repositories**。如果你的代码库位于本地部署环境或不在 GitHub 上，你可以使用 Codex SDK 在自己的基础设施上构建类似工作流。

要以管理员身份设置 Codex，你必须拥有组织中常用仓库的 GitHub 访问权限。如果你没有所需
访问权限，请与你工程团队中拥有权限的人协作。

#### 在工作区设置中启用 Codex 云

首先，在 [Workspace Settings > Settings and Permissions](https://chatgpt.com/admin/settings) 的 Codex 区域中开启 ChatGPT GitHub Connector。

要为你的工作区启用 Codex cloud，请开启 **Allow members to use Codex cloud**。启用后，用户可以直接从 ChatGPT 左侧导航面板访问 Codex。

注意，Codex 可能最多需要 10 分钟才会出现在 ChatGPT 中。

#### 启用 Codex Slack 应用在任务完成时发布答案

Codex 会在任务完成时将完整答案发回 Slack。否则，Codex 只会发布任务链接。

了解更多请参阅 [Codex in Slack](https://developers.openai.com/codex/integrations/slack)。

#### 启用 Codex 代理访问互联网

默认情况下，Codex cloud 代理在运行时期间没有互联网访问权限，以帮助防范提示注入等安全风险。

此设置允许用户为常见软件依赖域使用允许列表、添加域和受信任站点，并指定允许的 HTTP 方法。

有关互联网访问和运行时控制的安全影响，请参阅 [Agent approvals & security](https://developers.openai.com/codex/agent-approvals-security)。

#### 步骤 2：设置自定义角色 (RBAC)

使用 RBAC 对 Codex local 和 Codex cloud 的访问进行细粒度权限控制。

#### RBAC 能做什么

工作区所有者可以在 ChatGPT 管理设置中使用 RBAC 来：

- 为未分配任何自定义角色的用户设置默认角色
- 创建具有细粒度权限的自定义角色
- 将一个或多个自定义角色分配给组
- 通过 SCIM 自动同步用户到组
- 从 Custom Roles 标签页集中管理角色

用户可以继承多个角色，权限会解析为这些角色中最宽松（限制最少）的访问。

#### 创建 Codex 管理员组

设置专用的 "Codex Admin" 组，而不是将 Codex 管理权限授予广泛人群。

**Allow members to administer Codex** 开关会授予 Codex Admin 角色。Codex Admin 可以：

- 查看 Codex [workspace analytics](https://chatgpt.com/codex/settings/analytics)
- 打开 Codex [Policies page](https://chatgpt.com/codex/settings/policies) 来管理云托管的 `requirements.toml` 策略
- 将这些托管策略分配给用户组，或配置默认兜底策略
- 管理 Codex cloud 环境，包括编辑和删除环境

将此角色用于负责 Codex 推出、策略管理和治理的少数管理员。普通 Codex 用户不需要它。启用此开关不需要 Codex cloud。

推荐 rollout 模式：

- 为应使用 Codex 的人员创建 "Codex Users" 组
- 为应管理 Codex 设置和策略的较少人员创建单独的 "Codex Admin" 组
- 仅将启用了 **Allow members to administer Codex** 的自定义角色分配给 "Codex Admin" 组
- 将 "Codex Admin" 组成员限制为工作区所有者，或指定的平台、IT 和治理操作员
- 如果你使用 SCIM，请让 "Codex Admin" 组由你的身份提供商支撑，使成员变更可审计并集中管理

这种分离让 Codex 推出更容易，同时把分析、环境管理和策略部署限制在受信任管理员范围内。RBAC 设置详情和完整权限模型请参阅 [OpenAI RBAC Help Center article](https://help.openai.com/en/articles/11750701-rbac)。

#### 步骤 3：配置 Codex 本地要求

Codex Admin 可以从 Codex [Policies page](https://chatgpt.com/codex/settings/policies) 部署管理员强制执行的 `requirements.toml` 策略。

当你希望对不同组应用不同的本地 Codex 约束，而不先分发设备级文件时，请使用此页面。托管策略使用 [Managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration) 中描述的同一 `requirements.toml` 格式，因此你可以定义允许的审批策略、沙箱模式、网页搜索行为、网络访问要求、MCP 服务器允许列表、功能固定和限制性命令规则。要禁用 Browser Use、in-app browser 或 Computer Use，请参阅 [Pin feature flags](https://developers.openai.com/codex/enterprise/managed-configuration#pin-feature-flags)。

推荐设置：

1. 为大多数用户创建基线策略，然后仅在需要时创建更严格或更宽松的变体。
2. 将每个托管策略分配给特定用户组，并为其他所有人配置默认兜底策略。
3. 谨慎排序组规则。如果用户匹配多个组特定规则，则应用第一个匹配的规则。
4. 将每个策略视为该组的完整配置档。Codex 不会从后续匹配的组规则中填补缺失字段。

这些云托管策略会在用户使用 ChatGPT 登录时应用于 Codex local 使用界面，包括 Codex app、CLI 和 IDE extension。

#### `requirements.toml` 策略示例

使用云托管的 `requirements.toml` 策略为每个组强制执行你想要的护栏。下面的片段是可改造的示例，而不是必需设置。

示例：限制标准本地推出的网页搜索、沙箱模式和审批：

```toml
allowed_web_search_modes = ["disabled", "cached"]
allowed_sandbox_modes = ["workspace-write"]
allowed_approval_policies = ["on-request"]
```

示例：禁用 Browser Use、in-app browser 和 Computer Use：

```toml
[features]
browser_use = false
in_app_browser = false
computer_use = false
```

示例：定义由管理员拥有的网络要求：

```toml
experimental_network.enabled = true
experimental_network.dangerously_allow_all_unix_sockets = true
experimental_network.allow_local_binding = true
experimental_network.allowed_domains = [
  "api.openai.com",
  "*.example.com",
]
experimental_network.denied_domains = [
  "blocked.example.com",
  "*.exfil.example.com",
]
```

示例：当你希望管理员阻止或把关特定命令时，添加限制性命令规则：

```toml
[rules]
prefix_rules = [
  { pattern = [{ token = "git" }, { any_of = ["push", "commit"] }], decision = "prompt", justification = "Require review before mutating remote history." },
]
```

你可以单独使用任何示例，也可以将它们组合到某个组的单个托管策略中。确切 key、优先级和更多示例请参阅 [Managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration) 和 [Agent approvals & security](https://developers.openai.com/codex/agent-approvals-security)。

#### 检查用户策略

使用工作流末尾的策略查询工具来确认哪个托管策略适用于用户。你可以按组检查策略分配，或输入用户 email 检查。

如果你计划限制本地客户端的登录方法或工作区，请参阅 [Authentication](https://developers.openai.com/codex/auth) 中管理员托管的身份验证限制。

#### 步骤 4：使用团队配置标准化本地配置

希望在组织范围内标准化 Codex 的团队可以使用 Team Config 共享默认值、规则和技能，而不需要在每个本地配置上重复设置。

你可以将 Team Config 设置提交到仓库的 `.codex` 目录下。当用户打开该仓库时，Codex 会自动获取 Team Config 设置。

从流量最高的仓库开始使用 Team Config，让团队在最常使用 Codex 的地方获得一致行为。

| Type                                 | Path          | Use it to                                                                    |
| ------------------------------------ | ------------- | ---------------------------------------------------------------------------- |
| [Config basics](https://developers.openai.com/codex/config-basic) | `config.toml` | 设置沙箱模式、审批、模型、推理强度等默认值。 |
| [Rules](https://developers.openai.com/codex/rules)                | `rules/`      | 控制 Codex 可以在沙箱外运行哪些命令。                    |
| [Skills](https://developers.openai.com/codex/skills)              | `skills/`     | 让你的团队可以使用共享技能。                                   |

位置和优先级请参阅 [Config basics](https://developers.openai.com/codex/config-basic#configuration-precedence)。

#### 步骤 5：配置 Codex 云使用（如果已启用）

此步骤介绍启用 Codex cloud 工作区开关后的仓库和环境设置。

#### 将 Codex 云连接到仓库

1. 导航到 [Codex](https://chatgpt.com/codex) 并选择 **Get started**
2. 选择 **Connect to GitHub** 来安装 ChatGPT GitHub Connector（如果你尚未将 GitHub 连接到 ChatGPT）
3. 安装或连接 ChatGPT GitHub Connector
4. 为 ChatGPT Connector 选择安装目标（通常是你的主要组织）
5. 允许你想连接到 Codex 的仓库

对于 GitHub Enterprise Managed Users (EMU)，用户在 Codex cloud 中连接
仓库之前，组织所有者必须先为该组织安装
Codex GitHub App。

更多信息请参阅 [Cloud environments](https://developers.openai.com/codex/cloud/environments)。

Codex 为每项操作使用短生命周期、最小权限的 GitHub App 安装令牌，并遵循用户现有的 GitHub 仓库权限和分支保护规则。
