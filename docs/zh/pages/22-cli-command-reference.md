### CLI 命令参考

Source: [Command line options](https://developers.openai.com/codex/cli/reference.md)

### 如何阅读本参考

本页列出每个已记录的 Codex CLI 命令和标志。可按键或说明搜索表格。每个部分都会说明该选项是 stable 还是 experimental，并标出有风险的组合。

CLI 会从 `~/.codex/config.toml` 继承大多数默认值。你在命令行传入的任何 `-c key=value` 覆盖都会在该次调用中优先。更多信息请参阅 [配置基础](19-config-basics.md#configuration-precedence)。

### 全局标志

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `PROMPT` | `string` | `` | 用于启动会话的可选文本指令。省略时会启动没有预填消息的 TUI。 |
| `--image, -i` | `path[,path...]` | `` | 将一个或多个图片文件附加到初始提示词。多个路径可用逗号分隔，也可重复该标志。 |
| `--model, -m` | `string` | `` | 覆盖配置中设置的模型（例如 `gpt-5.4`）。 |
| `--oss` | `boolean` | `false` | 使用本地开源模型提供商（等同于 `-c model_provider="oss"`）。会验证 Ollama 正在运行。 |
| `--profile, -p` | `string` | `` | 将 `$CODEX_HOME/profile-name.config.toml` 叠加到基础用户配置之上。 |
| `--sandbox, -s` | `read-only \| workspace-write \| danger-full-access` | `` | 为模型生成的 shell 命令选择沙箱策略。 |
| `--ask-for-approval, -a` | `untrusted \| on-request \| never` | `` | 控制 Codex 在运行命令前何时暂停请求人工审批。`on-failure` 已弃用；交互式运行优先使用 `on-request`，非交互式运行优先使用 `never`。 |
| `--dangerously-bypass-approvals-and-sandbox, --yolo` | `boolean` | `false` | 在没有审批或沙箱的情况下运行每个命令。只应在外部已加固的环境中使用。 |
| `--dangerously-bypass-hook-trust` | `boolean` | `false` | 在本次调用中运行已启用 hooks，而不要求持久化钩子信任。仅适用于已经审查 hook 来源的自动化。 |
| `--cd, -C` | `path` | `` | 在智能体开始处理你的请求前设置工作目录。 |
| `--search` | `boolean` | `false` | 启用实时网页搜索（将 `web_search = "live"` 设为默认值，而不是默认的 `"cached"`）。 |
| `--add-dir` | `path` | `` | 在主 workspace 之外授予其他目录写入访问权限。可重复指定多个路径。 |
| `--no-alt-screen` | `boolean` | `false` | 禁用 TUI 的 alternate screen mode（覆盖本次运行的 `tui.alternate_screen`）。 |
| `--remote` | `ws://host:port \| wss://host:port \| unix:// \| unix://PATH` | `` | 通过 WebSocket 或 Unix socket 将交互式 TUI 连接到远程 app-server endpoint。支持 `codex`、`codex resume` 和 `codex fork`；其他子命令会拒绝 remote 模式。 |
| `--remote-auth-token-env` | `ENV_VAR` | `` | 从此环境变量读取 bearer token，并在使用 `--remote` 连接时发送。要求 `--remote`；token 只会通过 `wss://` URL 或仅本地的 `ws://` URL 发送。 |
| `--strict-config` | `boolean` | `false` | 当 `config.toml` 包含此 Codex 版本无法识别的字段时报错。由 `codex`、`exec`、`review`、`resume`、`fork`、`app-server`、`mcp-server` 和 `exec-server` 等运行时命令支持。 |
| `--enable` | `feature` | `` | 强制启用功能标志（转换为 `-c features.<name>=true`）。可重复。 |
| `--disable` | `feature` | `` | 强制禁用功能标志（转换为 `-c features.<name>=false`）。可重复。 |
| `--config, -c` | `key=value` | `` | 覆盖配置值。值会尽可能按 TOML 解析；否则使用字面字符串。 |

这些选项适用于基础 `codex` 命令。大多数选项会传播到其他命令；例外情况请参阅上面的说明或相关命令帮助。对于会传播的标志，请遵循相关命令帮助。例如，`codex exec --oss ...` 会将 `--oss` 应用于 `exec`。

### 命令概览

“成熟度”列使用 Experimental、Beta 和 Stable 等功能成熟度标签。请参阅 [功能成熟度](03-feature-maturity.md) 了解如何解释这些标签。

| 键 | 成熟度 | 说明 |
| --- | --- | --- |
| [codex](22-cli-command-reference.md#codex-interactive) | `stable` | 启动终端 UI。接受上面的全局标志，以及可选提示词或图片附件。 |
| [codex app-server](22-cli-command-reference.md#codex-app-server) | `experimental` | 启动 Codex app server，用于通过 stdio、WebSocket 或 Unix socket 进行本地开发或调试。 |
| [codex remote-control](22-cli-command-reference.md#codex-remote-control) | `experimental` | 确保本地 app-server daemon 正在运行并启用了 remote-control 支持。 |
| [codex app](22-cli-command-reference.md#codex-app) | `stable` | 在 macOS 或 Windows 上启动 Codex desktop app。在 macOS 上，Codex 可以打开工作区路径；在 Windows 上，Codex 会打印要打开的路径。 |
| [codex debug app-server send-message-v2](22-cli-command-reference.md#codex-debug-app-server-send-message-v2) | `experimental` | 通过内置测试客户端发送单条 V2 消息来调试 app-server。 |
| [codex debug models](22-cli-command-reference.md#codex-debug-models) | `experimental` | 打印 Codex 看到的原始模型目录，并可选择只检查捆绑的模型目录。 |
| [codex apply](22-cli-command-reference.md#codex-apply) | `stable` | 将 Codex Cloud 任务生成的最新 diff 应用到你的本地工作树。别名：`codex a`。 |
| [codex archive](22-cli-command-reference.md#codex-archive-and-codex-unarchive) | `stable` | 按 session ID 或 session name 归档已保存的交互式会话。 |
| [codex cloud](22-cli-command-reference.md#codex-cloud) | `experimental` | 从终端浏览或执行 Codex Cloud 任务，而不打开 TUI。别名：`codex cloud-tasks`。 |
| [codex completion](22-cli-command-reference.md#codex-completion) | `stable` | 为 Bash、Zsh、Fish 或 PowerShell 生成 shell 补全脚本。 |
| [codex doctor](22-cli-command-reference.md#codex-doctor) | `stable` | 为本地安装、配置、身份验证、运行时、Git、终端、app-server 和线程清单问题生成诊断报告。 |
| [codex features](22-cli-command-reference.md#codex-features) | `stable` | 列出功能标志，并在 `config.toml` 中持久启用或禁用它们。 |
| [codex exec](22-cli-command-reference.md#codex-exec) | `stable` | 非交互式运行 Codex。别名：`codex e`。将结果流式输出到 stdout 或 JSONL，并可选择恢复之前的会话。 |
| [codex execpolicy](22-cli-command-reference.md#codex-execpolicy) | `experimental` | 评估 execpolicy 规则文件，并查看某个命令会被允许、提示还是阻止。 |
| [codex login](22-cli-command-reference.md#codex-login) | `stable` | 使用 ChatGPT OAuth、device auth、API key 或通过 stdin 管道传入的 access token 对 Codex 进行身份验证。 |
| [codex logout](22-cli-command-reference.md#codex-logout) | `stable` | 移除已存储的身份验证凭据。 |
| [codex mcp](22-cli-command-reference.md#codex-mcp) | `experimental` | 管理 Model Context Protocol 服务器（list、add、remove、authenticate）。 |
| [codex plugin marketplace](22-cli-command-reference.md#codex-plugin-marketplace) | `experimental` | 从 Git 或本地源 add、list、upgrade 或 remove plugin marketplace。 |
| [codex plugin](22-cli-command-reference.md#codex-plugin) | `experimental` | 从已配置 marketplace source 安装、列出和移除插件。 |
| [codex mcp-server](22-cli-command-reference.md#codex-mcp-server) | `experimental` | 通过 stdio 将 Codex 本身作为 MCP 服务器运行。当另一个智能体使用 Codex 时很有用。 |
| [codex resume](22-cli-command-reference.md#codex-resume) | `stable` | 按 ID 继续之前的交互式会话，或恢复最近的对话。 |
| [codex fork](22-cli-command-reference.md#codex-fork) | `stable` | 将之前的交互式会话 fork 为新线程，同时保留原始 transcript。 |
| [codex sandbox](22-cli-command-reference.md#codex-sandbox) | `experimental` | 在 Codex 提供的 macOS、Linux 或 Windows 沙盒中运行任意命令。 |
| [codex update](22-cli-command-reference.md#codex-update) | `stable` | 当已安装版本支持 self-update 时，检查并应用 Codex CLI update。 |
| [codex unarchive](22-cli-command-reference.md#codex-archive-and-codex-unarchive) | `stable` | 按 session ID 或 session name 恢复已归档的交互式会话。 |

### 命令详情

#### `codex`（交互式）

不带子命令运行 `codex` 会启动交互式终端 UI (TUI)。智能体接受上面的全局标志和图片附件。网页搜索默认使用 cached 模式；使用 `--search` 可切换到实时浏览。对于低摩擦本地工作，请使用 `--sandbox workspace-write --ask-for-approval on-request`。

使用 `--remote ws://host:port` 或 `--remote wss://host:port`，可将 TUI 连接到通过 `codex app-server --listen ws://IP:PORT` 启动的 app server。对于本地 Unix socket，使用 `--remote unix://` 表示默认 socket，或使用 `--remote unix://PATH` 表示显式路径。当服务器要求 bearer token 进行 WebSocket 身份验证时，添加 `--remote-auth-token-env <ENV_VAR>`。

#### `codex app-server`

在本地启动 Codex app server。它主要用于开发和调试，可能会在不另行通知的情况下变更。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--stdio` | `boolean` | `false` | 使用 stdio 传输。等同于 `--listen stdio://`，并且与 `--listen` 互斥。 |
| `--listen` | `stdio:// \| ws://IP:PORT \| unix:// \| unix://PATH \| off` | `stdio://` | 传输监听 URL。使用 `stdio://` 表示 JSONL，`ws://IP:PORT` 表示 TCP WebSocket endpoint，`unix://` 表示默认 Unix socket，`unix://PATH` 表示自定义 Unix socket，或使用 `off` 禁用本地 transport。 |
| `--ws-auth` | `capability-token \| signed-bearer-token` | `` | app-server WebSocket 客户端的身份验证模式。如果省略，则禁用 WebSocket auth；非本地监听器会在启动期间发出警告。 |
| `--ws-token-file` | `absolute path` | `` | 包含 shared capability token 的文件。与 `--ws-auth capability-token` 一起使用，除非你改为提供 `--ws-token-sha256`。 |
| `--ws-token-sha256` | `hexadecimal SHA-256 digest` | `` | capability-token 身份验证所预期的 SHA-256 digest。当 client token 来自其他来源时，用它代替 `--ws-token-file`。 |
| `--ws-shared-secret-file` | `absolute path` | `` | 包含用于验证 signed JWT bearer tokens 的 HMAC shared secret 的文件。与 `--ws-auth signed-bearer-token` 一起使用时必需。 |
| `--ws-issuer` | `string` | `` | signed bearer tokens 中预期的 `iss` claim。要求 `--ws-auth signed-bearer-token`。 |
| `--ws-audience` | `string` | `` | signed bearer tokens 中预期的 `aud` claim。要求 `--ws-auth signed-bearer-token`。 |
| `--ws-max-clock-skew-seconds` | `number` | `30` | 验证 signed bearer token `exp` 和 `nbf` claims 时允许的时钟偏差。要求 `--ws-auth signed-bearer-token`。 |
| `--analytics-default-enabled` | `boolean` | `false` | 除非用户在配置中选择退出，否则默认为第一方 app-server 客户端启用 analytics。 |

`codex app-server --listen stdio://` 会保持默认的 JSONL-over-stdio 行为，`codex app-server --stdio` 是该传输的别名。`--listen ws://IP:PORT` 会为 app-server 客户端启用 WebSocket 传输。服务器接受 `ws://` 监听 URL；当客户端使用 `wss://` 连接时，请使用 TLS 终止或安全代理。使用 `--listen unix://` 可在 Codex 默认 Unix socket 上接受 WebSocket 握手，或使用 `--listen unix:///absolute/path.sock` 选择 socket 路径。如果你为 client bindings 生成 schemas，请添加 `--experimental` 以包含受控字段和方法。

#### `codex remote-control`

确保 app-server daemon 正在运行并启用了 remote-control 支持。托管 remote-control 客户端和 SSH 远程工作流会使用此命令；当你构建本地协议 client 时，它不能替代 `codex app-server --listen`。

#### `codex app`

从 macOS 或 Windows 上的终端启动 Codex Desktop。在 macOS 上，Codex 可以打开特定工作区路径；在 Windows 上，Codex 会打印要打开的路径。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `PATH` | `path` | `.` | Codex Desktop 的工作区路径。在 macOS 上，Codex 打开此路径；在 Windows 上，Codex 打印该路径。 |
| `--download-url` | `url` | `` | Codex desktop installer URL 的高级覆盖，用于安装期间。 |

`codex app` 会打开已安装的 Codex Desktop app，或在缺少 app 时启动 installer。在 macOS 上，Codex 会打开提供的工作区路径；在 Windows 上，它会在安装后打印要打开的路径。

#### `codex debug app-server send-message-v2`

使用内置 app-server 测试 client，通过 app-server 的 V2 线程/轮次流程发送一条消息。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `USER_MESSAGE` | `string` | `` | 通过内置 V2 test-client flow 发送给 app-server 的消息文本。 |

此 debug flow 使用 `experimentalApi: true` 初始化，启动线程，发送轮次，并流式传输 server notifications。使用它可在本地复现和检查 app-server protocol 行为。

#### `codex debug models`

以 JSON 打印 Codex 看到的原始模型目录。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--bundled` | `boolean` | `false` | 跳过刷新，只打印当前 Codex binary 捆绑的模型目录。 |

当你只想检查当前 binary 捆绑的模型目录，而不从远程 models endpoint 刷新时，请使用 `--bundled`。

#### `codex apply`

将 Codex cloud task 中最新的 diff 应用到你的本地仓库。你必须完成身份验证并有权访问该 task。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `TASK_ID` | `string` | `` | 应应用其 diff 的 Codex Cloud task 标识符。 |

如果 `git apply` 失败（例如因为冲突），Codex 会打印已打补丁的文件并以非零状态退出。

#### `codex archive` 和 `codex unarchive`

按 session ID 或 session name 归档或恢复已保存的交互式会话。当你想清理 session picker 但不删除 transcript 时，请使用这些命令。Session IDs 优先于 session names。

```bash
codex archive <SESSION>
codex unarchive <SESSION>
```

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `SESSION` | `session ID \| session name` | `` | 要归档或恢复的已保存会话。Session IDs 优先于 session names。 |
| `--remote` | `ws://host:port \| wss://host:port \| unix:// \| unix://PATH` | `` | 更改 归档状态前连接到远程 app-server endpoint。 |
| `--remote-auth-token-env` | `ENV_VAR` | `` | 当 `--remote` 需要身份验证时，从此环境变量读取 bearer token。 |

#### `codex cloud`

从终端与 Codex Cloud 任务交互。默认命令会打开交互式选择器；`codex cloud exec` 会直接提交任务，`codex cloud list` 会返回最近任务，便于脚本或快速检查。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `QUERY` | `string` | `` | 任务提示词。如果省略，Codex 会以交互方式提示输入细节。 |
| `--env` | `ENV_ID` | `` | 目标 Codex Cloud environment 标识符（必需）。使用 `codex cloud` 列出选项。 |
| `--attempts` | `1-4` | `1` | Codex Cloud 应运行的 assistant 尝试次数 (best-of-N)。 |

身份验证使用与主 CLI 相同的凭据。如果 task submission 失败，Codex 会以非零状态退出。

##### `codex cloud list`

列出最近的 Cloud 任务，支持可选过滤和分页。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--env` | `ENV_ID` | `` | 按 environment identifier 过滤任务。 |
| `--limit` | `1-20` | `20` | 返回任务的最大数量。 |
| `--cursor` | `string` | `` | 上一次请求返回的分页 cursor。 |
| `--json` | `boolean` | `false` | 输出 机器可读 JSON，而不是 plain text。 |

纯文本输出会先打印 task URL，然后打印状态详情。使用 `--json` 进行自动化。JSON payload 包含一个 `tasks` 数组和一个可选 `cursor` 值。每个任务包含 `id`、`url`、`title`、`status`、`updated_at`、`environment_id`、`environment_label`、`summary`、`is_review` 和 `attempt_total`。

#### `codex completion`

生成 shell 补全脚本，并将输出重定向到适当位置，例如 `codex completion zsh > "${fpath[1]}/_codex"`。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `SHELL` | `bash \| zsh \| fish \| power-shell \| elvish` | `bash` | 要为其生成 completions 的 shell。输出打印到 stdout。 |

#### `codex doctor`

在提交支持问题前，或调查损坏的 Codex 安装时，生成本地诊断报告。报告会检查安装、配置、身份验证、运行时、Git、终端、app-server 和线程清单的健康状况。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--json` | `boolean` | `false` | 输出经过 脱敏的 机器可读支持报告。 |
| `--summary` | `boolean` | `false` | 仅显示分组检查行和最终计数摘要。 |
| `--all` | `boolean` | `false` | 展开详细人类可读报告中的长列表。 |
| `--no-color` | `boolean` | `false` | 在人类可读输出中禁用 ANSI color。 |
| `--ascii` | `boolean` | `false` | 在人类可读输出中使用 ASCII 状态标签和分隔符。 |

#### `codex features`

管理存储在 `$CODEX_HOME/config.toml` 中的功能标志。`enable` 和 `disable` 命令会持久化更改，使其应用到未来会话。`features` 子命令不接受 `--profile`。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `List subcommand` | `codex features list` | `` | 显示已知功能标志、其成熟度阶段和有效状态。 |
| `Enable subcommand` | `codex features enable <feature>` | `` | 在 `$CODEX_HOME/config.toml` 中持久启用功能标志。 |
| `Disable subcommand` | `codex features disable <feature>` | `` | 在 `$CODEX_HOME/config.toml` 中持久禁用功能标志。 |

#### `codex exec`

对于应在没有人工交互的情况下完成的脚本化或 CI 风格运行，请使用 `codex exec`（或短形式 `codex e`）。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `PROMPT` | `string \| - (read stdin)` | `` | 任务的初始指令。使用 `-` 可从 stdin 管道传入提示词。 |
| `--image, -i` | `path[,path...]` | `` | 将图片附加到第一条消息。可重复；支持逗号分隔列表。 |
| `--model, -m` | `string` | `` | 覆盖本次运行配置的模型。 |
| `--oss` | `boolean` | `false` | 使用本地开源提供商（需要正在运行的 Ollama 实例）。 |
| `--sandbox, -s` | `read-only \| workspace-write \| danger-full-access` | `` | 模型生成命令使用的沙箱策略。默认使用配置。 |
| `--profile, -p` | `string` | `` | 将 `$CODEX_HOME/profile-name.config.toml` 叠加到基础用户配置之上。 |
| `--full-auto` | `boolean` | `false` | 已弃用的兼容 flag。请优先使用 `--sandbox workspace-write`；使用此标志时 Codex 会打印警告。 |
| `--dangerously-bypass-approvals-and-sandbox, --yolo` | `boolean` | `false` | 绕过审批提示和沙箱。危险：只应在隔离 runner 中使用。 |
| `--dangerously-bypass-hook-trust` | `boolean` | `false` | 在本次调用中运行已启用 hooks，而不要求持久化钩子信任。仅适用于已经审查 hook 来源的自动化。 |
| `--cd, -C` | `path` | `` | 执行任务前设置 workspace root。 |
| `--skip-git-repo-check` | `boolean` | `false` | 允许在 Git 仓库之外运行（适合一次性目录）。 |
| `--ephemeral` | `boolean` | `false` | 运行时不将 session rollout files 持久化到磁盘。 |
| `--ignore-user-config` | `boolean` | `false` | 不要加载 `$CODEX_HOME/config.toml`。身份验证仍使用 `CODEX_HOME`。 |
| `--ignore-rules` | `boolean` | `false` | 本次运行不加载用户或项目 execpolicy `.rules` 文件。 |
| `--output-schema` | `path` | `` | 描述预期最终响应形状的 JSON Schema 文件。Codex 会按它验证工具输出。 |
| `--color` | `always \| never \| auto` | `auto` | 控制 stdout 中的 ANSI color。 |
| `--json, --experimental-json` | `boolean` | `false` | 打印 newline-delimited JSON 事件，而不是格式化文本。 |
| `--output-last-message, -o` | `path` | `` | 将 assistant 的最终消息写入文件。适合下游脚本使用。 |
| `Resume subcommand` | `codex exec resume [SESSION_ID]` | `` | 按 ID 恢复 exec session，或添加 `--last` 继续当前工作目录中最近的会话。添加 `--all` 可考虑任意目录中的会话。接受可选后续提示词。 |
| `-c, --config` | `key=value` | `` | 非交互式运行的内联配置覆盖（可重复）。 |

Codex 默认写入格式化输出。添加 `--json` 可接收 newline-delimited JSON 事件（每次状态变化一个）。可选的 `resume` 子命令可继续非交互式任务。使用 `--last` 选择当前工作目录中最近的会话，或添加 `--all` 跨所有会话搜索：

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `SESSION_ID` | `uuid` | `` | 恢复指定会话。省略时使用 `--last` 继续最近的会话。 |
| `--last` | `boolean` | `false` | 恢复当前工作目录中最近的对话。 |
| `--all` | `boolean` | `false` | 选择最近会话时包含当前工作目录之外的会话。 |
| `--image, -i` | `path[,path...]` | `` | 将一个或多个图片附加到后续提示词。多个路径可用逗号分隔，也可重复该标志。 |
| `PROMPT` | `string \| - (read stdin)` | `` | 恢复后立即发送的可选后续指令。 |

#### `codex execpolicy`

保存 `execpolicy` rule files 前，可先检查它们。`codex execpolicy check` 接受一个或多个 `--rules` 标志（例如 `~/.codex/rules` 下的文件），并输出 JSON，显示最严格的 decision 和所有匹配 rules。添加 `--pretty` 可格式化输出。`execpolicy` 命令当前处于 preview。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--rules, -r` | `path (repeatable)` | `` | 要评估的 execpolicy rule file 路径。可提供多个 flag 以组合多个文件中的规则。 |
| `--pretty` | `boolean` | `false` | 美化打印 JSON 结果。 |
| `COMMAND...` | `var-args` | `` | 要按指定策略检查的命令。 |

#### `codex login`

使用 ChatGPT 账号、API key 或 access token 对 CLI 进行身份验证。不带标志时，Codex 会打开浏览器执行 ChatGPT OAuth flow。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--with-api-key` | `boolean` | `` | 从 stdin 读取 API key（例如 `printenv OPENAI_API_KEY \| codex login --with-api-key`）。 |
| `--with-access-token` | `boolean` | `` | 从 stdin 读取 access token（例如 `printenv CODEX_ACCESS_TOKEN \| codex login --with-access-token`）。 |
| `--device-auth` | `boolean` | `` | 使用 OAuth device code flow，而不是启动浏览器窗口。 |
| `status subcommand` | `codex login status` | `` | 打印当前身份验证模式；已登录时以 0 退出。 |

当存在凭据时，`codex login status` 会以 `0` 退出，这对自动化脚本很有用。

#### `codex logout`

移除 API key 和 ChatGPT 身份验证的已保存凭据。此命令没有标志。

#### `codex mcp`

管理存储在 `~/.codex/config.toml` 中的 Model Context Protocol 服务器条目。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `list` | `--json` | `` | 列出已配置 MCP 服务器。添加 `--json` 可输出 机器可读内容。 |
| `get <name>` | `--json` | `` | 显示特定服务器配置。`--json` 会打印原始配置条目。 |
| `add <name>` | `-- <command...> \| --url <value>` | `` | 用 stdio 启动命令或 streamable HTTP URL 注册 server。支持为 stdio 传输设置 `--env KEY=VALUE`。 |
| `remove <name>` | `` | `` | 删除已存储的 MCP 服务器定义。 |
| `login <name>` | `--scopes scope1,scope2` | `` | 为 streamable HTTP server 启动 OAuth 登录（仅限支持 OAuth 的 server）。 |
| `logout <name>` | `` | `` | 移除 streamable HTTP server 的已存储 OAuth 凭据。 |

`add` 子命令同时支持 stdio 和 streamable HTTP transports：

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `COMMAND...` | `stdio transport` | `` | 用于启动 MCP 服务器的可执行文件和参数。放在 `--` 之后提供。 |
| `--env KEY=VALUE` | `repeatable` | `` | 启动 stdio server 时应用的环境变量赋值。 |
| `--url` | `https://…` | `` | 注册 streamable HTTP server，而不是 stdio。与 `COMMAND...` 互斥。 |
| `--bearer-token-env-var` | `ENV_VAR` | `` | 连接到 streamable HTTP server 时，作为 bearer token 发送的环境变量值。 |
| `--oauth-client-id` | `CLIENT_ID` | `` | streamable HTTP MCP 服务器的 OAuth client identifier。要求 `--url`。 |
| `--oauth-resource` | `RESOURCE` | `` | streamable HTTP MCP 服务器登录期间要包含的 OAuth resource 参数。要求 `--url`。 |

OAuth 操作（`login`、`logout`）只适用于 streamable HTTP 服务器（并且只有在 server 支持 OAuth 时才可用）。

#### `codex plugin`

从已配置 marketplace 安装、列出和移除插件。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `add <plugin[@marketplace]>` | `[--marketplace, -m NAME] [--json]` | `` | 从已配置 marketplace 安装插件。当 plugin 参数省略 `@marketplace` 时，使用 `--marketplace` 或 `-m`。 |
| `list` | `[--marketplace, -m NAME] [--available --json] [--json]` | `` | 列出已安装插件。使用 `--json` 时，输出包含 `installed` 和 `available` 数组；`--available` 会包含未安装的 marketplace 插件，并且要求 `--json`。 |
| `remove <plugin[@marketplace]>` | `[--marketplace, -m NAME] [--json]` | `` | 从本地 config 和 cache 移除已安装插件。使用 `--json` 可获得适合自动化的输出。 |
| `marketplace` | `` | `` | 管理已配置 marketplace sources。见下方 `codex plugin marketplace`。 |

`codex plugin add --json` 会打印 `pluginId`、`name`、`marketplaceName`、`version`、`installedPath` 和 `authPolicy`。`codex plugin list --json` 会打印 `installed` 和 `available` 数组。条目包含 `pluginId`、`name`、`marketplaceName`、`version`、`installed`、`enabled`、`source`、`installPolicy`、`authPolicy`，并在可用时包含带有已配置 marketplace source type 和 value 的 `marketplaceSource`。`codex plugin remove --json` 会打印 `pluginId`、`name` 和 `marketplaceName`。

#### `codex plugin marketplace`

管理 Codex 可浏览和安装的 plugin marketplace sources。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `add <source>` | `[--ref REF] [--sparse PATH] [--json]` | `` | 从 GitHub shorthand、Git URL、SSH URL 或本地 marketplace 根目录安装 plugin marketplace。`--sparse` 仅支持 Git sources，并且可重复。 |
| `list` | `[--json]` | `` | 显示 Codex 当前考虑的 plugin marketplace，以及每个 marketplace 的 root path。 |
| `upgrade [marketplace-name]` | `[--json]` | `` | 刷新一个已配置 Git marketplace；未提供名称时刷新所有已配置 Git marketplace。 |
| `remove <marketplace-name>` | `[--json]` | `` | 移除已配置的 plugin marketplace。 |

`codex plugin marketplace add` 接受 `owner/repo` 或 `owner/repo@ref` 等 GitHub shorthand、HTTP 或 HTTPS Git URLs、SSH Git URLs，以及本地 marketplace 根目录。使用 `--ref` 固定 Git ref，并重复 `--sparse PATH` 为 Git-backed marketplace 仓库使用 sparse checkout。

`codex plugin marketplace list` 会打印范围内 marketplace 名称和 roots，包括隐式发现的默认 marketplace 以及已配置 marketplace 快照。

为 marketplace add、list、upgrade 或 remove 命令添加 `--json`，可获得适合自动化的输出。Marketplace add JSON 包含 `marketplaceName`、`installedRoot` 和 `alreadyAdded`；list JSON 包含一个 `marketplaces` 数组，带有 `name`、`root` 和可选 `marketplaceSource`；upgrade JSON 包含 `selectedMarketplaces`、`upgradedRoots` 和 `errors`；remove JSON 包含 `marketplaceName` 和 `installedRoot`。

#### `codex mcp-server`

通过 stdio 将 Codex 作为 MCP 服务器运行，以便其他工具连接。此命令会继承全局配置覆盖，并在下游 client 关闭连接时退出。

#### `codex resume`

按 ID 继续交互式会话，或恢复最近的对话。除非传入 `--all`，否则 `codex resume` 会将 `--last` 限定在当前工作目录。它接受与 `codex` 相同的全局标志，包括模型和沙箱覆盖。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `SESSION_ID` | `uuid` | `` | 恢复指定会话。省略时使用 `--last` 继续最近的会话。 |
| `--last` | `boolean` | `false` | 跳过选择器，并恢复当前工作目录中最近的对话。 |
| `--all` | `boolean` | `false` | 选择最近会话时包含当前工作目录之外的会话。 |

#### `codex fork`

将之前的交互式会话 fork 为新线程。默认情况下，`codex fork` 会打开 session picker；添加 `--last` 可改为 fork 最近的会话。

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `SESSION_ID` | `uuid` | `` | Fork 指定会话。省略时使用 `--last` fork 最近的会话。 |
| `--last` | `boolean` | `false` | 跳过选择器并自动 fork 最近的对话。 |
| `--all` | `boolean` | `false` | 在选择器中显示当前工作目录之外的会话。 |

#### `codex sandbox`

使用 sandbox helper，以 Codex 内部使用的相同策略运行命令。

##### macOS seatbelt

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--profile, -p` | `NAME` | `` | 将 `$CODEX_HOME/NAME.config.toml` 叠加到基础用户配置之上。 |
| `--permissions-profile, -P` | `NAME` | `` | 从活动配置栈应用命名权限配置档。 |
| `--cd, -C` | `DIR` | `` | 用于配置档解析和命令执行的工作目录。要求 `--permissions-profile`。 |
| `--include-managed-config` | `boolean` | `false` | 解析显式权限配置档时包含 managed requirements。要求 `--permissions-profile`。 |
| `--allow-unix-socket` | `path` | `` | 允许沙箱化命令绑定或连接以此路径为根的 Unix sockets。可重复以允许多个路径。 |
| `--log-denials` | `boolean` | `false` | 命令运行时用 `log stream` 捕获 macOS 沙箱拒绝记录，并在退出后打印。 |
| `--config, -c` | `key=value` | `` | 向沙箱化运行传入配置覆盖（可重复）。 |
| `COMMAND...` | `var-args` | `` | 在 macOS Seatbelt 下执行的 shell 命令。`--` 之后的所有内容都会转发。 |

##### Linux Landlock

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--profile, -p` | `NAME` | `` | 将 `$CODEX_HOME/NAME.config.toml` 叠加到基础用户配置之上。 |
| `--permissions-profile, -P` | `NAME` | `` | 从活动配置栈应用命名权限配置档。 |
| `--cd, -C` | `DIR` | `` | 用于配置档解析和命令执行的工作目录。要求 `--permissions-profile`。 |
| `--include-managed-config` | `boolean` | `false` | 解析显式权限配置档时包含 managed requirements。要求 `--permissions-profile`。 |
| `--config, -c` | `key=value` | `` | 启动沙箱前应用的配置覆盖（可重复）。 |
| `COMMAND...` | `var-args` | `` | 在 Landlock + seccomp 下执行的命令。可执行文件请放在 `--` 之后。 |

##### Windows

| 键 | 类型/取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--profile, -p` | `NAME` | `` | 将 `$CODEX_HOME/NAME.config.toml` 叠加到基础用户配置之上。 |
| `--permissions-profile, -P` | `NAME` | `` | 从活动配置栈应用命名权限配置档。 |
| `--cd, -C` | `DIR` | `` | 用于配置档解析和命令执行的工作目录。要求 `--permissions-profile`。 |
| `--include-managed-config` | `boolean` | `false` | 解析显式权限配置档时包含 managed requirements。要求 `--permissions-profile`。 |
| `--config, -c` | `key=value` | `` | 启动沙箱前应用的配置覆盖（可重复）。 |
| `COMMAND...` | `var-args` | `` | 在原生 Windows 沙箱下执行的命令。可执行文件请放在 `--` 之后。 |

#### `codex update`

当已安装 release 支持 self-update 时，检查并应用 Codex CLI update。Debug builds 会打印消息，提示你改为安装 release build。

### Flag 组合与安全提示

- 对于可以留在 workspace 内的无人值守本地工作，请使用 `--sandbox workspace-write`；除非你在专用 sandbox VM 中，否则避免使用 `--dangerously-bypass-approvals-and-sandbox`。
- 当需要授予 Codex 对更多目录的写入访问权限时，请优先使用 `--add-dir`，而不是强制使用 `--sandbox danger-full-access`。
- 在 CI 中将 `--json` 与 `--output-last-message` 搭配使用，以捕获机器可读进度和最终自然语言摘要。

### 相关资源

- [Codex CLI 概览](45-codex-cli.md)：安装、升级和快速提示。
- [配置基础](19-config-basics.md)：持久化模型和提供商等默认值。
- [高级配置](17-advanced-configuration.md)：配置档、提供商、沙箱调优和集成。
- [AGENTS.md](50-custom-instructions-with-agents-md.md)：Codex 智能体能力和最佳实践的概念性概览。
