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

已安装的插件也可以通过插件 manifest 或默认的 `hooks/hooks.json` 文件打包生命周期配置。有关插件打包规则，请参阅 [构建插件](69-build-plugins.md)。

实际使用中，四个最有用的位置是：

- `~/.codex/hooks.json`
- `~/.codex/config.toml`
- `<repo>/.codex/hooks.json`
- `<repo>/.codex/config.toml`

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

#### 来自 `requirements.toml` 的托管 hooks { #managed-hooks-from-requirementstoml }

企业托管 requirements 也可以在 `[hooks]` 下内联定义 hooks。当管理员想强制执行 hook 配置，同时通过 MDM 或其它设备管理系统分发实际脚本时，这很有用。要让托管 hooks 即使在用户本地禁用 hooks 时也强制生效，请在 `requirements.toml` 中同时固定 `[features].hooks = true` 和 `[hooks]`。如果要忽略用户、项目、会话和插件 hooks，但仍允许管理员托管 hooks，请设置 `allow_managed_hooks_only = true`。

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

托管 hooks 说明：

- `managed_dir` 用于 macOS 和 Linux。
- `windows_managed_dir` 用于 Windows。
- Codex 不会分发 `managed_dir` 中的脚本；你的企业工具必须单独安装和更新这些脚本。
- 托管 hook 命令应使用配置的托管目录下的绝对脚本路径。
- `allow_managed_hooks_only = true` 会跳过用户、项目、会话和插件来源的 hooks，但仍会加载来自 `requirements.toml` 和其它托管配置层的托管 hooks。

#### 插件打包的 hooks { #plugin-bundled-hooks }

启用插件后，Codex 可以从该插件加载 lifecycle hooks，并与用户、项目和托管 hooks 一起使用。

默认情况下，Codex 会在插件根目录内查找 `hooks/hooks.json`。插件 manifest 可以在 `.codex-plugin/plugin.json` 中通过 `hooks` 条目覆盖该默认路径。manifest 条目可以是以 `./` 开头的路径、以 `./` 开头的路径数组、内联 hooks 对象，或内联 hooks 对象数组。

```json
{
  "name": "repo-policy",
  "hooks": "./hooks/hooks.json"
}
```

Manifest hook 路径会相对于插件根目录解析，并且必须保持在该根目录内。如果 manifest 定义了 `hooks`，Codex 会使用这些 manifest 条目，而不是默认的 `hooks/hooks.json`。

插件 hook 命令会收到这些环境变量：

- `PLUGIN_ROOT` 是 Codex 专属扩展，指向已安装的插件根目录。
- `PLUGIN_DATA` 是 Codex 专属扩展，指向插件的可写数据目录。
- 为兼容现有插件 hooks，Codex 也会设置 `CLAUDE_PLUGIN_ROOT` 和 `CLAUDE_PLUGIN_DATA`。

插件 hooks 使用与其它 hooks 相同的事件 schema。安装或启用插件不会自动信任其 hooks；在你审查并信任当前 hook 定义之前，Codex 会跳过插件打包的 hooks。

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

#### 通用输入字段 { #common-input-fields }

每个 command hook 都会在 `stdin` 上收到一个 JSON 对象。

这些是你通常会使用的共享字段：

| 字段              | 类型             | 含义                                                              |
| ----------------- | ---------------- | ----------------------------------------------------------------- |
| `session_id`      | `string`         | 当前 Codex 会话 ID。Subagent hooks 使用父会话 ID。                |
| `transcript_path` | `string \| null` | 会话转录文件路径（如果存在）。                                    |
| `cwd`             | `string`         | 会话的工作目录。                                                  |
| `hook_event_name` | `string`         | 当前 hook 事件名称。                                              |
| `model`           | `string`         | Codex 专属扩展。当前活动模型 slug。                               |

Turn 作用域的 hooks 会在对应事件表中列出 `turn_id`，它是 Codex 专属扩展。

`SessionStart`、`PreToolUse`、`PermissionRequest`、`PostToolUse`、`UserPromptSubmit`、`SubagentStart`、`SubagentStop` 和 `Stop` 还包含 `permission_mode`，描述当前权限模式，其值为 `default`、`acceptEdits`、`plan`、`dontAsk` 或 `bypassPermissions`。

`transcript_path` 会为了方便指向一份对话转录记录，但转录格式不是 hooks 的稳定接口，未来可能变化。

如果你需要完整 wire format，请参阅 [Schemas](#schemas)。

#### 通用输出字段 { #common-output-fields }

`SessionStart`、`PreCompact`、`PostCompact`、`UserPromptSubmit`、`SubagentStop` 和 `Stop` 支持这些共享 JSON 字段。`SubagentStart` 对 `systemMessage` 和 hook-specific context 接受相同形状，但 `continue: false` 不会阻止 subagent：

```json
{
  "continue": true,
  "stopReason": "optional",
  "systemMessage": "optional",
  "suppressOutput": false
}
```

| 字段             | 效果                                      |
| ---------------- | ----------------------------------------- |
| `continue`       | 如果为 `false`，标记该 hook run 已停止。  |
| `stopReason`     | 记录为停止原因。                          |
| `systemMessage`  | 在 UI 或 event stream 中显示为警告。      |
| `suppressOutput` | 当前会解析，但尚未实现。                  |

退出码为 `0` 且没有输出会被视为成功，Codex 会继续运行。

`PreToolUse` 和 `PermissionRequest` 支持 `systemMessage`，但这些事件目前不支持 `continue`、`stopReason` 和 `suppressOutput`。如果 `PreToolUse` hook 返回这些不支持的字段之一，Codex 会将该 hook run 标记为失败，报告错误，并继续工具调用。

`PostToolUse` 支持 `systemMessage`、`continue: false` 和 `stopReason`。`suppressOutput` 会被解析，但该事件目前不支持。

#### Hooks { #hooks }

##### SessionStart { #sessionstart }

此事件会将 `matcher` 应用于 `source`。

除[通用输入字段](#common-input-fields)外，还包含：

| 字段     | 类型     | 含义                                                          |
| -------- | -------- | ------------------------------------------------------------- |
| `source` | `string` | 会话如何启动：`startup`、`resume`、`clear` 或 `compact`。     |

`stdout` 上的纯文本会作为额外 developer context 加入。

`stdout` 上的 JSON 支持[通用输出字段](#common-output-fields)，以及这个 hook-specific 形状：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Load the workspace conventions before editing."
  }
}
```

其中 `additionalContext` 文本会作为额外 developer context 加入。

##### SubagentStart { #subagentstart }

此事件会将 `matcher` 应用于 `agent_type`。

除[通用输入字段](#common-input-fields)外，还包含：

| 字段              | 类型     | 含义                                      |
| ----------------- | -------- | ----------------------------------------- |
| `turn_id`         | `string` | Codex 专属扩展。当前 Codex turn ID。      |
| `agent_id`        | `string` | Subagent 标识符。                         |
| `agent_type`      | `string` | Subagent 类型或 profile。                 |
| `permission_mode` | `string` | 当前权限模式。                            |

`stdout` 上的纯文本会作为该 subagent 的额外 developer context 加入。

`stdout` 上的 JSON 支持 `systemMessage` 和这个 hook-specific 形状：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Review the repository test conventions first."
  }
}
```

其中 `additionalContext` 文本会作为该 subagent 的额外 developer context 加入。`continue: false` 会为了兼容性而解析，但不会阻止 subagent 启动。

##### PreToolUse { #pretooluse }

`PreToolUse` 可以拦截 Bash、通过 `apply_patch` 执行的文件编辑，以及 MCP 工具调用。它仍然是 guardrail，而不是完整执行边界，因为 Codex 通常可以通过其它受支持工具路径完成等价工作。

它目前还不会拦截所有 shell 调用，只拦截简单调用。较新的 `unified_exec` 机制支持更丰富的 shell stdin/stdout 流式处理，但拦截尚不完整。同样，它不会拦截 `WebSearch` 或其它非 shell、非 MCP 工具调用。

`matcher` 会应用到 `tool_name` 和 matcher alias。对于通过 `apply_patch` 进行的文件编辑，`matcher` 值可以使用 `apply_patch`、`Edit` 或 `Write`；hook 输入仍会报告 `tool_name: "apply_patch"`。

除[通用输入字段](#common-input-fields)外，还包含：

| 字段          | 类型         | 含义                                                                                                       |
| ------------- | ------------ | ---------------------------------------------------------------------------------------------------------- |
| `turn_id`     | `string`     | Codex 专属扩展。当前 Codex turn ID。                                                                       |
| `tool_name`   | `string`     | 规范 hook 工具名，例如 `Bash`、`apply_patch`，或 `mcp__fs__read` 这样的 MCP 名称。                         |
| `tool_use_id` | `string`     | 本次调用的工具调用 ID。                                                                                    |
| `tool_input`  | `JSON value` | 工具专属输入。`Bash` 和 `apply_patch` 使用 `tool_input.command`，MCP 工具会发送所有参数。                  |

`stdout` 上的纯文本会被忽略。

`stdout` 上的 JSON 可以使用 `systemMessage`。要拒绝受支持的工具调用，请返回这个 hook-specific 形状：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by hook."
  }
}
```

Codex 也接受这个旧版 block 形状：

```json
{
  "decision": "block",
  "reason": "Destructive command blocked by hook."
}
```

你也可以使用退出码 `2`，并将阻止原因写入 `stderr`。

要在不阻止的情况下添加模型可见上下文，请返回 `hookSpecificOutput.additionalContext`：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": "The pending command touches generated files."
  }
}
```

要在不阻止的情况下重写受支持的工具调用，请返回带 `updatedInput` 的 `permissionDecision: "allow"`：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": {
      "command": "echo rewritten"
    }
  }
}
```

对于 Bash 命令和 `apply_patch`，`updatedInput` 必须包含字符串 `command` 字段。对于 MCP 工具，`updatedInput` 是替换后的参数对象。只有在 `permissionDecision: "allow"` 时才返回 `updatedInput`；其它 `updatedInput` 形状会被报告为错误。

`permissionDecision: "ask"`、旧版 `decision: "approve"`、`continue: false`、`stopReason` 和 `suppressOutput` 会被解析，但尚不支持。Codex 会将该 hook run 标记为失败，报告错误，并继续工具调用。

##### PermissionRequest { #permissionrequest }

当 Codex 即将请求批准时，`PermissionRequest` 会运行，例如 shell escalation 或 managed-network approval。它可以允许请求、拒绝请求，或不作决定并让正常审批提示继续。它不会为不需要审批的命令运行。

`matcher` 会应用到 `tool_name` 和 matcher alias。当前规范值包括 `Bash`、`apply_patch`，以及 `mcp__server__tool` 这样的 MCP 工具名；`apply_patch` 也匹配 `Edit` 和 `Write`。

除[通用输入字段](#common-input-fields)外，还包含：

| 字段                     | 类型             | 含义                                                                                                      |
| ------------------------ | ---------------- | --------------------------------------------------------------------------------------------------------- |
| `turn_id`                | `string`         | Codex 专属扩展。当前 Codex turn ID。                                                                      |
| `tool_name`              | `string`         | 规范 hook 工具名，例如 `Bash`、`apply_patch`，或 `mcp__fs__read` 这样的 MCP 名称。                        |
| `tool_input`             | `JSON value`     | 工具专属输入。`Bash` 和 `apply_patch` 使用 `tool_input.command`，MCP 工具会发送所有参数。                 |
| `tool_input.description` | `string \| null` | Codex 有可读审批原因时，该字段是人类可读审批原因。                                                       |

`stdout` 上的纯文本会被忽略。

有些工具输入可能包含人类可读描述，但不要假设每个工具都有 `tool_input.description` 字段。

要批准请求，请返回：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow"
    }
  }
}
```

要拒绝请求，请返回：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "deny",
      "message": "Blocked by repository policy."
    }
  }
}
```

如果多个匹配 hooks 返回决策，任何 `deny` 都优先。否则，一个 `allow` 会让请求继续，而不显示审批提示。如果没有匹配 hook 做出决定，Codex 使用正常审批流程。

不要为 `PermissionRequest` 返回 `updatedInput`、`updatedPermissions` 或 `interrupt`；这些字段为未来行为保留，当前会 fail closed。

##### PostToolUse { #posttooluse }

`PostToolUse` 会在受支持工具产生输出后运行，包括 Bash、`apply_patch` 和 MCP 工具调用。对于 Bash，它也会在命令以非零状态退出后运行。它无法撤销已经运行的工具副作用。

它目前还不会拦截所有 shell 调用，只拦截简单调用。较新的 `unified_exec` 机制支持更丰富的 shell stdin/stdout 流式处理，但拦截尚不完整。同样，它不会拦截 `WebSearch` 或其它非 shell、非 MCP 工具调用。

`matcher` 会应用到 `tool_name` 和 matcher alias。对于通过 `apply_patch` 进行的文件编辑，`matcher` 值可以使用 `apply_patch`、`Edit` 或 `Write`；hook 输入仍会报告 `tool_name: "apply_patch"`。

除[通用输入字段](#common-input-fields)外，还包含：

| 字段            | 类型         | 含义                                                                                                      |
| --------------- | ------------ | --------------------------------------------------------------------------------------------------------- |
| `turn_id`       | `string`     | Codex 专属扩展。当前 Codex turn ID。                                                                      |
| `tool_name`     | `string`     | 规范 hook 工具名，例如 `Bash`、`apply_patch`，或 `mcp__fs__read` 这样的 MCP 名称。                        |
| `tool_use_id`   | `string`     | 本次调用的工具调用 ID。                                                                                   |
| `tool_input`    | `JSON value` | 工具专属输入。`Bash` 和 `apply_patch` 使用 `tool_input.command`，MCP 工具会发送所有参数。                 |
| `tool_response` | `JSON value` | 工具专属输出。对于 MCP 工具，这是 MCP 调用结果。                                                         |

`stdout` 上的纯文本会被忽略。

`stdout` 上的 JSON 可以使用 `systemMessage` 和这个 hook-specific 形状：

```json
{
  "decision": "block",
  "reason": "The Bash output needs review before continuing.",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "The command updated generated files."
  }
}
```

其中 `additionalContext` 文本会作为额外 developer context 加入。

对于此事件，`decision: "block"` 不会撤销已完成的 Bash 命令。相反，Codex 会记录反馈，用该反馈替换工具结果，并从 hook 提供的消息继续模型。

你也可以使用退出码 `2`，并将反馈原因写入 `stderr`。

要在命令已经运行后停止对原始工具结果的正常处理，请返回 `continue: false`。Codex 会用你的反馈或停止文本替换工具结果，并从那里继续。

`updatedMCPToolOutput` 和 `suppressOutput` 会被解析，但尚不支持。Codex 会将该 hook run 标记为失败，报告错误，并继续正常处理工具结果。

##### PreCompact { #precompact }

`PreCompact` 会在 Codex 压缩对话前运行。`matcher` 应用于 `trigger`，其值为 `manual` 和 `auto`。

除[通用输入字段](#common-input-fields)外，还包含：

| 字段      | 类型     | 含义                                      |
| --------- | -------- | ----------------------------------------- |
| `turn_id` | `string` | Codex 专属扩展。当前 Codex turn ID。      |
| `trigger` | `string` | 触发压缩的原因：`manual` 或 `auto`。      |

`stdout` 上的纯文本会被忽略。

`stdout` 上的 JSON 支持[通用输出字段](#common-output-fields)。如果匹配的 `PreCompact` hook 返回 `continue: false`，Codex 会在压缩前停止。

##### PostCompact { #postcompact }

`PostCompact` 会在 Codex 压缩对话后运行。`matcher` 应用于 `trigger`，其值为 `manual` 和 `auto`。

除[通用输入字段](#common-input-fields)外，还包含：

| 字段      | 类型     | 含义                                      |
| --------- | -------- | ----------------------------------------- |
| `turn_id` | `string` | Codex 专属扩展。当前 Codex turn ID。      |
| `trigger` | `string` | 触发压缩的原因：`manual` 或 `auto`。      |

`stdout` 上的纯文本会被忽略。

`stdout` 上的 JSON 支持[通用输出字段](#common-output-fields)。如果匹配的 `PostCompact` hook 返回 `continue: false`，Codex 会在压缩后停止。

##### UserPromptSubmit { #userpromptsubmit }

此事件目前不使用 `matcher`。

除[通用输入字段](#common-input-fields)外，还包含：

| 字段      | 类型     | 含义                                      |
| --------- | -------- | ----------------------------------------- |
| `turn_id` | `string` | Codex 专属扩展。当前 Codex turn ID。      |
| `prompt`  | `string` | 即将发送的用户提示。                      |

`stdout` 上的纯文本会作为额外 developer context 加入。

`stdout` 上的 JSON 支持[通用输出字段](#common-output-fields)和这个 hook-specific 形状：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Ask for a clearer reproduction before editing files."
  }
}
```

其中 `additionalContext` 文本会作为额外 developer context 加入。

要阻止该提示，请返回：

```json
{
  "decision": "block",
  "reason": "Ask for confirmation before doing that."
}
```

你也可以使用退出码 `2`，并将阻止原因写入 `stderr`。

##### SubagentStop { #subagentstop }

此事件会将 `matcher` 应用于 `agent_type`。

除[通用输入字段](#common-input-fields)外，还包含：

| 字段                     | 类型             | 含义                                         |
| ------------------------ | ---------------- | -------------------------------------------- |
| `turn_id`                | `string`         | Codex 专属扩展。当前 Codex turn ID。         |
| `agent_id`               | `string`         | Subagent 标识符。                            |
| `agent_type`             | `string`         | Subagent 类型或 profile。                    |
| `agent_transcript_path`  | `string \| null` | Subagent 转录文件路径（如果存在）。          |
| `stop_hook_active`       | `boolean`        | 该 subagent 是否已经被继续过。               |
| `last_assistant_message` | `string \| null` | 最新 subagent assistant 消息（如果可用）。   |

`SubagentStop` 在退出码为 `0` 时要求 `stdout` 上是 JSON。纯文本输出对此事件无效。

`stdout` 上的 JSON 支持[通用输出字段](#common-output-fields)。要让 Codex 继续 subagent 流程，请返回：

```json
{
  "decision": "block",
  "reason": "Run one more focused pass inside the subagent."
}
```

你也可以使用退出码 `2`，并将继续原因写入 `stderr`。

如果任何匹配的 `SubagentStop` hook 返回 `continue: false`，它会优先于其它匹配 `SubagentStop` hooks 的继续决策。

##### Stop { #stop }

此事件目前不使用 `matcher`。

除[通用输入字段](#common-input-fields)外，还包含：

| 字段                     | 类型             | 含义                                             |
| ------------------------ | ---------------- | ------------------------------------------------ |
| `turn_id`                | `string`         | Codex 专属扩展。当前 Codex turn ID。             |
| `stop_hook_active`       | `boolean`        | 该 turn 是否已经被 `Stop` 继续过。               |
| `last_assistant_message` | `string \| null` | 最新 assistant 消息文本（如果可用）。            |

`Stop` 在退出码为 `0` 时要求 `stdout` 上是 JSON。纯文本输出对此事件无效。

`stdout` 上的 JSON 支持[通用输出字段](#common-output-fields)。要让 Codex 继续，请返回：

```json
{
  "decision": "block",
  "reason": "Run one more pass over the failing tests."
}
```

你也可以使用退出码 `2`，并将继续原因写入 `stderr`。

对于此事件，`decision: "block"` 不会拒绝该 turn。相反，它告诉 Codex 继续，并自动创建新的 continuation prompt；该 prompt 会作为新的用户提示，并使用你的 `reason` 作为提示文本。

如果任何匹配的 `Stop` hook 返回 `continue: false`，它会优先于其它匹配 `Stop` hooks 的继续决策。

#### Schemas { #schemas }

链接的 `main` 分支 schemas 可能包含当前 release 中尚不存在的 hook 字段。请以本页作为 release 行为参考。

如果你需要精确的当前 wire format，请查看 [Codex GitHub 仓库](https://github.com/openai/codex/tree/main/codex-rs/hooks/schema/generated)中的生成 schemas。
