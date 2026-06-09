### 智能体审批和安全

Source: [Agent approvals & security](https://developers.openai.com/codex/agent-approvals-security.md)

Codex 帮助保护你的代码和数据，并降低滥用风险。

本页介绍如何安全地操作 Codex，包括沙箱、审批
和网络访问。如果你正在寻找 Codex Security，即用于
扫描已连接 GitHub 仓库的产品，请参见 [Codex Security](71-codex-security.md)。

默认情况下，代理运行时会关闭网络访问。在本地，Codex 使用由操作系统强制执行的沙箱，限制它可以接触的内容（通常限于当前工作区），并配合审批策略来控制它在执行操作前何时必须停下来询问你。

关于沙箱如何在 Codex app、IDE
扩展和 CLI 中工作的高层解释，请参见 [沙箱](15-sandbox.md)。
如需更广泛的企业安全概览，请参见 [Codex 安全白皮书](https://trust.openai.com/?itemUid=382f924d-54f3-43a8-a9df-c39e6c959958&source=click)。

#### 沙箱和审批

Codex 安全控制来自两个协同工作的层：

- **沙箱模式**：当 Codex 执行模型生成的命令时，它在技术上能做什么（例如可以在哪里写入，以及是否可以访问网络）。
- **审批策略**：Codex 在执行某个动作前何时必须询问你（例如离开沙箱、使用网络，或在可信集合之外运行命令）。

Codex 会根据你运行它的位置使用不同的沙箱模式：

- **Codex cloud**：在 OpenAI 管理的隔离容器中运行，防止访问你的主机系统或无关数据。使用两阶段运行时模型：setup 在代理阶段之前运行，并可访问网络以安装指定依赖；随后代理阶段默认离线运行，除非你为该环境启用互联网访问。为云端环境配置的 secrets 只在 setup 期间可用，并会在代理阶段开始前移除。
- **Codex CLI / IDE 扩展**：由操作系统级机制强制执行沙箱策略。默认设置包括无网络访问，以及写权限仅限于活动工作区。你可以基于自己的风险承受度配置沙箱、审批策略和网络设置。

在 `Auto` 预设中（例如 `--sandbox workspace-write --ask-for-approval on-request`），Codex 可以自动读取文件、进行编辑，并在工作目录中运行命令。

Codex 会在编辑工作区外文件或运行需要网络访问的命令时请求审批。如果你想聊天或规划而不做变更，请使用 `/permissions` 命令切换到 `read-only` 模式。

Codex 也可以对声明有副作用的 app（connector）工具调用触发审批，即使该动作不是 shell 命令或文件变更。破坏性 app/MCP 工具调用在工具声明破坏性标注时始终需要审批，即使它同时声明了其它提示（例如只读提示）。

#### 网络访问

对于 Codex app、CLI 或 IDE 扩展，默认的 `workspace-write` 沙箱模式会保持网络访问关闭，除非你在配置中启用：

```toml
[sandbox_workspace_write]
network_access = true
```

#### 网络隔离

网络访问通过目的地规则控制，这些规则适用于由命令生成的脚本、
程序和子进程。当命令网络访问已经启用时，开启 `network_proxy` 功能可以将该流量限制到你配置的网络策略中。

```toml
[features.network_proxy]
enabled = true
domains = { "api.openai.com" = "allow", "example.com" = "deny" }
```

对于一次性 CLI 会话，如果只需要切换开关，请使用布尔简写；
如果还要设置策略选项，请使用表格形式：

```bash
codex \
  -c 'features.network_proxy=true' \
  -c 'sandbox_workspace_write.network_access=true'

codex \
  -c 'features.network_proxy.enabled=true' \
  -c 'features.network_proxy.domains={ "api.openai.com" = "allow", "example.com" = "deny" }' \
  -c 'sandbox_workspace_write.network_access=true'
```

该功能会改变已启用网络访问的执行方式；它本身不会授予
网络访问。使用带 `workspace-write` 配置的
`sandbox_workspace_write.network_access` 来决定命令是否完全拥有网络访问：

- 网络关闭 + `network_proxy` 开启：网络保持关闭，该功能不起作用。
- 网络开启 + `network_proxy` 关闭：网络保持开启，并拥有不受限制的直接
  出站访问。
- 网络开启 + `network_proxy` 开启：网络保持开启，出站流量会被
  配置的网络策略约束。

管理员管理的 `experimental_network` requirements 独立于用户
功能开关。它们可以配置并启动沙箱网络，而无需
`features.network_proxy`，但当活动
沙箱保持网络关闭时，它们不会开启网络访问。参见 [托管配置](67-managed-configuration.md#configure-network-access-requirements)
了解管理员侧 `requirements.toml` 的形状。

#### 网络策略

域名规则以允许列表优先：

- 精确主机只匹配自身。
- `*.example.com` 匹配 `api.example.com` 等子域，但不匹配
  `example.com`。
- `**.example.com` 同时匹配根域和子域。
- 全局 `*` allow 规则匹配任何未被 deny 的公共主机。请将 `*`
  视为广泛网络访问，并在可行时优先使用范围明确的规则。
- `deny` 始终优先于 `allow`，且全局 `*` 只对 allow 规则有效。

#### 本地和私有目的地

默认情况下，`allow_local_binding = false` 会阻止 loopback、link-local 和
私有目的地：

- 特定例外：当命令需要某个本地目标时，添加精确的本地 IP 字面量或 `localhost` allow 规则。
- 更广泛访问：仅当你有意希望获得更宽泛的本地/私有访问时，才设置 `allow_local_binding = true`。
- 通配符：通配符规则不算作明确的本地例外。
- 解析地址：解析到本地/私有 IP 的主机名即使匹配允许列表，仍会被阻止。

#### DNS 重绑定保护

在允许某个主机名之前，Codex 会执行尽力而为的 DNS 和 IP
分类检查：

- 查询失败或超时会被阻止。
- 解析到非公共地址的主机名会被阻止。
- 该检查降低 DNS 重绑定风险，但不能消除它。要完全防止
  重绑定，需要在传输层固定已解析 IP。

如果恶意 DNS 在威胁范围内，也应在更低层执行出站控制。

#### 危险设置

两个设置会有意扩大信任边界：

- `dangerously_allow_non_loopback_proxy = true` 可能会将代理监听器暴露到
  loopback 之外。
- `dangerously_allow_all_unix_sockets = true` 会绕过 Unix socket allowlist。

仅在严格受控的环境中使用它们。启用 Unix socket 代理时，
即使请求了非 loopback 绑定，监听器也会保持仅限 loopback，
因此沙箱网络不会变成通往本地守护进程的远程桥接。

`network_proxy` 默认关闭。启用它时：

| 设置                                   | 默认值  | 行为                                                                                                                                                        |
| -------------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `enabled`                              | `false` | 仅当命令网络访问已经开启时，才启动沙箱网络。                                                                                                                |
| `domains`                              | unset   | 使用允许列表行为，因此在你添加 `allow` 规则前，不允许任何外部目的地。支持精确主机、限定范围的通配符和全局 `*` allow 规则；`deny` 始终优先。                |
| `unix_sockets`                         | unset   | 在你添加显式 `allow` 规则前，不允许任何 Unix socket 目的地。                                                                                                |
| `allow_local_binding`                  | `false` | 阻止本地和私有网络目的地，除非你添加精确的本地 IP 字面量或 `localhost` allow 规则，或显式选择更广泛的本地/私有访问。                                      |
| `enable_socks5`                        | `true`  | 在策略允许时暴露 SOCKS5 支持。                                                                                                                             |
| `enable_socks5_udp`                    | `true`  | 当 SOCKS5 可用时允许通过 SOCKS5 使用 UDP。                                                                                                                  |
| `allow_upstream_proxy`                 | `true`  | 让沙箱网络遵循环境中的上游代理。                                                                                                                            |
| `dangerously_allow_non_loopback_proxy` | `false` | 保持监听端点位于 loopback，除非你有意将其暴露到 localhost 之外。                                                                                           |
| `dangerously_allow_all_unix_sockets`   | `false` | 保持 Unix socket 访问基于允许列表，除非你有意绕过该保护。                                                                                                  |

你也可以控制 [网页搜索工具](https://platform.openai.com/docs/guides/tools-web-search)，而无需授予派生命令完整网络访问。Codex 默认使用网页搜索缓存访问结果。该缓存是 OpenAI 维护的网页结果索引，因此缓存模式返回预索引结果，而不是获取实时页面。这减少了来自任意实时内容的提示注入暴露，但你仍应将网页结果视为不可信。如果你正在使用 `--yolo` 或其它 [完全访问沙箱设置](#common-sandbox-and-approval-combinations)，网页搜索默认使用实时结果。使用 `--search` 或设置 `web_search = "live"` 允许实时浏览，或将其设为 `"disabled"` 来关闭该工具：

```toml
web_search = "cached"  # default
# web_search = "disabled"
# web_search = "live"  # same as --search
```

在 Codex 中启用网络访问或网页搜索时请谨慎。提示注入可能导致代理获取并遵循不受信任的指令。

#### 默认值和建议

- 启动时，Codex 会检测文件夹是否处于版本控制下，并建议：
  - 受版本控制的文件夹：`Auto`（工作区写入 + 按需审批）
  - 不受版本控制的文件夹：`read-only`
- 根据你的设置，Codex 也可能以 `read-only` 启动，直到你明确信任工作目录（例如通过入门提示或 `/permissions`）。
- 工作区包括当前目录和 `/tmp` 等临时目录。使用 `/status` 命令查看哪些目录位于工作区中。
- 要接受默认值，请运行 `codex`。
- 你可以显式设置这些项：
  - `codex --sandbox workspace-write --ask-for-approval on-request`
  - `codex --sandbox read-only --ask-for-approval on-request`

#### 可写根目录中的受保护路径

在默认 `workspace-write` 沙箱策略中，可写根目录仍包含受保护路径：

- 无论 `/.git` 是目录还是文件，都会被保护为只读。
- 如果 `/.git` 是指针文件（`gitdir: ...`），解析后的 Git 目录路径也会被保护为只读。
- 当 `/.agents` 作为目录存在时，会被保护为只读。
- 当 `/.codex` 作为目录存在时，会被保护为只读。
- 保护是递归的，因此这些路径下的所有内容都是只读。

#### 不显示审批提示运行

你可以使用 `--ask-for-approval never` 或 `-a never`（简写）禁用审批提示。

该选项适用于所有 `--sandbox` 模式，因此你仍然可以控制 Codex 的自主级别。Codex 会在你设置的约束内尽力而为。

如果你需要 Codex 在没有审批提示的情况下读取文件、进行编辑，并运行带网络访问的命令，请使用 `--sandbox danger-full-access`（或 `--dangerously-bypass-approvals-and-sandbox` 标志）。这样做前请谨慎。

作为折中，`approval_policy = { granular = { ... } }` 允许你保持特定审批提示类别为交互式，同时自动拒绝其它类别。细粒度策略覆盖沙箱审批、execpolicy-rule 提示、MCP 提示、`request_permissions` 提示和 skill-script 审批。

#### 自动审批审查

默认情况下，审批请求会路由给你：

```toml
approvals_reviewer = "user"
```

自动审批审查会在审批为交互式时适用，例如
`approval_policy = "on-request"` 或细粒度审批策略。设置
`approvals_reviewer = "auto_review"` 可在 Codex 运行请求前，将符合条件的审批请求
路由给审查代理：

```toml
approval_policy = "on-request"
approvals_reviewer = "auto_review"
```

完整审查器生命周期、触发条件、配置优先级
和失败行为请参见
[Auto-review](65-auto-review.md)。

审查器只评估已经需要审批的动作，例如沙箱
提权、被阻止的网络请求、`request_permissions` 提示，或
有副作用的 app 和 MCP 工具调用。保持在沙箱内的动作
会继续执行，不增加额外审查步骤。

审查器策略会检查数据外泄、凭据探测、持久性
安全削弱和破坏性动作。当策略允许时，低风险和中风险动作
可以继续。策略会拒绝关键风险动作。
高风险动作需要足够的用户授权且没有匹配的 deny 规则。
提示构建、审查会话和解析失败会以关闭方式失败。超时会
单独显示，但动作仍不会运行。

[默认审查器策略](https://github.com/openai/codex/blob/main/codex-rs/core/src/guardian/policy.md)
位于开源 Codex 仓库中。企业可以在托管 requirements 中用 `guardian_policy_config` 替换其
租户特定部分。
本地 `[auto_review].policy` 文本也受支持，但托管 requirements
优先。设置细节请参见
[托管配置](67-managed-configuration.md#configure-automatic-review-policy)。

在 Codex app 中，这些审查会显示为自动审查项，其状态
例如 Reviewing、Approved、Denied、Aborted 或 Timed out。它们还可以
包含风险级别和针对被审查
请求的用户授权评估。

自动审查会使用额外模型调用，因此可能增加 Codex 用量。管理员
可以通过 `allowed_approvals_reviewers` 对其加以约束。
