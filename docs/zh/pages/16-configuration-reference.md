### 配置参考

Source: [Configuration Reference](https://developers.openai.com/codex/config-reference.md)

请将本页作为 Codex 配置文件的可搜索参考。有关概念性指导和示例，请先阅读 [配置基础](19-config-basics.md) 和 [高级配置](17-advanced-configuration.md)。

### `config.toml`

用户级配置位于 `~/.codex/config.toml`。你也可以在 `.codex/config.toml` 文件中添加项目范围覆盖。Codex 只有在你信任该项目时才会加载项目范围配置文件。

项目范围配置不能覆盖机器本地的提供商、认证、宿主持有的 app 请求元数据、通知、配置档选择或遥测路由 key。当 `openai_base_url`、`chatgpt_base_url`、`apps_mcp_product_sku`、`model_provider`、`model_providers`、`notify`、`profile`、`profiles`、`experimental_realtime_ws_base_url` 和 `otel` 出现在项目本地 `.codex/config.toml` 中时，Codex 会忽略它们；请改为把提供商、通知和遥测 key 放在用户级配置中。[配置档文件](17-advanced-configuration.md#profiles) 与 `config.toml` 位于同一目录，形式为 `$CODEX_HOME/profile-name.config.toml`；使用 `--profile profile-name` 选择。

对于沙箱和审批相关 key（`approval_policy`、`sandbox_mode` 和 `sandbox_workspace_write.*`），请将本参考与 [沙箱和审批](13-agent-approvals-security.md#sandbox-and-approvals)、[可写根目录中的受保护路径](13-agent-approvals-security.md#protected-paths-in-writable-roots) 和 [网络访问](13-agent-approvals-security.md#network-access) 一起阅读。Beta 版权限配置档请参阅 [权限](77-permissions.md)。

| 键 | 类型 | 说明 |
| --- | --- | --- |
| `model` | `string` | 要使用的模型（例如 `gpt-5.5`）。 |
| `review_model` | `string` | `/review` 使用的可选模型覆盖值（默认使用当前会话模型）。 |
| `model_provider` | `string` | 来自 `model_providers` 的提供商 id（默认：`openai`）。 |
| `openai_base_url` | `string` | 内置 `openai` 模型提供商的基础 URL 覆盖值。 |
| `model_context_window` | `number` | 当前活动模型可用的上下文窗口 token 数。 |
| `model_auto_compact_token_limit` | `number` | 触发自动历史压缩的 token 阈值（未设置时使用模型默认值）。 |
| `model_catalog_json` | `string (path)` | 启动时加载的可选 JSON 模型目录路径。选中的 `$CODEX_HOME/profile-name.config.toml` 配置档文件可以按配置档覆盖此值。 |
| `oss_provider` | `lmstudio \| ollama` | 使用 `--oss` 运行时的默认本地提供商（未设置时默认询问）。 |
| `approval_policy` | `untrusted \| on-request \| never \| { granular = { sandbox_approval = bool, rules = bool, mcp_elicitations = bool, request_permissions = bool, skill_approval = bool } }` | 控制 Codex 在执行命令前何时暂停并请求审批。也可以使用 `approval_policy = { granular = { ... } }`，在保持其他提示可交互的同时，允许或自动拒绝特定提示类别。`on-failure` 已弃用；交互式运行请使用 `on-request`，非交互式运行请使用 `never`。 |
| `approval_policy.granular.sandbox_approval` | `boolean` | 当为 `true` 时，允许显示沙箱提权审批提示。 |
| `approval_policy.granular.rules` | `boolean` | 当为 `true` 时，允许显示由 execpolicy `prompt` 规则触发的审批提示。 |
| `approval_policy.granular.mcp_elicitations` | `boolean` | 当为 `true` 时，允许显示 MCP 征询提示，而不是自动拒绝。 |
| `approval_policy.granular.request_permissions` | `boolean` | 当为 `true` 时，允许显示来自 `request_permissions` 工具的提示。 |
| `approval_policy.granular.skill_approval` | `boolean` | 当为 `true` 时，允许显示技能脚本审批提示。 |
| `approvals_reviewer` | `user \| auto_review` | 指定由谁审核 `on-request` 或粒度审批策略下符合条件的审批提示。默认为 `user`；`auto_review` 使用审查者 subagent。此设置不会改变沙箱行为，也不会改变沙箱内已经允许的审查操作。 |
| `auto_review.policy` | `string` | 本地自动审查 Markdown 策略说明。托管的 `guardian_policy_config` 优先。空白值会被忽略。 |
| `allow_login_shell` | `boolean` | 允许 shell 类工具使用 login shell 语义。默认值为 `true`；当为 `false` 时，`login = true` 请求会被拒绝，省略 `login` 时默认使用非 login shell。 |
| `sandbox_mode` | `read-only \| workspace-write \| danger-full-access` | 命令执行期间用于文件系统和网络访问的沙箱策略。 |
| `sandbox_workspace_write.writable_roots` | `array<string>` | 当 `sandbox_mode = "workspace-write"` 时额外允许写入的根目录。 |
| `sandbox_workspace_write.network_access` | `boolean` | 允许 workspace-write 沙箱内的出站网络访问。 |
| `sandbox_workspace_write.exclude_tmpdir_env_var` | `boolean` | 在 workspace-write 模式下从可写根目录中排除 `$TMPDIR`。 |
| `sandbox_workspace_write.exclude_slash_tmp` | `boolean` | 在 workspace-write 模式下从可写根目录中排除 `/tmp`。 |
| `windows.sandbox` | `unelevated \| elevated` | 在 Windows 原生运行 Codex 时专用的原生沙箱模式。 |
| `windows.sandbox_private_desktop` | `boolean` | 在原生 Windows 上，默认让最终的沙箱化子进程运行在私有桌面。只有为了兼容旧的 `Winsta0\Default` 行为时才设置为 `false`。 |
| `notify` | `array<string>` | 用于通知的命令；会接收来自 Codex 的 JSON payload。 |
| `check_for_update_on_startup` | `boolean` | 启动时检查 Codex 更新（只有在更新由集中方式管理时才设为 false）。 |
| `feedback.enabled` | `boolean` | 在 Codex 各界面启用通过 `/feedback` 提交反馈（默认：true）。 |
| `analytics.enabled` | `boolean` | 为这台机器或当前配置档启用或禁用 analytics。未设置时使用客户端默认值。 |
| `instructions` | `string` | 预留给未来使用；请优先使用 `model_instructions_file` 或 `AGENTS.md`。 |
| `developer_instructions` | `string` | 注入到会话中的附加 developer instructions（可选）。 |
| `log_dir` | `string (path)` | Codex 写入日志文件的目录；默认是 `$CODEX_HOME/log`。显式设置后，也会在该目录中启用可选的明文 TUI 日志 `codex-tui.log`。 |
| `sqlite_home` | `string (path)` | Codex 存储 SQLite 状态数据库的目录；该数据库用于 agent jobs 和其他可恢复的运行时状态。 |
| `compact_prompt` | `string` | 历史压缩提示词的内联覆盖值。 |
| `commit_attribution` | `string` | 启用 `[features].codex_git_commit` 时使用的提交 co-author trailer。默认是 `Codex <noreply@openai.com>`；设置为 `""` 可禁用。 |
| `model_instructions_file` | `string (path)` | 用于替换内置 instructions 的文件，而不是 `AGENTS.md`。 |
| `personality` | `none \| friendly \| pragmatic` | 支持 `supportsPersonality` 的模型的默认沟通风格；可按线程/轮次或通过 `/personality` 覆盖。 |
| `service_tier` | `string` | 新轮次的首选 service tier。内置值包括 `flex` 和 `fast`；旧版 `fast` 配置会映射为请求值 `priority`，也可以存储模型目录提供的 tier ID。 |
| `experimental_compact_prompt_file` | `string (path)` | 从文件加载压缩提示词覆盖值（实验性）。 |
| `skills.config` | `array<object>` | 存储在 config.toml 中的按技能启用状态覆盖。 |
| `skills.config.<index>.path` | `string (path)` | 包含 `SKILL.md` 的技能文件夹路径。 |
| `skills.config.<index>.enabled` | `boolean` | 启用或禁用引用的技能。 |
| `apps.<id>.enabled` | `boolean` | 按 id 启用或禁用特定 app/connector（默认：true）。 |
| `apps._default.enabled` | `boolean` | 除非按 app 覆盖，否则所有 app 的默认启用状态。 |
| `apps._default.destructive_enabled` | `boolean` | 带有 `destructive_hint = true` 的 app 工具的默认允许/拒绝设置。 |
| `apps._default.open_world_enabled` | `boolean` | 带有 `open_world_hint = true` 的 app 工具的默认允许/拒绝设置。 |
| `apps.<id>.destructive_enabled` | `boolean` | 允许或阻止此 app 中声明 `destructive_hint = true` 的工具。 |
| `apps.<id>.open_world_enabled` | `boolean` | 允许或阻止此 app 中声明 `open_world_hint = true` 的工具。 |
| `apps.<id>.default_tools_enabled` | `boolean` | 除非存在按工具覆盖，否则此 app 内工具的默认启用状态。 |
| `apps.<id>.default_tools_approval_mode` | `auto \| prompt \| approve` | 除非存在按工具覆盖，否则此 app 内工具的默认审批行为。 |
| `apps.<id>.tools.<tool>.enabled` | `boolean` | 某个 app 工具的按工具启用覆盖（例如 `repos/list`）。 |
| `apps.<id>.tools.<tool>.approval_mode` | `auto \| prompt \| approve` | 单个 app 工具的按工具审批行为覆盖。 |
| `tool_suggest.discoverables` | `array<table>` | 允许为其他可发现 connector 或 plugin 提供工具建议。每个条目使用 `type = "connector"` 或 `"plugin"` 以及一个 `id`。 |
| `tool_suggest.disabled_tools` | `array<table>` | 禁用特定可发现 connector 或 plugin 的建议。每个条目使用 `type = "connector"` 或 `"plugin"` 以及一个 `id`。 |
| `features.apps` | `boolean` | 启用 ChatGPT Apps/connectors 支持（实验性）。 |
| `features.hooks` | `boolean` | 启用从 `hooks.json` 或内联 `[hooks]` 配置加载的生命周期钩子。`features.codex_hooks` 是已弃用别名。 |
| `features.codex_git_commit` | `boolean` | 启用 Codex 生成 git commit。启用后，Codex 使用 `commit_attribution` 在生成的提交消息中追加 `Co-authored-by:` trailer。 |
| `hooks` | `table` | 在 `config.toml` 中内联配置的生命周期钩子。使用与 `hooks.json` 相同的事件 schema；示例和支持事件请参阅 Hooks 指南。 |
| `hooks.<Event>` | `array<table>` | 钩子事件的匹配器组，例如 `PreToolUse`、`PermissionRequest`、`PostToolUse`、`PreCompact`、`PostCompact`、`SessionStart`、`SubagentStart`、`SubagentStop`、`UserPromptSubmit` 或 `Stop`。 |
| `hooks.<Event>[].hooks` | `array<table>` | 某个匹配器组的钩子处理程序。当前支持命令钩子；prompt 和 agent 钩子处理程序会被解析但跳过。 |
| `hooks.<Event>[].hooks[].commandWindows` | `string` | 仅 Windows 使用的 command hook 命令覆盖。也接受 TOML 别名 `command_windows`。 |
| `features.memories` | `boolean` | 启用 [Memories](74-memories.md)（默认关闭）。 |
| `mcp_servers.<id>.command` | `string` | MCP stdio 服务器的启动命令。 |
| `mcp_servers.<id>.args` | `array<string>` | 传递给 MCP stdio 服务器命令的参数。 |
| `mcp_servers.<id>.env` | `map<string,string>` | 转发给 MCP stdio 服务器的环境变量。 |
| `mcp_servers.<id>.env_vars` | `array<string \| { name = string, source = "local" \| "remote" }>` | 允许传给 MCP stdio 服务器的额外环境变量。字符串条目默认使用 `source = "local"`；只有在由执行器支持的远程 stdio 中才使用 `source = "remote"`。 |
| `mcp_servers.<id>.cwd` | `string` | MCP stdio 服务器进程的工作目录。 |
| `mcp_servers.<id>.url` | `string` | MCP streamable HTTP 服务器的 endpoint。 |
| `mcp_servers.<id>.bearer_token_env_var` | `string` | 为 MCP HTTP 服务器提供 bearer token 的环境变量。 |
| `mcp_servers.<id>.http_headers` | `map<string,string>` | 每个 MCP HTTP 请求附带的静态 HTTP headers。 |
| `mcp_servers.<id>.env_http_headers` | `map<string,string>` | 从环境变量填充的 MCP HTTP 服务器 HTTP headers。 |
| `mcp_servers.<id>.enabled` | `boolean` | 在不移除配置的情况下禁用 MCP 服务器。 |
| `mcp_servers.<id>.required` | `boolean` | 当为 true 时，如果这个已启用 MCP 服务器无法初始化，则启动/恢复失败。 |
| `mcp_servers.<id>.startup_timeout_sec` | `number` | 覆盖 MCP 服务器默认 10 秒启动超时。 |
| `mcp_servers.<id>.startup_timeout_ms` | `number` | `startup_timeout_sec` 的毫秒别名。 |
| `mcp_servers.<id>.tool_timeout_sec` | `number` | 覆盖 MCP 服务器默认 60 秒按工具超时。 |
| `mcp_servers.<id>.enabled_tools` | `array<string>` | MCP 服务器暴露工具名称的允许列表。 |
| `mcp_servers.<id>.disabled_tools` | `array<string>` | 应用在 `enabled_tools` 之后的 MCP 服务器工具拒绝列表。 |
| `mcp_servers.<id>.default_tools_approval_mode` | `auto \| prompt \| approve` | 除非存在按工具覆盖，否则此服务器上 MCP 工具的默认审批行为。 |
| `mcp_servers.<id>.tools.<tool>.approval_mode` | `auto \| prompt \| approve` | 此服务器上某个 MCP 工具的按工具审批行为覆盖。 |
| `mcp_servers.<id>.scopes` | `array<string>` | 向该 MCP 服务器认证时请求的 OAuth scopes。 |
| `mcp_servers.<id>.oauth_resource` | `string` | MCP 登录期间要包含的可选 RFC 8707 OAuth resource 参数。 |
| `mcp_servers.<id>.experimental_environment` | `local \| remote` | MCP 服务器的实验性部署位置。`remote` 会通过远程执行器环境启动 stdio 服务器；streamable HTTP 的远程部署尚未实现。 |
| `agents.max_threads` | `number` | 可同时打开的 agent threads 最大数量。未设置时默认为 `6`。 |
| `agents.max_depth` | `number` | 允许 spawned agent threads 的最大嵌套深度（根会话深度为 0；默认：1）。 |
| `agents.job_max_runtime_seconds` | `number` | `spawn_agents_on_csv` jobs 的默认单 worker 超时。未设置时，该工具回退为每个 worker 1800 秒。 |
| `agents.<name>.description` | `string` | Codex 在选择和生成该 agent 类型时展示的角色指导。 |
| `agents.<name>.config_file` | `string (path)` | 该角色的 TOML 配置层路径；相对路径从声明该角色的配置文件开始解析。 |
| `agents.<name>.nickname_candidates` | `array<string>` | 该角色生成 agent 时可选的显示昵称池。 |
| `memories.generate_memories` | `boolean` | 当为 `false` 时，新创建的线程不会作为 memory-generation 输入存储。默认值为 `true`。 |
| `memories.use_memories` | `boolean` | 当为 `false` 时，Codex 不会向未来会话注入现有 memories。默认值为 `true`。 |
| `memories.disable_on_external_context` | `boolean` | 当为 `true` 时，使用 MCP 工具调用、网页搜索或工具搜索等外部上下文的线程会排除在记忆生成之外。默认值为 `false`。旧别名：`memories.no_memories_if_mcp_or_web_search`。 |
| `memories.max_raw_memories_for_consolidation` | `number` | 全局 consolidation 保留的最新 raw memories 最大数量。默认值为 `256`，上限为 `4096`。 |
| `memories.max_unused_days` | `number` | 某条 memory 上次使用后经过多少天会失去 consolidation 资格。默认值为 `30`，会限制在 `0`-`365`。 |
| `memories.max_rollout_age_days` | `number` | 用于 memory generation 的线程最大年龄。默认值为 `30`，会限制在 `0`-`90`。 |
| `memories.max_rollouts_per_startup` | `number` | 每次启动处理的 rollout candidates 最大数量。默认值为 `16`，上限为 `128`。 |
| `memories.min_rollout_idle_hours` | `number` | 线程被视为可用于 memory generation 前所需的最短空闲时间。默认值为 `6`，会限制在 `1`-`48`。 |
| `memories.min_rate_limit_remaining_percent` | `number` | memory generation 开始前，Codex rate-limit windows 中要求的最小剩余百分比。默认值为 `25`，会限制在 `0`-`100`。 |
| `memories.extract_model` | `string` | 按线程 memory extraction 的可选模型覆盖。 |
| `memories.consolidation_model` | `string` | 全局 memory consolidation 的可选模型覆盖。 |
| `features.unified_exec` | `boolean` | 使用统一的 PTY-backed exec 工具（稳定；除 Windows 外默认启用）。 |
| `features.shell_snapshot` | `boolean` | 快照 shell 环境以加速重复命令（稳定；默认开启）。 |
| `features.undo` | `boolean` | 启用 undo 支持（稳定；默认关闭）。 |
| `features.multi_agent` | `boolean` | 启用 multi-agent 协作工具（`spawn_agent`、`send_input`、`resume_agent`、`wait_agent` 和 `close_agent`）（稳定；默认开启）。 |
| `features.personality` | `boolean` | 启用 personality selection controls（稳定；默认开启）。 |
| `features.network_proxy` | `boolean \| table` | 启用沙箱化网络。设置 `domains` 等网络策略选项时可使用 table 形式（实验性；默认关闭）。 |
| `features.network_proxy.enabled` | `boolean` | 启用沙箱化网络。默认值为 `false`。 |
| `features.network_proxy.domains` | `map<string, allow \| deny>` | 沙箱化网络的域名策略。默认未设置，意味着在添加 `allow` 规则前不允许外部目的地。支持精确 host、仅匹配子域的 `*.example.com`、匹配根域与子域的 `**.example.com`，以及全局 `*` allow 规则；请优先使用有范围的规则，因为 `*` 会大范围开放公共出站访问。添加 `deny` 规则可阻止目的地；冲突时 `deny` 优先。 |
| `features.network_proxy.unix_sockets` | `map<string, allow \| deny>` | 沙箱化网络的 Unix socket 策略。默认未设置；为允许的 socket 添加 `allow` 条目。 |
| `features.network_proxy.allow_local_binding` | `boolean` | 允许更宽泛的本地/私有网络访问。默认值为 `false`；精确的本地 IP literal 或 `localhost` allow 规则仍可允许特定本地目标。 |
| `features.network_proxy.enable_socks5` | `boolean` | 暴露 SOCKS5 支持。默认值为 `true`。 |
| `features.network_proxy.enable_socks5_udp` | `boolean` | 允许通过 SOCKS5 使用 UDP。默认值为 `true`。 |
| `features.network_proxy.allow_upstream_proxy` | `boolean` | 允许通过环境中的 upstream proxy 进行链式代理。默认值为 `true`。 |
| `features.network_proxy.dangerously_allow_non_loopback_proxy` | `boolean` | 允许非 loopback 监听地址。默认值为 `false`；启用后可能把代理监听器暴露到 localhost 之外。 |
| `features.network_proxy.dangerously_allow_all_unix_sockets` | `boolean` | 允许任意 Unix socket 目的地，而不是仅允许 allowlist 访问。默认值为 `false`；仅在严格受控环境中使用。 |
| `features.network_proxy.proxy_url` | `string` | 沙箱化网络的 HTTP listener URL。默认值为 `"http://127.0.0.1:3128"`。 |
| `features.network_proxy.socks_url` | `string` | SOCKS5 listener URL。默认值为 `"http://127.0.0.1:8081"`。 |
| `features.web_search` | `boolean` | 已弃用的旧版开关；请优先使用顶层 `web_search` 设置。 |
| `features.web_search_cached` | `boolean` | 已弃用的旧版开关。当 `web_search` 未设置时，true 映射为 `web_search = "cached"`。 |
| `features.web_search_request` | `boolean` | 已弃用的旧版开关。当 `web_search` 未设置时，true 映射为 `web_search = "live"`。 |
| `features.shell_tool` | `boolean` | 启用用于运行命令的默认 `shell` 工具（稳定；默认开启）。 |
| `features.enable_request_compression` | `boolean` | 在支持时用 zstd 压缩 streaming request bodies（稳定；默认开启）。 |
| `features.skill_mcp_dependency_install` | `boolean` | 允许为技能提示并安装缺失的 MCP dependencies（稳定；默认开启）。 |
| `features.fast_mode` | `boolean` | 在 TUI 中启用模型目录服务层级选择，包括活动模型声明支持时的 Fast 层级命令（稳定；默认开启）。 |
| `features.prevent_idle_sleep` | `boolean` | 在一个 turn 正在主动运行时阻止机器进入睡眠（实验性；默认关闭）。 |
| `suppress_unstable_features_warning` | `boolean` | 抑制启用开发中 feature flags 时出现的警告。 |
| `model_providers.<id>` | `table` | 自定义 provider 定义。内置 provider IDs（`openai`、`ollama` 和 `lmstudio`）为保留值，不能覆盖。 |
| `model_providers.<id>.name` | `string` | 自定义模型 provider 的显示名称。 |
| `model_providers.<id>.base_url` | `string` | 模型 provider 的 API base URL。 |
| `model_providers.<id>.env_key` | `string` | 提供 provider API key 的环境变量。 |
| `model_providers.<id>.env_key_instructions` | `string` | Provider API key 的可选设置指导。 |
| `model_providers.<id>.experimental_bearer_token` | `string` | Provider 的直接 bearer token（不推荐；请使用 `env_key`）。 |
| `model_providers.<id>.requires_openai_auth` | `boolean` | 该 provider 使用 OpenAI authentication（默认 false）。 |
| `model_providers.<id>.wire_api` | `responses` | Provider 使用的协议。`responses` 是唯一支持的值，省略时也是默认值。 |
| `model_providers.<id>.query_params` | `map<string,string>` | 追加到 provider 请求的额外 query parameters。 |
| `model_providers.<id>.http_headers` | `map<string,string>` | 添加到 provider 请求的静态 HTTP headers。 |
| `model_providers.<id>.env_http_headers` | `map<string,string>` | 存在时从环境变量填充的 HTTP headers。 |
| `model_providers.<id>.request_max_retries` | `number` | 发往 provider 的 HTTP 请求重试次数（默认：4）。 |
| `model_providers.<id>.stream_max_retries` | `number` | SSE streaming 中断的重试次数（默认：5）。 |
| `model_providers.<id>.stream_idle_timeout_ms` | `number` | SSE streams 的 idle timeout，单位为毫秒（默认：300000）。 |
| `model_providers.<id>.supports_websockets` | `boolean` | 该提供商是否支持 Responses API WebSocket 传输。 |
| `model_providers.<id>.auth` | `table` | 自定义提供商的由命令提供的 bearer token 配置。不要与 `env_key`、`experimental_bearer_token` 或 `requires_openai_auth` 组合使用。 |
| `model_providers.<id>.auth.command` | `string` | Codex 需要 bearer token 时运行的命令。该命令必须将 token 打印到 stdout。 |
| `model_providers.<id>.auth.args` | `array<string>` | 传递给 token 命令的参数。 |
| `model_providers.<id>.auth.timeout_ms` | `number` | Token 命令的最大运行时间，单位为毫秒（默认：5000）。 |
| `model_providers.<id>.auth.refresh_interval_ms` | `number` | Codex 主动刷新 token 的频率，单位为毫秒（默认：300000）。设置为 `0` 表示只在认证重试后刷新。 |
| `model_providers.<id>.auth.cwd` | `string (path)` | Token 命令的工作目录。 |
| `model_providers.amazon-bedrock.aws.profile` | `string` | 内置 `amazon-bedrock` provider 使用的 AWS profile 名称。 |
| `model_providers.amazon-bedrock.aws.region` | `string` | 内置 `amazon-bedrock` provider 使用的 AWS region。 |
| `model_reasoning_effort` | `minimal \| low \| medium \| high \| xhigh` | 调整支持模型的 reasoning effort（仅 Responses API；`xhigh` 取决于模型）。 |
| `plan_mode_reasoning_effort` | `none \| minimal \| low \| medium \| high \| xhigh` | 计划模式专用 reasoning 覆盖。未设置时，计划模式使用其内置预设默认值。 |
| `model_reasoning_summary` | `auto \| concise \| detailed \| none` | 选择 reasoning summary 详细程度，或完全禁用 summaries。 |
| `model_verbosity` | `low \| medium \| high` | 可选的 GPT-5 Responses API 输出详细程度覆盖；未设置时使用所选模型/预设默认值。 |
| `model_supports_reasoning_summaries` | `boolean` | 强制 Codex 发送或不发送 reasoning metadata。 |
| `shell_environment_policy.inherit` | `all \| core \| none` | 生成 subprocesses 时的基线环境继承策略。 |
| `shell_environment_policy.ignore_default_excludes` | `boolean` | 在其他过滤器运行前保留包含 KEY/SECRET/TOKEN 的变量。 |
| `shell_environment_policy.exclude` | `array<string>` | 在 defaults 之后移除环境变量的 glob patterns。 |
| `shell_environment_policy.include_only` | `array<string>` | Patterns allowlist；设置后只保留匹配的变量。 |
| `shell_environment_policy.set` | `map<string,string>` | 注入到每个 subprocess 的显式环境覆盖。 |
| `shell_environment_policy.experimental_use_profile` | `boolean` | 生成 subprocesses 时使用用户 shell profile。 |
| `project_root_markers` | `array<string>` | 项目根标记文件名列表；搜索父目录以确定项目根时使用。 |
| `project_doc_max_bytes` | `number` | 构建项目 instructions 时从 `AGENTS.md` 读取的最大字节数。 |
| `project_doc_fallback_filenames` | `array<string>` | `AGENTS.md` 缺失时要尝试的其他文件名。 |
| `history.persistence` | `save-all \| none` | 控制 Codex 是否将会话 transcripts 保存到 history.jsonl。 |
| `tool_output_token_limit` | `number` | 历史记录中存储单个工具/函数输出的 token 预算。 |
| `background_terminal_max_timeout` | `number` | 空 `write_stdin` 轮询（后台终端轮询）的最大轮询窗口，单位为毫秒。默认：`300000`（5 分钟）。替代旧的 `background_terminal_timeout` key。 |
| `history.max_bytes` | `number` | 如果设置，则通过丢弃最旧条目把 history 文件大小限制在指定字节数以内。 |
| `file_opener` | `vscode \| vscode-insiders \| windsurf \| cursor \| none` | 用于从 Codex 输出打开 citations 的 URI scheme（默认：`vscode`）。 |
| `otel.environment` | `string` | 应用到发出的 OpenTelemetry events 的环境标签（默认：`dev`）。 |
| `otel.exporter` | `none \| otlp-http \| otlp-grpc` | 选择 OpenTelemetry 导出器，并提供 endpoint 元数据。 |
| `otel.trace_exporter` | `none \| otlp-http \| otlp-grpc` | 选择 OpenTelemetry trace 导出器，并提供 endpoint 元数据。 |
| `otel.metrics_exporter` | `none \| statsig \| otlp-http \| otlp-grpc` | 选择 OpenTelemetry metrics 导出器（默认：`statsig`）。 |
| `otel.log_user_prompt` | `boolean` | 选择导出包含原始用户提示词的 OpenTelemetry logs。 |
| `otel.exporter.<id>.endpoint` | `string` | OTEL logs 的导出器 endpoint。 |
| `otel.exporter.<id>.protocol` | `binary \| json` | OTLP/HTTP exporter 使用的协议。 |
| `otel.exporter.<id>.headers` | `map<string,string>` | OTEL exporter 请求附带的静态 headers。 |
| `otel.trace_exporter.<id>.endpoint` | `string` | OTEL logs 的 trace 导出器 endpoint。 |
| `otel.trace_exporter.<id>.protocol` | `binary \| json` | OTLP/HTTP trace exporter 使用的协议。 |
| `otel.trace_exporter.<id>.headers` | `map<string,string>` | OTEL trace exporter 请求附带的静态 headers。 |
| `otel.exporter.<id>.tls.ca-certificate` | `string` | OTEL 导出器 TLS 的 CA 证书路径。 |
| `otel.exporter.<id>.tls.client-certificate` | `string` | OTEL 导出器 TLS 的客户端证书路径。 |
| `otel.exporter.<id>.tls.client-private-key` | `string` | OTEL 导出器 TLS 的客户端私钥路径。 |
| `otel.trace_exporter.<id>.tls.ca-certificate` | `string` | OTEL trace 导出器 TLS 的 CA 证书路径。 |
| `otel.trace_exporter.<id>.tls.client-certificate` | `string` | OTEL trace 导出器 TLS 的客户端证书路径。 |
| `otel.trace_exporter.<id>.tls.client-private-key` | `string` | OTEL trace 导出器 TLS 的客户端私钥路径。 |
| `tui` | `table` | TUI 专用选项，例如启用内联桌面通知。 |
| `tui.notifications` | `boolean \| array<string>` | 启用 TUI notifications；也可限制为特定事件类型。 |
| `tui.notification_method` | `auto \| osc9 \| bel` | Terminal notifications 的通知方式（默认：auto）。 |
| `tui.notification_condition` | `unfocused \| always` | 控制 TUI notifications 是只在终端未聚焦时触发，还是无论焦点如何都触发。默认值为 `unfocused`。 |
| `tui.animations` | `boolean` | 启用终端动画（欢迎屏、shimmer、spinner）（默认：true）。 |
| `tui.alternate_screen` | `auto \| always \| never` | 控制 TUI 的备用屏幕使用方式（默认：auto；在 Zellij 中 auto 会跳过，以保留回滚缓冲）。 |
| `tui.vim_mode_default` | `boolean` | 让输入区启动时进入 Vim normal mode，而不是 insert mode（默认：false）。仍可在会话中用 `/vim` 切换。 |
| `tui.raw_output_mode` | `boolean` | 让 TUI 以原始回滚模式启动，便于在终端中复制选择（默认：false）。可用 `/raw` 或默认 `alt-r` 快捷键切换。 |
| `tui.show_tooltips` | `boolean` | 在 TUI 欢迎屏显示 onboarding tooltips（默认：true）。 |
| `tui.status_line` | `array<string> \| null` | TUI 页脚状态栏项标识符的有序列表。`null` 会禁用状态栏。 |
| `tui.terminal_title` | `array<string> \| null` | 终端窗口/标签页标题项标识符的有序列表。默认为 `["spinner", "project"]`；`null` 会禁用标题更新。 |
| `tui.theme` | `string` | 语法高亮主题覆盖（kebab-case 主题名称）。 |
| `tui.keymap.<context>.<action>` | `string \| array<string>` | TUI 动作的键盘快捷键绑定。支持的上下文包括 `global`、`chat`、`composer`、`editor`、`vim_normal`、`vim_operator`、`vim_text_object`、`pager`、`list` 和 `approval`。选定的输入区动作会回退到匹配的 `tui.keymap.global` 绑定；支持时，上下文专用绑定优先。 |
| `tui.keymap.<context>.<action> = []` | `empty array` | 在该快捷键映射上下文中解除动作绑定。按键名称使用规范化字符串，例如 `ctrl-a`、`shift-enter`、`page-down` 或 `minus`。 |
| `plugins.<plugin>.mcp_servers.<server>.enabled` | `boolean` | 启用或禁用已安装 plugin 打包的 MCP 服务器，而不改变 plugin manifest。 |
| `plugins.<plugin>.mcp_servers.<server>.default_tools_approval_mode` | `auto \| prompt \| approve` | Plugin 提供的 MCP 服务器上工具的默认审批行为。 |
| `plugins.<plugin>.mcp_servers.<server>.enabled_tools` | `array<string>` | Plugin 提供的 MCP 服务器暴露工具的允许列表。 |
| `plugins.<plugin>.mcp_servers.<server>.disabled_tools` | `array<string>` | 应用在 `enabled_tools` 之后的 plugin 提供的 MCP 服务器工具拒绝列表。 |
| `plugins.<plugin>.mcp_servers.<server>.tools.<tool>.approval_mode` | `auto \| prompt \| approve` | Plugin 提供的 MCP 工具的按工具审批行为覆盖。 |
| `tui.model_availability_nux.<model>` | `integer` | 按 model slug 记录的内部启动提示状态。 |
| `hide_agent_reasoning` | `boolean` | 在 TUI 和 `codex exec` 输出中都隐藏 reasoning 事件。 |
| `show_raw_agent_reasoning` | `boolean` | 当活动模型发出原始 reasoning 内容时显示它。 |
| `disable_paste_burst` | `boolean` | 在 TUI 中禁用突发粘贴检测。 |
| `windows_wsl_setup_acknowledged` | `boolean` | 跟踪 Windows onboarding 确认状态（仅 Windows）。 |
| `chatgpt_base_url` | `string` | 覆盖 ChatGPT 登录流程使用的 base URL。 |
| `cli_auth_credentials_store` | `file \| keyring \| auto` | 控制 CLI 缓存凭据的位置（基于文件的 auth.json 或 OS keychain）。 |
| `mcp_oauth_credentials_store` | `auto \| file \| keyring` | MCP OAuth 凭据的首选存储位置。 |
| `mcp_oauth_callback_port` | `integer` | MCP OAuth 登录期间本地 HTTP callback server 使用的可选固定端口。未设置时，Codex 绑定到 OS 选择的临时端口。 |
| `mcp_oauth_callback_url` | `string` | MCP OAuth 登录的可选重定向 URI 覆盖（例如 devbox ingress URL）。`mcp_oauth_callback_port` 仍控制回调监听端口。 |
| `experimental_use_unified_exec_tool` | `boolean` | 启用 unified exec 的旧名称；请优先使用 `[features].unified_exec` 或 `codex --enable unified_exec`。 |
| `tools.web_search` | `boolean \| { context_size = "low\|medium\|high", allowed_domains = [string], location = { country, region, city, timezone } }` | 可选网页搜索工具配置。仍接受旧版 boolean 形式，但 object 形式可设置搜索上下文大小、允许域名和近似用户位置。 |
| `tools.view_image` | `boolean` | 启用本地图片附件工具 `view_image`。 |
| `web_search` | `disabled \| cached \| live` | 网页搜索模式（默认：`"cached"`；cached 使用 OpenAI 维护的索引，不抓取实时网页；如果使用 `--yolo` 或其他完全访问沙箱设置，则默认变为 `"live"`）。使用 `"live"` 可从网页获取最新数据，使用 `"disabled"` 可移除该工具。 |
| `default_permissions` | `string` | 应用到沙箱化工具调用的默认权限配置档名称。内置值为 `:read-only`、`:workspace` 和 `:danger-full-access`；自定义配置档名称需要匹配的 `[permissions.<name>]` tables。不要与 `sandbox_mode` 或 `[sandbox_workspace_write]` 组合使用。 |
| `permissions.<name>.description` | `string` | 此命名配置档的人类可读说明。配置档不会通过 `extends` 继承父级说明。 |
| `permissions.<name>.extends` | `string` | 在此命名配置档之前应用的可选父配置档。可设置为另一个命名配置档、`:read-only` 或 `:workspace`；`:danger-full-access`、未定义父级和继承循环会被拒绝。 |
| `permissions.<name>.workspace_roots` | `table` | 由配置档定义的 workspace roots；它们会与会话运行时 workspace roots 一起接收 `:workspace_roots` filesystem rules。 |
| `permissions.<name>.workspace_roots.<path>` | `boolean` | 当为 `true` 时，把一个路径加入该配置档的 workspace root 集合。禁用条目保持不活跃。 |
| `permissions.<name>.filesystem` | `table` | 命名文件系统权限配置档。每个 key 是绝对路径，或 `:minimal`、`:workspace_roots` 等特殊 token。 |
| `permissions.<name>.filesystem.glob_scan_max_depth` | `number` | 在沙箱启动前会对 deny-read glob patterns 做快照匹配的平台上，扩展这些 glob patterns 的最大深度。设置时必须至少为 `1`。 |
| `permissions.<name>.filesystem.<path-or-glob>` | `"read" \| "write" \| "deny" \| table` | 为某个路径、glob pattern 或特殊 token 授予直接访问权限，或在该 root 下限定嵌套条目。使用 `"deny"` 可拒绝读取匹配路径。 |
| `permissions.<name>.filesystem.":workspace_roots".<subpath-or-glob>` | `"read" \| "write" \| "deny"` | 相对于每个有效 workspace root 的 有范围的文件系统访问。使用 `"."` 表示 root 本身；`"**/*.env"` 等 glob 子路径 可用 `"deny"` 拒绝读取。 |
| `permissions.<name>.network.enabled` | `boolean` | 为此命名权限配置档启用网络访问。这会改变沙箱网络策略；它本身不会启动 network proxy。 |
| `permissions.<name>.network.proxy_url` | `string` | 当此权限配置档启用沙箱化网络时使用的 HTTP listener URL。 |
| `permissions.<name>.network.enable_socks5` | `boolean` | 当此权限配置档启用沙箱化网络时暴露 SOCKS5 支持。 |
| `permissions.<name>.network.socks_url` | `string` | 此权限配置档使用的 SOCKS5 proxy endpoint。 |
| `permissions.<name>.network.enable_socks5_udp` | `boolean` | 启用后允许通过 SOCKS5 listener 使用 UDP。 |
| `permissions.<name>.network.allow_upstream_proxy` | `boolean` | 允许沙箱化网络通过另一个 upstream proxy 链式转发。 |
| `permissions.<name>.network.dangerously_allow_non_loopback_proxy` | `boolean` | 允许沙箱化网络监听器绑定非 loopback 地址。启用后可能把监听器暴露到 localhost 之外。 |
| `permissions.<name>.network.dangerously_allow_all_unix_sockets` | `boolean` | 允许任意 Unix socket 目的地，而不是默认受限集合。仅在严格受控环境中使用。 |
| `permissions.<name>.network.mode` | `limited \| full` | 用于子进程流量的网络代理模式。 |
| `permissions.<name>.network.domains` | `table` | 沙箱化网络的域名规则。支持精确 host、仅匹配子域的 `*.example.com`、匹配根域与子域的 `**.example.com`，以及全局 `*` allow 规则。冲突时 `deny` 优先。 |
| `permissions.<name>.network.domains.<pattern>` | `allow \| deny` | 允许或拒绝一个精确 host 或有范围的 wildcard pattern，例如 `*.example.com` 或 `**.example.com`。 |
| `permissions.<name>.network.unix_sockets` | `table` | 沙箱化网络的 Unix socket allowlist 覆盖。使用 socket 路径作为 key；`allow` 添加路径，`deny` 拒绝路径。 |
| `permissions.<name>.network.unix_sockets.<path>` | `allow \| deny` | 使用 `allow` 将一个绝对 Unix socket 路径加入有效 allowlist，或使用 `deny` 拒绝它。被拒绝的条目会从有效 allowlist 中省略。 |
| `permissions.<name>.network.allow_local_binding` | `boolean` | 允许通过沙箱化网络进行更宽泛的本地/私有网络访问。即使此值保持 `false`，精确本地 IP literal 或 `localhost` allow 规则仍可允许特定本地目标。 |
| `projects.<path>.trust_level` | `string` | 将项目或 worktree 标记为 trusted 或 untrusted（`"trusted"` \| `"untrusted"`）。不受信任的项目会跳过项目范围的 `.codex/` layers，包括项目本地 config、hooks 和 rules。 |
| `notice.hide_full_access_warning` | `boolean` | 跟踪完全访问警告提示的确认状态。 |
| `notice.hide_world_writable_warning` | `boolean` | 跟踪 Windows world-writable directories warning 的确认状态。 |
| `notice.hide_rate_limit_model_nudge` | `boolean` | 跟踪速率限制模型切换提醒的选择退出状态。 |
| `notice.hide_gpt5_1_migration_prompt` | `boolean` | 跟踪 GPT-5.1 migration prompt 的确认状态。 |
| `notice.hide_gpt-5.1-codex-max_migration_prompt` | `boolean` | 跟踪 gpt-5.1-codex-max 迁移提示的确认状态。 |
| `notice.model_migrations` | `map<string,string>` | 按 old->new 映射跟踪已确认的模型迁移。 |
| `forced_login_method` | `chatgpt \| api` | 将 Codex 限制为特定认证方式。 |
| `forced_chatgpt_workspace_id` | `string (uuid)` | 将 ChatGPT 登录限制到特定 workspace identifier。 |

你可以在[这里](https://developers.openai.com/codex/config-schema.json)找到最新的 `config.toml` JSON schema。

如果想在 VS Code 或 Cursor 中编辑 `config.toml` 时获得自动补全和诊断，可以安装 [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml) 扩展，并将下面这一行添加到 `config.toml` 顶部：

```toml
#:schema https://developers.openai.com/codex/config-schema.json
```

注意：请将 `experimental_instructions_file` 重命名为 `model_instructions_file`。Codex 已弃用旧 key；请把现有配置更新为新名称。

### `requirements.toml`

`requirements.toml` 是管理员强制配置文件，用于约束用户无法覆盖的安全敏感设置。有关详情、位置和示例，请参阅 [管理员强制要求](67-managed-configuration.md#admin-enforced-requirements-requirementstoml)。

对于 ChatGPT Business 和 Enterprise 用户，Codex 还可以应用从云端获取的 requirements。优先级详情请参阅安全页面。

在 `requirements.toml` 中使用 `[features]`，即可按 `config.toml` 使用的相同规范 key 固定功能标志。省略的 key 保持不受约束。

托管 permission-profile allowlists 需要 Codex 0.138.0 或更高版本。Codex 0.137.0 及更早版本会忽略 `allowed_permission_profiles` 和 managed `default_permissions`。

请将 `allowed_sandbox_modes` 与 `sandbox_mode` 搭配使用。对于权限配置档部署，请将 `allowed_permission_profiles` 与 managed `default_permissions` 搭配使用。

| 键 | 类型 | 说明 |
| --- | --- | --- |
| `allowed_approval_policies` | `array<string>` | `approval_policy` 允许的值（例如 `untrusted`、`on-request`、`never` 和 `granular`）。 |
| `allowed_approvals_reviewers` | `array<string>` | `approvals_reviewer` 允许的值，例如 `user` 和 `auto_review`。 |
| `guardian_policy_config` | `string` | 用于自动审查的托管 Markdown 策略说明。它优先于本地 `[auto_review].policy`。空白值会被忽略。 |
| `allowed_permission_profiles` | `table<boolean>` | 允许的权限配置档完整列表。设置为 `true` 的配置档被允许；省略或设置为 `false` 的配置档都会被拒绝，包括未来版本新增的配置档。组合 requirements sources 时，条目按配置档名称匹配。 |
| `allowed_permission_profiles.<name>` | `boolean` | 允许或拒绝在已加载 config 或 requirements source 中定义的内置或自定义权限配置档。较早的 requirements source 可以用 `false` 关闭较晚 source 允许的配置档。 |
| `default_permissions` | `string` | 管理员强制的默认权限配置档。该配置档必须被 `allowed_permission_profiles` 允许。请显式设置以获得可预测行为；如果省略，只有在 `:workspace` 和 `:read-only` 都被显式允许时，Codex 才默认使用 `:workspace`。 |
| `permissions.<name>` | `table` | 管理员定义的权限配置档。名称不能以 `:` 开头，不能使用保留名称 `filesystem`，也不能与已加载 config 中的配置档重名。使用与 `config.toml` 相同的 profile fields；完整 schema 请参阅 Permissions 指南。 |
| `allowed_sandbox_modes` | `array<string>` | `sandbox_mode` 允许的值。 |
| `windows.allowed_sandbox_implementations` | `array<string>` | `windows.sandbox` 允许的原生 Windows sandbox implementations（`elevated` 和 `unelevated`）。列表不能为空。当两者都允许且未选择模式时，Codex 优先使用 `elevated`。 |
| `remote_sandbox_config` | `array<table>` | 主机特定的沙箱要求。第一个 `hostname_patterns` 匹配解析后主机名的条目，会覆盖该 requirements source 的顶层 `allowed_sandbox_modes`。主机特定条目当前只覆盖沙箱模式。 |
| `remote_sandbox_config[].hostname_patterns` | `array<string>` | 不区分大小写的主机名 patterns。支持 `*` 匹配任意字符序列，`?` 匹配单个字符。 |
| `remote_sandbox_config[].allowed_sandbox_modes` | `array<string>` | 当此主机特定条目匹配时要应用的允许沙箱模式。 |
| `allowed_web_search_modes` | `array<string>` | `web_search` 允许的值（`disabled`、`cached`、`live`）。`disabled` 始终允许；空列表实际上只允许 `disabled`。 |
| `allow_managed_hooks_only` | `boolean` | 当为 `true` 时，Codex 跳过 用户、项目、会话和 plugin hooks，同时仍允许来自 `requirements.toml` 和其他托管配置层中的托管钩子。 |
| `features.plugin_sharing` | `boolean` | 在云托管 `requirements.toml` 中设置为 `false`，可禁用本地构建 plugins 的工作区共享。 |
| `features` | `table` | 按 `config.toml` 的 `[features]` table 中规范名称作为 key 固定功能值。 |
| `features.<name>` | `boolean` | 要求某个规范 feature key 保持启用或禁用。 |
| `features.in_app_browser` | `boolean` | 在 `requirements.toml` 中设置为 `false`，可禁用 in-app browser pane。 |
| `features.browser_use` | `boolean` | 在 `requirements.toml` 中设置为 `false`，可禁用 Browser Use 和 Browser Agent 可用性。 |
| `features.computer_use` | `boolean` | 在 `requirements.toml` 中设置为 `false`，可禁用 Computer Use 可用性 以及相关安装或启用流程。 |
| `experimental_network` | `table` | 从 `requirements.toml` 强制执行的网络访问要求。这些约束独立于 `features.network_proxy`，并且可以在没有用户 feature flag 的情况下配置沙箱化网络。 |
| `experimental_network.enabled` | `boolean` | 启用沙箱化网络要求。当活动沙箱保持 command networking 关闭时，这不会授予网络访问。 |
| `experimental_network.http_port` | `integer` | 用于 `[experimental_network]` requirements 的 loopback HTTP 监听端口。 |
| `experimental_network.socks_port` | `integer` | 用于 `[experimental_network]` requirements 的 loopback SOCKS5 监听端口。 |
| `experimental_network.allow_upstream_proxy` | `boolean` | 允许沙箱化网络通过环境中的 upstream proxy 链式转发。 |
| `experimental_network.dangerously_allow_non_loopback_proxy` | `boolean` | 允许 `[experimental_network]` requirements 使用非 loopback 监听地址。启用后可能把监听器暴露到 localhost 之外。 |
| `experimental_network.dangerously_allow_all_unix_sockets` | `boolean` | 允许任意 Unix socket 目的地，而不是仅允许 allowlist 访问。仅在严格受控环境中使用。 |
| `experimental_network.domains` | `map<string, allow \| deny>` | 沙箱化网络的 map 形式的管理员域名策略。支持精确 host、仅匹配子域的 `*.example.com`、匹配根域与子域的 `**.example.com`，以及全局 `*` allow 规则；请优先使用有范围的规则，因为 `*` 会大范围开放公共出站访问。冲突时 `deny` 优先。不要与 `experimental_network.allowed_domains` 或 `experimental_network.denied_domains` 组合使用。 |
| `experimental_network.allowed_domains` | `array<string>` | 沙箱化网络的 list 形式的管理员允许规则。不要与 `experimental_network.domains` 组合使用。 |
| `experimental_network.denied_domains` | `array<string>` | 沙箱化网络的 list 形式的管理员拒绝规则。不要与 `experimental_network.domains` 组合使用。 |
| `experimental_network.managed_allowed_domains_only` | `boolean` | 当为 `true` 时，只有管理员管理的 allow 规则会在沙箱化网络要求处于活动状态时保持有效；用户添加的 allowlist 条目会被忽略。没有托管 allow 规则时，用户添加的 domain allow 规则不会保持有效。 |
| `experimental_network.unix_sockets` | `map<string, allow \| deny>` | 沙箱化网络的管理员管理的 Unix socket 策略。 |
| `experimental_network.allow_local_binding` | `boolean` | 允许沙箱化网络进行更宽泛的本地/私有网络访问。即使此值保持 `false`，精确本地 IP literal 或 `localhost` allow 规则仍可允许特定本地目标。 |
| `hooks` | `table` | 管理员强制的托管生命周期钩子。需要托管钩子目录，并使用与 `config.toml` 内联 `[hooks]` 相同的事件 schema。 |
| `hooks.managed_dir` | `string (absolute path)` | 包含 macOS 和 Linux 托管钩子脚本 的目录。Codex 会在加载托管钩子 前验证它是绝对路径且存在。 |
| `hooks.windows_managed_dir` | `string (absolute path)` | 包含 Windows 托管钩子脚本 的目录。Codex 会在加载托管钩子 前验证它是绝对路径且存在。 |
| `hooks.<Event>` | `array<table>` | 钩子事件的匹配器组，例如 `PreToolUse`、`PermissionRequest`、`PostToolUse`、`PreCompact`、`PostCompact`、`SessionStart`、`SubagentStart`、`SubagentStop`、`UserPromptSubmit` 或 `Stop`。 |
| `hooks.<Event>[].hooks` | `array<table>` | 某个匹配器组的钩子处理程序。当前支持命令钩子；prompt 和 agent 钩子处理程序会被解析但跳过。 |
| `hooks.<Event>[].hooks[].commandWindows` | `string` | 仅 Windows 使用的 command hook 命令覆盖。也接受 TOML 别名 `command_windows`。 |
| `permissions.filesystem.deny_read` | `array<string>` | 管理员强制的文件系统读取拒绝项。条目可以是路径或 glob patterns，用户不能通过本地 config 削弱它们。 |
| `mcp_servers` | `table` | 可启用 MCP 服务器的 allowlist。MCP 服务器必须同时匹配服务器名称（`<id>`）和 identity 才会启用。任何不在 allowlist 中（或 identity 不匹配）的已配置 MCP 服务器都会被禁用。 |
| `mcp_servers.<id>.identity` | `table` | 单个 MCP 服务器的 identity rule。设置 `command`（stdio）或 `url`（streamable HTTP）之一。 |
| `mcp_servers.<id>.identity.command` | `string` | 当 `mcp_servers.<id>.command` 与此命令匹配时，允许一个 MCP stdio 服务器。 |
| `mcp_servers.<id>.identity.url` | `string` | 当 `mcp_servers.<id>.url` 与此 URL 匹配时，允许一个 MCP streamable HTTP 服务器。 |
| `rules` | `table` | 与 `.rules` 文件合并的管理员强制命令规则。requirements 规则必须是限制性的。 |
| `rules.prefix_rules` | `array<table>` | 强制 prefix rules 列表。每条规则必须包含 `pattern` 和 `decision`。 |
| `rules.prefix_rules[].pattern` | `array<table>` | 用 pattern tokens 表达的命令前缀。每个 token 设置 `token` 或 `any_of` 之一。 |
| `rules.prefix_rules[].pattern[].token` | `string` | 此位置的单个 literal token。 |
| `rules.prefix_rules[].pattern[].any_of` | `array<string>` | 此位置允许的 alternative tokens 列表。 |
| `rules.prefix_rules[].decision` | `prompt \| forbidden` | 必填。requirements 规则只能 prompt 或 forbid（不能 allow）。 |
| `rules.prefix_rules[].justification` | `string` | 审批提示或拒绝消息中显示的可选非空理由。 |
