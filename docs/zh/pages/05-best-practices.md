### 最佳实践

Source: [Best practices](https://developers.openai.com/codex/learn/best-practices.md)

如果你刚开始使用 Codex 或编程代理，本指南会帮助你更快获得更好的结果。它涵盖让 Codex 在 [CLI](https://developers.openai.com/codex/cli)、[IDE 扩展](https://developers.openai.com/codex/ide) 和 [Codex app](https://developers.openai.com/codex/app) 中更有效的核心习惯，从提示和规划，到验证、MCP、技能和自动化。

当你少把 Codex 当成一次性助手，而更多把它当成一个会被你配置并随时间改进的队友时，它的效果最好。

一个有用的思考方式是：从正确的任务上下文开始，使用 `AGENTS.md` 提供持久指导，配置 Codex 以匹配你的工作流，用 MCP 连接外部系统，把重复工作转化为技能，并自动化稳定的工作流。

#### 良好起步：上下文和提示

即使你的提示并不完美，Codex 也已经足够强大，可以提供实际帮助。你通常可以用很少的设置把一个困难问题交给它，并获得不错的结果。清晰的 [提示](https://developers.openai.com/codex/prompting) 并不是获得价值的前提，但它确实会让结果更可靠，尤其是在更大的代码库或更高风险的任务中。

如果你在大型或复杂仓库中工作，最大的提升来自于给 Codex 正确的任务上下文，并清楚说明你想完成的事情结构。

一个好的默认做法是在提示中包含四件事：

- **目标：** 你想改变或构建什么？
- **上下文：** 哪些文件、文件夹、文档、示例或错误与此任务相关？你可以 @ 提及某些文件作为上下文。
- **约束：** Codex 应该遵循哪些标准、架构、安全要求或约定？
- **完成条件：** 在任务完成之前应该满足什么条件，例如测试通过、行为变化，或 bug 不再复现？

这有助于 Codex 保持范围明确、减少假设，并产出更容易审查的工作。

根据任务难度选择推理级别，并测试哪种设置最适合你的工作流。不同用户和任务最适合的设置不同。

- Low 适合更快、范围明确的任务
- Medium 或 High 适合更复杂的变更或调试
- Extra High 适合长期、代理式、推理密集型任务

为了更快提供上下文，可以尝试在 Codex app 中使用语音听写来
口述你希望 Codex 做什么，而不是打字。

#### 困难任务先做计划

如果任务复杂、模糊，或很难描述清楚，请让 Codex 在开始编码前先制定计划。

有几种方法效果很好：

**使用 Plan mode：** 对大多数用户来说，这是最简单也最有效的选项。Plan mode 让 Codex 在实现前收集上下文、提出澄清问题，并构建更强的计划。使用 `/plan` 或 Shift+Tab 切换。

**让 Codex 访谈你：** 如果你大致知道自己想要什么，但不确定如何清楚描述，请让 Codex 先向你提问。告诉它挑战你的假设，并在写代码前把模糊想法转化为具体内容。

**使用 PLANS.md 模板：** 对于更高级的工作流，你可以配置 Codex，让它遵循 `PLANS.md` 或执行计划模板来处理运行时间更长或多步骤的工作。更多细节请参见 [执行计划指南](https://developers.openai.com/cookbook/articles/codex_exec_plans)。

#### 用 `AGENTS.md` 复用指导

一旦某种提示模式有效，下一步就是停止手动重复它。这正是 [AGENTS.md](https://developers.openai.com/codex/guides/agents-md) 的用途。

可以把 `AGENTS.md` 看作面向代理的开放格式 README。它会自动加载进上下文，也是记录你和团队希望 Codex 在仓库中如何工作的最佳位置。

一个好的 `AGENTS.md` 会涵盖：

- 仓库布局和重要目录
- 如何运行项目
- 构建、测试和 lint 命令
- 工程约定和 PR 期望
- 约束和禁止事项
- 完成意味着什么，以及如何验证工作

CLI 中的 `/init` 斜杠命令是在当前目录脚手架生成初始 `AGENTS.md` 的快速启动命令。它是很好的起点，但你应该编辑结果，让它匹配团队实际构建、测试、审查和发布代码的方式。

你可以在不同层级创建 `AGENTS.md` 文件：位于 `~/.codex` 中的全局 `AGENTS.md` 用作个人默认值，仓库级文件用于共享标准，子目录中的更具体文件用于局部规则。如果在更靠近当前目录的位置存在更具体的文件，则该指导优先生效。

保持实用。一个简短、准确的 `AGENTS.md` 比充满模糊规则的长文件更有用。从基础开始，然后只在你发现重复错误后添加新规则。

如果 `AGENTS.md` 变得过大，请保持主文件简洁，并引用针对任务的 Markdown 文件，例如规划、代码审查或架构相关文档。

当 Codex 第二次犯同样错误时，让它做一次回顾并更新
`AGENTS.md`。指导会保持实用，并基于真实摩擦。

#### 配置 Codex 以保持一致

配置是让 Codex 在不同会话和使用界面中表现更一致的主要方式之一。例如，你可以为模型选择、推理强度、沙箱模式、审批策略、配置档案和 MCP 设置配置默认值。

一个好的起点模式是：

- 将个人默认值保存在 `~/.codex/config.toml`（Codex app 中的 Settings → Configuration → Open config.toml）
- 将仓库特定行为保存在 `.codex/config.toml`
- 仅在一次性场景中使用命令行覆盖（如果你使用 CLI）

[`config.toml`](https://developers.openai.com/codex/config-basic) 是定义持久偏好的位置，例如 MCP 服务器、多代理设置和功能开关。特定配置档案的覆盖项位于单独的 `$CODEX_HOME/profile-name.config.toml` 文件中。

Codex 自带操作系统级沙箱，并有两个你可以控制的关键旋钮。Approval mode（审批模式）决定 Codex 何时需要在运行命令前请求你的许可，sandbox mode（沙箱模式）决定 Codex 是否可以在目录中读写，以及代理可以访问哪些文件。

如果你刚开始使用编码代理，请从默认权限开始。默认保持审批和沙箱严格，然后只在需求明确后，为可信仓库或特定工作流放宽权限。

请注意，CLI、IDE 和 Codex app 共享同一套配置层。可在 [示例配置](https://developers.openai.com/codex/config-sample) 页面了解更多。

尽早为真实环境配置 Codex。许多质量问题实际上是设置问题，例如工作目录错误、缺少写权限、模型默认值错误，或缺少工具和连接器。

#### 用测试和审查提高可靠性

不要止步于要求 Codex 做出变更。需要时让它创建测试、运行相关检查、确认结果，并在你接受之前审查工作。

Codex 可以为你完成这个循环，但前提是它知道“好”的标准是什么。该指导可以来自提示，也可以来自 `AGENTS.md`。

这可以包括：

- 为变更编写或更新测试
- 运行正确的测试套件
- 检查 lint、格式化或类型检查
- 确认最终行为符合请求
- 审查 diff 中的 bug、回归或风险模式

在 Codex app 中切换 diff 面板，可以直接在本地 [审查变更](https://developers.openai.com/codex/app/review)。点击特定行即可提供反馈，该反馈会作为上下文传入下一轮 Codex。

这里一个有用的选项是斜杠命令 `/review`，它提供几种代码审查方式：

- 针对基准分支做 PR 风格审查
- 审查未提交的变更
- 审查某个提交
- 使用自定义审查说明

如果你和团队有 `code_review.md` 文件，并从 `AGENTS.md` 引用它，Codex 在审查期间也可以遵循这些指导。对于希望审查行为在仓库和贡献者之间保持一致的团队来说，这是一个很强的模式。

Codex 不应该只是生成代码。通过正确说明，它也可以帮助 **测试代码、检查代码并审查代码**。

如果你使用 GitHub Cloud，可以设置 Codex 为你的 PR 运行 [代码审查](https://developers.openai.com/codex/integrations/github)。在 OpenAI，Codex 会审查 100% 的 PR。你可以启用自动审查，也可以在 @Codex 时让 Codex 响应式审查。
