### 保持文档更新

Source: [Keep documentation up-to-date](https://developers.openai.com/codex/use-cases/update-documentation.md)

使用代码和其它来源自动化文档更新。

#### 概览

使用 Codex 比较 source code changes、public docs、release notes 和 PR context，然后在发布前起草聚焦的文档更新，并附带验证步骤。

适合：

- 需要跟踪频繁变化行为的 developer docs、READMEs、runbooks、examples 和 migration notes。
- 维护技术产品文档的团队。

相关 skill：

- `github`：当 GitHub 是 bug intake 的一部分时，读取 issues、pull requests、comments、review threads 和 failed checks。

#### 起始提示

**根据源代码变更更新文档**

```text
根据以下来源更新 [product/feature] documentation：

- [this repo/source linked repo] 中已变更的 source files
- 提到新行为的现有 docs pages
- 我下面提供的任何 linked issue、PR、release note 或 public reference

然后：
- 识别哪些内容是 user-facing
- 只更新需要变更的 docs
- 不要把 unpublished roadmap、private customer details 和 internal-only context 放进 public docs
- 保留现有 docs structure、terminology 和 cross-links
- 运行适合该变更的 docs checks

在最终完成前，总结改了什么、验证了什么，以及哪些 claims 无法从 trusted sources 证明。

[link release notes or other references here]
```

#### 简介

文档在伴随 source changes 一起更新时最容易保持准确，而不是几周后再补。Codex 可以检查已变更代码、tests、release notes、linked issues 和 pull request context，然后起草一个范围明确、符合现有结构的 docs update。

这个工作流适用于 developer docs、README updates、changelog drafts、migration notes、runbooks，或任何需要跟踪频繁变化行为的内容。

#### 如何使用

1. 从你需要记录的变更开始。

   分享 branch、pull request、commit、issue 或 files。如果 docs 是公开的，请明确说明 unpublished roadmap、private customer details 和 internal-only context 不应出现。

2. 要求 Codex map 受影响 docs。

   让它在起草前搜索现有 docs 中的 feature names、config keys、commands、examples 和 related terms。

3. 更新最小有用 docs surface。

   Codex 应保留当前 page structure、terminology、cross-links 和 frontmatter。精准添加 note、example 或 section update 足够时，应避免大范围重写。

4. 验证变更。

   要求 Codex 运行适合 repo 的 formatting 和 docs checks，然后总结每个 user-facing claim 背后的证据。

#### 给 Codex 什么

| 来源 | 为什么有帮助 |
| --- | --- |
| 已变更代码和 tests | 让 Codex 分析实际行为，以起草聚焦文档更新。 |
| Public release notes 或 product docs | 帮助 Codex 匹配公开术语、可用性和 feature status。 |
| Pull request 或 issue context | 解释变更原因，以及哪些 user-facing behavior 重要。 |
| Local docs checks | 在 docs 发布前给 Codex 一个具体完成定义。 |

加入 public release notes 等更多上下文，可以帮助 Codex 避免包含私密上下文或尚未公开的更新。

#### 让工作流可重复

对于 repo-wide convention，请把文档期望加入 [AGENTS.md](50-custom-instructions-with-agents-md.md)。例如：

```md
## Documentation

- 当 user-facing behavior 发生变化时，检查 docs、examples 或 changelogs 是否需要更新。
- Public docs 只能包含 public information，或该 repo 中可见的 behavior。
- 保留现有 terminology 和 frontmatter。
- 最终 handoff 前运行 docs formatting 和 build checks。
```

如果流程步骤更多，请把它转成 [skill](48-agent-skills.md)，让未来 Codex threads 能遵循同样的 source-checking、drafting 和 verification loop。参阅 [Save workflows as skills](153-use-cases-reusable-codex-skills.md)，它更详细地介绍了这个模式。

你也可以要求 Codex 按计划运行，把这个工作流变成 [thread automation](24-automations.md#thread-automations)。例如，让它从 GitHub 获取所有近期 PR，自动保持 docs up-to-date，并按周执行：

#### 相关链接

- [Workflows](06-example-workflows.md)
