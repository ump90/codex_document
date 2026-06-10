### 部署应用或网站

Source: [Deploy an app or website](https://developers.openai.com/codex/use-cases/deploy-app-or-website.md)

构建或更新 Web 应用、部署预览，并获得 live URL。

#### 概览

结合 Build Web Apps 和 Vercel 使用 Codex，将仓库、截图、设计或粗略应用想法转化为可分享的可运行预览部署。

适合：

- 把截图、地图、设计简述或粗略应用想法转化为可运行 Web 预览。
- 不手动串接 Vercel 命令，就部署分支或本地应用。
- 在 Codex 运行构建并检查部署后，分享 live URL。

相关 skill：

- [`build-web-apps`](https://github.com/openai/plugins/tree/main/plugins/build-web-apps)：使用 React、UI、部署、支付和数据库指导来构建、审查并准备 Web 应用。
- [`vercel`](https://github.com/openai/plugins/tree/main/plugins/vercel)：部署预览、检查部署、读取构建日志，并管理 Vercel 项目设置。

#### 起始提示

**构建并部署预览**

```text
使用 @build-web-apps 将 [repo, screenshot, design, or rough app idea] 转化为可运行的网站。

然后使用 @vercel 部署预览，并把 live URL 交给我。

上下文：
- [what the site should do]
- [source data, API, docs, or assets to use]
- [style or product constraints]
- [anything not to change]

在交还之前，运行本地构建并验证部署已准备好。
```

建议使用中等工作量。

#### 相关链接

- [Build Web Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-web-apps)
- [Vercel plugin](https://github.com/openai/plugins/tree/main/plugins/vercel)
- [Vercel 部署](https://vercel.com/docs/deployments/overview)

## 从站点和部署目标开始

Codex 可以构建或更新网站或应用，运行项目检查，用 Vercel 部署，并返回 URL。

有用的交接应当具体：仓库、截图、地图、设计简述、产品说明、API 文档或数据源。Codex 应先检查项目再修改，然后默认使用 Vercel plugin 部署预览。

当 Codex 需要构建或打磨应用时使用 `@build-web-apps`。当它应部署、检查部署或读取 Vercel 构建日志时使用 `@vercel`。

## 分享前检查结果

Codex 应告诉你它改了什么、用哪个命令构建项目，以及 Vercel 部署是否已准备好。如果部署需要环境变量、团队选择、域名设置或登录步骤，Codex 应指出这一点，而不是假装站点已经完成。

保持生产变更显式。默认是预览部署；只有在你明确需要时才请求生产部署。

## 从 live URL 继续迭代

拿到预览后，保持同一个线程打开。让 Codex 打开 URL、修复布局问题、更新文案、接入缺失数据，或在部署失败时读取 Vercel 日志。这个线程已经拥有仓库、部署和构建上下文。

好的后续请求应当具体：

- “移动端布局太挤了。修复它并重新部署预览。”
- “使用同一个项目，并加入来自 [source] 的最新数据。”
- “读取失败的构建日志并修复部署。”
