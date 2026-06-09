### 在 Linear 中使用 Codex

Source: [Use Codex in Linear](https://developers.openai.com/codex/integrations/linear.md)

使用 Linear 中的 Codex，可以从 issue 委派工作。将 issue 分配给 Codex，或在评论中提及 `@Codex`，Codex 会创建云端任务，并回复进度和结果。

Linear 中的 Codex 可在付费计划中使用（参见 [Pricing](https://developers.openai.com/codex/pricing)）。

如果你使用 Enterprise 计划，请让你的 ChatGPT 工作区管理员在 [workspace settings](https://chatgpt.com/admin/settings) 中开启 Codex 云端任务，并在 [connector settings](https://chatgpt.com/admin/ca) 中启用 **Codex for Linear**。

#### 设置 Linear 集成

1. 在 [Codex](https://chatgpt.com/codex) 中连接 GitHub，并为你希望 Codex 处理的仓库创建一个[环境](https://developers.openai.com/codex/cloud/environments)，以设置 [Codex cloud tasks](https://developers.openai.com/codex/cloud)。
2. 前往 [Codex settings](https://chatgpt.com/codex/settings/connectors)，为你的工作区安装 **Codex for Linear**。
3. 通过在 Linear issue 的评论线程中提及 `@Codex` 来关联你的 Linear 账户。

#### 将工作委派给 Codex

你可以通过两种方式委派：

#### 将 issue 分配给 Codex

安装集成后，你可以像给队友分配 issue 一样把 issue 分配给 Codex。Codex 会开始工作，并把更新发布回 issue。

#### 在评论中提及 `@Codex`

你也可以在评论线程中提及 `@Codex` 来委派工作或提问。Codex 回复后，可以在线程中继续跟进，以延续同一个会话。

Codex 开始处理 issue 后，会[选择一个环境和仓库](#how-codex-chooses-an-environment-and-repo)来工作。
若要固定到特定仓库，请在评论中包含它，例如：`@Codex fix this in openai/codex`。

跟踪进度：

- 打开 issue 上的 **Activity** 查看进度更新。
- 打开任务链接以更详细地跟进。

任务完成后，Codex 会发布摘要和已完成任务的链接，以便你创建 pull request。

<a id="how-codex-chooses-an-environment-and-repo"></a>

#### Codex 如何选择环境和仓库

- Linear 会基于 issue 上下文建议一个仓库。Codex 会选择最匹配该建议的环境。如果请求含糊不清，它会回退到你最近使用过的环境。
- 任务会针对该环境的 repo map 中列出的第一个仓库的 default branch 运行。如果你需要不同默认值或更多仓库，请在 Codex 中更新 repo map。
- 如果没有合适的环境或仓库可用，Codex 会在 Linear 中回复修复问题的说明，然后再重试。

#### 自动将 issue 分配给 Codex

你可以使用 triage rules 自动将 issue 分配给 Codex：

1. 在 Linear 中，前往 **Settings**。
2. 在 **Your teams** 下，选择你的团队。
3. 在工作流设置中，打开 **Triage** 并启用它。
4. 在 **Triage rules** 中，创建一条 rule，并选择 **Delegate** > **Codex**（以及你想设置的任何其他属性）。

Linear 会自动把进入 triage 的新 issue 分配给 Codex。
当你使用 triage rules 时，Codex 会使用 issue 创建者的账户运行任务。

#### 数据使用、隐私与安全

当你提及 `@Codex` 或将 issue 分配给它时，Codex 会接收你的 issue 内容，以理解请求并创建任务。
数据处理遵循 OpenAI 的 [Privacy Policy](https://openai.com/privacy)、[Terms of Use](https://openai.com/terms/) 和其他适用的 [policies](https://openai.com/policies)。
有关安全的更多信息，请参阅 [Codex security documentation](https://developers.openai.com/codex/agent-approvals-security)。

Codex 使用大语言模型，可能会出错。请始终审查答案和 diff。

#### 提示与故障排查

- **缺少连接**：如果 Codex 无法确认你的 Linear 连接，它会在 issue 中回复一个用于连接账户的链接。
- **意外的环境选择**：在线程中回复你想使用的环境（例如 `@Codex please run this in openai/codex`）。
- **代码位置不对**：在 issue 中添加更多上下文，或在你的 `@Codex` 评论中给出明确说明。
- **更多帮助**：请参阅 [OpenAI Help Center](https://help.openai.com/)。

#### 为本地任务连接 Linear（MCP）

如果你使用 Codex app、CLI 或 IDE 扩展，并希望 Codex 在本地访问 Linear issue，请配置 Codex 使用 Linear Model Context Protocol (MCP) server。

要了解更多信息，请[查看 Linear MCP 文档](https://linear.app/integrations/codex-mcp)。

无论你使用 IDE 扩展还是 CLI，MCP server 的设置步骤都相同，因为两者共享同一配置。

#### 使用 CLI（推荐）

如果你已安装 CLI，请运行：

```bash
codex mcp add linear --url https://mcp.linear.app/mcp
```

这会提示你使用 Linear 账户登录，并将其连接到 Codex。

#### 手动配置

1. 在编辑器中打开 `~/.codex/config.toml`。
2. 添加以下内容：

```toml
[mcp_servers.linear]
url = "https://mcp.linear.app/mcp"
```

3. 运行 `codex mcp login linear` 登录。
