### 权限

Source: [Permissions](https://developers.openai.com/codex/permissions.md)

#### 定义并选择配置档

Codex 包含三个内置权限配置档：

- `:read-only` 让本地命令执行保持只读。
- `:workspace` 允许在活动 workspace roots 和系统临时目录内写入。
- `:danger-full-access` 移除本地沙箱限制，并且只应在明确需要这种广泛访问时使用。

在 `[permissions.]` 下创建命名配置档，然后将顶层 `default_permissions` key 设置为该配置档名称或上面的某个内置值。在此示例中，`project-edit` 是用户定义的配置档名称，不是内置值。

自定义配置档使用两个相关概念：

- `[permissions..workspace_roots]` 添加应计入该配置档的 workspace roots 的具体目录。
- `[permissions..filesystem.":workspace_roots"]` 定义 Codex 在每个有效 workspace root 内应用的 filesystem rules：当前会话的运行时 workspace roots 加上上面由 profile 定义的 roots。

配置档也使用常规配置层模型。更高优先级的层可以在同一配置档名下添加或替换条目，而无需重述整个配置档。

例如，组织级配置和用户级配置可以独立扩展同一个配置档：

```toml
# /etc/codex/config.toml
[permissions.server.workspace_roots]
"~/code/server" = true
```

```toml
# ~/.codex/config.toml
[permissions.server.workspace_roots]
"~/code/mobile-app" = true
```

当 `server` 处于活动状态时，两个 workspace roots 都会参与有效配置档。

```toml
default_permissions = "project-edit"

[permissions.project-edit.workspace_roots]
"~/code/app" = true
"~/code/shared-lib" = true

[permissions.project-edit.filesystem]
":minimal" = "read"

[permissions.project-edit.filesystem.":workspace_roots"]
"." = "write"
".devcontainer" = "read"
"**/*.env" = "deny"

[permissions.project-edit.network]
enabled = true

[permissions.project-edit.network.domains]
"api.openai.com" = "allow"
"objects.githubusercontent.com" = "allow"
"*.github.com" = "allow"
"tracking.example.com" = "deny"
```

此配置档：

- 读取常见开发者工具所需的最小运行时路径。
- 将相同 workspace-root 规则应用于当前会话和配置档定义的 roots。
- 在每个 root 下保持 `.devcontainer/` 等 IDE 相关设置为只读。
- 用 glob 规则拒绝匹配的环境文件。
- 仅通过配置的域名策略允许网络访问。

在活动配置档内，即使更宽泛的路径可读或可写，更窄的 deny 规则仍然生效。例如，一个配置档可以让 workspace roots 可写，同时仍将匹配的 `.env` 路径设置为 `deny`。

#### 扩展配置档

当一个配置档与内置配置档或另一个命名配置档基本相同时，使用 `extends`。建议扩展内置配置档，而不是从零开始，这样基线保护会继续保留。例如，扩展 `:workspace` 会保持 workspace root 的 `.codex` 目录只读，除非你显式覆盖。设置一次父级，然后只添加或覆盖不同的规则。

```toml
default_permissions = "project-edit"

[permissions.project-edit]
description = "Project editing with OpenAI API access."
extends = ":workspace"

[permissions.project-edit.filesystem.":workspace_roots"]
"**/*.env" = "deny"

[permissions.project-edit.network]
enabled = true

[permissions.project-edit.network.domains]
"api.openai.com" = "allow"
```

此配置档从 `:workspace` 开始，保持匹配的 `.env` 文件被拒绝，并允许请求 `api.openai.com`。一个配置档可以扩展 `:read-only`、`:workspace` 或另一个命名配置档。它不能扩展 `:danger-full-access`；Codex 也会拒绝未知父级和继承循环。
