### 术语表

Source: [Glossary](https://developers.openai.com/codex/glossary.md)

使用此术语表快速查阅 Codex 在 app、CLI、IDE 扩展、Cloud、SDK 以及相关集成中的术语。

| 术语 | 适用范围 | 定义 |
| --- | --- | --- |
| [Agent](01-codex.md) | App, CLI, IDE 扩展, Cloud | 在上下文上推理、使用工具并完成任务的 Codex 工作单元。 |
| [AGENTS.md](50-custom-instructions-with-agents-md.md) | App, CLI, IDE 扩展, Cloud | 为 Codex 提供持久说明的仓库或用户指导文件。 |
| [Analytics dashboard](66-governance.md#analytics-dashboard) | 企业 | 用于查看 Codex 使用情况、采用情况和代码审查指标的管理员视图。 |
| [API key sign-in](18-authentication-and-sessions.md#sign-in-with-an-api-key) | App, CLI, IDE 扩展 | 使用 OpenAI API key 进行身份验证。 |
| [Approval policy](13-agent-approvals-security.md#sandbox-and-approvals) | App, CLI, IDE 扩展 | 规定 Codex 何时必须在采取操作前请求确认的规则。 |
| [Approval request](13-agent-approvals-security.md#automatic-approval-reviews) | App, CLI, IDE 扩展 | Codex 请求允许执行受限制操作。 |
| [Apps (connectors)](78-plugins.md) | App, CLI, IDE 扩展 | 让 Codex 访问外部服务的集成。可通过插件获得，也称为 connectors。 |
| [Appshot](43-appshots.md) | App | 发送到 Codex 线程的最前方 app 窗口快照。 |
| [Auth cache](18-authentication-and-sessions.md#login-caching) | App, CLI, IDE 扩展 | 本地保存并由 Codex 复用的登录凭据。 |
| [Automatic approval review](13-agent-approvals-security.md#automatic-approval-reviews) | App, CLI, IDE 扩展 | 在符合条件的审批请求继续之前进行的模型审查。 |
| [Automation](24-automations.md) | App | 计划执行或重复执行的 Codex 任务。 |
| [Automation run](24-automations.md#managing-tasks) | App | 一次计划自动化执行，可能报告发现或将自身归档。 |
| [Browser use](36-in-app-browser.md#browser-use) | App | 让 Codex 直接操作 app 内浏览器的 app 功能。 |
| [Chat](27-codex-app-features.md#chats) | App | 不绑定到项目的 Codex 对话。 |
| [ChatGPT sign-in](18-authentication-and-sessions.md#sign-in-with-chatgpt) | App, CLI, IDE 扩展, Cloud | 使用 ChatGPT 账户和工作区权限进行身份验证。 |
| [Chronicle](70-chronicle.md) | App | 从近期屏幕上下文构建记忆的可选功能。 |
| [Cloud](47-codex-web.md) | App, IDE 扩展, Web | Codex 在 OpenAI 托管环境中远程工作的模式。 |
| [Cloud environment](25-cloud-environments.md) | Cloud | 用于 Codex cloud 任务的已配置容器设置。 |
| [Cloud task](25-cloud-environments.md#how-codex-cloud-tasks-run) | Cloud | 在云环境中远程执行的 Codex 任务。 |
| [Cloud thread](07-prompting.md#threads) | Cloud | 在 Codex cloud 环境中运行的线程。 |
| [Codex](01-codex.md) | App, CLI, IDE 扩展, Web, Cloud, SDK | OpenAI 面向软件开发任务的 coding agent。 |
| [Codex app](44-codex-app.md) | 桌面端 | 用于并行运行 Codex 线程的桌面 app，内置 worktree、自动化和 Git 功能。 |
| [Codex app-server](57-codex-app-server.md) | App, IDE 扩展, SDK | 本地 JSON-RPC 服务器，用于在自定义客户端中嵌入 Codex 线程、轮次、审批、历史和流式事件。 |
| [Codex CLI](45-codex-cli.md) | 终端 | 用于以交互方式或脚本方式运行 Codex 的终端客户端。 |
| [Codex cloud](47-codex-web.md) | Web, App, IDE 扩展 | OpenAI 托管的执行环境，Codex 可在其中远程处理仓库任务。 |
| [codex exec](60-non-interactive-mode.md) | CLI | 用于从脚本或 CI 非交互运行 Codex 的 CLI 命令。 |
| [Codex IDE extension](46-codex-ide-extension.md) | IDE | 在 VS Code、JetBrains IDE、Cursor 和 Windsurf 等 IDE 中使用 Codex 的编辑器集成。 |
| [Codex SDK](59-codex-sdk.md) | SDK | 用于构建 Codex 驱动工作流或集成的编程接口。 |
| [Codex web](47-codex-web.md) | 浏览器 | 用于委派 cloud 任务的浏览器版 Codex 界面。 |
| [Codex-managed worktree](42-worktrees.md#codex-managed-and-permanent-worktrees) | App | Codex 为某个线程创建并管理的临时 worktree。 |
| [Compaction](07-prompting.md#context) | App, CLI, IDE 扩展, Cloud | 总结较早上下文，使长时间运行的工作可以继续。 |
| [Compliance API](66-governance.md#compliance-api) | 企业 | 用于导出 Codex 活动和审计元数据的 API。 |
| [Computer use](35-computer-use.md) | App | 让 Codex 通过 UI 与桌面应用交互的 app 功能。 |
| [config.toml](16-configuration-reference.md#configtoml) | App, CLI, IDE 扩展 | 本地 Codex 配置文件。 |
| [Connected host](79-remote-connections.md#what-comes-from-the-connected-host) | App, 移动端 | 为远程 Codex 工作提供文件、工具和 shell 访问的计算机或开发环境。 |
| [Connector](78-plugins.md) | App, Cloud | 让 Codex 访问外部服务的 app 集成。可通过插件获得，也称为 apps。 |
| [Container cache](25-cloud-environments.md#container-caching) | Cloud | 保存的 cloud 容器状态，用于加速后续任务。 |
| [Context](07-prompting.md#context) | App, CLI, IDE 扩展, Cloud, SDK | Codex 工作时可使用的信息，例如文件、先前消息、工具输出和说明。 |
| [Context window](https://developers.openai.com/api/docs/guides/conversation-state#managing-the-context-window) | App, CLI, IDE 扩展, Cloud, SDK | 模型一次能考虑的最大信息量。 |
| [Custom agent](81-subagents-2.md#custom-agents) | App, CLI | 带有自身说明和设置的用户定义 agent 角色。 |
| [Deny-read rule](77-permissions.md#deny-reads-with-exact-paths-or-globs) | App, CLI, IDE 扩展, 企业 | 阻止 Codex 读取敏感路径或 glob 匹配项的文件系统权限规则。 |
| [Diff](38-review.md#what-changes-it-shows) | App, Git, 审查 | 用于检查、评论、暂存或还原的一组 Git 文件变更。 |
| [Domain allowlist](23-agent-internet-access.md#domain-allowlist) | Cloud | 启用 agent 互联网访问时 Codex cloud 可访问的一组域名。 |
| [Environment (local)](37-local-environments.md) | App, Worktree | 用于告诉 Codex 如何为项目设置 worktree 的 app 配置。 |
| [Environment variable](25-cloud-environments.md#environment-variables-and-secrets) | Cloud, CLI, IDE 扩展 | 任务执行期间可用的运行时配置值。 |
| [Ephemeral session](60-non-interactive-mode.md#basic-usage) | CLI | 完成后跳过保存会话状态的非交互运行。 |
| [Fast mode](08-speed.md#fast-mode) | CLI, IDE 扩展 | 让受支持模型以更高点数成本更快响应的速度设置。 |
| [Filesystem permission](77-permissions.md#filesystem-permissions) | App, CLI, IDE 扩展 | 授予或拒绝路径读写访问的权限配置规则。 |
| [Finding](24-automations.md#managing-tasks) | App | 自动化发现并呈现的重要结果或问题。 |
| [Full access](15-sandbox.md#configure-defaults) | App, CLI, IDE 扩展 | Codex 在没有常规沙盒限制的情况下运行的模式。 |
| [Git worktree](42-worktrees.md#whats-a-worktree) | App, Git | 同一仓库的第二个 checkout，用于并行分支工作。 |
| [Handoff](42-worktrees.md#working-between-local-and-worktree) | App | 在线程及其工作内容在 Local 和 Worktree 之间移动。 |
| [Heartbeat](24-automations.md#thread-automations) | App | 按计划将 Codex 带回同一对话的重复线程唤醒，也称为 thread automation。 |
| [Hook](73-hooks.md) | App, CLI, IDE 扩展 | 当 Codex 事件匹配时运行的生命周期处理程序，例如工具使用、权限请求或轮次停止。 |
| [Hook event](73-hooks.md#config-shape) | App, CLI, IDE 扩展 | 已配置 hook handler 可以运行的生命周期节点。 |
| [Hunk](38-review.md#staging-and-reverting-files) | App, Git, 审查 | diff 中可独立暂存、取消暂存或还原的连续片段。 |
| [Inline comment](38-review.md#inline-comments-for-feedback) | App | 附加到 diff 特定行的反馈。 |
| [Live web search](19-config-basics.md#web-search-mode) | App, CLI, IDE 扩展 | 用于获取最新信息的实时网页查询。 |
| [Local](42-worktrees.md#working-between-local-and-worktree) | App, CLI, IDE 扩展 | Codex 在用户电脑上工作的模式。 |
| [Local thread](07-prompting.md#threads) | App, CLI, IDE 扩展 | 在用户机器上运行的线程。 |
| [Maintenance script](25-cloud-environments.md#container-caching) | Cloud | 缓存的 cloud 容器恢复时可运行的可选脚本。 |
| [Managed configuration](67-managed-configuration.md) | 企业 | 组织控制的 Codex 默认值和限制。 |
| [MCP](53-model-context-protocol.md) | App, CLI, IDE 扩展 | Model Context Protocol，一种将 Codex 连接到外部工具和上下文的标准。 |
| [MCP resource](53-model-context-protocol.md#supported-mcp-features) | App, CLI, IDE 扩展 | MCP server 暴露给 Codex 检查的可读上下文。 |
| [MCP server](53-model-context-protocol.md#supported-mcp-features) | App, CLI, IDE 扩展 | 通过 MCP 暴露的外部工具或上下文提供者。 |
| [MCP tool](53-model-context-protocol.md#supported-mcp-features) | App, CLI, IDE 扩展 | MCP server 暴露并可由 Codex 在任务中调用的操作。 |
| [MDM](67-managed-configuration.md#macos-managed-preferences-mdm) | 企业 | 用于分发设备配置文件和托管 Codex 设置的移动设备管理工具。 |
| [Memories](74-memories.md) | App, CLI, IDE 扩展 | Codex 可跨会话复用的本地存储上下文。 |
| [Model](20-model-selection.md) | App, CLI, IDE 扩展, Cloud, SDK | Codex 用于推理和工具工作的 AI 模型。 |
| [Network access](13-agent-approvals-security.md#network-access-) | App, CLI, IDE 扩展, Cloud | 命令或环境访问互联网的权限。 |
| [Network policy](13-agent-approvals-security.md#network-policy) | App, CLI, IDE 扩展 | 约束沙盒出站网络流量的基于域名的允许和拒绝规则。 |
| [Non-interactive mode](60-non-interactive-mode.md) | CLI | 从脚本或 CI 运行 Codex 的 CLI 模式。 |
| [Output schema](60-non-interactive-mode.md#create-structured-outputs-with-a-schema) | CLI | 传递给 `codex exec`、用于约束最终响应的 JSON Schema。 |
| [Permanent worktree](42-worktrees.md#codex-managed-and-permanent-worktrees) | App | 作为独立项目保留的长期 worktree。 |
| [Permission profile](77-permissions.md#define-and-select-a-profile) | App, CLI, IDE 扩展 | 组合本地命令执行的文件系统和网络规则的命名最小权限策略。 |
| [Plan](05-best-practices.md#plan-first-for-difficult-tasks) | App, CLI, IDE 扩展, Cloud | Codex 为完成任务提出或跟踪的步骤。 |
| [Plugin](78-plugins.md) | App, CLI, IDE 扩展 | 可分发 skills、tools 和 integrations 的可安装 bundle。 |
| [Plugin manifest](69-build-plugins.md#plugin-structure) | App, CLI, IDE 扩展, 插件 | 标识插件并指向内含 skills、apps、MCP servers、hooks 和 metadata 的插件元数据文件。 |
| [Prefix rule](54-rules.md#understand-the-rules-language) | App, CLI, IDE 扩展, 企业 | 允许、提示或禁止匹配命令前缀的命令规则模式。 |
| [Profile](17-advanced-configuration.md#profiles) | CLI, IDE 扩展 | Codex 的命名配置预设。 |
| [Progressive disclosure](48-agent-skills.md) | App, CLI, IDE 扩展 | 仅在需要时加载 skill 细节，以节省上下文。 |
| [Project](27-codex-app-features.md#multitask-across-projects) | App | Codex 工作的已选代码库或文件夹。 |
| [Prompt](07-prompting.md) | App, CLI, IDE 扩展, Cloud, SDK | 发送给 Codex 的用户说明或请求。 |
| [Pull request review](38-review.md#pull-request-reviews) | App, CLI, GitHub | Codex 对变更的审查，或对 pull request 的反馈。 |
| [RBAC](64-admin-setup.md#step-2-set-up-custom-roles-rbac) | 企业 | 用于工作区权限的基于角色的访问控制。 |
| [Read-only mode](15-sandbox.md) | App, CLI, IDE 扩展 | Codex 可检查但未经批准不能修改的模式。 |
| [Reasoning effort](19-config-basics.md#reasoning-effort) | App, CLI, IDE 扩展, SDK | 控制模型使用多少推理预算的设置。 |
| [Remote connection](79-remote-connections.md) | App, 移动端 | 让 Codex 通过已连接 host 从另一台设备工作的连接。 |
| [requirements.toml](16-configuration-reference.md#requirementstoml) | 企业 | 用于托管 Codex 设置的管理员强制 requirements 文件。 |
| [Review pane](38-review.md) | App | 用于检查 diff、评论和 Git 变更的 app 视图。 |
| [Rules](54-rules.md) | App, CLI, IDE 扩展 | 允许、提示或拒绝命令前缀或权限例外的策略。 |
| [Sandbox](15-sandbox.md) | App, CLI, IDE 扩展 | 限制 Codex 命令可访问或可修改内容的强制边界。 |
| [Sandbox mode](19-config-basics.md#sandbox-level) | App, CLI, IDE 扩展 | 定义 Codex 文件系统和网络限制的配置。 |
| [Sandbox preset](59-codex-sdk.md#sandbox-presets) | SDK | SDK 中表示常见沙盒策略的简写，例如 read-only、workspace-write 或 full access。 |
| [Schedule](24-automations.md) | App | 自动化的计时规则。 |
| [Secret](25-cloud-environments.md#environment-variables-and-secrets) | Cloud | 可用于 setup scripts、但会在 agent 阶段前移除的加密值。 |
| [Setup script](37-local-environments.md#setup-scripts) | App worktrees | 在 agent 开始前运行，用于安装依赖或准备工具的脚本。 |
| [Skill](48-agent-skills.md) | App, CLI, IDE 扩展 | 带有说明以及可选脚本或参考资料的可复用工作流包。 |
| [Skill invocation](48-agent-skills.md#how-codex-uses-skills) | App, CLI, IDE 扩展 | 显式或隐式激活 skill。 |
| [Slash command](39-slash-commands-in-codex-cli.md) | CLI | 以斜杠开头、用于控制或检查 Codex CLI 会话的命令。 |
| [Standalone automation](24-automations.md) | App | 报告独立 findings 的独立计划运行。 |
| [STDIO MCP server](53-model-context-protocol.md#stdio-servers) | CLI, IDE 扩展 | 由已配置命令和参数作为本地进程启动的 MCP server。 |
| [Streamable HTTP MCP server](53-model-context-protocol.md#streamable-http-servers) | CLI, IDE 扩展 | 通过 HTTP 访问的 MCP server，可选使用 bearer token 或 OAuth 身份验证。 |
| [Subagent](68-subagents.md) | App, CLI | 被派生出来处理部分任务的专门 child agent。 |
| [Subagent workflow](68-subagents.md#core-terms) | App, CLI | Codex 并行运行委派 agents 并合并其结果的工作流。 |
| [Task](24-automations.md#managing-tasks) | App, CLI, IDE 扩展, Cloud, SDK | Codex 被要求完成的工作单位。 |
| [Thread](07-prompting.md#threads) | App, CLI, IDE 扩展, Cloud, SDK | 包含 prompts、模型输出和工具活动的单个 Codex 会话。 |
| [Thread automation](24-automations.md#thread-automations) | App | 附加到现有 thread 的重复唤醒，也称为 heartbeat。 |
| [Thread fork](57-codex-app-server.md#start-or-resume-a-thread) | app-server, SDK | 从现有 thread 的存储历史分支出来的新 thread。 |
| [Turn](57-codex-app-server.md#core-primitives) | App, CLI, IDE 扩展, Cloud, SDK | thread 中的一轮交换，通常包括用户 prompt 以及 Codex 的响应和操作。 |
| [Universal image](25-cloud-environments.md#default-universal-image) | Cloud | 带有常用工具的默认 Codex cloud 容器镜像。 |
| [Web search cache](19-config-basics.md#web-search-mode) | App, CLI, IDE 扩展 | Codex 可在不实时浏览的情况下使用的预索引搜索结果。 |
| [Worktree](42-worktrees.md) | App | Codex 在独立 Git worktree 中隔离变更的模式。 |
| [Writable roots](13-agent-approvals-security.md#protected-paths-in-writable-roots) | App, CLI, IDE 扩展 | Codex 被允许修改的目录。 |
