### 记忆

Source: [Memories](https://developers.openai.com/codex/memories.md)

Memories 默认关闭，并且在发布时不适用于欧洲经济区、英国或瑞士。可在 Codex 设置中启用，或在 `~/.codex/config.toml` 的 `[features]` 表中设置 `memories = true`。

Memories 让 Codex 能把早期线程中的有用上下文带入未来工作。启用 memories 后，Codex 可以记住稳定偏好、重复工作流、技术栈、项目约定和已知陷阱，这样你就不必在每个线程中重复相同上下文。

请将必需的团队指导放在 `AGENTS.md` 或已检入的文档中。把 memories 视为有帮助的本地记忆层，而不是必须始终适用的规则的唯一来源。

[Chronicle](https://developers.openai.com/codex/memories/chronicle) 可以帮助 Codex 从你的屏幕恢复最近的工作上下文，以逐步构建记忆。

#### 启用记忆

在 Codex app 中，在设置里启用 Memories。

对于基于配置的设置，将功能标志添加到 `config.toml`：

```toml
[features]
memories = true
```

有关 Codex 存储用户级配置的位置以及 Codex 如何加载 `~/.codex/config.toml`，请参阅 [配置基础](https://developers.openai.com/codex/config-basic)。

#### 记忆如何工作

启用 memories 后，Codex 可以把符合条件的既往线程中的有用上下文转为本地 memory 文件。Codex 会跳过活动会话或短生命周期会话，从生成的 memory 字段中遮盖 secrets，并在后台更新 memories，而不是在每个线程结束后立即更新。

线程结束时，memories 可能不会立刻更新。Codex 会等到线程空闲足够长的时间，以避免汇总仍在进行中的工作。

当你的 Codex rate-limit 剩余百分比低于配置阈值时，记忆生成也可能跳过一次后台处理，这样 Codex 在你接近限制时不会消耗额度。

#### 记忆存储

Codex 会将 memories 存储在你的 Codex 主目录下。默认情况下是 `~/.codex`。有关 Codex 如何使用 `CODEX_HOME`，请参阅 [配置和状态位置](https://developers.openai.com/codex/config-advanced#config-and-state-locations)。

主要 memory 文件位于 `~/.codex/memories/` 下，包含来自先前线程的摘要、持久条目、最近输入和支持证据。

请将这些文件视为生成的状态。排查问题或分享你的 Codex home directory 前可以检查它们，但不要依赖手动编辑这些文件作为主要控制界面。

#### 按线程控制记忆

在 Codex app 和 Codex TUI 中，使用 `/memories` 控制当前线程的 memory 行为。线程级选择允许你决定当前线程是否可以使用已有 memories，以及 Codex 是否可以使用该线程生成未来 memories。

线程级选择不会更改你的全局 memory 设置。

#### 配置

在 Codex app 设置中启用 memories，或在 `config.toml` 的 `[features]` 部分设置 `memories = true`。

有关配置文件位置和 memory 相关设置的完整列表，请参阅 [配置参考](https://developers.openai.com/codex/config-reference)。

常见的 memory 专用设置包括：

- `memories.generate_memories`：控制新创建的线程是否可以作为记忆生成输入存储。
- `memories.use_memories`：控制 Codex 是否将已有 memories 注入未来会话。
- `memories.disable_on_external_context`：当为 `true` 时，会将使用过 MCP tool calls、web search 或 tool search 等外部上下文的线程排除在记忆生成之外。旧的 `memories.no_memories_if_mcp_or_web_search` key 仍可作为别名接受。
- `memories.min_rate_limit_remaining_percent`：控制记忆生成启动前所需的最低 Codex rate-limit 剩余百分比。
- `memories.extract_model`：覆盖用于单线程 memory 提取的模型。
- `memories.consolidation_model`：覆盖用于全局记忆整合的模型。

#### 审查记忆

不要在 memories 中存储 secrets。Codex 会从生成的 memory 字段中遮盖 secrets，但在分享你的 Codex 主目录或生成的 memory artifacts 前，你仍应审查 memory 文件。
