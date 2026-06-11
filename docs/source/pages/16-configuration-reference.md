### Configuration Reference

Source: [Configuration Reference](https://developers.openai.com/codex/config-reference.md)

Use this page as a searchable reference for Codex configuration files. For conceptual guidance and examples, start with [Config basics](https://developers.openai.com/codex/config-basic) and [Advanced Config](https://developers.openai.com/codex/config-advanced).

### `config.toml`

User-level configuration lives in `~/.codex/config.toml`. You can also add project-scoped overrides in `.codex/config.toml` files. Codex loads project-scoped config files only when you trust the project.

Project-scoped config can't override machine-local provider, auth,
host-owned app request metadata, notification, configuration profile selection,
or telemetry routing keys. Codex ignores `openai_base_url`,
`chatgpt_base_url`, `apps_mcp_product_sku`, `model_provider`,
`model_providers`, `notify`, `profile`, `profiles`,
`experimental_realtime_ws_base_url`, and `otel` when they appear in a
project-local `.codex/config.toml`; put provider, notification, and telemetry
keys in user-level config instead. Config [profile files](https://developers.openai.com/codex/config-advanced#profiles) live next to
`config.toml` as `$CODEX_HOME/profile-name.config.toml`; select one with
`--profile profile-name`.

For sandbox and approval keys (`approval_policy`, `sandbox_mode`, and `sandbox_workspace_write.*`), pair this reference with [Sandbox and approvals](https://developers.openai.com/codex/agent-approvals-security#sandbox-and-approvals), [Protected paths in writable roots](https://developers.openai.com/codex/agent-approvals-security#protected-paths-in-writable-roots), and [Network access](https://developers.openai.com/codex/agent-approvals-security#network-access). For beta permission profiles, see [Permissions](https://developers.openai.com/codex/permissions).

| Key | Type | Description |
| --- | --- | --- |
| `model` | `string` | Model to use (e.g., `gpt-5.5`). |
| `review_model` | `string` | Optional model override used by `/review` (defaults to the current session model). |
| `model_provider` | `string` | Provider id from `model_providers` (default: `openai`). |
| `openai_base_url` | `string` | Base URL override for the built-in `openai` model provider. |
| `model_context_window` | `number` | Context window tokens available to the active model. |
| `model_auto_compact_token_limit` | `number` | Token threshold that triggers automatic history compaction (unset uses model defaults). |
| `model_catalog_json` | `string (path)` | Optional path to a JSON model catalog loaded on startup. A selected `$CODEX_HOME/profile-name.config.toml` profile file can override this per profile. |
| `oss_provider` | `lmstudio \| ollama` | Default local provider used when running with `--oss` (defaults to prompting if unset). |
| `approval_policy` | `untrusted \| on-request \| never \| { granular = { sandbox_approval = bool, rules = bool, mcp_elicitations = bool, request_permissions = bool, skill_approval = bool } }` | Controls when Codex pauses for approval before executing commands. You can also use `approval_policy = { granular = { ... } }` to allow or auto-reject specific prompt categories while keeping other prompts interactive. `on-failure` is deprecated; use `on-request` for interactive runs or `never` for non-interactive runs. |
| `approval_policy.granular.sandbox_approval` | `boolean` | When `true`, sandbox escalation approval prompts are allowed to surface. |
| `approval_policy.granular.rules` | `boolean` | When `true`, approvals triggered by execpolicy `prompt` rules are allowed to surface. |
| `approval_policy.granular.mcp_elicitations` | `boolean` | When `true`, MCP elicitation prompts are allowed to surface instead of being auto-rejected. |
| `approval_policy.granular.request_permissions` | `boolean` | When `true`, prompts from the `request_permissions` tool are allowed to surface. |
| `approval_policy.granular.skill_approval` | `boolean` | When `true`, skill-script approval prompts are allowed to surface. |
| `approvals_reviewer` | `user \| auto_review` | Who reviews eligible approval prompts under `on-request` or granular approval policies. Defaults to `user`; `auto_review` uses the reviewer subagent. This setting doesn't change sandboxing or review actions already allowed inside the sandbox. |
| `auto_review.policy` | `string` | Local Markdown policy instructions for automatic review. Managed `guardian_policy_config` takes precedence. Blank values are ignored. |
| `allow_login_shell` | `boolean` | Allow shell-based tools to use login-shell semantics. Defaults to `true`; when `false`, `login = true` requests are rejected and omitted `login` defaults to non-login shells. |
| `sandbox_mode` | `read-only \| workspace-write \| danger-full-access` | Sandbox policy for filesystem and network access during command execution. |
| `sandbox_workspace_write.writable_roots` | `array<string>` | Additional writable roots when `sandbox_mode = "workspace-write"`. |
| `sandbox_workspace_write.network_access` | `boolean` | Allow outbound network access inside the workspace-write sandbox. |
| `sandbox_workspace_write.exclude_tmpdir_env_var` | `boolean` | Exclude `$TMPDIR` from writable roots in workspace-write mode. |
| `sandbox_workspace_write.exclude_slash_tmp` | `boolean` | Exclude `/tmp` from writable roots in workspace-write mode. |
| `windows.sandbox` | `unelevated \| elevated` | Windows-only native sandbox mode when running Codex natively on Windows. |
| `windows.sandbox_private_desktop` | `boolean` | Run the final sandboxed child process on a private desktop by default on native Windows. Set `false` only for compatibility with the older `Winsta0\\Default` behavior. |
| `notify` | `array<string>` | Command invoked for notifications; receives a JSON payload from Codex. |
| `check_for_update_on_startup` | `boolean` | Check for Codex updates on startup (set to false only when updates are centrally managed). |
| `feedback.enabled` | `boolean` | Enable feedback submission via `/feedback` across Codex surfaces (default: true). |
| `analytics.enabled` | `boolean` | Enable or disable analytics for this machine/profile. When unset, the client default applies. |
| `instructions` | `string` | Reserved for future use; prefer `model_instructions_file` or `AGENTS.md`. |
| `developer_instructions` | `string` | Additional developer instructions injected into the session (optional). |
| `log_dir` | `string (path)` | Directory where Codex writes log files; defaults to `$CODEX_HOME/log`. Setting this explicitly also enables the opt-in plaintext TUI log, `codex-tui.log`, in that directory. |
| `sqlite_home` | `string (path)` | Directory where Codex stores the SQLite-backed state DB used by agent jobs and other resumable runtime state. |
| `compact_prompt` | `string` | Inline override for the history compaction prompt. |
| `commit_attribution` | `string` | Commit co-author trailer used when `[features].codex_git_commit` is enabled. Defaults to `Codex <noreply@openai.com>`; set `""` to disable. |
| `model_instructions_file` | `string (path)` | Replacement for built-in instructions instead of `AGENTS.md`. |
| `personality` | `none \| friendly \| pragmatic` | Default communication style for models that advertise `supportsPersonality`; can be overridden per thread/turn or via `/personality`. |
| `service_tier` | `string` | Preferred service tier for new turns. Built-in values include `flex` and `fast`; legacy `fast` config maps to the request value `priority`, and catalog-provided tier IDs can also be stored. |
| `experimental_compact_prompt_file` | `string (path)` | Load the compaction prompt override from a file (experimental). |
| `skills.config` | `array<object>` | Per-skill enablement overrides stored in config.toml. |
| `skills.config.<index>.path` | `string (path)` | Path to a skill folder containing `SKILL.md`. |
| `skills.config.<index>.enabled` | `boolean` | Enable or disable the referenced skill. |
| `apps.<id>.enabled` | `boolean` | Enable or disable a specific app/connector by id (default: true). |
| `apps._default.enabled` | `boolean` | Default app enabled state for all apps unless overridden per app. |
| `apps._default.destructive_enabled` | `boolean` | Default allow/deny for app tools with `destructive_hint = true`. |
| `apps._default.open_world_enabled` | `boolean` | Default allow/deny for app tools with `open_world_hint = true`. |
| `apps.<id>.destructive_enabled` | `boolean` | Allow or block tools in this app that advertise `destructive_hint = true`. |
| `apps.<id>.open_world_enabled` | `boolean` | Allow or block tools in this app that advertise `open_world_hint = true`. |
| `apps.<id>.default_tools_enabled` | `boolean` | Default enabled state for tools in this app unless a per-tool override exists. |
| `apps.<id>.default_tools_approval_mode` | `auto \| prompt \| approve` | Default approval behavior for tools in this app unless a per-tool override exists. |
| `apps.<id>.tools.<tool>.enabled` | `boolean` | Per-tool enabled override for an app tool (for example `repos/list`). |
| `apps.<id>.tools.<tool>.approval_mode` | `auto \| prompt \| approve` | Per-tool approval behavior override for a single app tool. |
| `tool_suggest.discoverables` | `array<table>` | Allow tool suggestions for additional discoverable connectors or plugins. Each entry uses `type = "connector"` or `"plugin"` and an `id`. |
| `tool_suggest.disabled_tools` | `array<table>` | Disable suggestions for specific discoverable connectors or plugins. Each entry uses `type = "connector"` or `"plugin"` and an `id`. |
| `features.apps` | `boolean` | Enable ChatGPT Apps/connectors support (experimental). |
| `features.hooks` | `boolean` | Enable lifecycle hooks loaded from `hooks.json` or inline `[hooks]` config. `features.codex_hooks` is a deprecated alias. |
| `features.codex_git_commit` | `boolean` | Enable Codex-generated git commits. When enabled, Codex uses `commit_attribution` to append a `Co-authored-by:` trailer to generated commit messages. |
| `hooks` | `table` | Lifecycle hooks configured inline in `config.toml`. Uses the same event schema as `hooks.json`; see the Hooks guide for examples and supported events. |
| `hooks.<Event>` | `array<table>` | Matcher groups for hook events such as `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SessionStart`, `SubagentStart`, `SubagentStop`, `UserPromptSubmit`, or `Stop`. |
| `hooks.<Event>[].hooks` | `array<table>` | Hook handlers for a matcher group. Command hooks are currently supported; prompt and agent hook handlers are parsed but skipped. |
| `hooks.<Event>[].hooks[].commandWindows` | `string` | Windows-only command override for command hooks. The TOML alias `command_windows` is also accepted. |
| `features.memories` | `boolean` | Enable [Memories](https://developers.openai.com/codex/memories) (off by default). |
| `mcp_servers.<id>.command` | `string` | Launcher command for an MCP stdio server. |
| `mcp_servers.<id>.args` | `array<string>` | Arguments passed to the MCP stdio server command. |
| `mcp_servers.<id>.env` | `map<string,string>` | Environment variables forwarded to the MCP stdio server. |
| `mcp_servers.<id>.env_vars` | `array<string \| { name = string, source = "local" \| "remote" }>` | Additional environment variables to whitelist for an MCP stdio server. String entries default to `source = "local"`; use `source = "remote"` only with executor-backed remote stdio. |
| `mcp_servers.<id>.cwd` | `string` | Working directory for the MCP stdio server process. |
| `mcp_servers.<id>.url` | `string` | Endpoint for an MCP streamable HTTP server. |
| `mcp_servers.<id>.bearer_token_env_var` | `string` | Environment variable sourcing the bearer token for an MCP HTTP server. |
| `mcp_servers.<id>.http_headers` | `map<string,string>` | Static HTTP headers included with each MCP HTTP request. |
| `mcp_servers.<id>.env_http_headers` | `map<string,string>` | HTTP headers populated from environment variables for an MCP HTTP server. |
| `mcp_servers.<id>.enabled` | `boolean` | Disable an MCP server without removing its configuration. |
| `mcp_servers.<id>.required` | `boolean` | When true, fail startup/resume if this enabled MCP server cannot initialize. |
| `mcp_servers.<id>.startup_timeout_sec` | `number` | Override the default 10s startup timeout for an MCP server. |
| `mcp_servers.<id>.startup_timeout_ms` | `number` | Alias for `startup_timeout_sec` in milliseconds. |
| `mcp_servers.<id>.tool_timeout_sec` | `number` | Override the default 60s per-tool timeout for an MCP server. |
| `mcp_servers.<id>.enabled_tools` | `array<string>` | Allow list of tool names exposed by the MCP server. |
| `mcp_servers.<id>.disabled_tools` | `array<string>` | Deny list applied after `enabled_tools` for the MCP server. |
| `mcp_servers.<id>.default_tools_approval_mode` | `auto \| prompt \| approve` | Default approval behavior for MCP tools on this server unless a per-tool override exists. |
| `mcp_servers.<id>.tools.<tool>.approval_mode` | `auto \| prompt \| approve` | Per-tool approval behavior override for one MCP tool on this server. |
| `mcp_servers.<id>.scopes` | `array<string>` | OAuth scopes to request when authenticating to that MCP server. |
| `mcp_servers.<id>.oauth_resource` | `string` | Optional RFC 8707 OAuth resource parameter to include during MCP login. |
| `mcp_servers.<id>.experimental_environment` | `local \| remote` | Experimental placement for an MCP server. `remote` starts stdio servers through a remote executor environment; streamable HTTP remote placement is not implemented. |
| `agents.max_threads` | `number` | Maximum number of agent threads that can be open concurrently. Defaults to `6` when unset. |
| `agents.max_depth` | `number` | Maximum nesting depth allowed for spawned agent threads (root sessions start at depth 0; default: 1). |
| `agents.job_max_runtime_seconds` | `number` | Default per-worker timeout for `spawn_agents_on_csv` jobs. When unset, the tool falls back to 1800 seconds per worker. |
| `agents.<name>.description` | `string` | Role guidance shown to Codex when choosing and spawning that agent type. |
| `agents.<name>.config_file` | `string (path)` | Path to a TOML config layer for that role; relative paths resolve from the config file that declares the role. |
| `agents.<name>.nickname_candidates` | `array<string>` | Optional pool of display nicknames for spawned agents in that role. |
| `memories.generate_memories` | `boolean` | When `false`, newly created threads are not stored as memory-generation inputs. Defaults to `true`. |
| `memories.use_memories` | `boolean` | When `false`, Codex skips injecting existing memories into future sessions. Defaults to `true`. |
| `memories.disable_on_external_context` | `boolean` | When `true`, threads that use external context such as MCP tool calls, web search, or tool search are kept out of memory generation. Defaults to `false`. Legacy alias: `memories.no_memories_if_mcp_or_web_search`. |
| `memories.max_raw_memories_for_consolidation` | `number` | Maximum recent raw memories retained for global consolidation. Defaults to `256` and is capped at `4096`. |
| `memories.max_unused_days` | `number` | Maximum days since a memory was last used before it becomes ineligible for consolidation. Defaults to `30` and is clamped to `0`-`365`. |
| `memories.max_rollout_age_days` | `number` | Maximum age of threads considered for memory generation. Defaults to `30` and is clamped to `0`-`90`. |
| `memories.max_rollouts_per_startup` | `number` | Maximum rollout candidates processed per startup pass. Defaults to `16` and is capped at `128`. |
| `memories.min_rollout_idle_hours` | `number` | Minimum idle time before a thread is considered for memory generation. Defaults to `6` and is clamped to `1`-`48`. |
| `memories.min_rate_limit_remaining_percent` | `number` | Minimum remaining percentage required in Codex rate-limit windows before memory generation starts. Defaults to `25` and is clamped to `0`-`100`. |
| `memories.extract_model` | `string` | Optional model override for per-thread memory extraction. |
| `memories.consolidation_model` | `string` | Optional model override for global memory consolidation. |
| `features.unified_exec` | `boolean` | Use the unified PTY-backed exec tool (stable; enabled by default except on Windows). |
| `features.shell_snapshot` | `boolean` | Snapshot shell environment to speed up repeated commands (stable; on by default). |
| `features.undo` | `boolean` | Enable undo support (stable; off by default). |
| `features.multi_agent` | `boolean` | Enable multi-agent collaboration tools (`spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, and `close_agent`) (stable; on by default). |
| `features.personality` | `boolean` | Enable personality selection controls (stable; on by default). |
| `features.network_proxy` | `boolean \| table` | Enable sandboxed networking. Use a table form when setting network policy options such as `domains` (experimental; off by default). |
| `features.network_proxy.enabled` | `boolean` | Enable sandboxed networking. Defaults to `false`. |
| `features.network_proxy.domains` | `map<string, allow \| deny>` | Domain policy for sandboxed networking. Unset by default, which means no external destinations are allowed until you add `allow` rules. Supports exact hosts, `*.example.com` for subdomains only, `**.example.com` for apex plus subdomains, and global `*` allow rules; prefer scoped rules because `*` broadly opens public outbound access. Add `deny` rules for blocked destinations; `deny` wins on conflicts. |
| `features.network_proxy.unix_sockets` | `map<string, allow \| deny>` | Unix socket policy for sandboxed networking. Unset by default; add `allow` entries for permitted sockets. |
| `features.network_proxy.allow_local_binding` | `boolean` | Allow broader local/private-network access. Defaults to `false`; exact local IP literal or `localhost` allow rules can still permit specific local targets. |
| `features.network_proxy.enable_socks5` | `boolean` | Expose SOCKS5 support. Defaults to `true`. |
| `features.network_proxy.enable_socks5_udp` | `boolean` | Allow UDP over SOCKS5. Defaults to `true`. |
| `features.network_proxy.allow_upstream_proxy` | `boolean` | Allow chaining through an upstream proxy from the environment. Defaults to `true`. |
| `features.network_proxy.dangerously_allow_non_loopback_proxy` | `boolean` | Permit non-loopback listener addresses. Defaults to `false`; enabling it can expose proxy listeners beyond localhost. |
| `features.network_proxy.dangerously_allow_all_unix_sockets` | `boolean` | Permit arbitrary Unix socket destinations instead of allowlist-only access. Defaults to `false`; use only in tightly controlled environments. |
| `features.network_proxy.proxy_url` | `string` | HTTP listener URL for sandboxed networking. Defaults to `"http://127.0.0.1:3128"`. |
| `features.network_proxy.socks_url` | `string` | SOCKS5 listener URL. Defaults to `"http://127.0.0.1:8081"`. |
| `features.web_search` | `boolean` | Deprecated legacy toggle; prefer the top-level `web_search` setting. |
| `features.web_search_cached` | `boolean` | Deprecated legacy toggle. When `web_search` is unset, true maps to `web_search = "cached"`. |
| `features.web_search_request` | `boolean` | Deprecated legacy toggle. When `web_search` is unset, true maps to `web_search = "live"`. |
| `features.shell_tool` | `boolean` | Enable the default `shell` tool for running commands (stable; on by default). |
| `features.enable_request_compression` | `boolean` | Compress streaming request bodies with zstd when supported (stable; on by default). |
| `features.skill_mcp_dependency_install` | `boolean` | Allow prompting and installing missing MCP dependencies for skills (stable; on by default). |
| `features.fast_mode` | `boolean` | Enable model-catalog service tier selection in the TUI, including Fast-tier commands when the active model advertises them (stable; on by default). |
| `features.prevent_idle_sleep` | `boolean` | Prevent the machine from sleeping while a turn is actively running (experimental; off by default). |
| `suppress_unstable_features_warning` | `boolean` | Suppress the warning that appears when under-development feature flags are enabled. |
| `model_providers.<id>` | `table` | Custom provider definition. Built-in provider IDs (`openai`, `ollama`, and `lmstudio`) are reserved and cannot be overridden. |
| `model_providers.<id>.name` | `string` | Display name for a custom model provider. |
| `model_providers.<id>.base_url` | `string` | API base URL for the model provider. |
| `model_providers.<id>.env_key` | `string` | Environment variable supplying the provider API key. |
| `model_providers.<id>.env_key_instructions` | `string` | Optional setup guidance for the provider API key. |
| `model_providers.<id>.experimental_bearer_token` | `string` | Direct bearer token for the provider (discouraged; use `env_key`). |
| `model_providers.<id>.requires_openai_auth` | `boolean` | The provider uses OpenAI authentication (defaults to false). |
| `model_providers.<id>.wire_api` | `responses` | Protocol used by the provider. `responses` is the only supported value, and it is the default when omitted. |
| `model_providers.<id>.query_params` | `map<string,string>` | Extra query parameters appended to provider requests. |
| `model_providers.<id>.http_headers` | `map<string,string>` | Static HTTP headers added to provider requests. |
| `model_providers.<id>.env_http_headers` | `map<string,string>` | HTTP headers populated from environment variables when present. |
| `model_providers.<id>.request_max_retries` | `number` | Retry count for HTTP requests to the provider (default: 4). |
| `model_providers.<id>.stream_max_retries` | `number` | Retry count for SSE streaming interruptions (default: 5). |
| `model_providers.<id>.stream_idle_timeout_ms` | `number` | Idle timeout for SSE streams in milliseconds (default: 300000). |
| `model_providers.<id>.supports_websockets` | `boolean` | Whether that provider supports the Responses API WebSocket transport. |
| `model_providers.<id>.auth` | `table` | Command-backed bearer token configuration for a custom provider. Do not combine with `env_key`, `experimental_bearer_token`, or `requires_openai_auth`. |
| `model_providers.<id>.auth.command` | `string` | Command to run when Codex needs a bearer token. The command must print the token to stdout. |
| `model_providers.<id>.auth.args` | `array<string>` | Arguments passed to the token command. |
| `model_providers.<id>.auth.timeout_ms` | `number` | Maximum token command runtime in milliseconds (default: 5000). |
| `model_providers.<id>.auth.refresh_interval_ms` | `number` | How often Codex proactively refreshes the token in milliseconds (default: 300000). Set to `0` to refresh only after an authentication retry. |
| `model_providers.<id>.auth.cwd` | `string (path)` | Working directory for the token command. |
| `model_providers.amazon-bedrock.aws.profile` | `string` | AWS profile name used by the built-in `amazon-bedrock` provider. |
| `model_providers.amazon-bedrock.aws.region` | `string` | AWS region used by the built-in `amazon-bedrock` provider. |
| `model_reasoning_effort` | `minimal \| low \| medium \| high \| xhigh` | Adjust reasoning effort for supported models (Responses API only; `xhigh` is model-dependent). |
| `plan_mode_reasoning_effort` | `none \| minimal \| low \| medium \| high \| xhigh` | Plan-mode-specific reasoning override. When unset, Plan mode uses its built-in preset default. |
| `model_reasoning_summary` | `auto \| concise \| detailed \| none` | Select reasoning summary detail or disable summaries entirely. |
| `model_verbosity` | `low \| medium \| high` | Optional GPT-5 Responses API verbosity override; when unset, the selected model/preset default is used. |
| `model_supports_reasoning_summaries` | `boolean` | Force Codex to send or not send reasoning metadata. |
| `shell_environment_policy.inherit` | `all \| core \| none` | Baseline environment inheritance when spawning subprocesses. |
| `shell_environment_policy.ignore_default_excludes` | `boolean` | Keep variables containing KEY/SECRET/TOKEN before other filters run. |
| `shell_environment_policy.exclude` | `array<string>` | Glob patterns for removing environment variables after the defaults. |
| `shell_environment_policy.include_only` | `array<string>` | Whitelist of patterns; when set only matching variables are kept. |
| `shell_environment_policy.set` | `map<string,string>` | Explicit environment overrides injected into every subprocess. |
| `shell_environment_policy.experimental_use_profile` | `boolean` | Use the user shell profile when spawning subprocesses. |
| `project_root_markers` | `array<string>` | List of project root marker filenames; used when searching parent directories for the project root. |
| `project_doc_max_bytes` | `number` | Maximum bytes read from `AGENTS.md` when building project instructions. |
| `project_doc_fallback_filenames` | `array<string>` | Additional filenames to try when `AGENTS.md` is missing. |
| `history.persistence` | `save-all \| none` | Control whether Codex saves session transcripts to history.jsonl. |
| `tool_output_token_limit` | `number` | Token budget for storing individual tool/function outputs in history. |
| `background_terminal_max_timeout` | `number` | Maximum poll window in milliseconds for empty `write_stdin` polls (background terminal polling). Default: `300000` (5 minutes). Replaces the older `background_terminal_timeout` key. |
| `history.max_bytes` | `number` | If set, caps the history file size in bytes by dropping oldest entries. |
| `file_opener` | `vscode \| vscode-insiders \| windsurf \| cursor \| none` | URI scheme used to open citations from Codex output (default: `vscode`). |
| `otel.environment` | `string` | Environment tag applied to emitted OpenTelemetry events (default: `dev`). |
| `otel.exporter` | `none \| otlp-http \| otlp-grpc` | Select the OpenTelemetry exporter and provide any endpoint metadata. |
| `otel.trace_exporter` | `none \| otlp-http \| otlp-grpc` | Select the OpenTelemetry trace exporter and provide any endpoint metadata. |
| `otel.metrics_exporter` | `none \| statsig \| otlp-http \| otlp-grpc` | Select the OpenTelemetry metrics exporter (defaults to `statsig`). |
| `otel.log_user_prompt` | `boolean` | Opt in to exporting raw user prompts with OpenTelemetry logs. |
| `otel.exporter.<id>.endpoint` | `string` | Exporter endpoint for OTEL logs. |
| `otel.exporter.<id>.protocol` | `binary \| json` | Protocol used by the OTLP/HTTP exporter. |
| `otel.exporter.<id>.headers` | `map<string,string>` | Static headers included with OTEL exporter requests. |
| `otel.trace_exporter.<id>.endpoint` | `string` | Trace exporter endpoint for OTEL logs. |
| `otel.trace_exporter.<id>.protocol` | `binary \| json` | Protocol used by the OTLP/HTTP trace exporter. |
| `otel.trace_exporter.<id>.headers` | `map<string,string>` | Static headers included with OTEL trace exporter requests. |
| `otel.exporter.<id>.tls.ca-certificate` | `string` | CA certificate path for OTEL exporter TLS. |
| `otel.exporter.<id>.tls.client-certificate` | `string` | Client certificate path for OTEL exporter TLS. |
| `otel.exporter.<id>.tls.client-private-key` | `string` | Client private key path for OTEL exporter TLS. |
| `otel.trace_exporter.<id>.tls.ca-certificate` | `string` | CA certificate path for OTEL trace exporter TLS. |
| `otel.trace_exporter.<id>.tls.client-certificate` | `string` | Client certificate path for OTEL trace exporter TLS. |
| `otel.trace_exporter.<id>.tls.client-private-key` | `string` | Client private key path for OTEL trace exporter TLS. |
| `tui` | `table` | TUI-specific options such as enabling inline desktop notifications. |
| `tui.notifications` | `boolean \| array<string>` | Enable TUI notifications; optionally restrict to specific event types. |
| `tui.notification_method` | `auto \| osc9 \| bel` | Notification method for terminal notifications (default: auto). |
| `tui.notification_condition` | `unfocused \| always` | Control whether TUI notifications fire only when the terminal is unfocused or regardless of focus. Defaults to `unfocused`. |
| `tui.animations` | `boolean` | Enable terminal animations (welcome screen, shimmer, spinner) (default: true). |
| `tui.alternate_screen` | `auto \| always \| never` | Control alternate screen usage for the TUI (default: auto; auto skips it in Zellij to preserve scrollback). |
| `tui.vim_mode_default` | `boolean` | Start the composer in Vim normal mode instead of insert mode (default: false). You can still toggle it per session with `/vim`. |
| `tui.raw_output_mode` | `boolean` | Start the TUI in raw scrollback mode for copy-friendly terminal selection (default: false). You can toggle it with `/raw` or the default `alt-r` key binding. |
| `tui.show_tooltips` | `boolean` | Show onboarding tooltips in the TUI welcome screen (default: true). |
| `tui.status_line` | `array<string> \| null` | Ordered list of TUI footer status-line item identifiers. `null` disables the status line. |
| `tui.terminal_title` | `array<string> \| null` | Ordered list of terminal window/tab title item identifiers. Defaults to `["spinner", "project"]`; `null` disables title updates. |
| `tui.theme` | `string` | Syntax-highlighting theme override (kebab-case theme name). |
| `tui.keymap.<context>.<action>` | `string \| array<string>` | Keyboard shortcut binding for a TUI action. Supported contexts include `global`, `chat`, `composer`, `editor`, `vim_normal`, `vim_operator`, `vim_text_object`, `pager`, `list`, and `approval`. Selected composer actions fall back to matching `tui.keymap.global` bindings; context-specific bindings take precedence when supported. |
| `tui.keymap.<context>.<action> = []` | `empty array` | Unbind the action in that keymap context. Key names use normalized strings such as `ctrl-a`, `shift-enter`, `page-down`, or `minus`. |
| `plugins.<plugin>.mcp_servers.<server>.enabled` | `boolean` | Enable or disable an MCP server bundled by an installed plugin without changing the plugin manifest. |
| `plugins.<plugin>.mcp_servers.<server>.default_tools_approval_mode` | `auto \| prompt \| approve` | Default approval behavior for tools on a plugin-provided MCP server. |
| `plugins.<plugin>.mcp_servers.<server>.enabled_tools` | `array<string>` | Allow list of tools exposed from a plugin-provided MCP server. |
| `plugins.<plugin>.mcp_servers.<server>.disabled_tools` | `array<string>` | Deny list applied after `enabled_tools` for a plugin-provided MCP server. |
| `plugins.<plugin>.mcp_servers.<server>.tools.<tool>.approval_mode` | `auto \| prompt \| approve` | Per-tool approval behavior override for a plugin-provided MCP tool. |
| `tui.model_availability_nux.<model>` | `integer` | Internal startup-tooltip state keyed by model slug. |
| `hide_agent_reasoning` | `boolean` | Suppress reasoning events in both the TUI and `codex exec` output. |
| `show_raw_agent_reasoning` | `boolean` | Surface raw reasoning content when the active model emits it. |
| `disable_paste_burst` | `boolean` | Disable burst-paste detection in the TUI. |
| `windows_wsl_setup_acknowledged` | `boolean` | Track Windows onboarding acknowledgement (Windows only). |
| `chatgpt_base_url` | `string` | Override the base URL used during the ChatGPT login flow. |
| `cli_auth_credentials_store` | `file \| keyring \| auto` | Control where the CLI stores cached credentials (file-based auth.json vs OS keychain). |
| `mcp_oauth_credentials_store` | `auto \| file \| keyring` | Preferred store for MCP OAuth credentials. |
| `mcp_oauth_callback_port` | `integer` | Optional fixed port for the local HTTP callback server used during MCP OAuth login. When unset, Codex binds to an ephemeral port chosen by the OS. |
| `mcp_oauth_callback_url` | `string` | Optional redirect URI override for MCP OAuth login (for example, a devbox ingress URL). `mcp_oauth_callback_port` still controls the callback listener port. |
| `experimental_use_unified_exec_tool` | `boolean` | Legacy name for enabling unified exec; prefer `[features].unified_exec` or `codex --enable unified_exec`. |
| `tools.web_search` | `boolean \| { context_size = "low\|medium\|high", allowed_domains = [string], location = { country, region, city, timezone } }` | Optional web search tool configuration. The legacy boolean form is still accepted, but the object form lets you set search context size, allowed domains, and approximate user location. |
| `tools.view_image` | `boolean` | Enable the local-image attachment tool `view_image`. |
| `web_search` | `disabled \| cached \| live` | Web search mode (default: `"cached"`; cached uses an OpenAI-maintained index and does not fetch live pages; if you use `--yolo` or another full access sandbox setting, it defaults to `"live"`). Use `"live"` to fetch the most recent data from the web, or `"disabled"` to remove the tool. |
| `default_permissions` | `string` | Name of the default permissions profile to apply to sandboxed tool calls. Built-ins are `:read-only`, `:workspace`, and `:danger-full-access`; custom profile names require matching `[permissions.<name>]` tables. Don't combine with `sandbox_mode` or `[sandbox_workspace_write]`. |
| `permissions.<name>.description` | `string` | Human-readable description for this named profile. A profile does not inherit its parent's description through `extends`. |
| `permissions.<name>.extends` | `string` | Optional parent profile applied before this named profile. Set it to another named profile, `:read-only`, or `:workspace`; `:danger-full-access`, undefined parents, and cycles are rejected. |
| `permissions.<name>.workspace_roots` | `table` | Profile-defined workspace roots that receive `:workspace_roots` filesystem rules alongside the session's runtime workspace roots. |
| `permissions.<name>.workspace_roots.<path>` | `boolean` | Opt a path into the profile's workspace root set when `true`. Disabled entries remain inactive. |
| `permissions.<name>.filesystem` | `table` | Named filesystem permission profile. Each key is an absolute path or special token such as `:minimal` or `:workspace_roots`. |
| `permissions.<name>.filesystem.glob_scan_max_depth` | `number` | Maximum depth for expanding deny-read glob patterns on platforms that snapshot matches before sandbox startup. Must be at least `1` when set. |
| `permissions.<name>.filesystem.<path-or-glob>` | `"read" \| "write" \| "deny" \| table` | Grant direct access for a path, glob pattern, or special token, or scope nested entries under that root. Use `"deny"` to deny reads for matching paths. |
| `permissions.<name>.filesystem.":workspace_roots".<subpath-or-glob>` | `"read" \| "write" \| "deny"` | Scoped filesystem access relative to each effective workspace root. Use `"."` for the root itself; glob subpaths such as `"**/*.env"` can deny reads with `"deny"`. |
| `permissions.<name>.network.enabled` | `boolean` | Enable network access for this named permissions profile. This changes the sandbox network policy; it does not start the network proxy by itself. |
| `permissions.<name>.network.proxy_url` | `string` | HTTP listener URL used when this permissions profile enables sandboxed networking. |
| `permissions.<name>.network.enable_socks5` | `boolean` | Expose SOCKS5 support when this permissions profile enables sandboxed networking. |
| `permissions.<name>.network.socks_url` | `string` | SOCKS5 proxy endpoint used by this permissions profile. |
| `permissions.<name>.network.enable_socks5_udp` | `boolean` | Allow UDP over the SOCKS5 listener when enabled. |
| `permissions.<name>.network.allow_upstream_proxy` | `boolean` | Allow sandboxed networking to chain through another upstream proxy. |
| `permissions.<name>.network.dangerously_allow_non_loopback_proxy` | `boolean` | Permit non-loopback bind addresses for sandboxed networking listeners. Enabling it can expose listeners beyond localhost. |
| `permissions.<name>.network.dangerously_allow_all_unix_sockets` | `boolean` | Allow arbitrary Unix socket destinations instead of the default restricted set. Use only in tightly controlled environments. |
| `permissions.<name>.network.mode` | `limited \| full` | Network proxy mode used for subprocess traffic. |
| `permissions.<name>.network.domains` | `table` | Domain rules for sandboxed networking. Supports exact hosts, `*.example.com` for subdomains only, `**.example.com` for apex plus subdomains, and global `*` allow rules. `deny` wins on conflicts. |
| `permissions.<name>.network.domains.<pattern>` | `allow \| deny` | Allow or deny an exact host or scoped wildcard pattern such as `*.example.com` or `**.example.com`. |
| `permissions.<name>.network.unix_sockets` | `table` | Unix socket allowlist overrides for sandboxed networking. Use socket paths as keys; `allow` adds a path, and `deny` rejects it. |
| `permissions.<name>.network.unix_sockets.<path>` | `allow \| deny` | Add an absolute Unix socket path to the effective allowlist with `allow`, or reject it with `deny`. Denied entries are omitted from the effective allowlist. |
| `permissions.<name>.network.allow_local_binding` | `boolean` | Permit broader local/private-network access through sandboxed networking. Exact local IP literal or `localhost` allow rules can still permit specific local targets when this stays `false`. |
| `projects.<path>.trust_level` | `string` | Mark a project or worktree as trusted or untrusted (`"trusted"` \| `"untrusted"`). Untrusted projects skip project-scoped `.codex/` layers, including project-local config, hooks, and rules. |
| `notice.hide_full_access_warning` | `boolean` | Track acknowledgement of the full access warning prompt. |
| `notice.hide_world_writable_warning` | `boolean` | Track acknowledgement of the Windows world-writable directories warning. |
| `notice.hide_rate_limit_model_nudge` | `boolean` | Track opt-out of the rate limit model switch reminder. |
| `notice.hide_gpt5_1_migration_prompt` | `boolean` | Track acknowledgement of the GPT-5.1 migration prompt. |
| `notice.hide_gpt-5.1-codex-max_migration_prompt` | `boolean` | Track acknowledgement of the gpt-5.1-codex-max migration prompt. |
| `notice.model_migrations` | `map<string,string>` | Track acknowledged model migrations as old->new mappings. |
| `forced_login_method` | `chatgpt \| api` | Restrict Codex to a specific authentication method. |
| `forced_chatgpt_workspace_id` | `string (uuid)` | Limit ChatGPT logins to a specific workspace identifier. |

You can find the latest JSON schema for `config.toml` [here](https://developers.openai.com/codex/config-schema.json).

To get autocompletion and diagnostics when editing `config.toml` in VS Code or Cursor, you can install the [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml) extension and add this line to the top of your `config.toml`:

```toml
#:schema https://developers.openai.com/codex/config-schema.json
```

Note: Rename `experimental_instructions_file` to `model_instructions_file`. Codex deprecates the old key; update existing configs to the new name.

### `requirements.toml`

`requirements.toml` is an admin-enforced configuration file that constrains security-sensitive settings users can't override. For details, locations, and examples, see [Admin-enforced requirements](https://developers.openai.com/codex/enterprise/managed-configuration#admin-enforced-requirements-requirementstoml).

For ChatGPT Business and Enterprise users, Codex can also apply cloud-fetched
requirements. See the security page for precedence details.

Use `[features]` in `requirements.toml` to pin feature flags by the same
canonical keys that `config.toml` uses. Omitted keys remain unconstrained.

Managed permission-profile allowlists require Codex 0.138.0 or later. Codex
0.137.0 and earlier ignore `allowed_permission_profiles` and managed
`default_permissions`.

Use `allowed_sandbox_modes` with `sandbox_mode`. For permission-profile
deployments, use `allowed_permission_profiles` with managed
`default_permissions`.

| Key | Type | Description |
| --- | --- | --- |
| `allowed_approval_policies` | `array<string>` | Allowed values for `approval_policy` (for example `untrusted`, `on-request`, `never`, and `granular`). |
| `allowed_approvals_reviewers` | `array<string>` | Allowed values for `approvals_reviewer`, such as `user` and `auto_review`. |
| `guardian_policy_config` | `string` | Managed Markdown policy instructions for automatic review. This takes precedence over local `[auto_review].policy`. Blank values are ignored. |
| `allowed_permission_profiles` | `table<boolean>` | Complete list of allowed permission profiles. Profiles set to `true` are allowed. Profiles that are omitted or set to `false` are denied, including profiles added in future versions. When requirements sources are combined, entries are matched by profile name. |
| `allowed_permission_profiles.<name>` | `boolean` | Allow or deny a built-in or custom permission profile defined in a loaded config or requirements source. An earlier requirements source can use `false` to turn off a profile allowed by a later source. |
| `default_permissions` | `string` | Managed default permission profile. The profile must be allowed by `allowed_permission_profiles`. Set this explicitly for predictable behavior; if omitted, Codex defaults to `:workspace` only when both `:workspace` and `:read-only` are explicitly allowed. |
| `permissions.<name>` | `table` | Admin-defined permission profile. The name can't start with `:`, use the reserved name `filesystem`, or duplicate a profile from a loaded config. Uses the same profile fields as `config.toml`; see the Permissions guide for the complete profile schema. |
| `allowed_sandbox_modes` | `array<string>` | Allowed values for `sandbox_mode`. |
| `windows.allowed_sandbox_implementations` | `array<string>` | Allowed native Windows sandbox implementations for `windows.sandbox` (`elevated` and `unelevated`). The list must not be empty. When both are allowed and no mode is selected, Codex prefers `elevated`. |
| `remote_sandbox_config` | `array<table>` | Host-specific sandbox requirements. The first entry whose `hostname_patterns` match the resolved host name overrides top-level `allowed_sandbox_modes` for that requirements source. Host-specific entries currently override sandbox modes only. |
| `remote_sandbox_config[].hostname_patterns` | `array<string>` | Case-insensitive host name patterns. Supports `*` for any sequence of characters and `?` for one character. |
| `remote_sandbox_config[].allowed_sandbox_modes` | `array<string>` | Allowed sandbox modes to apply when this host-specific entry matches. |
| `allowed_web_search_modes` | `array<string>` | Allowed values for `web_search` (`disabled`, `cached`, `live`). `disabled` is always allowed; an empty list effectively allows only `disabled`. |
| `allow_managed_hooks_only` | `boolean` | When `true`, Codex skips user, project, session, and plugin hooks while still allowing managed hooks from `requirements.toml` and other managed config layers. |
| `features.plugin_sharing` | `boolean` | Set to `false` in cloud-managed `requirements.toml` to disable workspace sharing for locally built plugins. |
| `features` | `table` | Pinned feature values keyed by the canonical names from `config.toml`'s `[features]` table. |
| `features.<name>` | `boolean` | Require a specific canonical feature key to stay enabled or disabled. |
| `features.in_app_browser` | `boolean` | Set to `false` in `requirements.toml` to disable the in-app browser pane. |
| `features.browser_use` | `boolean` | Set to `false` in `requirements.toml` to disable Browser Use and Browser Agent availability. |
| `features.computer_use` | `boolean` | Set to `false` in `requirements.toml` to disable Computer Use availability and related install or enablement flows. |
| `experimental_network` | `table` | Network access requirements enforced from `requirements.toml`. These constraints are separate from `features.network_proxy` and can configure sandboxed networking without the user feature flag. |
| `experimental_network.enabled` | `boolean` | Enable sandboxed networking requirements. This does not grant network access when the active sandbox keeps command networking off. |
| `experimental_network.http_port` | `integer` | Loopback HTTP listener port to use for `[experimental_network]` requirements. |
| `experimental_network.socks_port` | `integer` | Loopback SOCKS5 listener port to use for `[experimental_network]` requirements. |
| `experimental_network.allow_upstream_proxy` | `boolean` | Allow sandboxed networking to chain through an upstream proxy from the environment. |
| `experimental_network.dangerously_allow_non_loopback_proxy` | `boolean` | Permit non-loopback listener addresses for `[experimental_network]` requirements. Enabling it can expose listeners beyond localhost. |
| `experimental_network.dangerously_allow_all_unix_sockets` | `boolean` | Permit arbitrary Unix socket destinations instead of allowlist-only access. Use only in tightly controlled environments. |
| `experimental_network.domains` | `map<string, allow \| deny>` | Map-shaped administrator domain policy for sandboxed networking. Supports exact hosts, `*.example.com` for subdomains only, `**.example.com` for apex plus subdomains, and global `*` allow rules; prefer scoped rules because `*` broadly opens public outbound access. `deny` wins on conflicts. Do not combine this with `experimental_network.allowed_domains` or `experimental_network.denied_domains`. |
| `experimental_network.allowed_domains` | `array<string>` | List-shaped administrator allow rules for sandboxed networking. Do not combine this with `experimental_network.domains`. |
| `experimental_network.denied_domains` | `array<string>` | List-shaped administrator deny rules for sandboxed networking. Do not combine this with `experimental_network.domains`. |
| `experimental_network.managed_allowed_domains_only` | `boolean` | When `true`, only administrator-managed allow rules remain effective while sandboxed networking requirements are active; user allowlist additions are ignored. Without managed allow rules, user-added domain allow rules do not remain effective. |
| `experimental_network.unix_sockets` | `map<string, allow \| deny>` | Administrator-managed Unix socket policy for sandboxed networking. |
| `experimental_network.allow_local_binding` | `boolean` | Permit broader local/private-network access for sandboxed networking. Exact local IP literal or `localhost` allow rules can still permit specific local targets when this stays `false`. |
| `hooks` | `table` | Admin-enforced managed lifecycle hooks. Requires a managed hook directory and uses the same event schema as inline `[hooks]` in `config.toml`. |
| `hooks.managed_dir` | `string (absolute path)` | Directory containing managed hook scripts on macOS and Linux. Codex validates that it is absolute and exists before loading managed hooks. |
| `hooks.windows_managed_dir` | `string (absolute path)` | Directory containing managed hook scripts on Windows. Codex validates that it is absolute and exists before loading managed hooks. |
| `hooks.<Event>` | `array<table>` | Matcher groups for a hook event such as `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SessionStart`, `SubagentStart`, `SubagentStop`, `UserPromptSubmit`, or `Stop`. |
| `hooks.<Event>[].hooks` | `array<table>` | Hook handlers for a matcher group. Command hooks are currently supported; prompt and agent hook handlers are parsed but skipped. |
| `hooks.<Event>[].hooks[].commandWindows` | `string` | Windows-only command override for command hooks. The TOML alias `command_windows` is also accepted. |
| `permissions.filesystem.deny_read` | `array<string>` | Admin-enforced filesystem read denials. Entries can be paths or glob patterns, and users cannot weaken them with local config. |
| `mcp_servers` | `table` | Allowlist of MCP servers that may be enabled. Both the server name (`<id>`) and its identity must match for the MCP server to be enabled. Any configured MCP server not in the allowlist (or with a mismatched identity) is disabled. |
| `mcp_servers.<id>.identity` | `table` | Identity rule for a single MCP server. Set either `command` (stdio) or `url` (streamable HTTP). |
| `mcp_servers.<id>.identity.command` | `string` | Allow an MCP stdio server when its `mcp_servers.<id>.command` matches this command. |
| `mcp_servers.<id>.identity.url` | `string` | Allow an MCP streamable HTTP server when its `mcp_servers.<id>.url` matches this URL. |
| `rules` | `table` | Admin-enforced command rules merged with `.rules` files. Requirements rules must be restrictive. |
| `rules.prefix_rules` | `array<table>` | List of enforced prefix rules. Each rule must include `pattern` and `decision`. |
| `rules.prefix_rules[].pattern` | `array<table>` | Command prefix expressed as pattern tokens. Each token sets either `token` or `any_of`. |
| `rules.prefix_rules[].pattern[].token` | `string` | A single literal token at this position. |
| `rules.prefix_rules[].pattern[].any_of` | `array<string>` | A list of allowed alternative tokens at this position. |
| `rules.prefix_rules[].decision` | `prompt \| forbidden` | Required. Requirements rules can only prompt or forbid (not allow). |
| `rules.prefix_rules[].justification` | `string` | Optional non-empty rationale surfaced in approval prompts or rejection messages. |
