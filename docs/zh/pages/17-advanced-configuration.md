### 高级配置

Source: [Advanced Configuration](https://developers.openai.com/codex/config-advanced.md)

当你需要对提供商、策略和集成进行更多控制时，请使用这些选项。快速入门请参阅 [配置基础](19-config-basics.md)。

有关项目指导、可复用能力、自定义 slash commands、subagent 工作流和集成的背景信息，请参阅 [自定义](52-customization.md)。有关配置键，请参阅 [配置参考](16-configuration-reference.md)。

#### 配置档

Profiles 允许你保存命名配置层，并从 CLI 在它们之间切换。当你传入 `--profile profile-name` 时，Codex 会加载 `~/.codex/config.toml`，然后叠加 `~/.codex/profile-name.config.toml`。Profile 名称可以包含字母、数字、连字符和下划线。

为每个 profile 创建单独的 TOML 文件。在 profile 文件中使用顶层配置键；不要把它们嵌套在 `[profiles.profile-name]` 下。

```toml
# ~/.codex/deep-review.config.toml
model = "gpt-5.5"
model_reasoning_effort = "xhigh"
approval_policy = "on-request"
model_catalog_json = "/Users/me/.codex/model-catalogs/deep-review.json"
```

```shell
codex --profile deep-review
codex exec --profile deep-review "review this change"
```

因为 profile 文件是位于基础用户配置之上、项目和 CLI 配置之下的一层，所以它只需要包含与基础配置不同的值。Profile 文件也可以覆盖 `model_catalog_json`；当两个文件都设置它时，Codex 使用 profile 值。

在 Codex 0.134.0 及更高版本中，`--profile` 不再从 `config.toml` 读取 `[profiles.profile-name]`，也不再支持顶层 `profile = "profile-name"` 选择器。请将旧版 profile 设置移动到 `~/.codex/profile-name.config.toml`，然后从 `config.toml` 中移除匹配的 `[profiles.profile-name]` 表和 `profile = "profile-name"` 选择器。

#### 从 CLI 进行一次性覆盖

除了编辑 `~/.codex/config.toml`，你还可以从 CLI 为单次运行覆盖配置：

- 当存在专用标志时优先使用它们（例如 `--model`）。
- 当你需要覆盖任意键时，使用 `-c` / `--config`。

示例：

```shell
# Dedicated flag
codex --model gpt-5.4

# Generic key/value override (value is TOML, not JSON)
codex --config model='"gpt-5.4"'
codex --config sandbox_workspace_write.network_access=true
codex --config 'shell_environment_policy.include_only=["PATH","HOME"]'
```

说明：

- 键可以使用点号表示法设置嵌套值（例如 `mcp_servers.context7.enabled=false`）。
- `--config` 值会按 TOML 解析。拿不准时，请给值加引号，避免 shell 按空格拆分。
- 如果值无法按 TOML 解析，Codex 会将其视为字符串。

#### 配置和状态位置

Codex 将本地状态存储在 `CODEX_HOME` 下（默认是 `~/.codex`）。

你可能在那里看到的常见文件：

- `config.toml`（你的本地配置）
- `auth.json`（如果你使用基于文件的凭据存储）或你的操作系统 keychain/keyring
- `history.jsonl`（如果启用了历史持久化）
- 其它按用户保存的状态，例如日志和缓存

有关身份验证细节（包括凭据存储模式），请参阅 [身份验证](18-authentication-and-sessions.md)。有关完整配置键列表，请参阅 [配置参考](16-configuration-reference.md)。

有关签入仓库或系统路径的共享默认值、规则和 skills，请参阅 [团队配置](64-admin-setup.md#team-config)。

如果你只需要将内置 OpenAI provider 指向 LLM 代理、路由器或启用了 data residency 的项目，请在 `config.toml` 中设置 `openai_base_url`，而不是定义新 provider。这会更改内置 `openai` provider 的 base URL，而不需要单独的 `model_providers.<id>` 条目。

```toml
openai_base_url = "https://us.api.openai.com/v1"
```

#### 项目配置文件 (`.codex/config.toml`)

除了你的用户配置，Codex 还会从仓库内的 `.codex/config.toml` 文件读取项目范围覆盖。Codex 会从项目根目录遍历到当前工作目录，并加载找到的每个 `.codex/config.toml`。如果多个文件定义同一个键，最接近工作目录的文件胜出。

出于安全考虑，Codex 只会在项目受信任时加载项目范围配置文件。如果项目不受信任，Codex 会忽略项目 `.codex/` 层，包括 `.codex/config.toml`、项目本地 hooks 和项目本地 rules。用户和系统层保持独立并仍会加载。

项目配置中的相对路径（例如 `model_instructions_file`）会相对于包含 `config.toml` 的 `.codex/` 文件夹解析。

项目配置文件不能覆盖会重定向凭据、改变 host-owned app 请求元数据、更改 provider 认证、选择配置 profile，或运行机器本地 notification/telemetry 命令的设置。Codex 会忽略项目本地 `.codex/config.toml` 中的以下键，并在看到它们时打印启动警告：`openai_base_url`、`chatgpt_base_url`、`apps_mcp_product_sku`、`model_provider`、`model_providers`、`notify`、`profile`、`profiles`、`experimental_realtime_ws_base_url` 和 `otel`。请在用户级 `~/.codex/config.toml` 中设置 provider、notification 和 telemetry 键；使用 `--profile profile-name` 和 `~/.codex/profile-name.config.toml` 选择配置 profile。

#### 钩子

Codex 还可以从 `hooks.json` 文件或位于活动配置层旁边的 `config.toml` 文件中的 inline `[hooks]` 表加载生命周期 hooks。

实践中，四个最有用的位置是：

- `~/.codex/hooks.json`
- `~/.codex/config.toml`
- `<repo>/.codex/hooks.json`
- `<repo>/.codex/config.toml`

项目本地 hooks 只会在项目 `.codex/` 层受信任时加载。用户级 hooks 与项目信任无关。

Inline TOML hooks 使用与 `hooks.json` 相同的事件结构：

```toml
[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py"'
timeout = 30
statusMessage = "Checking Bash command"
```

如果单个层同时包含 `hooks.json` 和 inline `[hooks]`，Codex 会同时加载并发出警告。每个层优先使用一种表示方式。

有关当前事件列表、输入字段、输出行为和限制，请参阅 [Hooks](73-hooks.md)。

#### 智能体角色（`config.toml` 中的 `[agents]`）

有关 subagent 角色配置（`config.toml` 中的 `[agents]`），请参阅 [Subagents](81-subagents-2.md)。

#### 项目根目录检测

Codex 通过从工作目录向上遍历直到项目根目录，来发现项目配置（例如 `.codex/` 层和 `AGENTS.md`）。

默认情况下，Codex 将包含 `.git` 的目录视为项目根目录。要自定义此行为，请在 `config.toml` 中设置 `project_root_markers`：

```toml
# Treat a directory as the project root when it contains any of these markers.
project_root_markers = [".git", ".hg", ".sl"]
```

设置 `project_root_markers = []` 可跳过搜索父目录，并将当前工作目录视为项目根目录。

#### 自定义模型提供商

模型提供商定义 Codex 如何连接到模型（base URL、wire API、身份验证和可选 HTTP headers）。自定义 providers 不能复用保留的内置 provider ID：`openai`、`ollama` 和 `lmstudio`。

定义额外 providers，并将 `model_provider` 指向它们：

```toml
model = "gpt-5.4"
model_provider = "proxy"

[model_providers.proxy]
name = "OpenAI using LLM proxy"
base_url = "http://proxy.example.com"
env_key = "OPENAI_API_KEY"

[model_providers.local_ollama]
name = "Ollama"
base_url = "http://localhost:11434/v1"

[model_providers.mistral]
name = "Mistral"
base_url = "https://api.mistral.ai/v1"
env_key = "MISTRAL_API_KEY"
```

需要时添加请求 header：

```toml
[model_providers.example]
http_headers = { "X-Example-Header" = "example-value" }
env_http_headers = { "X-Example-Features" = "EXAMPLE_FEATURES" }
```

当 provider 需要 Codex 从外部凭据辅助程序获取 bearer token 时，请使用命令支持的身份验证：

```toml
[model_providers.proxy]
name = "OpenAI using LLM proxy"
base_url = "https://proxy.example.com/v1"
wire_api = "responses"

[model_providers.proxy.auth]
command = "/usr/local/bin/fetch-codex-token"
args = ["--audience", "codex"]
timeout_ms = 5000
refresh_interval_ms = 300000
```

认证命令不接收 `stdin`，并且必须将 token 打印到 stdout。Codex 会修剪周围空白，将空 token 视为错误，并在 `refresh_interval_ms` 主动刷新；设置 `refresh_interval_ms = 0` 表示仅在身份验证重试后刷新。不要将 `[model_providers.<id>.auth]` 与 `env_key`、`experimental_bearer_token` 或 `requires_openai_auth` 组合使用。

#### Amazon Bedrock 提供商

Codex 包含内置 `amazon-bedrock` 模型提供商。直接将其设置为 `model_provider`；不同于自定义 providers，此内置 provider 仅支持嵌套 AWS profile 和 region 覆盖。

```toml
model_provider = "amazon-bedrock"
model = "<bedrock-model-id>"

[model_providers.amazon-bedrock.aws]
profile = "default"
region = "eu-central-1"
```

如果省略 `profile`，Codex 会使用标准 AWS 凭据链。将 `region` 设置为应处理请求的受支持 Bedrock region。

有关完整设置流程、身份验证选项、受支持模型和功能可用性，请参阅 [Use Codex with Amazon Bedrock](82-use-codex-with-amazon-bedrock.md)。

#### OSS 模式（本地提供商）

当你传入 `--oss` 时，Codex 可以针对本地 "open source" provider（例如 Ollama 或 LM Studio）运行。如果传入 `--oss` 但未指定 provider，Codex 会使用 `oss_provider` 作为默认值。

```toml
# Default local provider used with `--oss`
oss_provider = "ollama" # or "lmstudio"
```

#### Azure 提供商和按提供商调优

```toml
[model_providers.azure]
name = "Azure"
base_url = "https://YOUR_PROJECT_NAME.openai.azure.com/openai"
env_key = "AZURE_OPENAI_API_KEY"
query_params = { api-version = "2025-04-01-preview" }
wire_api = "responses"
request_max_retries = 4
stream_max_retries = 10
stream_idle_timeout_ms = 300000
```

要更改内置 OpenAI provider 的 base URL，请使用 `openai_base_url`；不要创建 `[model_providers.openai]`，因为你不能覆盖内置 provider ID。

#### 使用数据驻留的 ChatGPT 客户

启用了 [data residency](https://help.openai.com/en/articles/9903489-data-residency-and-inference-residency-for-chatgpt) 的项目可以创建模型提供商，以用 [正确前缀](https://platform.openai.com/docs/guides/your-data#which-models-and-features-are-eligible-for-data-residency) 更新 base_url。

```toml
model_provider = "openaidr"
[model_providers.openaidr]
name = "OpenAI Data Residency"
base_url = "https://us.api.openai.com/v1" # Replace 'us' with domain prefix
```

#### 模型推理、详细程度和限制

```toml
model_reasoning_summary = "none"          # Disable summaries
model_verbosity = "low"                   # Shorten responses
model_supports_reasoning_summaries = true # Force reasoning
model_context_window = 128000             # Context window size
```

`model_verbosity` 只适用于使用 Responses API 的 providers。Chat Completions providers 会忽略该设置。

#### 审批策略和沙盒模式

选择审批严格度（影响 Codex 何时暂停）和沙盒级别（影响文件/网络访问权限）。

有关编辑 `config.toml` 时应牢记的运行细节，请参阅 [常见沙盒和审批组合](13-agent-approvals-security.md#common-sandbox-and-approval-combinations)、[可写根目录中的受保护路径](13-agent-approvals-security.md#protected-paths-in-writable-roots) 和 [网络访问](13-agent-approvals-security.md#network-access)。

有关同时配置文件系统和网络访问权限的 beta 权限 profile，请参阅 [权限](77-permissions.md)。

你也可以使用细粒度审批策略（`approval_policy = { granular = { ... } }`）来允许或自动拒绝单独的提示类别。当你希望某些场景保持正常交互式审批，但希望其它场景（例如 `request_permissions` 或 skill-script prompts）自动 fail closed 时，这很有用。

设置 `approvals_reviewer = "auto_review"` 可将符合条件的交互式审批请求通过自动审核路由。这改变的是审核者，而不是沙盒边界。

使用 `[auto_review].policy` 编写本地审核器策略指令。托管的 `guardian_policy_config` 优先。

```toml
approval_policy = "untrusted"   # Other options: on-request, never, or { granular = { ... } }
approvals_reviewer = "user"     # Or "auto_review" for automatic review
sandbox_mode = "workspace-write"
allow_login_shell = false       # Optional hardening: disallow login shells for shell tools

# Example granular approval policy:
# approval_policy = { granular = {
#   sandbox_approval = true,
#   rules = true,
#   mcp_elicitations = true,
#   request_permissions = false,
#   skill_approval = false
# } }

[sandbox_workspace_write]
exclude_tmpdir_env_var = false  # Allow $TMPDIR
exclude_slash_tmp = false       # Allow /tmp
writable_roots = ["/Users/YOU/.pyenv/shims"]
network_access = false          # Opt in to outbound network

[auto_review]
policy = """
Use your organization's automatic review policy.
"""
```

#### 命名权限配置档

有关内置 profiles、自定义 profile 语法，以及完整文件系统和网络配置模型，请参阅 [Permissions](77-permissions.md)。

有关完整键列表和要求约束，请参阅 [配置参考](16-configuration-reference.md) 和 [托管配置](67-managed-configuration.md)。

在 workspace-write 模式中，某些环境会让 `.git/` 和 `.codex/` 保持只读，即使工作区其余部分可写也是如此。这就是 `git commit` 等命令可能仍需要审批才能在沙盒外运行的原因。如果你希望 Codex 跳过特定命令（例如阻止沙盒外的 `git commit`），请使用 [Rules](54-rules.md)。

完全禁用沙盒（仅当你的环境已经隔离进程时使用）：

```toml
sandbox_mode = "danger-full-access"
```

#### Shell 环境策略

`shell_environment_policy` 控制 Codex 将哪些环境变量传递给它启动的任何子进程（例如运行模型提出的工具命令时）。从干净起点（`inherit = "none"`）或裁剪后的集合（`inherit = "core"`）开始，然后叠加 excludes、includes 和 overrides，以避免泄漏 secrets，同时仍提供任务所需的路径、键或标志。

```toml
[shell_environment_policy]
inherit = "none"
set = { PATH = "/usr/bin", MY_FLAG = "1" }
ignore_default_excludes = false
exclude = ["AWS_*", "AZURE_*"]
include_only = ["PATH", "HOME"]
```

Patterns 是大小写不敏感的 glob（`*`、`?`、`[A-Z]`）；`ignore_default_excludes = false` 会在你的 includes/excludes 运行前保留自动 KEY/SECRET/TOKEN 过滤器。

#### MCP 服务器

配置细节请参阅专门的 [MCP 文档](53-model-context-protocol.md)。

#### 可观测性和遥测

启用 OpenTelemetry (OTel) 日志导出以跟踪 Codex 运行（API 请求、SSE/events、提示词、工具审批/结果）。默认禁用；通过 `[otel]` opt in：

```toml
[otel]
environment = "staging"   # defaults to "dev"
exporter = "none"         # set to otlp-http or otlp-grpc to send events
log_user_prompt = false   # redact user prompts unless explicitly enabled
```

选择 exporter：

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

如果 `exporter = "none"`，Codex 会记录事件但不发送任何内容。Exporters 会异步批处理并在 shutdown 时 flush。事件元数据包括服务名、CLI 版本、环境标签、conversation id、模型、沙盒/审批设置，以及按事件记录的字段（参见 [配置参考](16-configuration-reference.md)）。

#### 会发出什么

Codex 会为运行和工具使用发出结构化日志事件。代表性事件类型包括：

- `codex.conversation_starts`（模型、推理设置、沙盒/审批策略）
- `codex.api_request`（attempt、status/success、duration 和 error details）
- `codex.sse_event`（stream event kind、success/failure、duration，以及 `response.completed` 上的 token counts）
- `codex.websocket_request` 和 `codex.websocket_event`（request duration 以及 per-message kind/success/error）
- `codex.user_prompt`（length；除非显式启用，否则 content 会 redact）
- `codex.tool_decision`（approved/denied，以及 decision 来自 config 还是 user）
- `codex.tool_result`（duration、success、output snippet）

#### 发出的 OTel 指标 { #otel-metrics-emitted }

启用 OTel metrics pipeline 后，Codex 会为 API、stream 和工具活动发出计数器与时长直方图。

下面每个指标还会包含默认元数据标签：`auth_mode`、`originator`、`session_source`、`model` 和 `app.version`。

| Metric                                | Type      | Fields              | Description                                  |
| ------------------------------------- | --------- | ------------------- | -------------------------------------------- |
| `codex.api_request`                   | counter   | `status`, `success` | 按 HTTP 状态和成功/失败统计 API 请求次数。   |
| `codex.api_request.duration_ms`       | histogram | `status`, `success` | API 请求时长（毫秒）。                       |
| `codex.sse_event`                     | counter   | `kind`, `success`   | 按事件类型和成功/失败统计 SSE 事件次数。     |
| `codex.sse_event.duration_ms`         | histogram | `kind`, `success`   | SSE 事件处理时长（毫秒）。                   |
| `codex.websocket.request`             | counter   | `success`           | 按成功/失败统计 WebSocket 请求次数。         |
| `codex.websocket.request.duration_ms` | histogram | `success`           | WebSocket 请求时长（毫秒）。                 |
| `codex.websocket.event`               | counter   | `kind`, `success`   | 按类型和成功/失败统计 WebSocket 消息/事件。  |
| `codex.websocket.event.duration_ms`   | histogram | `kind`, `success`   | WebSocket 消息/事件处理时长（毫秒）。        |
| `codex.tool.call`                     | counter   | `tool`, `success`   | 按工具名和成功/失败统计工具调用次数。        |
| `codex.tool.call.duration_ms`         | histogram | `tool`, `success`   | 按工具名和结果统计工具执行时长（毫秒）。     |

有关遥测的更多安全与隐私指导，请参阅 [Security](13-agent-approvals-security.md#monitoring-and-telemetry)。

#### Metrics { #metrics }

默认情况下，Codex 会定期向 OpenAI 发送少量匿名使用情况和健康数据。这有助于检测 Codex 何时工作异常，也能显示正在使用哪些功能和配置选项，让 Codex 团队专注于最重要的事项。这些 metrics 不包含任何个人身份信息（PII）。Metrics 收集独立于 OTel log/trace 导出。

如果你想在某台机器上完全禁用所有 Codex surface 的 metrics 收集，请在配置中设置 analytics flag：

```toml
[analytics]
enabled = false
```

每个 metric 都包含自己的字段，以及下面列出的默认上下文字段。

##### 默认上下文字段（适用于每个事件/metric） { #default-context-fields-applies-to-every-eventmetric }

- `auth_mode`：`swic` | `api` | `unknown`。
- `model`：使用的模型名称。
- `app.version`：Codex 版本。

##### Metrics catalog { #metrics-catalog }

每个 metric 都包含必需字段和上面的默认上下文字段。下面的 metric 名省略了 `codex.` 前缀。
大多数 metric 名集中定义在 `codex-rs/otel/src/metrics/names.rs`；这里也包含该文件之外发出的功能特定 metrics。
如果 metric 包含 `tool` 字段，它表示所用的内部工具（例如 `apply_patch` 或 `shell`），不包含 Codex 实际尝试应用的 shell 命令或 patch。

##### 运行时和模型传输 { #runtime-and-model-transport }

| Metric                                          | Type      | Fields               | Description                                      |
| ----------------------------------------------- | --------- | -------------------- | ------------------------------------------------ |
| `api_request`                                   | counter   | `status`, `success`  | 按 HTTP 状态和成功/失败统计 API 请求次数。       |
| `api_request.duration_ms`                       | histogram | `status`, `success`  | API 请求时长（毫秒）。                           |
| `sse_event`                                     | counter   | `kind`, `success`    | 按事件类型和成功/失败统计 SSE 事件次数。         |
| `sse_event.duration_ms`                         | histogram | `kind`, `success`    | SSE 事件处理时长（毫秒）。                       |
| `websocket.request`                             | counter   | `success`            | 按成功/失败统计 WebSocket 请求次数。             |
| `websocket.request.duration_ms`                 | histogram | `success`            | WebSocket 请求时长（毫秒）。                     |
| `websocket.event`                               | counter   | `kind`, `success`    | 按类型和成功/失败统计 WebSocket 消息/事件。      |
| `websocket.event.duration_ms`                   | histogram | `kind`, `success`    | WebSocket 消息/事件处理时长（毫秒）。            |
| `responses_api_overhead.duration_ms`            | histogram |                      | WebSocket response 中 Responses API 开销计时。   |
| `responses_api_inference_time.duration_ms`      | histogram |                      | WebSocket response 中 Responses API 推理计时。   |
| `responses_api_engine_iapi_ttft.duration_ms`    | histogram |                      | Responses API engine IAPI 首 token 时间计时。    |
| `responses_api_engine_service_ttft.duration_ms` | histogram |                      | Responses API engine service 首 token 时间计时。 |
| `responses_api_engine_iapi_tbt.duration_ms`     | histogram |                      | Responses API engine IAPI token 间隔计时。       |
| `responses_api_engine_service_tbt.duration_ms`  | histogram |                      | Responses API engine service token 间隔计时。    |
| `transport.fallback_to_http`                    | counter   | `from_wire_api`      | WebSocket 回退到 HTTP 的次数。                   |
| `remote_models.fetch_update.duration_ms`        | histogram |                      | 获取远程模型定义的耗时。                         |
| `remote_models.load_cache.duration_ms`          | histogram |                      | 加载远程模型缓存的耗时。                         |
| `startup_prewarm.duration_ms`                   | histogram | `status`             | 按结果统计启动预热时长。                         |
| `startup_prewarm.age_at_first_turn_ms`          | histogram | `status`             | 第一轮真实 turn 解析预热时的预热年龄。           |
| `cloud_requirements.fetch.duration_ms`          | histogram |                      | 工作区托管 cloud requirements 获取时长。         |
| `cloud_requirements.fetch_attempt`              | counter   | See note             | 工作区托管 cloud requirements 获取尝试次数。     |
| `cloud_requirements.fetch_final`                | counter   | See note             | 最终 cloud requirements 获取结果。               |
| `cloud_requirements.load`                       | counter   | `trigger`, `outcome` | 工作区托管 cloud requirements 加载结果。         |

`cloud_requirements.fetch_attempt` metric 包含 `trigger`、`attempt`、`outcome` 和 `status_code` 字段。`cloud_requirements.fetch_final` metric 包含 `trigger`、`outcome`、`reason`、`attempt_count` 和 `status_code` 字段。

##### Turn 和工具活动 { #turn-and-tool-activity }

| Metric                                 | Type      | Fields                                                                    | Description                                                                                 |
| -------------------------------------- | --------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `turn.e2e_duration_ms`                 | histogram |                                                                           | 完整 turn 的端到端耗时。                                                                    |
| `turn.ttft.duration_ms`                | histogram |                                                                           | turn 的首 token 时间。                                                                      |
| `turn.ttfm.duration_ms`                | histogram |                                                                           | turn 的首个模型输出项时间。                                                                |
| `turn.network_proxy`                   | counter   | `active`, `tmp_mem_enabled`                                               | 该 turn 是否启用了托管网络代理。                                                           |
| `turn.memory`                          | counter   | `read_allowed`, `feature_enabled`, `config_use_memories`, `has_citations` | 每个 turn 的 memory 读取可用性和 memory citation 使用情况。                                 |
| `turn.tool.call`                       | histogram | `tmp_mem_enabled`                                                         | turn 中的工具调用数量。                                                                     |
| `turn.token_usage`                     | histogram | `token_type`, `tmp_mem_enabled`                                           | 按 token 类型统计 turn token 使用量（`total`、`input`、`cached_input`、`output` 或 `reasoning_output`）。 |
| `tool.call`                            | counter   | `tool`, `success`                                                         | 按工具名和成功/失败统计工具调用次数。                                                       |
| `tool.call.duration_ms`                | histogram | `tool`, `success`                                                         | 按工具名和结果统计工具执行时长（毫秒）。                                                    |
| `tool.unified_exec`                    | counter   | `tty`                                                                     | 按 TTY 模式统计 unified exec 工具调用。                                                     |
| `approval.requested`                   | counter   | `tool`, `approved`                                                        | 工具审批请求结果（`approved`、`approved_with_amendment`、`approved_for_session`、`denied`、`abort`）。 |
| `mcp.call`                             | counter   | See note                                                                  | MCP 工具调用结果。                                                                          |
| `mcp.call.duration_ms`                 | histogram | See note                                                                  | MCP 工具调用时长。                                                                          |
| `mcp.tools.list.duration_ms`           | histogram | `cache`                                                                   | MCP 工具列表耗时，包括缓存命中/未命中状态。                                                 |
| `mcp.tools.fetch_uncached.duration_ms` | histogram |                                                                           | 未命中缓存的 MCP 工具获取耗时。                                                            |
| `mcp.tools.cache_write.duration_ms`    | histogram |                                                                           | Codex Apps MCP 工具缓存写入耗时。                                                          |
| `hooks.run`                            | counter   | `hook_name`, `source`, `status`                                           | 按 hook 名称、来源和状态统计 hook 运行次数。                                                |
| `hooks.run.duration_ms`                | histogram | `hook_name`, `source`, `status`                                           | Hook 运行时长（毫秒）。                                                                     |

`mcp.call` 和 `mcp.call.duration_ms` metrics 包含 `status`；普通工具调用发出项还包含 `tool`，并在可用时包含 `connector_id` 和 `connector_name`。被阻止的 Codex Apps MCP 调用可能只带 `status` 发出 `mcp.call`。

##### Threads、tasks 和 features { #threads-tasks-and-features }

| Metric                            | Type      | Fields                | Description                                                    |
| --------------------------------- | --------- | --------------------- | -------------------------------------------------------------- |
| `feature.state`                   | counter   | `feature`, `value`    | 与默认值不同的 feature 值（每个非默认值发出一行）。            |
| `status_line`                     | counter   |                       | 会话使用了配置的 status line 启动。                            |
| `model_warning`                   | counter   |                       | 发送给模型的警告。                                             |
| `thread.started`                  | counter   | `is_git`              | 新 thread 创建，并标注工作目录是否在 Git 仓库中。              |
| `conversation.turn.count`         | counter   |                       | 每个 thread 的用户/assistant turn 数，在 thread 结束时记录。   |
| `thread.fork`                     | counter   | `source`              | 通过 fork 现有 thread 创建的新 thread。                        |
| `thread.rename`                   | counter   |                       | Thread 被重命名。                                              |
| `thread.side`                     | counter   | `source`              | 创建了 side conversation。                                     |
| `thread.skills.enabled_total`     | histogram |                       | 新 thread 启用的 skill 数量。                                  |
| `thread.skills.kept_total`        | histogram |                       | prompt rendering 后保留的已启用 skill 数量。                   |
| `thread.skills.truncated`         | histogram |                       | skill rendering 是否截断了已启用 skill 列表（`1` 或 `0`）。    |
| `task.compact`                    | counter   | `type`                | 每种类型（`remote` 或 `local`）的 compaction 数量，包括手动和自动。 |
| `task.review`                     | counter   |                       | 触发 review 的次数。                                           |
| `task.undo`                       | counter   |                       | 触发 undo 的次数。                                             |
| `task.user_shell`                 | counter   |                       | 用户 shell 操作次数（例如 TUI 中的 `!`）。                     |
| `shell_snapshot`                  | counter   | See note              | shell snapshot 是否成功。                                      |
| `shell_snapshot.duration_ms`      | histogram | `success`             | 获取 shell snapshot 的耗时。                                   |
| `skill.injected`                  | counter   | `status`, `skill`     | 按 skill 统计 skill 注入结果。                                 |
| `plugins.startup_sync`            | counter   | `transport`, `status` | Curated plugin startup sync 尝试。                             |
| `plugins.startup_sync.final`      | counter   | `transport`, `status` | Curated plugin startup sync 最终结果。                         |
| `multi_agent.spawn`               | counter   | `role`                | 按 role 统计 agent spawn。                                     |
| `multi_agent.resume`              | counter   |                       | Agent resume 次数。                                            |
| `multi_agent.nickname_pool_reset` | counter   |                       | Agent nickname pool reset 次数。                               |

`shell_snapshot` metric 包含 `success`，失败时还包含 `failure_reason`。

##### Memory 和本地状态 { #memory-and-local-state }

| Metric                         | Type      | Fields                    | Description                                |
| ------------------------------ | --------- | ------------------------- | ------------------------------------------ |
| `memory.phase1`                | counter   | `status`                  | 按状态统计 memory phase 1 job 数量。       |
| `memory.phase1.e2e_ms`         | histogram |                           | Memory phase 1 的端到端耗时。              |
| `memory.phase1.output`         | counter   |                           | Memory phase 1 写出的输出数。              |
| `memory.phase1.token_usage`    | histogram | `token_type`              | 按 token 类型统计 memory phase 1 token 使用量。 |
| `memory.phase2`                | counter   | `status`                  | 按状态统计 memory phase 2 job 数量。       |
| `memory.phase2.e2e_ms`         | histogram |                           | Memory phase 2 的端到端耗时。              |
| `memory.phase2.input`          | counter   |                           | Memory phase 2 输入数量。                  |
| `memory.phase2.token_usage`    | histogram | `token_type`              | 按 token 类型统计 memory phase 2 token 使用量。 |
| `memories.usage`               | counter   | `kind`, `tool`, `success` | 按 kind、tool 和成功/失败统计 memory 使用。 |
| `external_agent_config.detect` | counter   | See note                  | 按 migration item 类型统计外部 agent config 检测。 |
| `external_agent_config.import` | counter   | See note                  | 按 migration item 类型统计外部 agent config 导入。 |
| `db.backfill`                  | counter   | `status`                  | 初始状态 DB backfill 结果（`upserted`、`failed`）。 |
| `db.backfill.duration_ms`      | histogram | `status`                  | 初始状态 DB backfill 的耗时。              |
| `db.error`                     | counter   | `stage`                   | 状态 DB 操作期间的错误。                   |

`external_agent_config.detect` 和 `external_agent_config.import` metrics 包含 `migration_type`；skills migration 还包含 `skills_count`。

##### Windows 沙盒 { #windows-sandbox }

| Metric                                           | Type      | Fields                                    | Description                                  |
| ------------------------------------------------ | --------- | ----------------------------------------- | -------------------------------------------- |
| `windows_sandbox.setup_success`                  | counter   | `originator`, `mode`                      | Windows sandbox setup 成功次数。             |
| `windows_sandbox.setup_failure`                  | counter   | `originator`, `mode`                      | Windows sandbox setup 失败次数。             |
| `windows_sandbox.setup_duration_ms`              | histogram | `result`, `originator`, `mode`            | Windows sandbox setup 耗时。                 |
| `windows_sandbox.elevated_setup_success`         | counter   |                                           | 提权 Windows sandbox setup 成功次数。        |
| `windows_sandbox.elevated_setup_failure`         | counter   | See note                                  | 提权 Windows sandbox setup 失败次数。        |
| `windows_sandbox.elevated_setup_canceled`        | counter   | See note                                  | 已取消的提权 Windows sandbox setup 尝试。    |
| `windows_sandbox.elevated_setup_duration_ms`     | histogram | `result`                                  | 提权 Windows sandbox setup 耗时。            |
| `windows_sandbox.elevated_prompt_shown`          | counter   |                                           | 显示提权 sandbox setup 提示的次数。          |
| `windows_sandbox.elevated_prompt_accept`         | counter   |                                           | 接受提权 sandbox setup 提示的次数。          |
| `windows_sandbox.elevated_prompt_use_legacy`     | counter   |                                           | 用户在提权提示中选择 legacy sandbox 的次数。 |
| `windows_sandbox.elevated_prompt_quit`           | counter   |                                           | 用户从提权提示退出的次数。                   |
| `windows_sandbox.fallback_prompt_shown`          | counter   |                                           | 显示 fallback sandbox 提示的次数。           |
| `windows_sandbox.fallback_retry_elevated`        | counter   |                                           | 用户从 fallback 提示重试提权 setup 的次数。  |
| `windows_sandbox.fallback_use_legacy`            | counter   |                                           | 用户从 fallback 提示选择 legacy sandbox 的次数。 |
| `windows_sandbox.fallback_prompt_quit`           | counter   |                                           | 用户从 fallback 提示退出的次数。             |
| `windows_sandbox.legacy_setup_preflight_failed`  | counter   | See note                                  | Legacy Windows sandbox setup 预检失败。      |
| `windows_sandbox.setup_elevated_sandbox_command` | counter   |                                           | 调用了提权 sandbox setup 命令。              |
| `windows_sandbox.createprocessasuserw_failed`    | counter   | `error_code`, `path_kind`, `exe`, `level` | Windows `CreateProcessAsUserW` 失败。        |

当有 Windows setup failure 详情可用时，提权 setup failure metrics 会包含 `code` 和 `message`，从共享 setup 路径发出时也可能包含 `originator`。`windows_sandbox.legacy_setup_preflight_failed` 从共享 setup 路径发出时包含 `originator`，但 fallback-prompt 预检失败可能不包含任何字段。

#### Feedback controls { #feedback-controls }

默认情况下，Codex 允许用户通过 `/feedback` 发送反馈。要在某台机器上的所有 Codex surface 中禁用反馈收集，请更新配置：

```toml
[feedback]
enabled = false
```

禁用后，`/feedback` 会显示禁用消息，并且 Codex 会拒绝反馈提交。

#### 隐藏或显示 reasoning events { #hide-or-surface-reasoning-events }

如果你想减少嘈杂的 "reasoning" 输出（例如 CI 日志中），可以将其抑制：

```toml
hide_agent_reasoning = true
```

如果你想在模型发出 raw reasoning content 时显示它：

```toml
show_raw_agent_reasoning = true
```

只有当 raw reasoning 适合你的工作流时才启用它。有些模型/provider（例如 `gpt-oss`）不会发出 raw reasoning；这种情况下，该设置没有可见效果。

#### 通知 { #notifications }

使用 `notify` 可在 Codex 发出受支持事件时触发外部程序（目前仅支持 `agent-turn-complete`）。这适合桌面 toast、聊天 webhook、CI 更新，或任何内置 TUI 通知无法覆盖的旁路提醒。

```toml
notify = ["python3", "/path/to/notify.py"]
```

响应 `agent-turn-complete` 的 `notify.py` 示例（已截断）：

```python
#!/usr/bin/env python3
import json, subprocess, sys

def main() -> int:
    notification = json.loads(sys.argv[1])
    if notification.get("type") != "agent-turn-complete":
        return 0
    title = f"Codex: {notification.get('last-assistant-message', 'Turn Complete!')}"
    message = " ".join(notification.get("input-messages", []))
    subprocess.check_output([
        "terminal-notifier",
        "-title", title,
        "-message", message,
        "-group", "codex-" + notification.get("thread-id", ""),
        "-activate", "com.googlecode.iterm2",
    ])
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

脚本会接收一个 JSON 参数。常见字段包括：

- `type`（目前为 `agent-turn-complete`）
- `thread-id`（会话标识符）
- `turn-id`（turn 标识符）
- `cwd`（工作目录）
- `input-messages`（导致该 turn 的用户消息）
- `last-assistant-message`（最后一条 assistant 消息文本）

将脚本放在磁盘某处，并让 `notify` 指向它。

##### `notify` 与 `tui.notifications` { #notify-vs-tuinotifications }

- `notify` 会运行外部程序（适合 webhook、桌面通知器、CI hook）。
- `tui.notifications` 内置于 TUI，并且可以选择按事件类型过滤（例如 `agent-turn-complete` 和 `approval-requested`）。
- `tui.notification_method` 控制 TUI 如何发出终端通知（`auto`、`osc9` 或 `bel`）。
- `tui.notification_condition` 控制 TUI 通知只在终端 `unfocused` 时触发，还是 `always` 触发。

在 `auto` 模式中，Codex 优先使用 OSC 9 通知（一些终端会将这种终端转义序列解释为桌面通知），否则回退到 BEL（`\x07`）。

确切键名请参阅 [配置参考](16-configuration-reference.md)。

#### 历史持久化 { #history-persistence }

默认情况下，Codex 会将本地会话转录记录保存在 `CODEX_HOME` 下（例如 `~/.codex/history.jsonl`）。要禁用本地历史持久化：

```toml
[history]
persistence = "none"
```

要限制 history 文件大小，请设置 `history.max_bytes`。当文件超过上限时，Codex 会丢弃最旧条目，并在保留最新记录的同时压缩文件。

```toml
[history]
max_bytes = 104857600 # 100 MiB
```

#### 可点击引用 { #clickable-citations }

如果你使用的终端/编辑器集成支持，Codex 可以将文件引用渲染为可点击链接。配置 `file_opener` 来选择 Codex 使用的 URI scheme：

```toml
file_opener = "vscode" # or cursor, windsurf, vscode-insiders, none
```

例如，类似 `/home/user/project/main.py:42` 的引用可被重写为可点击的 `vscode://file/...:42` 链接。

#### 项目指令发现 { #project-instructions-discovery }

Codex 会读取 `AGENTS.md`（以及相关文件），并在会话第一轮包含有限数量的项目指导。两个旋钮控制此行为：

- `project_doc_max_bytes`：从每个 `AGENTS.md` 文件读取多少内容
- `project_doc_fallback_filenames`：当某个目录层级缺少 `AGENTS.md` 时要尝试的其它文件名

详细 walkthrough 请参阅 [Custom instructions with AGENTS.md](50-custom-instructions-with-agents-md.md)。

#### TUI 选项 { #tui-options }

不带子命令运行 `codex` 会启动交互式终端 UI（TUI）。Codex 在 `[tui]` 下暴露一些 TUI 专属配置，包括：

- `tui.notifications`：启用/禁用通知（或限制为特定类型）
- `tui.notification_method`：为终端通知选择 `auto`、`osc9` 或 `bel`
- `tui.notification_condition`：选择通知在终端 `unfocused` 时触发，还是 `always` 触发
- `tui.animations`：启用/禁用 ASCII 动画和 shimmer 效果
- `tui.alternate_screen`：控制 alternate screen 使用（设置为 `never` 可保留终端 scrollback）
- `tui.show_tooltips`：在欢迎屏幕上显示或隐藏 onboarding tooltips

`tui.notification_method` 默认为 `auto`。在 `auto` 模式中，当终端看起来支持 OSC 9 通知时，Codex 优先使用 OSC 9（一种某些终端会解释为桌面通知的终端转义序列），否则回退到 BEL（`\x07`）。

完整键列表请参阅 [配置参考](16-configuration-reference.md)。
