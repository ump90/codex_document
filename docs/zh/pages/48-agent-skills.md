### 智能体技能

Source: [Agent Skills](https://developers.openai.com/codex/skills.md)

使用 agent skills 为 Codex 扩展特定任务能力。一个 skill 会打包说明、资源和可选脚本，使 Codex 能够可靠地遵循某个工作流。Skills 基于 [open agent skills standard](https://agentskills.io) 构建。

Skills 是可复用工作流的创作格式。Plugins 是 Codex 中可复用 skills 和 app 的可安装分发单元。使用 skills 设计工作流本身；当你希望其他开发者安装它时，再将其打包为 [plugin](https://developers.openai.com/codex/plugins/build)。

Skills 可在 Codex CLI、IDE 扩展和 Codex app 中使用。

Skills 使用**渐进式披露**来高效管理上下文：Codex 一开始只看到每个 skill 的名称、描述和文件路径。只有当 Codex 决定使用某个 skill 时，才会加载完整的 `SKILL.md` 说明。

Codex 会在上下文中包含可用 skills 的初始列表，以便为任务选择合适的 skill。为避免挤占提示的其余部分，该列表上限约为模型上下文窗口的 2%；当上下文窗口未知时，上限为 8,000 个字符。如果安装了很多 skills，Codex 会先缩短 skill 描述。对于非常大的 skill 集合，某些 skills 可能会从初始列表中省略，Codex 会显示警告。

此预算只适用于初始 skills 列表。当 Codex 选择某个 skill 后，它仍会读取该 skill 的完整 `SKILL.md` 说明。

一个 skill 是一个包含 `SKILL.md` 文件的目录，还可以包含可选脚本和参考资料。`SKILL.md` 文件必须包含 `name` 和 `description`。

#### Codex 如何使用技能

Codex 可以通过两种方式激活 skills：

1. **显式调用：** 在提示中直接包含该 skill。在 CLI/IDE 中，运行 `/skills` 或输入 `$` 来提及一个 skill。
2. **隐式调用：** 当你的任务与 skill 的 `description` 匹配时，Codex 可以选择该 skill。

由于隐式匹配依赖 `description`，请编写范围和边界清晰的简洁描述。把关键用例和触发词放在前面，这样即使描述被缩短，Codex 仍能匹配到该 skill。

#### 创建技能

优先使用内置创建器：

```text
$skill-creator
```

创建器会询问该 skill 做什么、何时触发，以及它应保持为仅说明，还是包含脚本。默认是仅说明。

你也可以手动创建一个 skill：创建一个包含 `SKILL.md` 文件的文件夹：

```md
---
name: skill-name
description: Explain exactly when this skill should and should not trigger.
---

Skill instructions for Codex to follow.
```

Codex 会自动检测 skill 变更。如果更新没有出现，请重启 Codex。

#### 技能保存位置

Codex 会从仓库、用户、管理员和系统位置读取 skills。对于仓库，Codex 会从当前工作目录到仓库根目录的每个目录中扫描 `.agents/skills`。如果两个 skills 共享同一个 `name`，Codex 不会合并它们；两者都可能出现在 skill 选择器中。

| Skill 范围                                                                    | 位置                                                                                                                                                                                                | 建议用途                                                                                                                          |
| :----------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| `REPO`                                                                         | `$CWD/.agents/skills`                                                                                                                                                                                |
| 当前工作目录：你启动 Codex 的位置。                                            | 如果你在仓库或代码环境中，团队可以签入与某个工作文件夹相关的 skills。例如，只与某个微服务或模块相关的 skills。                                                         |
| `REPO`                                                                         | `$CWD/../.agents/skills`                                                                                                                                                                             |
| 当你在 Git 仓库内启动 Codex 时，CWD 上方的文件夹。                      | 如果你的仓库有嵌套文件夹，组织可以签入与父文件夹中共享区域相关的 skills。                                                                                                                    |
| `REPO`                                                                         | `$REPO_ROOT/.agents/skills`                                                                                                                                                                          |
| 当你在 Git 仓库内启动 Codex 时，最顶层的根文件夹。                  | 如果你的仓库有嵌套文件夹，组织可以签入与仓库中所有使用者相关的 skills。这些作为根 skills，可供仓库中任意子文件夹使用。                                                     |
| `USER`                                                                         | `$HOME/.agents/skills`                                                                                                                                                                               |
| 签入到用户个人文件夹中的任何 skills。                                          | 用于整理适用于某个用户、并可应用到该用户可能处理的任何仓库的 skills。                                                                                                                         |
| `ADMIN`                                                                        | `/etc/codex/skills`                                                                                                                                                                                  |
| 签入到机器或容器的共享系统位置中的任何 skills。                            | 用于 SDK 脚本、自动化，以及签入默认管理员 skills，使其可供该机器上的每个用户使用。                                                                                                             |
| `SYSTEM`                                                                       | 由 OpenAI 随 Codex 捆绑。                                                                                                                                                                        | 面向广泛受众的有用 skills，例如 skill-creator 和 plan skills。每个人启动 Codex 时都可使用。                                                                                                      |

Codex 支持符号链接的 skill 文件夹，并在扫描这些位置时跟随符号链接目标。

这些位置用于创作和本地发现。当你想把可复用 skills 分发到单个仓库之外，或选择性地把它们与 app 集成捆绑时，请使用 [plugins](https://developers.openai.com/codex/plugins/build)。

#### 使用插件分发技能

直接使用 skill 文件夹最适合本地创作和仓库范围的工作流。如果你想分发一个可复用 skill、把两个或更多 skills 捆绑在一起，或将 skill 与 app 集成一起发布，请将它们打包为 [plugin](https://developers.openai.com/codex/plugins/build)。

Plugins 可以包含一个或多个 skills。它们还可以选择性地把 app 映射、MCP server 配置和展示资源捆绑到一个包中。

#### 安装精选技能供本地使用

若要为你自己的本地 Codex 设置添加内置项之外的精选 skills，请使用 `$skill-installer`。例如，要安装 `$linear` skill：

```bash
$skill-installer linear
```

你也可以提示安装器从其他仓库下载 skills。Codex 会自动检测新安装的 skills；如果某个 skill 没有出现，请重启 Codex。

这适用于本地设置和实验。对于你自己的 skills 的可复用分发，请优先使用 plugins。

#### 启用或禁用技能

使用 `~/.codex/config.toml` 中的 `[[skills.config]]` 条目，可以在不删除 skill 的情况下禁用它：

```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

更改 `~/.codex/config.toml` 后请重启 Codex。

#### 可选元数据

添加 `agents/openai.yaml` 可以在 [Codex app](https://developers.openai.com/codex/app) 中配置 UI 元数据、设置调用策略，并声明工具依赖，以便更顺畅地使用该 skill。

```yaml
interface:
  display_name: "Optional user-facing name"
  short_description: "Optional user-facing description"
  icon_small: "./assets/small-logo.svg"
  icon_large: "./assets/large-logo.png"
  brand_color: "#3B82F6"
  default_prompt: "Optional surrounding prompt to use the skill with"

policy:
  allow_implicit_invocation: false

dependencies:
  tools:
    - type: "mcp"
      value: "openaiDeveloperDocs"
      description: "OpenAI Docs MCP server"
      transport: "streamable_http"
      url: "https://developers.openai.com/mcp"
```

`allow_implicit_invocation`（默认值：`true`）：当为 `false` 时，Codex 不会基于用户提示隐式调用该 skill；显式 `$skill` 调用仍然有效。

#### 最佳实践

- 让每个 skill 专注于一项工作。
- 除非需要确定性行为或外部工具，否则优先使用说明而不是脚本。
- 使用带有明确输入和输出的命令式步骤。
- 用提示测试 skill 描述，以确认触发行为正确。

更多示例请参阅 [github.com/openai/skills](https://github.com/openai/skills) 和 [agent skills 规范](https://agentskills.io/specification)。
