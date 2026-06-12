### Codex 网页版

Source: [Codex web](https://developers.openai.com/codex/cloud.md)

Codex 是 OpenAI 的 coding agent，可以读取、编辑和运行代码。它帮助你更快地构建、修复 bug，并理解不熟悉的代码。借助 Codex cloud，Codex 可以使用自己的云端环境在后台处理任务，也可以并行处理多个任务。

#### Codex 网页版设置

前往 [Codex](https://chatgpt.com/codex) 并连接你的 GitHub 账户。这会让 Codex 能够处理你仓库中的代码，并基于它的工作创建 pull request。

你的 Plus、Pro、Business、Edu 或 Enterprise 计划包含 Codex。请查看[包含哪些内容](02-codex-pricing.md)了解更多。某些 Enterprise workspace 可能需要先完成[管理员设置](64-admin-setup.md)，然后你才能访问 Codex。

---

#### 使用 Codex 网页版工作

- [了解提示编写](07-prompting.md#prompts)：编写更清晰的 prompts，添加约束，并选择合适的详细程度，以获得更好的结果。
- [常见工作流](06-example-workflows.md)：从经过验证的模式开始，用于委派任务、审查变更，并将结果转换为 PR。
- [配置环境](25-cloud-environments.md)：选择 repo、setup steps，以及 Codex 在云端运行任务时应使用的工具。
- [从 IDE extension 委派工作](32-codex-ide-extension-features.md)：从编辑器启动 cloud task，然后监控进度并在本地应用生成的 diff。
- [从 GitHub 委派](49-codex-code-review-in-github.md)：在 issues 和 pull requests 中标记 `@codex`，即可启动任务并直接从 GitHub 提议变更。
- [控制互联网访问](23-agent-internet-access.md)：决定 Codex 是否可以从云端环境访问公共互联网，以及何时启用它。
