### 运行活动 playbook

Source: [Run event playbooks](https://developers.openai.com/codex/use-cases/event-launch-playbooks.md)

为活动项目管理创建可重复工作流。

#### 概览

将 Codex 与 Slack、Google Drive 和 Calendar 结合使用，收集规划上下文，起草面向参与者的文案，并准备包含 owner、审批和开放问题的私有检查清单。

适合：

- 运营活动的社区、开发者关系、市场和运营团队。
- 需要把公开文案和私有运营内容分开的活动页面、交接和发布检查清单。
- 需要有来源支撑的模板、owner、审批和开放问题的重复活动项目。

相关 skill：

- [`slack`](https://github.com/openai/plugins/tree/main/plugins/slack)：读取定义当前活动范围的规划频道、threads、canvases 和决策。
- [`google-drive`](https://github.com/openai/plugins/tree/main/plugins/google-drive)：收集已批准模板、活动文档、decks、复盘笔记和发布资产。
- [`google-calendar`](https://github.com/openai/plugins/tree/main/plugins/google-calendar)：在构建 playbook 时检查活动时间、截止日期和会议上下文。
- `sheets`：用结构化格式跟踪任务、owner 和截止日期。

#### 起始提示

**构建活动 Playbook**

```text
为 [event] 创建一个有来源支撑的 playbook。

要使用的来源：
- planning channels or threads: [links or names]
- approved docs, decks, sheets, or templates: [links or names]
- calendar events or deadlines: [links or dates]

将输出拆分为：
- 面向参与者的文案
- 私有运营检查清单
- owner map
- 支持计划或资源
- 仍需审批的事项
- 开放问题
- 来源附录

不要发布任何内容，也不要假设缺失细节。把未知项放入开放问题，并让私有运营内容远离公开文案。
```

建议使用中等工作量。

#### 相关链接

- [Codex plugins](78-plugins.md)
- [Codex automations](24-automations.md)
- [Use Codex in Slack](56-use-codex-in-slack.md)

## 介绍

当你有活动项目需要管理时，例如我们的 [Codex community meetups](https://developers.openai.com/community/meetups)，上下文通常散落在多个来源中：

- 公开活动页面
- 项目支持计划
- Slack 消息
- Sheets 或文档
- 等等

你可以使用 Codex 收集已批准的规划来源，并把它们转化为 playbook，将面向参与者的文案与私有运营细节分开。

## 创建第一个 playbook

使用起始提示让 Codex 为你生成活动 playbook。它应当：

- 命名规划来源（可以是链接、内部工具等）。
- 列出所需信息。
- 定义面向参与者文案的规则（把内部后勤排除在外）。

你应获得一份每次规划新活动时都可以检查和运行的事项列表。

## 将 playbook 作为自动化运行

当新的 playbook 第一次运行成功后，保持同一个线程打开，并让 Codex 将它作为定时自动化运行。
