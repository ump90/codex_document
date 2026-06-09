### 审查

Source: [Review](https://developers.openai.com/codex/app/review.md)

复查窗格帮助你了解 Codex 更改了什么、提供有针对性的反馈，并决定保留哪些内容。

它只适用于位于 Git 仓库中的项目。如果你的项目还不是 Git 仓库，复查窗格会提示你创建一个。

#### 它显示哪些变更

复查窗格反映的是你的 Git 仓库状态，而不只是 Codex 编辑过的内容。这意味着它会显示：

- Codex 做出的变更
- 你自己做出的变更
- 仓库中的任何其他未提交变更

默认情况下，复查窗格聚焦于 **uncommitted changes**。你也可以将范围切换为：

- **All branch changes**（相对于基准分支的 diff）
- **Last turn changes**（仅最近一次 assistant 回合）

本地工作时，你还可以在 **Unstaged** 和 **Staged** 变更之间切换。

#### 浏览复查窗格

- 点击文件名通常会在你选择的编辑器中打开该文件。你可以在 [settings](https://developers.openai.com/codex/app/settings) 中选择默认编辑器。
- 点击文件名背景会展开或折叠 diff。
- 按住 Cmd 时点击单行，会在你选择的编辑器中打开该行。
- 如果你满意某项变更，可以[暂存变更或还原你不喜欢的变更](#staging-and-reverting-files)。

#### 用内联评论提供反馈

内联评论让你可以把反馈直接附加到 diff 中的特定行。这通常是引导 Codex 找到正确修复的最快方式。

要留下内联评论：

1. 打开复查窗格。
2. 悬停在你想评论的行上。
3. 点击出现的 **+** 按钮。
4. 写下反馈并提交。
5. 完成反馈后，向线程发送一条消息。

因为评论是行级别的，Codex 可以比处理一般性指令更精确地回应。

Codex 会将内联评论视为复查指导。留下评论后，发送一条后续消息明确你的意图，例如 "Address the inline comments and keep the scope minimal."

#### 代码审查结果

如果你使用 `/review` 运行代码审查，评论会直接以内联方式显示在复查窗格中。

#### 拉取请求审查

当 Codex 拥有你仓库的 GitHub 访问权限，并且当前项目位于 pull request 分支上时，Codex app 可以帮助你在不离开 app 的情况下处理 pull request 反馈。侧边栏会显示 pull request 上下文和审查者的反馈，复查窗格会在 diff 旁显示评论，因此你可以要求 Codex 在同一线程中处理问题。

安装 GitHub CLI (`gh`) 并使用 `gh auth login` 认证，这样 Codex 才能加载 pull request 上下文、审查评论和变更文件。如果缺少 `gh` 或未认证，pull request 详情可能不会出现在侧边栏或复查窗格中。

当你想把完整修复循环保持在一个地方时，请使用此流程：

1. 在 pull request 分支上打开复查窗格。
2. 审查 pull request 上下文、评论和变更文件。
3. 要求 Codex 修复你想处理的具体评论。
4. 在复查窗格中检查生成的 diff。
5. 准备好后，将变更暂存、提交并推送到 PR 分支。

对于 GitHub 触发的审查，请参阅 [Use Codex in GitHub](https://developers.openai.com/codex/integrations/github)。

#### 暂存和还原文件

复查窗格包含 Git 操作，让你可以在提交前整理 diff。

你可以在这些层级暂存、取消暂存或还原变更：

- **Entire diff**：使用复查标题中的操作按钮（例如 "Stage all" 或 "Revert all"）
- **Per file**：暂存、取消暂存或还原单个文件
- **Per hunk**：暂存、取消暂存或还原单个 hunk

当你想接受一部分工作时使用暂存；当你想丢弃它时使用还原。

#### 已暂存和未暂存状态

Git 可以在同一文件中同时表示已暂存和未暂存变更。发生这种情况时，在已暂存和未暂存视图中可能看起来像窗格显示了 "the same file twice"。这是正常的 Git 行为。
