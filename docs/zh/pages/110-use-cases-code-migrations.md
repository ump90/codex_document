### 运行代码迁移

Source: [Run code migrations](https://developers.openai.com/codex/use-cases/code-migrations.md)

在受控检查点中迁移遗留技术栈。

#### 概览

使用 Codex 把遗留系统映射到新技术栈，按 milestones 落地迁移，并在每次过渡前验证 parity。

适合：

- 从遗留到现代技术栈的迁移，其中 frameworks、runtimes、build systems 或平台约定需要改变。
- 需要 compatibility layers、分阶段过渡，并在每个迁移检查点显式验证的团队。

相关 skill：

- `$security-best-practices`：在合并前检查有风险的迁移、依赖变更和暴露 surface。
- `$gh-fix-ci`：在每个迁移 milestone 后处理失败 CI，而不是把清理工作留到最后。
- `$aspnet-core`：当迁移涉及 ASP.NET Core app models、`Program.cs`、middleware、testing、performance 或 version upgrades 时，使用框架特定指南。

#### 起始提示

```text
把这个代码库从 [legacy stack or system] 迁移到 [target stack or system]。

要求：
- 先盘点遗留假设：routing、data models、auth、configuration、build tooling、tests、deployment 和 external contracts。
- 把旧技术栈映射到新技术栈，并指出没有直接等价物的内容。
- 提出增量迁移计划，包含 compatibility layers 或 checkpoints，而不是一次性大重写。
- 除非迁移明确需要用户可见变更，否则保持行为不变。
- 按 milestones 工作，并在每个 milestone 后运行 lint、type-check 和 focused tests。
- 在过渡完成前，让 rollback 或 fallback options 保持可见。
- 如果验证失败，先修复再继续。
- 先映射 migration surface，并提出 checkpoint plan。
```

#### 相关链接

- [使用 Codex 现代化代码库](https://developers.openai.com/cookbook/examples/codex/code_modernization)
- [跟进目标](130-use-cases-follow-goals.md)
- [Codex app 中的 worktrees](42-worktrees.md)

#### 引言

当你从一个技术栈迁移到另一个技术栈时，可以利用 Codex 映射并执行受控迁移：routing、data models、configuration、auth、background jobs、build tooling、deployment、tests，甚至语言和框架约定本身。

Codex 在这里很有用，因为它可以盘点遗留系统、把旧概念映射到新概念，并在检查点中落地变更，而不是做一次巨大的重写。当你正在摆脱遗留框架、迁移到新 runtime，或在产品仍需继续工作的同时逐步替换一个技术栈时，这一点很重要。

#### 如何使用

1. 先盘点迁移 surface：legacy packages、framework conventions、routing、data access、auth、configuration、build tooling、tests、deployment assumptions，以及任何迁移后必须保留的 external contracts。
2. 要求 Codex 把遗留概念映射到目标技术栈，并指出没有直接匹配的内容。
3. 选择增量策略：compatibility layer、逐模块移植、branch-by-abstraction，或围绕一次一个边界进行 strangler-style replacement。
4. 在迁移本身强制可见变更前保持行为稳定，并明确点名这些例外。
5. 每个 milestone 后，运行能够证明 parity 的最小验证：lint、type-check、focused tests、contract tests、smoke tests，或针对 legacy path 的 side-by-side check。
6. 每个 checkpoint 后审查 diff 和剩余过渡风险，而不是等到完整重写结束。

#### 利用 ExecPlans

在我们的 [code modernization cookbook](https://developers.openai.com/cookbook/examples/codex/code_modernization) 中，我们介绍了 ExecPlans：这类文档让 Codex 保持对清理工作的整体视图、写明预期最终状态，并在每次 pass 后记录验证结果。

当你要求 Codex 运行复杂迁移时，请让它为系统的每个部分创建一个 ExecPlan，以确保每个决策和技术栈选择都被记录，并可在之后审查。

#### 结合 goal 使用

对于长时间运行的迁移 slice，使用 [goal](130-use-cases-follow-goals.md) 引导 Codex 完成工作。用清晰的最终状态、parity checks、rollback expectations 和停止条件来设置 goal。
