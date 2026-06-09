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

如果你只需要将内置 OpenAI provider 指向 LLM 代理、路由器或启用了 data residency 的项目，请在 `config.toml` 中设置 `openai_base_url`，而不是定义新 provider。这会更改内置 `openai` provider 的 base URL，而不需要单独的 `model_providers.` 条目。

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
- `/.codex/hooks.json`
- `/.codex/config.toml`

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

Auth command 不接收 `stdin`，并且必须将 token 打印到 stdout。Codex 会修剪周围空白，将空 token 视为错误，并在 `refresh_interval_ms` 主动刷新；设置 `refresh_interval_ms = 0` 表示仅在身份验证重试后刷新。不要将 `[model_providers..auth]` 与 `env_key`、`experimental_bearer_token` 或 `requires_openai_auth` 组合使用。

#### Amazon Bedrock 提供商

Codex 包含内置 `amazon-bedrock` 模型提供商。直接将其设置为 `model_provider`；不同于自定义 providers，此内置 provider 仅支持嵌套 AWS profile 和 region 覆盖。

```toml
model_provider = "amazon-bedrock"
model = ""

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

在 workspace-write 模式中，某些环境会让 `.git/` 和 `.codex/` 保持 read-only，即使工作区其余部分可写也是如此。这就是 `git commit` 等命令可能仍需要审批才能在沙盒外运行的原因。如果你希望 Codex 跳过特定命令（例如阻止沙盒外的 `git commit`），请使用 rules。

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
