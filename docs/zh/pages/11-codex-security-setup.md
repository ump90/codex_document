### Codex Security 设置

Source: [Codex Security setup](https://developers.openai.com/codex/security/setup.md)

本页会带你完成从初始访问到在 Codex Security 中审查发现并创建修复 pull request 的流程。

请先确认你已经设置 Codex Cloud。如果还没有，请参见 [Codex
Cloud](47-codex-web.md) 开始。

#### 1. 访问和环境

Codex Security 会扫描通过 [Codex Cloud](47-codex-web.md) 连接的 GitHub 仓库。

- 确认你的工作区有权访问 Codex Security。
- 确认你要扫描的仓库在 Codex Cloud 中可用。

前往 [Codex environments](https://chatgpt.com/codex/settings/environments)，检查仓库是否已有环境。如果没有，请先在那里创建一个，再继续。

[打开环境](https://chatgpt.com/codex/settings/environments)

#### 2. 新建安全扫描

环境存在后，前往 [Create a security scan](https://chatgpt.com/codex/security/scans/new)（创建安全扫描），选择你刚连接的仓库。

[创建安全扫描](https://chatgpt.com/codex/security/scans/new)

Codex Security 会先从最新提交向后扫描仓库。它使用这种方式在新提交进入时构建并刷新扫描上下文。

要配置仓库：

1. 选择 GitHub 组织。
2. 选择仓库。
3. 选择你想扫描的分支。
4. 选择环境。
5. 选择 **历史窗口**。更长的窗口会提供更多上下文，但回填需要更长时间。
6. 点击 **Create**。

#### 3. 初始扫描可能需要一段时间

创建扫描后，Codex Security 首先会对所选历史窗口运行提交级安全检查。
初始回填可能需要几个小时，尤其是对于更大的仓库或更长的窗口。
如果发现没有立即可见，这是预期情况。请等待初始扫描完成，再开工单或排查问题。

初始扫描设置是自动且彻底的。这可能需要几个小时。如果第一批发现延迟出现，请不要
担心。

#### 4. 审查扫描并改进威胁模型

[审查扫描](https://chatgpt.com/codex/security/scans)

初始扫描完成后，打开扫描并审查生成的威胁模型。
初始发现出现后，更新威胁模型，使其与你的架构、信任边界和业务上下文匹配。
这有助于 Codex Security 为你的团队排序问题。

如果你希望扫描结果发生变化，可以使用更新后的范围、优先级和假设来编辑威胁模型。

初始发现出现后，重新查看该模型，使扫描指导始终与当前优先事项一致。
保持其最新有助于 Codex Security 产生更好的建议。

关于威胁模型及其如何影响严重性和分诊的更深入解释，请参见 [改进威胁模型](12-improving-the-threat-model.md)。

#### 5. 审查发现并打补丁

初始回填完成后，从 **Findings** 视图审查发现。

[打开发现](https://chatgpt.com/codex/security/findings)

你可以使用两个视图：

- **Recommended Findings**：仓库中最关键问题的动态前 10 列表
- **All Findings**：覆盖整个仓库、可排序和过滤的发现表

点击某个发现可打开其详情页，其中包括：

- 问题的简明描述
- 提交详情和文件路径等关键元数据
- 关于影响的上下文推理
- 相关代码摘录
- 可用时的调用路径或数据流上下文
- 验证步骤和验证输出

你可以审查每个发现，并直接从发现详情页创建 PR。

[审查发现并创建 PR](https://chatgpt.com/codex/security/findings)

#### 安全设置参考

- [Codex Security](71-codex-security.md) 提供产品概览。
- [FAQ](09-codex-security-faq.md) 覆盖常见问题。
- [改进威胁模型](12-improving-the-threat-model.md) 解释如何改进扫描上下文和发现优先级。
