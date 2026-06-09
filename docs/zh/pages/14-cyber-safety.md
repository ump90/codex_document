### 网络安全

Source: [Cyber Safety](https://developers.openai.com/codex/concepts/cyber-safety.md)

[GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/) 是我们根据 [Preparedness Framework](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf) 第一个按“高网络安全能力”处理的模型，这要求额外的防护措施。这些防护措施包括训练模型拒绝明显恶意的请求，例如窃取凭据。

除安全训练外，基于自动分类器的监控会检测可疑网络活动信号，并将高风险流量路由到网络能力较低的模型（GPT-5.2）。我们预计只有很小一部分流量会受到这些缓解措施影响，并正在持续优化我们的策略、分类器和产品内通知。

#### 我们为什么这样做

最近几个月，我们看到模型在网络安全任务上的性能取得了显著提升，使开发者和安全专业人员都受益。随着模型在漏洞发现等网络安全相关任务上的能力提升，我们采取预防性方法：扩展保护和执行措施，以支持合法研究，同时减缓滥用。

网络能力本质上具有双重用途特性。支撑重要防御工作的同一套知识和技术，例如渗透测试、漏洞研究、大规模扫描、恶意软件分析和威胁情报，也可能造成现实世界伤害。

这些能力和技术需要在可用于提升安全性的上下文中可用且更容易使用。我们的 [Trusted Access for Cyber](https://openai.com/index/trusted-access-for-cyber/) 试点使个人和组织能够继续使用模型进行潜在高风险网络安全活动而不受干扰。

#### 工作原理

从事网络安全相关工作或类似活动的开发者和安全专业人员，如果其请求可能被自动检测系统 [误判](#false-positives)，请求可能会被重新路由到 GPT-5.2 作为回退。我们预计只有很小一部分流量会受缓解措施影响，并正在积极校准我们的策略和分类器。

Codex CLI 的最新 alpha 版本包含产品内消息，用于提示
请求何时被重新路由。未来几天内，所有客户端都将支持
此消息。

受缓解措施影响的账户可以通过加入下面的 [Trusted Access](#trusted-access-for-cyber) 计划，重新获得对 GPT-5.3-Codex 的访问。

我们认识到，加入 Trusted Access 可能并不适合所有人，因此随着我们扩展这些缓解措施并 [加强](https://openai.com/index/strengthening-cyber-resilience/) 网络韧性，我们计划在大多数情况下从账户级安全检查转向请求级检查。

#### 网络安全可信访问（Trusted Access for Cyber）

我们正在试点“trusted access”，它允许开发者在我们继续为正式可用校准策略和分类器的同时保留高级能力。我们的目标是让极少用户需要加入 [Trusted Access for Cyber](https://openai.com/index/trusted-access-for-cyber/)。

要将模型用于潜在高风险网络安全工作：

- 用户可以在 [chatgpt.com/cyber](https://chatgpt.com/cyber) 验证身份
- 企业可以通过其 OpenAI 代表，为整个团队默认申请 [trusted access](https://openai.com/form/enterprise-trusted-access-for-cyber/)

可能需要访问网络能力更强或更宽松模型以加速合法防御工作的安全研究人员和团队，可以表达对我们的 [invite-only program⁠](https://docs.google.com/forms/d/e/1FAIpQLSea_ptovrS3xZeZ9FoZFkKtEJFWGxNrZb1c52GW4BVjB2KVNA/viewform?usp=header) 的兴趣。拥有 trusted access 的用户仍必须遵守我们的 [Usage Policies⁠](https://openai.com/policies/usage-policies/) 和 [Terms of Use⁠](https://openai.com/policies/row-terms-of-use/)。

#### 误报

合法或非网络安全活动偶尔可能被标记。发生重新路由时，响应模型会在 API 请求日志中可见，并在 CLI 中通过产品内通知显示，很快会覆盖所有使用界面。如果你遇到认为不正确的重新路由，请通过 `/feedback` 报告误报。
