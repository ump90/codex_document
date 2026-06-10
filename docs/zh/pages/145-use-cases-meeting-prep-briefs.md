### 准备会议简报

Source: [Prepare meeting briefs](https://developers.openai.com/codex/use-cases/meeting-prep-briefs.md)

把日历上下文转成议程和笔记计划。

#### 概览

使用 Codex 搭配 Calendar、Drive、Slack 和 Gmail，在会议前收集已批准来源，然后起草目标、议程、问题和笔记模板。

适合：

- 上下文分散在日历邀请、docs、Slack threads、email 和 notes 中的会议。
- 想要有来源支撑的会前资料包的 managers、product teams、operators 和 interviewers。

相关 skill：

- `google-calendar`：找到会议、参会者、时间和应影响简报的附件材料。
- `google-drive`：读取链接 docs、interview notes、pre-reads、trackers 和 source artifacts。
- `slack`：当会议依赖相关信息时，拉取最新 planning thread、decision context 或 collaborator updates。
- `gmail`：检查相关 email threads 中的日程变更、附件或外部上下文。

#### 起始提示

**构建会前简报**

```text
帮我准备 [meeting] 在 [date] 的会议。

只使用这些来源：
- calendar event: [event name or date range]
- docs or notes: [links or names]
- Slack channels or threads: [optional]
- Gmail thread or sender: [optional]

首先，盘点你能访问的来源，并说明任何来源缺口。

返回：
- meeting objective
- attendee context
- key source-backed facts
- likely agenda
- open questions
- decisions or follow-ups I may owe
- suggested notes template for the meeting

把 unsupported claims 放在单独的 source gaps section 中。在我批准前，不要更新 docs、发送消息或分享简报。
```

建议使用低推理强度。

#### 基于你已有的来源做准备

会议上下文经常不只存在于日历邀请中。Drive 里可能有 pre-read，Slack 里可能有一项决定，邮件线程里可能有背景，或者之前对话里有 notes。

使用 Codex 收集已批准来源，并起草一份简短会前简报，包含 objective、agenda、open questions 和 notes template。

#### 收集合适上下文

1. 指定会议、日期或 calendar event。
2. 指向 Codex 可使用的 docs、notes、Slack threads、email threads 或 folders。
3. 要求 Codex 在写简报前先盘点来源。
4. 让它区分已确认上下文、来源缺口和开放问题。
5. 如果你需要在会议中记录决定，请要求 notes template 或 scorecard。

对于面试循环，要求 Codex 阅读已批准 notes 或 question bank，然后生成结构化 scorecard。对于周期性 planning meetings，要求它把上一次 notes 与最新来源更新进行比较，让 agenda 从变化内容开始。

#### 保持简报易扫读

要求输出尽可能短，只保留真正有帮助的内容。你应该得到类似这样的内容：

<p>
    <strong>目标：</strong>决定 launch plan 在接下来两周是否有足够 owner 覆盖。
  </p>
  <p>
    <strong>上下文：</strong>pre-read 中有一版 owner map，但 Slack 里还有两个 follow-up item 需要日期。
  </p>
  <p>
    <strong>问题：</strong>谁负责 partner review，public copy freeze 的最晚日期是什么？
  </p>
  <p>
    <strong>笔记模板：</strong>decisions、owners、dates、risks 和 follow-ups。
  </p>

如果简报包含私密或敏感信息，请让输出留在本地线程中，并要求 Codex 标出不应进入共享 doc 的内容。

#### 相关链接

- [Codex plugins](78-plugins.md)
- [Use Codex with Google Calendar](78-plugins.md)
- [Codex app](44-codex-app.md)
