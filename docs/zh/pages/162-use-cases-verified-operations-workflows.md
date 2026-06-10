### 运行可验证的运营工作流

Source: [Run verified operations](https://developers.openai.com/codex/use-cases/verified-operations-workflows.md)

运行可重复工作流，并验证结果。

#### 概览

使用 Codex 规范化 inputs，运行已批准 scripts 或 APIs，在有边界的失败上重试，并在汇报前从 logs 或 artifacts 验证结果。

适合：

- 具有结构化 inputs、明确 approval，并且结果应可审计的 operations tasks。
- 重复性工作流，例如 access updates、invite batches、quota changes、customer setup tasks、routing checks 和 migration follow-ups。
- 需要 Codex 在狭窄范围内运行，并准确报告哪些成功、失败或需要人工决定的团队。

#### 起始提示

**运行已批准 workflow**

```text
我需要运行这个 workflow：

Goal: [what should happen]
Inputs: [CSV, Google Sheet, list, ticket, or file path]
Approval or policy source: [Slack thread, doc, ticket, or none]
Runner: [script, API, CLI, skill, or manual app workflow]
Verification artifact: [result CSV, log, dashboard, screenshot, or other proof]

请：
- 检查 inputs，并只询问缺失的 required fields
- 运行 workflow 前规范化 dates、amounts、owners 和 IDs
- 当 workflow 支持 dry run 时，先执行 dry run
- 只运行 approved scope
- 为每个 item 记录一行 success 或 failure
- 对 transient failures 重试一次，不要重新开始已成功 rows
- 汇总 totals、failures、retries 和 verification artifacts

在 irreversible actions 或 scope changes 前暂停。
```

建议使用中等推理强度。

#### 运行可审计的 operations

如果你有需要定期运行的重复 operations，例如给用户授予访问权限、应用 batch update，或用不同参数调用脚本，你可以使用 Codex 自动化它，并得到可审计输出。

当 Codex 应运行一个可重复 operation，并通过可作为验证的 artifact 展示发生了什么时，使用这个工作流。

#### 描述任务和输入

1. 给 Codex input table、files、tickets 或其它需要批量运行流程的 list。
2. 如果适用，指向定义允许范围的 approval source 或 policy。
3. 告诉 Codex 哪个 script、API、skill、CLI 或 app workflow 应执行工作。
4. 当 workflow 支持时，可以要求 dry run。
5. 要求 Codex 运行 batch operation，并为每个 item 记录一行 success 或 failure。

保持范围狭窄，并要求 Codex 只有在拥有所有 required inputs 时才运行 operation。
如果某行缺少 required field，Codex 应标记该行，而不是猜测。

通过 [plugins](78-plugins.md) 连接你用于运行 operation 的工具，例如 ticketing system，或包含 list items 的 spreadsheet。

#### 要求证据来验证结果

有用的 operations run 会包含你或队友可检查的 artifact，例如 result CSV、log file、dashboard link、screenshot、PR check，或任何其它能证明 operation 成功的 evidence。在使用 Codex app 时，你可以在运行后通过 artifact viewer 检查这个 artifact 来验证结果；相关能力见 [Codex 应用功能](27-codex-app-features.md)。

#### 把运行转成可复用 workflow

第一次成功运行后，要求 Codex 捕获可重复部分。对于常见 workflows，这可以变成 [skill](48-agent-skills.md)，或按计划运行的 [automation](24-automations.md)。

对于 scheduled operations，只有在 manual run 产生可靠输出后才使用 automation。除非你明确希望 Codex 执行操作，否则让可能影响 access 或 data 的敏感 actions 永久保持 draft-only。

#### 相关链接

- [Codex plugins](78-plugins.md)
- [Codex automations](24-automations.md)
- [Agent skills](48-agent-skills.md)
