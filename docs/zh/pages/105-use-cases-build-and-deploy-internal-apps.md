### 构建并部署内部应用

Source: [Build and deploy internal apps](https://developers.openai.com/codex/use-cases/build-and-deploy-internal-apps.md)

用 Sites 把团队工作流转成托管内部应用。

#### 概览

将 Codex 与 Sites 一起使用，构建、测试并部署内部应用，并使用内置存储和 auth context。

适合：

- 希望把重复性工作流转成交互式应用的团队。
- 需要轻量结构化持久化、文件上传或面向 workspace 分享的应用。
- 适合在一个 Codex thread 中完成构建、测试、部署和迭代的内部工具。

相关 skill：

- `sites`：从 Codex 构建、测试并部署静态站点或全栈 Web 应用。

#### 起始提示

```text
使用 @sites 为 [team or workflow] 构建并部署一个内部应用。

目标：
- [这个应用应帮助人们做什么]
- [谁应该使用它]
- [Codex 应检查的源文档、数据或已连接服务]

要求：
- 第一版聚焦一个有用工作流。
- 使用 D1 做结构化数据持久化。
- 如需要用户上传文件，使用 R2。
- 部署前测试主流程、持久化和响应式布局。

让所有 workspace users 都可访问。
```

建议使用中等工作量。

#### 相关链接

- [Sites documentation](80-sites.md)
- [Sites showcase](https://developers.openai.com/showcase/sites)

#### 从一个 thread 中构建并部署

Sites 是一个 plugin，也是面向你用 Codex 构建内容的托管服务。要求 Codex 创建应用，它可以构建项目、运行测试、部署，并返回一个可分享 URL。

范围可以从简单静态站点到全栈 JavaScript 或 TypeScript Web 应用。因此 Sites 非常适合聚焦的内部工具：入职 dashboard、赋能 hub、可搜索资源库、轻量工作流应用和报告视图。

关于 setup、存储、部署和访问指南，请参见 [Sites documentation](80-sites.md)。

从一个有用工作流开始。相比要求重建整个内部系统，清晰的第一版更容易审查、部署和改进。

#### 给 Codex 工作流上下文

告诉 Codex 这个应用面向谁、使用者应完成什么、它应检查哪些源材料，以及哪些内容应在 session 之间持久化。明确说明预期分享范围，并要求 Codex 在部署前测试主流程。

你也可以利用 [Plugins](78-plugins.md) 从内部来源获取或刷新数据。

如果需要实时数据获取，可以使用 API key 连接第三方工具。但如果你想利用 app connections，可以创建一个 [thread automation](24-automations.md#thread-automations)，按固定计划使用 plugins 获取数据、更新应用并重新部署。

#### 有意选择存储

许多内部应用需要持久化。Sites 支持两种存储原语：

- 使用 D1 这种 SQLite 兼容数据库存储结构化数据，例如 checklist 状态、bookmarks、filters、annotations、配置和文件元数据。
- 使用 R2 object storage 存储文件字节，例如应持久保存的上传文档、图像或其它资产。

把结构化元数据保存在 D1 中，把较大的文件对象保存在 R2 中。只读资源页或静态 microsite 可能两者都不需要。

#### 管理和分享项目

你可以管理谁有权访问已部署项目。

默认情况下，只有你（owner）和 workspace admins 可以访问。

但你可以允许以下范围访问：

- 所有 workspace users（`workspace_all`）
  或
- 特定 active users 或 groups（`custom`）

要更改访问权限，你可以从 Codex 的 Sites 页面管理项目，或直接要求 Codex 将访问权限更新为上述某一范围。

#### 示例

[Sites showcase](https://developers.openai.com/showcase/sites) 包含带完整 prompts 的站点示例。

- **[Onboarding Hub](https://developers.openai.com/showcase/onboarding-hub)** 组合第一周 checklist、资源、备注和上传文档。它使用 D1 存储用户状态和文件元数据，用 R2 存储上传文件字节。
- **[Enablement Hub](https://developers.openai.com/showcase/enablement-hub)** 提供带筛选器和已保存 bookmarks 的可搜索培训库，后端由 D1 支撑。
- **[Pulse Dashboard](https://developers.openai.com/showcase/pulse-dashboard)** 展示指标、趋势和 lineage 详情，同时使用 D1 存储配置和缓存快照。
- **[Sparkboard](https://developers.openai.com/showcase/idea-intake)** 把员工想法收集转成包含认证提交、投票、评论、状态板和贡献者排名的工作流。
- **[Launch Cal](https://developers.openai.com/showcase/launch-cal)** 把即将推出的产品发布组织成月历，包含筛选器、风险信号、checklists 和已连接来源引用。
- **[Event Planning Hub](https://developers.openai.com/showcase/event-planning-hub)** 组合活动请求、审批、模板、milestones、政策就绪状态和已连接的规划资源。

把这些示例作为起点，然后围绕你团队的工作流和源材料收窄 prompt。
