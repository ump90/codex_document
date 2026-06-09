### 自定义提示

Source: [Custom Prompts](https://developers.openai.com/codex/custom-prompts.md)

Custom prompts 已弃用。请使用 [skills](48-agent-skills.md) 来提供可复用说明，Codex 可以显式或隐式调用这些说明。

Custom prompts（已弃用）可让你把 Markdown 文件转换为可复用提示，并在 Codex CLI 和 Codex IDE 扩展中作为斜杠命令调用。

Custom prompts 需要显式调用，并位于你的本地 Codex home 目录（例如 `~/.codex`），因此不会通过仓库共享。如果你想共享一个提示（或希望 Codex 隐式调用它），请[使用 skills](48-agent-skills.md)。

1. 创建 prompts 目录：

   ```bash
   mkdir -p ~/.codex/prompts
   ```

2. 创建包含可复用指南的 `~/.codex/prompts/draftpr.md`：

   ```markdown
   ---
   description: Prep a branch, commit, and open a draft PR
   argument-hint: [FILES=] [PR_TITLE=""]
   ---

   Create a branch named `dev/` for this work.
   If files are specified, stage them first: $FILES.
   Commit the staged changes with a clear message.
   Open a draft PR on the same branch. Use $PR_TITLE when supplied; otherwise write a concise summary yourself.
   ```

3. 重启 Codex，使其加载新的 prompt（重启 CLI 会话；如果使用 IDE 扩展，请重新加载该扩展）。

预期：在斜杠命令菜单中输入 `/prompts:draftpr`，会显示你的自定义命令，并带有 front matter 中的 description，以及 files 和 PR title 为可选项的提示。

#### 添加元数据和参数

Codex 会在下一次会话启动时读取 prompt 元数据并解析占位符。

- **Description：** 显示在弹窗中的命令名称下方。请在 YAML front matter 中设置为 `description:`。
- **Argument hint：** 使用 `argument-hint: KEY=` 记录预期参数。
- **位置占位符：** `$1` 到 `$9` 会从你在命令后提供的空格分隔参数中展开。`$ARGUMENTS` 包含全部参数。
- **命名占位符：** 使用 `$FILE` 或 `$TICKET_ID` 等大写名称，并以 `KEY=value` 形式提供值。包含空格的值请加引号（例如 `FOCUS="loading state"`）。
- **字面美元符号：** 写 `$$` 可在展开后的提示中输出单个 `$`。

编辑 prompt 文件后，请重启 Codex 或打开新的聊天，以加载更新。Codex 会忽略 prompts 目录中的非 Markdown 文件。

#### 调用和管理自定义命令

1. 在 Codex（CLI 或 IDE 扩展）中输入 `/`，打开斜杠命令菜单。
2. 输入 `prompts:` 或提示名称，例如 `/prompts:draftpr`。
3. 提供必需参数：

   ```text
   /prompts:draftpr FILES="src/pages/index.astro src/lib/api.ts" PR_TITLE="Add hero animation"
   ```

4. 按 Enter 发送展开后的说明（不需要某个参数时可以跳过）。

预期：Codex 会展开 `draftpr.md` 的内容，用你提供的参数替换占位符，然后将结果作为消息发送。

通过编辑或删除 `~/.codex/prompts/` 下的文件来管理 prompts。Codex 只扫描该文件夹顶层的 Markdown 文件，因此请将每个 custom prompt 直接放在 `~/.codex/prompts/` 下，而不是放在子目录中。
