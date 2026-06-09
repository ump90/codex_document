### Codex 应用功能

Source: [Codex app features](https://developers.openai.com/codex/app/features.md)

Codex app 是专注于并行处理 Codex 线程的桌面体验，内置 worktree 支持、自动化和 Git 功能。

大多数 Codex app 功能同时适用于 macOS 和 Windows。以下各节会注明特定平台例外。

---

#### 跨项目多任务处理

使用一个 Codex app 窗口跨项目运行任务。为每个代码库添加一个项目，并按需在它们之间切换。

当你的 Codex 桌面 app 中可用时，你可以要求 Codex 管理本地项目或 worktree 中的线程。例如，要求它查找相关线程、继续现有线程，或固定或归档一个线程。要创建独立的后台线程，请明确提出该请求：`Create a separate background thread in a worktree for this project to update the tests.`

如果你使用过 [Codex CLI](https://developers.openai.com/codex/cli)，项目就像是在特定目录中启动会话。

如果你在包含两个或更多应用或软件包的单个仓库中工作，请将不同项目拆分为单独的 app 项目，使 [沙盒](https://developers.openai.com/codex/agent-approvals-security) 只包含该项目的文件。

#### 技能支持

Codex app 支持与 CLI 和 IDE Extension 相同的 [agent skills](https://developers.openai.com/codex/skills)。你也可以点击侧边栏中的 Skills，查看和探索团队在不同项目中创建的新 skills。

#### 自动化

你还可以将 skills 与 [自动化](https://developers.openai.com/codex/app/automations) 结合，以执行日常任务，例如评估遥测中的错误并提交修复，或创建近期代码库变更报告。对于应保持在一个线程中的持续工作，请使用 [线程自动化](https://developers.openai.com/codex/app/automations#thread-automations)。

#### 模式

每个线程都在所选模式中运行。启动线程时，你可以选择：

- **Local**：直接在当前项目目录中工作。
- **Worktree**：在 Git worktree 中隔离更改。[Learn more](https://developers.openai.com/codex/app/worktrees)。
- **Cloud**：在已配置的云环境中远程运行。

**Local** 和 **Worktree** 线程都会在你的计算机上运行。

有关完整术语表和概念，请浏览 [概念部分](https://developers.openai.com/codex/prompting)。

#### 内置 Git 工具

Codex app 在 app 内直接提供常见 Git 功能。

Diff 面板会显示本地项目或 worktree checkout 中更改的 Git diff。你也可以添加行内评论让 Codex 处理，并暂存或还原特定代码块或整个文件。

你还可以直接从 Codex app 内为本地任务和 worktree 任务提交、推送，并创建 pull request。

对于更高级的 Git 任务，请使用 [集成终端](#integrated-terminal)。

#### 工作树支持

创建新线程时，选择 **Local** 或 **Worktree**。**Local** 直接在你的项目中工作。**Worktree** 会创建新的 [Git worktree](https://git-scm.com/docs/git-worktree)，使更改与你的常规项目隔离。

当你想在不触碰当前工作的情况下尝试新想法，或希望 Codex 在同一项目中并行运行独立任务时，请使用 **Worktree**。

自动化会在 Git 仓库的专用后台 worktree 中运行，在非版本控制项目中则直接在项目目录中运行。

[了解如何在 Codex app 中使用 worktrees。](https://developers.openai.com/codex/app/worktrees)

#### 集成终端

每个线程都包含一个内置终端，作用域限定到当前项目或 worktree。使用 app 右上角的终端图标或按 Cmd+J 来切换它。

使用终端验证更改、运行脚本，并执行 Git 操作，而无需离开 app。Codex 也可以读取当前终端输出，因此它可以检查正在运行的开发服务器状态，或在与你协作时引用失败的构建。

常见任务包括：

- `git status`
- `git pull --rebase`
- `pnpm test` 或 `npm test`
- `pnpm run lint` 或类似项目命令

如果你定期运行某个任务，可以在 [本地环境](https://developers.openai.com/codex/app/local-environments) 中定义一个 **action**，以向 Codex app 窗口顶部添加快捷按钮。

请注意，Cmd+K 会在 Codex app 中打开命令面板。它不会清空终端。要清空终端，请使用 Ctrl+L。

#### 原生 Windows 沙盒

在 Windows 上，Codex 可以在 PowerShell 中原生运行并使用原生 Windows 沙盒，而不要求 WSL 或虚拟机。这让你可以继续使用 Windows 原生工作流，同时保留有边界的权限。

[了解更多 Windows 设置和沙盒信息](https://developers.openai.com/codex/app/windows)。

#### 语音听写

使用语音提示 Codex。当输入框可见时按住 Ctrl+M 并开始说话。你的语音会被转写。编辑转写后的提示词，或点击发送让 Codex 开始工作。

#### 浮动弹出窗口

将活动对话线程弹出到单独窗口，并移动到你正在工作的地方。这非常适合前端工作，因为你可以在快速迭代时将线程放在浏览器、编辑器或设计预览附近。

当你希望它在整个工作流中保持可见时，也可以将弹出窗口切换为置顶显示。

#### 应用内浏览器

使用 [应用内浏览器](https://developers.openai.com/codex/app/browser) 在迭代 Web app 时预览、审查和评论本地开发服务器、基于文件的预览，以及不需要登录的公开页面。

应用内浏览器不支持身份验证流程、已登录页面、你的常规浏览器 profile、cookies、扩展或现有标签页。

使用浏览器评论标记页面上的特定元素或区域，然后要求 Codex 处理该反馈。

当你希望 Codex 直接操作页面时，请对本地开发服务器和基于文件的页面使用 [browser use](https://developers.openai.com/codex/app/browser#browser-use)。你可以从设置管理 Browser plugin、允许的网站和阻止的网站。

#### 计算机使用

[Computer use](https://developers.openai.com/codex/app/computer-use) 通过查看、点击和输入，帮助 Codex 操作 macOS 或 Windows 应用。这对于测试桌面应用、检查浏览器或模拟器流程、处理无法作为插件使用的数据源、更改 app 设置，以及复现仅 GUI 可见的 bug 很有用。

由于 computer use 可能影响项目工作区外部的应用和系统状态，请保持任务范围狭窄，并在继续前审查权限提示。

该功能发布时不适用于 European Economic Area、United Kingdom 或 Switzerland。

#### 处理非代码产物

当任务产生非代码产物时，侧边栏可以预览 PDF 文件、电子表格、文档和演示文稿。向 Codex 提供源数据、预期文件类型、结构，以及你关心的审查标准。

对于电子表格和演示文稿，请描述工作表、列、图表、幻灯片部分和重要检查。要求 Codex 说明它将输出保存在哪里，以及如何检查结果。

使用任务侧边栏跟踪 Codex 在线程运行期间正在做什么。它可以展示智能体的计划、来源、生成产物和任务摘要，使你能够引导工作、检查生成文件，并决定哪些地方需要再处理。

---

#### 与 IDE 扩展同步

如果你已在编辑器中安装 [Codex IDE Extension](https://developers.openai.com/codex/ide)，当 Codex app 和 IDE Extension 位于同一项目时，它们会自动同步。

同步后，你会在 Codex app 输入框中看到 **IDE context** 选项。启用 "Auto context" 后，Codex app 会跟踪你正在查看的文件，因此你可以间接引用它们（例如，“What's this file about?”）。你也可以在 IDE Extension 中看到 Codex app 中运行的线程，反之亦然。

如果你不确定 app 是否包含上下文，请将其关闭，并再次询问同一问题以比较结果。

#### 线程自动化

自动化也可以附加到单个线程。这些线程自动化是周期性唤醒，会保留线程上下文，使 Codex 可以检查长时间运行的工作、轮询来源获取新信息，或继续跟进循环。将它们用于应按计划持续回到同一对话的心跳式自动化。

当下一次运行依赖当前对话时，请使用线程自动化。当你希望 Codex 为一个或多个项目启动新的周期性任务时，请使用独立自动化或项目 [自动化](https://developers.openai.com/codex/app/automations)。

#### 审批和沙盒

你的审批和沙盒设置会约束 Codex 的操作。

- 审批决定 Codex 何时在运行命令前暂停请求权限。
- 沙盒控制 Codex 可以使用哪些目录和网络访问权限。

当你看到 “approve once” 或 “approve for this session” 等提示时，你正在为工具执行授予不同范围的权限。如果不确定，请批准最窄的选项并继续迭代。

默认情况下，Codex 将工作限定到当前项目。在大多数情况下，这是正确的约束。

如果你的任务需要跨多个仓库或目录工作，优先打开单独项目或使用 worktree，而不是要求 Codex 在项目根目录外四处操作。

如果你的工作区中可用 [自动审核](https://developers.openai.com/codex/agent-approvals-security#automatic-approval-reviews)，你可以从权限选择器中选择它。它保持相同的沙盒边界，但会通过已配置的审核策略路由符合条件的审批请求，而不是等待你。

有关高层概览，请参阅 [沙盒](https://developers.openai.com/codex/concepts/sandboxing)。有关配置细节，请参阅 [智能体审批与安全文档](https://developers.openai.com/codex/agent-approvals-security)。

#### MCP 支持

Codex app、CLI 和 IDE Extension 共享 [Model Context Protocol (MCP)](https://developers.openai.com/codex/mcp) 设置。如果你已经在其中一个界面配置了 MCP 服务器，其它界面会自动采用这些配置。要配置新服务器，请打开 app 设置中的 MCP 部分，并启用推荐服务器或向配置添加新服务器。

#### 网页搜索

Codex 自带第一方 web search 工具。对于 Codex app 中的本地任务，Codex 默认启用 web search，并从 web search cache 提供结果。如果你将沙盒配置为 [full access](https://developers.openai.com/codex/agent-approvals-security)，web search 默认使用实时结果。请参阅 [配置基础](https://developers.openai.com/codex/config-basic)，了解如何禁用 web search 或切换到获取最新数据的实时结果。

#### 图像生成

直接在线程中要求 Codex 生成或编辑图像。这适用于 UI 资产、横幅、背景、插图、精灵图表，以及你希望与代码一起创建的占位图。当你希望 Codex 转换或扩展现有资产时，请添加参考图像。

你可以用自然语言提出请求，也可以通过在提示词中包含 `$imagegen` 来显式调用图像生成 skill。

内置图像生成使用 `gpt-image-2`，计入你的通用 Codex 用量限制，并且平均消耗包含额度的速度比不带图像生成的类似轮次快 3-5 倍，具体取决于图像质量和尺寸。详情请参阅 [定价](https://developers.openai.com/codex/pricing#image-generation-usage-limits)。有关提示技巧和模型细节，请参阅 [图像生成指南](https://developers.openai.com/api/docs/guides/image-generation)。

对于更大批量的图像生成，请在你的环境变量中设置 `OPENAI_API_KEY`，并要求 Codex 通过 API 生成图像，这样将按 API 定价计费。
