### Windows 应用

Source: [Windows](https://developers.openai.com/codex/app/windows.md)

[Codex app for Windows](https://get.microsoft.com/installer/download/9PLM9XGG6VKS?cid=website_cta_psi) 为跨项目工作、运行并行智能体线程和审查结果提供一个统一界面。Windows app 支持核心工作流，例如工作树、自动化、Git 功能、应用内浏览器、工件预览、插件和技能。它使用 PowerShell 和 [Windows 沙盒](https://developers.openai.com/codex/windows#windows-sandbox) 在 Windows 上原生运行，或者你也可以将它配置为在 [Windows Subsystem for Linux 2 (WSL2)](#windows-subsystem-for-linux-wsl) 中运行。

#### 下载和更新 Codex app

从 [Microsoft Store](https://get.microsoft.com/installer/download/9PLM9XGG6VKS?cid=website_cta_psi) 下载 Codex app。

然后按照 [快速入门](https://developers.openai.com/codex/quickstart?setup=app) 开始使用。

要更新 app，请打开 Microsoft Store，前往 **Downloads**，并点击 **Check for updates**。之后 Store 会安装最新版本。

对于企业，管理员可以通过企业管理工具使用 Microsoft Store 应用分发部署该 app。

如果你更喜欢命令行安装路径，或需要不打开 Microsoft Store UI 的替代方式，请运行：

```powershell
winget install Codex -s msstore
```

#### 原生沙盒

当智能体在 PowerShell 中运行时，Windows 上的 Codex app 支持原生 [Windows 沙盒](https://developers.openai.com/codex/windows#windows-sandbox)；当你在 [Windows Subsystem for Linux 2 (WSL2)](#windows-subsystem-for-linux-wsl) 中运行智能体时，则使用 Linux 沙盒。要在任一模式中应用沙盒保护，请在向 Codex 发送消息前，在 Composer 中将沙盒权限设置为 **Default permissions**。

以完全访问模式运行 Codex 意味着 Codex 不受项目目录限制，并可能执行非预期的破坏性操作，从而导致数据丢失。请保留沙盒边界，并使用 [rules](https://developers.openai.com/codex/rules) 进行有针对性的例外设置，或根据你的 [批准和安全设置](https://developers.openai.com/codex/agent-approvals-security)，将 [批准策略设置为 never](https://developers.openai.com/codex/agent-approvals-security#run-without-approval-prompts)，让 Codex 尝试在不请求升级权限的情况下解决问题。

#### 按你的开发设置自定义

#### 首选编辑器

为 **Open** 选择默认应用，例如 Visual Studio、VS Code 或其他编辑器。你可以按项目覆盖该选择。如果你已经从某个项目的 **Open** 菜单选择了不同应用，则该项目特定选择优先。

#### 集成终端

你也可以选择默认集成终端。根据你已安装的内容，选项包括：

- PowerShell
- Command Prompt
- Git Bash
- WSL

此更改仅适用于新的终端会话。如果你已经打开集成终端，请重启 app 或启动新线程，再期待新的默认终端出现。

#### Windows Subsystem for Linux (WSL)

默认情况下，Codex app 使用 Windows 原生智能体。这意味着智能体会在 PowerShell 中运行命令。该 app 仍可通过按需使用 `wsl` CLI 来处理位于 Windows Subsystem for Linux 2 (WSL2) 中的项目。

如果你想从 WSL 文件系统添加项目，请点击 **Add new project** 或按 Ctrl+O，然后在 File Explorer 窗口中输入 `\\wsl$\`。之后选择你的 Linux 发行版和要打开的文件夹。

如果你计划继续使用 Windows 原生智能体，建议将项目存储在 Windows 文件系统上，并通过 `/mnt//...` 从 WSL 访问它们。此设置比直接从 WSL 文件系统打开项目更可靠。

如果你希望智能体本身在 WSL2 中运行，请打开 **[Settings](codex://settings)**，将智能体从 Windows native 切换到 WSL，并 **restart the app**。在重启前，该更改不会生效。重启后，你的项目应保持原位。

Codex `0.114` 支持 WSL1。从 Codex `0.115` 开始，Linux 沙盒移至 `bubblewrap`，因此不再支持 WSL1。

你可以独立于智能体配置集成终端。终端选项请参阅[按你的开发设置自定义](#customize-for-your-dev-setup)。你可以让智能体留在 WSL 中，同时在终端中使用 PowerShell；也可以根据工作流让两者都使用 WSL。

#### 有用的开发工具

当一些常见开发工具已安装时，Codex 效果最佳：

- **Git**：驱动 Codex app 中的复查面板，并让你检查或还原变更。
- **Node.js**：智能体用于更高效执行任务的常见工具。
- **Python**：智能体用于更高效执行任务的常见工具。
- **.NET SDK**：当你想构建原生 Windows 应用时很有用。
- **GitHub CLI**：驱动 Codex app 中 GitHub 特定功能。

使用默认 Windows 包管理器 `winget` 安装它们，方法是将以下内容粘贴到 [集成终端](https://developers.openai.com/codex/app/features#integrated-terminal)，或要求 Codex 安装它们：

```powershell
winget install --id Git.Git
winget install --id OpenJS.NodeJS.LTS
winget install --id Python.Python.3.14
winget install --id Microsoft.DotNet.SDK.10
winget install --id GitHub.cli
```

安装 GitHub CLI 后，运行 `gh auth login` 以在 app 中启用 GitHub 功能。

如果你需要不同的 Python 或 .NET 版本，请将包 ID 更改为所需版本。

#### 故障排查和 FAQ

#### 使用提升权限运行命令

如果你需要 Codex 以提升权限运行命令，请以管理员身份启动 Codex app 本身。安装后，打开 Start menu，找到 Codex，并选择 Run as administrator。Codex 智能体会继承该权限级别。

#### PowerShell 执行策略阻止命令

如果你以前从未在 PowerShell 中使用 Node.js 或 `npm` 等工具，Codex 智能体或集成终端可能会遇到执行策略错误。

如果 Codex 为你创建 PowerShell 脚本，也可能发生这种情况。在这种情况下，你可能需要较不严格的执行策略，PowerShell 才会运行它们。

错误可能类似于：

```text
npm.ps1 cannot be loaded because running scripts is disabled on this system.
```

常见修复方式是将执行策略设置为 `RemoteSigned`：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
```

更改策略前，请查看 Microsoft 的 [执行策略指南](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies)，了解详情和其他选项。

#### Windows 上的本地环境脚本

如果你的 [本地环境](https://developers.openai.com/codex/app/local-environments) 使用跨平台命令，例如 `npm` 脚本，你可以为每个平台保留一个共享设置脚本或一组操作。

如果需要 Windows 特定行为，请创建 Windows 专用设置脚本或 Windows 专用操作。

操作会在集成终端使用的环境中运行。请参阅[按你的开发设置自定义](#customize-for-your-dev-setup)。

本地设置脚本会在智能体环境中运行：如果智能体使用 WSL，则在 WSL 中；否则在 PowerShell 中。

#### 与 WSL 共享配置、认证和会话

Windows app 使用与 Windows 上原生 Codex 相同的 Codex 主目录：`%USERPROFILE%\.codex`。

如果你也在 WSL 内运行 Codex CLI，CLI 默认使用 Linux 主目录，因此不会自动与 Windows app 共享配置、缓存认证或会话历史。

要共享它们，请使用以下方法之一：

- 将 WSL `~/.codex` 与文件系统上的 `%USERPROFILE%\.codex` 同步。
- 通过设置 `CODEX_HOME` 将 WSL 指向 Windows Codex 主目录：

```bash
export CODEX_HOME=/mnt/c/Users//.codex
```

如果你希望每个 shell 都有该设置，请将它添加到你的 WSL shell 配置文件，例如 `~/.bashrc` 或 `~/.zshrc`。

#### Git 功能不可用

如果你没有在 Windows 上原生安装 Git，app 无法使用某些功能。请从 PowerShell 或 `cmd.exe` 使用 `winget install Git.Git` 安装。

#### 从 `\\wsl$` 打开的项目检测不到 Git

目前，如果你想让 Windows 原生智能体使用一个也可从 WSL 访问的项目，最可靠的解决办法是将项目存储在原生 Windows 驱动器上，并通过 `/mnt//...` 在 WSL 中访问。

#### `Cmder` 未列在打开对话框中

如果已安装 `Cmder` 但它没有显示在 Codex 的打开对话框中，请将它添加到 Windows Start Menu：右键点击 `Cmder` 并选择 **Add to Start**，然后重启 Codex 或重新启动计算机。
