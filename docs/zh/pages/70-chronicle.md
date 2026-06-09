### Chronicle（长期记忆）

Source: [Chronicle](https://developers.openai.com/codex/memories/chronicle.md)

Chronicle 处于 **选择启用的研究预览** 阶段。它仅面向
macOS 上的 ChatGPT Pro 订阅者开放，且尚未在欧盟、英国和
瑞士可用。启用前，请查看 [Privacy and Security](#privacy-and-security)
小节，以了解详情和当前风险。

Chronicle 使用来自屏幕的上下文增强 Codex memories。当你提示
Codex 时，这些记忆可以帮助它理解你一直在处理的内容，
减少你重复说明上下文的需要。

Chronicle 在 macOS 的 Codex app 中作为选择启用的研究预览提供。
它需要 macOS Screen Recording 和 Accessibility 权限。启用前
请注意，Chronicle 会快速消耗速率限制，增加
提示注入风险，并将未加密记忆存储在你的设备上。

#### Chronicle 如何提供帮助

我们设计 Chronicle 是为了减少你在使用 Codex 工作时需要重复说明的上下文量。通过使用最近的屏幕上下文来改进记忆
构建，Chronicle 可以帮助 Codex 理解你指的是什么，识别
应使用的正确来源，并了解你依赖的工具和工作流。

#### 使用屏幕上的内容

借助 Chronicle，Codex 可以理解你当前正在查看的内容，节省
你的时间并减少上下文切换。

#### 填补缺失上下文

无需精心编写上下文并从零开始。Chronicle 让
Codex 能填补你上下文中的空白。

#### 记住工具和工作流

无需向 Codex 解释应使用哪些工具来完成你的工作。Codex
会随着你的工作而学习，从长远看为你节省时间。

在这些情况下，Codex 使用 Chronicle 提供额外上下文。当另一个
来源更适合这项工作时，例如读取特定文件、Slack thread、
Google Doc、仪表板或 pull request，Codex 会使用 Chronicle 识别
该来源，然后直接使用该来源。

#### 启用 Chronicle

1. 在 Codex app 中打开 Settings。
2. 前往 **Personalization**，并确保 **Memories** 已启用。
3. 在 Memories 设置下方打开 **Chronicle**。
4. 查看同意对话框并选择 **Continue**。
5. 出现提示时授予 macOS Screen Recording 和 Accessibility 权限。
6. 设置完成后，选择 **Try it out** 或开始一个新线程。

如果 macOS 报告 Screen Recording 或 Accessibility 权限被拒绝，
请打开 System Settings &gt; Privacy & Security &gt; Screen Recording 或
Accessibility 并启用 Codex。如果权限受 macOS 或你的
组织限制，Chronicle 会在限制移除且 Codex
获得所需权限后启动。

#### 随时暂停或禁用 Chronicle

你可以控制 Chronicle 何时使用屏幕上下文生成记忆。使用
Codex menu bar icon 选择 **Pause Chronicle** 或 **Resume Chronicle**。在会议前或查看你不希望
Codex 作为上下文使用的敏感内容时，请暂停
Chronicle。要禁用 Chronicle，请返回 **Settings &gt;
Personalization &gt; Memories** 并关闭 **Chronicle**。

你还可以控制是否在某个线程中使用记忆。[了解更多](https://developers.openai.com/codex/memories#control-memories-per-thread)。

#### 速率限制

Chronicle 的工作方式是在后台运行沙箱化代理，从捕获的屏幕图像中生成
记忆。这些代理目前会快速消耗速率限制。

#### 隐私和安全

Chronicle 使用屏幕截图，其中可能包含你屏幕上可见的敏感信息。
它无法访问你的麦克风或系统音频。
未经他人同意，不要使用 Chronicle 记录会议或与他人的沟通。
查看你不想被记入记忆的内容时，请暂停 Chronicle。

#### Chronicle 将我的数据存储在哪里？

屏幕截图是临时的，只会临时保存在你的
电脑上。Chronicle 运行时，临时屏幕截图文件可能出现在
`$TMPDIR/chronicle/screen_recording/` 下。Chronicle 运行时，
超过 6 小时的屏幕截图会被删除。

Chronicle 生成的记忆与其它 Codex memories 一样：
是未加密的 markdown 文件，你可以按需读取和修改。你也可以
让 Codex 搜索它们。如果你想让 Codex 忘记某些内容，可以
删除文件夹内对应文件，或选择性编辑 markdown
文件来移除你想删除的信息。你不应手动
添加新信息。生成的 Chronicle 记忆会本地存储在你的
电脑上的 `$CODEX_HOME/memories_extensions/chronicle/` 下（通常是
`~/.codex/memories_extensions/chronicle`）。

#### 哪些数据会与 OpenAI 共享？

Chronicle 在本地捕获屏幕上下文，然后周期性使用 Codex 将
最近活动汇总成记忆。为生成这些记忆，Chronicle
会启动一个临时 Codex 会话，并使其可以访问此屏幕上下文。该
会话可能会处理选定的截图帧、从
截图中提取的 OCR 文本、时间信息，以及相关时间
窗口的本地文件路径。

用于生成记忆的屏幕截图会临时存储在你的设备上。它们会在我们的
服务器上处理以生成记忆，随后记忆会存储在本地设备上。除非法律要求，
我们不会在处理后将截图存储在我们的服务器上，
也不会将它们用于训练。

生成的记忆是 Markdown 文件，存储在本地
`$CODEX_HOME/memories_extensions/chronicle/` 下。当 Codex 在
未来会话中使用记忆时，相关记忆内容可能会作为该
会话的上下文包含，并且如果你的 ChatGPT
设置允许，可能用于改进我们的模型。[了解更多](https://help.openai.com/en/articles/7730893-data-controls-faq)。

#### 提示注入风险

使用 Chronicle 会增加来自屏幕内容的提示注入攻击风险。
例如，如果你浏览包含恶意代理指令的网站，Codex 可能
会遵循这些指令。
