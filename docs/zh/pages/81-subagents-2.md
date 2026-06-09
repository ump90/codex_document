### 子智能体

Source: [Subagents](https://developers.openai.com/codex/subagents.md)

Codex 可以通过并行生成专门的 agents 来运行 subagent workflows，然后在一个响应中收集它们的结果。这对于高度并行的复杂任务尤其有用，例如代码库探索或实现多步骤功能计划。

借助 subagent workflows，你还可以根据任务定义具有不同模型配置和说明的自定义 agents。

有关 subagent workflows 背后的概念和权衡，包括上下文污染、上下文劣化和模型选择指导，请参阅 [Subagent concepts](68-subagents.md)。

#### 可用性

当前 Codex 版本默认启用 subagent workflows。

Subagent activity 目前会在 Codex app 和 CLI 中显示。IDE Extension 中的可见性即将推出。

Codex 只会在你明确要求时生成 subagents。由于每个 subagent 都会执行自己的模型和工具工作，subagent workflows 会比可比的单 agent 运行消耗更多 tokens。

#### 典型工作流

Codex 负责 agents 之间的编排，包括生成新的 subagents、路由后续说明、等待结果，以及关闭 agent threads。

当许多 agents 正在运行时，Codex 会等到所有请求的结果都可用，然后返回一个汇总响应。

Codex 只会在你明确要求时生成新的 agent。

要查看实际效果，请在你的项目上尝试以下 prompt：

```text
I would like to review the following points on the current PR (this branch vs main). Spawn one agent per point, wait for all of them, and summarize the result for each point.
1. Security issue
2. Code quality
3. Bugs
4. Race
5. Test flakiness
6. Maintainability of the code
```

#### 管理子智能体

- 在 CLI 中使用 `/agent` 在活动 agent threads 之间切换，并检查正在进行的 thread。
- 直接要求 Codex 引导正在运行的 subagent、停止它，或关闭已完成的 agent threads。

#### 审批和沙箱控制

Subagents 会继承你当前的沙箱策略。

在交互式 CLI 会话中，即使你正在查看主线程，approval requests 也可能从非活动 agent threads 显示出来。审批浮层会显示来源 thread label，你可以在批准、拒绝或回答该 request 之前按 `o` 打开该线程。

在非交互式流程中，或任何无法显示新审批的运行中，需要新审批的操作会失败，Codex 会将错误返回给 parent workflow。

Codex 在生成 child 时也会重新应用 parent turn 的实时运行时覆盖项。这包括你在会话中交互式设置的沙箱和审批选择，例如 `/permissions` 变更或 `--yolo`，即使所选 custom agent file 设置了不同默认值。

你也可以为单个 [custom agents](#custom-agents) 覆盖沙箱配置，例如明确标记某个 agent 以只读模式工作。

#### 自定义智能体

Codex 随附内置 agents：

- `default`：通用 fallback agent。
- `worker`：面向执行的 agent，用于实现和修复。
- `explorer`：偏重读取的代码库探索 agent。

要定义自己的 custom agents，请在 `~/.codex/agents/` 下添加独立 TOML 文件作为个人 agents，或在 `.codex/agents/` 下添加项目作用域 agents。

每个文件定义一个 custom agent。Codex 会将这些文件作为 spawned sessions 的配置层加载，因此 custom agents 可以覆盖与普通 Codex session config 相同的设置。这可能比专用 agent manifest 更重，且格式可能会随着创作和分享能力的成熟而演进。

每个独立 custom agent file 都必须定义：

- `name`
- `description`
- `developer_instructions`

如果省略 `nickname_candidates`、`model`、`model_reasoning_effort`、`sandbox_mode`、`mcp_servers` 和 `skills.config` 等可选字段，它们会从 parent session 继承。

#### 全局设置

全局 subagent 设置仍位于你的 [configuration](19-config-basics.md#configuration-precedence) 中的 `[agents]` 下。

| 字段                             | 类型   | 必填     | 用途                                                       |
| -------------------------------- | ------ | :------: | ---------------------------------------------------------- |
| `agents.max_threads`             | number |    No    | 并发打开的 agent thread 上限。                          |
| `agents.max_depth`               | number |    No    | Spawned agent 嵌套深度（root session 从 0 开始）。    |
| `agents.job_max_runtime_seconds` | number |    No    | `spawn_agents_on_csv` jobs 的每个 worker 默认 timeout。 |

**说明：**

- 如果未设置，`agents.max_threads` 默认为 `6`。
- `agents.max_depth` 默认为 `1`，这允许 direct child agent 生成，但会阻止更深层嵌套。除非你明确需要递归委派，否则保持默认值。提高该值可能会把宽泛委派说明变成重复扇出，从而增加 token 使用量、延迟和本地资源消耗。`agents.max_threads` 仍会限制并发打开的 threads，但不会消除更深递归带来的成本和可预测性风险。
- `agents.job_max_runtime_seconds` 是可选的。未设置时，`spawn_agents_on_csv` 会回退到其每次调用的默认 timeout，即每个 worker 1800 秒。
- 如果 custom agent name 与 `explorer` 等内置 agent 匹配，你的 custom agent 优先。

#### 自定义智能体文件 schema

| 字段                     | 类型     | 必填     | 用途                                                            |
| ------------------------ | -------- | :------: | --------------------------------------------------------------- |
| `name`                   | string   |   Yes    | Codex 在生成或引用该 agent 时使用的 agent name。 |
| `description`            | string   |   Yes    | 面向人的指导，说明 Codex 何时应使用该 agent。     |
| `developer_instructions` | string   |   Yes    | 定义 agent 行为的核心说明。             |
| `nickname_candidates`    | string[] |    No    | 用于 spawned agents 的可选显示昵称池。          |

你还可以在 custom agent file 中包含其他受支持的 `config.toml` keys，例如 `model`、`model_reasoning_effort`、`sandbox_mode`、`mcp_servers` 和 `skills.config`。

Codex 通过 `name` 字段识别 custom agent。让文件名与 agent name 匹配是最简单的约定，但 `name` 字段才是真实来源。

#### 显示昵称

当你希望 Codex 为 spawned agents 分配更易读的显示名称时，使用 `nickname_candidates`。当你运行同一个 custom agent 的许多实例，并希望 UI 显示不同 labels，而不是重复相同 agent name 时，这尤其有用。

Nicknames 仅用于展示。Codex 仍会通过其 `name` 识别和生成 agent。

Nickname candidates 必须是非空的唯一名称列表。每个 nickname 可以使用 ASCII 字母、数字、空格、连字符和下划线。

示例：

```toml
name = "reviewer"
description = "PR reviewer focused on correctness, security, and missing tests."
developer_instructions = """
Review code like an owner.
Prioritize correctness, security, behavior regressions, and missing test coverage.
"""
nickname_candidates = ["Atlas", "Delta", "Echo"]
```

实际使用中，Codex app 和 CLI 可以在显示 agent activity 的位置显示 nicknames，而底层 agent type 仍保持为 `reviewer`。

#### 自定义智能体示例

最好的 custom agents 范围明确且有主张。为每个 agent 赋予清晰的职责、与职责匹配的 tool surface，以及能防止它偏离到相邻工作的说明。
