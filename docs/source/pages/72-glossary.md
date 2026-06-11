### Glossary

Source: [Glossary](/codex/glossary.md)

Use this glossary as a quick reference for Codex terms across the app, CLI, IDE extension, cloud, SDK, and related integrations.

| Term | Applies to | Definition |
| --- | --- | --- |
| [Agent](/codex) | App, CLI, IDE extension, Cloud | The Codex worker that reasons over context, uses tools, and completes a task. |
| [AGENTS.md](/codex/guides/agents-md) | App, CLI, IDE extension, Cloud | Repository or user guidance file that gives Codex persistent instructions. |
| [Analytics dashboard](/codex/enterprise/governance#analytics-dashboard) | Enterprise | Admin view for Codex usage, adoption, and code review metrics. |
| [API key sign-in](/codex/auth#sign-in-with-an-api-key) | App, CLI, IDE extension | Authentication using an OpenAI API key. |
| [Approval policy](/codex/agent-approvals-security#sandbox-and-approvals) | App, CLI, IDE extension | Rules for when Codex must ask before taking an action. |
| [Approval request](/codex/agent-approvals-security#automatic-approval-reviews) | App, CLI, IDE extension | Codex asking to allow a restricted action. |
| [Apps (connectors)](/codex/plugins) | App, CLI, IDE extension | Integration that lets Codex access external services. Available through plugins; also called connectors. |
| [Appshot](/codex/appshots) | App | Snapshot of the frontmost app window sent to a Codex thread. |
| [Auth cache](/codex/auth#login-caching) | App, CLI, IDE extension | Locally stored login credentials reused by Codex. |
| [Automatic approval review](/codex/agent-approvals-security#automatic-approval-reviews) | App, CLI, IDE extension | Model-based review of eligible approval requests before they proceed. |
| [Automation](/codex/app/automations) | App | A scheduled or recurring Codex task. |
| [Automation run](/codex/app/automations#managing-tasks) | App | One execution of a scheduled automation that may report findings or archive itself. |
| [Browser use](/codex/app/browser#browser-use) | App | App capability that lets Codex operate the in-app browser directly. |
| [Chat](/codex/app/features#chats) | App | A Codex conversation not tied to a project. |
| [ChatGPT sign-in](/codex/auth#sign-in-with-chatgpt) | App, CLI, IDE extension, Cloud | Authentication using a ChatGPT account and workspace permissions. |
| [Chronicle](/codex/memories/chronicle) | App | Opt-in feature that builds memories from recent screen context. |
| [Cloud](/codex/cloud) | App, IDE extension, Web | Mode where Codex works remotely in an OpenAI-managed environment. |
| [Cloud environment](/codex/cloud/environments) | Cloud | Configured container setup used for Codex cloud tasks. |
| [Cloud task](/codex/cloud/environments#how-codex-cloud-tasks-run) | Cloud | A remotely executed Codex task that runs in a cloud environment. |
| [Cloud thread](/codex/prompting#threads) | Cloud | A thread that runs in a Codex cloud environment. |
| [Codex](/codex) | App, CLI, IDE extension, Web, Cloud, SDK | OpenAI's coding agent for software development tasks. |
| [Codex app](/codex/app) | Desktop | Desktop app for running Codex threads in parallel, with built-in worktree support, automations, and Git functionality. |
| [Codex app-server](/codex/app-server) | App, IDE extension, SDK | Local JSON-RPC server for embedding Codex threads, turns, approvals, history, and streamed events in custom clients. |
| [Codex CLI](/codex/cli) | Terminal | Terminal client for running Codex interactively or in scripts. |
| [Codex cloud](/codex/cloud) | Web, App, IDE extension | OpenAI-managed execution environment where Codex can work on repository tasks remotely. |
| [codex exec](/codex/noninteractive) | CLI | CLI command for running Codex non-interactively from scripts or CI. |
| [Codex IDE extension](/codex/ide) | IDE | Editor integration for using Codex inside IDEs like VS Code, JetBrains IDEs, Cursor, and Windsurf. |
| [Codex SDK](/codex/sdk) | SDK | Programmatic interface for building Codex-powered workflows or integrations. |
| [Codex web](/codex/cloud) | Browser | Browser-based Codex surface for delegating cloud tasks. |
| [Codex-managed worktree](/codex/app/worktrees#codex-managed-and-permanent-worktrees) | App | A temporary worktree Codex creates and manages for a thread. |
| [Compaction](/codex/prompting#context) | App, CLI, IDE extension, Cloud | Summarizing older context so long-running work can continue. |
| [Compliance API](/codex/enterprise/governance#compliance-api) | Enterprise | API for exporting Codex activity and audit metadata. |
| [Computer use](/codex/app/computer-use) | App | App capability that lets Codex interact with desktop applications through the UI. |
| [config.toml](/codex/config-reference#configtoml) | App, CLI, IDE extension | Local Codex configuration files. |
| [Connected host](/codex/remote-connections#what-comes-from-the-connected-host) | App, Mobile | Computer or development environment that provides files, tools, and shell access for remote Codex work. |
| [Connector](/codex/plugins) | App, Cloud | App integration that lets Codex access external services. Available through plugins; also called apps. |
| [Container cache](/codex/cloud/environments#container-caching) | Cloud | Saved cloud container state reused to speed up future tasks. |
| [Context](/codex/prompting#context) | App, CLI, IDE extension, Cloud, SDK | Information Codex can use while working, such as files, prior messages, tool output, and instructions. |
| [Context window](/api/docs/guides/conversation-state#managing-the-context-window) | App, CLI, IDE extension, Cloud, SDK | The maximum amount of information the model can consider at once. |
| [Custom agent](/codex/subagents#custom-agents) | App, CLI | User-defined agent role with its own instructions and settings. |
| [Deny-read rule](/codex/permissions#deny-reads-with-exact-paths-or-globs) | App, CLI, IDE extension, Enterprise | Filesystem permission rule that prevents Codex from reading sensitive paths or glob matches. |
| [Diff](/codex/app/review#what-changes-it-shows) | App, Git, Review | Set of Git file changes shown for inspection, comments, staging, or reverting. |
| [Domain allowlist](/codex/cloud/internet-access#domain-allowlist) | Cloud | Set of domains Codex cloud can reach when agent internet access is enabled. |
| [Environment (local)](/codex/app/local-environments) | App, Worktree | App configuration to tell Codex how to set up worktrees for a project. |
| [Environment variable](/codex/cloud/environments#environment-variables-and-secrets) | Cloud, CLI, IDE extension | Runtime configuration value available during task execution. |
| [Ephemeral session](/codex/noninteractive#basic-usage) | CLI | Non-interactive run that skips saving session state after it completes. |
| [Fast mode](/codex/speed#fast-mode) | CLI, IDE extension | Speed setting that makes supported models respond faster at a higher credit cost. |
| [Filesystem permission](/codex/permissions#filesystem-permissions) | App, CLI, IDE extension | Permission profile rule that grants or denies read and write access to paths. |
| [Finding](/codex/app/automations#managing-tasks) | App | A notable result or issue surfaced by an automation. |
| [Full access](/codex/concepts/sandboxing#configure-defaults) | App, CLI, IDE extension | Mode where Codex runs without normal sandbox restrictions. |
| [Git worktree](/codex/app/worktrees#whats-a-worktree) | App, Git | A second checkout of the same repository for parallel branch work. |
| [Handoff](/codex/app/worktrees#working-between-local-and-worktree) | App | Moving a thread and its work between Local and Worktree. |
| [Heartbeat](/codex/app/automations#thread-automations) | App | A recurring thread wake-up that returns Codex to the same conversation on a schedule. Also called a thread automation. |
| [Hook](/codex/hooks) | App, CLI, IDE extension | A lifecycle handler that runs when a Codex event matches, such as tool use, permission requests, or when a turn stops. |
| [Hook event](/codex/hooks#config-shape) | App, CLI, IDE extension | Lifecycle point where configured hook handlers can run. |
| [Hunk](/codex/app/review#staging-and-reverting-files) | App, Git, Review | Contiguous section of a diff that can be staged, unstaged, or reverted independently. |
| [Inline comment](/codex/app/review#inline-comments-for-feedback) | App | Line-specific feedback attached to a diff. |
| [Live web search](/codex/config-basic#web-search-mode) | App, CLI, IDE extension | Real-time web lookup for current information. |
| [Local](/codex/app/worktrees#working-between-local-and-worktree) | App, CLI, IDE extension | Mode where Codex works on the user's computer. |
| [Local thread](/codex/prompting#threads) | App, CLI, IDE extension | A thread that runs on the user's machine. |
| [Maintenance script](/codex/cloud/environments#container-caching) | Cloud | Optional script run when a cached cloud container resumes. |
| [Managed configuration](/codex/enterprise/managed-configuration) | Enterprise | Organization-controlled Codex defaults and restrictions. |
| [MCP](/codex/mcp) | App, CLI, IDE extension | Model Context Protocol, a standard for connecting Codex to external tools and context. |
| [MCP resource](/codex/mcp#supported-mcp-features) | App, CLI, IDE extension | Readable context exposed by an MCP server for Codex to inspect. |
| [MCP server](/codex/mcp#supported-mcp-features) | App, CLI, IDE extension | External tool or context provider exposed through MCP. |
| [MCP tool](/codex/mcp#supported-mcp-features) | App, CLI, IDE extension | Action exposed by an MCP server that Codex can call during a task. |
| [MDM](/codex/enterprise/managed-configuration#macos-managed-preferences-mdm) | Enterprise | Mobile device management tooling for distributing device profiles and managed Codex settings. |
| [Memories](/codex/memories) | App, CLI, IDE extension | Locally stored context Codex can reuse across sessions. |
| [Model](/codex/models) | App, CLI, IDE extension, Cloud, SDK | The AI model Codex uses for reasoning and tool work. |
| [Network access](/codex/agent-approvals-security#network-access-) | App, CLI, IDE extension, Cloud | Permission for commands or environments to reach the internet. |
| [Network policy](/codex/agent-approvals-security#network-policy) | App, CLI, IDE extension | Domain-based allow and deny rules that constrain sandboxed outbound network traffic. |
| [Non-interactive mode](/codex/noninteractive) | CLI | CLI mode for running Codex from scripts or CI. |
| [Output schema](/codex/noninteractive#create-structured-outputs-with-a-schema) | CLI | JSON Schema passed to `codex exec` to constrain the final response. |
| [Permanent worktree](/codex/app/worktrees#codex-managed-and-permanent-worktrees) | App | A long-lived worktree kept as its own project. |
| [Permission profile](/codex/permissions#define-and-select-a-profile) | App, CLI, IDE extension | Named least-privilege policy that combines filesystem and network rules for local command execution. |
| [Plan](/codex/learn/best-practices#plan-first-for-difficult-tasks) | App, CLI, IDE extension, Cloud | Codex's proposed or tracked steps for completing a task. |
| [Plugin](/codex/plugins) | App, CLI, IDE extension | Installable bundle that can distribute skills, tools, and integrations. |
| [Plugin manifest](/codex/plugins/build#plugin-structure) | App, CLI, IDE extension, Plugins | Plugin metadata file that identifies a plugin and points to bundled skills, apps, MCP servers, hooks, and metadata. |
| [Prefix rule](/codex/rules#understand-the-rules-language) | App, CLI, IDE extension, Enterprise | Command-rule pattern that allows, prompts for, or forbids matching command prefixes. |
| [Profile](/codex/config-advanced#profiles) | CLI, IDE extension | Named configuration preset for Codex. |
| [Progressive disclosure](/codex/skills) | App, CLI, IDE extension | Loading skill details only when needed to preserve context. |
| [Project](/codex/app/features#multitask-across-projects) | App | A selected codebase or folder Codex works in. |
| [Prompt](/codex/prompting) | App, CLI, IDE extension, Cloud, SDK | The user instruction or request sent to Codex. |
| [Pull request review](/codex/app/review#pull-request-reviews) | App, CLI, GitHub | Codex review of changes or feedback on a pull request. |
| [RBAC](/codex/enterprise/admin-setup#step-2-set-up-custom-roles-rbac) | Enterprise | Role-based access control for workspace permissions. |
| [Read-only mode](/codex/concepts/sandboxing) | App, CLI, IDE extension | Mode where Codex can inspect but not modify without approval. |
| [Reasoning effort](/codex/config-basic#reasoning-effort) | App, CLI, IDE extension, SDK | Setting that controls how much reasoning budget a model uses. |
| [Remote connection](/codex/remote-connections) | App, Mobile | Connection that lets Codex work from another device using a connected host. |
| [requirements.toml](/codex/config-reference#requirementstoml) | Enterprise | Admin-enforced requirements file for managed Codex setups. |
| [Review pane](/codex/app/review) | App | App view for inspecting diffs, comments, and Git changes. |
| [Rules](/codex/rules) | App, CLI, IDE extension | Policies that allow, prompt for, or deny command prefixes or permission exceptions. |
| [Sandbox](/codex/concepts/sandboxing) | App, CLI, IDE extension | Enforced boundary limiting what Codex commands can access or modify. |
| [Sandbox mode](/codex/config-basic#sandbox-level) | App, CLI, IDE extension | Configuration that defines Codex's filesystem and network limits. |
| [Sandbox preset](/codex/sdk#sandbox-presets) | SDK | SDK shorthand for common sandbox policies such as read-only, workspace-write, or full access. |
| [Schedule](/codex/app/automations) | App | The timing rule for an automation. |
| [Secret](/codex/cloud/environments#environment-variables-and-secrets) | Cloud | Encrypted value available to setup scripts but removed before the agent phase. |
| [Setup script](/codex/app/local-environments#setup-scripts) | App worktrees | Script run before the agent starts to install dependencies or prepare tools. |
| [Skill](/codex/skills) | App, CLI, IDE extension | Reusable workflow package with instructions and optional scripts or references. |
| [Skill invocation](/codex/skills#how-codex-uses-skills) | App, CLI, IDE extension | Explicit or implicit activation of a skill. |
| [Slash command](/codex/cli/slash-commands) | CLI | Command entered with a leading slash to control or inspect a Codex CLI session. |
| [Standalone automation](/codex/app/automations) | App | Independent scheduled run that reports separate findings. |
| [STDIO MCP server](/codex/mcp#stdio-servers) | CLI, IDE extension | MCP server launched as a local process by a configured command and arguments. |
| [Streamable HTTP MCP server](/codex/mcp#streamable-http-servers) | CLI, IDE extension | MCP server reached over HTTP, optionally with bearer token or OAuth authentication. |
| [Subagent](/codex/concepts/subagents) | App, CLI | Specialized child agent spawned to work on part of a task. |
| [Subagent workflow](/codex/concepts/subagents#core-terms) | App, CLI | Workflow where Codex runs delegated agents in parallel and combines their results. |
| [Task](/codex/app/automations#managing-tasks) | App, CLI, IDE extension, Cloud, SDK | The unit of work Codex is asked to complete. |
| [Thread](/codex/prompting#threads) | App, CLI, IDE extension, Cloud, SDK | A single Codex session containing prompts, model output, and tool activity. |
| [Thread automation](/codex/app/automations#thread-automations) | App | Recurring wake-up attached to an existing thread. Also called a heartbeat. |
| [Thread fork](/codex/app-server#start-or-resume-a-thread) | App-server, SDK | New thread branched from the stored history of an existing thread. |
| [Turn](/codex/app-server#core-primitives) | App, CLI, IDE extension, Cloud, SDK | One exchange in a thread, usually a user prompt plus Codex's response and actions. |
| [Universal image](/codex/cloud/environments#default-universal-image) | Cloud | Default Codex cloud container image with common tools preinstalled. |
| [Web search cache](/codex/config-basic#web-search-mode) | App, CLI, IDE extension | Pre-indexed search results Codex can use without live browsing. |
| [Worktree](/codex/app/worktrees) | App | Mode where Codex isolates changes in a separate Git worktree. |
| [Writable roots](/codex/agent-approvals-security#protected-paths-in-writable-roots) | App, CLI, IDE extension | Directories Codex is allowed to modify. |
