### 扫描代码变更中的安全问题

Source: [Scan code changes for security](https://developers.openai.com/codex/use-cases/scan-code-changes-for-security.md)

审查 pull request 或本地 diff 是否引入安全回归。

#### 概览

使用 Codex Security plugin 检查基于 Git 的变更集、验证可信的安全回归，并在合并前生成基于证据的报告。

适合：

- 触及认证、授权、解析、文件访问、secret 或特权工作流的 pull request。
- 合并前需要安全聚焦检查的 release branch 或本地 patch。
- 需要把发现锚定到变更代码和直接支持文件的审查者。

相关 skill：

- `$codex-security:security-diff-scan`：审查 pull request、commit、branch diff 或 working-tree patch 中的安全回归，并提供验证和攻击路径证据。

#### 起始提示

```text
/goal 扫描此 PR、commit、branch diff 或 working-tree patch 中的安全回归。在所有范围内变更文件覆盖完毕且所有必需步骤完成之前不要停止。

范围和规则：
- 目标：[此 pull request / commit SHA / 从 BASE 到 HEAD 的 branch diff / 当前 working-tree patch]
- 我已获得评估此仓库和变更集的授权。
- 请特别关注 [auth、input handling、secrets、filesystem、network、dependencies 或其它敏感面]。
- 保持本轮只读；不要修改代码或打开 pull request。

返回最终 Markdown 报告，以及需要人工审查的发现对应的 Codex app review directive。
```

建议使用高推理强度。

#### 审查变更，而不是整个仓库

当 pull request、commit、branch 或本地 patch 修改敏感代码路径时，请使用 security diff scan。Codex Security plugin 会使用仓库上下文理解变更，然后把发现和验证聚焦在 diff 及直接支持代码上。

这个工作流是普通代码审查的补充。请在你需要安全回归证据，而不是一般风格或测试审查时使用它。

#### 运行聚焦检查

1. 打开仓库，并检出或描述要审查的确切 Git 变更集。
2. 安装 [Codex Security plugin](10-codex-security-plugin.md)，并在起始提示中指定 pull request、commit、branch diff 或 working-tree patch。
3. 指明变更中的高风险表面，例如认证、解析器、文件路径、网络请求或凭据处理。
4. 运行提示时不要请求修复，让第一个结果保持为审查 artifact。
5. 在决定是否修复之前，检查每个报告的受影响行、验证结果和证明缺口。

#### 跟进发现

有用的报告应区分可达且有支撑的安全发现，以及仍需确认的怀疑项，并可为受影响行包含 Codex app review directive。对于可行动结果，请使用发现 identifier 或相关报告章节打开一个新的有边界修复任务。

修复和验证循环请参阅 [修复漏洞积压项](87-remediate-vulnerability-backlog.md)。

#### 相关链接

- [Codex Security plugin](10-codex-security-plugin.md)
- [代理审批和安全](13-agent-approvals-security.md)
