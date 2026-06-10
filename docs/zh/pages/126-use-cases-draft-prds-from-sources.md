### 从内部上下文起草 PRD

Source: [Draft PRDs from internal context](https://developers.openai.com/codex/use-cases/draft-prds-from-sources.md)

从 Linear、Slack、源文档和会议笔记创建产品需求文档。

#### 概览

将 Codex 与 `$documents` skill 以及 Linear、Slack、Notion 或 Google Drive 等已连接应用结合使用，创建可审查的 PRD，包含预期章节、时间线、决策、开放问题和来源附录。

适合：

- 将规划上下文转化为 PRD、proposal、launch brief 或 decision memo 的产品团队。
- 在内部讨论中与团队对齐后，需要快速起草 PRD 的 PM。

相关 skill：

- `$documents`：当 PRD 应成为精美文件而不是聊天文本时，创建、编辑并验证 DOCX。
- [`slack`](https://github.com/openai/plugins/tree/main/plugins/slack)：从已批准频道或 thread links 读取产品讨论、发布线程、决策说明和后续问题。
- [`linear`](https://github.com/openai/plugins/tree/main/plugins/linear)：读取应影响 PRD 的项目、issues、优先级、验收标准和开放工作。
- [`google-drive`](https://github.com/openai/plugins/tree/main/plugins/google-drive)：读取规划文档、研究笔记、规格、导出的会议笔记和源文件夹。
- [`notion`](https://github.com/openai/plugins/tree/main/plugins/notion)：读取应影响 PRD 的路线图页面、项目笔记、会议笔记和团队 wiki。

#### 起始提示

**起草 PRD**

```text
使用 $documents，基于 @linear [project or milestone]、@slack [channel or thread]，以及 @google-drive 或 @notion [planning docs, research notes, meeting notes, or source folder]，为 [feature or product area] 创建 PRD。

包含 problem、users、goals/non-goals、requirements、UX、technical considerations、metrics、launch plan、risks、open questions、decisions、timeline 和 source appendix。

引用 requirement-level claims 背后的来源。如果来源冲突，请指出冲突，而不是悄悄选择一方。仅起草。未经我批准，不要发布、更新 Linear 或分享文档。
```

建议使用中等工作量。

#### 相关链接

- [Codex plugins](78-plugins.md)
- [Agent skills](48-agent-skills.md)
- [Codex app](44-codex-app.md)

## 介绍

在处理新产品或功能之前，通常会起草产品需求文档（PRD），用于对齐范围和需求。编写 PRD 所需上下文往往已经存在于团队内部系统中：Linear 上的 tickets、Slack 中的讨论、Notion 或 Google Drive 中的草稿等。Codex 可以收集这些上下文并起草 PRD，供你审查和迭代，同时保持来源链路可见。

## 选择来源

从你希望 Codex 使用的来源开始：Linear 项目、Slack 规划频道或线程，以及应在 PRD 中引用的任何 Drive 文档、Notion 页面、会议笔记或本地文件。
你还应清楚列出预期的 PRD 章节，例如 problem、users、requirements、UX、tech、launch plan、timeline 或 decisions。

1. 当输出应是真实 DOCX 时，从 `$documents` 开始。
2. 直接命名来源：Linear 项目或 milestone、Slack 频道或线程，以及 Codex 应引用的文档或笔记。
3. 给 Codex PRD 章节契约。
4. 先审查 source appendix，再审查 requirements 和 open questions。
5. 使用同一个线程解决缺口、收紧范围，并准备交接。

## 在同一个线程中细化

使用本页起始提示生成第一版。如果缺少内容，请把 Codex 指向缺失来源，而不是重新开始。

## 检查来源链路

在分享 PRD 之前，让 Codex 列出支持较弱或缺失的 claims、未解决问题，以及它视为已确认的决策。如果 source appendix 不能让这些内容易于审计，请在导出或发布之前继续在同一线程中细化。

### 建议提示

**检查来源链路**
