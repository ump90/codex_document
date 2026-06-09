### CLI command reference

Source: [Command line options](/codex/cli/reference.md)

#### How to read this reference

This page catalogs every documented Codex CLI command and flag. Use the interactive tables to search by key or description. Each section indicates whether the option is stable or experimental and calls out risky combinations.

The CLI inherits most defaults from ~/.codex/config.toml. Any
-c key=value overrides you pass at the command line take
precedence for that invocation. See [Config
basics](/codex/config-basic#configuration-precedence) for more information.

#### Global flags

| Key                                                  | Type / Values                                                 | Default | Details                                                                                                                                                                                                           |
| ---------------------------------------------------- | ------------------------------------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--add-dir`                                          | `path`                                                        |         | Grant additional directories write access alongside the main workspace. Repeat for multiple paths.                                                                                                                |
| `--ask-for-approval, -a`                             | `untrusted \| on-request \| never`                            |         | Control when Codex pauses for human approval before running a command. `on-failure` is deprecated; prefer `on-request` for interactive runs or `never` for non-interactive runs.                                  |
| `--cd, -C`                                           | `path`                                                        |         | Set the working directory for the agent before it starts processing your request.                                                                                                                                 |
| `--config, -c`                                       | `key=value`                                                   |         | Override configuration values. Values parse as TOML if possible; otherwise the literal string is used.                                                                                                            |
| `--dangerously-bypass-approvals-and-sandbox, --yolo` | `boolean`                                                     | `false` | Run every command without approvals or sandboxing. Only use inside an externally hardened environment.                                                                                                            |
| `--dangerously-bypass-hook-trust`                    | `boolean`                                                     | `false` | Run enabled hooks without requiring persisted hook trust for this invocation. Intended only for automation that already vets hook sources.                                                                        |
| `--disable`                                          | `feature`                                                     |         | Force-disable a feature flag (translates to `-c features.=false`). Repeatable.                                                                                                                                    |
| `--enable`                                           | `feature`                                                     |         | Force-enable a feature flag (translates to `-c features.=true`). Repeatable.                                                                                                                                      |
| `--image, -i`                                        | `path[,path...]`                                              |         | Attach one or more image files to the initial prompt. Separate multiple paths with commas or repeat the flag.                                                                                                     |
| `--model, -m`                                        | `string`                                                      |         | Override the model set in configuration (for example `gpt-5.4`).                                                                                                                                                  |
| `--no-alt-screen`                                    | `boolean`                                                     | `false` | Disable alternate screen mode for the TUI (overrides `tui.alternate_screen` for this run).                                                                                                                        |
| `--oss`                                              | `boolean`                                                     | `false` | Use the local open source model provider (equivalent to `-c model_provider="oss"`). Validates that Ollama is running.                                                                                             |
| `--profile, -p`                                      | `string`                                                      |         | Layer `$CODEX_HOME/profile-name.config.toml` on top of the base user config.                                                                                                                                      |
| `--remote`                                           | `ws://host:port \| wss://host:port \| unix:// \| unix://PATH` |         | Connect the interactive TUI to a remote app-server endpoint over WebSocket or a Unix socket. Supported for `codex`, `codex resume`, and `codex fork`; other subcommands reject remote mode.                       |
| `--remote-auth-token-env`                            | `ENV_VAR`                                                     |         | Read a bearer token from this environment variable and send it when connecting with `--remote`. Requires `--remote`; tokens are only sent over `wss://` URLs or local-only `ws://` URLs.                          |
| `--sandbox, -s`                                      | `read-only \| workspace-write \| danger-full-access`          |         | Select the sandbox policy for model-generated shell commands.                                                                                                                                                     |
| `--search`                                           | `boolean`                                                     | `false` | Enable live web search (sets `web_search = "live"` instead of the default `"cached"`).                                                                                                                            |
| `--strict-config`                                    | `boolean`                                                     | `false` | Error when `config.toml` contains fields this Codex version does not recognize. Supported by runtime commands such as `codex`, `exec`, `review`, `resume`, `fork`, `app-server`, `mcp-server`, and `exec-server`. |
| `PROMPT`                                             | `string`                                                      |         | Optional text instruction to start the session. Omit to launch the TUI without a pre-filled message.                                                                                                              |

These options apply to the base `codex` command. Most propagate to commands;
see the notes above or the relevant command help for exceptions. For propagated
flags, follow the relevant command help. For example, `codex exec --oss ...`
applies `--oss` to `exec`.

#### Command overview

The Maturity column uses feature maturity labels such as Experimental, Beta,
and Stable. See [Feature Maturity](/codex/feature-maturity) for how to
interpret these labels.

| Key                                                                                                     | Maturity       | Default | Details                                                                                                                                 |
| ------------------------------------------------------------------------------------------------------- | -------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| [`codex`](/codex/cli/reference#codex-interactive)                                                       | `stable`       |         | Launch the terminal UI. Accepts the global flags above plus an optional prompt or image attachments.                                    |
| [`codex app`](/codex/cli/reference#codex-app)                                                           | `stable`       |         | Launch the Codex desktop app on macOS or Windows. On macOS, Codex can open a workspace path; on Windows, Codex prints the path to open. |
| [`codex app-server`](/codex/cli/reference#codex-app-server)                                             | `experimental` |         | Launch the Codex app server for local development or debugging over stdio, WebSocket, or a Unix socket.                                 |
| [`codex apply`](/codex/cli/reference#codex-apply)                                                       | `stable`       |         | Apply the latest diff generated by a Codex Cloud task to your local working tree. Alias: `codex a`.                                     |
| [`codex cloud`](/codex/cli/reference#codex-cloud)                                                       | `experimental` |         | Browse or execute Codex Cloud tasks from the terminal without opening the TUI. Alias: `codex cloud-tasks`.                              |
| [`codex completion`](/codex/cli/reference#codex-completion)                                             | `stable`       |         | Generate shell completion scripts for Bash, Zsh, Fish, or PowerShell.                                                                   |
| [`codex debug app-server send-message-v2`](/codex/cli/reference#codex-debug-app-server-send-message-v2) | `experimental` |         | Debug app-server by sending a single V2 message through the built-in test client.                                                       |
| [`codex debug models`](/codex/cli/reference#codex-debug-models)                                         | `experimental` |         | Print the raw model catalog Codex sees, including an option to inspect only the bundled catalog.                                        |
| [`codex doctor`](/codex/cli/reference#codex-doctor)                                                     | `stable`       |         | Generate a diagnostic report for local installation, config, auth, runtime, Git, terminal, app-server, and thread inventory issues.     |
| [`codex exec`](/codex/cli/reference#codex-exec)                                                         | `stable`       |         | Run Codex non-interactively. Alias: `codex e`. Stream results to stdout or JSONL and optionally resume previous sessions.               |
| [`codex execpolicy`](/codex/cli/reference#codex-execpolicy)                                             | `experimental` |         | Evaluate execpolicy rule files and see whether a command would be allowed, prompted, or blocked.                                        |
| [`codex features`](/codex/cli/reference#codex-features)                                                 | `stable`       |         | List feature flags and persistently enable or disable them in `config.toml`.                                                            |
| [`codex fork`](/codex/cli/reference#codex-fork)                                                         | `stable`       |         | Fork a previous interactive session into a new thread, preserving the original transcript.                                              |
| [`codex login`](/codex/cli/reference#codex-login)                                                       | `stable`       |         | Authenticate Codex using ChatGPT OAuth, device auth, an API key, or an access token piped over stdin.                                   |
| [`codex logout`](/codex/cli/reference#codex-logout)                                                     | `stable`       |         | Remove stored authentication credentials.                                                                                               |
| [`codex mcp`](/codex/cli/reference#codex-mcp)                                                           | `experimental` |         | Manage Model Context Protocol servers (list, add, remove, authenticate).                                                                |
| [`codex mcp-server`](/codex/cli/reference#codex-mcp-server)                                             | `experimental` |         | Run Codex itself as an MCP server over stdio. Useful when another agent consumes Codex.                                                 |
| [`codex plugin marketplace`](/codex/cli/reference#codex-plugin-marketplace)                             | `experimental` |         | Add, list, upgrade, or remove plugin marketplaces from Git or local sources.                                                            |
| [`codex remote-control`](/codex/cli/reference#codex-remote-control)                                     | `experimental` |         | Ensure the local app-server daemon is running with remote-control support enabled.                                                      |
| [`codex resume`](/codex/cli/reference#codex-resume)                                                     | `stable`       |         | Continue a previous interactive session by ID or resume the most recent conversation.                                                   |
| [`codex sandbox`](/codex/cli/reference#codex-sandbox)                                                   | `experimental` |         | Run arbitrary commands inside Codex-provided macOS, Linux, or Windows sandboxes.                                                        |
| [`codex update`](/codex/cli/reference#codex-update)                                                     | `stable`       |         | Check for and apply a Codex CLI update when the installed release supports self-update.                                                 |

#### Command details

#### `codex` (interactive)

Running `codex` with no subcommand launches the interactive terminal UI (TUI). The agent accepts the global flags above plus image attachments. Web search defaults to cached mode; use `--search` to switch to live browsing. For low-friction local work, use `--sandbox workspace-write --ask-for-approval on-request`.

Use `--remote ws://host:port` or `--remote wss://host:port` to connect the TUI to an app server started with `codex app-server --listen ws://IP:PORT`. For a local Unix socket, use `--remote unix://` for the default socket or `--remote unix://PATH` for an explicit path. Add `--remote-auth-token-env <ENV_VAR>` when the server requires a bearer token for WebSocket authentication.

#### `codex app-server`

Launch the Codex app server locally. This is primarily for development and debugging and may change without notice.

| Key                           | Type / Values                                               | Default    | Details                                                                                                                                                                                                                |
| ----------------------------- | ----------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--analytics-default-enabled` | `boolean`                                                   | `false`    | Defaults analytics to enabled for first-party app-server clients unless the user opts out in config.                                                                                                                   |
| `--listen`                    | `stdio:// \| ws://IP:PORT \| unix:// \| unix://PATH \| off` | `stdio://` | Transport listener URL. Use `stdio://` for JSONL, `ws://IP:PORT` for a TCP WebSocket endpoint, `unix://` for the default Unix socket, `unix://PATH` for a custom Unix socket, or `off` to disable the local transport. |
| `--ws-audience`               | `string`                                                    |            | Expected `aud` claim for signed bearer tokens. Requires `--ws-auth signed-bearer-token`.                                                                                                                               |
| `--ws-auth`                   | `capability-token \| signed-bearer-token`                   |            | Authentication mode for app-server WebSocket clients. If omitted, WebSocket auth is disabled; non-local listeners warn during startup.                                                                                 |
| `--ws-issuer`                 | `string`                                                    |            | Expected `iss` claim for signed bearer tokens. Requires `--ws-auth signed-bearer-token`.                                                                                                                               |
| `--ws-max-clock-skew-seconds` | `number`                                                    | `30`       | Clock skew allowance when validating signed bearer token `exp` and `nbf` claims. Requires `--ws-auth signed-bearer-token`.                                                                                             |
| `--ws-shared-secret-file`     | `absolute path`                                             |            | File containing the HMAC shared secret used to validate signed JWT bearer tokens. Required with `--ws-auth signed-bearer-token`.                                                                                       |
| `--ws-token-file`             | `absolute path`                                             |            | File containing the shared capability token. Use with `--ws-auth capability-token` unless you provide `--ws-token-sha256` instead.                                                                                     |
| `--ws-token-sha256`           | `hexadecimal SHA-256 digest`                                |            | Expected SHA-256 digest for capability-token authentication. Use instead of `--ws-token-file` when the client token comes from another source.                                                                         |

`codex app-server --listen stdio://` keeps the default JSONL-over-stdio behavior. `--listen ws://IP:PORT` enables WebSocket transport for app-server clients. The server accepts `ws://` listen URLs; use TLS termination or a secure proxy when clients connect with `wss://`. Use `--listen unix://` to accept WebSocket handshakes on Codex's default Unix socket, or `--listen unix:///absolute/path.sock` to choose a socket path. If you generate schemas for client bindings, add `--experimental` to include gated fields and methods.

#### `codex remote-control`

Ensure the app-server daemon is running with remote-control support enabled.
Managed remote-control clients and SSH remote workflows use this command; it's
not a replacement for `codex app-server --listen` when you are building a local
protocol client.

#### `codex app`

Launch Codex Desktop from the terminal on macOS or Windows. On macOS, Codex can open a specific workspace path; on Windows, Codex prints the path to open.

| Key              | Type / Values | Default | Details                                                                                               |
| ---------------- | ------------- | ------- | ----------------------------------------------------------------------------------------------------- |
| `--download-url` | `url`         |         | Advanced override for the Codex desktop installer URL used during install.                            |
| `PATH`           | `path`        | `.`     | Workspace path for Codex Desktop. On macOS, Codex opens this path; on Windows, Codex prints the path. |

`codex app` opens an installed Codex Desktop app, or starts the installer when
the app is missing. On macOS, Codex opens the provided workspace path; on
Windows, it prints the path to open after installation.

#### `codex debug app-server send-message-v2`

Send one message through app-server's V2 thread/turn flow using the built-in app-server test client.

| Key            | Type / Values | Default | Details                                                                   |
| -------------- | ------------- | ------- | ------------------------------------------------------------------------- |
| `USER_MESSAGE` | `string`      |         | Message text sent to app-server through the built-in V2 test-client flow. |

This debug flow initializes with `experimentalApi: true`, starts a thread, sends a turn, and streams server notifications. Use it to reproduce and inspect app-server protocol behavior locally.

#### `codex debug models`

Print the raw model catalog Codex sees as JSON.

| Key         | Type / Values | Default | Details                                                                              |
| ----------- | ------------- | ------- | ------------------------------------------------------------------------------------ |
| `--bundled` | `boolean`     | `false` | Skip refresh and print only the model catalog bundled with the current Codex binary. |

Use `--bundled` when you want to inspect only the catalog bundled with the current binary, without refreshing from the remote models endpoint.

#### `codex apply`

Apply the most recent diff from a Codex cloud task to your local repository. You must authenticate and have access to the task.

| Key       | Type / Values | Default | Details                                                          |
| --------- | ------------- | ------- | ---------------------------------------------------------------- |
| `TASK_ID` | `string`      |         | Identifier of the Codex Cloud task whose diff should be applied. |

Codex prints the patched files and exits non-zero if `git apply` fails (for example, due to conflicts).

#### `codex cloud`

Interact with Codex cloud tasks from the terminal. The default command opens an interactive picker; `codex cloud exec` submits a task directly, and `codex cloud list` returns recent tasks for scripting or quick inspection.

| Key          | Type / Values | Default | Details                                                                                  |
| ------------ | ------------- | ------- | ---------------------------------------------------------------------------------------- |
| `--attempts` | `1-4`         | `1`     | Number of assistant attempts (best-of-N) Codex Cloud should run.                         |
| `--env`      | `ENV_ID`      |         | Target Codex Cloud environment identifier (required). Use `codex cloud` to list options. |
| `QUERY`      | `string`      |         | Task prompt. If omitted, Codex prompts interactively for details.                        |

Authentication follows the same credentials as the main CLI. Codex exits non-zero if the task submission fails.

#### `codex cloud list`

List recent cloud tasks with optional filtering and pagination.

| Key        | Type / Values | Default | Details                                           |
| ---------- | ------------- | ------- | ------------------------------------------------- |
| `--cursor` | `string`      |         | Pagination cursor returned by a previous request. |
| `--env`    | `ENV_ID`      |         | Filter tasks by environment identifier.           |
| `--json`   | `boolean`     | `false` | Emit machine-readable JSON instead of plain text. |
| `--limit`  | `1-20`        | `20`    | Maximum number of tasks to return.                |

Plain-text output prints a task URL followed by status details. Use `--json` for automation. The JSON payload contains a `tasks` array plus an optional `cursor` value. Each task includes `id`, `url`, `title`, `status`, `updated_at`, `environment_id`, `environment_label`, `summary`, `is_review`, and `attempt_total`.

#### `codex completion`

Generate shell completion scripts and redirect the output to the appropriate location, for example `codex completion zsh > "${fpath[1]}/_codex"`.

| Key     | Type / Values                                  | Default | Details                                                     |
| ------- | ---------------------------------------------- | ------- | ----------------------------------------------------------- |
| `SHELL` | `bash \| zsh \| fish \| power-shell \| elvish` | `bash`  | Shell to generate completions for. Output prints to stdout. |

#### `codex doctor`

Generate a local diagnostic report before filing a support issue or
while investigating a broken Codex installation. The report checks installation,
configuration, authentication, runtime, Git, terminal, app-server, and thread
inventory health.

| Key          | Type / Values | Default | Details                                                          |
| ------------ | ------------- | ------- | ---------------------------------------------------------------- |
| `--all`      | `boolean`     | `false` | Expand long lists in the detailed human-readable report.         |
| `--ascii`    | `boolean`     | `false` | Use ASCII status labels and separators in human-readable output. |
| `--json`     | `boolean`     | `false` | Emit a redacted machine-readable support report.                 |
| `--no-color` | `boolean`     | `false` | Disable ANSI color in human-readable output.                     |
| `--summary`  | `boolean`     | `false` | Show grouped check rows and the final count summary only.        |

#### `codex features`

Manage feature flags stored in `$CODEX_HOME/config.toml`. The `enable` and
`disable` commands persist changes so they apply to future sessions. The
`features` subcommand doesn't accept `--profile`.

| Key                  | Type / Values             | Default | Details                                                                    |
| -------------------- | ------------------------- | ------- | -------------------------------------------------------------------------- |
| `Disable subcommand` | `codex features disable ` |         | Persistently disable a feature flag in `$CODEX_HOME/config.toml`.          |
| `Enable subcommand`  | `codex features enable `  |         | Persistently enable a feature flag in `$CODEX_HOME/config.toml`.           |
| `List subcommand`    | `codex features list`     |         | Show known feature flags, their maturity stage, and their effective state. |

