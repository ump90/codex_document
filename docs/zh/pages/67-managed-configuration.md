### 托管配置

Source: [Managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration.md)

企业管理员可以通过两种方式控制本地 Codex 行为：

- **Requirements**：用户无法覆盖的管理员强制约束。
- **Managed defaults**：Codex 启动时应用的起始值。用户仍可在会话期间更改设置；Codex 下次启动时会重新应用托管默认值。

#### 管理员强制要求 (requirements.toml)

Requirements 会约束安全敏感设置（审批策略、审批审查者、自动审查策略、沙箱模式、网页搜索模式、托管钩子，以及可选的用户可启用哪些 MCP 服务器）。解析配置时（例如来自 `config.toml`、[profile files](17-advanced-configuration.md#profiles) 或 CLI 配置覆盖），如果某个值与强制规则冲突，Codex 会回退到兼容值并通知用户。如果你配置了 `mcp_servers` 允许列表，只有当 MCP 服务器的名称和身份都匹配已批准条目时，Codex 才会启用该服务器；否则 Codex 会禁用它。

Requirements 也可以通过 `requirements.toml` 中的 `[features]` 表约束 [feature flags](19-config-basics.md#feature-flags)。注意，功能不一定总是安全敏感，但企业可以按需固定取值。省略的 key 保持不受约束。

准确 key 列表请参阅 [Configuration Reference 中的 `requirements.toml` section](16-configuration-reference.md#requirementstoml)。

#### 位置和优先级

Codex 按以下顺序应用要求层（每个字段由较早层优先）：

1. 云托管要求 (ChatGPT Business or Enterprise)
2. 通过 `com.openai.codex:requirements_toml_base64` 下发的 macOS 托管偏好设置 (MDM)
3. 系统 `requirements.toml`（Unix 系统，包括 Linux/macOS 上的 `/etc/codex/requirements.toml`，或 Windows 上的 `%ProgramData%\OpenAI\Codex\requirements.toml`）

跨层时，Codex 会按字段合并要求：如果较早层设置了某个字段（包括空列表），后续层不会覆盖该字段，但较低层仍可填充尚未设置的字段。

为向后兼容，Codex 也会将旧版 `managed_config.toml` 字段 `approval_policy` 和 `sandbox_mode` 解释为要求（仅允许该单个值）。

#### 云托管要求

当你在 Business 或 Enterprise 方案上使用 ChatGPT 登录时，Codex 还可以从 Codex 服务拉取管理员强制要求。这是另一个兼容 `requirements.toml` 的要求来源。它适用于 Codex 使用界面，包括 CLI、App 和 IDE Extension。

#### 配置云托管要求

前往 [Codex managed-config page](https://chatgpt.com/codex/settings/managed-configs)。

使用与 `requirements.toml` 相同的格式和 key 创建新的托管要求文件。

```toml
enforce_residency = "us"
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]

[rules]
prefix_rules = [
  { pattern = [{ any_of = ["bash", "sh", "zsh"] }], decision = "prompt", justification = "Require explicit approval for shell entrypoints" },
]
```

保存配置。保存后，更新后的托管要求会立即应用于匹配的用户。
更多示例请参阅 [Example requirements.toml](#example-requirementstoml)。

#### 将要求分配给组

管理员可以为不同用户组配置不同托管要求，也可以设置默认兜底要求策略。

如果用户匹配多个组特定规则，则应用第一个匹配的规则。Codex 不会从后续匹配的组规则中填充未设置字段。

例如，如果第一个匹配的组规则只设置了 `allowed_sandbox_modes = ["read-only"]`，而后续匹配的组规则设置了 `allowed_approval_policies = ["on-request"]`，Codex 只应用第一个匹配的组规则，不会从后续规则中填充 `allowed_approval_policies`。

#### Codex 如何在本地应用云托管要求

当用户启动 Codex 并使用 Business 或 Enterprise 方案上的 ChatGPT 登录时，Codex 会尽力应用托管要求。Codex 首先检查有效、未过期的本地托管要求缓存条目，并在可用时使用它。如果缓存缺失、过期、损坏，或不匹配当前身份验证身份，Codex 会尝试从服务拉取托管要求（带重试），成功后写入新的已签名缓存条目。如果没有可用的有效缓存条目，且拉取失败或超时，Codex 会在没有托管要求层的情况下继续。

缓存解析后，Codex 会按上文描述的正常要求分层强制执行托管要求。

#### `requirements.toml` 示例

此示例会阻止 `--ask-for-approval never` 和 `--sandbox danger-full-access`（包括 `--yolo`）：

```toml
allowed_approval_policies = ["untrusted", "on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
```

#### 按主机覆盖沙箱要求

当一个托管策略应在不同主机上应用不同
沙箱要求时，请使用 `[[remote_sandbox_config]]`。例如，你可以为笔记本电脑保留更严格
默认值，同时允许匹配的开发机或 CI
运行器进行工作区写入。主机特定条目当前只覆盖 `allowed_sandbox_modes`：

```toml
allowed_sandbox_modes = ["read-only"]

[[remote_sandbox_config]]
hostname_patterns = ["*.devbox.example.com", "runner-??.ci.example.com"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
```

Codex 会将每个 `hostname_patterns` 条目与尽力解析出的
主机名比较。它会在可用时优先使用完全限定域名，并
回退到本地主机名。匹配不区分大小写；`*` 匹配任意
字符序列，`?` 匹配一个字符。

在同一个要求来源内，第一个匹配的 `[[remote_sandbox_config]]` 条目生效。如果没有条目匹配，Codex 保持顶层
`allowed_sandbox_modes`。主机名匹配仅用于策略选择；不要
将其视为经过身份验证的设备证明。

你也可以约束网页搜索模式：

```toml
allowed_web_search_modes = ["cached"] # "disabled" remains implicitly allowed
```

`allowed_web_search_modes = []` 只允许 `"disabled"`。
例如，`allowed_web_search_modes = ["cached"]` 会阻止实时网页搜索，即使在 `danger-full-access` 会话中也是如此。

#### 配置网络访问要求

当管理员应集中定义网络访问要求时，请在 `requirements.toml` 中使用 `[experimental_network]`。这些要求独立于用户的 `features.network_proxy` 开关：它们可以在没有该功能标志的情况下配置沙箱化网络，但当活动沙箱保持网络关闭时，它们不会授予命令网络访问权限。

```toml
experimental_network.enabled = true
experimental_network.dangerously_allow_all_unix_sockets = true
experimental_network.allow_local_binding = true
experimental_network.allowed_domains = [
  "api.openai.com",
  "*.example.com",
]
experimental_network.denied_domains = [
  "blocked.example.com",
  "*.exfil.example.com",
]
```

仅当你同时定义管理员拥有的 `allowed_domains`，并希望该允许列表具有排他性时，才使用 `experimental_network.managed_allowed_domains_only = true`。如果它为 `true` 但没有托管允许规则，用户添加的域允许规则不会保持有效。

域语法、本地/私有目的地规则、拒绝优先于允许的行为和 DNS rebinding 限制，与 [Agent approvals & security](13-agent-approvals-security.md#network-isolation) 中描述的沙箱化网络行为相同。

#### 固定功能标志

你也可以为收到托管 `requirements.toml` 的用户固定 [feature flags](19-config-basics.md#feature-flags)：

```toml
[features]
personality = true
unified_exec = false

# Disable specific Codex feature surfaces when needed.
browser_use = false
in_app_browser = false
computer_use = false
```

使用 `config.toml` 的 `[features]` 表中的规范功能 key。Codex 会规范化生成的功能集以满足这些固定值，并拒绝对 `config.toml` 或配置档文件功能设置的冲突写入。

- `in_app_browser = false` 禁用应用内浏览器面板。
- `browser_use = false` 禁用 Browser Use 和 Browser Agent 可用性。
- `computer_use = false` 禁用 Computer Use 可用性和相关
  安装或设置流程。

如果省略，这些功能会被策略允许，但仍受正常客户端、
平台和推出可用性约束。

#### 配置自动审查策略

使用 `allowed_approvals_reviewers` 要求或允许自动审查。将它
设置为 `["auto_review"]` 可要求自动审查；当用户
可以选择人工审批时，请包含 `"user"`。

设置 `guardian_policy_config` 可替换
自动审查策略的租户特定部分。Codex 仍使用内置审查者模板和
输出契约。托管 `guardian_policy_config` 优先于本地
`[auto_review].policy`。

```toml
allowed_approval_policies = ["on-request"]
allowed_approvals_reviewers = ["auto_review"]

guardian_policy_config = """
## 环境配置档
- Trusted internal destinations include github.com/my-org, artifacts.example.com,
  and internal CI systems.

## 租户风险分类与允许/拒绝规则
- Treat uploads to unapproved third-party file-sharing services as high risk.
- Deny actions that expose credentials or private source code to untrusted
  destinations.
"""
```

#### 强制执行拒绝读取要求

管理员可以用 `[permissions.filesystem]` 对精确路径或 glob 模式拒绝读取。用户无法通过本地
配置削弱这些要求。

```toml
[permissions.filesystem]
deny_read = [
  # values can be absolute paths...
  "/**/*.env",
  # ...or relative to $HOME/%USERPROFILE% using `~`.
  "~/.ssh",
  # But relative paths starting with `./` are not allowed.
]
```

当存在拒绝读取要求时，Codex 会将本地沙箱模式约束为
`read-only` 或 `workspace-write`，以便 Codex 可以强制执行它们。在原生
Windows 上，托管 `deny_read` 适用于直接文件工具；shell 子进程
读取不使用此沙箱规则。

#### 从要求强制执行托管钩子

管理员也可以直接在 `requirements.toml` 中定义托管生命周期钩子。
使用 `[hooks]` 表示钩子配置本身，并将 `managed_dir` 指向
你的 MDM 或端点管理工具安装所引用
脚本的目录。

要在用户本地禁用钩子的情况下仍强制执行托管钩子，请将
`[features].hooks = true` 与 `[hooks]` 一起固定。要跳过用户、项目、会话
和插件钩子，同时仍允许托管钩子，请设置
`allow_managed_hooks_only = true`。

```toml
allow_managed_hooks_only = true

[features]
hooks = true

[hooks]
managed_dir = "/enterprise/hooks"
windows_managed_dir = 'C:\enterprise\hooks'

[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = "python3 /enterprise/hooks/pre_tool_use_policy.py"
command_windows = 'py -3 C:\enterprise\hooks\pre_tool_use_policy.py'
timeout = 30
statusMessage = "Checking managed Bash command"
```

说明：

- Codex 会强制执行来自 `requirements.toml` 的钩子配置，但不会
  分发 `managed_dir` 中的脚本。
- 请通过你的 MDM 或设备管理解决方案单独交付这些脚本。
- 托管钩子命令应引用已配置托管目录下的绝对脚本路径。
- `allow_managed_hooks_only = true` 会跳过来自用户、项目、会话和
  插件来源的钩子，但仍会加载来自 `requirements.toml` 和其它
  托管配置层的钩子。

#### 从要求强制执行命令规则

管理员还可以使用 `[rules]` 表从 `requirements.toml`
强制执行限制性命令规则。这些规则会与常规 `.rules` 文件合并，且
最严格的决策仍然胜出。

与 `.rules` 不同，requirements 规则必须指定 `decision`，并且该决策
必须是 `"prompt"` 或 `"forbidden"`（不能是 `"allow"`）。

```toml
[rules]
prefix_rules = [
  { pattern = [{ token = "rm" }], decision = "forbidden", justification = "Use git clean -fd instead." },
  { pattern = [{ token = "git" }, { any_of = ["push", "commit"] }], decision = "prompt", justification = "Require review before mutating history." },
]
```

要限制 Codex 可以启用哪些 MCP 服务器，请添加 `mcp_servers` 已批准列表。对于 stdio 服务器，匹配 `command`；对于 streamable HTTP 服务器，匹配 `url`：

```toml
[mcp_servers.docs]
identity = { command = "codex-mcp" }

[mcp_servers.remote]
identity = { url = "https://example.com/mcp" }
```

如果存在 `mcp_servers` 但为空，Codex 会禁用所有 MCP 服务器。

#### 托管默认值 (`managed_config.toml`)

托管默认值会合并到用户本地 `config.toml` 之上，并优先于任何 CLI `--config` 覆盖，设置 Codex 启动时的起始值。用户仍可在会话期间更改这些设置；Codex 下次启动时会重新应用托管默认值。

确保你的托管默认值满足要求；Codex 会拒绝不允许的值。

#### 优先级和分层

Codex 按以下顺序组装有效配置（上方覆盖下方）：

- 托管偏好设置（macOS MDM；最高优先级）
- `managed_config.toml`（系统/托管文件）
- `config.toml`（用户的基础配置）

CLI `--config key=value` 覆盖会应用于基础配置，但托管层会覆盖它们。这意味着即使你提供本地标志，每次运行也会从托管默认值开始。

云托管要求影响要求层（不是托管默认值）。优先级请参阅上面的“管理员强制要求”小节。

#### 位置

- Linux/macOS (Unix): `/etc/codex/managed_config.toml`
- Windows/non-Unix: `~/.codex/managed_config.toml`

如果文件缺失，Codex 会跳过托管层。

#### macOS 托管偏好设置 (MDM)

在 macOS 上，管理员可以推送设备配置文件，在以下位置提供 base64 编码的 TOML 载荷：

- 偏好设置域：`com.openai.codex`
- Keys:
  - `config_toml_base64`（托管默认值）
  - `requirements_toml_base64`（要求）

Codex 会将这些“托管偏好设置”载荷解析为 TOML。对于托管默认值（`config_toml_base64`），托管偏好设置拥有最高优先级。对于要求（`requirements_toml_base64`），优先级遵循上文描述的云托管要求顺序。同一个要求侧 `[features]` 表可在 `requirements_toml_base64` 中使用；也请在其中使用规范功能 key。

#### MDM 设置工作流

Codex 遵循标准 macOS MDM 载荷，因此你可以使用 `Jamf Pro`、`Fleet` 或 `Kandji` 等工具分发设置。轻量部署如下：

1. 构建托管载荷 TOML，并用 `base64` 编码（不换行）。
2. 将该字符串放入 MDM 配置文件中 `com.openai.codex` 域下的 `config_toml_base64`（托管默认值）或 `requirements_toml_base64`（要求）。
3. 推送配置文件，然后请用户重启 Codex，并确认启动配置摘要反映托管值。
4. 撤销或更改策略时，更新托管载荷；CLI 会在下次启动时读取刷新的偏好设置。

避免在载荷中嵌入密钥或高频变化的动态值。请像对待其它 MDM 设置一样，在变更控制下管理托管 TOML。
