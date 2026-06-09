### 故障排查

Source: [Troubleshooting](https://developers.openai.com/codex/app/troubleshooting.md)

#### 常见问题

#### 侧边面板出现 Codex 没有编辑过的文件

如果你的项目位于 Git 仓库中，复查面板会根据项目的 Git 状态自动显示变更，包括不是 Codex 做出的变更。

在复查窗格中，你可以在已暂存变更和未暂存变更之间切换，并将你的分支与 main 比较。

如果你只想查看上一次 Codex 回合的变更，请将 diff 窗格切换到 "Last turn changes" 视图。

[进一步了解如何使用复查窗格](38-review.md)。

#### 从侧边栏移除项目

要从侧边栏移除项目，请悬停在项目名称上，点击三个点并选择 "Remove"。要恢复它，请使用 **Threads** 旁边的 **Add new project** 按钮，或使用 Cmd+O 重新添加项目。

#### 查找已归档线程

已归档线程可以在 [Settings](codex://settings) 中找到。当你取消归档一个线程时，它会重新出现在侧边栏中的原始位置。

#### 侧边栏只显示部分线程

侧边栏允许根据项目状态过滤线程。如果你缺少某些线程，请点击 **Threads** 标签旁边的筛选图标，并切换到 Chronological。如果仍然看不到该线程，请打开 [Settings](codex://settings)，检查已归档聊天或已归档线程部分。

#### 代码无法在工作树上运行

工作树会在不同目录中创建，并且只继承签入 Git 的文件。根据你管理项目依赖和工具链的方式，你可能必须使用 [本地环境](37-local-environments.md) 在工作树上运行一些设置脚本。或者，你也可以在常规本地项目中检出这些变更。查看 [工作树文档](42-worktrees.md) 了解更多信息。

#### 应用没有识别队友共享的本地环境

本地环境配置必须位于项目根目录的 `.codex` 文件夹内。如果你在包含多个项目的 monorepo 中工作，请确保你在包含 `.codex` 文件夹的目录中打开项目。

#### Codex 请求访问 Apple Music

根据任务不同，Codex 可能需要浏览文件系统。macOS 上的某些目录（包括 Music、Downloads 或 Desktop）需要用户额外批准。如果 Codex 需要读取你的主目录，macOS 会提示你批准访问这些文件夹。

#### 自动化创建了很多工作树

频繁的自动化可能会随着时间创建许多工作树。归档你不再需要的自动化运行，并避免固定运行，除非你打算保留它们的工作树。

#### 选择错误目标后恢复提示

如果你不小心用错误目标（**Local**、**Worktree** 或 **Cloud**）启动了线程，可以取消当前运行，并在输入区中按向上箭头键恢复之前的提示。

#### 功能可在 Codex CLI 中使用，但不能在 Codex app 中使用

Codex app 和 Codex CLI 使用相同的底层 Codex 智能体和配置，但它们在任何时候都可能依赖不同版本的智能体，并且某些实验功能可能会先进入 Codex CLI。

要获取系统上 Codex CLI 的版本，请运行：

```bash
codex --version
```

要获取 Codex app 捆绑的 Codex 版本，请运行：

```bash
/Applications/Codex.app/Contents/Resources/codex --version
```

#### 反馈和日志

在消息输入区中输入 `/` 可向团队提供反馈。如果你在现有对话中触发反馈，可以选择随反馈一起共享现有会话。提交反馈后，你会收到一个会话 ID，可以与团队共享。

报告问题：

1. 在 Codex GitHub 仓库上查找 [已有 issue](https://github.com/openai/codex/issues)。
2. [打开新的 GitHub issue](https://github.com/openai/codex/issues/new?template=2-bug-report.yml&steps=Uploaded%20thread%3A%20019c0d37-d2b6-74c0-918f-0e64af9b6e14)

更多日志位于以下位置：

- App 日志 (macOS): `~/Library/Logs/com.openai.codex/YYYY/MM/DD`
- 会话转录记录: `$CODEX_HOME/sessions`（默认：`~/.codex/sessions`）
- 已归档会话: `$CODEX_HOME/archived_sessions`（默认：`~/.codex/archived_sessions`）

如果你共享日志，请先审查它们，确认其中不包含敏感信息。

#### 卡住状态和恢复模式

如果线程看起来卡住：

1. 检查 Codex 是否正在等待批准。
2. 打开终端并运行一个基础命令，例如 `git status`。
3. 用更小、更聚焦的提示启动一个新线程。

如果你误取消工作树创建并丢失提示，请在输入区中按向上箭头键恢复它。

#### 终端问题

**终端看起来卡住**

1. 关闭终端面板。
2. 使用 Cmd+J 重新打开。
3. 重新运行一个基础命令，例如 `pwd` 或 `git status`。

如果命令表现不符合预期，请先在终端中验证当前目录和分支。

如果它仍然卡住，请等到你的活动 Codex 线程完成后重启 app。

**字体渲染不正确**

Codex 会为复查窗格、集成终端，以及 app 内显示的任何其他代码使用相同字体。你可以在 [Settings](codex://settings) 面板中将字体配置为 **Code font**。
