### 访问令牌

Source: [Access tokens](https://developers.openai.com/codex/enterprise/access-tokens.md)

Codex 访问令牌允许受信任自动化使用 ChatGPT 工作区身份运行本地 Codex。当脚本、计划任务或 CI 运行器需要可重复、非交互的 Codex 访问时，请使用它们。

Codex 访问令牌目前支持 ChatGPT Business 和
Enterprise 工作区。

访问令牌在 ChatGPT 管理控制台的 [Access tokens](https://chatgpt.com/admin/access-tokens) 中创建。它们绑定到创建它们的 ChatGPT 用户和工作区，Codex 会将它们用作程序化本地工作流的代理身份。

如果 Platform API key 可以满足你的自动化，请继续使用 API key 身份验证。当工作流明确需要 ChatGPT 工作区
访问、ChatGPT 托管的 Codex 权益或企业工作区控制时，再使用
Codex 访问令牌。

#### 访问令牌如何工作

当 Codex 需要在没有用户完成浏览器登录的情况下运行时，使用访问令牌。该令牌代表创建它的 ChatGPT 工作区用户，因此运行可以使用该用户的 Codex 访问权限，并出现在工作区治理数据中。

Codex 会在运行开始时检查令牌，并将该运行绑定到对应的工作区身份。请像对待其它自动化密钥一样对待该令牌：将其存储在密钥管理器中，避免出现在日志中，并定期轮换。

访问令牌适用于：

- 从受信任自动化运行的 `codex exec` 作业。
- 需要可重复、非交互 Codex 运行的本地脚本。
- 使用情况应关联到 ChatGPT 工作区用户，而不是 API 组织 key 的企业工作流。

需要避免的主要风险：

- **密钥泄露：** 任何持有令牌的人都可以以令牌创建者身份启动 Codex 运行。请将令牌存储在密钥管理器中，避免出现在日志中，并定期轮换。
- **不受信任的运行器：** 公共 CI、forked pull request 或共享机器可能会把令牌暴露给工作区外部人员。仅在受信任运行器上使用访问令牌。
- **共享身份：** 在无关团队之间复用某个人的令牌，会使归属和审计轨迹更难解读。请为特定工作流所有者创建令牌。
- **陈旧凭据：** 长期有效令牌可能在工作流变化后仍保持活跃。优先使用有限过期时间，并撤销不再使用的令牌。
- **凭据类型错误：** 访问令牌用于本地 Codex 工作流。一般 OpenAI API 调用请使用 Platform API key。

#### 启用访问令牌创建

使用工作区设置中的 Codex Local 控制，为允许的成员开启访问令牌创建。

1. 前往 [Workspace Settings > Permissions & roles](https://chatgpt.com/admin/settings)。
2. 在 Codex Local 区域中，确保 **Allow members to use Codex Local** 已开启。
3. 如果所有允许的成员都应该能够创建访问令牌，请开启 **Allow members to use Codex access tokens**。
4. 如果你使用自定义角色进行更窄范围的推出，请只向需要创建令牌的组分配访问令牌权限。

请将访问令牌创建限制在理解令牌将存储在哪里、哪些自动化会使用它，以及如何轮换它的人员或服务所有者范围内。

#### 设置访问令牌过期限制

工作区所有者和管理员可以设置成员创建 Codex 访问令牌时可选择的最长过期时间。前往 [Workspace Settings > Permissions & roles](https://chatgpt.com/admin/settings)，然后在 Codex Local 区域中设置 **Access token expiration limit**。

该限制适用于新的访问令牌。现有令牌保持当前过期时间。

#### 创建访问令牌

使用 Access tokens 页面为令牌命名并选择过期时间。

1. 前往 [Access tokens](https://chatgpt.com/admin/access-tokens)。
2. 选择 **Create**。

3. 输入描述性名称，例如 `release-ci` 或 `nightly-docs-check`。

4. 选择过期时间。优先选择有限过期时间，例如 7、30、60 或 90 天。如果选择 **No expiration**，请按固定计划轮换令牌。
5. 选择 **Create**。
6. 立即复制生成的访问令牌。关闭模态框后无法再次查看它。
7. 将令牌存储到你的密钥管理器或 CI 密钥存储。

最短的自定义过期时间是一天。已撤销和已过期的令牌不能用于启动新的 Codex 运行。

#### 在 Codex CLI 中使用访问令牌

对于临时自动化，将令牌存储在 `CODEX_ACCESS_TOKEN` 中并正常运行 Codex：

```bash
export CODEX_ACCESS_TOKEN=""
codex exec --json "review this repository and summarize the top risks"
```

对于持久本地登录，请将令牌通过管道传给 `codex login --with-access-token`：

```bash
printf '%s' "$CODEX_ACCESS_TOKEN" | codex login --with-access-token
codex exec "summarize the last release diff"
```

`codex login --with-access-token` 会在 Codex 身份验证存储中存储代理身份凭据。如果你不希望在机器上持久化凭据，请改用 `CODEX_ACCESS_TOKEN` 环境变量。

#### 轮换或撤销令牌

像轮换其它自动化密钥一样轮换访问令牌：

1. 创建替换令牌。
2. 更新运行器、调度器或密钥管理器中的密钥。
3. 使用新令牌运行冒烟测试。
4. 从 [Access tokens](https://chatgpt.com/admin/access-tokens) 撤销旧令牌。

在 Access tokens 页面，工作区所有者和管理员可以撤销任何工作区令牌。拥有访问令牌权限的成员只能撤销自己创建的令牌。

#### 权限模型

访问令牌权限与一般本地 Codex 权限相互独立。成员可以访问 Codex app、CLI 或 IDE extension，但不一定被允许创建访问令牌。

| Capability                                                    | Workspace owners and admins                          | Member with access token permission           | Member without access token permission |
| ------------------------------------------------------------- | ---------------------------------------------------- | --------------------------------------------- | -------------------------------------- |
| Open [Access tokens](https://chatgpt.com/admin/access-tokens) | Yes                                                  | Yes                                           | No                                     |
| Create access tokens                                          | Yes, for their own ChatGPT workspace identity        | Yes, for their own ChatGPT workspace identity | No                                     |
| List access tokens                                            | Workspace list, including who created each token     | Only tokens they created                      | No                                     |
| Revoke access tokens from the Access tokens page              | Any token in the workspace                           | Only tokens they created                      | No page access                         |
| Grant or remove access token permission                       | Yes                                                  | No                                            | No                                     |
| Manage other Codex enterprise settings                        | Yes, based on admin role and Codex admin permissions | No, unless separately granted                 | No                                     |

简而言之：工作区所有者和管理员在工作区级别管理访问。成员需要访问令牌权限来创建和管理自己的令牌，但该权限不会授予管理员权限，也不会授予访问其它成员令牌的能力。

#### 故障排查

#### 访问令牌页面返回 404 或 forbidden

请让工作区所有者或管理员确认 Codex 访问令牌已启用，并且你的角色包含访问令牌权限。

#### `codex login --with-access-token` 失败

确认你复制的是生成的访问令牌，而不是浏览器会话令牌或 Platform API key。还要确认令牌未过期且未被撤销。

#### 相关文档

- [Authentication](18-authentication-and-sessions.md)
- [Non-interactive mode](60-non-interactive-mode.md)
- [Admin setup](64-admin-setup.md)
- [Governance](66-governance.md)
