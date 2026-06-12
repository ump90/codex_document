### Codex IDE 扩展

Source: [Codex IDE extension](https://developers.openai.com/codex/ide.md)

Codex 是 OpenAI 的编程代理，可以读取、编辑和运行代码。它帮助你更快地构建、修复 bug，并理解不熟悉的代码。借助 Codex VS Code extension，你可以在 IDE 中并排使用 Codex，或将任务委派给 Codex Cloud。

ChatGPT Plus、Pro、Business、Edu 和 Enterprise 计划包含 Codex。请查看[包含哪些内容](02-codex-pricing.md)了解更多。

[观看 Codex IDE extension overview 视频](https://www.youtube.com/watch?v=sd21Igx4HtA)。

#### 扩展设置

Codex IDE extension 可用于 Cursor 和 Windsurf 等 VS Code forks。

你可以从 [Visual Studio Code Marketplace](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt) 获取 Codex extension，也可以按 IDE 下载：

- [Download for Visual Studio Code](vscode:extension/openai.chatgpt)
- [Download for Cursor](cursor:extension/openai.chatgpt)
- [Download for Windsurf](windsurf:extension/openai.chatgpt)
- [Download for Visual Studio Code Insiders](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt)
- [Download for JetBrains IDEs](#jetbrains-ide)

适用于 VS Code-compatible editors 和 JetBrains IDEs 的 Codex IDE integrations 可在 macOS、Windows 和 Linux 上使用。在 Windows 上，可以配合 Windows sandbox 原生运行 Codex；当你需要 Linux 原生环境时，也可以使用 WSL2。设置详情请参阅 [Windows 设置指南](83-windows-platform.md)。

安装后，你会在编辑器侧边栏中看到 Codex。在 VS Code 中，Codex 默认在右侧边栏打开。如果你使用 VS Code 且没有立即看到 Codex，请重启编辑器。

如果你使用 Cursor，activity bar 默认水平显示。折叠项可能隐藏 Codex，因此你可以 pin 它并重新排列扩展顺序。

![Codex extension](https://cdn.openai.com/devhub/docs/codex-extension.webp)

#### JetBrains IDE 集成

如果你想在 Rider、IntelliJ、PyCharm 或 WebStorm 等 JetBrains IDE 中使用 Codex，请安装 JetBrains IDE integration。它支持使用 ChatGPT、API key 或 JetBrains AI subscription 登录。

[为 JetBrains IDE 安装 Codex](https://blog.jetbrains.com/ai/2026/01/codex-in-jetbrains-ides/)

##### 将 Codex 移到右侧边栏

在 VS Code 中，Codex 会自动显示在右侧边栏。如果你更希望它显示在主（左）侧边栏，可以把 Codex 图标拖回左侧 activity bar。

在 Cursor 等 VS Code forks 中，你可能需要手动将 Codex 移到右侧边栏。为此，你可能需要先临时更改 activity bar orientation：

1. 打开编辑器设置并搜索 `activity bar`（在 Workbench settings 中）。
2. 将 orientation 更改为 `vertical`。
3. 重启编辑器。

![codex-workbench-setting](https://cdn.openai.com/devhub/docs/codex-workbench-setting.webp)

现在将 Codex 图标拖到右侧边栏，例如放在 Cursor chat 旁边。Codex 会作为侧边栏中的另一个 tab 显示。

移动后，将 activity bar orientation 重置为 `horizontal`，以恢复默认行为。如果之后改变主意，你可以随时把 Codex 拖回主（左）侧边栏。

#### 登录

安装 extension 后，它会提示你使用 ChatGPT 账户或 API key 登录。你的 ChatGPT 计划包含使用额度，因此无需额外设置即可使用 Codex。可在[定价页面](02-codex-pricing.md)了解更多信息。

#### 更新 extension

Extension 会自动更新，但你也可以在 IDE 中打开 extension 页面检查更新。

#### 设置键盘快捷键

Codex 包含可在 IDE settings 中绑定为 keyboard shortcuts 的命令，例如切换 Codex chat，或把条目添加到 Codex context。

要查看所有可用命令并绑定键盘快捷键，请选择 Codex chat 中的 settings 图标，然后选择 **Keyboard shortcuts**。

你也可以参考 [Codex IDE extension commands](31-codex-ide-extension-commands.md) 页面。支持的 slash commands 列表见 [Codex IDE extension slash commands](34-codex-ide-extension-slash-commands.md)。如果你刚开始使用 Codex，请阅读[最佳实践指南](05-best-practices.md)。

---

#### 使用 Codex IDE extension 工作

- [使用编辑器上下文提示](32-codex-ide-extension-features.md)：使用打开的文件、选区和 `@file` 引用，让较短的 prompt 得到更相关的结果。
- [切换模型](32-codex-ide-extension-features.md)：使用默认模型，或切换到其他模型以利用各自优势。
- [调整推理强度](32-codex-ide-extension-features.md)：选择 `low`、`medium` 或 `high`，根据任务在速度和深度之间取舍。
- [图片生成](32-codex-ide-extension-features.md)：无需离开编辑器即可生成或编辑图片；需要迭代时可使用参考素材。
- [选择审批模式](32-codex-ide-extension-features.md)：根据你希望 Codex 拥有多少自主权，在 `Chat`、`Agent` 和 `Agent (Full Access)` 之间切换。
- [委派到云端](32-codex-ide-extension-features.md)：把较长的作业 offload 到云端环境，然后无需离开 IDE 即可监控进度并审查结果。
- [跟进云端工作](32-codex-ide-extension-features.md)：预览云端变更、请求后续处理，并把生成的 diff 应用到本地以测试和收尾。
- [IDE extension commands](31-codex-ide-extension-commands.md)：浏览可从命令面板运行并绑定到键盘快捷键的完整命令列表。
- [Slash commands](34-codex-ide-extension-slash-commands.md)：使用 slash commands 控制 Codex 行为，并从 chat 快速更改常用设置。
- [Extension settings](33-codex-ide-extension-settings.md)：通过模型、审批和其他默认值等 editor settings，把 Codex 调整到适合你的工作流。
