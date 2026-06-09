### GitHub 中的 Codex 代码审查

Source: [Codex code review in GitHub](https://developers.openai.com/codex/integrations/github.md)

使用 Codex code review，可以在 GitHub pull request 上获得另一次高信号审查。Codex 会审查 pull request diff，遵循你的仓库指南，并发布一个标准的 GitHub 代码审查，重点关注严重问题。

#### 开始之前

请确保你具备：

- 为要审查的仓库设置了 [Codex cloud](47-codex-web.md)。
- 能够访问 [Codex code review settings](https://chatgpt.com/codex/settings/code-review)。
- 如果你希望 Codex 遵循仓库特定的审查指南，请准备一个 `AGENTS.md` 文件。

#### 设置 Codex 代码审查

1. 设置 [Codex cloud](47-codex-web.md)。
2. 前往 [Codex settings](https://chatgpt.com/codex/settings/code-review)。
3. 为你的仓库开启 **Code review**。

#### 请求 Codex 审查

1. 在 pull request 评论中提及 `@codex review`。
2. 等待 Codex 作出反应（👀）并发布审查。

Codex 会像队友一样在 pull request 上发布审查。在 GitHub 中，Codex 只标记 P0 和 P1 问题，以便审查评论聚焦于高优先级风险。

#### 启用自动审查

如果你希望 Codex 自动审查每个 pull request，请在 [Codex settings](https://chatgpt.com/codex/settings/code-review) 中开启 **Automatic reviews**。
Codex 会在有人打开新的 PR 供审查时发布审查，无需 `@codex review` 评论。

#### 自定义 Codex 代码审查内容

Codex 会在你的仓库中搜索 `AGENTS.md` 文件，并遵循你包含的任何 **Review guidelines**。

若要为仓库设置指南，请添加或更新顶层 `AGENTS.md`，并包含如下 section：

```md
## 审查指南

- Don't log PII.
- Verify that authentication middleware wraps every route.
```

Codex 会将距离每个变更文件最近的 `AGENTS.md` 中的指南应用于该文件。当特定包需要额外审查时，你可以在目录树更深处放置更具体的说明。

对于一次性关注点，请把它添加到 pull request 评论中：

`@codex review for security regressions`

如果你希望 Codex 标记文档中的拼写错误，请在 `AGENTS.md` 中添加指南（例如，“Treat typos in docs as P1.”）。

#### 处理审查发现

Codex 发布审查后，你可以在同一个 pull request 中再留一条评论，请它修复问题：

```md
@codex fix the P1 issue
```

Codex 会以该 pull request 作为上下文启动一个云端任务，并且在有权限时可以把修复推回该分支。

#### 给 Codex 其他任务

如果你在评论中提及 `@codex`，但内容不是 `review`，Codex 会使用你的 pull request 作为上下文启动一个[云端任务](47-codex-web.md)。

```md
@codex fix the CI failures
```

#### 排查代码审查问题

如果 Codex 没有反应或没有发布审查：

- 确认你已在 [Codex settings](https://chatgpt.com/codex/settings/code-review) 中为该仓库开启 **Code review**。
- 确认该 pull request 属于已设置 [Codex cloud](47-codex-web.md) 的仓库。
- 在 pull request 评论中使用准确触发语 `@codex review`。
- 对于 automatic reviews，请检查你已开启 **Automatic reviews**，并且 pull request 事件与你的审查触发设置匹配。
