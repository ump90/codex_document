### Codex IDE 扩展功能

Source: [Codex IDE extension features](https://developers.openai.com/codex/ide/features.md)

Codex IDE 扩展让你可以直接在 VS Code、Cursor、Windsurf 和其他兼容 VS Code 的编辑器中使用 Codex。它使用与 Codex CLI 相同的智能体，并共享相同配置。

#### 向 Codex 提示

在编辑器中使用 Codex 可以无缝聊天、编辑和预览变更。当 Codex 拥有打开文件和选中代码的上下文时，你可以编写更短的提示，并获得更快、更相关的结果。

你可以在提示中像这样标记任意编辑器文件来引用它：

```text
Use @example.tsx as a reference to add a new page named "Resources" to the app that contains a list of resources defined in @resources.ts
```

#### 在模型之间切换

你可以使用聊天输入框下方的切换器切换模型。

#### 调整推理强度

你可以调整推理强度，以控制 Codex 在回应前思考多久。更高的强度有助于复杂任务，但响应会更慢。更高的强度也会使用更多 token，并可能更快消耗你的速率限制，尤其是在使用能力更强的模型时。

使用上面同一个模型切换器，并为每个模型选择 `low`、`medium` 或 `high`。从 `medium` 开始，只有在需要更深入推理时才切换到 `high`。

#### 选择批准模式

默认情况下，Codex 运行在 `Agent` 模式。在此模式下，Codex 可以自动读取文件、进行编辑，并在工作目录中运行命令。Codex 在工作目录之外操作或访问网络时仍需要你的批准。

当你只想聊天，或想先规划再进行更改时，请使用聊天输入框下方的切换器切换到 `Chat`。

如果你需要 Codex 在无需批准的情况下读取文件、进行编辑，并带网络访问运行命令，请使用 `Agent (Full Access)`。这样做前请谨慎。

#### 云端委派

你可以把较大的工作交给云端 Codex，然后无需离开 IDE 即可跟踪进度并审查结果。

1. 为 Codex 设置一个 [云环境](https://chatgpt.com/codex/settings/environments)。
2. 选择你的环境并选择 **Run in the cloud**。

你可以让 Codex 从 `main` 运行（适合开始新想法），也可以从你的本地变更运行（适合完成任务）。

当你从本地对话启动云任务时，Codex 会记住对话上下文，以便从你离开的地方继续。

#### 云任务后续处理

Codex 扩展让预览云端变更变得直接。你可以要求后续任务在云端运行，但通常你会想把变更应用到本地，以便测试和收尾。当你在本地继续对话时，Codex 也会保留上下文来节省时间。

你也可以在 [Codex cloud 界面](https://chatgpt.com/codex) 中查看云任务。

#### 网页搜索

Codex 随附第一方网页搜索工具。对于 Codex IDE 扩展中的本地任务，Codex 默认启用网页搜索，并从网页搜索缓存提供结果。该缓存是 OpenAI 维护的网页结果索引，因此缓存模式会返回预索引结果，而不是抓取实时页面。这减少了暴露于任意实时内容中提示注入的风险，但你仍应将网页结果视为不可信。如果你将沙盒配置为 [full access](https://developers.openai.com/codex/agent-approvals-security)，网页搜索默认使用实时结果。请参阅 [Config basics](https://developers.openai.com/codex/config-basic)，了解如何禁用网页搜索或切换到会抓取最新数据的实时结果。

每当 Codex 查找内容时，你会在转录记录或 `codex exec --json` 输出中看到 `web_search` 项。

#### 将图片拖放到提示中

你可以将图片拖放到提示输入区中，把它们作为上下文包含进去。

拖放图片时按住 `Shift`。否则 VS Code 会阻止扩展接受拖放。

#### 图片生成

无需离开编辑器，就可以要求 Codex 生成或编辑图片。这对于 UI 资产、布局、插图、精灵图表，以及工作时的快速占位图很有用。当你希望 Codex 转换或扩展现有资产时，请在提示中添加参考图片。

你可以用自然语言请求，也可以在提示中包含 `$imagegen` 来显式调用图片生成技能。

内置图片生成使用 `gpt-image-2`，计入你的常规 Codex 使用限制，并且根据图片质量和尺寸，平均消耗包含额度的速度比没有图片生成的类似回合快 3-5 倍。详情请参阅 [定价](https://developers.openai.com/codex/pricing#image-generation-usage-limits)。提示技巧和模型详情请参阅 [图像生成指南](https://developers.openai.com/api/docs/guides/image-generation)。

对于更大批量的图片生成，请在环境变量中设置 `OPENAI_API_KEY`，并要求 Codex 通过 API 生成图片，这样会适用 API 价格。

#### IDE 功能参考

- [Codex IDE extension settings](https://developers.openai.com/codex/ide/settings)
