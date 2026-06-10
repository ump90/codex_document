### 重构你的代码库

Source: [Refactor your codebase](https://developers.openai.com/codex/use-cases/refactor-your-codebase.md)

在不改变行为的前提下删除 dead code，并现代化 legacy patterns。

#### 概览

使用 Codex 以小而可审查的 pass 删除 dead code、理清大文件、合并重复逻辑，并现代化陈旧 patterns。

适合：

- 存在 dead code、oversized modules、duplicated logic 或 stale abstractions，导致日常改动成本很高的代码库。
- 需要在原地现代化代码，而不是把工作变成 framework 或 stack migration 的团队。

相关 skill：

- `$security-best-practices`：在合并 modernization pass 前，审查 security-sensitive cleanup、dependency changes、auth flows 和 exposed surfaces。
- `$skill-creator`：把已验证的 modernization pattern、review checklist 或 parity workflow 转成可复用 repo 或 team skill。

#### 起始提示

**小步现代化**

```text
现代化并重构这个代码库。

要求：
- 除非我明确要求功能变更，否则保持行为不变。
- 先识别正在拖慢改动的 dead code、duplicated paths、oversized modules、stale abstractions 和 legacy patterns。
- 对每个 proposed pass，说明当前行为、结构改进，以及应该证明行为保持稳定的 validation check。
- 把工作拆成小而可审查的 refactor passes，例如删除 dead code、简化 control flow、提取 helpers，或用 repo 当前 conventions 替换过时 patterns。
- 除非 refactor 必须，否则保持 public APIs 稳定。
- 指出任何 framework migration、dependency upgrade、API change 或 architecture move，它们应拆成单独 migration task。
- 如果工作范围很广，提出我们在 implementation 前应创建的 docs、specs 和 parity checks。

请提出执行计划。
```

#### 简介

当代码库积累了 unused code、duplicated logic、stale abstractions、大文件或 legacy patterns，让每次改动都变得比应有成本更高时，你应该考虑通过 refactor 降低 engineering debt。重构是改进现有系统形态，而不是把它变成 stack migration。

Codex 在这里很有用，因为它可以先绘制混乱区域，然后用小而可审查的 pass 完成清理：删除 unused paths、理清 large modules、合并 duplicate paths、现代化旧 framework patterns，并围绕每个 pass 收紧验证。

目标是在原地改进当前代码库：

1. 删除不再需要的 unused code、stale helpers、old flags 和 compatibility shims。
2. 通过提取 helpers、拆分 components 或把 side effects 移到更清晰边界来缩小 noisy modules。
3. 用 repo 当前 conventions 替换 legacy patterns：更新的 framework primitives、更清晰 types、更简单 state flow 或 standard library utilities。
4. 在让下一次改动更便宜的同时，保持 public behavior 稳定。

#### 如何使用

1. 编辑前先让 Codex map 该区域：noisy modules、duplicated logic、unused code、tests、public contracts，以及 repo 已经不再需要的旧 patterns。
2. 一次选择一个 cleanup theme：删除 unused code、简化 control flow、现代化 outdated pattern，或把大文件拆成更小、ownership 更清晰的部分。
3. 在 Codex patch 文件前，让它说明当前行为、想做的结构改进，以及应该证明行为保持稳定的最小检查。
4. 每个 pass 后审查并运行最小有用检查，而不是把整个 cleanup 批量放进一个 diff。
5. 除非完成 cleanup 必须，否则把 stack changes、dependency migrations 和 architecture moves 作为单独任务处理。

你可以使用 Plan mode 在开始工作前为 refactor 创建计划。

#### 利用 ExecPlans

[code modernization cookbook](https://developers.openai.com/cookbook/examples/codex/code_modernization) 介绍了 ExecPlans：这些文档让 Codex 保持 cleanup 全局视图，说明目标终态，并在每个 pass 后记录验证。

当 refactor 跨越多个 module 或需要多个 session 时，它们很有用。用它们记录 deletions、pattern updates、必须保持稳定的 contracts，以及仍然 deferred 的事项。

#### 为可重复 patterns 使用 skills

[Skills](48-agent-skills.md) 适用于同样 cleanup rules 会在多个 repos、services 或 teams 中重复出现的情况。在可用时使用 framework-specific skills，为高风险 cleanup 添加 security 和 CI skills，并在你已经有 unused-code removal、module extraction 或 legacy-pattern modernization 的成熟 checklist 后创建 team skill。

如果你最终在多个代码库中执行同一种 modernization pass，Codex 可以帮助把第一次成功 pass 转成可复用 skill。

#### 相关链接

- [使用 Codex 现代化代码库](https://developers.openai.com/cookbook/examples/codex/code_modernization)
