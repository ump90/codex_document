### 插件

Source: [Plugins](https://developers.openai.com/codex/plugins.md)

#### 概览

Plugins 将 skills、app integrations 和 MCP servers 打包为 Codex 可复用的工作流。

扩展 Codex 能做的事情，例如：

- 安装 Codex Security plugin，扫描已授权代码并确认可信的漏洞发现。
- 安装 Gmail plugin，让 Codex 读取和管理 Gmail。
- 安装 Google Drive plugin，跨 Drive、Docs、Sheets 和 Slides 工作。
- 安装 Slack plugin，汇总频道或起草回复。
- 安装 [Sites](80-sites.md)，创建并部署托管网站、web app 和游戏。

一个 plugin 可以包含：

- **Skills:** 面向特定工作类型的可复用说明。Codex 可以在需要时加载它们，以便遵循正确步骤，并使用任务所需的参考资料或辅助脚本。
- **Apps:** 与 GitHub、Slack 或 Google Drive 等工具的连接，让 Codex 可以从这些工具读取信息并在其中执行操作。
- **MCP servers:** 为 Codex 提供更多工具或共享信息的服务，通常来自本地项目之外的系统。

你可以通过 marketplace source 发布 plugins 来分享它们，例如用于项目或团队的 repo marketplace。有关 marketplace 设置、打包和分发指导，请参阅 [构建插件](69-build-plugins.md)。

#### 使用和安装插件

#### Codex 应用中的插件目录

在 Codex app 中打开 **Plugins**，浏览并安装精选 plugins。

Plugin directory 会将 plugins 分组为以下类别：

- **Curated by OpenAI:** 对所有 Codex 用户可用的精选 plugins。
- **Shared with you:** 由 ChatGPT 工作区中其他成员与你分享的 plugins。
- **Created by you:** 你创建或添加到自己工作区的 plugins。

#### CLI 中的插件目录

在 Codex CLI 中，运行以下命令打开 plugins 列表：

```text
codex
/plugins
```

CLI 插件浏览器会按 marketplace 对 plugins 分组。使用 marketplace 标签页切换来源，打开 plugin 检查详情，安装或卸载 marketplace 条目，并在已安装 plugin 上按 Space 切换其启用状态。

#### 安装并使用插件

打开 plugin directory 后：

1. 搜索或浏览 plugin，然后打开其详情。
2. 选择安装按钮。在 app 中，选择加号按钮或 **Add to Codex**。在 CLI 中，选择 `Install plugin`。
3. 如果 plugin 需要外部 app，请在提示时连接。有些 plugins 会在安装期间要求你进行身份验证。另一些会等到你首次使用时再要求。
4. 安装后，开始一个新线程并要求 Codex 使用该 plugin。

安装 plugin 后，你可以直接在提示窗口中使用它：

    直接描述任务

      说明你想要的结果，例如 "Summarize unread Gmail threads
      from today" 或 "Pull the latest launch notes from Google Drive."

      当你希望 Codex 为任务选择合适的已安装工具时，使用这种方式。

    选择特定 plugin

      输入 @ 来显式调用 plugin 或它打包的某个 skill。

      当你希望明确指定 Codex 应使用哪个 plugin 或 skill 时，使用这种方式。请参阅 Codex app commands 和 Skills。

#### 权限和数据共享如何工作

安装 plugin 会让它的工作流在 Codex 中可用，但你现有的 [审批设置](13-agent-approvals-security.md) 仍然适用。任何已连接的外部服务仍受其自身的身份验证、隐私和数据共享政策约束。

- 打包的 skills 会在你安装 plugin 后立即可用。
- 如果 plugin 包含 apps，Codex 可能会在设置期间或首次使用时提示你在 ChatGPT 中安装或登录这些 apps。
- 如果 plugin 包含 MCP servers，它们可能需要额外设置或身份验证后才能使用。
- 当 Codex 通过打包的 app 发送数据时，该 app 的条款和隐私政策适用。

#### 移除或关闭插件

要移除 plugin，请从 plugin browser 重新打开它并选择 **Uninstall plugin**。

卸载 plugin 会从 Codex 移除 plugin bundle，但打包的 apps 会保持安装，直到你在 ChatGPT 中管理它们。

如果想保留已安装 plugin 但将其关闭，请将它在 `~/.codex/config.toml` 中的条目设置为 `enabled = false`，然后重启 Codex：

```toml
[plugins."gmail@openai-curated"]
enabled = false
```

#### 构建你自己的插件

如果你想创建、测试或分发自己的 plugin，请参阅 [构建插件](69-build-plugins.md)。该页面涵盖本地脚手架、手动 marketplace 设置、工作区分享、plugin manifests 和打包指导。

#### 插件指南

- [Codex Security plugin](10-codex-security-plugin.md)：扫描已授权代码、确认发现，并准备已审查的修复。
