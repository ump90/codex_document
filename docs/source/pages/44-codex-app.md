### Codex app

Source: [Codex app](https://developers.openai.com/codex/app.md)

The Codex app is a focused desktop experience for working on Codex threads in parallel, with built-in worktree support, automations, and Git functionality.

ChatGPT Plus, Pro, Business, Edu, and Enterprise plans include Codex. Learn more about [what's included](https://developers.openai.com/codex/pricing).

![Codex app window with a project sidebar, active thread, and review pane](https://developers.openai.com/images/codex/app/app-screenshot-light.webp)

![Codex app for Windows showing a project sidebar, active thread, and review pane](https://developers.openai.com/images/codex/windows/codex-windows-light.webp)

#### Getting started

The Codex app is available on macOS and Windows.

Most Codex app features are available on both platforms. The relevant docs describe platform-specific exceptions.

1. Download and install the Codex app.

   Download the Codex app for macOS or Windows. Choose the Intel build if you're using an Intel-based Mac. Linux users can [get notified when the app is available](https://openai.com/form/codex-app/).

2. Open Codex and sign in.

   Once you downloaded and installed the Codex app, open it and sign in with your ChatGPT account or an OpenAI API key.

   If you sign in with an OpenAI API key, [some functionality might not be available](https://developers.openai.com/codex/pricing#feature-availability).

3. Select a project.

   Choose a project folder that you want Codex to work in.

   If you used the Codex app, CLI, or IDE Extension before you'll see past projects that you worked on.

4. Send your first message.

   After choosing the project, make sure **Local** is selected to have Codex work on your machine and send your first message to Codex.

   You can ask Codex anything about the project or your computer in general. For example, try one of the first-message prompts below.

If you need more inspiration, explore [Codex use cases](https://developers.openai.com/codex/use-cases). If you're new to Codex, read the [best practices guide](https://developers.openai.com/codex/learn/best-practices).

#### First-message prompts

The official app page includes example task cards. The prompts below preserve their text in plain Markdown.

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

#### Work with the Codex app

- [Multitask across projects](https://developers.openai.com/codex/app/features#multitask-across-projects): run project threads side by side and switch between them quickly.
- [Worktrees](https://developers.openai.com/codex/app/worktrees): keep parallel code changes isolated with built-in Git worktree support.
- [Remote connections](https://developers.openai.com/codex/remote-connections): use the ChatGPT mobile app to start, steer, approve, and review Codex work on a connected host.
- [Computer use](https://developers.openai.com/codex/app/computer-use): let Codex use macOS apps for GUI tasks, browser flows, and native app testing.
- [Appshots](https://developers.openai.com/codex/appshots): send the frontmost Mac app window to Codex with a screenshot and available text.
- [Review and ship changes](https://developers.openai.com/codex/app/review): inspect diffs, address PR feedback, stage files, commit, and push.
- [Terminal and actions](https://developers.openai.com/codex/app/features#integrated-terminal): run commands in each thread and launch repeatable project actions.
- [In-app browser](https://developers.openai.com/codex/app/browser): open rendered pages, leave comments, or let Codex operate local browser flows.
- [Chrome extension](https://developers.openai.com/codex/app/chrome-extension): add the Chrome plugin so Codex can use Chrome for signed-in browser tasks while you manage website approvals.
- [Image generation](https://developers.openai.com/codex/app/features#image-generation): generate or edit images in a thread while you work on the surrounding code and assets.
- [Automations](https://developers.openai.com/codex/app/automations): schedule recurring tasks, or wake up the same thread for ongoing checks.
- [Skills](https://developers.openai.com/codex/app/features#skills-support): reuse instructions and workflows across the app, CLI, and IDE Extension.
- [Sidebar and artifacts](https://developers.openai.com/codex/app/features#richer-outputs-and-artifacts): follow plans, sources, task summaries, and generated file previews.
- [Plugins](https://developers.openai.com/codex/plugins): connect apps, skills, and MCP servers to extend what Codex can do.
- [Sites](https://developers.openai.com/codex/sites): build and deploy hosted websites, web apps, and games with the Sites plugin.
- [IDE Extension sync](https://developers.openai.com/codex/app/features#sync-with-the-ide-extension): share Auto Context and active threads across app and IDE sessions.

Need help? Visit the [troubleshooting guide](https://developers.openai.com/codex/app/troubleshooting).
