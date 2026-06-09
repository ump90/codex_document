### 自动审查

Source: [Auto-review](https://developers.openai.com/codex/concepts/sandboxing/auto-review.md)

Auto-review 会用一个单独的
审查代理替代沙箱边界处的人工审批。主 Codex 代理仍在同一个沙箱内运行，使用
相同的审批策略，以及相同的网络和文件系统限制。
区别在于由谁审查符合条件的提权请求。

Auto-review 只在审批是交互式时适用。实践中，这
意味着 `approval_policy = "on-request"`，或仍会显示相关提示类别的细粒度审批策略。使用 `approval_policy = "never"` 时，
没有内容需要审查。

#### 自动审查如何工作

概括来说，流程如下：

1. 主代理在 `read-only` 或 `workspace-write` 内工作。
2. 当它需要跨越沙箱边界时，会请求审批。
3. 如果 `approvals_reviewer = "auto_review"`，Codex 会将该审批请求
   路由给单独的审查代理，而不是停下来等待人工。
4. 审查代理决定是否应运行该操作，并返回理由。
5. 如果操作被批准，执行继续。如果被拒绝，主
   代理会被指示寻找实质上更安全的路径，或停止并询问
   用户。

Auto-review 是审查者替换，而不是权限授予。它不会扩大
`writable_roots`、启用网络访问，或削弱受保护路径。它只
改变 Codex 处理已经需要审批的操作的方式。

#### 何时触发

Auto-review 会评估否则会暂停等待人工的审批请求。
这些包括：

- 请求提权沙箱权限的 shell 或 exec 工具调用。
- 被当前沙箱或策略阻止的网络请求。
- 允许的 writable roots 之外的文件编辑。
- 根据工具标注或配置的审批模式需要审批的 MCP 或 app 工具调用。
- Browser Use 访问新网站或域。

Auto-review 不会针对沙箱内已允许的常规操作运行。如果命令可以在活动 `sandbox_mode` 下运行，或工具调用
保持在允许的策略内，主代理会继续，无需审查。

Computer Use 是单独情况。Computer Use 的 app 审批仍会
直接显示给用户，因此 Auto-review 不会替代这些 app 级提示。

#### 自动审查会阻止什么

概括来说，Auto-review 旨在阻止如下操作：

- 将私有数据、密钥或凭据发送到不受信任的目的地
- 探测凭据、令牌、cookie 或会话材料
- 广泛或持久地削弱安全性
- 具有重大不可逆损害风险的破坏性操作

确切策略位于开源 Codex 仓库：
[policy_template.md](https://github.com/openai/codex/blob/main/codex-rs/core/src/guardian/policy_template.md)
和
[policy.md](https://github.com/openai/codex/blob/main/codex-rs/core/src/guardian/policy.md)。
该策略可按企业使用 `guardian_policy_config` 自定义，或
按用户使用本地 [`[auto_review].policy`](https://developers.openai.com/codex/config-advanced#approval-policies-and-sandbox-modes) 自定义。

#### 审查代理会看到什么

审查代理本身是一个 Codex 代理，但任务比主代理更窄：
决定某个特定跨边界操作是否应运行。

审查代理会看到精简转录和确切的审批请求。这
通常包括用户消息、显示给用户的 assistant 更新、相关工具
调用和工具输出，以及当前被提议批准的操作。它也可以
执行只读检查以收集缺失上下文，但很少这样做。

隐藏的 assistant 推理不包含在内。Auto-review 看到的是保留的
对话 item 和工具证据，而不是私有思维链。

#### 拒绝和失败行为

明确拒绝不会被当作普通沙箱错误。Codex 会将
审查理由返回给主代理，并添加更强的指令：

- 不要通过变通方法、间接执行或规避策略来追求相同结果。
- 仅在存在实质上更安全的替代方案时继续。
- 否则，停止并询问用户。

Codex 还会按轮次应用拒绝断路器。在当前
开源实现中，Auto-review 会在同一轮次内连续 `3`
次拒绝，或最近 `50` 次审查的滚动窗口中出现 `10` 次拒绝后中断该轮次。

任何非拒绝都会重置连续拒绝计数器。当断路器触发时，
Codex 会发出警告，并以 interrupt 中止当前轮次，而不是
让代理在更多提权尝试上循环。

超时会与明确拒绝分开显示，主代理会
被告知超时本身并不能证明该操作不安全。

对于被拒绝的 action，也存在显式 override 路径。在当前
开源 TUI 中，运行 `/approve` 打开 **Auto-review Denials** 选择器，然后
选择一个最近被拒绝的操作，批准它重试一次。Codex 每个线程最多记录 10 个
近期拒绝。该审批范围很窄：它适用于确切的
被拒绝操作，而不是类似的未来操作；它会在同一上下文中记录用于一次重试；并且重试仍会经过 Auto-review。在底层，
Codex 会为该确切操作注入开发者作用域的审批标记。
审查代理随后会将该显式用户覆盖视为上下文，但它仍会遵循
策略，如果策略认为用户不能覆盖该类
拒绝，它仍可再次拒绝。

#### 配置

设置详情请参阅
[Managed configuration](https://developers.openai.com/codex/enterprise/managed-configuration#configure-automatic-review-policy)。

默认审查策略位于开源 Codex 仓库：
[core/src/guardian/policy.md](https://github.com/openai/codex/blob/main/codex-rs/core/src/guardian/policy.md)。
企业可以使用托管要求中的
`guardian_policy_config` 替换其租户特定部分。个人用户也可以在其 `config.toml` 中设置本地
[`[auto_review].policy`](https://developers.openai.com/codex/config-advanced#approval-policies-and-sandbox-modes)，
但托管要求优先级更高：

```toml
[auto_review]
policy = """
YOUR POLICY GOES HERE
"""
```

要自定义策略，请先复制整个默认策略文本，然后
根据你的具体风险画像迭代。

#### 在不削弱安全性的情况下降低审查量

当沙箱已经覆盖常见安全
工作流时，Auto-review 效果最好。如果过多日常操作需要审查，请先修复边界，
而不是教审查代理永久批准噪声很大的提权请求。

实践中，杠杆最高的变更是：

- 为你有意使用的临时目录或相邻仓库添加狭窄的
  [`writable_roots`](https://developers.openai.com/codex/config-advanced#approval-policies-and-sandbox-modes)。
- 添加窄作用域的 [prefix rules](https://developers.openai.com/codex/rules)。相比 `["python"]` 或 `["curl"]` 等宽泛
  模式，优先选择精确命令
  前缀，例如 `["cargo", "test"]` 或 `["pnpm", "run", "lint"]`。宽泛规则往往会抹掉
  Auto-review 旨在守护的边界。

默认情况下，Auto-review 会话转录会保留在 `~/.codex/sessions` 下，
因此你可以在更改策略或权限之前，让 Codex 分析那里的历史流量。

#### 限制

Auto-review 改善了长期运行代理式工作的默认操作点，
但它不是确定性的安全保证。

- 它只评估请求跨越边界的操作。
- 它仍可能犯错，尤其是在对抗性或异常上下文中。
- 它应补充而不是替代良好的沙箱设计、监控和
  组织特定策略。

研究动机和已发布评估结果请参阅
[Alignment Research post on Auto-review](https://alignment.openai.com/auto-review/)。
