### 在 Slack 中使用 Codex

Source: [Use Codex in Slack](https://developers.openai.com/codex/integrations/slack.md)

使用 Slack 中的 Codex，可以从频道和线程发起编码任务。用提示提及 `@Codex`，Codex 会创建云端任务并回复结果。

#### 设置 Slack 应用

1. 设置 [Codex cloud tasks](47-codex-web.md)。你需要 Plus、Pro、Business、Enterprise 或 Edu 计划（参见 [ChatGPT pricing](https://chatgpt.com/pricing)）、已连接的 GitHub 账户，以及至少一个[环境](25-cloud-environments.md)。
2. 前往 [Codex settings](https://chatgpt.com/codex/settings/connectors)，为你的工作区安装 Slack app。根据你的 Slack 工作区政策，可能需要管理员批准安装。
3. 将 `@Codex` 添加到频道。如果尚未添加，在你提及时 Slack 会提示你。

#### 启动任务

1. 在频道或线程中提及 `@Codex` 并包含你的提示。Codex 可以引用线程中较早的消息，因此你通常无需重新说明上下文。
2. （可选）在提示中指定环境或仓库，例如：`@Codex fix the above in openai/codex`。
3. 等待 Codex 作出反应（👀）并回复任务链接。完成后，Codex 会发布结果，并根据你的设置在线程中发布答案。

<a id="how-codex-chooses-an-environment-and-repo"></a>

#### Codex 如何选择环境和仓库

- Codex 会检查你有权访问的环境，并选择最匹配你请求的一个。如果请求含糊不清，它会回退到你最近使用过的环境。
- 任务会针对该环境的 repo map 中列出的第一个仓库的 default branch 运行。如果你需要不同默认值或更多仓库，请在 Codex 中更新 repo map。
- 如果没有合适的环境或仓库可用，Codex 会在 Slack 中回复修复问题的说明，然后再重试。

#### 企业数据控制

默认情况下，Codex 会在线程中回复答案，其中可能包含来自其运行环境的信息。
为防止这种情况，Enterprise 管理员可以在 [ChatGPT workspace settings](https://chatgpt.com/admin/settings) 中清除 **Allow Codex Slack app to post answers on task completion**。当管理员关闭答案后，Codex 只会回复任务链接。

#### 数据使用、隐私与安全

当你提及 `@Codex` 时，Codex 会接收你的消息和线程历史，以理解请求并创建任务。
数据处理遵循 OpenAI 的 [Privacy Policy](https://openai.com/privacy)、[Terms of Use](https://openai.com/terms/) 和其他适用的 [policies](https://openai.com/policies)。
有关安全的更多信息，请参阅 Codex [security documentation](13-agent-approvals-security.md)。

Codex 使用大语言模型，可能会出错。请始终审查答案和 diff。

#### 提示与故障排查

- **缺少连接**：如果 Codex 无法确认你的 Slack 或 GitHub 连接，它会回复一个用于重新连接的链接。
- **意外的环境选择**：在线程中回复你想使用的环境（例如 `Please run this in openai/openai (applied)`），然后再次提及 `@Codex`。
- **较长或复杂的线程**：在最新消息中总结关键细节，以免 Codex 漏掉埋在较早线程位置的上下文。
- **工作区发帖**：某些 Enterprise 工作区会限制发布最终答案。在这些情况下，请打开任务链接查看进度和结果。
- **更多帮助**：请参阅 [OpenAI Help Center](https://help.openai.com/)。

## 非交互式和程序化接口

<a id="automation-and-programmatic-interfaces"></a>

用于 CI、SDK 使用、app-server、GitHub Actions 和相关 agents 工具的自动化路径。
