### Codex CLI 功能

Source: [Codex CLI features](https://developers.openai.com/codex/cli/features.md)

Codex 支持聊天之外的工作流。使用本指南了解每项能力能解锁什么，以及何时使用。

#### 以交互模式运行 { #running-in-interactive-mode }

Codex 会启动一个全屏终端 UI，可以读取你的仓库、进行编辑，并在你们一起迭代时运行命令。当你想要一种对话式工作流，并希望实时审查 Codex 的操作时，请使用它。

```bash
codex
```

你也可以在命令行指定初始提示。

```bash
codex "Explain this codebase to me"
```

会话打开后，你可以：

- 将提示、代码片段或截图（参见 [图片输入](#image-inputs)）直接发送到输入区。
- 在 Codex 做出更改前观看它解释计划，并以内联方式批准或拒绝步骤。
- 在 TUI 中阅读带语法高亮的 Markdown 代码块和 diff，然后使用 `/theme` 预览并保存偏好的主题。
- 使用 `/clear` 清空终端并开始新的聊天，或按 <kbd>Ctrl</kbd>+<kbd>L</kbd> 清屏但不开始新对话。
- 使用 `/copy` 或按 <kbd>Ctrl</kbd>+<kbd>O</kbd> 复制最近完成的 Codex 输出。如果某一轮仍在运行，Codex 会复制最近完成的输出，而不是进行中的文本。
- 在 Codex 运行时按 <kbd>Tab</kbd>，将后续文本、斜杠命令或 `!` shell 命令排队到下一轮。
- 在输入区中用 <kbd>Up</kbd>/<kbd>Down</kbd> 浏览草稿历史；Codex 会恢复之前的草稿文本和图片占位符。
- 在输入区中按 <kbd>Ctrl</kbd>+<kbd>R</kbd> 搜索提示历史，然后按 <kbd>Enter</kbd> 接受匹配项，或按 <kbd>Esc</kbd> 取消。
- 完成后按 <kbd>Ctrl</kbd>+<kbd>C</kbd> 或使用 `/exit` 关闭交互式会话。

#### 恢复对话 { #resuming-conversations }

Codex 会在本地存储你的转录记录，因此你可以从离开的地方继续，而不必重复上下文。当你想用相同的仓库状态和指令重新打开早先线程时，请使用 `resume` 子命令。

- `codex resume` 会启动最近交互式会话的选择器。高亮某次运行可查看其摘要，按 <kbd>Enter</kbd> 重新打开。
- `codex resume --all` 会显示当前工作目录之外的会话，因此你可以重新打开任意本地运行。
- `codex resume --last` 会跳过选择器，直接跳到当前工作目录中最近的会话（添加 `--all` 可忽略当前工作目录过滤器）。
- `codex resume <SESSION_ID>` 会定位特定运行。你可以从选择器、`/status`，或 `~/.codex/sessions/` 下的文件复制 ID。

非交互式自动化运行也可以恢复：

```bash
codex exec resume --last "Fix the race conditions you found"
codex exec resume 7f9f9a2e-1b3c-4c7a-9b0e-.... "Implement the plan"
```

每次恢复的运行都会保留原始转录记录、计划历史和批准记录，因此 Codex 可以在你提供新指令时使用之前的上下文。如果你需要在恢复前调整环境，可以使用 `--cd` 覆盖工作目录，或用 `--add-dir` 添加额外根目录。

#### 将 TUI 连接到远程应用服务器 { #connect-the-tui-to-a-remote-app-server }

远程 TUI 模式让你可以在一台机器上运行 Codex app server，并从另一台机器使用 Codex 终端 UI。使用 WebSocket 监听器启动 app server：

```bash
codex app-server --listen ws://127.0.0.1:4500
```

然后将 TUI 连接到该端点：

```bash
codex --remote ws://127.0.0.1:4500
```

若要从另一台机器访问，请将 app server 绑定到可访问的网络接口，并在远程使用前配置 WebSocket 认证：

```bash
TOKEN_FILE="$HOME/.codex/app-server-token"
openssl rand -base64 32 > "$TOKEN_FILE"
chmod 600 "$TOKEN_FILE"
codex app-server --listen ws://0.0.0.0:4500 --ws-auth capability-token --ws-token-file "$TOKEN_FILE"
```

`--remote` 接受显式的 `ws://host:port`、`wss://host:port`、`unix://` 和 `unix://PATH` 地址。使用 `unix://` 表示 Codex 默认的本地 Unix socket，或使用 `unix://PATH` 表示显式本地 socket 路径。普通 WebSocket 连接适合 localhost 和 SSH 端口转发工作流。对于非本地客户端，请使用 WebSocket 认证，并将连接置于 TLS 后面。

Codex 支持这些 WebSocket 认证模式：

- Capability token：使用 `--ws-auth capability-token` 启动 server，并提供 `--ws-token-file /absolute/path` 或 `--ws-token-sha256 HEX`。
- Signed bearer token：使用 `--ws-auth signed-bearer-token --ws-shared-secret-file /absolute/path` 启动 server，并可附加可选的 `--ws-issuer`、`--ws-audience` 和 `--ws-max-clock-skew-seconds`。

TUI 会在 WebSocket 握手期间，以 `Authorization: Bearer <token>` 标头发送远程认证令牌。Codex 只接受通过 `wss://` URL 或仅本地 `ws://` URL 传递的远程认证令牌。

```bash
export CODEX_REMOTE_TOKEN="$(cat "$TOKEN_FILE")"
codex --remote wss://remote-host:4500 --remote-auth-token-env CODEX_REMOTE_TOKEN
```

对于 Codex app 中的 SSH 远程项目，请使用[远程连接](79-remote-connections.md)。对于托管的远程控制客户端，`codex remote-control` 会启动启用了远程控制支持的 app-server 进程。

#### 模型和推理 { #models-and-reasoning }

对于 Codex 中的大多数任务，`gpt-5.5` 是推荐模型。它是 OpenAI 最新的前沿模型，适用于复杂编码、计算机使用、知识工作和研究工作流，在规划、工具使用以及多步骤任务推进方面更强。对于特别快速的任务，ChatGPT Pro 订阅者可以访问研究预览版的 GPT-5.3-Codex-Spark 模型。

使用 `/model` 命令在会话中切换模型，或在启动 CLI 时指定模型。

```bash
codex --model gpt-5.5
```

[了解 Codex 中可用的模型](20-model-selection.md)。

#### 功能标志 { #feature-flags }

Codex 包含少量功能标志。使用 `features` 子命令查看可用项，并将更改持久化到配置中。

```bash
codex features list
codex features enable unified_exec
codex features disable shell_snapshot
```

`codex features enable <feature>` 和 `codex features disable <feature>` 会写入 `$CODEX_HOME/config.toml`。`features` 子命令不接受 `--profile`。

#### 子智能体 { #subagents }

使用 Codex 子智能体工作流来并行化更大的任务。关于设置、角色配置（`config.toml` 中的 `[agents]`）和示例，请参阅[子智能体](81-subagents-2.md)。

只有在你明确要求时，Codex 才会生成子智能体。由于每个子智能体都会执行自己的模型和工具工作，子智能体工作流会比可比的单智能体运行消耗更多 token。

#### 图片输入 { #image-inputs }

附加截图或设计规格，让 Codex 可以结合你的提示读取图片细节。你可以将图片粘贴到交互式输入区，或在命令行提供文件。

```bash
codex -i screenshot.png "Explain this error"
```

```bash
codex --image img1.png,img2.jpg "Summarize these diagrams"
```

Codex 接受 PNG 和 JPEG 等常见格式。对于两张或更多图片，请使用逗号分隔的文件名，并将它们与文本指令结合以添加上下文。

#### 图片生成 { #image-generation }

要求 Codex 直接在 CLI 中生成或编辑图片。这很适合图标、横幅、插图、精灵图表和占位图等资产。如果你希望 Codex 转换或扩展现有资产，请在提示中附加参考图片。

你可以使用自然语言请求，也可以在提示中包含 `$imagegen` 来显式调用图片生成技能。

内置图片生成使用 `gpt-image-2`，计入你的常规 Codex 使用限制；根据图片质量和尺寸，消耗包含额度的速度平均比没有图片生成的类似回合快 3-5 倍。详情请参阅[定价](02-codex-pricing.md#image-generation-usage-limits)。提示技巧和模型详情请参阅[图像生成指南](https://developers.openai.com/api/docs/guides/image-generation)。

对于更大批量的图片生成，请在环境变量中设置 `OPENAI_API_KEY`，并要求 Codex 通过 API 生成图片，这样会适用 API 价格。

#### 语法高亮和主题 { #syntax-highlighting-and-themes }

TUI 会对带围栏的 Markdown 代码块和文件 diff 做语法高亮，让代码在复查和调试期间更易浏览。

使用 `/theme` 打开主题选择器，实时预览主题，并将选择保存到 `~/.codex/config.toml` 中的 `tui.theme`。你也可以在 `$CODEX_HOME/themes` 下添加自定义 `.tmTheme` 文件，并在选择器中选择它们。

#### 运行本地代码审查 { #running-local-code-review }

在 CLI 中输入 `/review` 可打开 Codex 的审查预设。CLI 会启动一个专用审查器，读取你选择的 diff，并报告按优先级排序、可执行的发现，而不会触碰你的工作树。默认情况下它使用当前会话模型；可在 `config.toml` 中设置 `review_model` 来覆盖。

- **Review against a base branch** 让你选择本地分支；Codex 会查找相对于其上游的 merge base，对你的工作做 diff，并在你打开 pull request 前突出最大的风险。
- **Review uncommitted changes** 会检查所有已暂存、未暂存或未跟踪的内容，以便你在提交前处理问题。
- **Review a commit** 会列出最近的提交，并让 Codex 读取你选择的 SHA 对应的准确变更集。
- **Custom review instructions** 接受你自己的措辞（例如 "Focus on accessibility regressions"），并用该提示运行相同审查器。

每次运行都会作为单独的一轮出现在转录记录中，因此你可以随着代码演进重新运行审查，并比较反馈。

#### 网页搜索 { #web-search }

Codex 随附第一方网页搜索工具。对于 Codex CLI 中的本地任务，Codex 默认启用网页搜索，并从网页搜索缓存提供结果。该缓存是 OpenAI 维护的网页结果索引，因此缓存模式会返回预索引结果，而不是抓取实时页面。这减少了暴露于任意实时内容中提示注入的风险，但你仍应将网页结果视为不可信。如果你使用 `--yolo` 或其他[完全访问沙盒设置](13-agent-approvals-security.md)，网页搜索默认使用实时结果。要获取最新数据，请为单次运行传递 `--search`，或在 [Config basics](19-config-basics.md) 中设置 `web_search = "live"`。你也可以设置 `web_search = "disabled"` 来关闭该工具。

每当 Codex 查找内容时，你会在转录记录或 `codex exec --json` 输出中看到 `web_search` 项。

#### 使用输入提示运行 { #running-with-an-input-prompt }

当你只需要快速答案时，可以用单个提示运行 Codex，并跳过交互式 UI。

```bash
codex "explain this codebase"
```

Codex 会读取工作目录、制定计划，并在退出前将响应流式返回到你的终端。可以配合 `--path` 等标志来定位特定目录，或使用 `--model` 预先调整行为。

#### Shell 补全 { #shell-completions }

安装为你的 shell 生成的补全脚本，以加速日常使用：

```bash
codex completion bash
codex completion zsh
codex completion fish
```

在你的 shell 配置文件中运行补全脚本，为新会话设置补全。例如，如果你使用 `zsh`，可以将以下内容添加到 `~/.zshrc` 文件末尾：

```bash
# ~/.zshrc
eval "$(codex completion zsh)"
```

启动新会话，输入 `codex`，然后按 <kbd>Tab</kbd> 查看补全。如果看到 `command not found: compdef` 错误，请在 `eval "$(codex completion zsh)"` 行之前，将 `autoload -Uz compinit && compinit` 添加到 `~/.zshrc` 文件，然后重启 shell。

#### 批准模式 { #approval-modes }

批准模式定义 Codex 可以在不停止请求确认的情况下做多少事。在交互式会话中使用 `/permissions`，可随着你的舒适程度变化切换模式。

- **Auto**（默认）允许 Codex 读取文件、编辑，并在工作目录内运行命令。它在触碰该范围之外的任何内容或使用网络前仍会询问。
- **Read-only** 让 Codex 保持咨询模式。它可以浏览文件，但在你批准计划前不会更改或运行命令。
- **Full Access** 授予 Codex 跨你的机器工作的能力，包括无需询问即可访问网络。请谨慎使用，并且只在你信任该仓库和任务时使用。

Codex 始终会展示其操作的转录记录，因此你可以用常规 git 工作流审查或回滚变更。

#### 编写 Codex 脚本 { #scripting-codex }

使用 `exec` 子命令自动化工作流，或将 Codex 接入现有脚本。它会非交互式运行 Codex，并将最终计划和结果通过 `stdout` 返回。

```bash
codex exec "fix the CI failure"
```

将 `exec` 与 shell 脚本结合，可以构建自定义工作流，例如在 PR 发布前自动更新 changelog、整理 issue，或执行编辑检查。

#### 使用 Codex 云 { #working-with-codex-cloud }

`codex cloud` 命令让你无需离开终端即可分流并启动 [Codex cloud 任务](47-codex-web.md)。不带参数运行它可打开交互式选择器，浏览活动或已完成的任务，并将变更应用到你的本地项目。

你也可以直接从终端启动任务：

```bash
codex cloud exec --env ENV_ID "Summarize open bugs"
```

当你希望 Codex cloud 生成多个解决方案时，添加 `--attempts` (1-4) 请求 best-of-N 运行。例如，`codex cloud exec --env ENV_ID --attempts 3 "Summarize open bugs"`。

环境 ID 来自你的 Codex cloud 配置；使用 `codex cloud` 并按 <kbd>Ctrl</kbd>+<kbd>O</kbd> 选择环境，或通过 Web 控制台确认确切值。认证遵循你现有的 CLI 登录，如果提交失败，该命令会以非零状态退出，因此你可以将它接入脚本或 CI。

#### 斜杠命令 { #slash-commands }

斜杠命令让你可以快速访问专用工作流，例如 `/review`、`/fork`、`/side`，或你自己的可复用提示。Codex 随附一组精选内置命令，你也可以为团队特定任务或个人快捷方式创建自定义命令。

请参阅[斜杠命令指南](39-slash-commands-in-codex-cli.md)，浏览内置命令目录、了解如何编写自定义命令，以及它们在磁盘上的位置。

#### 提示编辑器 { #prompt-editor }

当你正在起草较长提示时，切换到完整编辑器，然后将结果发送回输入区可能更方便。

在提示输入框中，按 <kbd>Ctrl</kbd>+<kbd>G</kbd> 打开由 `VISUAL` 环境变量定义的编辑器（如果未设置 `VISUAL`，则使用 `EDITOR`）。

#### 模型上下文协议（MCP） { #model-context-protocol-mcp }

通过配置 Model Context Protocol（MCP）服务器，将 Codex 连接到更多工具。可在 `~/.codex/config.toml` 中添加 STDIO 或 streaming HTTP server，或使用 `codex mcp` CLI 命令管理它们；Codex 会在会话开始时自动启动它们，并把它们的工具与内置工具一起暴露出来。当你需要在另一个智能体内使用 Codex 时，甚至可以将 Codex 本身作为 MCP server 运行。

请参阅 [Model Context Protocol](53-model-context-protocol.md)，了解示例配置、支持的认证流程和更详细指南。

#### 技巧和快捷键 { #tips-and-shortcuts }

- 在输入区键入 `@`，可在工作区根目录中打开模糊文件搜索；按 <kbd>Tab</kbd> 或 <kbd>Enter</kbd> 可将高亮路径插入消息。
- 在 Codex 运行时按 <kbd>Enter</kbd> 可向当前回合注入新指令，或按 <kbd>Tab</kbd> 将后续输入排队到下一轮。排队输入可以是普通提示、`/review` 等斜杠命令，或 `!` shell 命令。Codex 会在排队的斜杠命令运行时解析它们。
- 在行首加 `!` 可运行本地 shell 命令（例如 `!ls`）。Codex 会把输出视为用户提供的命令结果，同时仍然应用你的批准和沙盒设置。
- 当输入区为空时，连按两次 <kbd>Esc</kbd> 可编辑上一条用户消息。继续按 <kbd>Esc</kbd> 可在转录记录中继续向前回溯，然后按 <kbd>Enter</kbd> 从该位置分叉。
- 使用 `codex --cd <path>` 可从任意目录启动 Codex，并设置工作根目录，无需先运行 `cd`。活动路径会显示在 TUI 标头中。
- 需要跨多个项目协调更改时，可使用 `--add-dir` 暴露更多可写根目录（例如 `codex --cd apps/frontend --add-dir ../backend --add-dir ../shared`）。
- 启动 Codex 前请确保环境已经设置好，这样它就不会花 token 探测要激活什么。例如，提前 source Python 虚拟环境（或其它语言环境）、启动所需 daemon，并导出你希望使用的环境变量。
