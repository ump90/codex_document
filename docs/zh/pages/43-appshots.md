### Appshots（应用快照）

Source: [Appshots](https://developers.openai.com/codex/appshots.md)

Appshots 可让你把最前面的应用窗口发送到 Codex 线程。当你正在电脑上的另一个应用中工作，并希望向 Codex 提供当前上下文以便它帮助完成任务时，可以使用 Appshots。

Appshots 可在 macOS 上的 Codex app 中使用。按下两个 Command 键，或按下你自定义的 Appshots 热键，即可拍摄一个 appshot。

#### Appshots 会捕获什么

一个 appshot 只捕获最前面的窗口。它可以包含：

- 可见窗口的图像。
- 该窗口中可用的文本，包括可见文本，以及应用在可见滚动区域之外提供的文本。

将 appshot 添加到线程后，它的行为类似 Codex 附件。Codex 会像保存你手动附加的文件或图像一样，把 appshots 本地存储在会话文件中。

#### 何时使用 appshots

当 Codex 在采取行动前需要来自 Mac 应用的上下文时，请使用 appshots。

示例：

- 分享一个 API 参考页面，并让 Codex 编写使用它的脚本。
- 分享一封邮件或日历视图，并让 Codex 起草下一步内容。
- 分享图像编辑器、设计或预览窗口，并让 Codex 修改相关资产或代码。
- 分享错误、设置面板或应用状态，这些内容展示出来比描述更容易。

#### 拍摄 appshot

1. 在你的 Mac 上打开 Codex app。
2. 打开你想分享的应用和窗口。
3. 按下两个 Command 键，或按下你在 Codex 设置中配置的自定义热键。
4. 如果 Codex 请求 macOS 权限，请允许。
5. 要求 Codex 基于该 appshot 执行任务。

默认情况下，Codex 会为 appshot 启动一个新线程。如果你在过去 60 秒内与某个 Codex 线程交互过，Codex 会改为把 appshot 添加到那个最近的线程。连续拍摄 appshots 会把它们添加到同一个线程。

你可以在 Codex 设置中更改 Appshots 热键。

#### 权限与安全

在能够拍摄 appshots 之前，Codex 可能会请求权限：

- **Screen & System Audio Recording** 允许 Codex 捕获最前面窗口的图像。
- **Accessibility** 允许 Codex 读取最前面窗口中的可用文本。

拍摄 appshot 会与 Codex 共享捕获的图像和可用文本。除非任务需要敏感内容，否则请避免拍摄包含敏感内容的 appshots。

请像审查要与 Codex 共享的截图和文档一样审查 appshots。

#### 限制与故障排查

Appshots 是 Codex app 的功能。请在 macOS 上通过 Codex app 创建它们。如果你在 CLI 中恢复一个已经包含 appshot 的线程，该附件会成为线程历史的一部分，但 CLI 无法创建新的 appshot。

对于某些应用和网站，包括 Google Docs、Gmail、Google Sheets 和 Google Slides，Codex 可能只收到可见截图，而无法收到完整文档或屏幕外文本。如果你安装了匹配的插件，Codex 可以使用该插件访问相关应用内容并帮助处理你的请求。

如果 appshots 无法工作：

1. 打开 **System Settings > Privacy & Security**。
2. 检查 Codex Computer Use 的 **Screen & System Audio Recording** 和 **Accessibility** 权限。
3. 重启 Codex 后重试。
