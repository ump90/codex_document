### 把会议转成 follow-ups

Source: [Turn meetings into follow-ups](https://developers.openai.com/codex/use-cases/zoom-meeting-follow-ups.md)

把 Zoom 会议洞察转成跨工具 actions。

#### 概览

使用 Codex 搭配 Zoom transcripts 和 AI Companion summaries，为 customer follow-up emails、account plans、CRM updates 和 team notifications 起草可审查内容。

适合：

- 希望不在工具间复制 notes，也能拥有可重复 post-meeting execution 的团队。
- discovery、renewal、implementation 或 executive sponsor calls 之后的 customer follow-ups。
- 需要跨 meeting notes、docs、CRM 和 team messages 更新的 sales 和 customer success workflows。

相关 skill：

- `zoom`：在 authentication 和 admin approval 后，读取可访问的 Zoom meetings、recordings、transcripts 和 AI Companion summaries。
- `google-drive`：创建或起草 account plans、meeting briefs 和其它可审查 follow-up documents。
- `slack`：在用户审查并批准消息后，起草 team updates。

#### 起始提示

**创建会后 follow-up package**

```text
使用我最近一次与 [customer or account] 的 Zoom meeting。

检索 Zoom transcript 和 AI Companion summary。起草前说明你无法访问的任何内容。

总结 key takeaways、decisions、risks、opportunities 和 action items。然后起草：
- customer follow-up email
- Google Docs account plan
- CRM update，包含 notes、risks、next steps 和 owners
- 发给 [team/channel/person] 的 Slack message，包含最重要细节

尽可能使用 transcript 中的证据。标记任何 uncertain 内容，并把 internal-only details 从 customer draft 中移除。

在我审查并批准每个 action 前，不要发送 emails、发布 Slack messages、创建 docs、更新 CRM records、分配 owners 或暴露 private data。
```

建议使用低推理强度。

#### 简介

面向客户的团队会在会议后花费真实时间把对话转成行动。一次电话可能产生 follow-up email、CRM notes、account plan、risk updates 和 internal handoffs，但这些 artifacts 通常分布在不同系统中。

借助 Zoom meeting data 和已连接工具，Codex 可以检索相关 transcript 和 AI Companion summary，提取结构化洞察，并准备推动工作所需的下游 drafts。在任何内容被发布、发送、分配或写入另一个系统之前，你都保留审查环节。

#### 创建第一个 follow-up package

1. 启用 Zoom AI Companion meeting summaries、smart recordings、transcript generation、cloud recording 和 audio transcripts。
2. 连接 Zoom 以及你希望 Codex 使用的工具，例如 Google Docs、Slack、Gmail 或你的 CRM。
3. 要求 Codex 按 customer、date、recurring series 或 meeting title 查找会议。
4. 审查生成的 summary、risks、actions、email draft、account plan、CRM notes 和 Slack message。
5. 只有在验证内容之后，才批准 external actions。

使用本页起始提示完成第一轮。Codex 应返回结构化 package，包括 key takeaways、risks、opportunities、decisions、action items、follow-up email draft、account plan outline、CRM update draft 和 Slack notification draft。

#### 给 Codex 合适上下文

当 Codex 能读取 meeting source material，并知道每个 follow-up 应去哪里时，这个工作流效果最好。

有用输入包括：

- Zoom meeting recording、transcript 和 AI Companion summary。
- Meeting metadata，例如 customer name、date、title 或 recurring series。
- Destination tools，例如 Google Docs、Slack、Gmail 或 CRM records。
- Tone、privacy、account-plan structure 或 internal handoff format 的任何规则。

Codex 可以随后总结 transcript，识别 decisions 和 owner/date commitments，起草 customer-facing email，准备 account plan，并编写 team update。对于 recurring meetings，它可以把最新 transcript 与之前几次 calls 对比，并突出变化。

#### 先审查再行动

Meeting follow-up 可能触及 customer data、private notes 和 systems of record。使用 Codex 准备 drafts、引用 transcript evidence，并在你批准下一步之前暂存 updates。

行动前请审查：

- Audience 或 destination，例如 customer、Slack channel、CRM record 或 document permissions。
- Customer commitments、owners、dates、risks 和 uncertain claims。
- 哪些 items 应保持为 drafts，哪些可以发送、发布、共享或保存。
- 是否应移除 confidential 或 internal-only details。

对于 recurring workflows，保持模式聚焦：draft、review、approve，然后 act。

#### 跟进第一版草稿

第一份 package 准备好后，在同一线程中继续针对 audience 或下一步 workflow 调整它。

你也可以要求 Codex 将这次 call 与过去几次 weekly calls 比较，把 action items 转成 mutual action plan，为 sales engineer 创建只包含 technical blockers 的版本，或起草 CRM updates 但不保存。

#### 自动化周期性 meeting intelligence

对于 weekly account check-ins 或 deal reviews，pin 线程，并要求 Codex 创建 [thread automation](24-automations.md#thread-automations)。

你不一定希望 Codex 自动发布，但它可以创建 drafts 供你审查，然后由你批准并发布。

#### 相关链接

- [Codex plugins](78-plugins.md)
- [Codex automations](24-automations.md)
