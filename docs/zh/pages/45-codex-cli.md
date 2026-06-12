---
title: Codex CLI
---

Source: [Codex CLI](https://developers.openai.com/codex/cli.md)

Codex CLI 是 OpenAI 的 coding agent，你可以在本地终端中运行它。它可以在所选目录中读取、修改并运行你机器上的代码。

它是[开源项目](https://github.com/openai/codex)，并使用 Rust 构建，以获得更好的速度和效率。

ChatGPT Plus、Pro、Business、Edu 和 Enterprise 计划均包含 Codex。请查看[包含哪些内容](02-codex-pricing.md)了解更多。

[观看 Codex CLI overview 视频](https://www.youtube.com/watch?v=iqNzfK4_meQ)。

## CLI setup { .codex-visually-hidden }

<div class="codex-step-card" markdown="1">
<div class="codex-step-heading"><span class="codex-step-number">1</span><h3>Install</h3></div>

使用 macOS 和 Linux 的独立安装器安装 Codex CLI。

```text
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

对于无人值守安装，请在运行已下载安装器的 shell 中设置 `CODEX_NON_INTERACTIVE=1`。详情请参阅[环境变量](62-environment-variables.md#installer-variables)。

```text
curl -fsSL https://chatgpt.com/codex/install.sh | CODEX_NON_INTERACTIVE=1 sh
```
</div>

<div class="codex-step-card" markdown="1">
<div class="codex-step-heading"><span class="codex-step-number">2</span><h3>Run</h3></div>

在终端中运行 Codex。它可以检查你的仓库、编辑文件并运行命令。

```text
codex
```

第一次运行 Codex 时，系统会提示你登录。请使用你的 ChatGPT 账户或 API key 进行身份验证。

如果不确定哪些计划包含 Codex 访问权限，请查看[定价页面](02-codex-pricing.md)。
</div>

<div class="codex-step-card" markdown="1">
<div class="codex-step-heading"><span class="codex-step-number">3</span><h3>Upgrade</h3></div>

Codex CLI 会定期发布新版本。请查看[更新日志](88-changelog.md)了解发布说明。要升级独立安装版本，请重新运行安装器：

```text
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```
</div>

<div class="codex-info-card" markdown="1">
<span class="codex-info-icon">i</span>

Codex CLI 可在 macOS、Windows 和 Linux 上使用。在 Windows 上，可以在 PowerShell 中配合 Windows 沙箱原生运行 Codex；当你需要 Linux 原生环境时，也可以使用 WSL2。设置详情请参阅 [Windows 设置指南](83-windows-platform.md)。
</div>

如果你刚开始使用 Codex，请阅读[最佳实践指南](05-best-practices.md)。

---

## Work with the Codex CLI

- [交互式运行 Codex](30-codex-cli-features.md#running-in-interactive-mode)：运行 `codex` 启动交互式终端 UI（TUI）会话。
- [控制模型和推理](30-codex-cli-features.md#models-and-reasoning)：使用 `/model` 在 GPT-5.4、GPT-5.3-Codex 和其他可用模型之间切换，或调整推理级别。
- [图片输入](30-codex-cli-features.md#image-inputs)：附加截图或设计规格，让 Codex 在阅读 prompt 时一并参考。
- [图片生成](30-codex-cli-features.md#image-generation)：直接在 CLI 中生成或编辑图片；当你希望 Codex 基于现有素材迭代时，也可以附加参考图。
- [运行本地代码审查](30-codex-cli-features.md#running-local-code-review)：在提交或推送变更之前，让一个独立的 Codex agent 审查你的代码。
- [使用 subagents](68-subagents.md)：使用 subagents 并行处理复杂任务。
- [Web search](30-codex-cli-features.md#web-search)：让 Codex 搜索网页，为任务获取最新信息。
- [Codex Cloud 任务](30-codex-cli-features.md#working-with-codex-cloud)：无需离开终端即可启动 Codex Cloud 任务、选择环境并应用生成的 diff。
- [脚本化 Codex](60-non-interactive-mode.md)：使用 `exec` 命令编写脚本，自动化可重复工作流。
- [Model Context Protocol](53-model-context-protocol.md)：通过 Model Context Protocol（MCP）让 Codex 访问额外的第三方工具和上下文。
- [审批模式](30-codex-cli-features.md#approval-modes)：在 Codex 编辑或运行命令前，选择与你舒适度匹配的审批模式。
