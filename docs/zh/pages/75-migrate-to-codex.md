### 迁移到 Codex

Source: [Migrate to Codex](https://developers.openai.com/codex/migrate.md)

使用导入流程，将你的说明、配置、skills、MCP servers、hooks、subagents 和最近会话从另一个 agent 带入 Codex。Codex 会迁移它能直接处理的部分，并可以打开一个后续线程来帮助迁移剩余内容。

#### 开始迁移

1. 在 Codex app 中打开 **Settings**。
2. 在 **General** 页面中，找到 **Import other agent setup**。
3. 选择 **Import** 或 **Import again**。
4. 审查 Codex 找到的内容，选择要带入的项目，然后选择 **Import**。
5. 导入完成后，如果想检查结果，请选择 **View imported files**。

#### 迁移如何工作

Codex 会同时检查你的用户级设置和当前项目。用户级设置来自你机器上的文件；项目级设置来自你打开的仓库中的文件。

导入时，Codex 会：

1. 检测它能找到的设置。
2. 导入所选的、它可以直接迁移的项目。
3. 导入完成后再次检查。
4. 如果仍有内容需要后续处理，则提供在新线程中继续迁移的选项。

#### Codex 可以导入哪些内容

| 检测到的设置                          | Codex 目标位置                         |
| ------------------------------------- | -------------------------------------- |
| 说明文件                              | [`AGENTS.md`](https://developers.openai.com/codex/guides/agents-md) |
| `settings.json`                       | [`config.toml`](https://developers.openai.com/codex/config-basic)   |
| Skills                                | [Codex skills](https://developers.openai.com/codex/skills)          |
| 最近 30 天的会话                      | Codex 线程和项目                       |
| MCP server 配置                       | [Codex MCP 配置](https://developers.openai.com/codex/mcp)           |
| Hooks                                 | [Codex hooks](https://developers.openai.com/codex/hooks)            |
| 斜杠命令                              | [Codex skills](https://developers.openai.com/codex/skills)          |
| Subagents                             | [Codex agents](https://developers.openai.com/codex/subagents)       |

#### 在新线程中完成剩余设置

某些检测到的设置无法干净地一对一映射到 Codex。对于这些项目，Codex 可以打开一个带有 [`migrate-to-codex`](https://github.com/openai/skills/tree/main/skills/.curated/migrate-to-codex) skill 的新线程，帮助完成迁移。

发生这种情况时，Codex 会显示剩余设置，并提供 **Continue in Codex**。

如果你继续，Codex 会打开一个新线程，其中已填入剩余工作。该线程会将用户级设置与项目级设置分开，这样你可以看到每个剩余项目应该归属在哪里。

#### 导入后要审查什么

在依赖任何已迁移设置前，请先审查，尤其是：

- 已导入 skills 和 agents 中的工具限制或权限。
- 使用自定义身份验证、标头、环境变量或传输方式的 MCP server 设置。
- 在 Codex 中行为可能不同的 hooks。
- 需要手动后续处理的 plugins、marketplaces 或其他剩余设置。
- 依赖参数、shell 插值或文件路径占位符的提示模板或命令式提示。

#### 切换之后

导入完成后，打开你的某个已迁移项目，并从那里继续。如果你刚开始使用 Codex，请参阅 [快速入门](https://developers.openai.com/codex/quickstart) 了解其余设置流程。
