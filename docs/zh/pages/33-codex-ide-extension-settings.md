### Codex IDE 扩展设置

Source: [Codex IDE extension settings](https://developers.openai.com/codex/ide/settings.md)

使用这些设置来自定义 Codex IDE 扩展。

#### 更改设置

要更改设置，请按以下步骤操作：

1. 打开你的编辑器设置。
2. 搜索 `Codex` 或设置名称。
3. 更新值。

Codex IDE 扩展使用 Codex CLI。某些行为（例如默认模型、批准和沙盒设置）请在共享的 `~/.codex/config.toml` 文件中配置，而不是在编辑器设置中配置。请参阅 [Config basics](https://developers.openai.com/codex/config-basic)。

该扩展也会遵循 VS Code 内置的聊天字体设置，用于 Codex 对话界面。

#### 设置参考

| 设置                                         | 说明                                                                                                                                                      |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `chat.fontSize`                              | 控制 Codex 侧边栏中的聊天文本，包括对话内容和输入区。                                                                                                     |
| `chat.editor.fontSize`                       | 控制 Codex 对话中的代码渲染内容，包括代码片段和 diff。                                                                                                    |
| `chatgpt.cliExecutable`                      | 仅用于开发：Codex CLI 可执行文件路径。除非你正在主动开发 Codex CLI，否则不需要设置它。如果手动设置，扩展的某些部分可能无法按预期工作。                   |
| `chatgpt.commentCodeLensEnabled`             | 在待办注释上方显示 CodeLens，以便你可以用 Codex 完成它们。                                                                                                |
| `chatgpt.localeOverride`                     | Codex UI 的首选语言。留空则自动检测。                                                                                                                     |
| `chatgpt.openOnStartup`                      | 扩展启动完成后聚焦 Codex 侧边栏。                                                                                                                         |
| `chatgpt.runCodexInWindowsSubsystemForLinux` | 仅 Windows：当 Windows Subsystem for Linux (WSL) 可用时，在 WSL 中运行 Codex。当你的仓库和工具链位于 WSL2，或需要 Linux 原生工具链时使用。否则，Codex 可以配合 Windows 沙盒在 Windows 上原生运行。更改此设置会重新加载 VS Code 以应用变更。 |
