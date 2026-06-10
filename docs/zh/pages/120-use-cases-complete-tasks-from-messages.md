### 完成消息中的任务

Source: [Complete tasks from messages](https://developers.openai.com/codex/use-cases/complete-tasks-from-messages.md)

把 iMessage 对话串转化为跨相关应用完成的工作。

#### 概览

使用 Computer Use 读取一个 Messages 对话串、完成任务并起草回复。

适合：

- 包含具体请求、跟进事项或预订任务的消息对话串。
- 需要在 Messages 以及少数相关应用中快速核对的工作。

#### 起始提示

**从消息对话串完成一个任务**

```text
@Computer 查看我来自 [person] 的消息。

然后：

- 理解请求
- 跨相关应用完成任务
- 在同一个对话串中起草回复

在任何不可逆操作之前暂停，例如下单或确认预订。
```

#### 相关链接

- [Computer Use](35-computer-use.md)
- [自定义 Codex](52-customization.md)

## 介绍

许多消息对话串里都藏着待办事项：预订晚餐、安排跟进、研究选项、提交收据，或整理信息以便回复。Computer Use 可以读取对话、识别任务，并在相关应用中完成工作。

当消息包含具体请求，而你希望 Codex 负责后续执行，而不只是总结对话时，这个用例很合适。

## 如何使用

1. 安装 [Computer Use plugin](35-computer-use.md)。
2. 让 Codex 审查特定消息对话串或发送者。
3. 告诉它要采取什么动作，以及在完成任何操作前是否需要暂停。
4. 指定它是否应在原始对话串中起草回复。

例如：

- `@Computer 查看我来自 [person] 的消息。检查我的可用时间，在 Hayes Valley 找 2 个晚餐选项，并在同一个对话串中起草回复。在完成预订前先和我确认。`

## 实用技巧

### 在不可逆操作前要求暂停

如果任务可能会转账、提交订单、确认预订或最终敲定日程，请告诉 Codex 在采取最后一步之前停下来询问。

### 确保辅助应用已准备好

当相关应用已经登录且可用时，效果最好。如果任务依赖 Maps、Calendar、Notes、预订网站或浏览器会话，请提前准备好。

### 预期对话串会被标为已读

当 Codex 在 Messages 中打开对话串时，它的行为就像普通用户查看对话一样。请把它视为已读。

## 良好的后续操作

同一模式也可用于 Slack 或电子邮件等其他 inbox 风格界面：工作从一条消息开始，并在其他地方完成。如果该工作流变得常见，请在 [customization](52-customization.md) 中添加可复用偏好或指令，让 Codex 每次以相同方式处理这些请求。

### 建议提示

**从消息对话串完成一个任务**
