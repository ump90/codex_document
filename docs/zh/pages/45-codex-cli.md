---
title: Codex CLI
---

## CLI setup { .codex-visually-hidden }

<div class="codex-step-card" markdown="1">
<div class="codex-step-heading"><span class="codex-step-number">1</span><h3>Install</h3></div>

使用 macOS 和 Linux 的独立安装器安装 Codex CLI。

```text
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

对于无人值守安装，请在运行已下载安装器的 shell 中设置 `CODEX_NON_INTERACTIVE=1`。详情请参阅 [环境变量](62-environment-variables.md)。

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

如果不确定哪些计划包含 Codex 访问权限，请查看 [定价页面](02-codex-pricing.md)。
</div>

<div class="codex-step-card" markdown="1">
<div class="codex-step-heading"><span class="codex-step-number">3</span><h3>Upgrade</h3></div>

Codex CLI 会定期发布新版本。请查看 [更新日志](88-changelog.md) 了解发布说明。要升级独立安装版本，请重新运行安装器：

```text
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```
</div>

<div class="codex-info-card" markdown="1">
<span class="codex-info-icon">i</span>

Codex CLI 可在 macOS、Windows 和 Linux 上使用。在 Windows 上，可以在 PowerShell 中配合 Windows 沙箱原生运行 Codex；当你需要 Linux 原生环境时，也可以使用 WSL2。设置详情请参阅 [Windows 设置指南](41-windows-app.md)。
</div>

---

## Work with the Codex CLI

### 运行本地代码审查

在提交或推送变更之前，让一个独立的 Codex 代理审查你的代码。
