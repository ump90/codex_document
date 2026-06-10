### 管理收件箱

Source: [Manage your inbox](https://developers.openai.com/codex/use-cases/manage-your-inbox.md)

让 Codex 找出重要邮件，并用你的语气撰写回复。

#### 概览

使用 Codex 搭配 Gmail 找出需要关注的邮件，用你的语气起草回复，从工作发生的工具中拉取上下文，并按计划持续关注新回复。

适合：

- 希望 Codex 找出需要关注的邮件，而不是手动整理收件箱的人。
- 可在后台创建可审查草稿的周期性收件箱检查。

相关 skill：

- `gmail`：搜索和 triage Gmail threads，阅读周围对话，按明确要求创建回复草稿并整理邮件。
- `slack`：当邮件需要最新决定、owner、asset 或 blocker 时，检查团队消息上下文。
- `google-drive`：读取应影响草稿的源 docs、FAQs、notes 或已批准写作示例。

#### 起始提示

**检查 Gmail 并起草回复**

```text
你能检查我的 @gmail，弄清楚我需要回复什么，并用我的语气写草稿吗。

使用我最近发出的回复，或 @google-drive [writing examples] 来确定语气。

当邮件缺少最新决定、owner、file 或 blocker 时，使用 @slack、@google-drive 或其它工作发生处的来源。
```

建议使用低推理强度。

#### 审查你的收件箱

让 Codex 检查 Gmail，找出值得回复的消息，并用你的语气写草稿。它可以使用最近已发送邮件或已批准写作示例来匹配风格，然后在邮件本身缺少上下文时搜索 Slack、docs、project notes 或其它工具。

使用 Codex 对收件箱做第一轮处理：找出需要你注意的邮件，起草回复，并带入能解释大背景的工作上下文。

1. 要求 Codex 审查 Gmail，找出需要你注意的邮件。
2. 要求它使用 Slack、docs 或 project notes 补充能解释大背景的上下文。
3. 告诉 Codex 哪些草稿有用，哪些邮件下次应忽略。
4. 当线程有用时添加 automation；如果想快速访问，可以 pin 它。

直接使用 Gmail plugin。你可以给 Codex 一个宽泛的收件箱请求、一个时间窗口，或一个 label，如果你已经知道范围。如果语气很重要，请先让 Codex 查看最近已发送回复，或包含示例的 doc，再开始起草。

使用本页的起始提示完成第一轮收件箱处理。Codex 应返回一个简短队列：需要关注邮件的草稿、可以等待的消息，以及当答案不只依赖邮件线程时它使用的上下文。

#### 让线程学习你的偏好

把第一轮当作校准。如果 Codex 起草了太多回复，告诉它哪些邮件是噪声。如果它漏掉了重要内容，告诉它为什么那个 thread 重要。如果语气不对，直接修改草稿。

随着时间推移，这个线程应该更擅长判断什么需要草稿，什么可以不打扰你。

#### 按计划自动化邮件 triage

你可以创建 automations，在同一线程上运行定期 check-in。Codex 会被唤醒，检查 Gmail 和你指定的上下文来源，并且只有在有需要你关注的邮件或值得审查的草稿时才发帖。

草稿开始有用后，可以要求 Codex 持续关注 Gmail。邮件 triage 很适合自动化：草稿可审查，最终由你决定发送什么。

在线程已经对你的回复模式有较好理解后，配合 Codex [automations](24-automations.md) 使用。如果 Codex 找到需要你做决定的邮件，它应该标出问题，而不是猜测。

#### 整理收件箱

Gmail plugin 也可以帮助整理收件箱。请把这作为你信任 triage 后的单独命令。

对于删除操作，请把指令写得明确且狭窄。起草回复适合自动化后审查；破坏性清理应该保持有意为之。

#### 相关链接

- [Codex plugins](78-plugins.md)
- [Codex automations](24-automations.md)
