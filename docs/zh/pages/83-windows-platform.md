### Windows 平台

Source: [Windows](https://developers.openai.com/codex/windows.md)

在 Windows 上使用 Codex，可通过原生 [Codex app](41-windows-app.md)、[CLI](45-codex-cli.md) 或 [IDE extension](46-codex-ide-extension.md)。

Windows 上的 Codex app 支持核心工作流，例如并行 agent 线程、worktrees、automations、Git 功能、in-app browser、artifact previews、plugins 和 skills。

根据使用界面和你的设置，Codex 可以通过三种实际方式在 Windows 上运行：

- 在 Windows 上原生运行，使用更强的 `elevated` sandbox；
- 在 Windows 上原生运行，使用 fallback `unelevated` sandbox；
- 或在 [Windows Subsystem for Linux 2](https://learn.microsoft.com/en-us/windows/wsl/install) (WSL2) 中运行，使用 Linux sandbox 实现。

#### Windows 沙盒

当你在 Windows 上原生运行 Codex 时，agent mode 会使用 Windows sandbox 阻止在工作文件夹外写入文件系统，并在没有你明确批准的情况下阻止网络访问。

原生 Windows sandbox 支持两种可在 `config.toml` 中配置的模式：

```toml
[windows]
sandbox = "elevated" # or "unelevated"
```

`elevated` 是首选的原生 Windows sandbox。它使用专用的低权限 sandbox users、文件系统权限边界、防火墙规则，以及 sandbox 中运行的 commands 所需的本地策略变更。

`unelevated` 是 fallback 原生 Windows sandbox。它使用从当前用户派生的受限 Windows token 运行 commands，应用基于 ACL 的文件系统边界，并使用环境级离线控制，而不是专用离线用户防火墙规则。它弱于 `elevated`，但当管理员批准的设置被本地或企业策略阻止时仍然有用。

如果两种模式都可用，请使用 `elevated`。如果默认原生 sandbox 在你的环境中无法工作，请在排查设置时使用 `unelevated` 作为 fallback。

企业管理员可以通过 [`requirements.toml`](67-managed-configuration.md#admin-enforced-requirements-requirementstoml) 约束 Codex 可以使用哪些原生 sandbox 实现：

```toml
[windows]
allowed_sandbox_implementations = ["elevated"]
```

此示例要求使用 `elevated` sandbox，并阻止用户回退到 `unelevated`。若要允许任一实现，请包含两个值；当未选择模式时，Codex 偏好 `elevated`。有关支持的值，请参阅 [`requirements.toml` 参考](16-configuration-reference.md#requirementstoml)。

默认情况下，两种 sandbox modes 也会使用 private desktop，以提供更强的 UI 隔离。仅当你因兼容性需要旧的 `Winsta0\\Default` 行为时，才设置 `windows.sandbox_private_desktop = false`。

#### 沙盒权限

以 full access mode 运行 Codex 意味着 Codex 不受项目目录限制，并且可能执行会导致数据丢失的意外破坏性操作。为了更安全地自动化，请保留 sandbox boundaries，并为特定例外使用 [rules](54-rules.md)，或将你的 [approval policy 设置为 never](13-agent-approvals-security.md#run-without-approval-prompts)，让 Codex 根据你的 [审批与安全设置](13-agent-approvals-security.md) 尝试在不请求 escalated permissions 的情况下解决问题。

#### Windows 版本矩阵

| Windows 版本                     | 支持级别        | 说明                                                                                                                                                                                  |
| -------------------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Windows 11                       | 推荐            | Codex 在 Windows 上的最佳基线。如果你正在标准化企业部署，请使用它。                                                                                       |
| 最近且完整更新的 Windows 10      | 尽力支持        | 可以工作，但可靠性低于 Windows 11。对于 Windows 10，Codex 依赖现代控制台支持，包括 ConPTY。实际需要 Windows 10 version 1809 或更新版本。 |
| 较旧的 Windows 10 构建           | 不推荐          | 更可能缺少 ConPTY 等必需控制台组件，也更可能在企业设置中失败。                                                                          |

其他环境假设：

- `winget` 应可用。如果缺失，请在设置 Codex 前更新 Windows 或安装 Windows Package Manager。
- 推荐的原生 sandbox 依赖管理员批准的设置。
- 即使 OS version 本身可接受，某些企业托管设备也会阻止必需的设置步骤。

#### 授予沙盒读取访问

当命令因 Windows sandbox 无法读取目录而失败时，使用：

```text
/sandbox-add-read-dir C:\absolute\directory\path
```

路径必须是已存在的绝对目录。命令成功后，之后在 sandbox 中运行的 commands 可以在当前会话中读取该目录。

默认使用原生 Windows sandbox。原生 Windows sandbox 在保持相同安全性的同时提供最佳性能和最高速度。当你需要 Windows 上的 Linux-native environment、工作流已经位于 WSL2 中，或两个原生 Windows sandbox modes 都无法满足需要时，选择 WSL2。

#### Windows Subsystem for Linux

如果选择 WSL2，Codex 会在 Linux 环境内运行，而不是使用原生 Windows sandbox。当你需要 Windows 上的 Linux-native tooling、repositories 和 developer workflow 已经位于 WSL2 中，或两个原生 Windows sandbox modes 都不适用于你的环境时，这很有用。

WSL1 支持到 Codex `0.114`。从 Codex `0.115` 开始，Linux sandbox 迁移到 `bubblewrap`，因此不再支持 WSL1。

#### 从 WSL 内启动 VS Code

有关逐步说明，请参阅 [官方 VS Code WSL 教程](https://code.visualstudio.com/docs/remote/wsl-tutorial)。

#### 前置条件

- 已安装 WSL 的 Windows。要安装 WSL，请以 administrator 身份打开 PowerShell，然后运行 `wsl --install`（Ubuntu 是常见选择）。
- 已安装 [WSL extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) 的 VS Code。

#### 从 WSL 终端打开 VS Code

```bash
# From your WSL shell
cd ~/code/your-project
code .
```

这会打开一个 WSL remote window，在需要时安装 VS Code Server，并确保 integrated terminals 在 Linux 中运行。

#### 确认你已连接到 WSL

- 查找显示 `WSL: ` 的绿色状态栏。
- Integrated terminals 应显示 Linux paths（例如 `/home/...`），而不是 `C:\`。
- 你可以用以下命令验证：

  ```bash
  echo $WSL_DISTRO_NAME
  ```

  这会打印你的发行版名称。

如果状态栏中没有看到 "WSL: ..."，按 `Ctrl+Shift+P`，选择 `WSL: Reopen Folder in WSL`，并将你的 repository 放在 `/home/...` 下（不要放在 `C:\` 下），以获得最佳性能。

如果 Windows app 或 project picker 没有显示你的 WSL repository，请在 file picker 或 Explorer 中输入 \\wsl$，然后导航到你的发行版 home directory。

#### 在 WSL 中使用 Codex CLI

从 elevated PowerShell 或 Windows Terminal 运行这些命令：

```powershell
# Install default Linux distribution (like Ubuntu)
wsl --install

# Start a shell inside Windows Subsystem for Linux
wsl
```

然后从你的 WSL shell 运行这些命令：

```bash
# Install and run Codex in WSL
curl -fsSL https://chatgpt.com/codex/install.sh | sh
codex
```

#### 在 WSL 内处理代码

- 在 /mnt/c/... 这样的 Windows-mounted paths 中工作，可能比在 Windows-native paths 中工作更慢。请将 repositories 放在你的 Linux home directory 下（例如 ~/code/my-app），以获得更快 I/O，并减少 symlink 和 permission 问题：
  ```bash
  mkdir -p ~/code && cd ~/code
  git clone https://github.com/your/repo.git
  cd repo
  ```
- 如果需要从 Windows 访问文件，它们位于 Explorer 中的 \\wsl$\Ubuntu\home\&lt;user&gt; 下。
