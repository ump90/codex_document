### Codex Chrome 扩展

Source: [Codex Chrome extension](https://developers.openai.com/codex/app/chrome-extension.md)

Codex Chrome 扩展让 Codex 可以使用 Chrome 来完成需要你已登录浏览器状态的浏览器任务。当 Codex 需要读取或操作 LinkedIn、Salesforce、Gmail 或内部工具等网站时，可以使用它。

对于本地开发服务器、基于文件的预览，以及不需要登录的公开页面，请优先使用 [应用内浏览器](36-in-app-browser.md)。应用内浏览器会把预览和验证工作保留在 Codex 内部，而不会使用你的 Chrome 个人资料。

Codex 也可以根据任务需要在工具之间切换：有专用集成时使用插件，需要已登录浏览器上下文时使用 Chrome，处理 localhost 时使用应用内浏览器。

#### 从插件设置 Chrome

从 Codex 设置扩展：

1. 打开 Codex，前往 **Plugins**。
2. 添加 **Chrome** 插件。
3. 按照设置流程操作。它会引导你安装 [Codex Chrome
   扩展](https://chromewebstore.google.com/detail/codex/hehggadaopoacecdllhhajmbjkdcmajg)
   并批准 Chrome 的权限提示。
4. 打开 Chrome，确认 Codex 扩展显示 **Connected**。

插件设置完成后，启动一个新的 Codex 线程。当任务需要已登录的网站时，Codex 可以建议使用 Chrome。你也可以在提示中直接调用它：

```text
@Chrome open Salesforce and update the account from these call notes.
```

如果 Chrome 尚未打开，Codex 可以打开它。Chrome 浏览器任务会在 Chrome 标签页组中运行，因此一个线程的工作会保持在同一组中。

#### 控制网站访问

默认情况下，Codex 在与每个新网站交互前都会询问。Codex 会基于网站主机发起提示，例如 `example.com`。

当 Codex 请求使用某个网站时，你可以选择与任务和风险承受能力匹配的选项：

- 允许当前聊天使用该网站。
- 始终允许该主机，这样 Codex 之后可以不再询问就使用该网站。
- 拒绝该网站。

#### 管理允许列表和阻止列表

在 Computer Use 设置中，你可以管理域名的允许列表和阻止列表。允许列表包含 Codex 可以不再询问就使用的域名。阻止列表包含 Codex 不应使用的域名。

从允许列表移除域名意味着 Codex 使用前会再次询问。从阻止列表移除域名意味着 Codex 可以再次询问，而不是把该域名视为已阻止。

#### 始终允许浏览器内容

如果你开启“始终允许浏览器内容”，Codex 在使用网站前不再请求确认。

#### 浏览器历史记录

浏览器历史记录可能包含敏感遥测、内部 URL、搜索词，以及已登录设备上 Chrome 会话的活动。如果你允许 Codex 访问浏览器历史记录，相关历史记录条目可能会成为 Codex 用于任务的上下文的一部分。恶意或误导性页面内容可能增加 Codex 将这些数据复制到非预期位置的风险。

Codex 想要使用浏览器历史记录时会询问。Codex 会将历史记录访问限定在该请求内，并且历史记录没有“始终允许”选项。

#### 数据和安全

#### Chrome 扩展权限

安装扩展时，Chrome 会要求你接受扩展权限。权限提示可能包括：

- 访问页面调试器
- 读取和更改所有网站上的所有数据
- 读取和更改你所有已登录设备上的浏览历史记录
- 显示通知
- 读取和更改你的书签
- 管理你的下载
- 与配套的原生应用通信
- 查看和管理你的标签页组

这些 Chrome 权限使扩展具备操作浏览器工作流的能力。Codex 在任务期间使用网站或浏览器历史记录前，仍会使用自己的确认、设置、允许列表和阻止列表。

#### 记忆

浏览器使用会遵循你的 Codex Memories 设置。如果 Memories 开启，Codex 在 Chrome 中工作时可以使用相关的已保存记忆。如果 Memories 关闭，浏览器使用不会使用记忆。

#### OpenAI 会存储哪些浏览内容

OpenAI 不会存储一份来自扩展的完整 Chrome 操作独立记录。OpenAI 只会在浏览器活动成为 Codex 上下文的一部分时存储它，例如 Codex 从页面读取的文本、截图、工具调用、摘要、消息，或线程中包含的其他内容。

你的 ChatGPT 和 Codex 数据控制适用于在上下文中处理的内容。除非任务确实需要，并且你在场审查每个提示，否则请避免通过浏览器任务发送密钥或高度敏感的数据。

#### 故障排查

如果 Codex 无法连接 Chrome，请先确认 Codex 正尝试访问的网站没有位于 Settings 的阻止列表中。如果网站未被阻止，请完成以下检查：

1. 从 Chrome 工具栏或 Chrome 扩展菜单打开 Codex 扩展。确保它显示 **Connected**。如果它显示已断开连接或提到缺少 native host，请在 Codex 的 **Plugins** 中移除并重新添加 Chrome 插件，然后再次按照设置流程操作。
2. 在 Codex 中打开 **Plugins**，确认 Chrome 插件已开启。如果插件关闭，请开启后重试任务。
3. 确保你正在使用安装了 Codex 扩展的同一个 Chrome 个人资料。如果你使用多个 Chrome 个人资料，请在当前活动的个人资料中安装并启用该扩展。
4. 启动一个新的 Codex 线程，然后再次尝试 Chrome 任务。这可以清除线程特定的连接状态。
5. 重启 Chrome 和 Codex，然后重试。如果扩展仍无法连接，请卸载 Codex Chrome 扩展，在 **Plugins** 中移除并重新添加 Chrome 插件，然后再次按照设置流程操作。
6. 如果扩展显示 **Connected** 但 Codex 仍无法使用 Chrome，请在 Codex app 中运行 `/feedback`，并在联系支持时包含线程 ID。

#### 上传文件

如果 Chrome 任务需要从你的计算机上传文件，请允许 Codex 扩展在 Chrome 中访问文件 URL：

1. 在 Chrome 中，打开工具栏里的扩展图标，然后点击 **Manage
   Extensions**。
2. 在 Codex 扩展卡片上，点击 **Details**。
3. 开启 **Allow access to file URLs**。

更改设置后，重新启动 Chrome 任务。
