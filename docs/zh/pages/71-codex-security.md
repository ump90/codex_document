### Codex 安全

Source: [Codex Security](https://developers.openai.com/codex/security/index.md)

[在 Codex App 中安装插件](https://chatgpt.com/plugins/share/676aca3811d54fa7bcdef5255236b3c4)

有关安装步骤、支持的技能和审查边界，请参阅
[Codex Security 插件指南](https://developers.openai.com/codex/security/plugin)。

#### 探索插件用例

- [运行深度安全扫描](https://developers.openai.com/codex/use-cases/deep-security-scan)，执行召回率更高的全仓库审计。
- [扫描代码变更的安全性](https://developers.openai.com/codex/use-cases/scan-code-changes-for-security)，在合并拉取请求或分支前扫描代码变更。
- [修复漏洞积压项](https://developers.openai.com/codex/use-cases/remediate-vulnerability-backlog)，针对已批准的发现进行有边界的修复。

该插件在你的 Codex 线程中运行。Codex Security 云端扫描会通过 Codex Web 扫描已连接的 GitHub 仓库。有关 Codex 沙箱、审批、网络控制和管理员设置，请参阅 [Agent 审批与安全](https://developers.openai.com/codex/agent-approvals-security)。

#### Codex Security 云

Codex Security 云目前处于研究预览阶段。它会扫描已连接的 GitHub 仓库，查找可能的安全问题。

它可以帮助团队：

1. **发现可能的漏洞**，方式是使用特定于仓库的威胁模型和真实代码上下文。
2. **减少噪音**，方式是在你审查之前验证发现。
3. **推动发现走向修复**，提供排序后的结果、证据和建议的补丁选项。

#### Codex Security 云如何工作

Codex Security 会逐个 commit 扫描已连接的仓库。
它从你的仓库构建扫描上下文，基于该上下文检查可能的漏洞，并在隔离环境中验证高信号问题，然后再展示出来。

你会得到一个聚焦于以下内容的工作流：

- 特定于仓库的上下文，而不是通用签名
- 有助于减少误报的验证证据
- 可在 GitHub 中审查的建议修复

#### Codex Security 云访问权限和前置条件

Codex Security 面向 ChatGPT Enterprise、Edu、Business 和 Pro 用户开放。它通过 Codex Web 与已连接的 GitHub 仓库配合使用。如果你需要访问权限，或者某个仓库不可见，请确认该仓库可通过你的 Codex Web 工作区访问，或联系你的 OpenAI 客户团队。

#### 安全概览参考

- [Codex Security 插件指南](https://developers.openai.com/codex/security/plugin) 介绍 Codex 中的本地仓库和差异审查工作流。
- [Codex Security 云端设置](https://developers.openai.com/codex/security/setup) 介绍设置、扫描和发现审查。
- [改进威胁模型](https://developers.openai.com/codex/security/threat-model) 说明如何调整范围、攻击面和关键性假设。
- [FAQ](https://developers.openai.com/codex/security/faq) 涵盖常见产品问题。
