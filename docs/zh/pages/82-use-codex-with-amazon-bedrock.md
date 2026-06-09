### 将 Codex 与 Amazon Bedrock 配合使用

Source: [Use Codex with Amazon Bedrock](https://developers.openai.com/codex/amazon-bedrock.md)

配置 Codex 使用通过 Amazon Bedrock 提供的 OpenAI models。在此设置中，Codex 在本地运行，并使用 AWS 管理的身份验证和访问控制将 model requests 发送到 Bedrock。

#### 工作原理

当你将 Codex 配置为使用 Amazon Bedrock 作为 model provider 时，OpenAI 托管的 Responses API 不在请求路径中。Codex 会将 model requests 发送到 Amazon Bedrock，而 Bedrock 会为受支持的 OpenAI models 提供 OpenAI 兼容的 Responses API 实现。

身份验证是 AWS 原生的。用户使用 Bedrock API key 或 AWS IAM credentials 进行身份验证。此 provider 不使用 ChatGPT 登录或 `OPENAI_API_KEY`。

#### 开始之前

请确认你具备：

- Amazon Bedrock 中受支持 OpenAI models 的访问权限。
- 所选 model 可用的 AWS Region。
- 已为 AWS account 配置 Amazon Bedrock Mantle path 的身份验证。

#### 配置 Codex

将 Amazon Bedrock Mantle path 的 `amazon-bedrock` model provider 添加到 `~/.codex/config.toml`。提供 model 是可选的。需要时请显式选择受支持的 model。

```toml
model_provider = "amazon-bedrock"
```

本指南涵盖受支持商业 AWS Regions 中的 Amazon Bedrock Mantle path。Codex 不支持 AWS GovCloud Regions 中的 Bedrock Mantle endpoints。

#### 身份验证选项

Codex 支持两条 Bedrock 身份验证路径。它会按以下顺序检查：

1. Bedrock API key。
2. AWS SDK credential chain。

#### 选项 1：Bedrock API 密钥

在 Codex 读取的环境中设置 Bedrock API key。使用 API-key 身份验证时必须指定 Region。

```shell
export AWS_BEARER_TOKEN_BEDROCK=
export AWS_REGION=us-east-2
```

#### 选项 2：AWS SDK 凭据

当你的组织通过 AWS SDK credential chain 管理 Bedrock 访问时，使用此路径。Codex 可以使用这些标准 AWS SDK credential sources：

1. 共享 AWS `config` 和 `credentials` 文件。

   ```shell
   aws configure
   ```

2. 环境变量。

   ```shell
   export AWS_ACCESS_KEY_ID=
   export AWS_SECRET_ACCESS_KEY=
   export AWS_SESSION_TOKEN=
   ```

3. AWS Management Console credentials。

   ```shell
   aws login
   ```

4. AWS SSO 或命名 profile。

   ```shell
   aws sso login --profile codex-bedrock
   export AWS_PROFILE=codex-bedrock
   ```

5. 使用 `credential_process` 配置的联合身份。对于企业 SSO 或 OIDC 联合，请在 Codex 外部配置 AWS profile，并让 AWS SDK 解析 credentials。将浏览器登录、token 交换、缓存和刷新放入你的 AWS profile 的 `credential_process` helper。

#### 桌面应用和 VS Code 扩展

桌面 app 和 IDE extensions 可能不会继承 shell 中的环境变量。请将必需值放入 `~/.codex/.env`，然后重启 app 或 extension。

```shell
export AWS_BEARER_TOKEN_BEDROCK=
export AWS_REGION=us-east-2
```

#### 验证设置

- 在 Codex CLI 中，打开 `/status` 并确认 Codex 正在使用 `amazon-bedrock` model provider。
- 在 desktop app 或 VS Code extension 中，重启 app 后开始一个新会话。
- 确认所选 model 在配置的 AWS Region 中可用，并且 AWS identity 有权限访问它。

#### 支持的模型

使用准确的 model IDs：

```text
openai.gpt-5.5
openai.gpt-5.4
```

模型可用性因 AWS Region 而异。选择 model 前，请参阅 [按 AWS Region 列出的模型支持](https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html)。

#### 功能可用性

此配置支持本地 Codex workflows。依赖 OpenAI 托管云服务、托管工具或云端托管发现能力的某些功能目前不可用。

Fast Mode 不适用于 Amazon Bedrock。Fast Mode 使用优先处理，而初始 Amazon Bedrock offering 仅支持按需推理。

#### 详细功能可用性

- 功能目前仅限特定 regions。请检查单个功能文档以了解更多地理限制。

  † 某些第一方 plugins 不可用。
