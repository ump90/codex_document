### 排定 Slack action items 优先级

Source: [Prioritize Slack action items](https://developers.openai.com/codex/use-cases/slack-action-triage.md)

把 Slack threads 和 DMs 转成按优先级排序的下一步队列。

#### 概览

使用 Codex 搭配 Slack 和工作发生处的工具，找出直接请求、隐含 follow-ups、已解决事项，以及在起草 replies 或 handoffs 前最高影响的 next actions。

适合：

- 通过 Slack 接收工作，并需要 Codex 把活跃请求与已经处理过的聊天分开的人员。
- 上下文分散在 DMs、channels 和 threads 中的 launch、community、support、product 和 operations workstreams。
- 希望在起草 replies、handoffs、docs changes 或 follow-up tasks 前先得到 ranked action queue 的团队。

相关 skill：

- `slack`：搜索 DMs、channels、thread replies、mentions 和 shared context，再决定哪些仍需要关注。
- `gmail`：当 Slack thread 提到 outreach、intro 或 sent follow-up 时，交叉检查 email。
- `google-drive`：当 Slack thread 依赖 artifact 时，读取链接 docs、decks、sheets 或 source material。
- `google-calendar`：当 thread 依赖 meeting、launch、webinar 或 deadline 时，检查 event timing。

#### 起始提示

**找出 Slack 中需要关注的事项**

```text
你能检查 @slack 中 [time window] 以来发给我的、关于 [workstream] 的消息，并返回一个 ranked action queue 吗？

查看 DMs、group DMs、channel mentions 和 threads。

对每个 item，包含：
- source link 或 thread
- 对方在请求什么
- 它是否需要我回复、需要某个人或 lead、需要 docs 或 code change，还是只需要一个 decision
- 它为什么重要
- 推荐的 next step

在把任何事项称为 unresolved 之前，阅读最新 thread replies，并跳过已经处理过的 items。

不要直接发布消息，只提供供我审查的草稿。
```

建议使用低推理强度。

#### 找出藏在 Slack 里的工作

Slack 经常是请求开始的地方，但完整上下文不一定在那里。队友可能在 DM 里请求回复，在 thread 中澄清真正的 action，在 channel 中链接 doc，然后之后又解决了问题，却没有再次提到你。

当你希望 Codex 读取 Slack 上下文、检查请求是否仍然活跃，并返回真正需要你关注的少数 items 时，可以使用这个工作流。目标是得到 ranked action queue：哪些需要 reply、decision、contact person、doc update 或 handoff。

#### 运行 triage pass

1. 给 Codex 一个 time window、workstream、person、channel 或 topic。
2. 要求它搜索 DMs、group DMs、channel mentions 和相关 thread replies。
3. 让 Codex 在把 item 称为 unresolved 前，先读取最新 thread tail。
4. 要求按 urgency 和 impact 排序的 ranked queue。
5. 要求 Codex 起草 reply、handoff 或 follow-up task。

试用并调整流程以匹配你的需求后，你可以要求 Codex 按计划做同样的事，把它变成 [thread automation](24-automations.md#thread-automations)。

#### 要求合适的输出

有用的 triage result 应解释每个 item 为什么仍然活跃。它也应该跳过 thread 后面已经有人回答过的旧请求。

你应该看到类似这样的内容：

<p>
    <strong>最高优先级 action item：</strong>Priya 要的是具体 customer examples，而不只是更多想法。
  </p>
  <p>
    <strong>为什么重要：</strong>launch update 需要团队本周可以联系的真实人员。
  </p>
  <p>
    <strong>证据：</strong>原始 channel message 请求 use cases，但 thread 后面说“please DM me if you have leads.”
  </p>
  <p>
    <strong>下一步：</strong>回复两个具名 leads，或者说明如果更有用，你自己也可以作为 example。
  </p>

好输出会明确区分：idea 不同于 lead，live ask 不同于 FYI，而你已经回答过的请求不应该继续留在队列里。

如果噪声太多或 actionable items 太少，请调整 prompt；必要时，可以指定你希望 Codex 重点关注的 slack channels。

#### 起草 follow-up

当队列正确后，让 action 留在同一线程中。要求 Codex 基于它已经收集的证据起草 reply 或 handoff：

#### 相关链接

- [Codex plugins](78-plugins.md)
- [Use Codex in Slack](56-use-codex-in-slack.md)
- [Codex automations](24-automations.md)
