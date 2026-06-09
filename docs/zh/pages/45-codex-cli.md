### Codex CLI

Source: [Codex CLI](https://developers.openai.com/codex/cli.md)

Codex CLI 是 OpenAI 的编程代理，你可以在本地终端中运行它。它可以在所选目录中读取、修改并运行你机器上的代码。
它是[开源的](https://github.com/openai/codex)，并使用 Rust 构建，以获得速度和效率。

ChatGPT Plus、Pro、Business、Edu 和 Enterprise 计划包含 Codex。了解更多关于[包含内容](02-codex-pricing.md)的信息。

#### CLI 设置

Codex CLI 可在 macOS、Windows 和 Linux 上使用。在 Windows 上，可以在 PowerShell 中配合 Windows 沙箱原生运行 Codex；当你需要 Linux 原生环境时，也可以使用 WSL2。有关设置详情，请参阅 Windows 设置指南。

---

#### 使用 Codex CLI 工作

#### 运行本地代码审查

在提交或推送变更之前，让一个独立的 Codex 代理审查你的代码。
