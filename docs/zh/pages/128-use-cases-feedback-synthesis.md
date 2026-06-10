### 将反馈转化为行动

Source: [Turn feedback into actions](https://developers.openai.com/codex/use-cases/feedback-synthesis.md)

把来自多个来源的反馈综合成可审查 artifact。

#### 概览

将 Codex 连接到 Slack、GitHub、Linear 或 Google Drive 等多个数据源，把反馈分组到可审查的 Google Sheet、Google Doc、Slack 更新或定期反馈检查中。

适合：

- 分析来自 Slack 频道、issue threads、survey exports、support-ticket CSVs 或研究笔记的反馈。
- 需要把反馈转化为可执行洞察的团队。

相关 skill：

- [`slack`](https://github.com/openai/plugins/tree/main/plugins/slack)：读取已批准的反馈频道或 thread links。
- [`github`](https://github.com/openai/plugins/tree/main/plugins/github)：读取 issues、PR comments 和 discussion threads。
- [`linear`](https://github.com/openai/plugins/tree/main/plugins/linear)：读取 bug 或 feature queues。
- [`google-drive`](https://github.com/openai/plugins/tree/main/plugins/google-drive)：读取反馈文档、exports 和 folders，然后创建 Google Doc 或 Sheet。
- [`google-sheets`](78-plugins.md)：创建团队可以排序、评论和更新的反馈 sheet。

#### 起始提示

**创建第一版**

```text
你能把 [feature or product area] 的 beta feedback 综合到一个 @google-sheets 审查表中吗？

使用这些来源：
- @slack [feedback channel or thread links]
- @github [issue search or issue links]
- @google-drive [survey export, notes doc, or Drive folder]

在 sheet 中，对重复反馈分组，包含 source links 或 IDs，标记 confidence，并指出哪些项目需要 product 或 engineering follow-up。

除非我批准，不要在可见摘要中包含姓名和私有引述。不要发布、发送、创建 issues 或分配 owners。
```

建议使用低工作量。

#### 相关链接

- [Codex plugins](78-plugins.md)
- [Codex automations](24-automations.md)
- [Agent skills](48-agent-skills.md)

当反馈分散在 Slack 频道、survey export 和几个 issue threads 中时，Codex 可以把它们汇总成团队可审查的 Google Sheet 或 Doc。

## 创建第一版

1. 给 Codex 反馈来源和一句上下文。
2. 要求生成包含 themes、evidence links、questions 和 follow-ups 的 Google Sheet 或 Doc。
3. 使用同一个线程把已审查 sheet 转化为 Slack 更新或 issue 草稿。
4. 如果反馈来源持续变化，请 pin 该线程并添加自动化。

使用本页起始提示进行第一轮。来源可以是 plugin links、附加文件，或 Google Drive 中的文件。

## 将 sheet 转化为下一版草稿

sheet 创建后，使用同一个线程让它对下一个人更有用。让 Codex 添加一列、拆分一个 theme、起草 Slack 更新，或把已审查 theme 转化为 issue 草稿。

## 保持反馈频道更新

对于持续收到新报告的 Slack 频道或 issue queue，请 pin 线程并让 Codex 按计划检查。
