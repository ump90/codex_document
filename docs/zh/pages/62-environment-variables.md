### 环境变量

Source: [Environment variables](https://developers.openai.com/codex/environment-variables.md)

Codex 使用 `config.toml` 保存持久设置。环境变量适用于
shell 作用域的覆盖、自动化密钥、安装器行为或诊断。

本页列出 Codex 会直接读取的稳定公开环境变量。
它不列出内部开发变量、测试变量，或你通过
[`env_key`](17-advanced-configuration.md#custom-model-providers)
自行选择的提供商专用密钥名称。

#### 核心位置

| Variable            | Used by                                    | Default      | Description                                                                                                                                                      |
| ------------------- | ------------------------------------------ | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CODEX_HOME`        | CLI, IDE extension, app-server, installers | `~/.codex`   | 设置 Codex 状态的根目录，包括配置、身份验证、日志、会话、技能和独立包元数据。如果你设置了它，该目录必须已经存在。 |
| `CODEX_SQLITE_HOME` | CLI and app-server state                   | `CODEX_HOME` | 设置 SQLite 后端状态的存储位置。`sqlite_home` 配置选项优先级更高。相对路径会从当前工作目录解析。           |

有关 `CODEX_HOME` 下存储文件的更多信息，请参阅
[配置和状态位置](17-advanced-configuration.md#config-and-state-locations)。

#### 安装器变量

这些变量适用于由
`https://chatgpt.com/codex/install.sh` 和
`https://chatgpt.com/codex/install.ps1` 提供的独立安装脚本。

| Variable                | Default                                                                              | Description                                                                                                                                                     |
| ----------------------- | ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CODEX_NON_INTERACTIVE` | `false`                                                                              | 设置为 `1`、`true` 或 `yes` 可跳过安装器提示。提示会使用其默认响应，因此请将它用于脚本化安装和更新，而不是首次运行设置。 |
| `CODEX_INSTALL_DIR`     | `~/.local/bin` on macOS/Linux; `%LOCALAPPDATA%\Programs\OpenAI\Codex\bin` on Windows | 更改可见 `codex` 命令的安装位置。独立包缓存仍位于 `CODEX_HOME/packages/standalone` 下。                        |

对于无人值守安装，请在运行已下载安装器的 shell 上设置 `CODEX_NON_INTERACTIVE=1`：

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | CODEX_NON_INTERACTIVE=1 sh
```

```powershell
$env:CODEX_NON_INTERACTIVE=1; irm https://chatgpt.com/codex/install.ps1 | iex
```

#### 身份验证和网络

| Variable               | Used by                             | Description                                                                                                                                                               |
| ---------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CODEX_API_KEY`        | `codex exec`                        | 为单次非交互运行提供 API key。它仅在 `codex exec` 中受支持；运行仓库控制代码时，请内联设置，而不是作业级设置。 |
| `CODEX_ACCESS_TOKEN`   | CLI, app-server, trusted automation | 为受信任自动化提供 ChatGPT 或 Codex 访问令牌。对于持久化登录，请通过管道传给 `codex login --with-access-token`。                                       |
| `CODEX_CA_CERTIFICATE` | HTTPS, login, and WebSocket clients | 指向 PEM CA 包，适用于存在企业 TLS 拦截或私有根 CA 的环境。优先级高于 `SSL_CERT_FILE`。                                    |
| `SSL_CERT_FILE`        | HTTPS, login, and WebSocket clients | 当未设置 `CODEX_CA_CERTIFICATE` 时的备用 PEM CA 包路径。                                                                                                         |

对于提供商 API key，请在模型提供商
配置中设置 [`env_key`](17-advanced-configuration.md#custom-model-providers)。
Codex 会读取该配置指定名称的变量，因此变量
名称本身并不是固定的 Codex 环境变量。

有关自动化密钥处理，请参阅
[使用 API key 身份验证](60-non-interactive-mode.md#use-api-key-auth)。
有关访问令牌设置，请参阅 [Access tokens](63-access-tokens.md)。

#### 诊断

| Variable   | Used by            | Description                                                                                                             |
| ---------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `RUST_LOG` | CLI and app-server | 控制 Rust 日志过滤和详细程度。除非你设置更详细的值，否则 `codex exec` 默认输出 `error`。 |

`RUST_LOG` 接受 `error`、`warn`、`info`、`debug` 和
`trace` 等值。它也接受更有针对性的 Rust 日志过滤器，例如
`codex_core=debug,codex_tui=debug`。

默认情况下，交互式 CLI 会将诊断记录在有界本地存储中，但
明文 `codex-tui.log` 文件需要选择启用。当你
需要明文日志来排查问题时，请显式设置 `log_dir`：

```bash
RUST_LOG=debug codex -c log_dir=./.codex-log
tail -F ./.codex-log/codex-tui.log
```

在非交互模式中，`codex exec` 会内联打印消息，而不是写入
单独的 TUI 日志文件。
