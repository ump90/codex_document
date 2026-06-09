### 远程连接

Source: [Remote connections](https://developers.openai.com/codex/remote-connections.md)

import {
Desktop,
Storage,
Terminal,
} from "@components/react/oai/platform/ui/Icon.react";

远程连接让你可以从另一台设备或另一台机器使用 Codex。你可以在 ChatGPT mobile app 中使用 Codex，在已连接的 Mac 或 Windows 设备上工作；也可以从另一台受支持的 Codex App 设备继续工作；还可以将 Codex App 连接到 SSH host 上的项目。

远程访问会使用已连接 host 的项目、线程、文件、凭据、权限、plugins、Computer Use、浏览器设置和本地工具。

#### 你可以远程做什么

- 在 host 上的项目中启动新线程，或继续现有线程。
- 发送后续说明、回答问题并引导正在进行的工作。
- 批准命令和其他操作。
- 审查输出、diff、测试结果、终端输出和截图。
- 在 Codex 完成任务或需要你关注时收到通知。
- 在已连接 hosts 和线程之间切换。

后续章节介绍如何在 ChatGPT mobile app 中使用 Codex 控制 Codex App host。要将 Codex 连接到 SSH host 上的项目，请参阅 [连接到 SSH host](#connect-to-an-ssh-host)。

#### 设置移动访问之前

Codex 移动设置支持 macOS 和 Windows 上的 Codex App hosts。你可以从 iOS 或 Android 上的 ChatGPT 控制 Windows host，也可以从运行 Codex 的 Mac 控制 Windows host。Windows 目前无法从 Codex App 控制另一台计算机。

请确认你具备：

- 你想使用的 ChatGPT 账号和工作区中的 Codex 访问权限。
- iOS 或 Android 设备上最新的 ChatGPT mobile app。如果你在 ChatGPT mobile app 中看不到 Codex，请先更新 ChatGPT。
- 最新的 macOS 或 Windows Codex App，运行在一台保持唤醒、在线，并已登录同一账号和工作区的 host 上。移动设置从 Codex App 开始；无法从 Codex CLI 或 IDE Extension 设置。
- 该账号或工作区所需的任何多因素身份验证、SSO 或 passkey 配置。

如果你通过 ChatGPT workspace 使用 Codex，管理员可能需要先启用 Remote Control access，你才能从手机连接。

#### 设置移动访问

从你想连接的 host 上的 Codex App 开始。设置流程会为该 host 启用远程访问，然后显示一个可用手机扫描的二维码。

1. 启动 Codex 移动设置。

   在 host 上打开 Codex，并在侧边栏中选择 **Set up Codex mobile**。

2. 扫描二维码。

   使用手机扫描 Codex 显示的二维码。该二维码会打开 ChatGPT，以便你完成 mobile app 到 host 的连接。

3. 在 ChatGPT 中完成设置。

   ChatGPT 会打开 Codex 移动设置流程。确认使用相同的 ChatGPT 账号和工作区，然后完成任何必需的多因素身份验证、SSO 或 passkey 步骤。设置成功后，该 host 会出现在你手机上的 Codex 中。

4. 审查 host 设置。

   在 host 上的 Codex 中，使用 **Settings > Connections** 管理已连接设备。你也可以选择是否保持计算机唤醒、启用 Computer Use，或安装 Chrome extension。

#### 选择要连接的内容

从你已经使用 Codex 的笔记本或台式机开始。当你需要持续访问或不同环境时，再添加常开计算机或 SSH host。

#### 你的笔记本或台式机

连接你日常运行 Codex 的 Mac 或 Windows PC。这样可远程访问你已经使用的相同项目、线程、凭据、plugins 和本地设置。

如果该计算机休眠、失去网络访问或关闭 Codex，远程访问会停止，直到它再次可用。如果你将这台计算机用作 host device，请保持接入电源，并在可用时使用 host 的连接设置让它保持唤醒。

在 Mac 笔记本上，保持屏幕打开并接入电源时，远程访问可以保持可用。合上屏幕时，还需要连接外接显示器。选择 **Sleep** 仍会停止远程访问。

在 Windows host 上，对于使用 [Computer Use](https://developers.openai.com/codex/app/computer-use) 的任务，请保持会话解锁且可用。Windows 上的 Computer Use 在前台运行，因此远程控制最适合在你将 host desktop 专用于任务时启动或检查工作。

#### 专用常开计算机

当你希望 Codex 可用于较长时间运行的工作时，请使用专用的常开 Mac 或 Windows PC。

在该机器上安装 Codex 应使用的项目、凭据、plugins、MCP servers 和工具。

#### 远程开发环境

当项目已经位于远程环境中时，使用 SSH host 或托管远程开发环境。先将 Codex App host 连接到该环境；你的手机仍连接到 Codex App host，而 Codex 会在远程环境中使用其依赖项、安全策略和计算资源工作。

有关 SSH 设置详情，请参阅 [连接到 SSH host](#connect-to-an-ssh-host)。

对于常开计算机或 remote host 上的浏览器或桌面任务，请在该 host 上启用 Computer Use 并安装 Chrome extension。

#### 已连接主机提供什么

你的手机会向 Codex 发送提示、审批和后续消息。已连接 host 提供 Codex 使用的环境。

这意味着：

- 仓库文件和本地文档来自已连接 host。
- Shell commands 在该 host 或远程环境上运行。
- 当你远程使用 Codex 时，该 host 上安装的任何 plugin 都可用。
- MCP servers、skills、浏览器访问和 Computer Use 来自该 host 的配置。
- 已登录的网站和桌面 app 只有在 host 可以访问时才可用。
- 沙箱设置、安全控制和操作审批仍适用于已连接会话。

Codex 使用安全中继层，让受信任机器可在你已授权的 ChatGPT devices 间访问，而不会将它们直接暴露到公网。

#### 从另一台设备继续工作

你可以从另一台支持远程控制的已登录 Codex App 设备继续工作。例如，如果你的笔记本不可用，你可以从手机在常开 host 上启动一个线程，之后再在笔记本上打开 Codex 并继续同一个线程。

在 Mac 上的 Codex 中，使用 **Settings > Connections > Control other devices** 添加另一台 host。一台设备可以允许远程访问，同时也控制另一台设备。你可以从 Mac 或 iOS/Android 上的 ChatGPT 控制 Windows hosts，但不能用 Windows 控制另一台计算机。例如，你可以从 Mac 或手机控制 Windows 设备，但不能使用 Windows 设备控制另一台 Windows 设备。

#### 连接到 SSH 主机

在 Codex App 中，从 SSH host 添加 remote projects，并针对远程 filesystem 和 shell 运行 threads。远程项目线程会在 remote host 上运行 commands、读取 files 并写入 changes。

请让 remote host 采用与常规 SSH 访问相同的安全预期配置：受信任密钥、最小权限账号，并且没有未经身份验证的公开监听器。

1. 将 host 添加到 SSH config，以便 Codex 可以自动发现它。

   ```text
   Host devbox
     HostName devbox.example.com
     User you
     IdentityFile ~/.ssh/id_ed25519
   ```

   Codex 会从 `~/.ssh/config` 读取具体 host aliases，用 OpenSSH 解析它们，并忽略仅包含 pattern 的 hosts。

2. 确认你可以从运行 Codex App 的机器 SSH 到该 host。

   ```bash
   ssh devbox
   ```

3. 在 remote host 上安装 Codex 并完成身份验证。

   该 app 会通过 SSH 启动远程 Codex app server，并使用远程用户的 login shell。请确保 `codex` 命令在 remote host 的该 shell 的 `PATH` 中可用。

4. 在 Codex App 中，打开 **Settings > Connections**，添加或启用 SSH host，然后选择 remote project folder。

#### 身份验证和网络暴露

远程连接使用 SSH 启动和管理远程 Codex app server。不要在共享网络或公共网络上直接暴露 app-server transports。

如果需要访问当前网络之外的远程机器，请使用 VPN 或 mesh networking tool，而不是将 app server 直接暴露到互联网。
