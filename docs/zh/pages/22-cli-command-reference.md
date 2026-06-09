### CLI 命令参考

Source: [Command line options](https://developers.openai.com/codex/cli/reference.md)

#### 如何阅读本参考

本页列出每个已记录的 Codex CLI 命令和标志。使用交互式表格按键或说明搜索。每个部分都会指出该选项是 stable 还是 experimental，并标出有风险的组合。

CLI 会从 `~/.codex/config.toml` 继承大多数默认值。你在命令行传入的任何 `-c key=value` 覆盖都会在该次调用中优先。更多信息请参阅 [Config basics](https://developers.openai.com/codex/config-basic#configuration-precedence)。

#### 全局标志

| Key                                                  | Type / Values                                                 | Default | Details                                                                                                                                                                                                           |
| ---------------------------------------------------- | ------------------------------------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--add-dir`                                          | `path`                                                        |         | 在主工作区之外授予其它目录写入访问权限。可重复指定多个路径。                                                                                                                |
| `--ask-for-approval, -a`                             | `untrusted \| on-request \| never`                            |         | 控制 Codex 在运行命令前何时暂停请求人工审批。`on-failure` 已弃用；交互式运行优先使用 `on-request`，非交互式运行优先使用 `never`。                                  |
| `--cd, -C`                                           | `path`                                                        |         | 在智能体开始处理你的请求前设置工作目录。                                                                                                                                 |
| `--config, -c`                                       | `key=value`                                                   |         | 覆盖配置值。值会尽可能按 TOML 解析；否则使用字面字符串。                                                                                                            |
| `--dangerously-bypass-approvals-and-sandbox, --yolo` | `boolean`                                                     | `false` | 在没有审批或沙盒的情况下运行每个命令。仅在外部已加固的环境中使用。                                                                                                            |
| `--dangerously-bypass-hook-trust`                    | `boolean`                                                     | `false` | 在本次调用中运行已启用 hooks，而不要求持久化 hook trust。仅适用于已经审查 hook 来源的自动化。                                                                        |
| `--disable`                                          | `feature`                                                     |         | 强制禁用 feature flag（转换为 `-c features.=false`）。可重复。                                                                                                                                    |
| `--enable`                                           | `feature`                                                     |         | 强制启用 feature flag（转换为 `-c features.=true`）。可重复。                                                                                                                                      |
| `--image, -i`                                        | `path[,path...]`                                              |         | 将一个或多个图像文件附加到初始提示词。多个路径可用逗号分隔，也可重复该标志。                                                                                                      |
| `--model, -m`                                        | `string`                                                      |         | 覆盖配置中设置的模型（例如 `gpt-5.4`）。                                                                                                                                                  |
| `--no-alt-screen`                                    | `boolean`                                                     | `false` | 禁用 TUI 的 alternate screen mode（覆盖本次运行的 `tui.alternate_screen`）。                                                                                                                        |
| `--oss`                                              | `boolean`                                                     | `false` | 使用本地开源模型提供商（等同于 `-c model_provider="oss"`）。会验证 Ollama 正在运行。                                                                                             |
| `--profile, -p`                                      | `string`                                                      |         | 将 `$CODEX_HOME/profile-name.config.toml` 叠加到基础用户配置之上。                                                                                                                                |
| `--remote`                                           | `ws://host:port \| wss://host:port \| unix:// \| unix://PATH` |         | 通过 WebSocket 或 Unix socket 将交互式 TUI 连接到远程 app-server endpoint。支持 `codex`、`codex resume` 和 `codex fork`；其它子命令会拒绝 remote mode。                       |
| `--remote-auth-token-env`                            | `ENV_VAR`                                                     |         | 从此环境变量读取 bearer token，并在使用 `--remote` 连接时发送。要求 `--remote`；token 只会通过 `wss://` URL 或仅本地的 `ws://` URL 发送。                           |
| `--sandbox, -s`                                      | `read-only \| workspace-write \| danger-full-access`          |         | 为模型生成的 shell 命令选择沙盒策略。                                                                                                                                                           |
| `--search`                                           | `boolean`                                                     | `false` | 启用 live web search（将 `web_search = "live"` 设为默认值，而不是默认的 `"cached"`）。                                                                                                                            |
| `--strict-config`                                    | `boolean`                                                     | `false` | 当 `config.toml` 包含此 Codex 版本无法识别的字段时报错。由 `codex`、`exec`、`review`、`resume`、`fork`、`app-server`、`mcp-server` 和 `exec-server` 等运行时命令支持。 |
| `PROMPT`                                             | `string`                                                      |         | 用于启动会话的可选文本指令。省略则启动没有预填消息的 TUI。                                                                                                              |

这些选项适用于基础 `codex` 命令。大多数会传播到其它命令；例外请参阅上面的说明或相关命令帮助。对于传播的标志，请遵循相关命令帮助。例如，`codex exec --oss ...` 会将 `--oss` 应用于 `exec`。

#### 命令概览

Maturity 列使用 Experimental、Beta 和 Stable 等功能成熟度标签。请参阅 [Feature Maturity](https://developers.openai.com/codex/feature-maturity) 了解如何解释这些标签。

| Key                                                                                                     | Maturity       | Default | Details                                                                                                                                 |
| ------------------------------------------------------------------------------------------------------- | -------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| [`codex`](https://developers.openai.com/codex/cli/reference#codex-interactive)                                                       | `stable`       |         | 启动 terminal UI。接受上面的全局标志，以及可选提示词或图像附件。                                    |
| [`codex app`](https://developers.openai.com/codex/cli/reference#codex-app)                                                           | `stable`       |         | 在 macOS 或 Windows 上启动 Codex desktop app。在 macOS 上，Codex 可以打开工作区路径；在 Windows 上，Codex 会打印要打开的路径。 |
| [`codex app-server`](https://developers.openai.com/codex/cli/reference#codex-app-server)                                             | `experimental` |         | 启动 Codex app server，用于通过 stdio、WebSocket 或 Unix socket 进行本地开发或调试。                                 |
| [`codex apply`](https://developers.openai.com/codex/cli/reference#codex-apply)                                                       | `stable`       |         | 将 Codex Cloud task 生成的最新 diff 应用到你的本地 working tree。Alias：`codex a`。                                     |
| [`codex cloud`](https://developers.openai.com/codex/cli/reference#codex-cloud)                                                       | `experimental` |         | 从终端浏览或执行 Codex Cloud tasks，而不打开 TUI。Alias：`codex cloud-tasks`。                              |
| [`codex completion`](https://developers.openai.com/codex/cli/reference#codex-completion)                                             | `stable`       |         | 为 Bash、Zsh、Fish 或 PowerShell 生成 shell completion scripts。                                                                   |
| [`codex debug app-server send-message-v2`](https://developers.openai.com/codex/cli/reference#codex-debug-app-server-send-message-v2) | `experimental` |         | 通过内置 test client 发送单条 V2 message 来调试 app-server。                                                       |
| [`codex debug models`](https://developers.openai.com/codex/cli/reference#codex-debug-models)                                         | `experimental` |         | 打印 Codex 看到的原始 model catalog，包括只检查捆绑 catalog 的选项。                                        |
| [`codex doctor`](https://developers.openai.com/codex/cli/reference#codex-doctor)                                                     | `stable`       |         | 为本地安装、配置、身份验证、运行时、Git、终端、app-server 和线程清单问题生成诊断报告。                 |
| [`codex exec`](https://developers.openai.com/codex/cli/reference#codex-exec)                                                         | `stable`       |         | 非交互式运行 Codex。Alias：`codex e`。将结果流式输出到 stdout 或 JSONL，并可选择恢复之前的会话。               |
| [`codex execpolicy`](https://developers.openai.com/codex/cli/reference#codex-execpolicy)                                             | `experimental` |         | 评估 execpolicy rule files，并查看某个命令会被允许、提示还是阻止。                                        |
| [`codex features`](https://developers.openai.com/codex/cli/reference#codex-features)                                                 | `stable`       |         | 列出 feature flags，并在 `config.toml` 中持久启用或禁用它们。                                                            |
| [`codex fork`](https://developers.openai.com/codex/cli/reference#codex-fork)                                                         | `stable`       |         | 将之前的交互式会话 fork 为新的线程，同时保留原 transcript。                                              |
| [`codex login`](https://developers.openai.com/codex/cli/reference#codex-login)                                                       | `stable`       |         | 使用 ChatGPT OAuth、device auth、API key 或通过 stdin 管道传入的 access token 对 Codex 进行身份验证。                                   |
| [`codex logout`](https://developers.openai.com/codex/cli/reference#codex-logout)                                                     | `stable`       |         | 移除已存储的身份验证凭据。                                                                                               |
| [`codex mcp`](https://developers.openai.com/codex/cli/reference#codex-mcp)                                                           | `experimental` |         | 管理 Model Context Protocol servers（list、add、remove、authenticate）。                                                                |
| [`codex mcp-server`](https://developers.openai.com/codex/cli/reference#codex-mcp-server)                                             | `experimental` |         | 通过 stdio 将 Codex 本身作为 MCP server 运行。当另一个 agent 使用 Codex 时很有用。                                                 |
| [`codex plugin marketplace`](https://developers.openai.com/codex/cli/reference#codex-plugin-marketplace)                             | `experimental` |         | 从 Git 或本地源 add、list、upgrade 或 remove plugin marketplaces。                                                            |
| [`codex remote-control`](https://developers.openai.com/codex/cli/reference#codex-remote-control)                                     | `experimental` |         | 确保本地 app-server daemon 正在运行并启用了 remote-control 支持。                                                      |
| [`codex resume`](https://developers.openai.com/codex/cli/reference#codex-resume)                                                     | `stable`       |         | 按 ID 继续之前的交互式会话，或恢复最近的对话。                                                   |
| [`codex sandbox`](https://developers.openai.com/codex/cli/reference#codex-sandbox)                                                   | `experimental` |         | 在 Codex 提供的 macOS、Linux 或 Windows 沙盒中运行任意命令。                                                        |
| [`codex update`](https://developers.openai.com/codex/cli/reference#codex-update)                                                     | `stable`       |         | 当已安装版本支持 self-update 时，检查并应用 Codex CLI update。                                                 |

#### 命令详情

#### `codex` (interactive)

不带子命令运行 `codex` 会启动交互式终端 UI (TUI)。智能体接受上面的全局标志和图像附件。Web search 默认使用 cached mode；使用 `--search` 切换到实时浏览。对于低摩擦本地工作，请使用 `--sandbox workspace-write --ask-for-approval on-request`。

使用 `--remote ws://host:port` 或 `--remote wss://host:port` 将 TUI 连接到通过 `codex app-server --listen ws://IP:PORT` 启动的 app server。对于本地 Unix socket，使用 `--remote unix://` 表示默认 socket，或使用 `--remote unix://PATH` 表示显式路径。当服务器要求 bearer token 进行 WebSocket 身份验证时，添加 `--remote-auth-token-env <ENV_VAR>`。

#### `codex app-server`

在本地启动 Codex app server。这主要用于开发和调试，可能会在不另行通知的情况下更改。

| Key                           | Type / Values                                               | Default    | Details                                                                                                                                                                                                                |
| ----------------------------- | ----------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--analytics-default-enabled` | `boolean`                                                   | `false`    | 除非用户在配置中 opt out，否则默认为 first-party app-server clients 启用 analytics。                                                                                                                   |
| `--listen`                    | `stdio:// \| ws://IP:PORT \| unix:// \| unix://PATH \| off` | `stdio://` | Transport listener URL。使用 `stdio://` 表示 JSONL，`ws://IP:PORT` 表示 TCP WebSocket endpoint，`unix://` 表示默认 Unix socket，`unix://PATH` 表示自定义 Unix socket，或使用 `off` 禁用本地 transport。 |
| `--ws-audience`               | `string`                                                    |            | signed bearer token 中预期的 `aud` claim。要求 `--ws-auth signed-bearer-token`。                                                                                                                               |
| `--ws-auth`                   | `capability-token \| signed-bearer-token`                   |            | app-server WebSocket client 的身份验证模式。如果省略，则禁用 WebSocket auth；非本地 listener 会在启动期间发出警告。                                                                                 |
| `--ws-issuer`                 | `string`                                                    |            | signed bearer token 中预期的 `iss` claim。要求 `--ws-auth signed-bearer-token`。                                                                                                                               |
| `--ws-max-clock-skew-seconds` | `number`                                                    | `30`       | 验证 signed bearer token `exp` 和 `nbf` claim 时允许的 clock skew。要求 `--ws-auth signed-bearer-token`。                                                                                             |
| `--ws-shared-secret-file`     | `absolute path`                                             |            | 包含用于验证 signed JWT bearer token 的 HMAC shared secret 的文件。与 `--ws-auth signed-bearer-token` 一起使用时必需。                                                                                       |
| `--ws-token-file`             | `absolute path`                                             |            | 包含 shared capability token 的文件。与 `--ws-auth capability-token` 一起使用，除非你改为提供 `--ws-token-sha256`。                                                                                     |
| `--ws-token-sha256`           | `hexadecimal SHA-256 digest`                                |            | capability-token 身份验证所预期的 SHA-256 digest。当 client token 来自其它来源时，用它代替 `--ws-token-file`。                                                                         |

`codex app-server --listen stdio://` 保持默认的 JSONL-over-stdio 行为。`--listen ws://IP:PORT` 为 app-server clients 启用 WebSocket transport。服务器接受 `ws://` listen URLs；当 clients 使用 `wss://` 连接时，请使用 TLS termination 或安全代理。使用 `--listen unix://` 在 Codex 默认 Unix socket 上接受 WebSocket handshakes，或使用 `--listen unix:///absolute/path.sock` 选择 socket path。如果你为 client bindings 生成 schemas，请添加 `--experimental` 以包含 gated fields 和 methods。

#### `codex remote-control`

确保 app-server daemon 正在运行并启用了 remote-control 支持。托管 remote-control client 和 SSH 远程工作流使用此命令；当你构建本地协议 client 时，它不能替代 `codex app-server --listen`。

#### `codex app`

从 macOS 或 Windows 上的终端启动 Codex Desktop。在 macOS 上，Codex 可以打开特定工作区路径；在 Windows 上，Codex 会打印要打开的路径。

| Key              | Type / Values | Default | Details                                                                                               |
| ---------------- | ------------- | ------- | ----------------------------------------------------------------------------------------------------- |
| `--download-url` | `url`         |         | Codex desktop installer URL 的高级覆盖，用于安装期间。                            |
| `PATH`           | `path`        | `.`     | Codex Desktop 的工作区路径。在 macOS 上，Codex 打开此路径；在 Windows 上，Codex 打印该路径。 |

`codex app` 会打开已安装的 Codex Desktop app，或在缺少 app 时启动 installer。在 macOS 上，Codex 打开提供的工作区路径；在 Windows 上，它会在安装后打印要打开的路径。

#### `codex debug app-server send-message-v2`

使用内置 app-server test client，通过 app-server 的 V2 线程/轮次流程发送一条消息。

| Key            | Type / Values | Default | Details                                                                   |
| -------------- | ------------- | ------- | ------------------------------------------------------------------------- |
| `USER_MESSAGE` | `string`      |         | 通过内置 V2 test-client flow 发送给 app-server 的消息文本。 |

此 debug flow 使用 `experimentalApi: true` 初始化，启动线程，发送轮次，并流式传输 server notifications。使用它在本地复现和检查 app-server protocol 行为。

#### `codex debug models`

以 JSON 打印 Codex 看到的原始 model catalog。

| Key         | Type / Values | Default | Details                                                                              |
| ----------- | ------------- | ------- | ------------------------------------------------------------------------------------ |
| `--bundled` | `boolean`     | `false` | 跳过刷新，只打印当前 Codex binary 捆绑的 model catalog。 |

当你只想检查当前 binary 捆绑的 catalog，而不从远程 models endpoint 刷新时，请使用 `--bundled`。

#### `codex apply`

将 Codex cloud task 中最新的 diff 应用到你的本地仓库。你必须完成身份验证并有权访问该 task。

| Key       | Type / Values | Default | Details                                                          |
| --------- | ------------- | ------- | ---------------------------------------------------------------- |
| `TASK_ID` | `string`      |         | 应用其 diff 的 Codex Cloud task 标识符。 |

如果 `git apply` 失败（例如由于冲突），Codex 会打印已 patch 的文件并以非零状态退出。

#### `codex cloud`

从终端与 Codex cloud tasks 交互。默认命令会打开交互式选择器；`codex cloud exec` 直接提交 task，`codex cloud list` 返回最近 tasks，便于脚本或快速检查。

| Key          | Type / Values | Default | Details                                                                                  |
| ------------ | ------------- | ------- | ---------------------------------------------------------------------------------------- |
| `--attempts` | `1-4`         | `1`     | Codex Cloud 应运行的 assistant attempts 数量 (best-of-N)。                         |
| `--env`      | `ENV_ID`      |         | 目标 Codex Cloud environment 标识符（必需）。使用 `codex cloud` 列出选项。 |
| `QUERY`      | `string`      |         | 任务提示词。如果省略，Codex 会以交互方式提示输入细节。                        |

身份验证遵循与主 CLI 相同的凭据。如果 task submission 失败，Codex 会以非零状态退出。

#### `codex cloud list`

列出最近 cloud tasks，支持可选过滤和分页。

| Key        | Type / Values | Default | Details                                           |
| ---------- | ------------- | ------- | ------------------------------------------------- |
| `--cursor` | `string`      |         | 上一次请求返回的 pagination cursor。 |
| `--env`    | `ENV_ID`      |         | 按环境标识符过滤 tasks。             |
| `--json`   | `boolean`     | `false` | 输出机器可读 JSON，而不是 plain text。 |
| `--limit`  | `1-20`        | `20`    | 返回 tasks 的最大数量。              |

Plain-text 输出会先打印 task URL，然后打印状态详情。使用 `--json` 进行自动化。JSON payload 包含一个 `tasks` 数组和一个可选 `cursor` 值。每个 task 包含 `id`、`url`、`title`、`status`、`updated_at`、`environment_id`、`environment_label`、`summary`、`is_review` 和 `attempt_total`。

#### `codex completion`

生成 shell completion scripts，并将输出重定向到适当位置，例如 `codex completion zsh > "${fpath[1]}/_codex"`。

| Key     | Type / Values                                  | Default | Details                                                     |
| ------- | ---------------------------------------------- | ------- | ----------------------------------------------------------- |
| `SHELL` | `bash \| zsh \| fish \| power-shell \| elvish` | `bash`  | 要为其生成 completions 的 shell。输出打印到 stdout。 |

#### `codex doctor`

在提交支持问题前，或调查损坏的 Codex 安装时，生成本地诊断报告。报告会检查安装、配置、身份验证、运行时、Git、终端、app-server 和线程清单的健康状况。

| Key          | Type / Values | Default | Details                                                          |
| ------------ | ------------- | ------- | ---------------------------------------------------------------- |
| `--all`      | `boolean`     | `false` | 展开详细 human-readable report 中的长列表。         |
| `--ascii`    | `boolean`     | `false` | 在 human-readable output 中使用 ASCII 状态标签和分隔符。 |
| `--json`     | `boolean`     | `false` | 输出经过 redact 的 machine-readable support report。                 |
| `--no-color` | `boolean`     | `false` | 在 human-readable output 中禁用 ANSI color。                     |
| `--summary`  | `boolean`     | `false` | 仅显示分组 check rows 和最终 count summary。        |

#### `codex features`

管理存储在 `$CODEX_HOME/config.toml` 中的 feature flags。`enable` 和 `disable` 命令会持久化更改，使其应用到未来会话。`features` 子命令不接受 `--profile`。

| Key                  | Type / Values             | Default | Details                                                                    |
| -------------------- | ------------------------- | ------- | -------------------------------------------------------------------------- |
| `Disable subcommand` | `codex features disable ` |         | 在 `$CODEX_HOME/config.toml` 中持久禁用 feature flag。          |
| `Enable subcommand`  | `codex features enable `  |         | 在 `$CODEX_HOME/config.toml` 中持久启用 feature flag。           |
| `List subcommand`    | `codex features list`     |         | 显示已知 feature flags、其成熟度阶段和有效状态。               |
