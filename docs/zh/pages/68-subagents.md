### 子智能体

Source: [Subagents](https://developers.openai.com/codex/concepts/subagents.md)

Codex 可以通过并行生成专门代理来运行子代理工作流，使
它们可以并发探索、处理或分析工作。

本页解释核心概念和权衡。有关设置、代理配置和示例，请参阅 [Subagents](https://developers.openai.com/codex/subagents)。

#### 为什么子代理工作流有帮助

即使有很大的上下文窗口，模型也有局限。如果你把主对话（你在其中定义要求、约束和决策的地方）塞满嘈杂的中间输出，例如探索笔记、测试日志、堆栈跟踪和命令输出，会话可能会随着时间推移变得不那么可靠。

这通常被描述为：

- **Context pollution**：有用信息被嘈杂的中间输出淹没。
- **Context rot**：随着对话充满较不相关的细节，性能下降。

背景信息请参阅 Chroma 关于 [context rot](https://research.trychroma.com/context-rot) 的文章。

子代理工作流通过将噪声工作移出主线程来提供帮助：

- 让 **主代理** 专注于要求、决策和最终输出。
- 并行运行专门的 **子代理**，用于探索、测试或日志分析。
- 从子代理返回 **摘要**，而不是原始中间输出。

当工作可以独立并行运行时，它们也可以节省时间，并且
通过将较大型任务拆成有界
片段，使其更易处理。例如，Codex 可以将数百万 token
文档的分析拆成较小问题，并把提炼后的要点返回给主
线程。

作为起点，请将并行代理用于以读取为主的任务，例如
探索、测试、分诊和摘要。对于并行的
写入密集型工作流要更谨慎，因为代理同时编辑代码可能产生
冲突并增加协调开销。

#### 核心术语

Codex 在子代理工作流中使用几个相关术语：

- **Subagent workflow**：Codex 运行并行代理并合并其结果的工作流。
- **Subagent**：Codex 启动来处理特定任务的委派代理。
- **Agent thread**：某个代理的 CLI 线程，你可以用 `/agent` 检查并在它们之间切换。

#### 触发子代理工作流

Codex 不会自动生成 subagents，并且只有当你
明确要求 subagents 或并行代理工作时，它才应使用 subagents。

实践中，手动触发意味着使用直接指令，例如
"spawn two agents,"、"delegate this work in parallel," 或 "use one agent per
point." 子代理工作流会比可比的单代理运行消耗更多 token，
因为每个子代理都会执行自己的模型和工具工作。

一个好的子代理提示应说明如何划分工作、Codex
是否应等待所有代理后再继续，以及应返回什么摘要或输出。

```text
Review this branch with parallel subagents. Spawn one subagent for security risks, one for test gaps, and one for maintainability. Wait for all three, then summarize the findings by category with file references.
```

#### 选择模型和推理

不同代理需要不同的模型和推理设置。

如果你没有固定 model 或 `model_reasoning_effort`，Codex 可以选择一种
在智能、速度和价格之间取得平衡的设置。它可能偏向使用 `gpt-5.4-mini` 进行快速扫描，或使用更高推理强度的 `gpt-5.5` 配置处理更高要求的推理。当你想要更精细控制时，请在提示中引导该选择，或直接在代理文件中设置 `model` 和 `model_reasoning_effort`。

对于 Codex 中的大多数任务，请从
`gpt-5.5` 开始。需要
更快、成本更低的轻量子代理工作时，使用
`gpt-5.4-mini`。如果你拥有 ChatGPT Pro
并希望近乎即时的纯文本迭代，`gpt-5.3-codex-spark` 仍
以研究预览形式可用。

#### 模型选择

- **`gpt-5.5`**：高要求代理从这里开始。它最适合模糊、多步骤的工作，这类工作需要规划、工具使用、验证，并在更大上下文中贯彻到底。
- **`gpt-5.4`**：当工作流固定到 GPT-5.4 时使用。它结合了强编码、推理、工具使用和更广泛工作流能力。
- **`gpt-5.4-mini`**：用于相比深度更重视速度和效率的代理，例如探索、以读取为主的扫描、大文件审查或处理支持文档。它非常适合作为并行工作者，将提炼后的结果返回给主代理。
- **`gpt-5.3-codex-spark`**：如果你有 ChatGPT Pro，当延迟比更广能力更重要时，可以使用这个研究预览模型进行近乎即时的纯文本迭代。

#### 推理强度（`model_reasoning_effort`）

- **`high`**：当代理需要追踪复杂逻辑、检查假设或处理边界情况时使用（例如审查代理或安全聚焦代理）。
- **`medium`**：大多数代理的平衡默认值。
- **`low`**：当任务直接且速度最重要时使用。

更高推理强度会增加响应时间和 token 使用量，但它可以提升复杂工作的质量。详情请参阅 [Models](https://developers.openai.com/codex/models)、[Config basics](https://developers.openai.com/codex/config-basic) 和 [Configuration Reference](https://developers.openai.com/codex/config-reference)。
