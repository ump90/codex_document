### 钩子

Source: [Hooks](https://developers.openai.com/codex/hooks.md)

Hooks 是 Codex 的可扩展性框架。它们允许你将自己的脚本注入 agent 循环，从而启用如下功能：

- 将对话发送到自定义日志或分析引擎
- 扫描团队提示词，阻止意外粘贴 API key
- 汇总对话，自动创建持久记忆
- 在对话轮次停止时运行自定义验证检查以强制执行标准
- 在特定目录中自定义提示

Hooks 默认启用。如果需要在 `config.toml` 中关闭它们，请设置：

```toml
[features]
hooks = false
```

使用 `hooks` 作为规范功能键。`codex_hooks` 仍可作为已弃用的别名使用。

管理员也可以在 `requirements.toml` 中用同样方式通过 `[features].hooks = false` 强制关闭 hooks。

需要记住的运行时行为：

- 来自多个文件的匹配 hooks 都会运行。
- 同一事件的多个匹配 command hooks 会并发启动，因此一个 hook 无法阻止另一个匹配 hook 启动。
- 非托管 command hooks 必须先经过审查并被信任，之后才会运行。
- `PreToolUse`、`PermissionRequest`、`PostToolUse`、`PreCompact`、
  `PostCompact`、`UserPromptSubmit`、`SubagentStop` 和 `Stop` 在轮次作用域运行。`SessionStart` 和 `SubagentStart` 在线程或 subagent 启动作用域运行。

#### Codex 在哪里查找钩子

Codex 会在活动配置层旁边发现以下任一形式的 hooks：

- `hooks.json`
- `config.toml` 中的内联 `[hooks]` 表

已安装的插件也可以通过插件 manifest 或默认的 `hooks/hooks.json` 文件打包生命周期配置。有关插件打包规则，请参阅 [构建插件](69-build-plugins.md#bundled-mcp-servers-and-lifecycle-config)。

实际使用中，四个最有用的位置是：

- `~/.codex/hooks.json`
- `~/.codex/config.toml`
- `/.codex/hooks.json`
- `/.codex/config.toml`

如果存在多个 hook 来源，Codex 会加载所有匹配的 hooks。
高优先级配置层不会替换低优先级 hooks。
如果单个配置层同时包含 `hooks.json` 和内联 `[hooks]`，Codex 会合并它们并在启动时发出警告。建议每个配置层只使用一种表示方式。

Codex 也可以发现随已启用插件打包的 hooks。插件打包的 hooks 会与其他 hook 来源一起加载，并使用与其他非托管 hooks 相同的信任审查流程。

项目本地 hooks 只会在项目 `.codex/` 层受信任时加载。在不受信任的项目中，Codex 仍会从各自的活动配置层加载用户和系统 hooks。

#### 审查和信任钩子

Codex 会在决定哪些 hooks 可以运行之前列出已配置的 hooks。非托管 command hook 运行前，Codex 要求你审查并信任精确的 hook 定义。Codex 会根据 hook 当前的 hash 记录信任状态，因此新的或已变更的 hooks 会被标记为待审查，并在被信任之前跳过。

在 CLI 中使用 `/hooks` 检查 hook 来源、审查新的或已变更的 hooks、信任 hooks，或禁用单个非托管 hooks。如果启动时有 hooks 需要审查，Codex 会打印警告，提示你打开 `/hooks`。

来自系统、MDM、云端或 `requirements.toml` 来源的托管 hooks 会被标记为 managed，由策略信任，并且无法从用户 hook 浏览器中禁用。

对于已经在 Codex 外部审查 hook 来源的一次性自动化，可以传入 `--dangerously-bypass-hook-trust`，让已启用的 hooks 在该次调用中运行，而无需持久化 hook 信任。

#### 配置形状

Hooks 按三个层级组织：

- 一个 hook 事件，例如 `PreToolUse`、`PostToolUse`、`PreCompact`、
  `SubagentStart` 或 `Stop`
- 一个 matcher group，用于决定该事件何时匹配
- 一个或多个 hook handlers，在 matcher group 匹配时运行

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.codex/hooks/session_start.py",
            "statusMessage": "Loading session notes"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py\"",
            "statusMessage": "Checking Bash command"
          }
        ]
      }
    ],
    "PermissionRequest": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/permission_request.py\"",
            "statusMessage": "Checking approval request"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/post_tool_use_review.py\"",
            "statusMessage": "Reviewing Bash output"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/user_prompt_submit_data_flywheel.py\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/stop_continue.py\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

说明：

- `timeout` 以秒为单位。
- 如果省略 `timeout`，Codex 使用 `600` 秒。
- `statusMessage` 是可选的。
- `commandWindows` 是可选的、仅限 Windows 的命令覆盖项。在 TOML 中，使用
  `command_windows` 或 `commandWindows`。
- `async` 会被解析，但尚不支持异步 command hooks。Codex 会跳过带有
  `async: true` 的 handlers。
- 目前只有 `type: "command"` handlers 会运行。`prompt` 和 `agent` handlers 会被解析但跳过。
- 命令会以会话 `cwd` 作为工作目录运行。
- 对于仓库本地 hooks，建议从 git root 解析，而不是使用 `.codex/hooks/...` 这样的相对路径。Codex 可能从子目录启动，而基于 git root 的路径能让 hook 位置保持稳定。

`config.toml` 中等效的内联 TOML：

```toml
[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py"'
timeout = 30
statusMessage = "Checking Bash command"

[[hooks.PostToolUse]]
matcher = "^Bash$"

[[hooks.PostToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/post_tool_use_review.py"'
timeout = 30
statusMessage = "Reviewing Bash output"
```

#### 匹配器模式

`matcher` 字段是一个 regex 字符串，用于过滤 hooks 何时触发。使用 `"*"`、
`""`，或完全省略 `matcher`，即可匹配受支持事件的每一次出现。

当前只有部分 Codex 事件会遵循 `matcher`：

| 事件                | `matcher` 过滤内容     | 说明                                                         |
| ------------------- | ---------------------- | ------------------------------------------------------------ |
| `PermissionRequest` | 工具名称               | 支持 `Bash`、`apply_patch`\* 和 MCP 工具名称 |
| `PostToolUse`       | 工具名称               | 支持 `Bash`、`apply_patch`\* 和 MCP 工具名称 |
| `PostCompact`       | 压缩触发器             | 值为 `manual` 或 `auto` |
| `PreCompact`        | 压缩触发器             | 值为 `manual` 或 `auto` |
| `PreToolUse`        | 工具名称               | 支持 `Bash`、`apply_patch`\* 和 MCP 工具名称 |
| `SessionStart`      | 启动来源               | 值为 `startup`、`resume`、`clear` 和 `compact` |
| `SubagentStart`     | subagent 类型          | 值取决于启动的 subagent |
| `SubagentStop`      | subagent 类型          | 值取决于停止的 subagent |
| `UserPromptSubmit`  | 不支持                 | 此事件会忽略任何已配置的 `matcher` |
| `Stop`              | 不支持                 | 此事件会忽略任何已配置的 `matcher` |

\*对于 `apply_patch`，`matcher` 值也可以使用 `Edit` 或 `Write`。

示例：

- `Bash`
- `^apply_patch$`
- `Edit|Write`
- `mcp__filesystem__read_file`
- `mcp__filesystem__.*`
- `startup|resume|clear|compact`
- `manual|auto`
