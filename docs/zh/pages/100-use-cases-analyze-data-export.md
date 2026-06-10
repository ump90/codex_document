### 查询表格数据

Source: [Query tabular data](https://developers.openai.com/codex/use-cases/analyze-data-export.md)

询问关于 CSV、电子表格、导出或数据文件夹的问题。

#### 概览

将 Codex 与 CSV、电子表格、dashboard 导出、Google Sheet 或本地数据文件一起使用，用来回答问题、创建浏览器可视化，并保存结果。

适合：

- 可以通过快速计算、图表、表格或简短摘要回答的问题。
- 需要分析数据并创建可视化的角色。

相关 skill：

- `$spreadsheet`：检查表格数据、运行计算，并创建图表或表格。
- `google-sheets`：当数据位于共享电子表格中时，分析已批准的 Google Sheets。

#### 起始提示

```text
分析 @sales-export.csv

问题：上个季度哪个客户细分变化最大？

请：
- 先检查列，再开始分析
- 根据数据回答问题
- 创建一个简单的浏览器可视化 HTML 文件
- 启动本地预览，方便我在 Codex 浏览器中打开
```

建议使用低工作量。

#### 相关链接

- [文件输入](https://developers.openai.com/api/docs/guides/file-inputs)
- [Agent skills](48-agent-skills.md)

#### 分析数据

当你有 CSV、电子表格、dashboard 导出、Google Sheet 或本地数据文件，并希望根据它回答问题时，可以使用 Codex。从文件和问题开始。Codex 可以检查列、运行分析，并创建你可以在 Codex app 中打开的浏览器可视化。

1. 附加文件，或提及已连接的数据源。
2. 提出你想回答的问题。
3. 让 Codex 检查列、运行计算，并创建 HTML 可视化。
4. 在 Codex 浏览器中打开本地预览，然后在同一个 thread 中继续调整图表，或用另一种方式切分数据。

使用 `@` 附加 CSV，或提及 Google Sheet。如果数据来自 dashboard，请先导出行，让 Codex 能够检查原始列。

#### 后续分析

Codex 给出第一个答案后，继续询问你通常会检查的下一个比较。

你可以在同一个 thread 中继续：清理某一列、排除测试细分、比较两个时间窗口、让图表更易读，或把结果转成会议用的简短备注。
