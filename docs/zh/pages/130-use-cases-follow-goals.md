### 跟随目标

Source: [Follow a goal](https://developers.openai.com/codex/use-cases/follow-goals.md)

为 Codex 提供一个可持久执行的长时间工作目标。

#### 概览

当任务需要 Codex 跨多个回合持续工作，直到达到可验证停止条件时，使用 `/goal`。

适合：

- 有清晰成功条件和验证循环的长时间编码工作。
- 代码迁移、大型重构、部署重试循环、实验、游戏和 side projects，其中 Codex 可以持续推进有边界的进度。
- 需要用明确成功标准运行长实验的团队。

#### 起始提示

**设置长时间目标**

```text
/goal Complete [objective] without stopping until [verifiable end state].
```

#### 相关链接

- [CLI 斜杠命令中的 `/goal`](39-slash-commands-in-codex-cli.md#set-a-goal-with-goal)
- [Codex workflows](06-example-workflows.md)
- [运行代码迁移](110-use-cases-code-migrations.md)
- [迭代处理困难问题](139-use-cases-iterate-on-difficult-problems.md)

## 介绍

当你希望 Codex 围绕一个持久目标持续工作，而不是在一个普通回合后停止时，使用 `/goal`。它适用于有清晰目标、验证循环，并且 Codex 有足够空间在不需要你每一步引导的情况下推进的工作。使用 `/goal` 时，Codex 可以独立工作多个小时而不需要你的输入。

用 `/goal <objective>` 设置目标，用 `/goal` 检查当前目标，并在需要控制运行时使用 `/goal pause`、`/goal resume` 或 `/goal clear`。

如果 slash command 列表中没有 `/goal`，请在 `config.toml` 中启用 `features.goals`：

```toml
[features]
goals = true
```

你也可以从 CLI 运行 `codex features enable goals`，或让 Codex 运行它。

## 选择合适的工作

一个好的 goal 应该比一条提示更大，但小于开放式 backlog。它应定义 Codex 要达成什么、不应改变什么、如何验证进度，以及何时停止。

这很适合：

- 目标技术栈、parity checks 和约束都清晰的代码迁移。
- Codex 可以在每个 checkpoint 后运行测试的大型重构。
- Codex 可以持续改进可运行 artifact 的实验、游戏或原型。

避免将 goal 用于一组松散且彼此无关的工作。

## 设置循环

1. 命名一个目标和一个停止条件。
2. 指向 Codex 必须先阅读的文件、文档、issue、日志或计划。
3. 定义能证明进度的命令或 artifact。
4. 告诉 Codex 按 checkpoint 工作，并保持简短进度日志。
5. 在运行时使用 `/goal` 查看状态。
6. 当运行完成、受阻或改变方向时，暂停、恢复或清除 goal。

关键在于契约。Codex 开始前应知道“完成”意味着什么。如果 goal 是迁移，“完成”可能意味着新路径通过 contract tests，且 legacy path 仍有 rollback。如果 goal 是游戏或原型，“完成”可能意味着应用能构建、启动，并匹配输入参考或预期行为。

让 Codex 帮忙：先讨论你想构建什么，然后让它直接设置 goal 并开始工作。

## 让 Codex 独立工作

在 goal 期间，要求简洁的进度报告，让运行更可信。有用的状态更新应说明当前 checkpoint、已验证内容、剩余事项，以及 Codex 是否受阻。
如果状态变得含糊，请收紧 goal，而不是添加更多一次性指令。准确告诉 Codex 下一个 checkpoint 是什么、哪个命令能证明它，以及什么情况应触发暂停。

当 Codex 跟随 goal 时，它可以独立工作许多小时，而你不必持续检查。它会在确信已达到停止条件时停止运行，因此你可以把 `/goal` 视为无需监控的后台任务。

## 示例目标

### 迁移

无论你是把游戏迁移到新技术栈、把移动应用迁移到新平台，还是把代码库迁移到新框架，都可以使用 `/goal` 让 Codex 执行迁移：

### 原型创建

无论你是从零创建新应用、新游戏还是新功能，都可以使用 `/goal` 让 Codex 完成一个打磨好的第一版。你可以用 PLAN.md 文件指导第一版创建，精确描述想构建的内容。

### 提示优化

当你有 eval suite 时，可以使用 `/goal` 根据 eval 结果优化 prompts。Codex 可以检查失败、更新 prompt、重新运行 evals，并持续迭代，直到分数提升或达到你的停止条件。
