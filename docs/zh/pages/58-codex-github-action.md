### Codex GitHub Action（GitHub 动作）

Source: [Codex GitHub Action](https://developers.openai.com/codex/github-action.md)

使用 Codex GitHub Action（`openai/codex-action@v1`）在 CI/CD 作业中运行 Codex、应用补丁，或从 GitHub Actions 工作流发布审查。
该 action 会安装 Codex CLI，在你提供 API key 时启动 Responses API 代理，并按照你指定的权限运行 `codex exec`。

当你想要执行以下操作时，请使用该 action：

- 在不自行管理 CLI 的情况下，自动为 pull request 或 release 提供 Codex 反馈。
- 将 Codex 驱动的质量检查作为 CI 流水线的一部分，用来阻止不合格变更。
- 从工作流文件运行可重复的 Codex 任务（代码审查、发布准备、迁移）。

CI 示例请参阅 [Non-interactive mode](60-non-interactive-mode.md)，并在 [openai/codex-action repository](https://github.com/openai/codex-action) 中查看源码。

#### 前提条件

- 将你的 OpenAI key 保存为 GitHub secret（例如 `OPENAI_API_KEY`），并在工作流中引用它。
- 在 Linux 或 macOS 运行器上运行作业。对于 Windows，请设置 `safety-strategy: unsafe`。
- 在调用 action 之前 checkout 你的代码，以便 Codex 可以读取仓库内容。
- 决定要运行哪些 prompt。你可以通过 `prompt` 提供内联文本，或通过 `prompt-file` 指向仓库中提交的文件。

#### 示例工作流

下面的示例工作流会审查新的 pull request，捕获 Codex 的响应，并将其发布回 PR。

```yaml
name: Codex pull request review
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  codex:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    outputs:
      final_message: ${{ steps.run_codex.outputs.final-message }}
    steps:
      - uses: actions/checkout@v5
        with:
          ref: refs/pull/${{ github.event.pull_request.number }}/merge
          persist-credentials: false

      - name: Pre-fetch base and head refs
        env:
          PR_BASE_REF: ${{ github.event.pull_request.base.ref }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
        run: |
          git fetch --no-tags origin \
            "$PR_BASE_REF" \
            "+refs/pull/$PR_NUMBER/head"

      - name: Run Codex
        id: run_codex
        uses: openai/codex-action@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          prompt-file: .github/codex/prompts/review.md
          output-file: codex-output.md

  post_feedback:
    runs-on: ubuntu-latest
    needs: codex
    if: needs.codex.outputs.final_message != ''
    permissions:
      issues: write
      pull-requests: write
    steps:
      - name: Post Codex feedback
        uses: actions/github-script@v7
        with:
          github-token: ${{ github.token }}
          script: |
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.payload.pull_request.number,
              body: process.env.CODEX_FINAL_MESSAGE,
            });
        env:
          CODEX_FINAL_MESSAGE: ${{ needs.codex.outputs.final_message }}
```

将 `.github/codex/prompts/review.md` 替换为你自己的提示文件，或使用 `prompt` 输入提供内联文本。该示例还会将最终 Codex 消息写入 `codex-output.md`，方便之后检查或上传制品。

#### 配置 `codex exec`

通过设置映射到 `codex exec` 选项的 action 输入，微调 Codex 的运行方式：

- `prompt` 或 `prompt-file`（二选一）：内联指令，或指向包含任务的 Markdown/文本文件的仓库路径。可以考虑把提示存放在 `.github/codex/prompts/`。
- `codex-args`：额外 CLI 标志。提供 JSON 数组（例如 `["--ephemeral"]`）或 shell 字符串（`--profile ci`），用于配置会话、配置档或 MCP 设置。
- `model` 和 `effort`：选择你想要的 Codex 代理配置；留空则使用默认值。
- `sandbox`：将沙箱模式（`workspace-write`、`read-only`、`danger-full-access`）与 Codex 在运行期间所需的权限匹配。
- `output-file`：将最终 Codex 消息保存到磁盘，以便后续步骤上传或 diff。
- `codex-version`：固定到特定 CLI release。留空则使用最新发布版本。
- `codex-home`：如果想跨步骤复用配置文件或 MCP 设置，可指向共享的 Codex home 目录。

#### 管理权限

除非你限制它，否则 Codex 在 GitHub 托管运行器上拥有较宽的访问权限。使用以下输入控制暴露面：

- `safety-strategy`（默认 `drop-sudo`）会在运行 Codex 之前移除 `sudo`。这对该作业不可逆，并能保护内存中的 secret。在 Windows 上必须设置 `safety-strategy: unsafe`。
- `unprivileged-user` 将 `safety-strategy: unprivileged-user` 与 `codex-user` 配对，使 Codex 以特定账户运行。确保该用户可以读写仓库 checkout（所有权修复请参阅 [`unprivileged-user` example](https://github.com/openai/codex-action/blob/main/examples/unprivileged-user.yml)）。
- `read-only` 会阻止 Codex 修改文件或使用网络，但它仍然以提升权限运行。不要仅依赖 `read-only` 来保护 secret。
- `sandbox` 会在 Codex 自身内部限制文件系统和网络访问。选择仍能完成任务的最窄选项。
- `allow-users` 和 `allow-bots` 限制谁可以触发工作流。默认只有拥有写入权限的用户可以运行该 action；如需添加额外受信任账户，请显式列出，或留空以使用默认行为。

#### 捕获输出

该 action 会通过 `final-message` 输出发出最后一条 Codex 消息。将其映射为作业输出（如上所示），或在后续步骤中直接处理。如果你希望从运行器收集完整转录，可将 `output-file` 与上传制品功能结合使用。当需要结构化数据时，通过 `codex-args` 传入 `--output-schema` 来强制 JSON 形状。

#### 安全检查清单

- 限制谁可以启动工作流。优先使用受信任事件或显式审批，而不是允许所有人针对你的仓库运行 Codex。
- 清理来自 pull request、commit message 或 issue body 的提示输入，避免提示注入。在输入 Codex 前审查 HTML 注释或隐藏文本。
- 通过保持 `safety-strategy` 为 `drop-sudo`，或将 Codex 移到非特权用户，来保护你的 `OPENAI_API_KEY`。切勿在多租户运行器上让 action 保持 `unsafe` 模式。
- 将 Codex 作为作业中的最后一步运行，避免后续步骤继承任何意外状态变更。
- 如果怀疑 proxy 日志或 action 输出暴露了 secret material，请立即轮换 key。

#### 故障排查

- **你同时设置了 prompt 和 prompt-file**：移除重复输入，确保只提供一个来源。
- **responses-api-proxy didn't write server info**：确认 API key 存在且有效；proxy 只会在你提供 `openai-api-key` 时启动。
- **预期 `sudo` 被移除，但 `sudo` 成功执行**：确保没有早前步骤恢复了 `sudo`，并确认运行器 OS 是 Linux 或 macOS。使用新作业重新运行。
- **`drop-sudo` 后出现权限错误**：在 action 运行前授予写入访问权限（例如使用 `chmod -R g+rwX "$GITHUB_WORKSPACE"`，或采用 unprivileged-user 模式）。
- **Unauthorized trigger blocked**：如果需要允许默认写入协作者之外的服务账户，请调整 `allow-users` 或 `allow-bots` 输入。
