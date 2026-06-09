### 运行深度安全扫描

Source: [Run a deep security scan](https://developers.openai.com/codex/use-cases/deep-security-scan.md)

在已授权的仓库中深入搜索可信的漏洞。

#### 概览

使用 Codex Security plugin 运行召回率更高的全仓库审计。该流程会重复发现候选问题、验证候选项，并生成可审查的报告 artifact。

适合：

- 对你拥有或被授权评估的完整仓库进行应用安全审查。
- 需要更高召回率，并愿意投入更多运行时间和 token 来发现更多候选问题的审查。
- 安全团队在决定修复内容之前，需要可追溯的发现证据。

相关 skill：

- `$codex-security:deep-security-scan`：运行重复的全仓库安全发现 pass，验证存活的发现，分析攻击路径，并创建可审查报告。

#### 起始提示

```text
/goal 对此仓库运行一次深度安全扫描。在所有必需步骤完成且最终报告准备好之前不要停止。

范围和规则：
- 我已获得评估此仓库的授权。
- 将整个仓库视为范围内。
- 使用 Codex Security plugin 的 deep scan 工作流；不要把它扩展为 diff 审查或限定路径审查。
- 保持扫描只读；不要修改代码、打开 pull request，或测试外部目标。

返回最终 Markdown 和 HTML 报告路径，并优先总结需要人工审查的发现。
```

建议使用高推理强度。

#### 选择深度仓库审查

当你需要在完整仓库中进行高召回率漏洞发现，并且可以为更长运行时间留出预算时，请使用 deep scan。Codex Security plugin 会在验证和排序发现之前重复执行发现 pass，因此这个工作流比普通扫描花费更多时间和 token。

Deep scan 面向整个仓库。若要审查某个 package 或目录，请使用 `$codex-security:security-scan`。若要审查 pull request、commit、branch diff 或 working-tree patch，请使用 [$codex-security:security-diff-scan](86-scan-code-changes-for-security.md)。

#### 准备已授权扫描

1. 在 Codex 中打开仓库，并安装 [Codex Security plugin](10-codex-security-plugin.md)。
2. 确认你拥有该仓库，或已获得评估授权。
3. 如果能提升审查质量，请在 `AGENTS.md` 中添加仓库特定的架构、信任边界、构建、测试和验证指导。
4. 运行起始提示，并让扫描完成重复发现、验证、攻击路径分析和最终报告阶段。
5. 在要求 Codex 修改代码或进一步复现某个发现之前，先审查最终报告。

#### 修复前审查证据

最终结果应识别受影响位置、行为为何可达、Codex 执行了哪些验证、仍有哪些证明缺口，以及有边界的修复方向。请区分没有验证证据的发现和已验证的发现。

仅针对你已选择并审查过的发现开始修复。使用 [修复漏洞积压项](87-remediate-vulnerability-backlog.md)，一次修复一个发现，并进行聚焦的回归验证。

#### 相关链接

- [Codex Security plugin](10-codex-security-plugin.md)
- [代理审批和安全](13-agent-approvals-security.md)
- [Codex 网络安全](14-cyber-safety.md)
