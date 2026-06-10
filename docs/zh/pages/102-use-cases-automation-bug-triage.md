### 自动化 bug 分诊

Source: [Automate bug triage](https://developers.openai.com/codex/use-cases/automation-bug-triage.md)

把每日 bug 报告转成优先级列表，然后自动化这次扫描。

#### 概览

让 Codex 检查近期 alerts、issues、失败 checks、日志和聊天报告，在一个 thread 中调优列表，然后按计划运行这次扫描。

适合：

- 跨 Sentry alerts、Slack threads、Linear issues、GitHub issues、失败 PR checks、支持 tickets 或日志跟踪 bug 的团队。
- 想先在一个 Codex thread 中手动运行，再调度为自动化的分诊工作流。

相关 skill：

- `github`：当 GitHub 是 bug intake 的一部分时，读取 issues、pull requests、comments、review threads 和失败 checks。
- `$sentry`：当 alerts 是扫描的一部分时，检查生产错误、stack traces、受影响版本和 event context。
- `slack`：读取队友报告 bug 的 channels 或 threads，并为团队 channel 准备草稿摘要。
- `linear`：读取 bug queues、查找现有 issues、起草更新，或在分诊 pass 后准备关联的 follow-up tickets。

#### 起始提示

```text
为 [repo/service/team] 运行一次 bug 分诊扫描，覆盖过去 [time window]。

使用这些 plugins：[@Sentry / @Slack / @Linear / @GitHub / none]

输入来源：
- Sentry：[project / alert link / none]
- Slack：[channel / thread links / none]
- Linear：[team / project / view / issue query / none]
- GitHub：[repo / issue query / PR checks / none]
- 其它：[logs / support tickets / deploy link / dashboard / attached file / none]

输出格式：
首先，说明任何无法访问的输入来源。
然后返回按 P0 到 P3 排序的 bug 优先级列表。
如果没有找到 bug，请说：No qualifying bugs found.

对于每个 bug，请包含：
- Priority：P0、P1、P2 或 P3
- Title
- Evidence（链接或简短引用）
- Recommended next action

规则：
- 不要发布、创建、指派、打标签、关闭、重跑或编辑任何内容。
- 把重复报告归并到同一个 bug 下。
- 将观察到的证据与猜测分开。
```

#### 相关链接

- [Codex automations](24-automations.md)
- [Codex plugins](78-plugins.md)
- [Codex MCP](53-model-context-protocol.md)
- [Use Codex in Linear](55-use-codex-in-linear.md)

#### 技术栈建议

| 需求 | 推荐默认 | 原因 |
| --- | --- | --- |
| bug 上下文聚集的位置 | Sentry alerts、Slack channels、Linear views、GitHub issues、PR checks、support queues、on-call notes、logs、dashboards 和 deploy notes | 点明 Codex 应扫描的确切 queues、channels、views、repos、alert links、dashboards 和 files。 |
| Codex 如何读取它 | 用于 Slack、Linear、GitHub 和 Sentry 的 [Plugins](78-plugins.md)；connectors；[MCP servers](53-model-context-protocol.md)；repo CLIs；links；exports；attachments；以及粘贴的 logs | 当已有集成时安装它。对于 Codex 还不能读取的内部来源，构建或配置一个小型 MCP server、CLI、export 或 dashboard link。 |

#### 如何使用

要求 Codex 检查 bug 已经出现的地方：Sentry alerts、Linear issues、GitHub issues、PR checks、deploy logs、support tickets 和 Slack threads。从一次手动扫描开始，在 thread 中调优报告，然后按计划运行。

用一个 Codex thread 完成整个分诊循环：

1. 运行一次按需扫描，获得草稿列表。
2. 审查列表，并在同一个 thread 中给出反馈。
3. 把同一个 thread 转成自动化。
4. 可选：当你对报告有信心后，让 Codex 起草 Linear issues、Slack updates、GitHub comments 或交接备注。

开始前，安装 Codex 需要的 [plugins](78-plugins.md)，例如 Sentry、Slack、Linear 或 GitHub。在起始提示中，用真实的 `@` plugin chips 替换括号中的 plugin 列表。然后用要搜索的确切位置替换每个括号中的来源：Sentry project 或 alert URL、Slack channel 或 thread、Linear team、view 或 query、GitHub repo、issue query 或 PR check、deploy link、log file、support queue 或 dashboard。

#### 阶段 1：运行扫描

当本地上下文有帮助时，从拥有这些 bug 的 repo 启动 Codex：测试、仓库工具、构建检查或 CI 失败。只要 bug 来源可以通过 plugins、connectors、MCP servers、links、exports、粘贴 logs 或 attachments 获得，你也可以从任何 repo 运行扫描。

先运行上面的起始提示。只保留属于本次扫描的 plugins 和 sources。

例如，填好的提示可以点明你希望纳入扫描的 plugins，以及确切 queues、channels 或 repos。

#### 阶段 2：让报告有用

自动化之前，先确保报告足够有用，值得每天阅读。

有用的第一次运行应包含：

- 从 P0 到 P3 排序的高信号 bug。
- 重复报告被归并到同一个 bug 下。
- 每个 bug 都有链接证据或简短引用。
- 猜测与观察到的事实分开。
- 每个 bug 都有简短的建议下一步。

在自动化之前，在同一个 thread 中调优报告。你可以要求 Codex：

- 排序列表前再检查一个来源。
- 去掉团队已知的嘈杂 alerts。
- 只返回 P0 和 P1 bug。
- 当 Slack reports、Sentry alerts 和 GitHub failures 指向同一个 bug 时，把它们合并。
- 为每个 bug 展示单个最佳链接。
- 添加足够证据，让其他人可以复现或路由该问题。

#### 阶段 3：自动化它

当按需报告有用后，留在同一个 thread 中，把它转成自动化。Codex 可以使用你在 thread 中细化的内容来编写重复运行的自动化提示。

**创建自动化**

#### 阶段 4：路由 follow-up

当计划报告有用后，决定接下来的工作应流向哪里。Codex 可以为团队 channel 起草 Slack update，为你想跟踪的 bugs 编写 Linear issues，为失败 PR 编写 GitHub comments，或为 on-call 人员产出交接。
