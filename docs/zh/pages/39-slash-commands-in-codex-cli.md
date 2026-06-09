### Codex CLI 中的斜杠命令

Source: [Slash commands in Codex CLI](https://developers.openai.com/codex/cli/slash-commands.md)

斜杠命令为你提供快速、键盘优先的 Codex 控制方式。在输入区中输入 `/` 打开斜杠弹窗，选择一个命令，Codex 就会执行切换模型、调整权限或总结长对话等操作，而无需离开终端。

本指南说明如何：

- 为任务找到合适的内置斜杠命令
- 使用 `/model`、`/fast`、`/personality`、`/permissions`、`/approve`、`/raw`、`/agent` 和 `/status` 等命令引导活动会话

#### 内置斜杠命令

Codex 随附以下命令。打开斜杠弹窗并开始输入命令名称以筛选列表。

当任务已经运行时，你可以输入斜杠命令并按 `Tab` 将它排队到下一轮。Codex 会在运行时解析排队的斜杠命令，因此命令菜单和错误会在当前轮完成后出现。斜杠补全在你排队命令前仍然有效。

| 命令                                                                            | 用途                                                | 何时使用                                                                       |
| ------------------------------------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------ |
| [`/permissions`](#update-permissions-with-permissions)                          | 设置 Codex 可以在不先询问的情况下做什么。           | 在会话中途放宽或收紧批准要求，例如在 Auto 和 Read Only 间切换。                |
| [`/ide`](#include-ide-context-with-ide)                                         | 包含打开文件、当前选择和其他 IDE 上下文。           | 将编辑器上下文拉入下一条提示，而无需重新解释 IDE 中打开了什么。                |
| [`/keymap`](#remap-tui-shortcuts-with-keymap)                                   | 重新映射 TUI 键盘快捷键。                           | 检查并持久化 `config.toml` 中的自定义快捷键绑定。                              |
| [`/vim`](#toggle-vim-mode-with-vim)                                             | 切换输入区的 Vim 模式。                             | 在 Vim normal/insert 行为和默认输入区编辑模式之间切换。                        |
| [`/sandbox-add-read-dir`](#grant-sandbox-read-access-with-sandbox-add-read-dir) | 授予沙盒对额外目录的读取访问权限（仅 Windows）。    | 解除需要读取当前可读根目录之外绝对目录路径的命令阻塞。                         |
| [`/agent`](#switch-agent-threads-with-agent)                                    | 切换活动智能体线程。                                | 检查或继续已生成子智能体线程中的工作。                                         |
| [`/apps`](#browse-apps-with-apps)                                               | 浏览应用（连接器）并将它们插入提示。                | 在要求 Codex 使用某个应用前，将其作为 `$app-slug` 附加。                       |
| [`/plugins`](#browse-plugins-with-plugins)                                      | 浏览已安装和可发现的插件。                          | 检查插件工具、安装建议的插件，或管理插件可用性。                               |
| [`/hooks`](#review-hooks-with-hooks)                                            | 审查生命周期 hook。                                 | 检查已配置 hook，信任新的或已更改的 hook，或在非托管 hook 运行前禁用它们。     |
| [`/clear`](#clear-the-terminal-and-start-a-new-chat-with-clear)                 | 清空终端并开始新的聊天。                            | 当你想重新开始时，同时重置可见 UI 和对话。                                     |
| [`/compact`](#keep-transcripts-lean-with-compact)                               | 总结可见对话以释放 token。                          | 在长时间运行后使用，让 Codex 保留关键点而不撑满上下文窗口。                    |
| [`/copy`](#copy-the-latest-response-with-copy)                                  | 复制最近完成的 Codex 输出。                         | 无需手动选择即可获取最近完成的响应或计划文本。你也可以按 `Ctrl+O`。           |
| [`/diff`](#review-changes-with-diff)                                            | 显示 Git diff，包括 Git 尚未跟踪的文件。            | 在 commit 或运行测试前审查 Codex 的编辑。                                      |
| [`/exit`](#exit-the-cli-with-quit-or-exit)                                      | 退出 CLI（与 `/quit` 相同）。                       | 另一种拼写；两个命令都会退出会话。                                             |
| [`/experimental`](#toggle-experimental-features-with-experimental)              | 切换实验功能。                                      | 从 CLI 启用 subagents 等可选功能。                                             |
| [`/approve`](#approve-an-auto-review-denial-with-approve)                       | 批准最近自动审查拒绝后的一次重试。                  | 重试被自动审查器拒绝的命令或操作。                                             |
| [`/memories`](#configure-memories-with-memories)                                | 配置记忆使用和生成。                                | 不离开 TUI 即可开启或关闭记忆注入或记忆生成。                                  |
| [`/skills`](#use-skills-with-skills)                                            | 浏览和使用技能。                                    | 通过选择相关本地技能改进特定任务行为。                                         |
| [`/hooks`](#view-lifecycle-hooks-with-hooks)                                    | 查看和管理生命周期 hook。                           | 检查加载到当前会话的 hook 配置。                                               |
| [`/feedback`](#send-feedback-with-feedback)                                     | 向 Codex 维护者发送日志。                           | 报告问题或与支持团队共享诊断信息。                                             |
| [`/init`](#generate-agentsmd-with-init)                                         | 在当前目录生成 `AGENTS.md` 脚手架。                 | 捕获你正在处理的仓库或子目录的持久指令。                                       |
| [`/logout`](#sign-out-with-logout)                                              | 登出 Codex。                                        | 在共享机器上清除本地凭据。                                                     |
| [`/mcp`](#list-mcp-tools-with-mcp)                                              | 列出已配置的 Model Context Protocol (MCP) 工具。    | 检查 Codex 在会话中可以调用哪些外部工具；添加 `verbose` 查看服务器详情。       |
| [`/mention`](#highlight-files-with-mention)                                     | 将文件附加到对话。                                  | 指向你希望 Codex 接下来检查的特定文件或文件夹。                                |
| [`/model`](#set-the-active-model-with-model)                                    | 选择活动模型（可用时也包括推理强度）。              | 在运行任务前，在通用模型 (`gpt-4.1-mini`) 和更深推理模型之间切换。             |
| [`/fast`](#toggle-fast-mode-with-fast)                                          | 当模型目录提供 Fast 服务层级时切换它。              | 开启或关闭当前模型的 Fast 层级，或检查线程是否正在使用它。                    |
| [`/plan`](#switch-to-plan-mode-with-plan)                                       | 切换到计划模式，并可选择发送提示。                  | 要求 Codex 在实现工作开始前提出执行计划。                                      |
| [`/goal`](#set-or-view-a-task-goal-with-goal)                                   | 设置、暂停、恢复、查看或清除任务目标。              | 给 Codex 一个持久目标，在较大任务运行期间跟踪。                                |
| [`/personality`](#set-a-communication-style-with-personality)                   | 为响应选择沟通风格。                                | 让 Codex 更简洁、更具解释性或更协作，而无需更改你的指令。                     |
| [`/ps`](#check-background-terminals-with-ps)                                    | 显示实验性后台终端及其最近输出。                    | 不离开主转录记录即可检查长时间运行的命令。                                     |
| [`/stop`](#stop-background-terminals-with-stop)                                 | 停止所有后台终端。                                  | 取消当前会话启动的后台终端工作。                                               |
| [`/fork`](#fork-the-current-conversation-with-fork)                             | 将当前对话 fork 到新线程。                          | 从活动会话分支出新线程来探索新方法，而不丢失当前转录记录。                    |
| [`/side`, `/btw`](#start-a-side-conversation-with-side)                         | 启动一个临时旁路对话。                              | 提出聚焦的后续问题，而不打扰主线程转录记录。                                   |
| [`/raw`](#toggle-raw-scrollback-with-raw)                                       | 切换原始回滚缓冲模式。                              | 在审查长输出时，让终端选择和复制减少格式化。                                   |
| [`/resume`](#resume-a-saved-conversation-with-resume)                           | 从会话列表恢复已保存对话。                          | 从之前的 CLI 会话继续工作，而不用重新开始。                                    |
| [`/new`](#start-a-new-conversation-with-new)                                    | 在同一个 CLI 会话内开始新对话。                     | 当你想在同一仓库中用新提示重置聊天上下文，而不离开 CLI。                      |
| [`/quit`](#exit-the-cli-with-quit-or-exit)                                      | 退出 CLI。                                          | 立即离开会话。                                                                 |
| [`/review`](#ask-for-a-working-tree-review-with-review)                         | 要求 Codex 审查你的工作树。                         | 在 Codex 完成工作后，或当你希望对本地变更再多一组视角时运行。                 |
| [`/status`](#inspect-the-session-with-status)                                   | 显示会话配置和 token 用量。                         | 确认活动模型、批准策略、可写根目录和剩余上下文容量。                           |
| [`/debug-config`](#inspect-config-layers-with-debug-config)                     | 打印配置层和要求诊断信息。                          | 调试优先级和策略要求，包括实验性网络约束。                                     |
| [`/statusline`](#configure-footer-items-with-statusline)                        | 交互式配置 TUI 状态行字段。                         | 选择并重排页脚项（model/context/limits/git/tokens/session），并持久化到 `config.toml`。 |
| [`/title`](#configure-terminal-title-items-with-title)                          | 交互式配置终端窗口或标签页标题字段。                | 选择并重排标题项，例如 project、status、thread、branch、model 和 task progress。 |
| [`/theme`](#choose-a-syntax-theme-with-theme)                                   | 选择语法高亮主题。                                  | 预览并持久化终端语法高亮主题。                                                 |

`/quit` 和 `/exit` 都会退出 CLI。只有在你已保存或提交任何重要工作后才使用它们。

使用 `/permissions` 调整 Codex 可以在不先询问的情况下做什么。只有在需要重试最近被 automatic review 拒绝的操作时，才使用 `/approve`。

#### 使用斜杠命令控制会话

以下工作流可让你的会话保持在轨道上，而无需重启 Codex。

#### 使用 `/model` 设置活动模型

1. 启动 Codex 并打开输入区。
2. 输入 `/model` 并按 Enter。
3. 从弹窗中选择模型，例如 `gpt-4.1-mini` 或 `gpt-4.1`。

预期结果：Codex 会在转录记录中确认新模型。运行 `/status` 验证更改。

#### 使用 `/fast` 切换 Fast 模式

1. 输入 `/fast on`、`/fast off` 或 `/fast status`。
2. 如果你希望该设置持久化，请在 Codex 提示保存时确认更新。

预期结果：Codex 会报告当前模型的 Fast 服务层级在当前线程中是开启还是关闭。在 TUI 页脚中，你也可以使用 `/statusline` 显示 Fast 模式状态行项目。

Fast 层级命令由目录驱动。如果当前模型没有声明 Fast 层级，Codex 不会显示 `/fast`。

#### 使用 `/personality` 设置沟通风格

使用 `/personality` 可以更改 Codex 的沟通方式，而无需重写提示。

1. 在活动对话中，输入 `/personality` 并按 Enter。
2. 从弹窗中选择一种风格。

预期结果：Codex 会在转录记录中确认新的风格，并在该线程后续响应中使用它。

Codex 支持 `friendly`、`pragmatic` 和 `none` 风格。使用 `none` 可禁用风格指令。

如果活动模型不支持特定风格指令，Codex 会隐藏此命令。

#### 使用 `/plan` 切换到计划模式

1. 输入 `/plan` 并按 Enter，将活动对话切换到计划模式。
2. 可选：提供内联提示文本（例如 `/plan Propose a
migration plan for this service`）。
3. 使用内联 `/plan` 参数时，你可以粘贴内容或附加图片。

预期结果：Codex 进入计划模式，并使用你的可选内联提示作为第一个规划请求。

当任务已经运行时，`/plan` 会暂时不可用。

#### 使用 `/goal` 设置或查看任务目标

1. 输入 `/goal ` 设置目标，例如 `/goal Finish the migration and keep tests green`。
2. 输入 `/goal` 查看当前目标。
3. 使用 `/goal pause`、`/goal resume` 或 `/goal clear` 暂停、恢复或移除它。

预期结果：Codex 会在工作继续时，将目标附加到活动线程。

目标内容必须非空，且最多 4,000 个字符。对于更长指令，请将详情放入文件，并让目标指向该文件。

#### 使用 `/experimental` 切换实验功能

1. 输入 `/experimental` 并按 Enter。
2. 切换你想要的功能（例如 Apps 或 Smart Approvals），如果提示要求重启 Codex，请重启。

预期结果：Codex 会将你的功能选择保存到配置，并在重启后应用。

#### 使用 `/approve` 批准自动审查拒绝

当自动审查器拒绝了最近的操作，而你希望 Codex 重试一次时，使用 `/approve`。

1. 输入 `/approve`。
2. 当 Codex 显示相关被拒绝操作时，确认重试。

预期结果：Codex 会在当前会话策略下重试该被拒绝操作一次。

#### 使用 `/memories` 配置记忆

1. 输入 `/memories`。
2. 选择 Codex 应使用现有记忆、生成新记忆，还是保持记忆行为禁用。

预期结果：Codex 会更新未来会话的相关记忆设置。

#### 使用 `/skills` 使用技能

1. 输入 `/skills`。
2. 选择你希望 Codex 应用的技能。

预期结果：Codex 会插入所选技能上下文，使下一个请求遵循该技能的指令。

#### 使用 `/hooks` 查看生命周期 hook

1. 输入 `/hooks`。
2. 审查已加载的生命周期 hook 配置。

预期结果：Codex 会显示当前会话中可运行的 hook。

#### 使用 `/clear` 清空终端并开始新聊天

1. 输入 `/clear` 并按 Enter。

预期结果：Codex 会清空终端、重置可见转录记录，并在同一 CLI 会话中开始新聊天。

与 Ctrl+L 不同，`/clear` 会开始新对话。

Ctrl+L 只清空终端视图，并保留当前聊天。Codex 会在任务进行中禁用这两个操作。

#### 使用 `/permissions` 更新权限

1. 输入 `/permissions` 并按 Enter。
2. 选择与你的舒适程度匹配的批准预设，例如适合免手动运行的 `Auto`，或用于审查编辑的 `Read Only`。当命名权限配置处于活动状态时，选择器也会显示已配置的自定义配置及其说明。

预期结果：Codex 会宣布更新后的策略。后续操作会遵循更新后的批准模式，直到你再次更改。

#### 使用 `/ide` 包含 IDE 上下文

1. 输入 `/ide`。
2. 如果你想说明 Codex 应如何处理当前 IDE 选区或打开的文件，可以添加可选内联文本。

预期结果：Codex 会在下一条提示中包含可用的 IDE context。

#### 使用 `/vim` 切换 Vim 模式

1. 输入 `/vim`。
2. 继续在输入区中编辑。

预期结果：Codex 会切换当前会话的输入区 Vim 模式。若要让 Vim 模式成为新会话的默认模式，请在 `config.toml` 中设置 `tui.vim_mode_default = true`。
