### 权限

Source: [Permissions](https://developers.openai.com/codex/permissions.md)

Beta。权限配置档仍在积极开发中，未来可能变化。

权限配置档不会与旧版沙箱设置组合使用。请配置 `default_permissions` 和 `[permissions]`，或者配置 `sandbox_mode` / `sandbox_workspace_write`，不要两者同时使用。如果任何已加载的配置文件中出现 `sandbox_mode`、你传入了 `--sandbox`，或者所选配置档设置了 `sandbox_mode`，Codex 会使用这些旧版沙箱设置，而不是 `default_permissions`。

托管的 `allowed_permission_profiles` 是例外：它会让 Codex 使用权限配置档。部署托管配置档 allowlist 前，请移除 `sandbox_mode` 和 `[sandbox_workspace_write]` 等旧设置。对于混合版本的企业 rollout，可以暂时保留托管的 `allowed_sandbox_modes` 要求作为兼容约束，直到所有客户端都运行 Codex 0.138.0 或更高版本。

权限配置档可让你为 Codex 代表你运行的本地命令应用最小权限边界。配置档是一条命名策略，组合了文件系统规则和网络规则：文件系统规则定义命令可以读取或写入什么，网络规则定义命令可以访问哪些目标。

使用配置档可以给 Codex 当前任务所需的足够访问权限，而不授予对你的机器或网络的广泛访问。例如，只读配置档可让 Codex 检查项目而不编辑它；可写配置档可将编辑限制在选定的 workspace roots 内。

本地权限配置档支持 macOS、Linux、WSL 和原生 Windows。平台特定细节和注意事项请参阅[范围与执行](#范围与执行)。

Codex cloud 的网络设置请参阅 [Internet Access](23-agent-internet-access.md)。

## 定义并选择配置档

Codex 包含三个内置权限配置档：

- `:read-only` 让本地命令执行保持只读。
- `:workspace` 允许在活动 workspace roots 和系统临时目录内写入。
- `:danger-full-access` 移除本地沙箱限制，并且只应在明确需要这种广泛访问时使用。

在 `[permissions.<name>]` 下创建命名配置档，然后将顶层 `default_permissions` key 设置为该配置档名称或上面的某个内置值。在此示例中，`project-edit` 是用户定义的配置档名称，不是内置值。

企业管理员可以通过托管的 `requirements.toml` 定义配置档，并限制用户可以选择哪些配置档。一旦出现 `allowed_permission_profiles`，未列出的配置档都会被拒绝，包括未列出的内置配置档和未来 Codex 版本添加的配置档。推荐的托管配置请参阅[控制可用权限配置档](67-managed-configuration.md#control-available-permission-profiles)。

自定义配置档使用两个相关概念：

- `[permissions.<name>.workspace_roots]` 添加应计入该配置档 workspace roots 的具体目录。
- `[permissions.<name>.filesystem.":workspace_roots"]` 定义 Codex 在每个有效 workspace root 内应用的文件系统规则：当前会话的运行时 workspace roots，加上上面由配置档定义的 roots。

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
- 只通过配置的域名策略允许网络访问。

在活动配置档内，即使更宽泛的路径可读或可写，更窄的 deny 规则仍然生效。例如，一个配置档可以让 workspace roots 可写，同时仍将匹配的 `.env` 路径设置为 `deny`。

## 扩展配置档

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

此配置档从 `:workspace` 开始，保持匹配的 `.env` 文件被拒绝，并允许请求 `api.openai.com`。配置档可以扩展 `:read-only`、`:workspace` 或另一个命名配置档。它不能扩展 `:danger-full-access`；Codex 也会拒绝未知父级和继承循环。

## 配置规范

| 条目 | 类型 / 取值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `default_permissions` | 字符串配置档名称 | 无 | 命名 Codex 默认应用的权限配置档。它必须匹配 `[permissions]` 下的某个配置档，或 `:workspace` 等内置配置档。请显式设置它以获得可预测行为；只有在 `:workspace` 和 `:read-only` 都被显式允许时，托管要求才可以省略它。除非托管的 `allowed_permission_profiles` 告诉 Codex 在此设置中使用权限配置档，否则 Codex 会使用旧版沙箱设置。 |
| `[permissions.<name>]` | 表 | 无 | 定义命名配置档。`default_permissions` 选择一个配置档作为默认值；其他权限配置档设置也使用配置档名称。 |
| `permissions.<name>.description` | 字符串 | 无 | 为配置档提供人类可读的说明。配置档不会通过 `extends` 继承父级的说明。 |
| `permissions.<name>.extends` | 字符串配置档名称 | 无 | 从另一个命名配置档或内置 `:read-only` / `:workspace` 配置档开始构建此配置档。Codex 会拒绝 `:danger-full-access`、未知父级和继承循环。 |
| `[permissions.<name>.workspace_roots]` | 表 | 无 | 添加由配置档定义的 workspace roots，让它们与当前会话的运行时 workspace roots 一起接收 `:workspace_roots` 文件系统规则。 |
| `permissions.<name>.workspace_roots."<path>"` | Boolean | `false` | 当为 `true` 时，将该路径加入配置档的 workspace root 集合。设置为 `false` 的条目保持不活动。 |
| `[permissions.<name>.filesystem]` | 表 | 无 | 将文件系统路径映射到访问值或作用域子路径映射。缺失或空的 filesystem 表会保持文件系统访问受限，并发出启动警告。 |
| `permissions.<name>.filesystem.glob_scan_max_depth` | Number | 无 | 在 Linux、WSL 和原生 Windows 上，当 Codex 在沙箱启动前快照匹配项时，限制 deny-read glob 展开的深度。较大的值会增加启动扫描工作。无界 `**` 模式需要有界预展开时，请使用至少为 `1` 的值。 |
| `[permissions.<name>.filesystem]."<path>"` | `read`、`write` 或 `deny` | 无 | 为受支持路径授予直接访问。`deny` 会拒绝访问，并优先于同等具体度的 `write` 或 `read` 条目。Codex 会拒绝当前运行时无法执行的直接 write 规则。 |
| `[permissions.<name>.filesystem."<path>"]."<subpath>"` | `read`、`write` 或 `deny` | 无 | 授予对 `<path>` 后代的访问。使用 `.` 表示基准路径。其他 subpaths 必须是相对后代，且不能包含 `.` 或 `..` 组件。 |
| `[permissions.<name>.network]` | 表 | 无 | 为该配置档配置网络沙箱代理和沙箱网络策略。 |
| `permissions.<name>.network.enabled` | Boolean | `false` | 为该配置档中的沙箱化命令启用网络访问。这会改变沙箱网络策略；它本身不会启动网络代理。 |
| `[permissions.<name>.network.domains]` | 表 | 无 | 将 host patterns 映射到 `allow` 或 `deny`。如果没有 `allow` 条目，域名请求会被阻止。Deny 条目会覆盖 allow 条目。 |
| `permissions.<name>.network.domains."<pattern>"` | `allow` 或 `deny` | 无 | 支持精确 host、表示子域名的 `*.example.com`、表示 apex 加子域名的 `**.example.com`，以及作为仅 allow 全局通配符的 `*`。Host patterns 会通过修剪、转小写、去除尾随点，以及去除简单端口或括号来规范化。 |
| `[permissions.<name>.network.unix_sockets]` | 表 | 无 | 映射 Unix socket allowlist 覆盖。仅用于 Docker 等本地集成。 |
| `permissions.<name>.network.unix_sockets."<path>"` | `allow` 或 `deny` | 无 | 使用 `allow` 将绝对 Unix socket 路径加入有效 allowlist，或使用 `deny` 拒绝它。被拒绝的条目会从有效 allowlist 中省略。 |
| `permissions.<name>.network.proxy_url` | URL 字符串 | `http://127.0.0.1:3128` | 用于 `HTTP_PROXY`、`HTTPS_PROXY`、websocket 代理变量和相关工具代理环境变量的 HTTP 代理 listener。 |
| `permissions.<name>.network.enable_socks5` | Boolean | `true` | 启用用于 `ALL_PROXY` 和 FTP 代理变量的 SOCKS5 listener。 |
| `permissions.<name>.network.socks_url` | URL 字符串 | `http://127.0.0.1:8081` | SOCKS5 listener 地址。 |
| `permissions.<name>.network.enable_socks5_udp` | Boolean | `true` | 在 SOCKS5 listener 启用时启用 SOCKS5 UDP 支持。 |
| `permissions.<name>.network.allow_upstream_proxy` | Boolean | `true` | 允许网络沙箱代理在出站请求中遵循上游 `HTTP(S)_PROXY` 和 `ALL_PROXY` 设置。 |
| `permissions.<name>.network.allow_local_binding` | Boolean | `false` | 当为 `true` 时，禁用本地/私有网络防护。当为 `false` 时，`localhost` 或 `127.0.0.1` 等精确本地字面量必须显式加入 allowlist，解析到本地或私有 IP 的主机名仍会被阻止。 |
| `permissions.<name>.network.dangerously_allow_non_loopback_proxy` | Boolean | `false` | 允许代理 listener 绑定非 loopback 地址。普通本地开发应保持未设置。 |
| `permissions.<name>.network.dangerously_allow_all_unix_sockets` | Boolean | `false` | 在支持 Unix socket 代理的位置绕过 Unix socket allowlist。这是一个范围很大的本地逃逸口。 |

## 文件系统权限

文件系统条目使用 `read`、`write` 或 `deny`：

| 访问 | 含义 |
| --- | --- |
| `read` | 允许命令读取文件并列出该路径下的目录。命令不能在那里创建、修改、重命名或删除文件。 |
| `write` | 允许命令读取和修改该路径下的文件，包括在 OS 允许时创建、重命名和删除文件。 |
| `deny` | 拒绝该路径下的读取和写入。可用它从更宽泛的 `read` 或 `write` 授权中切出一个被拒绝的子路径。 |

更具体的条目会覆盖更宽泛的条目。当两个条目指向同一路径时，`deny` 优先于 `write`，`write` 优先于 `read`。

这种优先级让配置档可以先描述一个宽泛工作区域，然后切出应保持不可读的文件或目录：

```toml
[permissions.project-edit.filesystem]
":minimal" = "read"

[permissions.project-edit.filesystem.":workspace_roots"]
"." = "write"
".devcontainer" = "read"
"**/*.env" = "deny"
```

在此示例中，workspace root 保持可写，`.devcontainer/` 保持可读但不可写，匹配的环境文件对沙箱化命令仍不可用。

更具体的路径也可以在更宽泛的 deny 内重新打开更窄的子树：

```toml
[permissions.project-edit.filesystem]
"~/Documents" = "deny"
"~/Documents/codex" = "write"
```

支持的路径形式：

| 路径 | 含义 | 作用域子路径 |
| --- | --- | --- |
| `:root` | 文件系统根目录 | 仅 `.` |
| `:minimal` | 常见工具所需的平台和运行时路径 | 仅 `.` |
| `:workspace_roots` | 当前会话的 workspace roots 加上任何启用的配置档定义 workspace roots | 是 |
| `:tmpdir` | 可用时的 `$TMPDIR` 位置 | 仅 `.` |
| `:slash_tmp` | 如果存在，则为 `/tmp` 文件夹 | 仅 `.` |
| `/absolute/path` | 平台绝对路径，例如 macOS/Linux/WSL 上的 `/path`，或原生 Windows 上的 `C:\path` | 是 |
| `~/path` | 当前用户 home 目录下的路径 | 是 |

在原生 Windows 上，home-relative paths 也可以使用反斜杠，例如 `~\work`。

只有当配置档确实需要宽泛读取覆盖时，才使用 `:root`：

```toml
[permissions.audit.filesystem]
":root" = "read"
```

在 `:workspace_roots` 下使用嵌套条目，可将访问限定到相对于 workspace root 的子路径：

```toml
[permissions.project-edit.filesystem.":workspace_roots"]
"." = "write"          # each workspace root
"docs" = "read"        # each workspace-root docs directory
"generated" = "deny"   # each workspace-root generated directory
```

嵌套子路径必须保持在其 workspace root 内。`../other-repo` 等父级遍历会被拒绝。

### 使用精确路径或 globs 拒绝读取

对于 Codex 不应读取的文件或子树，请使用 `deny`，即使附近有更宽泛的配置档规则授予了访问。精确路径适合 `~/.ssh` 等稳定位置。Glob patterns 更适合覆盖一类敏感文件，尤其是这些文件在不同仓库中的精确位置会变化时。

当 glob 位于 `:workspace_roots` 下时，Codex 会相对于每个有效 workspace root 解释它。例如：

```toml
[permissions.project-edit.filesystem.":workspace_roots"]
"**/*.env" = "deny"
```

此规则会拒绝读取每个运行时或配置档定义 workspace root 下匹配的 `.env` 文件。当你想保留正常 workspace 写入，同时让环境文件、生成的 secrets 或类似带凭据的文件保持不可读时，请使用它。

`deny` glob patterns 支持作为 deny-read 规则。`read` 或 `write` globs 在 Linux、WSL 和原生 Windows 沙箱中可移植性较低，因此尽可能优先使用精确路径，或使用 `"docs/**" = "read"` 等子树规则。

在 Linux、WSL 和原生 Windows 上，无界 `**` deny-read pattern 可能需要在沙箱启动前进行有界预展开。使用 `"**/*.env" = "deny"` 这类无界模式时，请设置 `glob_scan_max_depth`：

```toml
[permissions.project-edit.filesystem]
glob_scan_max_depth = 3

[permissions.project-edit.filesystem.":workspace_roots"]
"**/*.env" = "deny"
```

`glob_scan_max_depth` 必须至少为 `1`。更高的值会在沙箱启动前扫描更深层级，这会增加 Linux、WSL 和原生 Windows 上的启动工作。如果不想使用有界展开，可以枚举显式深度，例如 `*.env`、`*/*.env` 和 `*/*/*.env`。

当相同规则应应用到当前会话 root 之外的更多位置时，请向配置档添加可复用 workspace roots：

```toml
[permissions.project-edit.workspace_roots]
"~/code/app" = true
"~/code/shared-lib" = true
```

当此配置档处于活动状态时，Codex 会把 `:workspace_roots` 规则应用到当前会话的运行时 workspace roots，以及每个已启用的配置档定义 workspace root。

在原生 Windows 上，支持 `D:\work` 等盘符路径，也支持 `\\server\share` 等 UNC 路径作为绝对路径。

## 网络权限

设置 `enabled = true` 可为所选配置档允许网络访问：

```toml
[permissions.project-edit.network]
enabled = true
```

启用网络访问后，Codex 默认使用完整网络行为。多数配置档也应定义域名规则：

```toml
[permissions.project-edit.network.domains]
"example.com" = "allow"      # exact host
"*.example.com" = "allow"    # subdomains only
"**.example.com" = "allow"   # apex and subdomains
"ads.example.com" = "deny"   # deny wins over allow
```

网络沙箱代理默认绑定到本地 listeners：

```toml
[permissions.project-edit.network]
enabled = true
proxy_url = "http://127.0.0.1:3128"
enable_socks5 = true
socks_url = "http://127.0.0.1:8081"
enable_socks5_udp = true
```

除非你正在与特定运行时集成，否则请保留这些 listener 设置的默认值。`dangerously_*` 网络 key 是专用环境的逃逸口，不应用于普通本地开发。

### 本地和私有网络

Codex 默认应用本地/私有网络防护，以防御 DNS rebinding 和意外访问本地服务。若要有意允许字面本地目标，请将精确 host 或 IP 字面量加入 allowlist：

```toml
[permissions.project-edit.network.domains]
"localhost" = "allow"
"127.0.0.1" = "allow"
```

只有当配置档必须访问解析到本地或私有地址的 allowlisted 主机名时，才设置 `allow_local_binding = true`：

```toml
[permissions.project-edit.network]
enabled = true
allow_local_binding = true

[permissions.project-edit.network.domains]
"localhost" = "allow"
```

### Unix sockets

Unix socket 代理是 Docker 等工具使用的本地逃逸口。请谨慎使用：

```toml
[permissions.project-edit.network.unix_sockets]
"/var/run/docker.sock" = "allow"
"/tmp/old.sock" = "deny"
```

使用 `deny` 可以拒绝一个 socket 路径，包括继承来的 allow 条目。被拒绝的 socket 路径会从有效 allowlist 中省略。

启用 Unix sockets 时，请让代理 listeners 绑定到 loopback 地址。

## 从旧版沙箱设置迁移

当你希望用一个可复用配置档同时描述文件系统和网络行为时，权限配置档会取代旧版的 `sandbox_mode` 与 `sandbox_workspace_write` 组合。一个会话请使用其中一种系统，不要混用。

建议起点：

- 对于只读工作流，使用内置 `:read-only` 配置档，或定义一个只在需要位置授予读取访问的自定义配置档。
- 对于 workspace 编辑，使用内置 `:workspace` 配置档，或定义一个通过 `:workspace_roots` 写入的自定义配置档，并只添加工作流所需的额外 temp 或 cache 路径。
- 对于不受限制的本地执行，只有当你确实想要最宽泛的本地访问模型时才使用 `:danger-full-access`。

配置档描述会话的本地默认姿态。组织托管要求仍然可以添加用户配置不应放宽的限制。管理员强制执行的文件系统和网络约束请参阅[托管配置](67-managed-configuration.md)。

## 范围与执行

权限配置档定义本地沙箱化命令执行的边界。请将它们与审批策略，以及其他 Codex surface 的独立控制一起使用。

### 配置档控制什么

- **本地命令执行：** 权限配置档约束在你的机器上运行的沙箱化命令。App connectors、MCP servers、browser 或 computer-use surfaces、Codex cloud 环境设置，以及已批准的 escalations 都使用各自的控制。
- **文件系统写入：** 可写配置档可以创建持久变更。对脚本、构建步骤、包管理器 hooks、shell 启动文件和共享目录的写入应视为敏感，因为后续工具或用户可能在原始沙箱上下文之外执行这些文件。
- **出站目标：** 网络域名规则约束沙箱化命令流量可以通过网络代理前往哪里。它们不判断允许目标是否可信，通配符 allow 规则仍然很宽泛。
- **本地服务：** 本地和私有网络目标默认被阻止。将 `localhost`、私有 IP、Unix sockets 加入 allowlist，或设置 `allow_local_binding = true`，都会显式打开对本地服务的访问。

### 执行方式

- 在 macOS 上，Codex 使用 Seatbelt 沙箱配置档。如果所选策略无法由平台沙箱执行，Codex 会拒绝运行命令，而不是静默地以未沙箱化方式运行。
- 在 Linux 和 WSL 上，Codex 使用 [bubblewrap](https://github.com/containers/bubblewrap) 和 [seccomp](https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html)，并在兼容性 fallback 路径中使用 Landlock。最强执行路径取决于 user namespaces 和 kernel 支持；受限 container hosts 可能迫使 Codex 使用兼容路径，不受支持的 split policies 会被拒绝。
- 在原生 Windows 上，[`elevated` 沙箱](83-windows-platform.md#windows-sandbox) 最强，因为它可以使用专门的低权限沙箱用户、文件系统权限边界和防火墙规则。`unelevated` 沙箱是较弱网络隔离的 fallback，不能执行每个 split read/write carveout，因此不受支持的策略会被拒绝。当你需要 Linux 沙箱模型时，请使用 WSL。

### 操作建议

选择仍能完成任务的最窄配置档，尤其是在授予写入或出站网络访问时。让审批策略、secret 处理和 allow 规则与该访问级别保持一致。

## 常见配置档

### 带网络 allowlist 的只读配置档

```toml
default_permissions = "readonly-net"

[permissions.readonly-net.filesystem]
":minimal" = "read"

[permissions.readonly-net.filesystem.":workspace_roots"]
"." = "read"

[permissions.readonly-net.network]
enabled = true

[permissions.readonly-net.network.domains]
"api.openai.com" = "allow"
```

### 文件访问仅限 workspace

下面示例会让 Codex 可写你的 workspace 文件夹，同时拒绝读取文件系统其余部分（少量例外由 `:minimal` 决定）。

```toml
default_permissions = "workspace-only"

[permissions.workspace-only]
# By extending the :workspace profile, you get Codex's safeguards to ensure
# subfolders such as .codex/ and .git/ within a workspace root are read-only
# while the rest of the folder is writable.
extends = ":workspace"

[permissions.workspace-only.filesystem]
# By default, deny read access to all files on disk.
":root" = "deny"

# Though in practice, a software agent needs to be able to read folders that
# contain common tools, such as `/usr/bin`, to get work done, so grant access
# to a "minimal" set of files and folders, as determined by Codex.
":minimal" = "read"

# By extending the :workspace profile, :tmpdir and :slash_tmp are "write" by
# default, though you can deny access to them altogether, if desired.
":tmpdir" = "deny"
":slash_tmp" = "deny"
```

### 无网络的 workspace 写入

```toml
default_permissions = "project-edit"

[permissions.project-edit.filesystem]
":minimal" = "read"

[permissions.project-edit.filesystem.":workspace_roots"]
"." = "write"

[permissions.project-edit.network]
enabled = false
```

### 带公共 Web 访问的 workspace 写入

```toml
default_permissions = "workspace-net"

[permissions.workspace-net.filesystem]
":minimal" = "read"

[permissions.workspace-net.filesystem.":workspace_roots"]
"." = "write"

[permissions.workspace-net.network]
enabled = true

[permissions.workspace-net.network.domains]
"*" = "allow"
```

只有当你确实想允许公共网络访问时，才使用全局 `"*"` allow 规则。Deny 规则可以收窄宽泛 allowlist。
