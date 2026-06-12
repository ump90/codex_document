### 智能体审批和安全

Source: [Agent approvals & security](https://developers.openai.com/codex/agent-approvals-security.md)

Codex 帮助保护你的代码和数据，并降低滥用风险。

本页介绍如何安全地操作 Codex，包括沙箱、审批
和网络访问。如果你正在寻找 Codex Security，即用于
扫描已连接 GitHub 仓库的产品，请参见 [Codex Security](71-codex-security.md)。

默认情况下，代理运行时会关闭网络访问。在本地，Codex 使用由操作系统强制执行的沙箱，限制它可以接触的内容（通常限于当前工作区），并配合审批策略来控制它在执行操作前何时必须停下来询问你。

关于沙箱如何在 Codex app、IDE
扩展和 CLI 中工作的高层解释，请参见 [沙箱](15-sandbox.md)。
如需更广泛的企业安全概览，请参见 [Codex 安全白皮书](https://trust.openai.com/?itemUid=382f924d-54f3-43a8-a9df-c39e6c959958&source=click)。

#### 沙箱和审批

Codex 安全控制来自两个协同工作的层：

- **沙箱模式**：当 Codex 执行模型生成的命令时，它在技术上能做什么（例如可以在哪里写入，以及是否可以访问网络）。
- **审批策略**：Codex 在执行某个动作前何时必须询问你（例如离开沙箱、使用网络，或在可信集合之外运行命令）。

Codex 会根据你运行它的位置使用不同的沙箱模式：

- **Codex cloud**：在 OpenAI 管理的隔离容器中运行，防止访问你的主机系统或无关数据。使用两阶段运行时模型：setup 在代理阶段之前运行，并可访问网络以安装指定依赖；随后代理阶段默认离线运行，除非你为该环境启用互联网访问。为云端环境配置的 secrets 只在 setup 期间可用，并会在代理阶段开始前移除。
- **Codex CLI / IDE 扩展**：由操作系统级机制强制执行沙箱策略。默认设置包括无网络访问，以及写权限仅限于活动工作区。你可以基于自己的风险承受度配置沙箱、审批策略和网络设置。

在 `Auto` 预设中（例如 `--sandbox workspace-write --ask-for-approval on-request`），Codex 可以自动读取文件、进行编辑，并在工作目录中运行命令。

Codex 会在编辑工作区外文件或运行需要网络访问的命令时请求审批。如果你想聊天或规划而不做变更，请使用 `/permissions` 命令切换到 `read-only` 模式。

Codex 也可以对声明有副作用的 app（connector）工具调用触发审批，即使该动作不是 shell 命令或文件变更。破坏性 app/MCP 工具调用在工具声明破坏性标注时始终需要审批，即使它同时声明了其它提示（例如只读提示）。

#### 网络访问

对于 Codex cloud，请参阅 [agent internet access](23-agent-internet-access.md)，以启用完整互联网访问或域名 allow list。

对于 Codex app、CLI 或 IDE 扩展，默认的 `workspace-write` 沙箱模式会保持网络访问关闭，除非你在配置中启用：

```toml
[sandbox_workspace_write]
network_access = true
```

#### 网络隔离

网络访问通过目的地规则控制，这些规则适用于由命令生成的脚本、
程序和子进程。当命令网络访问已经启用时，开启 `network_proxy` 功能可以将该流量限制到你配置的网络策略中。

```toml
[features.network_proxy]
enabled = true
domains = { "api.openai.com" = "allow", "example.com" = "deny" }
```

对于一次性 CLI 会话，如果只需要切换开关，请使用布尔简写；
如果还要设置策略选项，请使用表格形式：

```bash
codex \
  -c 'features.network_proxy=true' \
  -c 'sandbox_workspace_write.network_access=true'

codex \
  -c 'features.network_proxy.enabled=true' \
  -c 'features.network_proxy.domains={ "api.openai.com" = "allow", "example.com" = "deny" }' \
  -c 'sandbox_workspace_write.network_access=true'
```

该功能会改变已启用网络访问的执行方式；它本身不会授予
网络访问。使用带 `workspace-write` 配置的
`sandbox_workspace_write.network_access` 来决定命令是否完全拥有网络访问：

- 网络关闭 + `network_proxy` 开启：网络保持关闭，该功能不起作用。
- 网络开启 + `network_proxy` 关闭：网络保持开启，并拥有不受限制的直接
  出站访问。
- 网络开启 + `network_proxy` 开启：网络保持开启，出站流量会被
  配置的网络策略约束。

管理员管理的 `experimental_network` requirements 独立于用户
功能开关。它们可以配置并启动沙箱网络，而无需
`features.network_proxy`，但当活动
沙箱保持网络关闭时，它们不会开启网络访问。参见 [托管配置](67-managed-configuration.md#configure-network-access-requirements)
了解管理员侧 `requirements.toml` 的形状。

#### 网络策略

域名规则以允许列表优先：

- 精确主机只匹配自身。
- `*.example.com` 匹配 `api.example.com` 等子域，但不匹配
  `example.com`。
- `**.example.com` 同时匹配根域和子域。
- 全局 `*` allow 规则匹配任何未被 deny 的公共主机。请将 `*`
  视为广泛网络访问，并在可行时优先使用范围明确的规则。
- `deny` 始终优先于 `allow`，且全局 `*` 只对 allow 规则有效。

#### 本地和私有目的地

默认情况下，`allow_local_binding = false` 会阻止 loopback、link-local 和
私有目的地：

- 特定例外：当命令需要某个本地目标时，添加精确的本地 IP 字面量或 `localhost` allow 规则。
- 更广泛访问：仅当你有意希望获得更宽泛的本地/私有访问时，才设置 `allow_local_binding = true`。
- 通配符：通配符规则不算作明确的本地例外。
- 解析地址：解析到本地/私有 IP 的主机名即使匹配允许列表，仍会被阻止。

#### DNS 重绑定保护

在允许某个主机名之前，Codex 会执行尽力而为的 DNS 和 IP
分类检查：

- 查询失败或超时会被阻止。
- 解析到非公共地址的主机名会被阻止。
- 该检查降低 DNS 重绑定风险，但不能消除它。要完全防止
  重绑定，需要在传输层固定已解析 IP。

如果恶意 DNS 在威胁范围内，也应在更低层执行出站控制。

#### 危险设置

两个设置会有意扩大信任边界：

- `dangerously_allow_non_loopback_proxy = true` 可能会将代理监听器暴露到
  loopback 之外。
- `dangerously_allow_all_unix_sockets = true` 会绕过 Unix socket allowlist。

仅在严格受控的环境中使用它们。启用 Unix socket 代理时，
即使请求了非 loopback 绑定，监听器也会保持仅限 loopback，
因此沙箱网络不会变成通往本地守护进程的远程桥接。

`network_proxy` 默认关闭。启用它时：

| 设置                                   | 默认值  | 行为                                                                                                                                                        |
| -------------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `enabled`                              | `false` | 仅当命令网络访问已经开启时，才启动沙箱网络。                                                                                                                |
| `domains`                              | unset   | 使用允许列表行为，因此在你添加 `allow` 规则前，不允许任何外部目的地。支持精确主机、限定范围的通配符和全局 `*` allow 规则；`deny` 始终优先。                |
| `unix_sockets`                         | unset   | 在你添加显式 `allow` 规则前，不允许任何 Unix socket 目的地。                                                                                                |
| `allow_local_binding`                  | `false` | 阻止本地和私有网络目的地，除非你添加精确的本地 IP 字面量或 `localhost` allow 规则，或显式选择更广泛的本地/私有访问。                                      |
| `enable_socks5`                        | `true`  | 在策略允许时暴露 SOCKS5 支持。                                                                                                                             |
| `enable_socks5_udp`                    | `true`  | 当 SOCKS5 可用时允许通过 SOCKS5 使用 UDP。                                                                                                                  |
| `allow_upstream_proxy`                 | `true`  | 让沙箱网络遵循环境中的上游代理。                                                                                                                            |
| `dangerously_allow_non_loopback_proxy` | `false` | 保持监听端点位于 loopback，除非你有意将其暴露到 localhost 之外。                                                                                           |
| `dangerously_allow_all_unix_sockets`   | `false` | 保持 Unix socket 访问基于允许列表，除非你有意绕过该保护。                                                                                                  |

你也可以控制 [网页搜索工具](https://platform.openai.com/docs/guides/tools-web-search)，而无需授予派生命令完整网络访问。Codex 默认使用网页搜索缓存访问结果。该缓存是 OpenAI 维护的网页结果索引，因此缓存模式返回预索引结果，而不是获取实时页面。这减少了来自任意实时内容的提示注入暴露，但你仍应将网页结果视为不可信。如果你正在使用 `--yolo` 或其它 [完全访问沙箱设置](#common-sandbox-and-approval-combinations)，网页搜索默认使用实时结果。使用 `--search` 或设置 `web_search = "live"` 允许实时浏览，或将其设为 `"disabled"` 来关闭该工具：

```toml
web_search = "cached"  # default
# web_search = "disabled"
# web_search = "live"  # same as --search
```

在 Codex 中启用网络访问或网页搜索时请谨慎。提示注入可能导致代理获取并遵循不受信任的指令。

#### 默认值和建议

- 启动时，Codex 会检测文件夹是否处于版本控制下，并建议：
  - 受版本控制的文件夹：`Auto`（工作区写入 + 按需审批）
  - 不受版本控制的文件夹：`read-only`
- 根据你的设置，Codex 也可能以 `read-only` 启动，直到你明确信任工作目录（例如通过入门提示或 `/permissions`）。
- 工作区包括当前目录和 `/tmp` 等临时目录。使用 `/status` 命令查看哪些目录位于工作区中。
- 要接受默认值，请运行 `codex`。
- 你可以显式设置这些项：
  - `codex --sandbox workspace-write --ask-for-approval on-request`
  - `codex --sandbox read-only --ask-for-approval on-request`

#### 可写根目录中的受保护路径

在默认 `workspace-write` 沙箱策略中，可写根目录仍包含受保护路径：

- 无论 `<writable_root>/.git` 是目录还是文件，都会被保护为只读。
- 如果 `<writable_root>/.git` 是指针文件（`gitdir: ...`），解析后的 Git 目录路径也会被保护为只读。
- 当 `<writable_root>/.agents` 作为目录存在时，会被保护为只读。
- 当 `<writable_root>/.codex` 作为目录存在时，会被保护为只读。
- 保护是递归的，因此这些路径下的所有内容都是只读。

#### 不显示审批提示运行

你可以使用 `--ask-for-approval never` 或 `-a never`（简写）禁用审批提示。

该选项适用于所有 `--sandbox` 模式，因此你仍然可以控制 Codex 的自主级别。Codex 会在你设置的约束内尽力而为。

如果你需要 Codex 在没有审批提示的情况下读取文件、进行编辑，并运行带网络访问的命令，请使用 `--sandbox danger-full-access`（或 `--dangerously-bypass-approvals-and-sandbox` 标志）。这样做前请谨慎。

作为折中，`approval_policy = { granular = { ... } }` 允许你保持特定审批提示类别为交互式，同时自动拒绝其它类别。细粒度策略覆盖沙箱审批、execpolicy-rule 提示、MCP 提示、`request_permissions` 提示和 skill-script 审批。

#### 自动审批审查

默认情况下，审批请求会路由给你：

```toml
approvals_reviewer = "user"
```

自动审批审查会在审批为交互式时适用，例如
`approval_policy = "on-request"` 或细粒度审批策略。设置
`approvals_reviewer = "auto_review"` 可在 Codex 运行请求前，将符合条件的审批请求
路由给审查代理：

```toml
approval_policy = "on-request"
approvals_reviewer = "auto_review"
```

完整审查器生命周期、触发条件、配置优先级
和失败行为请参见
[Auto-review](65-auto-review.md)。

审查器只评估已经需要审批的动作，例如沙箱
提权、被阻止的网络请求、`request_permissions` 提示，或
有副作用的 app 和 MCP 工具调用。保持在沙箱内的动作
会继续执行，不增加额外审查步骤。

审查器策略会检查数据外泄、凭据探测、持久性
安全削弱和破坏性动作。当策略允许时，低风险和中风险动作
可以继续。策略会拒绝关键风险动作。
高风险动作需要足够的用户授权且没有匹配的 deny 规则。
提示构建、审查会话和解析失败会以关闭方式失败。超时会
单独显示，但动作仍不会运行。

[默认审查器策略](https://github.com/openai/codex/blob/main/codex-rs/core/src/guardian/policy.md)
位于开源 Codex 仓库中。企业可以在托管 requirements 中用 `guardian_policy_config` 替换其
租户特定部分。
本地 `[auto_review].policy` 文本也受支持，但托管 requirements
优先。设置细节请参见
[托管配置](67-managed-configuration.md#configure-automatic-review-policy)。

在 Codex app 中，这些审查会显示为自动审查项，其状态
例如 Reviewing、Approved、Denied、Aborted 或 Timed out。它们还可以
包含风险级别和针对被审查
请求的用户授权评估。

自动审查会使用额外模型调用，因此可能增加 Codex 用量。管理员
可以通过 `allowed_approvals_reviewers` 对其加以约束。

#### 常见沙箱和审批组合

| 目标 | 标志 / 配置 | 效果 |
| --- | --- | --- |
| Auto（预设） | 不需要标志，或 `--sandbox workspace-write --ask-for-approval on-request` | Codex 可以读取文件、进行编辑，并在 workspace 中运行命令。Codex 需要审批才能编辑 workspace 外的文件或访问网络。 |
| 安全只读浏览 | `--sandbox read-only --ask-for-approval on-request` | Codex 可以读取文件并回答问题。Codex 需要审批才能进行编辑、运行命令或访问网络。 |
| 只读非交互式（CI） | `--sandbox read-only --ask-for-approval never` | Codex 只能读取文件；不会请求审批。 |
| 自动编辑，但运行不可信命令前请求审批 | `--sandbox workspace-write --ask-for-approval untrusted` | Codex 可以读取和编辑文件，但会在运行不可信命令前请求审批。 |
| Auto-review 模式 | `--sandbox workspace-write --ask-for-approval on-request -c approvals_reviewer=auto_review` 或 `approvals_reviewer = "auto_review"` | 与标准 on-request 模式使用相同沙箱边界，但符合条件的审批请求由 Auto-review 审查，而不是显示给用户。 |
| 危险完全访问 | `--dangerously-bypass-approvals-and-sandbox`（别名：`--yolo`） | 高风险：无沙箱、无审批（不推荐）。 |

对于非交互式运行，请使用 `codex exec --sandbox workspace-write`；Codex 仍将旧的 `codex exec --full-auto` 调用作为已弃用的兼容路径，并会打印警告。

使用 `--ask-for-approval untrusted` 时，Codex 只会自动运行已知安全的读取操作。可以改变状态或触发外部执行路径的命令（例如破坏性 Git 操作，或 Git 输出 / 配置覆盖标志）需要审批。

##### `config.toml` 中的配置

更完整的配置流程请参阅 [配置基础](19-config-basics.md)、[高级配置](17-advanced-configuration.md#approval-policies-and-sandbox-modes) 和 [配置参考](16-configuration-reference.md)。

```toml
# Always ask for approval mode
approval_policy = "untrusted"
sandbox_mode    = "read-only"
allow_login_shell = false # optional hardening: disallow login shells for shell-based tools

# Optional: Allow network in workspace-write mode
[sandbox_workspace_write]
network_access = true

# Optional: granular approval policy
# approval_policy = { granular = {
#   sandbox_approval = true,
#   rules = true,
#   mcp_elicitations = true,
#   request_permissions = false,
#   skill_approval = false
# } }
```

你也可以将预设保存为 [profile 文件](17-advanced-configuration.md#profiles)，然后用 `codex --profile profile-name` 选择：

```toml
# ~/.codex/full_auto.config.toml
approval_policy = "on-request"
sandbox_mode    = "workspace-write"
```

```toml
# ~/.codex/readonly_quiet.config.toml
approval_policy = "never"
sandbox_mode    = "read-only"
```

##### 本地测试沙箱

要查看命令在 Codex 沙箱下运行时会发生什么，请使用这些 Codex CLI 命令：

```bash
# macOS
codex sandbox macos [--permissions-profile <name>] [--log-denials] [COMMAND]...
# Linux
codex sandbox linux [--permissions-profile <name>] [COMMAND]...
# Windows
codex sandbox windows [--permissions-profile <name>] [COMMAND]...
```

`sandbox` 命令也可作为 `codex debug` 使用，平台 helper 还有别名（例如 `codex sandbox seatbelt` 和 `codex sandbox landlock`）。

#### OS 级沙箱

Codex 会根据你的 OS 以不同方式执行沙箱：

- **macOS** 使用 Seatbelt policy，并通过 `sandbox-exec` 运行命令，使用与你选择的 `--sandbox` 模式对应的 profile（`-p`）。当受限读取访问启用平台默认值时，Codex 会附加精选 macOS 平台 policy（而不是宽泛允许 `/System`），以保持常见工具兼容性。
- **Linux** 默认使用 `bwrap` 加 `seccomp`。
- **Windows** 在 [Windows Subsystem for Linux 2 (WSL2)](83-windows-platform.md#windows-subsystem-for-linux) 中运行时使用 Linux 沙箱实现。WSL1 支持到 Codex `0.114`；从 `0.115` 开始，Linux 沙箱迁移到 `bwrap`，因此不再支持 WSL1。原生 Windows 运行时，Codex 使用 [Windows sandbox](83-windows-platform.md#windows-sandbox) 实现。

如果你在 Windows 上使用 Codex IDE 扩展，它直接支持 WSL2。请在 VS Code 设置中添加以下配置，使 agent 在可用时保持在 WSL2 内：

```json
{
  "chatgpt.runCodexInWindowsSubsystemForLinux": true
}
```

这可确保即使宿主 OS 是 Windows，IDE 扩展中的命令、审批和文件系统访问也继承 Linux 沙箱语义。更多信息见 [Windows 设置指南](83-windows-platform.md)。

原生 Windows 运行时，请在 `config.toml` 中配置原生沙箱模式：

```toml
[windows]
sandbox = "unelevated" # or "elevated"
# sandbox_private_desktop = true  # default; set false only for compatibility
```

详情请参阅 [Windows 设置指南](83-windows-platform.md#windows-sandbox)。

当你在 Docker 等容器化环境中运行 Linux 时，如果 host 或 container 配置阻止 Codex 需要的 namespace、setuid `bwrap` 或 `seccomp` 操作，沙箱可能无法工作。

在这种情况下，请配置 Docker container 来提供你需要的隔离，然后在 container 内使用 `--sandbox danger-full-access`（或 `--dangerously-bypass-approvals-and-sandbox` 标志）运行 `codex`。

##### 在 Dev Containers 中运行 Codex

如果宿主机无法直接运行 Linux 沙箱，或组织已经标准化使用容器化开发，请用 Dev Containers 运行 Codex，并让 Docker 提供外层隔离边界。这适用于 Visual Studio Code Dev Containers 和兼容工具。

可参考 [Codex secure devcontainer example](https://github.com/openai/codex/tree/main/.devcontainer)。该示例会安装 Codex、常见开发工具、`bubblewrap`，以及基于防火墙的出站控制。

Devcontainers 提供了相当强的保护，但不能防止所有攻击。如果你在 container 内使用 `--sandbox danger-full-access` 或 `--dangerously-bypass-approvals-and-sandbox` 运行 Codex，恶意项目可以外泄 devcontainer 内可用的任何内容，包括 Codex 凭据。只有在可信仓库中才使用这种模式，并像任何其他 elevated 环境一样监控 Codex 活动。

参考实现包括：

- Ubuntu 24.04 基础镜像，已安装 Codex 和常见开发工具；
- 基于 allowlist 的出站访问防火墙 profile；
- 用于在 container 中重新打开 workspace 的 VS Code 设置和扩展推荐；
- 命令历史和 Codex 配置的持久挂载；
- `bubblewrap`，因此当 container 授予所需 capabilities 时，Codex 仍可使用其 Linux 沙箱。

试用步骤：

1. 安装 Visual Studio Code 和 [Dev Containers 扩展](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)。
2. 将 Codex 示例 `.devcontainer` 设置复制到你的仓库，或直接从 Codex 仓库开始。
3. 在 VS Code 中运行 **Dev Containers: Open Folder in Container...**，并选择 `.devcontainer/devcontainer.secure.json`。
4. Container 启动后，打开终端并运行 `codex`。

也可以从 CLI 启动 container：

```bash
devcontainer up --workspace-folder . --config .devcontainer/devcontainer.secure.json
```

示例包含三个主要部分：

- `.devcontainer/devcontainer.secure.json` 控制 container 设置、capabilities、mounts、环境变量和 VS Code 扩展。
- `.devcontainer/Dockerfile.secure` 定义基于 Ubuntu 的镜像和已安装工具。
- `.devcontainer/init-firewall.sh` 应用出站网络策略。

参考防火墙有意作为起点。如果你依赖域名 allowlisting 做隔离，请实现适合你环境的 DNS rebinding 和 DNS refresh 保护，例如感知 TTL 的刷新或 DNS-aware firewall。

在 container 内，请选择以下模式之一：

- 如果 Dev Container profile 授予 `bwrap` 创建内层沙箱所需的 capabilities，请保持 Codex 的 Linux 沙箱启用。
- 如果 container 是你预期的安全边界，请在 container 内用 `--sandbox danger-full-access` 运行 Codex，这样 Codex 不会尝试创建第二层沙箱。

#### 版本控制

Codex 最适合配合版本控制工作流：

- 在 feature branch 上工作，并在委派前保持 `git status` 干净。这让 Codex patch 更容易隔离和回滚。
- 优先使用基于 patch 的工作流（例如 `git diff` / `git apply`），而不是直接编辑 tracked files。频繁提交，这样可以小步回滚。
- 像对待任何其他 PR 一样对待 Codex 建议：运行有针对性的验证、审查 diff，并在 commit message 中记录决策以便审计。

#### 监控和遥测

Codex 支持通过 OpenTelemetry (OTel) 选择性监控，帮助团队审计用量、调查问题并满足合规要求，同时不削弱本地安全默认值。Telemetry 默认关闭；请在配置中显式启用。

##### 概览

- Codex 默认关闭 OTel export，让本地运行保持自包含。
- 启用后，Codex 会发出结构化 log events，覆盖 conversations、API requests、SSE/WebSocket stream activity、user prompts（默认 redacted）、tool approval decisions 和 tool results。
- Codex 会用 `service.name`（originator）、CLI version 和 environment label 标记导出的 events，用于区分 dev/staging/prod 流量。

##### 启用 OTel（选择加入）

向 Codex 配置（通常是 `~/.codex/config.toml`）添加 `[otel]` block，选择 exporter，并决定是否记录 prompt 文本。

```toml
[otel]
environment = "staging"   # dev | staging | prod
exporter = "none"          # none | otlp-http | otlp-grpc
log_user_prompt = false     # redact prompt text unless policy allows
```

- `exporter = "none"` 会保留 instrumentation，但不会向任何位置发送数据。
- 若要把 events 发送到你自己的 collector，请选择以下之一：

```toml
[otel]
exporter = { otlp-http = {
  endpoint = "https://otel.example.com/v1/logs",
  protocol = "binary",
  headers = { "x-otlp-api-key" = "${OTLP_TOKEN}" }
}}
```

```toml
[otel]
exporter = { otlp-grpc = {
  endpoint = "https://otel.example.com:4317",
  headers = { "x-otlp-meta" = "abc123" }
}}
```

Codex 会批量发送 events，并在 shutdown 时 flush。Codex 只导出其 OTel module 产生的 telemetry。

##### 事件类别

代表性 event types 包括：

- `codex.conversation_starts`（model、reasoning settings、sandbox / approval policy）
- `codex.api_request`（attempt、status/success、duration 和 error details）
- `codex.sse_event`（stream event kind、success/failure、duration，以及 `response.completed` 上的 token counts）
- `codex.websocket_request` 和 `codex.websocket_event`（request duration，以及每条 message 的 kind/success/error）
- `codex.user_prompt`（length；除非显式启用，否则 content 会被 redacted）
- `codex.tool_decision`（approved/denied，source：configuration vs. user）
- `codex.tool_result`（duration、success、output snippet）

关联的 OTel metrics（counter 加 duration histogram pair）包括 `codex.api_request`、`codex.sse_event`、`codex.websocket.request`、`codex.websocket.event` 和 `codex.tool.call`（以及对应的 `.duration_ms` instruments）。

完整 event catalog 和配置参考请参阅 GitHub 上的 [Codex configuration documentation](https://github.com/openai/codex/blob/main/docs/config.md#otel)。

##### 安全和隐私建议

- 除非 policy 明确允许存储 prompt contents，否则保持 `log_user_prompt = false`。Prompts 可能包含源代码和敏感数据。
- 只将 telemetry 路由到你控制的 collectors；应用与你的合规要求一致的保留限制和访问控制。
- 将 tool arguments 和 outputs 视为敏感数据。可行时优先在 collector 或 SIEM 上做 redaction。
- 如果你不希望 Codex 在 `CODEX_HOME` 下保存 session transcripts，请审查本地数据保留设置（例如 `history.persistence` / `history.max_bytes`）。请参阅 [高级配置](17-advanced-configuration.md#history-persistence) 和 [配置参考](16-configuration-reference.md)。
- 如果 CLI 在网络访问关闭的情况下运行，OTel export 无法访问 collector。若要 export，请在 `workspace-write` 模式中允许 OTel endpoint 的网络访问，或从 Codex cloud export 并将 collector domain 加入 approved list。
- 定期审查 events，关注审批 / 沙箱变更和意外工具执行。

OTel 是可选功能，旨在补充而不是替代上文描述的沙箱和审批保护。

#### 托管配置

企业管理员可以在[托管配置](67-managed-configuration.md)中为其 workspace 配置 Codex 安全设置。有关设置和策略的详情，请参阅该页面。
