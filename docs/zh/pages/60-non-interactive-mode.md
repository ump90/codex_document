### 非交互模式

Source: [Non-interactive mode](https://developers.openai.com/codex/noninteractive.md)

非交互模式允许你从脚本中运行 Codex（例如持续集成 (CI) 作业），而无需打开交互式 TUI。
你可以用 `codex exec` 调用它。

有关各个标志的详细信息，请参阅 [`codex exec`](https://developers.openai.com/codex/cli/reference#codex-exec)。

#### 何时使用 `codex exec`

当你希望 Codex 执行以下操作时，请使用 `codex exec`：

- 作为流水线的一部分运行（CI、合并前检查、计划任务）。
- 生成可以通过管道传给其它工具的输出（例如生成发布说明或摘要）。
- 自然融入 CLI 工作流，将命令输出串接到 Codex，并把 Codex 输出传给其它工具。
- 使用明确、预设的沙箱和审批设置运行。

#### 基本用法

将任务提示作为单个参数传入：

```bash
codex exec "summarize the repository structure and list the top 5 risky areas"
```

`codex exec` 运行时，Codex 会将进度流式输出到 `stderr`，并且只把最终代理消息打印到 `stdout`。这使重定向或通过管道传递最终结果变得很直接：

```bash
codex exec "generate release notes for the last 10 commits" | tee release-notes.md
```

当你不想把会话 rollout 文件持久化到磁盘时，请使用 `--ephemeral`：

```bash
codex exec --ephemeral "triage this repository and suggest next steps"
```

如果 stdin 通过管道传入，同时你也提供了提示参数，Codex 会把提示视为指令，并把管道传入的内容作为额外上下文。

这让你可以很容易地用一个命令生成输入，并直接交给 Codex：

```bash
curl -s https://jsonplaceholder.typicode.com/comments \
  | codex exec "format the top 20 items into a markdown table" \
  > table.md
```

更多高级 stdin 管道模式请参阅 [Advanced stdin piping](#advanced-stdin-piping)。

#### 权限和安全

默认情况下，`codex exec` 在只读沙箱中运行。在自动化中，请设置工作流所需的最小权限：

- 允许编辑：`codex exec --sandbox workspace-write ""`
- 允许更广访问：`codex exec --sandbox danger-full-access ""`

仅在受控环境中使用 `danger-full-access`（例如隔离的 CI 运行器或容器）。

Codex 保留 `codex exec --full-auto` 作为已弃用的兼容标志，并会打印警告。新脚本中优先使用显式的 `--sandbox workspace-write` 标志。

当你需要一次不加载 `$CODEX_HOME/config.toml` 的运行时，使用 `--ignore-user-config`；当你需要在受控自动化环境中跳过用户和项目 execpolicy `.rules` 文件时，使用 `--ignore-rules`。

如果你配置了已启用且 `required = true` 的 MCP 服务器，但它初始化失败，`codex exec` 会以错误退出，而不是在没有该服务器的情况下继续。

#### 让输出可被机器读取

要在脚本中消费 Codex 输出，请使用 JSON Lines 输出：

```bash
codex exec --json "summarize the repo structure" | jq
```

启用 `--json` 后，`stdout` 会变成 JSON Lines (JSONL) 流，因此你可以捕获 Codex 运行时发出的每个事件。事件类型包括 `thread.started`、`turn.started`、`turn.completed`、`turn.failed`、`item.*` 和 `error`。

Item 类型包括代理消息、推理、命令执行、文件变更、MCP 工具调用、网页搜索和计划更新。

示例 JSON 流（每一行都是一个 JSON 对象）：

```jsonl
{"type":"thread.started","thread_id":"0199a213-81c0-7800-8aa1-bbab2a035a53"}
{"type":"turn.started"}
{"type":"item.started","item":{"id":"item_1","type":"command_execution","command":"bash -lc ls","status":"in_progress"}}
{"type":"item.completed","item":{"id":"item_3","type":"agent_message","text":"Repo contains docs, sdk, and examples directories."}}
{"type":"turn.completed","usage":{"input_tokens":24763,"cached_input_tokens":24448,"output_tokens":122,"reasoning_output_tokens":0}}
```

如果你只需要最终消息，请使用 `-o`/`--output-last-message` 将其写入文件。这会把最终消息写入文件，同时仍然打印到 `stdout`（详情见 [`codex exec`](https://developers.openai.com/codex/cli/reference#codex-exec)）。

#### 使用 schema 创建结构化输出

如果下游步骤需要结构化数据，请使用 `--output-schema` 请求符合 JSON Schema 的最终响应。
这对于需要稳定字段的自动化工作流很有用（例如作业摘要、风险报告或发布元数据）。

`schema.json`

```json
{
  "type": "object",
  "properties": {
    "project_name": { "type": "string" },
    "programming_languages": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["project_name", "programming_languages"],
  "additionalProperties": false
}
```

使用该 schema 运行 Codex，并将最终 JSON 响应写入磁盘：

```bash
codex exec "Extract project metadata" \
  --output-schema ./schema.json \
  -o ./project-metadata.json
```

最终输出示例（stdout）：

```json
{
  "project_name": "Codex CLI",
  "programming_languages": ["Rust", "TypeScript", "Shell"]
}
```

#### 在自动化中进行身份验证

默认情况下，`codex exec` 会复用已保存的 CLI 身份验证。在 CI 中，通常会显式提供凭据：

#### 使用 API key 身份验证

对于 GitHub Actions，请使用 [Codex GitHub Action](https://developers.openai.com/codex/github-action)，而不是自行安装和验证 CLI。该 action 通过安装 Codex、启动 Responses API 代理，并用可配置的安全策略运行 Codex，来减少 API key 暴露。

不要在会 checkout 或运行仓库控制代码的工作流中，把 `OPENAI_API_KEY` 或 `CODEX_API_KEY` 设置为作业级环境变量。构建脚本、测试、依赖生命周期钩子，或同一作业中被攻陷的 action，都可以读取这些环境变量。

对于其它自动化环境，只为单次 `codex exec` 调用设置 `CODEX_API_KEY`，并确保同一个进程环境中没有运行不受信任的代码。

要为单次运行使用不同的 API key，请内联设置 `CODEX_API_KEY`：

```bash
CODEX_API_KEY= codex exec --json "triage open bug reports"
```

`CODEX_API_KEY` 仅在 `codex exec` 中受支持。

#### 在 CI/CD 中使用 ChatGPT 托管身份验证（高级）

如果你需要用 Codex 用户账户而不是
API key 来运行 CI/CD 作业，请阅读本节，例如在受信任
运行器上使用 ChatGPT 托管 Codex 访问权限的企业团队，或需要 ChatGPT/Codex 速率限制而不是 API key 用量的用户。

API key 是自动化的合适默认选择，因为它们更容易
配置和轮换。只有当你明确需要以
你的 Codex 账户身份运行时，才使用这条路径。

请把 `~/.codex/auth.json` 当作密码对待：它包含访问令牌。不要
提交它、粘贴到工单中，或在聊天中分享。

不要将此工作流用于公共或开源仓库。如果运行器上不能使用 `codex login`，
请通过安全存储注入 `auth.json`，在运行器上运行
Codex，使 Codex 就地刷新它，并在运行之间持久化更新后的文件。

请参阅 [Maintain Codex account auth in CI/CD (advanced)](https://developers.openai.com/codex/auth/ci-cd-auth)。

#### 恢复非交互会话

如果需要继续之前的运行（例如两阶段流水线），请使用 `resume` 子命令：

```bash
codex exec "review the change for race conditions"
codex exec resume --last "fix the race conditions you found"
```

你也可以使用 `codex exec resume <SESSION_ID>` 指定特定会话 ID。

#### 需要 Git 仓库

Codex 要求命令在 Git 仓库内运行，以防止破坏性更改。如果你确认环境是安全的，可以用 `codex exec --skip-git-repo-check` 覆盖此检查。

#### 常见自动化模式

#### 示例：在 GitHub Actions 中自动修复 CI 失败

对于 GitHub Actions 工作流，请使用 [`openai/codex-action`](https://github.com/openai/codex-action)，而不是安装 Codex 并把 API key 传给 shell 步骤。该 action 会为 OpenAI API key 启动安全代理。

你可以使用 Codex 在 CI 工作流失败时自动提出修复。该模式是：

1. 当主 CI 工作流以错误完成时，触发后续工作流。
2. 仅使用仓库读取权限 checkout 失败的 commit。
3. 在 Codex 之前运行设置命令，不向这些步骤暴露你的 OpenAI API key。
4. 运行 Codex GitHub Action。
5. 将 Codex 的本地更改保存为补丁制品。
6. 在单独的作业中应用补丁并打开 pull request。

下面的 Codex 作业只有 `contents: read`。Codex 运行后，它只会将 diff 序列化为制品。`open_pr` 作业会收到仓库写入权限，但不会收到 `OPENAI_API_KEY`。

该示例假设是 Node.js 项目。请调整设置和测试命令以匹配你的技术栈。

更深入的安全检查清单请参阅 [Codex GitHub Action security guidance](https://github.com/openai/codex-action/blob/main/docs/security.md)。

```yaml
name: Codex auto-fix on CI failure

on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]

jobs:
  generate_fix:
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    runs-on: ubuntu-latest
    permissions:
      contents: read
    outputs:
      has_patch: ${{ steps.diff.outputs.has_patch }}
    steps:
      - uses: actions/checkout@v5
        with:
          ref: ${{ github.event.workflow_run.head_sha }}
          fetch-depth: 0
          persist-credentials: false

      - uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install dependencies
        run: |
          if [ -f package-lock.json ]; then npm ci; fi

      - name: Run Codex
        uses: openai/codex-action@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          prompt: |
            The CI workflow "${{ github.event.workflow_run.name }}" failed for commit
            ${{ github.event.workflow_run.head_sha }}.

            Run `npm test --silent` to reproduce the failure. Identify the minimal
            change needed to make the tests pass, implement only that change, and
            run `npm test --silent` again.

            Do not refactor unrelated files.

      - name: Create patch artifact
        id: diff
        run: |
          git add -N .
          git diff --binary HEAD > codex.patch
          if [ -s codex.patch ]; then
            echo "has_patch=true" >> "$GITHUB_OUTPUT"
          else
            echo "has_patch=false" >> "$GITHUB_OUTPUT"
          fi

      - name: Upload patch artifact
        if: steps.diff.outputs.has_patch == 'true'
        uses: actions/upload-artifact@v4
        with:
          name: codex-fix-patch
          path: codex.patch
          if-no-files-found: error

  open_pr:
    runs-on: ubuntu-latest
    needs: generate_fix
    if: needs.generate_fix.outputs.has_patch == 'true'
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v5
        with:
          ref: ${{ github.event.workflow_run.head_sha }}
          fetch-depth: 0

      - uses: actions/download-artifact@v4
        with:
          name: codex-fix-patch

      - name: Apply Codex patch
        run: git apply --index codex.patch

      - name: Open pull request
        env:
          GH_TOKEN: ${{ github.token }}
          FAILED_HEAD_BRANCH: ${{ github.event.workflow_run.head_branch }}
          FAILED_HEAD_SHA: ${{ github.event.workflow_run.head_sha }}
          RUN_ID: ${{ github.event.workflow_run.run_id }}
        run: |
          branch="codex/auto-fix-$RUN_ID"

          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git switch -c "$branch"
          git commit -m "Auto-fix failing CI via Codex"
          git push origin "$branch"

          {
            echo "Codex generated this patch after CI failed for \`$FAILED_HEAD_SHA\`."
            echo
            echo "Review the changes before merging."
          } > pr-body.md

          gh pr create \
            --base "$FAILED_HEAD_BRANCH" \
            --head "$branch" \
            --title "Auto-fix failing CI via Codex" \
            --body-file pr-body.md
```

#### 高级 stdin 管道

当另一个命令为 Codex 生成输入时，请根据指令应来自哪里来选择 stdin 模式。当你已经知道指令，并希望把管道输出作为上下文传入时，使用 prompt-plus-stdin。当 stdin 应成为完整提示时，使用 `codex exec -`。

#### 使用 prompt-plus-stdin

当另一个命令已经生成了你希望 Codex 检查的数据时，prompt-plus-stdin 很有用。在这种模式下，你自己编写指令，并把输出通过管道传入作为上下文，这使它自然适配围绕命令输出、日志和生成数据构建的 CLI 工作流。

```bash
npm test 2>&1 \
  | codex exec "summarize the failing tests and propose the smallest likely fix" \
  | tee test-summary.md
```

#### 更多 prompt-plus-stdin 示例

#### 汇总日志

```bash
tail -n 200 app.log \
  | codex exec "identify the likely root cause, cite the most important errors, and suggest the next three debugging steps" \
  > log-triage.md
```

#### 检查 TLS 或 HTTP 问题

```bash
curl -vv https://api.example.com/health 2>&1 \
  | codex exec "explain the TLS or HTTP failure and suggest the most likely fix" \
  > tls-debug.md
```

#### 准备可发到 Slack 的更新

```bash
gh run view 123456 --log \
  | codex exec "write a concise Slack-ready update on the CI failure, including the likely cause and next step" \
  | pbcopy
```

#### 从 CI 日志草拟 pull request 评论

```bash
gh run view 123456 --log \
  | codex exec "summarize the failure in 5 bullets for the pull request thread" \
  | gh pr comment 789 --body-file -
```
