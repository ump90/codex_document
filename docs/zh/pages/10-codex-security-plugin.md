### Codex Security 插件

Source: [Codex Security plugin](https://developers.openai.com/codex/security/plugin.md)

Codex Security 插件为 Codex 添加安全审查工作流，用于你有授权评估的代码。你可以在打开的仓库中使用它来调查代码库、审查变更集中的安全回归、确认可信发现，并准备最小修复以供审查。

本页介绍在你的 Codex 线程中运行的可安装插件。对于
通过 Codex Web 扫描已连接 GitHub 仓库的研究预览版产品，
请参见 [Codex Security](https://developers.openai.com/codex/security)。

#### 安装插件

安装 Codex Security 插件

    安装后，在你想要评估的仓库中启动一个新线程。

1. 打开 Codex

   从你的仓库启动 Codex：

   ```bash
   codex
   ```

   2. 打开插件浏览器

      输入：

      ```text
      /plugins
      ```

   3. 安装 Codex Security

      搜索 **Codex Security**，打开它，并选择 `Install plugin`。

   4. 启动新线程

      在你有授权审查的仓库中启动一个新线程。

#### 选择安全工作流

选择能够回答你问题的最窄工作流。面向 diff 的扫描比全仓库扫描更容易审查；深度扫描会有意使用更多时间和 token 来搜索更多候选发现。

| 目标                                   | Skill                                | 范围和输出                                                                                                    |
| -------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| 审查仓库或一个限定路径                 | `$codex-security:security-scan`      | 运行威胁建模、发现查找、验证、攻击路径分析，并生成 Markdown 和 HTML 报告。                                   |
| 运行更高召回率的审计                   | `$codex-security:deep-security-scan` | 在验证和报告前，通过委派 worker 重复进行全仓库发现。仅用于整个仓库。                                         |
| 合并前审查变更                         | `$codex-security:security-diff-scan` | 审查 pull request、commit、branch diff 或 working-tree patch，并生成基于变更代码的 Markdown 报告。            |
| 修复一个发现                           | `$codex-security:fix-finding`        | 复现或验证一个可信发现，在需要时做最小修复，并检查易受攻击行为不再复现。                                    |

例如，要扫描仓库：

```text
使用 $codex-security:security-scan 扫描此仓库中的安全
漏洞。让扫描基于代码证据，在可行时验证可信
发现，并返回最终报告路径。不要修改代码。
```

要改为审查当前变更：

```text
使用 $codex-security:security-diff-scan 审查当前分支 diff 中的
安全回归。将审查范围限定在变更代码和直接
支撑文件内。不要修改代码。
```

#### 审查结果并修复发现

仓库扫描使用分阶段工作流：

1. **威胁建模** 识别入口点、信任边界、敏感
   操作和高风险组件。
2. **发现查找** 在请求范围内寻找具体的 source-to-sink 路径或失效
   控制。
3. **验证** 测试或以其它方式验证可信发现，并记录
   证据或证明缺口。
4. **攻击路径分析** 追踪可利用路径，并为
   通过验证的发现评定严重性。
5. **报告** 将发现、受影响位置、验证证据、
   修复指导和审查指令写入产物。

普通仓库扫描或深度扫描会在其扫描目录内写入 `report.md` 和可读的
`report.html`。diff 扫描会写入聚焦的 Markdown
报告。在开始修复前，请审查受影响文件、证据、假设和严重性。

当某个发现可操作时，请请求一个有边界的修复：

```text
使用 $codex-security:fix-finding 修复发现 [发现 ID 或报告
引用]。添加聚焦的回归覆盖，验证合法行为仍然
有效，并证明原始问题不再复现。不要将
变更扩展到此发现之外。
```

#### 确保安全工作经过授权且可审查

只对你拥有或你的组织授权你评估的仓库、diff 和系统运行扫描。发现是审查输入，
不是合并代码或测试无关目标的指令。

- 除非你明确要求 Codex 准备
  修复，否则保持第一次扫描只读。
- 在批准构建、运行或复现行为的命令前先审查它们，
  尤其是在陌生仓库中。
- 合并前审查每个建议补丁和验证结果。
- 使用插件时，保留仓库说明和审批策略。
  详情请参见 [代理审批和安全](https://developers.openai.com/codex/agent-approvals-security)。

#### 探索安全用例

- [运行深度安全扫描](https://developers.openai.com/codex/use-cases/deep-security-scan)
- [扫描代码变更中的安全问题](https://developers.openai.com/codex/use-cases/scan-code-changes-for-security)
- [修复漏洞积压](https://developers.openai.com/codex/use-cases/remediate-vulnerability-backlog)
