### 建立 DCF 估值模型

Source: [Model a DCF valuation](https://developers.openai.com/codex/use-cases/dcf-model.md)

把财务输入转化为可编辑的估值工作簿。

#### 概览

附上历史财务数据、估值假设和建模说明，然后让 Codex 生成一个可在 Codex 中检查和修改的可编辑 DCF 工作簿。

适合：

- 将历史财务数据和假设转化为 DCF 工作簿的分析师。
- 希望在 Codex 中检查并迭代工作簿的财务团队。
- 正在根据源文件准备估值模型的团队。

相关 skill：

- `$spreadsheets`：根据附加输入、公式和假设创建可编辑电子表格工作簿。

#### 起始提示

**建立 DCF 估值模型**

```text
使用 $spreadsheets 为附加源文件中的公司构建一个 DCF 工作簿。

包含收入增长、利润率、资本开支和营运资本的明确经营驱动因素。计算 unlevered free cash flow、WACC、terminal value 和 enterprise value。如果提供了资本结构和摊薄后股数，请桥接到 implied equity value 和 implied equity value per share。

使用源文件中包含的任何假设。如果缺少某个假设，请在 assumptions tab 中添加清晰标注的占位项，而不是把它隐藏在公式里。如果缺少完整资产负债表或现金流量表输入，请创建计算 unlevered free cash flow 所需的经营预测，并标记缺失的报表输入。

将结果生成为可编辑的 .xlsx 工作簿。
```

建议使用中等工作量。

#### 相关链接

- [Agent skills](48-agent-skills.md)
- [文件输入](https://developers.openai.com/api/docs/guides/file-inputs)

## 介绍

Codex 可以帮助你创建一个功能完整、可检查且可修改的 DCF 工作簿。

它可以使用多个文件作为上下文，包括历史财务数据、估值假设和任何建模说明。
你可以直接提供这些文件；如果输入位于 Google Drive 或其他已连接来源，也可以使用文件引用。如果是后者，请提供准确的文件引用，这比让 Codex 搜索你的所有文件更有效。

## 创建工作簿

1. 附加历史财务数据、估值假设和任何建模说明，或提供准确文件引用以及来源。
2. 运行起始提示，并要求生成可编辑的 `.xlsx` 工作簿。
3. 在 Codex 中打开生成的工作簿。将它展开到全屏视图，检查模型 tabs、公式、假设和估值摘要。
4. 在同一个线程中继续检查公式链接、改变假设、添加情景或收紧模型。

当工作簿出现在对话线程中时，在 Codex 中打开并全屏展开。审查源输入、预测驱动因素、估值输出和敏感性表，然后让 Codex 从那里继续修改同一个工作簿。

## 检查估值

在使用工作簿之前，让 Codex 像财务队友一样审查模型：source tie-outs、公式、硬编码假设和估值输出。

## 修改一个假设

在 Codex 中审查工作簿后，在同一线程中要求定向修改。一次只改一个 driver，这样影响更容易检查。
