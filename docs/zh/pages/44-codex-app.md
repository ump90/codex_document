### Codex 应用

Source: [Codex app](https://developers.openai.com/codex/app.md)

Codex app 是一个专注的桌面体验，用于并行处理 Codex 线程，内置 worktree 支持、自动化和 Git 功能。

ChatGPT Plus、Pro、Business、Edu 和 Enterprise 计划包含 Codex。请查看[包含哪些内容](02-codex-pricing.md)了解更多。

![显示项目侧边栏、活动线程和审查面板的 Codex app 窗口](https://developers.openai.com/images/codex/app/app-screenshot-light.webp)

![Windows 版 Codex app，显示项目侧边栏、活动线程和审查面板](https://developers.openai.com/images/codex/windows/codex-windows-light.webp)

#### 开始使用

Codex app 可在 macOS 和 Windows 上使用。

大多数 Codex app 功能在两个平台上都可用。相关文档会说明特定平台的例外情况。

1. 下载并安装 Codex app。

   下载适用于 macOS 或 Windows 的 Codex app。如果你使用的是 Intel 芯片的 Mac，请选择 Intel 构建版本。Linux 用户可以[登记以便在 app 可用时收到通知](https://openai.com/form/codex-app/)。

2. 打开 Codex 并登录。

   下载并安装 Codex app 后，打开它并使用你的 ChatGPT 账户或 OpenAI API key 登录。

   如果使用 OpenAI API key 登录，[某些功能可能不可用](02-codex-pricing.md#feature-availability)。

3. 选择项目。

   选择一个你希望 Codex 在其中工作的项目文件夹。

   如果你之前使用过 Codex app、CLI 或 IDE Extension，会看到过去处理过的项目。

4. 发送第一条消息。

   选择项目后，确保选择 **Local**，让 Codex 在你的机器上工作，然后向 Codex 发送第一条消息。

   你可以向 Codex 询问有关该项目或你的电脑的一般问题。例如，可以尝试下面的首次消息提示。

如果需要更多灵感，请浏览 [Codex 使用场景](97-use-cases.md)。如果你刚开始使用 Codex，请阅读[最佳实践指南](05-best-practices.md)。

#### 首次消息提示

官方 app 页面包含示例任务卡片。下面用普通 Markdown 保留这些卡片中的 prompt 文本，方便复制。

##### Tell me about this project

```text
Tell me about this project
```

##### Build a classic Snake game in this repo

```text
Build a classic Snake game in this repo.

Scope & constraints:
- Implement ONLY the classic Snake loop: grid movement, growing snake, food spawn, score, game-over, restart.
- Reuse existing project tooling/frameworks; do NOT add new dependencies unless truly required.
- Keep UI minimal and consistent with the repo's existing styles (no new design systems, no extra animations).

Implementation plan:
1) Inspect the repo to find the right place to add a small interactive game (existing pages/routes/components).
2) Implement game state (snake positions, direction, food, score, tick timer) with deterministic, testable logic.
3) Render: simple grid + snake + food; support keyboard controls (arrow keys/WASD) and on-screen controls if mobile is present in the repo.
4) Add basic tests for the core game logic (movement, collisions, growth, food placement) if the repo has a test runner.

Deliverables:
- A small set of files/changes with clear names.
- Short run instructions (how to start dev server + where to navigate).
- A brief checklist of what to manually verify (controls, pause/restart, boundaries).
```

##### Find and fix bugs in my codebase

```text
Find and fix bugs in my codebase with minimal, high-confidence changes.

Method (grounded + disciplined):
1) Reproduce: run tests/lint/build (or follow the existing repo scripts). If I provided an error, reproduce that exact failure.
2) Localize: identify the smallest set of files/lines involved (stack traces, failing tests, logs).
3) Fix: implement the minimal change that resolves the issue without refactors or unrelated cleanup.
4) Prove: add/update a focused test (or a tight repro) that fails before and passes after.

Constraints:
- Do NOT invent errors or pretend to run commands you cannot run.
- No scope drift: no new features, no UI embellishments, no style overhauls.
- If information is missing, state what you can confirm from the repo and what remains unknown.

Output:
- Summary (3-6 sentences max): what was broken, why, and the fix.
- Then <=5 bullets: What changed, Where (paths), Evidence (tests/logs), Risks, Next steps.
```

---

#### 使用 Codex app 工作

- [跨项目多任务](27-codex-app-features.md#multitask-across-projects)：并排运行项目线程，并在它们之间快速切换。
- [Worktrees](42-worktrees.md)：使用内置 Git worktree 支持，让并行代码变更保持隔离。
- [远程连接](79-remote-connections.md)：使用 ChatGPT mobile app 在已连接主机上启动、引导、审批并审查 Codex 工作。
- [Computer use](35-computer-use.md)：让 Codex 使用 macOS app 完成 GUI 任务、浏览器流程和原生 app 测试。
- [Appshots](43-appshots.md)：把最前方的 Mac app 窗口连同截图和可用文本发送给 Codex。
- [审查并发布变更](38-review.md)：检查 diff、处理 PR 反馈、暂存文件、提交并推送。
- [终端和 actions](27-codex-app-features.md#integrated-terminal)：在每个线程中运行命令，并启动可重复的项目 actions。
- [In-app browser](36-in-app-browser.md)：打开渲染后的页面、留下评论，或让 Codex 操作本地浏览器流程。
- [Chrome extension](29-codex-chrome-extension.md)：添加 Chrome plugin，让 Codex 可以使用 Chrome 执行已登录的浏览器任务，同时由你管理网站审批。
- [图片生成](27-codex-app-features.md#image-generation)：在线程中生成或编辑图片，同时处理周边代码和素材。
- [自动化](24-automations.md)：排定 recurring tasks，或唤醒同一线程进行持续检查。
- [Skills](27-codex-app-features.md#skills-support)：在 app、CLI 和 IDE Extension 中复用说明和工作流。
- [侧边栏和 artifacts](27-codex-app-features.md#richer-outputs-and-artifacts)：跟踪计划、来源、任务摘要和生成文件预览。
- [Plugins](78-plugins.md)：连接 apps、skills 和 MCP servers，扩展 Codex 能做的事。
- [Sites](80-sites.md)：使用 Sites plugin 构建和部署托管网站、web apps 和游戏。
- [IDE Extension sync](27-codex-app-features.md#sync-with-the-ide-extension)：在 app 和 IDE 会话之间共享 Auto Context 和活动线程。

需要帮助？请访问[故障排除指南](40-troubleshooting.md)。
