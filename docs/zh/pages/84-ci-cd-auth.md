### 在 CI/CD 中维护 Codex 账户认证（高级）

Source: [Maintain Codex account auth in CI/CD (advanced)](https://developers.openai.com/codex/auth/ci-cd-auth.md)

本指南说明如何在可信 CI/CD runner 上保持 ChatGPT 托管的 Codex 认证可用，而不需要你自己调用 OAuth token endpoint。

自动化认证的推荐方式是 API key。只有当你明确需要让工作流以你的 Codex 账户身份运行时，才使用本指南。

整体模式如下：

1. 在可信机器上运行一次 `codex login`，创建 `auth.json`。
2. 将该文件放到 runner 上。
3. 正常运行 Codex。
4. 当 session 变旧时，让 Codex 刷新 session。
5. 保留刷新后的 `auth.json`，供下一次运行使用。

这是面向企业和其它可信私有自动化场景的高级工作流。对大多数 CI/CD job 来说，API key 仍然是推荐选项。

请像对待密码一样对待 `~/.codex/auth.json`：它包含 access token。不要提交它、粘贴到 ticket 中，或在聊天中共享。不要在公开或开源仓库中使用此工作流。

#### 为什么这样可行

Codex 已经知道如何刷新 ChatGPT 托管的 session。

以当前开源客户端为准：

- Codex 会从 `auth.json` 加载本地认证缓存
- 如果 `last_refresh` 早于约 8 天，Codex 会在继续运行前刷新 token bundle
- 刷新成功后，Codex 会把新 token 和新的 `last_refresh` 写回 `auth.json`
- 如果某个请求收到 `401`，Codex 也内置了刷新并重试的路径

这意味着受支持的 CI/CD 策略不是“自己调用 refresh API”，而是“运行 Codex，并持久化更新后的 `auth.json`”。

#### 何时使用

仅当以下条件全部成立时，才使用本指南：

- 你需要 ChatGPT 托管的 Codex 认证，而不是 API key
- 远程 runner 无法运行 `codex login`
- runner 是可信的私有基础设施
- 你可以在多次运行之间保留刷新后的 `auth.json`
- 某个 `auth.json` 副本只会由一台机器或一个串行化的 job 流使用

本指南适用于 Codex 托管的 ChatGPT auth（`auth_mode: "chatgpt"`）。

它不适用于：

- API key auth
- 外部 token host integration（`auth_mode: "chatgptAuthTokens"`）
- Codex 之外的通用 OAuth client

如果你的凭据存储在操作系统 keyring 中，请先切换到文件后端存储。参见 [Credential storage](18-authentication-and-sessions.md#credential-storage)。

#### 一次性生成 `auth.json`

在可以使用浏览器登录的可信机器上：

1. 配置 Codex，把凭据存入文件：

```toml
cli_auth_credentials_store = "file"
```

2. 运行：

```bash
codex login
```

3. 验证该文件看起来像托管 ChatGPT auth：

```bash
AUTH_FILE="${CODEX_HOME:-$HOME/.codex}/auth.json"

jq '{
  auth_mode,
  has_tokens: (.tokens != null),
  has_refresh_token: ((.tokens.refresh_token // "") != ""),
  last_refresh
}' "$AUTH_FILE"
```

仅当以下条件成立时继续：

- `auth_mode` 是 `"chatgpt"`
- `has_refresh_token` 是 `true`

然后将 `auth.json` 的内容放入你的 CI/CD secret manager，或复制到可信的持久 runner。

#### 推荐模式：在自托管 runner 上使用 GitHub Actions

最简单的全自动设置，是使用带有持久 `CODEX_HOME` 的自托管 GitHub Actions runner。

这个模式效果好的原因：

- runner 可以在多次 job 之间把 `auth.json` 保留在磁盘上
- Codex 可以原地刷新该文件
- 后续 job 会自动使用刷新后的 token
- 原始 secret 只需要用于 bootstrap 或重新播种

关键细节是：只在 `auth.json` 缺失时才播种。如果你每次运行都用原始 secret 覆盖文件，就会丢弃 Codex 刚写入的刷新后 token。

示例定时 workflow：

```yaml
name: Keep Codex auth fresh

on:
  schedule:
    - cron: "0 9 * * 1"
  workflow_dispatch:

jobs:
  keep-codex-auth-fresh:
    runs-on: self-hosted
    steps:
      - name: Bootstrap auth.json if needed
        shell: bash
        env:
          CODEX_AUTH_JSON: ${{ secrets.CODEX_AUTH_JSON }}
        run: |
          export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
          mkdir -p "$CODEX_HOME"
          chmod 700 "$CODEX_HOME"

          if [ ! -f "$CODEX_HOME/auth.json" ]; then
            printf '%s' "$CODEX_AUTH_JSON" > "$CODEX_HOME/auth.json"
            chmod 600 "$CODEX_HOME/auth.json"
          fi

      - name: Run Codex
        shell: bash
        run: |
          codex exec --json "Reply with the single word OK." >/dev/null
```

这会做到：

- 第一次运行播种 `auth.json`
- 后续运行复用同一个文件
- 一旦缓存 session 足够旧，Codex 会在正常的 `codex exec` 步骤中刷新它
- 刷新后的文件保留在磁盘上，供下一个 workflow run 使用

在当前开源客户端中，Codex 大约会在 8 天后把 session 视为 stale，因此每周一次的 schedule 通常足够。

#### 短生命周期 runner：恢复、运行 Codex、持久化更新后的文件

如果你使用 GitHub-hosted runner、GitLab shared runner 或任何其它短生命周期环境，runner 文件系统会在每个 job 后消失。在这种设置中，你需要一个往返流程：

1. 从安全存储恢复当前 `auth.json`
2. 运行 Codex
3. 将更新后的 `auth.json` 写回安全存储

通用 GitHub Actions 形状：

```yaml
name: Run Codex with managed auth

on:
  workflow_dispatch:

jobs:
  codex-job:
    runs-on: ubuntu-latest
    steps:
      - name: Restore auth.json
        shell: bash
        run: |
          export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
          mkdir -p "$CODEX_HOME"
          chmod 700 "$CODEX_HOME"

          # Replace this with your secret manager or secure storage command.
          my-secret-cli read codex-auth-json > "$CODEX_HOME/auth.json"
          chmod 600 "$CODEX_HOME/auth.json"

      - name: Run Codex
        shell: bash
        run: |
          codex exec --json "summarize the failing tests"

      - name: Persist refreshed auth.json
        if: always()
        shell: bash
        run: |
          # Replace this with your secret manager or secure storage command.
          my-secret-cli write codex-auth-json < "$CODEX_HOME/auth.json"
```

关键要求是：写回步骤存储的是 Codex 在本次运行中产生的刷新后文件，而不是原始 seed。

#### 你不需要单独的刷新命令

任何正常的 Codex 运行都可以刷新 session。

这意味着你有两个好选项：

- 让现有 CI/CD Codex job 自然刷新该文件
- 如果真实 job 运行得不够频繁，则添加一个轻量的定时维护 job，例如上面的 GitHub Actions 示例

session 变 stale 后的第一次 Codex 运行，就是刷新 `auth.json` 的那次运行。

#### 重要运行规则

- 每个 runner 或每个串行化 workflow 流使用一个 `auth.json`。
- 不要在并发 job 或多台机器之间共享同一个文件。
- 不要在每次运行时用原始 seed 覆盖持久 runner 上已刷新的文件。
- 不要把 `auth.json` 存在仓库、日志或公开 artifact storage 中。
- 如果内置刷新停止工作，请从可信机器重新播种。

#### 刷新停止工作时怎么办

此流程可以减少人工操作，但不能保证同一个 session 永久有效。

如果出现以下情况，请用新的 `auth.json` 重新播种 runner：

- Codex 开始返回 `401`，且 runner 已无法刷新
- refresh token 被撤销或过期
- 另一台机器或并发 job 先轮换了 token
- 安全存储往返失败，恢复了旧文件

重新播种：

1. 在可信机器上运行 `codex login`。
2. 替换 CI/CD 中存储的 `auth.json` 副本。
3. 让下一个 runner job 继续使用 Codex 的内置刷新流程。

#### 验证 runner 正在维护 session

检查 runner 是否仍有托管 auth token，以及 `last_refresh` 是否存在：

```bash
AUTH_FILE="${CODEX_HOME:-$HOME/.codex}/auth.json"

jq '{
  auth_mode,
  last_refresh,
  has_access_token: ((.tokens.access_token // "") != ""),
  has_id_token: ((.tokens.id_token // "") != ""),
  has_refresh_token: ((.tokens.refresh_token // "") != "")
}' "$AUTH_FILE"
```

如果 runner 是持久的，你应该看到同一个文件在多次运行之间持续存在。如果 runner 是短生命周期的，请确认写回步骤保存的是上一个 job 更新后的文件。

#### 源码参考

如果你想在开源客户端中验证此行为：

- [`codex-rs/core/src/auth.rs`](https://github.com/openai/codex/blob/main/codex-rs/core/src/auth.rs) 涵盖 stale-token 检测、自动刷新、401 后刷新重试恢复，以及刷新后 token 的持久化
- [`codex-rs/core/src/auth/storage.rs`](https://github.com/openai/codex/blob/main/codex-rs/core/src/auth/storage.rs) 涵盖文件后端的 `auth.json` 存储
