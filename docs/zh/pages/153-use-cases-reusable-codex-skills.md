### 把工作流保存为 skills

Source: [Save workflows as skills](https://developers.openai.com/codex/use-cases/reusable-codex-skills.md)

创建一个 Codex 可以随时使用的 skill，用于你会重复执行的工作。

#### 概览

把一个有效的 Codex 线程、review rules、test commands、release checklists、design conventions、writing examples 或 repo-specific scripts 转成 Codex 可在未来线程中使用的 skill。

适合：

- 你希望 Codex 再次使用的已编码工作流。
- 希望使用可复用 skill，而不是在每个线程中粘贴长 prompt 的团队。

相关 skill：

- `$skill-creator`：收集工作流信息，scaffold 一个 skill，保持主说明简短，并验证结果。

#### 起始提示

**从我的上下文创建 Skill**

```text
使用 $skill-creator 创建一个 Codex skill，用于 [fixes failing Buildkite checks on a GitHub PR / turns PR notes into inline review comments / writes our release notes from merged PRs]

创建 skill 时使用这些来源：
- Working example: [say "use this thread," link a merged PR, or paste a good Codex answer]
- Source: [paste a Slack thread, PR review link, runbook URL, docs URL, or ticket]
- Repo: [repo path, if this skill depends on one repo]
- Scripts or commands to reuse: [test command], [preview command], [log-fetch script], [release command]
- Good output: [paste the Slack update, changelog entry, review comment, ticket, or final answer you want future threads to match]
```

#### 创建一个 Codex 可以随时使用的 skill

使用 skills 为 Codex 提供可复用 instructions、resources 和 scripts，用于你会重复执行的工作。[skill](48-agent-skills.md) 可以保留第一次让 Codex 有用的 thread、doc、command 或 example。

从一个有效例子开始：一个 cherry-picked PR 的 Codex thread、Notion 中的 release checklist、一组有用的 PR comments，或解释 launch process 的 Slack thread。

#### 如何使用

1. 添加你希望 Codex 使用的上下文。

   留在你想保存的 Codex thread 中，粘贴 Slack thread 或 docs link，并添加 Codex 应记住的 rule、command 或 example。

2. 运行起始提示。

   该提示会说明你想要的 skill，然后把要保留的 thread、doc、PR、command 或 output 交给 `$skill-creator`。

3. 让 Codex 创建并验证 skill。

   结果应定义 `$skill-name`，说明它何时触发，并把可复用 instructions 放在正确位置。

   `~/.codex/skills` 中的 skills 可从任何 repo 使用。当前 repo 中的 skills 可以提交，让队友也能使用。

4. 使用 skill，然后从线程中更新它。

   在下一个 PR、alert、review、release note 或 design task 上调用新的 `$skill-name`。如果它用了错误 test command、漏掉 review rule、跳过 runbook step，或写出了你不会发送的草稿，请要求 Codex 把该修正加入 skill。

#### 提供源材料

给 `$skill-creator` 提供解释 skill 应如何工作的材料。

| 你已有的内容 | 应添加的内容 |
| --- | --- |
| **想要保留的 Codex thread 中的 workflow** | 留在该 thread 中，并说 `use this thread`。Codex 可以把该 thread 中的对话、命令、编辑和反馈作为起点。 |
| **Docs 或 runbook** | 粘贴 release checklist，链接 incident-response runbook，附上 API PDF，或让 Codex 查看 repo 中的 markdown guide。 |
| **团队对话** | 粘贴某人解释 alert 的 Slack thread，链接带 frontend rules 的 PR review，或附上解释 customer problem 的 support conversation。 |
| **skill 应复用的 scripts 或 commands** | 添加 test command、preview command、release script、log-fetch script，或你希望未来 Codex threads 运行的 local helper command。 |
| **一个好结果** | 添加 merged PR、final changelog entry、accepted launch note、resolved ticket、before/after screenshot，或你希望未来 threads 匹配的最终 Codex answer。 |

如果来源在 Slack、Linear、GitHub、Notion 或 Sentry 中，请在 Codex 中通过 [plugin](78-plugins.md) 连接该工具，在起始提示中提到它，或把相关部分粘贴到线程中。

#### Codex 会创建什么

大多数 skills 都从一个 `SKILL.md` 文件开始。当工作流需要时，`$skill-creator` 可以添加更长的 references、scripts 或 assets。

#### 你可以创建的 skills

当未来 threads 应读取同一 runbook、运行同一 CLI、遵循同一 review rubric、写同一 team update，或 QA 同一 browser flow 时，可以使用同一模式。例如：

- **`$buildkite-fix-ci`** 下载 failed job logs，诊断错误，并提出最小 code fix。
- **`$fix-merge-conflicts`** checkout 一个 GitHub PR，基于 base branch 更新它，解决 conflicts，并返回确切 push command。
- **`$frontend-skill`** 让 Codex 贴近你的 UI taste、现有 components、screenshot QA loop、asset choices 和 browser polish pass。
- **`$pr-review-comments`** 把 review notes 转成语气合适、带 GitHub links 的简洁 inline comments。
- **`$web-game-prototyper`** 定义 first playable loop 的范围，选择 assets，调 game feel，捕获 screenshots，并在 browser 中 polish。

#### 相关链接

- [Agent skills](48-agent-skills.md)
