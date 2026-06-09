### 沙盒

Source: [Sandbox](https://developers.openai.com/codex/concepts/sandboxing.md)

沙盒是让 Codex 能够自主行动、同时不授予其对你机器无限制访问权限的边界。当 Codex 在 **Codex app**、**IDE extension** 或 **CLI** 中运行本地命令时，这些命令默认会在受约束的环境中运行，而不是以完全访问权限运行。

该环境定义了 Codex 可以自行执行哪些操作，例如可以修改哪些文件，以及命令是否可以使用网络。当任务保持在这些边界内时，Codex 可以继续推进而不必停下来请求确认。当它需要越过边界时，Codex 会回退到审批流程。

沙盒和审批是两种协同工作的不同控制手段。沙盒定义技术边界。审批策略决定 Codex 何时必须停下来询问，才能越过这些边界。

#### 沙盒的作用

沙盒适用于派生出的命令，而不只是 Codex 内置的文件操作。如果 Codex 运行 `git`、包管理器或测试运行器等工具，这些命令会继承相同的沙盒边界。

Codex 会在每个操作系统上使用平台原生的强制执行机制。macOS、Linux、WSL2 和原生 Windows 上的实现有所不同，但跨不同使用界面的思路是一致的：为智能体提供一个有边界的工作空间，使日常任务可以在清晰限制内自主运行。

#### 为什么重要

沙盒可以减少审批疲劳。Codex 不需要要求你确认每一个低风险命令，而是可以在你已经批准的边界内读取文件、进行编辑并运行常规项目命令。

它也为智能体式工作提供了更清晰的信任模型。你信任的不只是智能体的意图；你也信任智能体确实在强制执行的限制内运行。这使你更容易让 Codex 独立工作，同时仍然知道它何时会停下来寻求帮助。

#### 开始使用

当你使用默认权限模式时，Codex 会自动应用沙盒。

#### 前提条件

在 **macOS** 上，沙盒使用内置的 Seatbelt 框架开箱即用。

在 **Windows** 上，当你在 PowerShell 中运行时，Codex 使用原生 [Windows 沙盒](83-windows-platform.md#windows-sandbox)；当你在 WSL2 中运行时，则使用 Linux 沙盒实现。

在 **Linux 和 WSL2** 上，请先使用包管理器安装 `bubblewrap`：

```bash
sudo apt install bubblewrap
```

```bash
sudo dnf install bubblewrap
```

Codex 会使用它在 `PATH` 上找到的第一个 `bwrap` 可执行文件。如果没有可用的 `bwrap` 可执行文件，Codex 会回退到捆绑的辅助程序，但该辅助程序需要支持创建非特权用户命名空间。安装发行版提供 `bwrap` 的软件包可以让此设置更可靠。

当缺少 `bwrap`，或辅助程序无法创建所需用户命名空间时，Codex 会显示启动警告。在限制此 AppArmor 设置的发行版上，建议加载 `bwrap` AppArmor 配置文件，使 `bwrap` 能够继续工作，而无需全局禁用该限制。

**Ubuntu AppArmor 说明：** 在 Ubuntu 25.04 上，从 Ubuntu 软件包仓库安装 `bubblewrap` 后，通常无需额外 AppArmor 设置即可工作。`bwrap-userns-restrict` 配置文件随 `apparmor` 软件包提供，路径为 `/etc/apparmor.d/bwrap-userns-restrict`。

在 Ubuntu 24.04 上，即使已安装 `bubblewrap`，Codex 仍可能警告无法创建所需用户命名空间。请复制并加载额外配置文件：

```bash
sudo apt update
sudo apt install apparmor-profiles apparmor-utils
sudo install -m 0644 \
  /usr/share/apparmor/extra-profiles/bwrap-userns-restrict \
  /etc/apparmor.d/bwrap-userns-restrict
sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict
```

`apparmor_parser -r` 会在无需重启的情况下将配置文件加载到内核中。你也可以重新加载所有 AppArmor 配置文件：

```bash
sudo systemctl reload apparmor.service
```

如果该配置文件不可用或无法解决问题，你可以使用以下命令禁用 AppArmor 对非特权用户命名空间的限制：

```bash
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
```

#### 如何控制它

大多数人从产品中的权限控制开始。

在 Codex app 和 IDE 中，你可以从编辑器或聊天输入框下方的权限选择器中选择一种模式。该选择器允许你依赖 Codex 的默认权限、切换到完全访问权限，或使用你的自定义配置。

在 CLI 中，使用 [`/permissions`](39-slash-commands-in-codex-cli.md#update-permissions-with-permissions) 在会话期间切换模式。

#### 配置默认值

如果你希望 Codex 每次启动时都采用相同行为，请使用自定义配置。Codex 会将这些默认值存储在本地设置文件 `config.toml` 中。[配置基础](19-config-basics.md) 解释其工作方式，[配置参考](16-configuration-reference.md) 记录了 `sandbox_mode`、`approval_policy`、`approvals_reviewer` 和 `sandbox_workspace_write.writable_roots` 的确切键。使用这些设置决定 Codex 默认获得多少自主权、可以写入哪些目录、何时应暂停请求审批，以及由谁审核符合条件的审批请求。

概括来说，常见的沙盒模式包括：

- `read-only`：Codex 可以检查文件，但未经审批不能编辑文件或运行命令。
- `workspace-write`：Codex 可以读取文件、在工作区内编辑，并在该边界内运行常规本地命令。这是本地工作的默认低摩擦模式。
- `danger-full-access`：Codex 在没有沙盒限制的情况下运行。这会移除文件系统和网络边界，应仅在你希望 Codex 以完全访问权限行动时使用。

常见的审批策略包括：

- `untrusted`：Codex 会在运行不属于其可信集合的命令前询问。
- `on-request`：Codex 默认在沙盒内工作，并在需要越过该边界时询问。
- `never`：Codex 不会因审批提示而停止。

当审批是交互式的，你还可以使用 `approvals_reviewer` 选择由谁审核：

- `user`：审批提示显示给用户。这是默认值。
- `auto_review`：符合条件的审批提示会发送给审核智能体（参见 [自动审核](65-auto-review.md)）。

完全访问权限意味着将 `sandbox_mode = "danger-full-access"` 与 `approval_policy = "never"` 搭配使用。相比之下，风险较低的本地自动化预设是将 `sandbox_mode = "workspace-write"` 与 `approval_policy = "on-request"` 搭配使用，或使用对应的 CLI 标志 `--sandbox workspace-write --ask-for-approval on-request`。然后，你可以保留 `approvals_reviewer = "user"` 以进行人工审批，或设置 `approvals_reviewer = "auto_review"` 以进行自动审批审核。

如果你需要 Codex 跨多个目录工作，可写根目录让你可以扩展它能够修改的位置，而无需完全移除沙盒。如果你需要更宽或更窄的信任边界，请调整默认沙盒模式和审批策略，而不是依赖一次性例外。

当某个工作流需要特定例外时，请使用 [规则](54-rules.md)。规则允许你在沙盒之外允许、提示或禁止命令前缀，这通常比大范围扩大访问权限更合适。有关应用中审批和沙盒行为的高层概览，请参阅 [Codex app 功能](27-codex-app-features.md#approvals-and-sandboxing)；有关 IDE 专属设置入口，请参阅 [Codex IDE 扩展设置](33-codex-ide-extension-settings.md)。

自动审核在可用时不会改变沙盒边界。它是在该边界上处理审批请求的一种 `approvals_reviewer`，例如沙盒提权、被阻止的网络访问，或仍需审批的有副作用工具调用。已经允许在沙盒内执行的操作会直接运行，无需额外审核。有关审核器生命周期、触发类型、拒绝语义和配置细节，请参阅 [自动审核](65-auto-review.md)。

平台细节位于特定平台文档中。有关原生 Windows 设置、行为和故障排除，请参阅 [Windows](83-windows-platform.md)。有关沙盒和审批的管理员要求及组织级约束，请参阅 [智能体审批与安全](13-agent-approvals-security.md)。
