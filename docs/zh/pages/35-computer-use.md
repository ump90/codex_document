### 计算机使用

Source: [Computer Use](https://developers.openai.com/codex/app/computer-use.md)

在 Codex app 中，计算机使用在 macOS 和 Windows 上可用，但发布时不包括欧洲经济区、英国和瑞士。安装 Computer Use 插件。在 macOS 上，根据提示授予 Screen Recording 和 Accessibility 权限。

通过计算机使用，Codex 可以查看并操作 macOS 或 Windows 上的图形用户界面。对于命令行工具或结构化集成不足以完成的任务，可以使用它，例如检查桌面应用、使用浏览器、更改应用设置、处理没有插件可用的数据源，或复现只发生在图形用户界面中的 bug。

由于计算机使用可能影响项目工作区之外的应用和系统状态，请将它用于范围明确的任务，并在继续前审查权限提示。

#### 设置计算机使用

在 Codex 设置中，打开 **Computer Use** 并点击 **Install**，在要求 Codex 操作桌面应用前安装 Computer Use 插件。在 Windows 上，任务运行时请保持目标应用在活动桌面上可见。在 macOS 上，根据提示授予 Screen Recording 和 Accessibility 权限，以便 Codex 可以看到目标应用并与其交互。

在 macOS 上，授予：

- **Screen Recording** 权限，使 Codex 可以看到目标应用。
- **Accessibility** 权限，使 Codex 可以点击、输入和导航。

#### 何时使用计算机使用

当任务依赖图形用户界面，并且很难仅通过文件或命令输出验证时，请选择计算机使用。

适合的场景包括：

- 测试 Codex 正在构建的 macOS 应用、Windows 应用、iOS 模拟器流程或其他桌面应用。
- 执行需要你的 Web 浏览器的任务。
- 复现只出现在图形界面中的 bug。
- 更改需要通过 UI 点击完成的应用设置。
- 检查无法通过插件获得的应用或数据源中的信息。
- 在 macOS 上，在你继续处理其他事情时，在后台运行范围明确的任务。
- 执行跨多个应用的工作流。

对于你在本地构建的 Web 应用，请优先使用 [应用内浏览器](36-in-app-browser.md)。

#### Windows 前台使用

在 Windows 上，计算机使用运行在活动桌面上。它无法在你继续使用同一个 Windows 会话时在后台操作，因此在任务运行时，预计 Codex 会移动指针、输入并接管前台。

对于你离开后仍应继续的 Windows 任务，请保持 Windows 设备解锁并连接互联网。使用手机上的 [远程控制](79-remote-connections.md) 查看进度或发送后续指令，或在 Windows 虚拟机中运行 Codex app，这样计算机使用会接管 VM 而不是你的主桌面。

#### 启动计算机使用任务

在提示中提到 `@Computer` 或 `@AppName`，或要求 Codex 使用计算机使用。描述 Codex 应该操作的确切应用、窗口或流程。

```text
Open the app with computer use, reproduce the onboarding bug, and fix the
smallest code path that causes it. After each change, run the same UI flow
again.
```

```text
Open @Chrome and verify the checkout page still works after the latest changes.
```

如果目标应用提供了专用插件或 MCP server，请优先选择该结构化集成来进行数据访问和可重复操作。当 Codex 需要以视觉方式检查或操作应用时，再选择计算机使用。

#### 权限和批准

计算机使用的系统权限独立于 Codex 中的应用批准。在 macOS 上，Screen Recording 和 Accessibility 权限让 Codex 可以查看并操作应用。应用批准决定你允许 Codex 使用哪些应用。文件读取、文件编辑和 shell 命令仍遵循该线程的沙盒和批准设置。

通过计算机使用，Codex 只能在你允许的应用中查看和采取行动。在任务期间，Codex 在使用你计算机上的应用前会请求你的许可。你可以选择 **Always allow**，让 Codex 将来可以不再询问就使用该应用。你可以在 Codex 设置的 **Computer Use** 部分从 **Always allow** 列表中移除应用。

Codex 也可能在采取敏感或破坏性操作前请求许可。

如果 Codex 无法看到或控制某个应用，请打开 **System Settings > Privacy &
Security**，并在 macOS 上检查 Codex app 的 **Screen Recording** 和 **Accessibility**。在 Windows 上，确保目标应用在活动桌面会话中可见。

#### 锁定后使用

Locked use 适用于 macOS。在 Windows 上，计算机使用在前台工作。

锁定后计算机使用让 Codex 可以在你的 Mac 锁定后使用 Computer Use，但前提是你已启用它。当 Codex 任务需要在 Mac 锁定后从已连接设备使用桌面应用时，可以使用它。

启用锁定后计算机使用后，Codex 会安装一个 Apple [authorization plug-in](https://developer.apple.com/documentation/security/authorization-plug-ins)，参与 macOS 解锁流程。

Locked use 的范围刻意很窄。它不是适用于你的 Mac 的通用远程解锁路径，也不会让其他应用或本地进程解锁计算机。

使用锁定后计算机使用：

1. 打开 **Codex settings > Computer Use**。
2. 启用锁定后计算机使用。
3. 在你的 Mac 屏幕锁定后，从已连接设备启动使用计算机使用的任务。

当 Codex 任务在你的 Mac 锁定后通过 Computer Use 访问应用时，Codex 会临时解锁 Mac，同时阻止本地使用并保留锁屏保护。解锁前，Codex 会检查本次解锁尝试是否属于一个活动且可信的计算机使用轮次。在这个短暂窗口之外，Codex 会拒绝解锁，并在需要时要求你手动解锁。

Locked use 包含安全保护：

- 授权窗口生命周期很短，并限定于当前解锁尝试。
- 自动解锁仅在活动的计算机使用轮次期间对 Codex 可用。
- Codex 会在桌面被临时解锁时覆盖每个显示器。
- 如果 Codex 检测到本地键盘或指针输入，它会重新锁定 Mac，并暂停自动解锁，直到你手动解锁。

#### 安全指南

通过计算机使用，Codex 可以查看屏幕内容、截图，并与目标应用中的窗口、菜单、键盘输入和剪贴板状态交互。请将可见的应用内容、浏览器页面、截图，以及目标应用中打开的文件视为 Codex 在任务运行时可能处理的上下文。

保持任务范围狭窄，并在敏感流程中保持在场：

- 一次只给 Codex 一个明确的目标应用或流程。
- 你可以随时停止任务或接管计算机。
- 除非任务需要，否则关闭敏感应用。
- 在 Windows 上，预计 Codex 工作时会接管前台输入；使用辅助设备、VM，或在自己使用该桌面前停止任务。
- 避免需要密钥的任务，除非你在场并可以批准每一步。
- 在允许 Codex 使用应用前审查应用权限提示。
- 仅对你信任 Codex 在未来任务中自动使用的应用使用 **Always allow**。
- 对于账户、安全、隐私、网络、支付或凭据相关设置，请保持在场。
- 如果 Codex 开始与错误窗口交互，请取消任务。

如果 Codex 使用你的浏览器，它可以与已登录页面交互。请像你自己操作一样审查网站操作：网页可能包含恶意或误导性内容，站点可能会把已批准的点击、表单提交和已登录操作视为来自你的账户。若要在 Codex 工作时继续使用浏览器，请要求 Codex 使用不同的浏览器。

该功能无法自动化终端应用或 Codex 本身，因为自动化它们可能绕过 Codex 安全策略。它也无法以管理员身份认证，或批准你计算机上的安全和隐私权限提示。

文件编辑和 shell 命令在适用时仍遵循 Codex 批准和沙盒设置。通过桌面应用做出的更改，可能在保存到磁盘并被项目跟踪之前不会出现在复查窗格中。你的 ChatGPT 数据控制适用于通过 Codex 处理的内容，包括计算机使用拍摄的截图。
