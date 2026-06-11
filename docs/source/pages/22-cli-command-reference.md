### CLI command reference

Source: [Command line options](https://developers.openai.com/codex/cli/reference.md)

### How to read this reference

This page catalogs every documented Codex CLI command and flag. Use the interactive tables to search by key or description. Each section indicates whether the option is stable or experimental and calls out risky combinations.

The CLI inherits most defaults from `~/.codex/config.toml`. Any
  `-c key=value` overrides you pass at the command line take
  precedence for that invocation. See [Config
  basics](https://developers.openai.com/codex/config-basic#configuration-precedence) for more information.

### Global flags

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `PROMPT` | `string` | `` | Optional text instruction to start the session. Omit to launch the TUI without a pre-filled message. |
| `--image, -i` | `path[,path...]` | `` | Attach one or more image files to the initial prompt. Separate multiple paths with commas or repeat the flag. |
| `--model, -m` | `string` | `` | Override the model set in configuration (for example `gpt-5.4`). |
| `--oss` | `boolean` | `false` | Use the local open source model provider (equivalent to `-c model_provider="oss"`). Validates that Ollama is running. |
| `--profile, -p` | `string` | `` | Layer `$CODEX_HOME/profile-name.config.toml` on top of the base user config. |
| `--sandbox, -s` | `read-only \| workspace-write \| danger-full-access` | `` | Select the sandbox policy for model-generated shell commands. |
| `--ask-for-approval, -a` | `untrusted \| on-request \| never` | `` | Control when Codex pauses for human approval before running a command. `on-failure` is deprecated; prefer `on-request` for interactive runs or `never` for non-interactive runs. |
| `--dangerously-bypass-approvals-and-sandbox, --yolo` | `boolean` | `false` | Run every command without approvals or sandboxing. Only use inside an externally hardened environment. |
| `--dangerously-bypass-hook-trust` | `boolean` | `false` | Run enabled hooks without requiring persisted hook trust for this invocation. Intended only for automation that already vets hook sources. |
| `--cd, -C` | `path` | `` | Set the working directory for the agent before it starts processing your request. |
| `--search` | `boolean` | `false` | Enable live web search (sets `web_search = "live"` instead of the default `"cached"`). |
| `--add-dir` | `path` | `` | Grant additional directories write access alongside the main workspace. Repeat for multiple paths. |
| `--no-alt-screen` | `boolean` | `false` | Disable alternate screen mode for the TUI (overrides `tui.alternate_screen` for this run). |
| `--remote` | `ws://host:port \| wss://host:port \| unix:// \| unix://PATH` | `` | Connect the interactive TUI to a remote app-server endpoint over WebSocket or a Unix socket. Supported for `codex`, `codex resume`, and `codex fork`; other subcommands reject remote mode. |
| `--remote-auth-token-env` | `ENV_VAR` | `` | Read a bearer token from this environment variable and send it when connecting with `--remote`. Requires `--remote`; tokens are only sent over `wss://` URLs or local-only `ws://` URLs. |
| `--strict-config` | `boolean` | `false` | Error when `config.toml` contains fields this Codex version does not recognize. Supported by runtime commands such as `codex`, `exec`, `review`, `resume`, `fork`, `app-server`, `mcp-server`, and `exec-server`. |
| `--enable` | `feature` | `` | Force-enable a feature flag (translates to `-c features.<name>=true`). Repeatable. |
| `--disable` | `feature` | `` | Force-disable a feature flag (translates to `-c features.<name>=false`). Repeatable. |
| `--config, -c` | `key=value` | `` | Override configuration values. Values parse as TOML if possible; otherwise the literal string is used. |

These options apply to the base `codex` command. Most propagate to commands;
see the notes above or the relevant command help for exceptions. For propagated
flags, follow the relevant command help. For example, `codex exec --oss ...`
applies `--oss` to `exec`.

### Command overview

The Maturity column uses feature maturity labels such as Experimental, Beta,
  and Stable. See [Feature Maturity](https://developers.openai.com/codex/feature-maturity) for how to
  interpret these labels.

| Key | Maturity | Details |
| --- | --- | --- |
| [codex](/codex/cli/reference#codex-interactive) | `stable` | Launch the terminal UI. Accepts the global flags above plus an optional prompt or image attachments. |
| [codex app-server](/codex/cli/reference#codex-app-server) | `experimental` | Launch the Codex app server for local development or debugging over stdio, WebSocket, or a Unix socket. |
| [codex remote-control](/codex/cli/reference#codex-remote-control) | `experimental` | Ensure the local app-server daemon is running with remote-control support enabled. |
| [codex app](/codex/cli/reference#codex-app) | `stable` | Launch the Codex desktop app on macOS or Windows. On macOS, Codex can open a workspace path; on Windows, Codex prints the path to open. |
| [codex debug app-server send-message-v2](/codex/cli/reference#codex-debug-app-server-send-message-v2) | `experimental` | Debug app-server by sending a single V2 message through the built-in test client. |
| [codex debug models](/codex/cli/reference#codex-debug-models) | `experimental` | Print the raw model catalog Codex sees, including an option to inspect only the bundled catalog. |
| [codex apply](/codex/cli/reference#codex-apply) | `stable` | Apply the latest diff generated by a Codex Cloud task to your local working tree. Alias: `codex a`. |
| [codex archive](/codex/cli/reference#codex-archive-and-codex-unarchive) | `stable` | Archive a saved interactive session by session ID or session name. |
| [codex cloud](/codex/cli/reference#codex-cloud) | `experimental` | Browse or execute Codex Cloud tasks from the terminal without opening the TUI. Alias: `codex cloud-tasks`. |
| [codex completion](/codex/cli/reference#codex-completion) | `stable` | Generate shell completion scripts for Bash, Zsh, Fish, or PowerShell. |
| [codex doctor](/codex/cli/reference#codex-doctor) | `stable` | Generate a diagnostic report for local installation, config, auth, runtime, Git, terminal, app-server, and thread inventory issues. |
| [codex features](/codex/cli/reference#codex-features) | `stable` | List feature flags and persistently enable or disable them in `config.toml`. |
| [codex exec](/codex/cli/reference#codex-exec) | `stable` | Run Codex non-interactively. Alias: `codex e`. Stream results to stdout or JSONL and optionally resume previous sessions. |
| [codex execpolicy](/codex/cli/reference#codex-execpolicy) | `experimental` | Evaluate execpolicy rule files and see whether a command would be allowed, prompted, or blocked. |
| [codex login](/codex/cli/reference#codex-login) | `stable` | Authenticate Codex using ChatGPT OAuth, device auth, an API key, or an access token piped over stdin. |
| [codex logout](/codex/cli/reference#codex-logout) | `stable` | Remove stored authentication credentials. |
| [codex mcp](/codex/cli/reference#codex-mcp) | `experimental` | Manage Model Context Protocol servers (list, add, remove, authenticate). |
| [codex plugin marketplace](/codex/cli/reference#codex-plugin-marketplace) | `experimental` | Add, list, upgrade, or remove plugin marketplaces from Git or local sources. |
| [codex plugin](/codex/cli/reference#codex-plugin) | `experimental` | Install, list, and remove plugins from configured marketplace sources. |
| [codex mcp-server](/codex/cli/reference#codex-mcp-server) | `experimental` | Run Codex itself as an MCP server over stdio. Useful when another agent consumes Codex. |
| [codex resume](/codex/cli/reference#codex-resume) | `stable` | Continue a previous interactive session by ID or resume the most recent conversation. |
| [codex fork](/codex/cli/reference#codex-fork) | `stable` | Fork a previous interactive session into a new thread, preserving the original transcript. |
| [codex sandbox](/codex/cli/reference#codex-sandbox) | `experimental` | Run arbitrary commands inside Codex-provided macOS, Linux, or Windows sandboxes. |
| [codex update](/codex/cli/reference#codex-update) | `stable` | Check for and apply a Codex CLI update when the installed release supports self-update. |
| [codex unarchive](/codex/cli/reference#codex-archive-and-codex-unarchive) | `stable` | Restore an archived interactive session by session ID or session name. |

### Command details

#### `codex` (interactive)

Running `codex` with no subcommand launches the interactive terminal UI (TUI). The agent accepts the global flags above plus image attachments. Web search defaults to cached mode; use `--search` to switch to live browsing. For low-friction local work, use `--sandbox workspace-write --ask-for-approval on-request`.

Use `--remote ws://host:port` or `--remote wss://host:port` to connect the TUI to an app server started with `codex app-server --listen ws://IP:PORT`. For a local Unix socket, use `--remote unix://` for the default socket or `--remote unix://PATH` for an explicit path. Add `--remote-auth-token-env <ENV_VAR>` when the server requires a bearer token for WebSocket authentication.

#### `codex app-server`

Launch the Codex app server locally. This is primarily for development and debugging and may change without notice.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `--stdio` | `boolean` | `false` | Use stdio transport. Equivalent to `--listen stdio://` and mutually exclusive with `--listen`. |
| `--listen` | `stdio:// \| ws://IP:PORT \| unix:// \| unix://PATH \| off` | `stdio://` | Transport listener URL. Use `stdio://` for JSONL, `ws://IP:PORT` for a TCP WebSocket endpoint, `unix://` for the default Unix socket, `unix://PATH` for a custom Unix socket, or `off` to disable the local transport. |
| `--ws-auth` | `capability-token \| signed-bearer-token` | `` | Authentication mode for app-server WebSocket clients. If omitted, WebSocket auth is disabled; non-local listeners warn during startup. |
| `--ws-token-file` | `absolute path` | `` | File containing the shared capability token. Use with `--ws-auth capability-token` unless you provide `--ws-token-sha256` instead. |
| `--ws-token-sha256` | `hexadecimal SHA-256 digest` | `` | Expected SHA-256 digest for capability-token authentication. Use instead of `--ws-token-file` when the client token comes from another source. |
| `--ws-shared-secret-file` | `absolute path` | `` | File containing the HMAC shared secret used to validate signed JWT bearer tokens. Required with `--ws-auth signed-bearer-token`. |
| `--ws-issuer` | `string` | `` | Expected `iss` claim for signed bearer tokens. Requires `--ws-auth signed-bearer-token`. |
| `--ws-audience` | `string` | `` | Expected `aud` claim for signed bearer tokens. Requires `--ws-auth signed-bearer-token`. |
| `--ws-max-clock-skew-seconds` | `number` | `30` | Clock skew allowance when validating signed bearer token `exp` and `nbf` claims. Requires `--ws-auth signed-bearer-token`. |
| `--analytics-default-enabled` | `boolean` | `false` | Defaults analytics to enabled for first-party app-server clients unless the user opts out in config. |

`codex app-server --listen stdio://` keeps the default JSONL-over-stdio behavior, and `codex app-server --stdio` is an alias for that transport. `--listen ws://IP:PORT` enables WebSocket transport for app-server clients. The server accepts `ws://` listen URLs; use TLS termination or a secure proxy when clients connect with `wss://`. Use `--listen unix://` to accept WebSocket handshakes on Codex's default Unix socket, or `--listen unix:///absolute/path.sock` to choose a socket path. If you generate schemas for client bindings, add `--experimental` to include gated fields and methods.

#### `codex remote-control`

Ensure the app-server daemon is running with remote-control support enabled.
Managed remote-control clients and SSH remote workflows use this command; it's
not a replacement for `codex app-server --listen` when you are building a local
protocol client.

#### `codex app`

Launch Codex Desktop from the terminal on macOS or Windows. On macOS, Codex can open a specific workspace path; on Windows, Codex prints the path to open.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `PATH` | `path` | `.` | Workspace path for Codex Desktop. On macOS, Codex opens this path; on Windows, Codex prints the path. |
| `--download-url` | `url` | `` | Advanced override for the Codex desktop installer URL used during install. |

`codex app` opens an installed Codex Desktop app, or starts the installer when
the app is missing. On macOS, Codex opens the provided workspace path; on
Windows, it prints the path to open after installation.

#### `codex debug app-server send-message-v2`

Send one message through app-server's V2 thread/turn flow using the built-in app-server test client.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `USER_MESSAGE` | `string` | `` | Message text sent to app-server through the built-in V2 test-client flow. |

This debug flow initializes with `experimentalApi: true`, starts a thread, sends a turn, and streams server notifications. Use it to reproduce and inspect app-server protocol behavior locally.

#### `codex debug models`

Print the raw model catalog Codex sees as JSON.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `--bundled` | `boolean` | `false` | Skip refresh and print only the model catalog bundled with the current Codex binary. |

Use `--bundled` when you want to inspect only the catalog bundled with the current binary, without refreshing from the remote models endpoint.

#### `codex apply`

Apply the most recent diff from a Codex cloud task to your local repository. You must authenticate and have access to the task.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `TASK_ID` | `string` | `` | Identifier of the Codex Cloud task whose diff should be applied. |

Codex prints the patched files and exits non-zero if `git apply` fails (for example, due to conflicts).

#### `codex archive` and `codex unarchive`

Archive or restore a saved interactive session by session ID or session name.
Use these commands when you want to clean up the session picker without deleting
the transcript. Session IDs take precedence over session names.

```bash
codex archive <SESSION>
codex unarchive <SESSION>
```

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `SESSION` | `session ID \| session name` | `` | Saved session to archive or restore. Session IDs take precedence over session names. |
| `--remote` | `ws://host:port \| wss://host:port \| unix:// \| unix://PATH` | `` | Connect to a remote app-server endpoint before changing archive state. |
| `--remote-auth-token-env` | `ENV_VAR` | `` | Read a bearer token from this environment variable when `--remote` requires authentication. |

#### `codex cloud`

Interact with Codex cloud tasks from the terminal. The default command opens an interactive picker; `codex cloud exec` submits a task directly, and `codex cloud list` returns recent tasks for scripting or quick inspection.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `QUERY` | `string` | `` | Task prompt. If omitted, Codex prompts interactively for details. |
| `--env` | `ENV_ID` | `` | Target Codex Cloud environment identifier (required). Use `codex cloud` to list options. |
| `--attempts` | `1-4` | `1` | Number of assistant attempts (best-of-N) Codex Cloud should run. |

Authentication follows the same credentials as the main CLI. Codex exits non-zero if the task submission fails.

##### `codex cloud list`

List recent cloud tasks with optional filtering and pagination.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `--env` | `ENV_ID` | `` | Filter tasks by environment identifier. |
| `--limit` | `1-20` | `20` | Maximum number of tasks to return. |
| `--cursor` | `string` | `` | Pagination cursor returned by a previous request. |
| `--json` | `boolean` | `false` | Emit machine-readable JSON instead of plain text. |

Plain-text output prints a task URL followed by status details. Use `--json` for automation. The JSON payload contains a `tasks` array plus an optional `cursor` value. Each task includes `id`, `url`, `title`, `status`, `updated_at`, `environment_id`, `environment_label`, `summary`, `is_review`, and `attempt_total`.

#### `codex completion`

Generate shell completion scripts and redirect the output to the appropriate location, for example `codex completion zsh > "${fpath[1]}/_codex"`.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `SHELL` | `bash \| zsh \| fish \| power-shell \| elvish` | `bash` | Shell to generate completions for. Output prints to stdout. |

#### `codex doctor`

Generate a local diagnostic report before filing a support issue or
while investigating a broken Codex installation. The report checks installation,
configuration, authentication, runtime, Git, terminal, app-server, and thread
inventory health.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `--json` | `boolean` | `false` | Emit a redacted machine-readable support report. |
| `--summary` | `boolean` | `false` | Show grouped check rows and the final count summary only. |
| `--all` | `boolean` | `false` | Expand long lists in the detailed human-readable report. |
| `--no-color` | `boolean` | `false` | Disable ANSI color in human-readable output. |
| `--ascii` | `boolean` | `false` | Use ASCII status labels and separators in human-readable output. |

#### `codex features`

Manage feature flags stored in `$CODEX_HOME/config.toml`. The `enable` and
`disable` commands persist changes so they apply to future sessions. The
`features` subcommand doesn't accept `--profile`.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `List subcommand` | `codex features list` | `` | Show known feature flags, their maturity stage, and their effective state. |
| `Enable subcommand` | `codex features enable <feature>` | `` | Persistently enable a feature flag in `$CODEX_HOME/config.toml`. |
| `Disable subcommand` | `codex features disable <feature>` | `` | Persistently disable a feature flag in `$CODEX_HOME/config.toml`. |

#### `codex exec`

Use `codex exec` (or the short form `codex e`) for scripted or CI-style runs that should finish without human interaction.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `PROMPT` | `string \| - (read stdin)` | `` | Initial instruction for the task. Use `-` to pipe the prompt from stdin. |
| `--image, -i` | `path[,path...]` | `` | Attach images to the first message. Repeatable; supports comma-separated lists. |
| `--model, -m` | `string` | `` | Override the configured model for this run. |
| `--oss` | `boolean` | `false` | Use the local open source provider (requires a running Ollama instance). |
| `--sandbox, -s` | `read-only \| workspace-write \| danger-full-access` | `` | Sandbox policy for model-generated commands. Defaults to configuration. |
| `--profile, -p` | `string` | `` | Layer `$CODEX_HOME/profile-name.config.toml` on top of the base user config. |
| `--full-auto` | `boolean` | `false` | Deprecated compatibility flag. Prefer `--sandbox workspace-write`; Codex prints a warning when this flag is used. |
| `--dangerously-bypass-approvals-and-sandbox, --yolo` | `boolean` | `false` | Bypass approval prompts and sandboxing. Dangerous—only use inside an isolated runner. |
| `--dangerously-bypass-hook-trust` | `boolean` | `false` | Run enabled hooks without requiring persisted hook trust for this invocation. Intended only for automation that already vets hook sources. |
| `--cd, -C` | `path` | `` | Set the workspace root before executing the task. |
| `--skip-git-repo-check` | `boolean` | `false` | Allow running outside a Git repository (useful for one-off directories). |
| `--ephemeral` | `boolean` | `false` | Run without persisting session rollout files to disk. |
| `--ignore-user-config` | `boolean` | `false` | Do not load `$CODEX_HOME/config.toml`. Authentication still uses `CODEX_HOME`. |
| `--ignore-rules` | `boolean` | `false` | Do not load user or project execpolicy `.rules` files for this run. |
| `--output-schema` | `path` | `` | JSON Schema file describing the expected final response shape. Codex validates tool output against it. |
| `--color` | `always \| never \| auto` | `auto` | Control ANSI color in stdout. |
| `--json, --experimental-json` | `boolean` | `false` | Print newline-delimited JSON events instead of formatted text. |
| `--output-last-message, -o` | `path` | `` | Write the assistant’s final message to a file. Useful for downstream scripting. |
| `Resume subcommand` | `codex exec resume [SESSION_ID]` | `` | Resume an exec session by ID or add `--last` to continue the most recent session from the current working directory. Add `--all` to consider sessions from any directory. Accepts an optional follow-up prompt. |
| `-c, --config` | `key=value` | `` | Inline configuration override for the non-interactive run (repeatable). |

Codex writes formatted output by default. Add `--json` to receive newline-delimited JSON events (one per state change). The optional `resume` subcommand lets you continue non-interactive tasks. Use `--last` to pick the most recent session from the current working directory, or add `--all` to search across all sessions:

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `SESSION_ID` | `uuid` | `` | Resume the specified session. Omit and use `--last` to continue the most recent session. |
| `--last` | `boolean` | `false` | Resume the most recent conversation from the current working directory. |
| `--all` | `boolean` | `false` | Include sessions outside the current working directory when selecting the most recent session. |
| `--image, -i` | `path[,path...]` | `` | Attach one or more images to the follow-up prompt. Separate multiple paths with commas or repeat the flag. |
| `PROMPT` | `string \| - (read stdin)` | `` | Optional follow-up instruction sent immediately after resuming. |

#### `codex execpolicy`

Check `execpolicy` rule files before you save them. `codex execpolicy check` accepts one or more `--rules` flags (for example, files under `~/.codex/rules`) and emits JSON showing the strictest decision and any matching rules. Add `--pretty` to format the output. The `execpolicy` command is currently in preview.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `--rules, -r` | `path (repeatable)` | `` | Path to an execpolicy rule file to evaluate. Provide multiple flags to combine rules across files. |
| `--pretty` | `boolean` | `false` | Pretty-print the JSON result. |
| `COMMAND...` | `var-args` | `` | Command to be checked against the specified policies. |

#### `codex login`

Authenticate the CLI with a ChatGPT account, API key, or access token. With no flags, Codex opens a browser for the ChatGPT OAuth flow.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `--with-api-key` | `boolean` | `` | Read an API key from stdin (for example `printenv OPENAI_API_KEY \| codex login --with-api-key`). |
| `--with-access-token` | `boolean` | `` | Read an access token from stdin (for example `printenv CODEX_ACCESS_TOKEN \| codex login --with-access-token`). |
| `--device-auth` | `boolean` | `` | Use OAuth device code flow instead of launching a browser window. |
| `status subcommand` | `codex login status` | `` | Print the active authentication mode and exit with 0 when logged in. |

`codex login status` exits with `0` when credentials are present, which is helpful in automation scripts.

#### `codex logout`

Remove saved credentials for both API key and ChatGPT authentication. This command has no flags.

#### `codex mcp`

Manage Model Context Protocol server entries stored in `~/.codex/config.toml`.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `list` | `--json` | `` | List configured MCP servers. Add `--json` for machine-readable output. |
| `get <name>` | `--json` | `` | Show a specific server configuration. `--json` prints the raw config entry. |
| `add <name>` | `-- <command...> \| --url <value>` | `` | Register a server using a stdio launcher command or a streamable HTTP URL. Supports `--env KEY=VALUE` for stdio transports. |
| `remove <name>` | `` | `` | Delete a stored MCP server definition. |
| `login <name>` | `--scopes scope1,scope2` | `` | Start an OAuth login for a streamable HTTP server (servers that support OAuth only). |
| `logout <name>` | `` | `` | Remove stored OAuth credentials for a streamable HTTP server. |

The `add` subcommand supports both stdio and streamable HTTP transports:

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `COMMAND...` | `stdio transport` | `` | Executable plus arguments to launch the MCP server. Provide after `--`. |
| `--env KEY=VALUE` | `repeatable` | `` | Environment variable assignments applied when launching a stdio server. |
| `--url` | `https://…` | `` | Register a streamable HTTP server instead of stdio. Mutually exclusive with `COMMAND...`. |
| `--bearer-token-env-var` | `ENV_VAR` | `` | Environment variable whose value is sent as a bearer token when connecting to a streamable HTTP server. |
| `--oauth-client-id` | `CLIENT_ID` | `` | OAuth client identifier for a streamable HTTP MCP server. Requires `--url`. |
| `--oauth-resource` | `RESOURCE` | `` | OAuth resource parameter to include during login for a streamable HTTP MCP server. Requires `--url`. |

OAuth actions (`login`, `logout`) only work with streamable HTTP servers (and only when the server supports OAuth).

#### `codex plugin`

Install, list, and remove plugins from configured marketplaces.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `add <plugin[@marketplace]>` | `[--marketplace, -m NAME] [--json]` | `` | Install a plugin from a configured marketplace. Use `--marketplace` or `-m` when the plugin argument omits `@marketplace`. |
| `list` | `[--marketplace, -m NAME] [--available --json] [--json]` | `` | List installed plugins. With `--json`, output has `installed` and `available` arrays; `--available` includes uninstalled marketplace plugins and requires `--json`. |
| `remove <plugin[@marketplace]>` | `[--marketplace, -m NAME] [--json]` | `` | Remove an installed plugin from local config and cache. Use `--json` for automation-friendly output. |
| `marketplace` | `` | `` | Manage configured marketplace sources. See `codex plugin marketplace` below. |

`codex plugin add --json` prints `pluginId`, `name`, `marketplaceName`,
`version`, `installedPath`, and `authPolicy`. `codex plugin list --json` prints
`installed` and `available` arrays. Entries include `pluginId`, `name`,
`marketplaceName`, `version`, `installed`, `enabled`, `source`, `installPolicy`,
`authPolicy`, and, when available, `marketplaceSource` with the configured
marketplace source type and value. `codex plugin remove --json` prints
`pluginId`, `name`, and `marketplaceName`.

#### `codex plugin marketplace`

Manage plugin marketplace sources that Codex can browse and install from.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `add <source>` | `[--ref REF] [--sparse PATH] [--json]` | `` | Install a plugin marketplace from GitHub shorthand, a Git URL, an SSH URL, or a local marketplace root directory. `--sparse` is supported only for Git sources and can be repeated. |
| `list` | `[--json]` | `` | Show plugin marketplaces Codex is currently considering and the root path for each marketplace. |
| `upgrade [marketplace-name]` | `[--json]` | `` | Refresh one configured Git marketplace, or all configured Git marketplaces when no name is provided. |
| `remove <marketplace-name>` | `[--json]` | `` | Remove a configured plugin marketplace. |

`codex plugin marketplace add` accepts GitHub shorthand such as `owner/repo` or
`owner/repo@ref`, HTTP or HTTPS Git URLs, SSH Git URLs, and local marketplace
root directories. Use `--ref` to pin a Git ref, and repeat `--sparse PATH` to
use a sparse checkout for Git-backed marketplace repositories.

`codex plugin marketplace list` prints in-scope marketplace names and roots,
including implicitly discovered default marketplaces and configured marketplace
snapshots.

Add `--json` to marketplace add, list, upgrade, or remove commands for
automation-friendly output. Marketplace add JSON includes `marketplaceName`,
`installedRoot`, and `alreadyAdded`; list JSON includes a `marketplaces` array
with `name`, `root`, and optional `marketplaceSource`; upgrade JSON includes
`selectedMarketplaces`, `upgradedRoots`, and `errors`; remove JSON includes
`marketplaceName` and `installedRoot`.

#### `codex mcp-server`

Run Codex as an MCP server over stdio so that other tools can connect. This command inherits global configuration overrides and exits when the downstream client closes the connection.

#### `codex resume`

Continue an interactive session by ID or resume the most recent conversation. `codex resume` scopes `--last` to the current working directory unless you pass `--all`. It accepts the same global flags as `codex`, including model and sandbox overrides.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `SESSION_ID` | `uuid` | `` | Resume the specified session. Omit and use `--last` to continue the most recent session. |
| `--last` | `boolean` | `false` | Skip the picker and resume the most recent conversation from the current working directory. |
| `--all` | `boolean` | `false` | Include sessions outside the current working directory when selecting the most recent session. |

#### `codex fork`

Fork a previous interactive session into a new thread. By default, `codex fork` opens the session picker; add `--last` to fork your most recent session instead.

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `SESSION_ID` | `uuid` | `` | Fork the specified session. Omit and use `--last` to fork the most recent session. |
| `--last` | `boolean` | `false` | Skip the picker and fork the most recent conversation automatically. |
| `--all` | `boolean` | `false` | Show sessions beyond the current working directory in the picker. |

#### `codex sandbox`

Use the sandbox helper to run a command under the same policies Codex uses internally.

##### macOS seatbelt

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `--profile, -p` | `NAME` | `` | Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config. |
| `--permissions-profile, -P` | `NAME` | `` | Apply a named permissions profile from the active configuration stack. |
| `--cd, -C` | `DIR` | `` | Working directory used for profile resolution and command execution. Requires `--permissions-profile`. |
| `--include-managed-config` | `boolean` | `false` | Include managed requirements while resolving an explicit permissions profile. Requires `--permissions-profile`. |
| `--allow-unix-socket` | `path` | `` | Allow the sandboxed command to bind or connect Unix sockets rooted at this path. Repeat to allow multiple paths. |
| `--log-denials` | `boolean` | `false` | Capture macOS sandbox denials with `log stream` while the command runs and print them after exit. |
| `--config, -c` | `key=value` | `` | Pass configuration overrides into the sandboxed run (repeatable). |
| `COMMAND...` | `var-args` | `` | Shell command to execute under macOS Seatbelt. Everything after `--` is forwarded. |

##### Linux Landlock

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `--profile, -p` | `NAME` | `` | Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config. |
| `--permissions-profile, -P` | `NAME` | `` | Apply a named permissions profile from the active configuration stack. |
| `--cd, -C` | `DIR` | `` | Working directory used for profile resolution and command execution. Requires `--permissions-profile`. |
| `--include-managed-config` | `boolean` | `false` | Include managed requirements while resolving an explicit permissions profile. Requires `--permissions-profile`. |
| `--config, -c` | `key=value` | `` | Configuration overrides applied before launching the sandbox (repeatable). |
| `COMMAND...` | `var-args` | `` | Command to execute under Landlock + seccomp. Provide the executable after `--`. |

##### Windows

| Key | Type / Values | Default | Details |
| --- | --- | --- | --- |
| `--profile, -p` | `NAME` | `` | Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config. |
| `--permissions-profile, -P` | `NAME` | `` | Apply a named permissions profile from the active configuration stack. |
| `--cd, -C` | `DIR` | `` | Working directory used for profile resolution and command execution. Requires `--permissions-profile`. |
| `--include-managed-config` | `boolean` | `false` | Include managed requirements while resolving an explicit permissions profile. Requires `--permissions-profile`. |
| `--config, -c` | `key=value` | `` | Configuration overrides applied before launching the sandbox (repeatable). |
| `COMMAND...` | `var-args` | `` | Command to execute under the native Windows sandbox. Provide the executable after `--`. |

#### `codex update`

Check for and apply a Codex CLI update when the installed release supports self-update. Debug builds print a message telling you to install a release build instead.

### Flag combinations and safety tips

- Use `--sandbox workspace-write` for unattended local work that can stay inside the workspace, and avoid `--dangerously-bypass-approvals-and-sandbox` unless you are inside a dedicated sandbox VM.
- When you need to grant Codex write access to more directories, prefer `--add-dir` rather than forcing `--sandbox danger-full-access`.
- Pair `--json` with `--output-last-message` in CI to capture machine-readable progress and a final natural-language summary.

### Related resources

- [Codex CLI overview](https://developers.openai.com/codex/cli): installation, upgrades, and quick tips.
- [Config basics](https://developers.openai.com/codex/config-basic): persist defaults like the model and provider.
- [Advanced Config](https://developers.openai.com/codex/config-advanced): profiles, providers, sandbox tuning, and integrations.
- [AGENTS.md](https://developers.openai.com/codex/guides/agents-md): conceptual overview of Codex agent capabilities and best practices.
