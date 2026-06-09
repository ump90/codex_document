### 模型上下文协议（MCP）

Source: [Model Context Protocol](https://developers.openai.com/codex/mcp.md)

Model Context Protocol (MCP) 将模型连接到工具和上下文。使用它可以让 Codex 访问第三方文档，或让它与你的浏览器、Figma 等开发者工具交互。

Codex 在 CLI 和 IDE 扩展中都支持 MCP servers。

#### 支持的 MCP 功能

- **STDIO servers**：作为本地进程运行的 servers（由命令启动）。
  - 环境变量
- **Streamable HTTP servers**：通过地址访问的 servers。
  - Bearer token 认证
  - OAuth 认证（对支持 OAuth 的 servers 运行 `codex mcp login `）
- **Server instructions**：Codex 会读取初始化期间返回的 MCP `instructions` 字段，并将其作为 server 范围的指南与 server 的工具一起使用。

如果你为 Codex 构建或维护 MCP server，请使用 `instructions` 表达适用于整个 server 的跨工具工作流、约束和速率限制。保持前 512 个字符自包含，这样 Codex 决定如何使用 server 时可获得最重要的指南。

#### 将 Codex 连接到 MCP 服务器

Codex 将 MCP 配置与其他 Codex 配置设置一起存储在 `config.toml` 中。默认是 `~/.codex/config.toml`，但你也可以使用 `.codex/config.toml` 将 MCP servers 限定到项目范围（仅限受信任项目）。

CLI 和 IDE 扩展共享此配置。配置好 MCP servers 后，你可以在两个 Codex 客户端之间切换，而无需重新设置。

要配置 MCP servers，请选择一种方式：

1. **使用 CLI**：运行 `codex mcp` 来添加和管理 servers。
2. **编辑 `config.toml`**：直接更新 `~/.codex/config.toml`（或受信任项目中项目范围的 `.codex/config.toml`）。

#### 使用 CLI 配置

#### 添加 MCP 服务器

```bash
codex mcp add  --env VAR1=VALUE1 --env VAR2=VALUE2 --
```

例如，要添加 Context7（一个用于开发者文档的免费 MCP server），可以运行以下命令：

```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
```

#### 其他 CLI 命令

若要查看所有可用 MCP 命令，可以运行 `codex mcp --help`。

#### 终端 UI（TUI）

在 `codex` TUI 中，使用 `/mcp` 查看你的活动 MCP servers。

#### 使用 config.toml 配置

如需更细粒度地控制 MCP server 选项，请编辑 `~/.codex/config.toml`（或项目范围的 `.codex/config.toml`）。在 IDE 扩展中，从齿轮菜单选择 **MCP settings** > **Open config.toml**。

在配置文件中使用 `[mcp_servers.]` table 配置每个 MCP server。

#### STDIO 服务器

- `command`（必需）：启动 server 的命令。
- `args`（可选）：传递给 server 的参数。
- `env`（可选）：为 server 设置的环境变量。
- `env_vars`（可选）：允许并转发的环境变量。
- `cwd`（可选）：启动 server 时使用的工作目录。
- `experimental_environment`（可选）：设置为 `remote`，以便在可用时通过远程执行器环境启动 stdio server。

`env_vars` 可以包含普通变量名，也可以包含带 source 的对象：

```toml
env_vars = ["LOCAL_TOKEN", { name = "REMOTE_TOKEN", source = "remote" }]
```

字符串条目和 `source = "local"` 会从 Codex 的本地环境读取。
`source = "remote"` 会从远程执行器环境读取，并要求使用远程 MCP stdio。

#### 可流式 HTTP 服务器

- `url`（必需）：server 地址。
- `bearer_token_env_var`（可选）：用于在 `Authorization` 中发送 bearer token 的环境变量名称。
- `http_headers`（可选）：header 名称到静态值的映射。
- `env_http_headers`（可选）：header 名称到环境变量名称的映射（值从环境中提取）。

#### 其他配置选项

- `startup_timeout_sec`（可选）：server 启动超时（秒）。默认：`10`。
- `tool_timeout_sec`（可选）：server 运行工具的超时（秒）。默认：`60`。
- `enabled`（可选）：设置为 `false` 可在不删除 server 的情况下禁用它。
- `required`（可选）：设置为 `true` 会在此已启用 server 无法初始化时使启动失败。
- `enabled_tools`（可选）：工具允许列表。
- `disabled_tools`（可选）：工具拒绝列表（在 `enabled_tools` 之后应用）。
- `default_tools_approval_mode`（可选）：来自此 server 的工具的默认审批行为。支持的值为 `auto`、`prompt` 和 `approve`。
- `tools..approval_mode`（可选）：单个工具的审批行为覆盖。

如果你的 OAuth provider 需要固定 callback port，请在 `config.toml` 中设置顶层 `mcp_oauth_callback_port`。如果未设置，Codex 会绑定到临时端口。

如果你的 MCP OAuth 流程必须使用特定 callback URL（例如远程 Devbox ingress URL 或自定义 callback 路径），请设置 `mcp_oauth_callback_url`。Codex 会将此值作为 OAuth `redirect_uri`，同时仍使用 `mcp_oauth_callback_port` 作为 callback 监听端口。本地 callback URL（例如 `localhost`）会绑定到本地接口；非本地 callback URL 会绑定到 `0.0.0.0`，以便 callback 能到达主机。

如果 MCP server 宣告了 `scopes_supported`，Codex 会在 OAuth 登录期间优先使用 server 宣告的 scopes。否则，Codex 会回退到 `config.toml` 中配置的 scopes。

#### config.toml 示例

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
env_vars = ["LOCAL_TOKEN"]

[mcp_servers.context7.env]
MY_ENV_VAR = "MY_ENV_VALUE"
```

```toml
# Optional MCP OAuth callback overrides (used by `codex mcp login`)
mcp_oauth_callback_port = 5555
mcp_oauth_callback_url = "https://devbox.example.internal/callback"
```

```toml
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
http_headers = { "X-Figma-Region" = "us-east-1" }
```

```toml
[mcp_servers.chrome_devtools]
url = "http://localhost:3000/mcp"
enabled_tools = ["open", "screenshot"]
disabled_tools = ["screenshot"] # applied after enabled_tools
default_tools_approval_mode = "prompt"
startup_timeout_sec = 20
tool_timeout_sec = 45
enabled = true

[mcp_servers.chrome_devtools.tools.open]
approval_mode = "approve"
```

#### 插件提供的 MCP 服务器

已安装的 plugins 可以在其 plugin manifest 中捆绑 MCP servers。这些 servers 会从 plugin 启动，因此用户配置不设置它们的传输命令。用户配置仍可在 `plugins..mcp_servers.` 下控制开关状态和工具策略。

```toml
[plugins."sample@test".mcp_servers.sample]
enabled = true
default_tools_approval_mode = "prompt"
enabled_tools = ["read", "search"]

[plugins."sample@test".mcp_servers.sample.tools.search]
approval_mode = "approve"
```

#### 实用 MCP 服务器示例

MCP servers 列表仍在增长。以下是一些常见示例：

- [OpenAI Docs MCP](https://developers.openai.com/learn/docs-mcp)：搜索和读取 OpenAI 开发者文档。
- [Context7](https://github.com/upstash/context7)：连接到最新的开发者文档。
- Figma [Local](https://developers.figma.com/docs/figma-mcp-server/local-server-installation/) 和 [Remote](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/)：访问你的 Figma 设计。
- [Playwright](https://www.npmjs.com/package/@playwright/mcp)：使用 Playwright 控制和检查浏览器。
- [Chrome Developer Tools](https://github.com/ChromeDevTools/chrome-devtools-mcp/)：控制和检查 Chrome。
- [Sentry](https://docs.sentry.io/product/sentry-mcp/#codex)：访问 Sentry 日志。
- [GitHub](https://github.com/github/github-mcp-server)：管理 `git` 支持范围之外的 GitHub 内容（例如 pull request 和 issue）。
