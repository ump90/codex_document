### Sites（站点）

Source: [Sites](https://developers.openai.com/codex/sites.md)

Sites 让 Codex 可以创建、保存、部署和检查由 OpenAI 托管的网站、web app 和游戏。当你想把一个提示词或兼容的现有项目变成托管站点，并且不想设置单独的部署工作流时，请使用 **Sites** plugin。

每个 Sites 部署 URL 都是生产部署。如果你想在构建上线前审查它，请让 Codex 保存一个 version，而不要部署它。

#### 理解项目、版本和部署

Sites project 会将本地 source project 与通过 Sites 管理的托管关联起来。Codex 会将该关联和可选的 storage binding names 存储在 `.openai/hosting.json` 中。新创建的本地 starter 可以一开始没有 `project_id`；Sites 在预配托管 project 后会添加一个。

例如，一个已预配的 site 如果使用关系数据库绑定且没有文件存储，可以包含：

```json
{
  "project_id": "",
  "d1": "DB",
  "r2": null
}
```

Sites 发布有两个独立阶段：

1. **Save a version.** Codex 构建可部署 site，并将该 version 与用于构建的 source Git commit 关联起来。当你需要一个可审查的部署候选版本时，使用此阶段。
2. **Deploy a version.** Codex 发布已保存的 version，并在部署成功时报告 production URL。仅当你希望所选受众可以访问该 site 时才使用此阶段。

需要识别之前的部署候选版本时，请让 Codex 列出或检查已保存的 versions。

#### 选择受支持的站点形态

Sites 托管的项目需要构建出与 Cloudflare Worker 兼容的 ES modules 输出。对于新项目，Sites 工作流可以从其推荐的 site starter 开始。对于现有 site，在请求部署前，请让 Codex 确认项目的 build 可以生成兼容的部署产物。

告诉 Codex 你需要的产品行为，以便它选择合适的 site 形态：

| 站点需求                                                       | 应向 Sites 请求什么                                                           |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| 内容驱动的网站或 landing page                                  | 不带持久应用状态的 site，除非体验需要它                                      |
| 保存的记录、用户进度或游戏分数                                 | D1，用于持久结构化数据的关系数据库                                           |
| 图片、文档、音频、视频或其他上传内容                           | R2，用于文件的对象存储                                                       |
| 带可搜索 metadata 的已上传文件                                 | D1 存储 metadata，R2 存储文件内容                                            |
| 需要当前工作区用户身份的内部 site                              | 工作区认证的用户身份                                                         |
| 公开登录或外部身份提供方                                       | 启用身份验证的 Sites project                                                 |

不要为临时展示状态请求持久存储，例如主题选择或已关闭的横幅。对于人们期望托管 site 记住的产品数据，请请求它。

#### 控制访问和密钥

分享已部署 URL 前设置受众。对于新站点，在审查内容、数据处理和预期受众前，请将访问限制为所有者和工作区管理员。

你可以要求 Sites 应用以下访问模式之一：

| 访问模式                         | 谁可以访问站点                                                                                |
| -------------------------------- | --------------------------------------------------------------------------------------------- |
| Owner and admins (`admins_only`) | 站点所有者和工作区管理员                                                                |
| Workspace (`workspace_all`)      | 工作区中的所有 active users                                                                   |
| Custom (`custom`)                | 你选择的特定 active users 或 workspace groups；Sites 仍允许 owner 访问                        |

例如：

```text
@Sites Change this deployed site's access to everyone in my workspace after
showing me the current site and confirming the deployment URL.
```

#### 配置运行时环境值

在 app 侧边栏中打开 **Sites**，选择一个 project，以便在 Sites panel 中添加、更新或移除托管环境变量和 secrets。不要把这些值存储在 `.openai/hosting.json` 中。让本地 `.env` 和 `.env.example` 文件与本地开发所需的 keys 保持一致，并且不要提交 secret values。

添加、更新或移除托管环境值后，请让 Codex 重新部署已批准的 saved version，以便下一次部署使用更新后的配置。

#### 分享前审查

在部署或扩大访问范围前：

- 在 Codex [review pane](https://developers.openai.com/codex/app/review) 中审查 source changes 和任何数据库迁移。
- 确认 build 成功，并确认所选 saved version 是你想发布的 version。
- 检查只有预期受众可以访问该 site。
- 确认你已通过 Sites 配置运行时 secret values，且没有将它们提交到 source files。
- 部署后，在分享前让 Codex 确认部署状态和 production URL。

#### 相关文档

- [Plugins](https://developers.openai.com/codex/plugins) 说明如何安装和调用 Codex plugins。
- [Codex app](https://developers.openai.com/codex/app) 介绍 app 导航和项目线程。
- [审查并发布变更](https://developers.openai.com/codex/app/review) 说明如何在发布前检查 source changes。
