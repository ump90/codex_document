### Codex 应用设置

Source: [Codex app settings](https://developers.openai.com/codex/app/settings.md)

使用设置面板调整 Codex app 的行为、文件打开方式，以及它如何连接工具。从 app 菜单打开 [**Settings**](codex://settings)，或按 Cmd+,。

#### 通用

选择文件在哪里打开、线程中显示多少命令输出，以及终端标签页默认在哪里打开。你也可以要求多行提示词使用 Cmd+Enter，或在线程运行时防止系统休眠。

#### 个人资料

使用 **Profile** 查看活动洞察、累计 token、峰值 token、连续使用记录、你的最长任务和 token 活动。你也可以更新个人资料详情，例如头像、显示名称和用户名，并保存带有使用亮点的个人资料卡。面向消费者的 ChatGPT 计划支持分享个人资料卡。

#### 键盘快捷键

打开 **Keyboard Shortcuts** 以查看命令、更改绑定，或将自定义快捷键重置为默认值。使用搜索框按命令名称查找快捷键，或切换到按键搜索并按下组合键，以查找使用该组合键的命令。

#### 通知

选择轮次完成通知何时出现，以及 app 是否应请求通知权限。

#### 智能体配置

App 中的 Codex 智能体继承与 IDE 和 CLI extension 相同的配置。使用 app 内控件进行常见设置，或编辑 `config.toml` 进行高级配置。更多细节请参阅 [Codex 安全](13-agent-approvals-security.md) 和 [配置基础](19-config-basics.md)。

#### 外观

在 **Settings** 中，你可以选择基础主题、调整强调色、背景色和前景色，并更改 UI 和代码字体，从而改变 Codex app 的外观。你也可以与朋友分享你的自定义主题。

#### Codex 宠物

Codex pets 是 app 的可选动画伙伴。在 **Settings** 中，进入 **Appearance** 并选择 **Pets**，以选择内置 pet，或从本地 Codex home 刷新自定义 pets。在输入框中输入 `/pet`，在 **Settings > Appearance** 中使用 **Wake Pet** 或 **Tuck Away Pet**，或按 Cmd+K 或 Ctrl+K 并运行相同命令，以切换浮动覆盖层。

    该覆盖层会在你使用其它应用时保持活动 Codex 工作可见。它会显示活动线程，反映 Codex 正在运行、等待输入还是准备审查，并将该状态与简短进度提示搭配显示，使你无需重新打开线程即可快速了解发生了什么变化。

要创建自己的 pet，请安装 `hatch-pet` skill：

```text
$skill-installer hatch-pet
```

从命令菜单重新加载 skills。按 Cmd+K 或 Ctrl+K，选择 **Force Reload Skills**，然后要求该 skill 创建 pet：

```text
$hatch-pet create a new pet inspired by my recent projects
```

#### Git

使用 Git 设置来标准化分支命名，并选择 Codex 是否使用 force push。你也可以设置 Codex 用于生成 commit message 和 pull request description 的提示词。

#### 集成与 MCP

通过 MCP (Model Context Protocol) 连接外部工具。启用推荐服务器或添加你自己的服务器。如果某个服务器需要 OAuth，app 会启动认证流程。由于 MCP 配置位于 `config.toml`，这些设置也适用于 Codex CLI 和 IDE extension。详情请参阅 [Model Context Protocol 文档](53-model-context-protocol.md)。

#### 浏览器使用

使用这些设置安装或启用捆绑的 Browser plugin、设置 [Codex Chrome extension](29-codex-chrome-extension.md)，并管理允许和阻止的网站。除非你已经允许某个网站，否则 Codex 会在使用前询问。移除被阻止的网站后，Codex 可以在浏览器中使用它之前再次询问。

有关浏览器预览、评论和 browser use 工作流，请参阅 [应用内浏览器](36-in-app-browser.md)。

#### 计算机使用

设置完成后，检查你的 Computer Use 设置，以查看桌面应用访问权限和相关偏好。在 macOS 上，可通过更新 macOS Privacy & Security 设置中的 Screen Recording 或 Accessibility 权限来撤销系统级访问权限。该功能发布时不适用于 EEA、United Kingdom 或 Switzerland。

#### 个性化

选择 **Friendly**、**Pragmatic** 或 **None** 作为你的默认个性。使用 **None** 禁用个性指令。你可以随时更新此设置。

你也可以添加自己的自定义指令。编辑自定义指令会更新你的 [`AGENTS.md` 中的个人指令](50-custom-instructions-with-agents-md.md)。

#### 上下文感知建议

使用上下文感知建议，在你启动或返回 Codex 时显示可能想继续的后续事项和任务。

#### 记忆

在可用时启用 Memories，让 Codex 将过去线程中的有用上下文带入未来工作。有关设置、存储和按线程控制，请参阅 [Memories](74-memories.md)。

#### 已归档线程

**Archived threads** 部分会列出已归档聊天及其日期和项目上下文。使用 **Unarchive** 恢复线程。
