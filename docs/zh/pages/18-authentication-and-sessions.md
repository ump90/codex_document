### 身份验证和会话

Source: [Authentication](https://developers.openai.com/codex/auth.md)

#### OpenAI 身份验证

使用 OpenAI 模型时，Codex 支持两种登录方式：

- 使用 ChatGPT 登录以获得订阅访问权限
- 使用 API key 登录以获得按用量计费的访问权限

Codex cloud 要求使用 ChatGPT 登录。Codex CLI 和 IDE extension 支持这两种登录方式。

你的登录方式也会决定适用哪些管理员控制和数据处理策略。

- 使用 ChatGPT 登录时，Codex 遵循你的 ChatGPT 工作区权限、RBAC，以及 ChatGPT Enterprise 的保留和驻留设置
- 使用 API key 时，则遵循你的 API 组织的保留和数据共享设置

对于 CLI，当没有可用的有效会话时，Sign in with ChatGPT 是默认身份验证路径。

#### 使用 ChatGPT 登录

当你从 Codex app、CLI 或 IDE Extension 使用 ChatGPT 登录时，Codex 会打开浏览器窗口，让你完成登录流程。登录后，浏览器会将访问令牌返回给 CLI 或 IDE 扩展。

如果你的环境已经提供 ChatGPT access token，CLI 可以从 stdin 读取它：

```shell
printenv CODEX_ACCESS_TOKEN | codex login --with-access-token
```

#### 使用 API key 登录

你也可以使用 API key 登录 Codex app、CLI 或 IDE Extension。请从 [OpenAI dashboard](https://platform.openai.com/api-keys) 获取你的 API key。

OpenAI 会通过你的 OpenAI Platform 账户按标准 API 费率对 API key 使用量计费。请参阅 [API pricing page](https://openai.com/api/pricing/)。

API key 身份验证支持本地 Codex 工作流，但依赖 ChatGPT workspace 访问权限或云服务的某些功能会受到限制或不可用。请在 [Feature availability](02-codex-pricing.md#feature-availability) 中按计划比较支持情况。

当你使用 API key 登录时，Codex 使用标准 API 价格，而不是包含在 ChatGPT 计划中的额度。

我们建议将 API key 身份验证用于程序化 Codex CLI 工作流，例如 CI/CD 作业。不要在不受信任或公共环境中暴露 Codex 执行能力。

#### 将 Codex 访问令牌用于企业自动化

在 ChatGPT Enterprise 工作区中，管理员可以允许获准成员为可信的非交互式 Codex 本地工作流创建 Codex 访问令牌。当自动化需要 ChatGPT 工作区访问权限、ChatGPT 管理的 Codex 权益，或不通过浏览器登录即可使用的企业工作区控制时，请使用访问令牌。

访问令牌适用于可信脚本、调度器和私有 CI runner。对于一般 OpenAI API 调用，请继续使用 Platform API key。

有关设置步骤、权限、轮换和撤销指导，请参阅 [Access tokens](63-access-tokens.md)。

#### 保护你的 Codex cloud 账户

Codex cloud 会直接与你的代码库交互，因此它需要比许多其他 ChatGPT 功能更强的安全性。请启用多因素身份验证 (MFA)。

如果你使用社交登录提供商（Google、Microsoft、Apple），则不要求你在 ChatGPT 账户上启用 MFA，但你可以通过社交登录提供商进行设置。

设置说明请参阅：

- [Google](https://support.google.com/accounts/answer/185839)
- [Microsoft](https://support.microsoft.com/en-us/topic/what-is-multifactor-authentication-e5e39437-121c-be60-d123-eda06bddf661)
- [Apple](https://support.apple.com/en-us/102660)

如果你通过单点登录 (SSO) 访问 ChatGPT，你的组织 SSO 管理员应为所有用户强制启用 MFA。

如果你使用电子邮件和密码登录，则必须先在账户上设置 MFA，才能访问 Codex cloud。

如果你的账户支持多种登录方式，其中一种是电子邮件和密码，则即使你以其他方式登录，也必须先设置 MFA 才能访问 Codex。

#### 登录缓存

当你使用 ChatGPT 或 API key 登录 Codex app、CLI 或 IDE Extension 时，Codex 会缓存你的登录详细信息，并在下次启动 CLI 或扩展时复用。CLI 和扩展共享相同的缓存登录详细信息。如果你从其中任一端登出，下次启动 CLI 或扩展时都需要重新登录。

Codex 会将登录详细信息本地缓存在 `~/.codex/auth.json` 的明文文件中，或缓存在你的操作系统专用凭据存储中。

对于使用 ChatGPT 登录的会话，Codex 会在令牌过期前于使用过程中自动刷新令牌，因此活动会话通常无需再次通过浏览器登录即可继续。

#### 凭据存储

使用 `cli_auth_credentials_store` 控制 Codex CLI 将缓存凭据存储在哪里：

```toml
# file | keyring | auto
cli_auth_credentials_store = "keyring"
```

- `file` 将凭据存储在 `CODEX_HOME` 下的 `auth.json` 中（默认是 `~/.codex`）。
- `keyring` 将凭据存储在你的操作系统凭据存储中。
- `auto` 在可用时使用 OS 凭据存储，否则回退到 `auth.json`。

如果你使用基于文件的存储，请像对待密码一样对待 `~/.codex/auth.json`：它包含访问令牌。不要提交它，不要粘贴到工单中，也不要在聊天中分享。

#### 强制登录方式或 workspace

在托管环境中，管理员可以限制允许用户如何进行身份验证：

```toml
# Only allow ChatGPT login or only allow API key login.
forced_login_method = "chatgpt" # or "api"

# When using ChatGPT login, restrict users to a specific workspace.
forced_chatgpt_workspace_id = "00000000-0000-0000-0000-000000000000"
```

如果活动凭据与已配置限制不匹配，Codex 会将用户登出并退出。

这些设置通常通过 managed configuration 应用，而不是由每个用户单独设置。请参阅 [Managed configuration](67-managed-configuration.md)。

#### 登录诊断

直接运行 `codex login` 会在你配置的日志目录下写入专用的 `codex-login.log` 文件。当你需要调试浏览器登录或设备码失败，或支持人员要求提供登录专用日志时，请使用它。

#### 自定义 CA bundles

如果你的网络使用企业 TLS 代理或私有根 CA，请在登录前将 `CODEX_CA_CERTIFICATE` 设置为 PEM bundle。未设置 `CODEX_CA_CERTIFICATE` 时，Codex 会回退到 `SSL_CERT_FILE`。相同的自定义 CA 设置适用于登录、普通 HTTPS 请求和安全 WebSocket 连接。

```shell
export CODEX_CA_CERTIFICATE=/path/to/corporate-root-ca.pem
codex login
```

#### 在无头设备上登录

如果你使用 Codex CLI 登录 ChatGPT，在某些情况下，基于浏览器的登录 UI 可能无法工作：

- 你正在远程或无头环境中运行 CLI。
- 你的本地网络配置阻止了 Codex 在你登录后用于将 OAuth 令牌返回给 CLI 的 localhost 回调。

在这些情况下，优先使用设备码身份验证 (beta)。在交互式登录 UI 中选择 **Sign in with Device Code**，或直接运行 `codex login --device-auth`。如果设备码身份验证在你的环境中不起作用，请使用其中一种备用方法。

#### 首选：设备码身份验证 (beta)

1. 在你的 ChatGPT 安全设置（个人账户）或 ChatGPT 工作区权限（工作区管理员）中启用设备码登录。
2. 在运行 Codex 的终端中，选择以下选项之一：
   - 在交互式登录 UI 中，选择 **Sign in with Device Code**。
   - 运行 `codex login --device-auth`。
3. 在浏览器中打开链接，登录，然后输入一次性代码。

如果服务器未启用设备码登录，Codex 会回退到标准的基于浏览器的登录流程。

#### 备用方法：在本地完成身份验证并复制认证缓存

如果你可以在带浏览器的机器上完成登录流程，可以将缓存凭据复制到无头机器。

1. 在可以使用基于浏览器登录流程的机器上，运行 `codex login`。
2. 确认登录缓存存在于 `~/.codex/auth.json`。
3. 将 `~/.codex/auth.json` 复制到无头机器上的 `~/.codex/auth.json`。

请像对待密码一样对待 `~/.codex/auth.json`：它包含访问令牌。不要提交它，不要粘贴到工单中，也不要在聊天中分享。

如果你的操作系统将凭据存储在凭据存储中，而不是 `~/.codex/auth.json`，此方法可能不适用。有关如何配置基于文件的存储，请参阅 [凭据存储](#credential-storage)。

通过 SSH 复制到远程机器：

```shell
ssh user@remote 'mkdir -p ~/.codex'
scp ~/.codex/auth.json user@remote:~/.codex/auth.json
```

或者使用避免 `scp` 的单行命令：

```shell
ssh user@remote 'mkdir -p ~/.codex && cat > ~/.codex/auth.json' < ~/.codex/auth.json
```

复制到 Docker container：

```shell
# Replace MY_CONTAINER with the name or ID of your container.
CONTAINER_HOME=$(docker exec MY_CONTAINER printenv HOME)
docker exec MY_CONTAINER mkdir -p "$CONTAINER_HOME/.codex"
docker cp ~/.codex/auth.json MY_CONTAINER:"$CONTAINER_HOME/.codex/auth.json"
```

有关在可信 CI/CD runner 上使用同一模式的更高级版本，请参阅 [在 CI/CD 中维护 Codex 账户认证（高级）](84-ci-cd-auth.md)。该指南解释了如何让 Codex 在正常运行期间刷新 `auth.json`，并将更新后的文件保留给下一个 job。对于自动化，API key 仍然是推荐的默认选择。

#### 备用方法：通过 SSH 转发 localhost 回调

如果你可以在本地机器和远程主机之间转发端口，可以通过隧道转发 Codex 的本地回调服务器（默认 `localhost:1455`）来使用标准的基于浏览器流程。

1. 从本地机器启动端口转发：

```shell
ssh -L 1455:localhost:1455 user@remote
```

2. 在该 SSH 会话中运行 `codex login`，并在本地机器上跟随打印出的地址操作。

#### 替代模型提供商

当你在配置文件中定义 [custom model provider](17-advanced-configuration.md#custom-model-providers) 时，可以选择以下身份验证方法之一：

- **OpenAI 身份验证**：设置 `requires_openai_auth = true` 以使用 OpenAI 身份验证。然后你可以使用 ChatGPT 或 API key 登录。当你通过 LLM 代理服务器访问 OpenAI 模型时，这很有用。当 `requires_openai_auth = true` 时，Codex 会忽略 `env_key`。
- **环境变量身份验证**：设置 `env_key = "<ENV_VARIABLE_NAME>"`，以使用名为 `<ENV_VARIABLE_NAME>` 的本地环境变量中的提供商专用 API key。
- **无身份验证**：如果你未设置 `requires_openai_auth`（或将其设为 `false`），且未设置 `env_key`，Codex 会假定该提供商不需要身份验证。这对本地模型很有用。
