### Best practices

Source: [Best practices](/codex/learn/best-practices.md)

If you’re new to Codex or coding agents in general, this guide will help you get better results faster. It covers the core habits that make Codex more effective across the [CLI](/codex/cli), [IDE extension](/codex/ide), and the [Codex app](/codex/app), from prompting and planning to validation, MCP, skills, and automations.

Codex works best when you treat it less like a one-off assistant and more like a teammate you configure and improve over time.

A useful way to think about this: start with the right task context, use `AGENTS.md` for durable guidance, configure Codex to match your workflow, connect external systems with MCP, turn repeated work into skills, and automate stable workflows.

#### Strong first use: Context and prompts

Codex is already strong enough to be useful even when your prompt isn't perfect. You can often hand it a hard problem with minimal setup and still get a strong result. Clear [prompting](/codex/prompting) isn't required to get value, but it does make results more reliable, especially in larger codebases or higher-stakes tasks.

If you work in a large or complex repository, the biggest unlock is giving Codex the right task context and a clear structure for what you want done.

A good default is to include four things in your prompt:

- **Goal:** What are you trying to change or build?
- **Context:** Which files, folders, docs, examples, or errors matter for this task? You can @ mention certain files as context.
- **Constraints:** What standards, architecture, safety requirements, or conventions should Codex follow?
- **Done when:** What should be true before the task is complete, such as tests passing, behavior changing, or a bug no longer reproducing?

This helps Codex stay scoped, make fewer assumptions, and produce work that's easier to review.

Choose a reasoning level based on how hard the task is and test what works best for your workflow. Different users and tasks work best with different settings.

- Low for faster, well-scoped tasks
- Medium or High for more complex changes or debugging
- Extra High for long, agentic, reasoning-heavy tasks

To provide context faster, try using speech dictation inside the Codex app to
dictate what you want Codex to do rather than typing it.

#### Plan first for difficult tasks

If the task is complex, ambiguous, or hard to describe well, ask Codex to plan before it starts coding.

A few approaches work well:

**Use Plan mode:** For most users, this is the easiest and most effective option. Plan mode lets Codex gather context, ask clarifying questions, and build a stronger plan before implementation. Toggle with `/plan` or Shift+Tab.

**Ask Codex to interview you:** If you have a rough idea of what you want but aren't sure how to describe it well, ask Codex to question you first. Tell it to challenge your assumptions and turn the fuzzy idea into something concrete before writing code.

**Use a PLANS.md template:** For more advanced workflows, you can configure Codex to follow a `PLANS.md` or execution-plan template for longer-running or multi-step work. For more detail, see the [execution plans guide](/cookbook/articles/codex_exec_plans).

#### Make guidance reusable with `AGENTS.md`

Once a prompting pattern works, the next step is to stop repeating it manually. That's where [AGENTS.md](/codex/guides/agents-md) comes in.

Think of `AGENTS.md` as an open-format README for agents. It loads into context automatically and is the best place to encode how you and your team want Codex to work in a repository.

A good `AGENTS.md` covers:

- repo layout and important directories
- How to run the project
- Build, test, and lint commands
- Engineering conventions and PR expectations
- Constraints and do-not rules
- What done means and how to verify work

The `/init` slash command in the CLI is the quick-start command to scaffold a starter `AGENTS.md` in the current directory. It's a great starting point, but you should edit the result to match how your team actually builds, tests, reviews, and ships code.

You can create `AGENTS.md` files at different levels: a global `AGENTS.md` for personal defaults that sits in `~/.codex`, a repo-level file for shared standards, and more specific files in subdirectories for local rules. If there’s a more specific file closer to your current directory, that guidance wins.

Keep it practical. A short, accurate `AGENTS.md` is more useful than a long file full of vague rules. Start with the basics, then add new rules only after you notice repeated mistakes.

If `AGENTS.md` starts getting too large, keep the main file concise and reference task-specific markdown files for things like planning, code review, or architecture.

When Codex makes the same mistake twice, ask it for a retrospective and update
`AGENTS.md`. Guidance stays practical and based on real friction.

#### Configure Codex for consistency

Configuration is one of the main ways to make Codex behave more consistently across sessions and surfaces. For example, you can set defaults for model choice, reasoning effort, sandbox mode, approval policy, profiles, and MCP setup.

A good starting pattern is:

- Keep personal defaults in `~/.codex/config.toml` (Settings → Configuration → Open config.toml from the Codex app)
- Keep repo-specific behavior in `.codex/config.toml`
- Use command-line overrides only for one-off situations (if you use the CLI)

[`config.toml`](/codex/config-basic) is where you define durable preferences such as MCP servers, multi-agent setup, and feature flags. Profile-specific overrides live in separate `$CODEX_HOME/profile-name.config.toml` files.

Codex ships with operating level sandboxing and has two key knobs that you can control. Approval mode determines when Codex asks for your permission to run a command and sandbox mode determines if Codex can read or write in the directory and what files the agent can access.

If you're new to coding agents, start with the default permissions. Keep approval and sandboxing tight by default, then loosen permissions only for trusted repos or specific workflows once the need is clear.

Note that the CLI, IDE, and Codex app all share the same configuration layers. Learn more on the [sample configuration](/codex/config-sample) page.

Configure Codex for your real environment early. Many quality issues are
really setup issues, like the wrong working directory, missing write access,
wrong model defaults, or missing tools and connectors.

#### Improve reliability with testing and review

Don't stop at asking Codex to make a change. Ask it to create tests when needed, run the relevant checks, confirm the result, and review the work before you accept it.

Codex can do this loop for you, but only if it knows what “good” looks like. That guidance can come from either the prompt or `AGENTS.md`.

That can include:

- Writing or updating tests for the change
- Running the right test suites
- Checking lint, formatting, or type checks
- Confirming the final behavior matches the request
- Reviewing the diff for bugs, regressions, or risky patterns

Toggle the diff panel in the Codex app to directly [review
changes](/codex/app/review) locally. Click on a specific row to provide
feedback that gets fed as context to the next Codex turn.

A useful option here is the slash command `/review`, which gives you a few ways to review code:

- Review against a base branch for PR-style review
- Review uncommitted changes
- Review a commit
- Use custom review instructions

If you and your team have a `code_review.md` file and reference it from `AGENTS.md`, Codex can follow that guidance during review as well. This is a strong pattern for teams that want review behavior to stay consistent across repositories and contributors.

Codex shouldn't just generate code. With the right instructions, it can also help **test it, check it, and review it**.

If you use GitHub Cloud, you can set up Codex to run [code reviews for your PRs](/codex/integrations/github). At OpenAI, Codex reviews 100% of PRs. You can enable automatic reviews or have Codex reactively review when you @Codex.

