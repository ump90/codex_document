### 配置基础

Source: [Config basics](https://developers.openai.com/codex/config-basic.md)

Codex 会从多个位置读取配置细节。你的个人默认值位于 `~/.codex/config.toml`，你也可以使用 `.codex/config.toml` 文件添加项目覆盖。出于安全考虑，Codex 只会在你信任项目时加载项目 `.codex/` 层。

#### Codex 配置文件

Codex 将用户级配置存储在 `~/.codex/config.toml`。要将设置限定到特定项目或子文件夹，请在你的 repo 中添加 `.codex/config.toml` 文件。

要从 Codex IDE extension 打开配置文件，请选择右上角的齿轮图标，然后选择 **Codex Settings > Open config.toml**。

CLI 和 IDE extension 共享相同的配置层。你可以使用这些配置来：

- 设置默认模型和提供商。
- 配置 [审批策略和沙盒设置](https://developers.openai.com/codex/agent-approvals-security#sandbox-and-approvals)。
- 配置 [MCP servers](https://developers.openai.com/codex/mcp)。

#### 配置优先级

Codex 按以下顺序解析值（优先级从高到低）：

1. CLI 标志和 `--config` 覆盖
2. 项目配置文件：`.codex/config.toml`，按从项目根目录到当前工作目录的顺序排列（最近者优先；仅限可信项目）
3. 使用 `--profile profile-name` 选择的 [Profile](https://developers.openai.com/codex/config-advanced#profiles) 文件（`~/.codex/profile-name.config.toml`）
4. 用户配置：`~/.codex/config.toml`
5. 系统配置（如果存在）：Unix 上的 `/etc/codex/config.toml`
6. 内置默认值

使用该优先级在 `config.toml` 中设置共享默认值，并让 [profile 文件](https://developers.openai.com/codex/config-advanced#profiles) 专注于不同的值。

如果你将项目标记为 untrusted，Codex 会跳过项目范围 `.codex/` 层，包括项目本地配置、hooks 和 rules。用户和系统配置仍会加载，包括用户/全局 hooks 和 rules。

有关通过 `-c`/`--config` 进行一次性覆盖（包括 TOML 引号规则），请参阅 [高级配置](https://developers.openai.com/codex/config-advanced#one-off-overrides-from-the-cli)。

在托管机器上，你的组织还可以通过 `requirements.toml` 强制执行约束（例如，不允许 `approval_policy = "never"` 或 `sandbox_mode = "danger-full-access"`）。请参阅 [Managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration) 和 [Admin-enforced requirements](https://developers.openai.com/codex/enterprise/managed-configuration#admin-enforced-requirements-requirementstoml)。

#### 常见配置选项

下面是人们最常修改的一些选项：

#### 默认模型

选择 Codex 在 CLI 和 IDE 中默认使用的模型。

```toml
model = "gpt-5.5"
```

#### 审批提示

控制 Codex 何时在运行生成命令前暂停询问。

```toml
approval_policy = "on-request"
```

有关 `untrusted`、`on-request` 和 `never` 的行为差异，请参阅 [不显示审批提示运行](https://developers.openai.com/codex/agent-approvals-security#run-without-approval-prompts) 和 [常见沙盒和审批组合](https://developers.openai.com/codex/agent-approvals-security#common-sandbox-and-approval-combinations)。

#### 沙盒级别

调整 Codex 在执行命令时拥有多少文件系统和网络访问权限。

```toml
sandbox_mode = "workspace-write"
```

有关逐模式行为（包括受保护的 `.git`/`.codex` 路径和网络默认值），请参阅 [沙盒和审批](https://developers.openai.com/codex/agent-approvals-security#sandbox-and-approvals)、[可写根目录中的受保护路径](https://developers.openai.com/codex/agent-approvals-security#protected-paths-in-writable-roots) 和 [网络访问](https://developers.openai.com/codex/agent-approvals-security#network-access)。

#### 权限配置档

Codex 还支持用于可复用文件系统和网络策略的命名权限 profiles。内置 profiles 为 `:read-only`、`:workspace` 和 `:danger-full-access`。自定义 profiles 使用 `[permissions.]` 表和匹配的 `default_permissions` 值。请参阅 [Permissions](https://developers.openai.com/codex/permissions)。

#### Windows 沙盒模式

在 Windows 上原生运行 Codex 时，请在 `windows` 表中将原生沙盒模式设置为 `elevated`。只有在你没有管理员权限或 elevated 设置失败时，才使用 `unelevated`。

```toml
[windows]
sandbox = "elevated"   # Recommended
# sandbox = "unelevated" # Fallback if admin permissions/setup are unavailable
```

#### 网页搜索模式

Codex 默认为本地任务启用 web search，并从 web search cache 提供结果。该缓存是 OpenAI 维护的 Web 结果索引，因此 cached mode 会返回预先索引的结果，而不是抓取实时页面。这降低了暴露于任意实时内容中 prompt injection 的风险，但你仍应将 Web 结果视为不可信。如果你使用 `--yolo` 或其他 [full access 沙盒设置](https://developers.openai.com/codex/agent-approvals-security#common-sandbox-and-approval-combinations)，web search 默认使用实时结果。使用 `web_search` 选择模式：

- `"cached"`（默认）从 web search cache 提供结果。
- `"live"` 从 Web 获取最新数据（等同于 `--search`）。
- `"disabled"` 关闭 web search 工具。

```toml
web_search = "cached"  # default; serves results from the web search cache
# web_search = "live"  # fetch the most recent data from the web (same as --search)
# web_search = "disabled"
```

#### 推理强度

在支持时，调整模型应用多少推理强度。

```toml
model_reasoning_effort = "high"
```

#### 沟通风格

为受支持模型设置默认沟通风格。

```toml
personality = "friendly" # or "pragmatic" or "none"
```

你可以稍后在活动会话中使用 `/personality` 覆盖此设置，或在使用 app-server APIs 时按线程/轮次覆盖。

#### TUI 键位映射

在 `tui.keymap` 下自定义终端快捷键。选定的输入框动作会回退到匹配的 `tui.keymap.global` 绑定；在支持时，特定上下文绑定优先。空列表会解除该动作的绑定。

```toml
[tui.keymap.global]
open_transcript = "ctrl-t"

[tui.keymap.composer]
submit = ["enter", "ctrl-m"]

[tui.keymap.chat]
interrupt_turn = "f12"
```

#### 命令环境

控制 Codex 将哪些环境变量转发给派生出的命令。

```toml
[shell_environment_policy]
include_only = ["PATH", "HOME"]
```

#### 日志目录

覆盖 Codex 写入本地日志文件的位置。显式设置 `log_dir` 也会在该目录中启用可选的明文 TUI 日志 `codex-tui.log`。

```toml
log_dir = "/absolute/path/to/codex-logs"
```

对于一次性运行，你也可以从 CLI 设置它：

```bash
codex -c log_dir=./.codex-log
```

#### 功能标志

使用 `config.toml` 中的 `[features]` 表切换可选和实验性能力。

```toml
[features]
shell_snapshot = true           # Speed up repeated commands
```

#### 支持的功能

| Key                  |        Default        | Maturity     | Description                                                                              |
| -------------------- | :-------------------: | ------------ | ---------------------------------------------------------------------------------------- |
| `apps`               |         false         | Experimental | 启用 ChatGPT Apps/connectors 支持                                                   |
| `codex_git_commit`   |         false         | Experimental | 启用 Codex 生成的 git commits 和 commit attribution trailers                       |
| `hooks`              |         true          | Stable       | 启用来自 `hooks.json` 或 inline `[hooks]` 的 lifecycle hooks。参见 [Hooks](https://developers.openai.com/codex/hooks)。 |
| `fast_mode`          |         true          | Stable       | 启用 Fast mode 选择和 `service_tier = "fast"` 路径                          |
| `memories`           |         false         | Stable       | 启用 [Memories](https://developers.openai.com/codex/memories)                                                       |
| `multi_agent`        |         true          | Stable       | 启用 subagent 协作工具                                                      |
| `personality`        |         true          | Stable       | 启用 personality 选择控制                                                    |
| `shell_snapshot`     |         true          | Stable       | 为你的 shell environment 创建快照，以加速重复命令                            |
| `shell_tool`         |         true          | Stable       | 启用默认 `shell` tool                                                          |
| `unified_exec`       | `true` except Windows | Stable       | 使用由 PTY 支持的 unified exec tool                                                     |
| `undo`               |         false         | Stable       | 通过 per-turn git ghost snapshots 启用 undo                                             |
| `web_search`         |         true          | Deprecated   | 旧版开关；优先使用顶层 `web_search` 设置                                 |
| `web_search_cached`  |         false         | Deprecated   | 旧版开关，在未设置时映射到 `web_search = "cached"`                            |
| `web_search_request` |         false         | Deprecated   | 旧版开关，在未设置时映射到 `web_search = "live"`                              |

Maturity 列使用 Experimental、Beta 和 Stable 等功能成熟度标签。请参阅 [Feature Maturity](https://developers.openai.com/codex/feature-maturity) 了解如何解释这些标签。

省略 feature keys 以保留其默认值。

有关 lifecycle hook 配置，请参阅 [Hooks](https://developers.openai.com/codex/hooks)。

#### 启用功能

- 在 `config.toml` 中，在 `[features]` 下添加 `feature_name = true`。
- 从 CLI 运行 `codex --enable feature_name`。
- 要启用多个 feature，请运行 `codex --enable feature_a --enable feature_b`。
- 要禁用某个 feature，请在 `config.toml` 中将该键设置为 `false`。
