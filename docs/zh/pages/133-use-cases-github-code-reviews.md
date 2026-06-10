### 审查 GitHub pull requests

Source: [Review GitHub pull requests](https://developers.openai.com/codex/use-cases/github-code-reviews.md)

在人工审查前捕获回归和潜在问题。

#### 概览

在 GitHub 中使用 Codex code review，自动在 pull request 上直接暴露回归、缺失测试和文档问题。

适合：

- 希望在人工合并批准前获得另一个审查信号的团队。
- 生产项目中的大型代码库。

相关 skill：

- [`$security-best-practices`](https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices)：把审查聚焦在 secrets、auth 和 dependency changes 等高风险表面。

#### 起始提示

**请求 Codex 审查 pull request**

```text
@codex review for security regressions, missing tests, and risky behavior changes.
```

建议使用 cloud model。

#### 相关链接

- [GitHub 中的 Codex 代码审查](49-codex-code-review-in-github.md)
- [使用 AGENTS.md 自定义指令](50-custom-instructions-with-agents-md.md)

## 如何使用

先把 Codex code review 添加到你的 GitHub organization 或 repository。
更多细节请参阅 [Codex code review in GitHub](49-codex-code-review-in-github.md)。

你可以设置 Codex 自动审查每个 pull request，也可以在 pull request comment 中使用 `@codex review` 请求审查。

如果 Codex 标记了回归或潜在问题，你可以在 pull request 上评论后续提示，例如 `@codex fix it`，让它修复。

这会启动一个新的 cloud task，用来修复问题并更新 pull request。

## 定义审查指导

要自定义 Codex 审查内容，请添加或更新顶层 `AGENTS.md`，其中包含类似这样的章节：

```md
## Review guidelines

- 将拼写和语法问题标记为 P0 issues。
- 将可能缺失文档的问题标记为 P1 issues。
- 将缺失测试标记为 P1 issues。
  ...
```

Codex 会把距离每个变更文件最近的 `AGENTS.md` 中的指导应用到该文件。对于需要额外审查的特定 packages，你可以在目录树更深处放置更具体的指令。
