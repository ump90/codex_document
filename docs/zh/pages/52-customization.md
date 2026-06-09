### 自定义

Source: [Customization](https://developers.openai.com/codex/concepts/customization.md)

自定义是让 Codex 按照你团队工作方式运行的方法。

在 Codex 中，customization 来自几个协同工作的层：

- 用于持久说明的**项目指南（`AGENTS.md`）**
- 用于保存从以往工作中学到的有用上下文的 **[Memories](74-memories.md)**
- 用于可复用工作流和领域专业知识的 **Skills**
- 用于访问外部工具和共享系统的 **[MCP](53-model-context-protocol.md)**
- 用于把工作委派给专门 subagents 的 **[Subagents](68-subagents.md)**

这些层是互补的，而不是相互竞争的。`AGENTS.md` 塑造行为，memories 延续本地上下文，skills 打包可重复流程，[MCP](53-model-context-protocol.md) 将 Codex 连接到本地工作区之外的系统。

#### AGENTS 指南

`AGENTS.md` 为 Codex 提供持久的项目指南，它会随仓库一起移动，并在代理开始工作前生效。请保持简洁。

用它记录你希望 Codex 每次在 repo 中都遵循的规则，例如：

- 构建和测试命令
- 审查预期
- 仓库特定约定
- 目录特定说明

当代理对你的代码库做出错误假设时，请在 `AGENTS.md` 中纠正，并让代理更新 `AGENTS.md`，这样修复会持续保留。把它当作反馈循环。

**更新 `AGENTS.md`：** 从真正重要的说明开始。将反复出现的审查反馈固化下来，把指南放在最接近其适用位置的目录中，并在你纠正某件事时告诉代理更新 `AGENTS.md`，让未来会话继承该修复。

#### 何时更新 `AGENTS.md`

- **重复错误**：如果代理反复犯同样的错误，请添加规则。
- **阅读过多**：如果它找到了正确文件，但读取了太多文档，请添加路由指南（优先查看哪些目录/文件）。
- **重复出现的 PR 反馈**：如果你不止一次留下相同反馈，请将其固化。
- **在 GitHub 中**：在 pull request 评论中，用请求标记 `@codex`（例如 `@codex add this to AGENTS.md`），把更新委派给云端任务。
- **自动化漂移检查**：使用 [automations](24-automations.md) 运行重复检查（例如每天），查找指南缺口，并建议要添加到 `AGENTS.md` 的内容。

将 `AGENTS.md` 与执行这些规则的基础设施搭配使用：pre-commit hooks、linters 和 type checkers 会在你看到问题之前捕获它们，因此系统会更善于防止重复错误。

Codex 可以从多个位置加载指南：Codex home 目录中的全局文件（面向你作为开发者）以及团队可以签入的仓库特定文件。离工作目录更近的文件优先级更高。
使用全局文件来塑造 Codex 与你的沟通方式（例如审查风格、详细程度和默认值），并让仓库文件专注于团队和代码库规则。

[Custom instructions with AGENTS.md](50-custom-instructions-with-agents-md.md)

#### 技能

Skills 为 Codex 提供可复用能力，用于可重复工作流。
Skills 通常最适合可复用工作流，因为它们支持更丰富的说明、脚本和参考资料，同时能跨任务复用。
Skills 会被加载并对代理可见（至少其元数据可见），因此 Codex 可以发现并隐式选择它们。这让丰富工作流可用，同时不会在一开始就膨胀上下文。

使用 skill 文件夹在本地创作和迭代工作流。如果该工作流已有 plugin，请优先安装它，以复用经过验证的设置。当你想在团队之间分发自己的工作流，或把它与 app 集成捆绑时，请将其打包为 [plugin](69-build-plugins.md)。Skills 仍是创作格式；plugins 是可安装的分发单元。

一个 skill 通常是一个 `SKILL.md` 文件，加上可选脚本、参考资料和资源。

skill 目录可以包含一个 `scripts/` 文件夹，其中放置 Codex 作为工作流一部分调用的 CLI 脚本（例如为数据设定初始值或运行校验）。当工作流需要外部系统（issue tracker、设计工具、文档服务器）时，请将 skill 与 [MCP](53-model-context-protocol.md) 搭配使用。

示例 `SKILL.md`：

```md
---
name: commit
description: Stage and commit changes in semantic groups. Use when the user wants to commit, organize commits, or clean up a branch before pushing.
---

1. Do not run `git add .`. Stage files in logical groups by purpose.
2. Group into separate commits: feat → test → docs → refactor → chore.
3. Write concise commit messages that match the change scope.
4. Keep each commit focused and reviewable.
```

使用 skills 处理：

- 可重复工作流（发布步骤、审查流程、文档更新）
- 团队特定专业知识
- 需要示例、参考资料或辅助脚本的流程

Skills 可以是全局的（在你的用户目录中，面向你作为开发者），也可以是仓库特定的（签入 `.agents/skills`，面向你的团队）。当工作流适用于某个项目时，把仓库 skills 放在 `.agents/skills` 中；对于你希望跨所有仓库使用的 skills，请使用你的用户目录。

| 层级   | 全局                   | 仓库                                           |
| :----- | :--------------------- | :--------------------------------------------- |
| AGENTS | `~/.codex/AGENTS.md`   | 仓库根目录或嵌套目录中的 `AGENTS.md` |
| Skills | `$HOME/.agents/skills` | `.agents/skills` in repo                       |

Codex 对 skills 使用渐进式披露：

- 它从元数据（`name`、`description`）开始用于发现
- 只有在选择某个 skill 时才加载 `SKILL.md`
- 只有在需要时才读取参考资料或运行脚本

Skills 可以被显式调用；当任务匹配 skill 描述时，Codex 也可以隐式选择它们。清晰的 skill 描述会提高触发可靠性。

[Agent Skills](48-agent-skills.md)

#### MCP

MCP（Model Context Protocol）是将 Codex 连接到外部工具和上下文提供方的标准方式。
它特别适用于远程托管系统，例如 Figma、Linear、GitHub，或你的团队依赖的内部知识服务。

当 Codex 需要本地仓库之外的能力时，请使用 MCP，例如 issue tracker、设计工具、浏览器或共享文档系统。

一种理解方式：

- **Host**：Codex
- **Client**：Codex 内部的 MCP 连接
- **Server**：外部工具或上下文提供方

MCP servers 可以暴露：

- **Tools**（操作）
- **Resources**（可读取数据）
- **Prompts**（可复用提示模板）

这种分离有助于你推理信任和能力边界。有些 servers 主要提供上下文，而另一些会暴露强大的操作。

在实践中，MCP 与 skills 搭配时通常最有用：

- skill 定义工作流，并指定要使用的 MCP 工具

[Model Context Protocol](53-model-context-protocol.md)

#### 子智能体

你可以创建具有不同角色的不同 agents，并提示它们以不同方式使用工具。例如，一个 agent 可能运行特定测试命令和配置，而另一个 agent 拥有用于获取生产日志进行调试的 MCP servers。每个 subagent 都保持专注，并使用适合其工作的工具。

[Subagent concepts](68-subagents.md)

#### 技能与 MCP 配合使用

Skills 加 MCP 是这些能力组合在一起的地方：skills 定义可重复工作流，MCP 将它们连接到外部工具和系统。
如果某个 skill 依赖 MCP，请在 `agents/openai.yaml` 中声明该依赖，以便 Codex 能自动安装和连接它（参见 [Agent Skills](48-agent-skills.md)）。

#### 后续步骤

按以下顺序构建：

1. 使用 [Custom instructions with AGENTS.md](50-custom-instructions-with-agents-md.md)，让 Codex 遵循你的仓库约定。添加 pre-commit hooks 和 linters 来执行这些规则。
2. 当已有可复用工作流时，安装一个 [plugin](78-plugins.md)。否则，创建一个 [skill](48-agent-skills.md)，并在想共享时把它打包为 plugin。
3. 当工作流需要外部系统（Linear、GitHub、文档服务器、设计工具）时，使用 [MCP](53-model-context-protocol.md)。
4. 当你准备把嘈杂或专门任务委派给 subagents 时，使用 [Subagents](81-subagents-2.md)。
