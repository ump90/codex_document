### Codex IDE 扩展

Source: [Codex IDE extension](https://developers.openai.com/codex/ide.md)

Codex 是 OpenAI 的编程代理，可以读取、编辑和运行代码。它帮助你更快地构建、修复 bug，并理解不熟悉的代码。借助 Codex VS Code 扩展，你可以在 IDE 中并排使用 Codex，或将任务委派给 Codex Cloud。

ChatGPT Plus、Pro、Business、Edu 和 Enterprise 计划包含 Codex。了解更多关于[包含内容](https://developers.openai.com/codex/pricing)的信息。

#### JetBrains IDE 集成

如果你想在 Rider、IntelliJ、PyCharm 或 WebStorm 等 JetBrains IDE 中使用 Codex，请安装 JetBrains IDE 集成。它支持使用 ChatGPT、API key 或 JetBrains AI 订阅登录。

[为 JetBrains IDE 安装 Codex](https://blog.jetbrains.com/ai/2026/01/codex-in-jetbrains-ides/)

#### 将 Codex 移到右侧边栏

在 VS Code 中，Codex 会自动显示在右侧边栏。
如果你更希望它显示在主（左）侧边栏，可以把 Codex 图标拖回左侧活动栏。

在 Cursor 等 VS Code 分支版本中，你可能需要手动将 Codex 移到右侧边栏。
为此，你可能需要先临时更改活动栏方向：

1. 打开编辑器设置并搜索 `activity bar`（在 Workbench 设置中）。
2. 将方向更改为 `vertical`。
3. 重启编辑器。

现在将 Codex 图标拖到右侧边栏（例如，放在 Cursor 聊天旁边）。Codex 会作为侧边栏中的另一个标签页显示。

移动后，将活动栏方向重置为 `horizontal`，以恢复默认行为。
如果之后改变主意，你可以随时把 Codex 拖回主（左）侧边栏。

#### 登录

安装扩展后，它会提示你使用 ChatGPT 账户或 API key 登录。你的 ChatGPT 计划包含使用额度，因此无需额外设置即可使用 Codex。可在[定价页面](https://developers.openai.com/codex/pricing)了解更多信息。
