### 设置一个队友

Source: [Set up a teammate](https://developers.openai.com/codex/use-cases/proactive-teammate.md)

给 Codex 一个持久的工作视图，让它能注意到变化。

#### 概览

连接工作发生的工具，教会一个线程什么重要，然后添加 automation，让 Codex 可以发现变化的 docs、被埋没的请求、受阻的 handoffs，以及需要你判断的决定。

适合：

- 上下文分散在 Slack、Gmail、calendar、docs、trackers、code 和 notes 中的角色。
- 理解活跃工作、周期性决定、collaborators，并从噪声中找到信号。
- 需要升级值得关注事项的团队。

相关 skill：

- `slack`：查找围绕请求、owner changes、blockers 和 decisions 的 Slack 上下文。
- `gmail`：查找值得回复的 threads，并与 workstream 的其它部分交叉检查。
- `google-calendar`：利用当天会议判断哪些 updates 现在重要，哪些可以等待。
- `notion`：读取定义 workstream 的 project notes、trackers 或 decision logs。

#### 起始提示

**检查哪些事情需要关注**

```text
你能检查 @slack、@gmail、@google-calendar 和 @notion，并告诉我哪些事情需要我关注吗？

寻找任何重要或意外、我可能错过的事情。
```

建议使用低推理强度。

#### 技术栈建议

| 需求 | 推荐默认项 | 原因 |
| --- | --- | --- |
| 要检查的来源 | Slack 用于活跃请求，Gmail 用于待回复邮件，Google Calendar 用于时间判断，Notion 或 docs 用于项目状态。当 GitHub、Linear、MCPs 或本地 notes 是工作发生处时，也加入它们。 | 视图越强，Codex 越容易理解大背景，并跨来源找出信号。 |

#### 把 Codex 当作队友使用

当 Codex 能看到你的工作发生地时，它会更有用：Slack、Gmail、calendar、project trackers、docs、code 和 local notes。合在一起，这些来源展示了你在做什么、和谁合作，以及哪些请求或决定可能在一天中被埋没。

有了这个视图，一个 Codex 线程就可以成为 proactive teammate。它会随着你的使用学习你关心什么，然后 automation 会让 Codex 回到同一组来源中，只把值得打断你的信号带回来。

#### 开始一个 teammate thread

1. 连接工作发生工具的 plugins 或 MCPs。
2. 开始一个新的 Codex thread，并要求它检查这些来源。
3. 告诉 Codex 哪些 item 有用，哪些是噪声。
4. 给该线程添加 automation，然后 pin 线程并关注 notifications。
5. 从同一线程中操作：提问、拿草稿，并告诉 Codex 下一步要采取什么 action。

#### 运行一次有用检查

从已经保存你工作上下文的工具开始。对一个人来说，这可能是 Gmail、Slack、calendar、Notion、GitHub、Linear 和本地 notes 文件夹。要求 Codex 检查这些来源，并告诉你什么需要关注。

使用本页起始提示完成第一次检查。你可以保持一般性，也可以指定某个 workstream、account、launch、team 或 project。

一个有用的 Codex 回复可能像这样：

<p>
    <strong>有一件事变了。</strong>
  </p>
  <p>
    renewal prep 现在说明，customer 在 partner note 发出前需要 security export wording。partner update 仍把这项工作描述为广泛的 reporting automation。
  </p>
  <p>
    有用的动作是让 Lina 的 note 保持狭窄：说明 export 帮助 audit prep，链接 renewal prep，并在 Owen sign off 前不要加入更广泛的 automation claim。
  </p>
  <p>
    <strong>优先级：</strong>在发送 review packet 前更新 partner line。
  </p>

有用输出会说明 trigger、展示 source、解释影响，并建议下一步动作。当你纠正线程时，Codex 会更多了解你的工作方式：哪些来源重要，哪些 owners 已经接手工作，草稿应该多直接，以及什么值得带回来。

#### 把线程变成 automation

当线程变得有用后，要求 Codex 在同一线程中持续关注。Automation 是定时 check-in，会把 Codex 送回你指定的来源，然后只有在发现值得你关注的信号时才发布新消息。它可以每小时运行、每个工作日早上运行，或在其它指定时间运行。

这正适合 Codex [automations](24-automations.md)：先在普通线程中测试 prompt，再向该线程添加 automation。因为 Codex 可以 compact 长对话，同一个线程可以随你的纠正持续改进，而不是每天早上重新开始。

#### 从同一线程中操作

teammate 在提醒之后会变得更有价值。像对待同事一样操作 Codex：在同一线程中提问，然后让它把信号转成 reply、handoff note 或 decision brief。

Codex 可以观察、解释和起草。外部操作仍由你批准。

#### 相关链接

- [Codex automations](24-automations.md)
- [Codex plugins](78-plugins.md)
