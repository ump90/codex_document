### Slash commands in Codex CLI

Source: [Slash commands in Codex CLI](/codex/cli/slash-commands.md)

Slash commands give you fast, keyboard-first control over Codex. Type `/` in
the composer to open the slash popup, choose a command, and Codex will perform
actions such as switching models, adjusting permissions, or summarizing long
conversations without leaving the terminal.

This guide shows you how to:

- Find the right built-in slash command for a task
- Steer an active session with commands like `/model`, `/fast`,
  `/personality`, `/permissions`, `/approve`, `/raw`, `/agent`, and `/status`

#### Built-in slash commands

Codex ships with the following commands. Open the slash popup and start typing
the command name to filter the list.

When a task is already running, you can type a slash command and press `Tab` to
queue it for the next turn. Codex parses queued slash commands when they run, so
command menus and errors appear after the current turn finishes. Slash
completion still works before you queue the command.

| Command                                                                         | Purpose                                                         | When to use it                                                                                             |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| [`/permissions`](#update-permissions-with-permissions)                          | Set what Codex can do without asking first.                     | Relax or tighten approval requirements mid-session, such as switching between Auto and Read Only.          |
| [`/ide`](#include-ide-context-with-ide)                                         | Include open files, current selection, and other IDE context.   | Pull editor context into the next prompt without re-explaining what's open in your IDE.                    |
| [`/keymap`](#remap-tui-shortcuts-with-keymap)                                   | Remap TUI keyboard shortcuts.                                   | Inspect and persist custom shortcut bindings in `config.toml`.                                             |
| [`/vim`](#toggle-vim-mode-with-vim)                                             | Toggle Vim mode for the composer.                               | Switch between Vim normal/insert behavior and the default composer editing mode.                           |
| [`/sandbox-add-read-dir`](#grant-sandbox-read-access-with-sandbox-add-read-dir) | Grant sandbox read access to an extra directory (Windows only). | Unblock commands that need to read an absolute directory path outside the current readable roots.          |
| [`/agent`](#switch-agent-threads-with-agent)                                    | Switch the active agent thread.                                 | Inspect or continue work in a spawned subagent thread.                                                     |
| [`/apps`](#browse-apps-with-apps)                                               | Browse apps (connectors) and insert them into your prompt.      | Attach an app as `$app-slug` before asking Codex to use it.                                                |
| [`/plugins`](#browse-plugins-with-plugins)                                      | Browse installed and discoverable plugins.                      | Inspect plugin tools, install suggested plugins, or manage plugin availability.                            |
| [`/hooks`](#review-hooks-with-hooks)                                            | Review lifecycle hooks.                                         | Inspect configured hooks, trust new or changed hooks, or disable non-managed hooks before they run.        |
| [`/clear`](#clear-the-terminal-and-start-a-new-chat-with-clear)                 | Clear the terminal and start a fresh chat.                      | Reset the visible UI and conversation together when you want a fresh start.                                |
| [`/compact`](#keep-transcripts-lean-with-compact)                               | Summarize the visible conversation to free tokens.              | Use after long runs so Codex retains key points without blowing the context window.                        |
| [`/copy`](#copy-the-latest-response-with-copy)                                  | Copy the latest completed Codex output.                         | Grab the latest finished response or plan text without manually selecting it. You can also press `Ctrl+O`. |
| [`/diff`](#review-changes-with-diff)                                            | Show the Git diff, including files Git isn't tracking yet.      | Review Codex's edits before you commit or run tests.                                                       |
| [`/exit`](#exit-the-cli-with-quit-or-exit)                                      | Exit the CLI (same as `/quit`).                                 | Alternative spelling; both commands exit the session.                                                      |
| [`/experimental`](#toggle-experimental-features-with-experimental)              | Toggle experimental features.                                   | Enable optional features such as subagents from the CLI.                                                   |
| [`/approve`](#approve-an-auto-review-denial-with-approve)                       | Approve one retry of a recent auto review denial.               | Retry a command or action that the auto reviewer denied.                                                   |
| [`/memories`](#configure-memories-with-memories)                                | Configure memory use and generation.                            | Turn memory injection or memory generation on or off without leaving the TUI.                              |
| [`/skills`](#use-skills-with-skills)                                            | Browse and use skills.                                          | Improve task-specific behavior by selecting a relevant local skill.                                        |
| [`/hooks`](#view-lifecycle-hooks-with-hooks)                                    | View and manage lifecycle hooks.                                | Inspect hook configuration loaded into the current session.                                                |
| [`/feedback`](#send-feedback-with-feedback)                                     | Send logs to the Codex maintainers.                             | Report issues or share diagnostics with support.                                                           |
| [`/init`](#generate-agentsmd-with-init)                                         | Generate an `AGENTS.md` scaffold in the current directory.      | Capture persistent instructions for the repository or subdirectory you're working in.                      |
| [`/logout`](#sign-out-with-logout)                                              | Sign out of Codex.                                              | Clear local credentials when using a shared machine.                                                       |
| [`/mcp`](#list-mcp-tools-with-mcp)                                              | List configured Model Context Protocol (MCP) tools.             | Check which external tools Codex can call during the session; add `verbose` for server details.            |
| [`/mention`](#highlight-files-with-mention)                                     | Attach a file to the conversation.                              | Point Codex at specific files or folders you want it to inspect next.                                      |
| [`/model`](#set-the-active-model-with-model)                                    | Choose the active model (and reasoning effort, when available). | Switch between general-purpose models (`gpt-4.1-mini`) and deeper reasoning models before running a task.  |
| [`/fast`](#toggle-fast-mode-with-fast)                                          | Toggle a Fast service tier when the model catalog exposes one.  | Turn the current model's Fast tier on or off, or check whether the thread is using it.                     |
| [`/plan`](#switch-to-plan-mode-with-plan)                                       | Switch to plan mode and optionally send a prompt.               | Ask Codex to propose an execution plan before implementation work starts.                                  |
| [`/goal`](#set-or-view-a-task-goal-with-goal)                                   | Set, pause, resume, view, or clear a task goal.                 | Give Codex a persistent target to track while a larger task runs.                                          |
| [`/personality`](#set-a-communication-style-with-personality)                   | Choose a communication style for responses.                     | Make Codex more concise, more explanatory, or more collaborative without changing your instructions.       |
| [`/ps`](#check-background-terminals-with-ps)                                    | Show experimental background terminals and their recent output. | Check long-running commands without leaving the main transcript.                                           |
| [`/stop`](#stop-background-terminals-with-stop)                                 | Stop all background terminals.                                  | Cancel background terminal work started by the current session.                                            |
| [`/fork`](#fork-the-current-conversation-with-fork)                             | Fork the current conversation into a new thread.                | Branch the active session to explore a new approach without losing the current transcript.                 |
| [`/side`, `/btw`](#start-a-side-conversation-with-side)                         | Start an ephemeral side conversation.                           | Ask a focused follow-up without disrupting the main thread's transcript.                                   |
| [`/raw`](#toggle-raw-scrollback-with-raw)                                       | Toggle raw scrollback mode.                                     | Make terminal selection and copying less formatted while reviewing long output.                            |
| [`/resume`](#resume-a-saved-conversation-with-resume)                           | Resume a saved conversation from your session list.             | Continue work from a previous CLI session without starting over.                                           |
| [`/new`](#start-a-new-conversation-with-new)                                    | Start a new conversation inside the same CLI session.           | Reset the chat context without leaving the CLI when you want a fresh prompt in the same repo.              |
| [`/quit`](#exit-the-cli-with-quit-or-exit)                                      | Exit the CLI.                                                   | Leave the session immediately.                                                                             |
| [`/review`](#ask-for-a-working-tree-review-with-review)                         | Ask Codex to review your working tree.                          | Run after Codex completes work or when you want a second set of eyes on local changes.                     |
| [`/status`](#inspect-the-session-with-status)                                   | Display session configuration and token usage.                  | Confirm the active model, approval policy, writable roots, and remaining context capacity.                 |
| [`/debug-config`](#inspect-config-layers-with-debug-config)                     | Print config layer and requirements diagnostics.                | Debug precedence and policy requirements, including experimental network constraints.                      |
| [`/statusline`](#configure-footer-items-with-statusline)                        | Configure TUI status-line fields interactively.                 | Pick and reorder footer items (model/context/limits/git/tokens/session) and persist in config.toml.        |
| [`/title`](#configure-terminal-title-items-with-title)                          | Configure terminal window or tab title fields interactively.    | Pick and reorder title items such as project, status, thread, branch, model, and task progress.            |
| [`/theme`](#choose-a-syntax-theme-with-theme)                                   | Choose a syntax-highlighting theme.                             | Preview and persist a terminal syntax-highlighting theme.                                                  |

`/quit` and `/exit` both exit the CLI. Use them only after you have saved or
committed any important work.

Use `/permissions` to adjust what Codex can do without asking first. Use
`/approve` only when you need to retry a recent action that automatic review
denied.

#### Control your session with slash commands

The following workflows keep your session on track without restarting Codex.

#### Set the active model with `/model`

1. Start Codex and open the composer.
2. Type `/model` and press Enter.
3. Choose a model such as `gpt-4.1-mini` or `gpt-4.1` from the popup.

Expected: Codex confirms the new model in the transcript. Run `/status` to verify the change.

#### Toggle Fast mode with `/fast`

1. Type `/fast on`, `/fast off`, or `/fast status`.
2. If you want the setting to persist, confirm the update when Codex offers to save it.

Expected: Codex reports whether the current model's Fast service tier is on or
off for the current thread. In the TUI footer, you can also show a Fast mode
status-line item with `/statusline`.

Fast tier commands are catalog-driven. If the current model doesn't advertise a
Fast tier, Codex won't show `/fast`.

#### Set a communication style with `/personality`

Use `/personality` to change how Codex communicates without rewriting your prompt.

1. In an active conversation, type `/personality` and press Enter.
2. Choose a style from the popup.

Expected: Codex confirms the new style in the transcript and uses it for later
responses in the thread.

Codex supports `friendly`, `pragmatic`, and `none` personalities. Use `none`
to disable personality instructions.

If the active model doesn't support personality-specific instructions, Codex hides this command.

#### Switch to plan mode with `/plan`

1. Type `/plan` and press Enter to switch the active conversation into plan
   mode.
2. Optional: provide inline prompt text (for example, `/plan Propose a
migration plan for this service`).
3. You can paste content or attach images while using inline `/plan` arguments.

Expected: Codex enters plan mode and uses your optional inline prompt as the first planning request.

While a task is already running, `/plan` is temporarily unavailable.

#### Set or view a task goal with `/goal`

1. Type `/goal ` to set the goal, for example `/goal Finish the migration and keep tests green`.
2. Type `/goal` to view the current goal.
3. Use `/goal pause`, `/goal resume`, or `/goal clear` to pause, resume, or remove it.

Expected: Codex keeps the goal attached to the active thread while work continues.

Goal objectives must be non-empty and at most 4,000 characters. For longer
instructions, put the details in a file and point the goal at that file.

#### Toggle experimental features with `/experimental`

1. Type `/experimental` and press Enter.
2. Toggle the features you want (for example, Apps or Smart Approvals), then restart Codex if the prompt asks you to.

Expected: Codex saves your feature choices to config and applies them on restart.

#### Approve an auto review denial with `/approve`

Use `/approve` when the automatic reviewer denied a recent action and you want
Codex to retry it once.

1. Type `/approve`.
2. Confirm the retry when Codex shows the relevant denied action.

Expected: Codex retries that denied action once under the current session
policy.

#### Configure memories with `/memories`

1. Type `/memories`.
2. Choose whether Codex should use existing memories, generate new memories, or
   keep memory behavior disabled.

Expected: Codex updates the relevant memory settings for future sessions.

#### Use skills with `/skills`

1. Type `/skills`.
2. Pick the skill you want Codex to apply.

Expected: Codex inserts the selected skill context so the next request follows
that skill's instructions.

#### View lifecycle hooks with `/hooks`

1. Type `/hooks`.
2. Review the loaded lifecycle hook configuration.

Expected: Codex shows the hooks that can run in the current session.

#### Clear the terminal and start a new chat with `/clear`

1. Type `/clear` and press Enter.

Expected: Codex clears the terminal, resets the visible transcript, and starts
a fresh chat in the same CLI session.

Unlike Ctrl+L, `/clear` starts a new conversation.

Ctrl+L only clears the terminal view and keeps the current
chat. Codex disables both actions while a task is in progress.

#### Update permissions with `/permissions`

1. Type `/permissions` and press Enter.
2. Select the approval preset that matches your comfort level, for example
   `Auto` for hands-off runs or `Read Only` to review edits. When named
   permission profiles are active, the picker also shows configured custom
   profiles and their descriptions.

Expected: Codex announces the updated policy. Future actions respect the
updated approval mode until you change it again.

#### Include IDE context with `/ide`

1. Type `/ide`.
2. Add optional inline text if you want to explain what Codex should do with the
   current IDE selection or open files.

Expected: Codex includes available IDE context in the next prompt.

#### Toggle Vim mode with `/vim`

1. Type `/vim`.
2. Continue editing in the composer.

Expected: Codex toggles composer Vim mode for the current session. To make Vim
mode the default for new sessions, set `tui.vim_mode_default = true` in
`config.toml`.

