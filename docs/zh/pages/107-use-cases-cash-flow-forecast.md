### 预测现金流

Source: [Forecast cash flow](https://developers.openai.com/codex/use-cases/cash-flow-forecast.md)

在可编辑预测工作簿中找到流动性低点。

#### 概览

向 Codex 提供现金流输入和模型约束，然后要求它创建可编辑工作簿：保留源数据频率、标记安全余额阈值突破，并展示哪些假设推动现金压力。

适合：

- 构建 13 周或月度现金预测的财务和运营团队。
- 需要在一个工作簿中包含回款、薪资、供应商付款和营运资本假设的预测。
- 在规划会议前审查 runway、安全余额阈值突破和情景驱动因素的团队。

相关 skill：

- `$spreadsheets`：构建可编辑预测工作簿，把公式连接到假设，并为情景和输入缺口添加检查。

#### 起始提示

```text
使用 $spreadsheets 基于附加源文件构建一个可编辑现金流预测工作簿。

在可用时，使用 beginning cash、expected receipts、payroll、vendor payments、debt、tax、capex、working-capital items 和 timing assumptions。保留源数据频率，无论是 weekly 还是 monthly。

包含一个摘要视图，标记 liquidity low point、minimum ending cash balance，以及任何 safety cash threshold breach。使用公式，方便我之后修改假设，并在使用 placeholders 前指出缺失的 timing assumptions。
```

建议使用中等工作量。

#### 相关链接

- [Agent skills](48-agent-skills.md)

#### 引言

构建现金流预测时，你需要确保它准确并反映业务现实。你可以使用 Codex 帮助创建可在 Codex 中检查和修订的预测工作簿。附加现金流输入、运营假设和模型约束。当输入位于 Google Drive 或其它已连接来源中时，也可以使用文件引用。

#### 生成预测

1. 附加现金流输入、运营假设和模型约束。
2. 运行起始提示，并要求生成可编辑 `.xlsx` 工作簿。
3. 在 Codex 中打开工作簿。展开为全屏视图，检查假设、公式、情景和摘要 tab。
4. 在同一个 thread 中继续修改 collections、payroll、vendor payment、growth 或 safety-balance 假设。

当工作簿出现在 thread 中时，在 Codex 中打开并展开全屏。审查 timing assumptions、公式、情景和摘要 tab，然后要求 Codex 从同一个工作簿继续修订。

#### 审查现金压力

使用预测前，要求 Codex 识别低点，把工作簿追溯到源输入，并列出需要审查的假设。

#### 运行情景

在 Codex 中审查工作簿后，使用 follow-up prompts 一次修改一个情景驱动因素。
