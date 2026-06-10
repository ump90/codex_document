### 从 Slack 启动编码任务

Source: [Kick off coding tasks from Slack](https://developers.openai.com/codex/use-cases/slack-coding-tasks.md)

把 Slack threads 转成有范围的 cloud tasks。

#### 概览

在 Slack 中提到 `@Codex`，即可启动一个绑定到正确 repo 和 environment 的任务，然后回到 thread 或 Codex cloud 中审查结果。

适合：

- 从 Slack thread 开始、且已经有足够上下文可执行的异步 handoffs。
- 希望快速 issue triage、bug fixes 或 scoped implementation work，同时减少 context switching 的团队。

#### 起始提示

**从 thread 启动任务**

```text
@Codex analyze the issue mentioned in this thread and implement a fix in <name of your environment>.
```

建议使用 cloud model。

#### 如何使用

1. 安装 Slack app，连接正确的 repositories 和 environments，并把 `@Codex` 添加到 channel。
2. 在 thread 中提到 `@Codex`，并给出清晰请求、约束和你想要的结果。
3. 打开任务链接，审查结果；如果任务需要另一轮处理，可以在 Slack 中继续 follow-up。

你可以在 [dedicated guide](56-use-codex-in-slack.md) 中进一步了解如何在 Slack 中使用 Codex。

#### 提示

- 如果 thread 中还没有足够上下文或 suggested fix，请在 prompt 中加入一些指导。
- 通过在 prompt 中提到项目或 environment 名称，确保 repo 和 environment mapping 正确。
- 控制请求范围，让 Codex 不需要第二轮 planning loop 也能完成。
- 如果项目是大型代码库，请通过说明与任务相关的 files 或 folders 来引导 Codex。

#### 相关链接

- [Use Codex in Slack](56-use-codex-in-slack.md)
- [Codex cloud environments](25-cloud-environments.md)
