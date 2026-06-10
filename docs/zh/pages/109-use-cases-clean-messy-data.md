### 清理和准备杂乱数据

Source: [Clean and prepare messy data](https://developers.openai.com/codex/use-cases/clean-messy-data.md)

处理表格数据，而不影响原始文件。

#### 概览

拖入或提及一个杂乱 CSV 或电子表格，描述你看到的问题，并要求 Codex 写出一份清理后的副本，同时保持原始文件不变。

适合：

- 日期、货币、重复项、汇总行或缺失值混杂的 CSV 或电子表格导出。
- 使用来自多个来源的数据的团队。

相关 skill：

- `$spreadsheet`：检查表格文件、清理列，并产出可审查输出。

#### 起始提示

```text
清理 @marketplace-risk-rollout-export.csv。

问题：
- 日期混用了 MM/DD/YYYY 和 YYYY-MM-DD
- 货币值包含 $、逗号和空白单元格
- 几条重复 customer rows 来自重复导出
- region 和 category 名称使用了多个别名
- 数据中混入了粘贴的 summary rows

我想要：
- 写出清理后的 CSV
- 保持原始文件不变
- 使用一种日期格式
- 保留空白货币单元格为空白
- 尽可能保留 source row IDs
- 添加简短 data-quality note，说明你更改、移除或无法有把握清理的行
```

建议使用低工作量。

#### 相关链接

- [用 Codex 分析数据](100-use-cases-analyze-data-export.md)
- [文件输入](https://developers.openai.com/api/docs/guides/file-inputs)
- [Agent skills](48-agent-skills.md)

#### 引言

Codex 非常适合系统化清理表格数据。当 CSV 或电子表格中存在混合日期、重复行、货币字符串、空白单元格、别名或粘贴的汇总行时，要求 Codex 清理一份副本，并保持原始文件不变。

#### 如何使用

1. 把文件拖入 Codex，或在提示中提及它，例如 `@customer-export.csv`。
2. 描述你已经看到的问题。
3. 告诉 Codex 清理后的版本应是什么：CSV、电子表格 tab，或可上传文件。
4. 使用前审查清理后的副本。

使用本页的起始提示完成第一次清理 pass。把文件名和 bullets 替换为你自己的内容。有用的细节是你已经看到的问题，以及下一步需要的文件：清理后的 CSV、干净的电子表格 tab，或可上传文件。Codex 写出干净副本后，先打开清理后的文件和 thread 中的 data-quality note，再把数据用于下游。
