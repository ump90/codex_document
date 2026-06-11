### 安全

Source: [Security](https://developers.openai.com/codex/use-cases/collections/security.md)

评估代码、审查变更并修复安全发现。

Codex 可以帮助工程和安全团队评估已授权代码、收集证据，并把已审查的发现转化为聚焦修复。这些用例覆盖仓库扫描、变更审查、依赖事件和漏洞修复。

## 评估仓库

使用 Codex Security plugin 对已授权仓库运行召回率更高的扫描，审查可信发现，并生成支持人工分流的报告。

- [运行深度安全扫描](85-run-a-deep-security-scan.md)

## 合并前审查变更

让 Codex 检查 pull request、branch、commit 或 working-tree diff 中的安全回归，并返回与变更代码绑定的证据。

- [扫描代码变更中的安全问题](86-scan-code-changes-for-security.md)

## 审计依赖事件

把公开 package 或供应链 advisory 转化为只读仓库审计，覆盖 manifests、lock files、scripts、workflows 和暴露路径。

- [审计依赖事件](123-use-cases-dependency-incident-audits.md)

## 修复已审查发现

把安全报告、advisory 或 ticket 中的已批准发现交给 Codex，然后让它做最小修复，并验证易受攻击行为不再复现。

- [修复漏洞积压项](87-remediate-vulnerability-backlog.md)
