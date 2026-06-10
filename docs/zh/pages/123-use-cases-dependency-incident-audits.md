### 审计依赖事件

Source: [Audit dependency incidents](https://developers.openai.com/codex/use-cases/dependency-incident-audits.md)

把公开 package advisory 转化为安全的仓库审计计划。

#### 概览

使用 Codex 将公开 package 或供应链 advisory 转化为只读审计，然后在不运行不可信代码的情况下检查 manifests、lock files、CI workflows 和 scripts。

适合：

- 正在响应公开 package 或供应链 advisories 的工程和安全团队。
- 在变更依赖前需要检查 lock files、scripts、CI permissions 和 caches 的维护者。
- 希望 Codex 在不安装 packages 或运行不可信代码的情况下收集证据的事件审查。

相关 skill：

- [`github`](49-codex-code-review-in-github.md)：检查仓库文件、pull requests、workflows 和安全相关历史。

#### 起始提示

**构建事件审计**

```text
帮我审计此仓库是否暴露于这个公开 package advisory：[advisory URL]。

除非我明确批准修复步骤，否则保持只读。

首先，总结：
- 受影响 packages 和版本范围
- 权威来源与更广泛报道的区别
- 哪些证据可以证明此仓库存在暴露
- 哪些证据可以排除暴露

然后检查：
- package manifests 和 lock files
- CI workflows 和 permissions
- install、build 和 postinstall scripts
- 如果相关，检查 vendored artifacts、containers 或 generated bundles
- 如果 advisory 涉及 CI 或发布，检查 cache 或 token 暴露路径

返回：
- 证据状态：confirmed exposure、needs verification 或 ruled out
- 严重性和 blast-radius 说明
- 每个仓库特定 claim 的文件引用
- caveats 和建议的下一步

不要安装 packages、运行 lifecycle scripts、构建项目、执行不可信代码、轮换凭据或清理文件，除非我明确批准该步骤。
```

建议使用高工作量。

#### 相关链接

- [Codex Security](71-codex-security.md)
- [Agent approvals and security](13-agent-approvals-security.md)
- [Codex cyber safety](14-cyber-safety.md)

## 从安全审计计划开始

当依赖或供应链事件快速发展时，第一份有用输出不是仓促 patch，而是清晰的审计计划：发生了什么变化，哪些 packages 或 workflows 可能受影响，以及哪些证据能证明你的仓库存在暴露。

在安装、构建、测试或运行任何内容之前，使用 Codex 把 advisory 转化为保守的只读检查清单。

## 保持第一轮只读

1. 给 Codex 提供公开 advisory、事件报告或受影响 package 列表。
2. 让它把权威来源与更广泛评论分开。
3. 让它定义能证明或排除暴露的证据。
4. 让它检查 manifests、lock files、CI workflows、scripts 和相关仓库文件。
5. 要求按证据状态、严重性和建议的下一步对发现分组。

对于 package 事件，在知道 advisory 影响范围之前，避免运行 install、build、test、import 或 lifecycle commands。Codex 可以在不执行不可信代码的情况下搜索 lock files 和 workflows。

## 将证据状态与严重性分开报告

有用的审计结果应同时展示发现可能有多糟，以及证据有多强：

- **Confirmed exposure：** lockfile 在 production dependency path 中包含受影响 package 版本。
- **Needs verification：** 一个 CI job 具有发布权限，但 workflow 看起来没有直接安装受影响 package。
- **Ruled out：** package 名称只出现在文档中，并未出现在 manifests 或 lock files 中。
- **Next step：** 在任何破坏性操作前审查建议的依赖更新和 token rotation plan。

只读 pass 完成后，你可以让 Codex 准备修复 PR、更新 CI permissions，或编写后续事件说明。请把这些动作与初始审计分开。
