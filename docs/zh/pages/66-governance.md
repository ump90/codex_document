### 治理

Source: [Governance](https://developers.openai.com/codex/enterprise/governance.md)

Codex 为企业团队提供采用情况和影响的可见性，以及安全与合规项目所需的可审计性。日常跟踪可使用自助仪表板，程序化报告可使用 Analytics API，并可用 Compliance API 将详细日志导出到你的治理技术栈。

#### 跟踪 Codex 使用情况的方式

根据你的需求，有三种方式可监控 Codex 使用情况：

- **Analytics Dashboard**：快速了解采用情况、使用情况和代码审查影响。
- **Analytics API**：将结构化每日指标拉取到你的数据仓库或 BI 工具。
- **Compliance API**：导出详细活动日志，用于审计、监控和调查。

#### 分析仪表板

#### 仪表板视图

分析仪表板允许 ChatGPT 工作区管理员和分析查看者跟踪 Codex 采用情况、使用情况和 Code Review 反馈。使用数据最多可能滞后 12 小时。

Codex 提供用于每日和每周视图的日期范围控件。关键图表包括：

- 按产品界面划分的活跃用户，包括 CLI、IDE extension、cloud、desktop 和 Code Review
- 工作区和个人使用明细，包括按产品界面或模型划分的额度和 token 使用量
- 按客户端划分的 thread 和 turn 产品活动
- 用户排名表，带有客户端过滤器和排序选项，例如额度、thread、turn、文本 token 和当前连续使用天数
- Code Review 活动，包括已审查的 PR、按优先级划分的问题、评论、回复、反应和反馈情绪
- 当你的工作区具备相关功能时，包含技能调用、代理身份使用和访问令牌使用

#### 数据导出

管理员还可以以 CSV 或 JSON 格式导出 Codex 分析数据。Codex 提供以下导出选项：

- 工作区使用情况，包括按界面划分的每日活跃用户、thread、turn 和额度
- 每用户使用情况，包括跨界面的每日 thread、turn 和额度，在允许时可包含 email 地址
- Code Review 详情，包括每日评论、反应、回复和优先级级别的发现

#### 分析 API

当你希望自动化报告、构建内部仪表板，或将 Codex 指标与现有工程数据结合时，请使用 [Analytics API](https://chatgpt.com/codex/cloud/settings/apireference)。

#### 它衡量什么

企业 Analytics API 为工作区返回每日或每周 UTC 分桶。它支持工作区级和每用户使用情况、每客户端明细、Code Review 吞吐量、Code Review 评论优先级，以及用户与 Code Review 评论的互动。

#### 端点

base URL 是 `https://api.chatgpt.com/v1/analytics/codex`。所有端点都返回分页的 `page` 对象，其中包含 `has_more` 和 `next_page`。

使用 `start_time` 表示报告窗口开始处的包含式 Unix 时间戳，`end_time` 表示报告窗口结束处的排除式 Unix 时间戳，`group_by` 表示 `day` 或 `week` 分桶，`limit` 表示页面大小，`page` 用于从前一个响应继续。请求最多可回溯 90 天。

#### 使用情况

`GET /workspaces/{workspace_id}/usage`

- 返回每日或每周分桶中的 thread、turn、额度和每客户端使用量总计。
- 省略 `group` 可返回每用户行。
- 设置 `group=workspace` 可返回工作区范围的行。
- 包含文本输入、缓存输入和输出 token 字段。

#### 代码审查活动

`GET /workspaces/{workspace_id}/code_reviews`

- 返回 Codex 完成的 pull request 审查。
- 返回 Codex 生成的评论总数。
- 按 P0、P1 和 P2 优先级拆分评论。

#### 用户与代码审查的互动

`GET /workspaces/{workspace_id}/code_review_responses`

- 返回对 Codex 评论的回复和反应。
- 将反应拆分为正面、负面和其它反应。
- 统计收到反应、回复或任一形式互动的评论。

#### 工作方式

Analytics 使用时间窗口，并支持按天或周分组。结果按时间排序，并通过基于游标的分页返回。请使用作用域为 `codex.enterprise.analytics.read` 的 API key。

#### 常见用例

- 工程可观测性仪表板
- 面向领导层更新的采用情况报告
- 使用治理和成本监控

#### 合规 API

当你需要用于安全、法律和治理工作流的可审计记录时，请使用 [Compliance API](https://chatgpt.com/admin/api-reference)。

#### 它衡量什么

Compliance API 为企业提供导出 Codex 活动日志和元数据的方式，因此你可以将这些数据连接到现有审计、监控和安全工作流。它设计用于 eDiscovery、DLP、SIEM 或其它合规系统等工具。

对于通过 ChatGPT 身份验证的 Codex 使用，Compliance API 导出会提供 Codex 活动的审计记录，并可用于调查和合规工作流。这些审计日志最多保留 30 天。通过 API key 身份验证的 Codex 使用遵循你的 API 组织设置，不包含在 Compliance API 导出中。

#### 可以导出什么

#### 活动日志

- 发送给 Codex 的提示文本
- Codex 生成的响应
- 工作区、用户、时间戳和模型等标识符
- Token 使用量和相关请求元数据

#### 用于审计和调查的元数据

使用记录元数据回答如下问题：

- 谁运行了任务
- 谁创建或撤销了访问令牌
- 何时运行
- 使用了哪个 model
- 处理了多少内容

#### 常见用例

- 安全调查
- 合规报告
- 策略执行审计
- 将事件路由到 SIEM 和 eDiscovery 流水线
