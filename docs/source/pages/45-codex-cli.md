### Codex CLI

Source: [Codex CLI](https://developers.openai.com/codex/cli.md)

Codex CLI is OpenAI's coding agent that you can run locally from your terminal. It can read, change, and run code on your machine in the selected directory.

It's [open source](https://github.com/openai/codex) and built in Rust for speed and efficiency.

ChatGPT Plus, Pro, Business, Edu, and Enterprise plans include Codex. Learn more about [what's included](https://developers.openai.com/codex/pricing).

[Watch the Codex CLI overview video](https://www.youtube.com/watch?v=iqNzfK4_meQ).

#### CLI setup

The official page renders these setup steps through an interactive component. This static snapshot preserves the same steps in Markdown.

##### Install

Install the Codex CLI with the standalone installer for macOS and Linux.

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

For unattended installs, set `CODEX_NON_INTERACTIVE=1` on the shell that runs the downloaded installer. See [Environment variables](https://developers.openai.com/codex/environment-variables#installer-variables) for details.

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | CODEX_NON_INTERACTIVE=1 sh
```

##### Run

Run Codex in a terminal. It can inspect your repository, edit files, and run commands.

```bash
codex
```

The first time you run Codex, you'll be prompted to sign in. Authenticate with your ChatGPT account or an API key.

See the [pricing page](https://developers.openai.com/codex/pricing) if you're not sure which plans include Codex access.

##### Upgrade

New versions of the Codex CLI are released regularly. See the changelog for release notes. To upgrade a standalone install, rerun the installer:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

The Codex CLI is available on macOS, Windows, and Linux. On Windows, run Codex natively in PowerShell with the Windows sandbox, or use WSL2 when you need a Linux-native environment. For setup details, see the [Windows setup guide](https://developers.openai.com/codex/windows).

If you're new to Codex, read the [best practices guide](https://developers.openai.com/codex/learn/best-practices).

---

#### Work with the Codex CLI

- [Run Codex interactively](https://developers.openai.com/codex/cli/features#running-in-interactive-mode): run `codex` to start an interactive terminal UI (TUI) session.
- [Control model and reasoning](https://developers.openai.com/codex/cli/features#models-and-reasoning): use `/model` to switch between GPT-5.4, GPT-5.3-Codex, and other available models, or adjust reasoning levels.
- [Image inputs](https://developers.openai.com/codex/cli/features#image-inputs): attach screenshots or design specs so Codex reads them alongside your prompt.
- [Image generation](https://developers.openai.com/codex/cli/features#image-generation): generate or edit images directly in the CLI, and attach references when you want Codex to iterate on an existing asset.
- [Run local code review](https://developers.openai.com/codex/cli/features#running-local-code-review): get your code reviewed by a separate Codex agent before you commit or push your changes.
- [Use subagents](https://developers.openai.com/codex/subagents): use subagents to parallelize complex tasks.
- [Web search](https://developers.openai.com/codex/cli/features#web-search): use Codex to search the web and get up-to-date information for your task.
- [Codex Cloud tasks](https://developers.openai.com/codex/cli/features#working-with-codex-cloud): launch a Codex Cloud task, choose environments, and apply the resulting diffs without leaving your terminal.
- [Scripting Codex](https://developers.openai.com/codex/noninteractive): automate repeatable workflows by scripting Codex with the `exec` command.
- [Model Context Protocol](https://developers.openai.com/codex/mcp): give Codex access to additional third-party tools and context with Model Context Protocol (MCP).
- [Approval modes](https://developers.openai.com/codex/cli/features#approval-modes): choose the approval mode that matches your comfort level before Codex edits or runs commands.
