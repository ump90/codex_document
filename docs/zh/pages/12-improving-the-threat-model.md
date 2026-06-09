### 改进威胁模型

Source: [Improving the threat model](https://developers.openai.com/codex/security/threat-model.md)

了解威胁模型是什么，以及编辑它如何改进 Codex Security 的建议。

#### 什么是威胁模型

威胁模型是关于你的仓库如何工作的简短安全摘要。在 Codex Security 中，你以 `project overview` 的形式编辑它，系统会将其作为未来扫描、优先级排序和审查的扫描上下文。

Codex Security 会根据代码创建第一版草稿。如果发现结果感觉不准确，这是首先要编辑的内容。

一个有用的威胁模型会指出：

- 入口点和不受信任的输入
- 信任边界和认证假设
- 敏感数据路径或特权操作
- 团队希望优先审查的区域

例如：

> 用于账户变更的公共 API。接受 JSON 请求和文件上传。使用内部认证服务进行身份检查，并通过内部服务写入账单变更。重点审查认证检查、上传解析和服务间信任边界。

这会为 Codex Security 未来的扫描和发现优先级排序提供更好的起点。

#### 改进并重新查看威胁模型

如果你想改进结果，请先编辑威胁模型。当发现遗漏了你关心的区域，或出现在你意料之外的位置时，请使用它。威胁模型会改变未来扫描上下文。

一些用户会把当前威胁模型复制到 Codex 中，通过对话
根据他们想更仔细审查的区域改进它，然后将
更新后的版本粘贴回 web UI。

#### 在哪里编辑

要审查或更新威胁模型，请前往 [Codex Security scans](https://chatgpt.com/codex/security/scans)，打开仓库并点击 **Edit**。

#### 威胁模型参考

- [Codex Security 设置](https://developers.openai.com/codex/security/setup) 覆盖仓库设置和发现审查。
- [Codex Security](https://developers.openai.com/codex/security) 提供产品概览。
- [FAQ](https://developers.openai.com/codex/security/faq) 覆盖常见问题。
