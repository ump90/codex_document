### 创建基于浏览器的游戏

Source: [Create browser-based games](https://developers.openai.com/codex/use-cases/browser-games.md)

定义游戏计划，并让 Codex 在实时浏览器中构建和测试。

#### 概览

使用 Codex 把游戏 brief 先转成定义清楚的计划，再转成真实的浏览器游戏。使用 imagegen 生成视觉资产，并让 Codex 在实时浏览器中测试游戏，迭代控制、UI 和手感。

适合：

- 从零构建基于浏览器的游戏。
- 需要反复测试和调优控制、视觉效果与部署的游戏构建。

相关 skill：

- `$playwright`：在实时浏览器中试玩游戏、检查当前状态，并基于真实构建迭代控制、节奏和 UI 手感。
- `$imagegen`：生成概念图、sprites、背景和 UI 资产，并保留 prompts 以便后续生成同系列资产。
- `$openai-docs`：在把 OpenAI 驱动功能接入游戏前，拉取当前官方指南。

#### 起始提示

```text
使用 $playwright-interactive、$imagegen 和 $openai-docs，在这个 repo 中规划并构建一个浏览器游戏。

实现 PLAN.md，并把工作日志记录在 `.logs/` 下。
```

#### 相关链接

- [使用 AGENTS.md 自定义指令](50-custom-instructions-with-agents-md.md)
- [Codex skills](48-agent-skills.md)

#### 技术栈建议

| 需求 | 推荐默认 | 原因 |
| --- | --- | --- |
| Web 游戏技术栈 | [Next.js](https://nextjs.org/) 搭配 [Phaser](https://phaser.io/) 或 [PixiJS](https://pixijs.com/) | 这是浏览器游戏 UI 加渲染层的实用默认选择。 |
| 后端技术栈 | [Fastify](https://fastify.dev/)、WebSockets、[Postgres](https://www.postgresql.org/) 和 [Redis](https://redis.io/) | 当游戏需要持久化、匹配、排行榜或 pub/sub 时，这是稳健默认选择。 |

#### 引言

构建游戏是最能说明 Codex 不只是生成代码的例子之一。一个真实游戏通常需要书面概念、渲染层、前端外壳工作、后端状态、资产制作，以及持续的视觉调优。

当 Codex 从明确写下游戏应做什么开始，再使用 Playwright interactive 在实时浏览器中测试游戏并迭代时，这个使用场景效果最好。

#### 从游戏计划开始

在 Codex 搭建任何东西之前，要求它创建一个 `PLAN.md`，用具体术语定义游戏：

- 玩家目标
- 主循环
- 输入和控制
- 胜利和失败状态
- 进度或难度
- 视觉方向
- 技术栈和托管假设
- milestone 顺序

这个计划很重要，因为“构建一个游戏”本身过于模糊。Codex 需要知道如何实现游戏的每一部分，并且在构建过程中经常参考实现细节。

你可以使用 `/plan` slash command 激活 plan mode。拿到输出后，把它保存到 `PLAN.md` 文件。

#### 用 AGENTS.md 引导 Codex 行为

为了确保 Codex 遵循计划、验证工作并使用正确工具，定义一个类似下面的 `AGENTS.md`：

```text
# Game name

<Type of game>

Tech Stack:

- NextJS for frontend (hosted on Vercel)
- <insert technology> for rendering
- Fastify for backend, websockets (hosted on <hosting platform>)
- Postgres for database (hosted on <hosting platform>)
- Redis for caching and pub/sub (hosted on <hosting platform>)
- OpenAI for generative AI features

Tips:

- Use build and test commands to verify your work as soon as you complete a feature or task
- Use the PLAN.md file to guide your work when building new features
- Log your work under .logs (create new log files as you see fit) to record your thought process and decisions, and reference them when iterating on features
- Use playwright to test the visual output of your work, and iterate if it doesn't look right or fit the vibe
- Use imagegen to generate visual assets for your work, and every time you generate a collection of assets, save the prompts you used to be able to continue generating more of the same assets later (create files in .prompts)
- Use Context7 MCP to fetch <rendering framework> docs
```

这让 Codex 可以长时间独立运行，并在需要时使用相关 skills。

#### 利用 skills

添加 `AGENTS.md` 文件中提到的 skills：

- Imagegen，让 Codex 按需为游戏生成视觉资产。
- Playwright interactive，让 Codex 在实时浏览器中测试游戏。
- OpenAI docs，让 Codex 获取最新 OpenAI API 文档。
- 可选：添加 Context7 MCP server，用来获取渲染框架的最新文档。

在 [skills documentation](48-agent-skills.md) 中了解如何添加 skills。

**提示**：要求 Codex 把图像生成 prompts 保存到文件中，让视觉资产保持一致。给出你想生成的资产风格方向，并让 Codex 提出详细、可复用的 prompts。

#### 让 Codex 工作并迭代

Codex 会基于初始计划生成游戏的第一个版本。

如果有大量图像资产需要生成，这个第一版可能需要一段时间，有时会持续数小时。由于 Codex 可以测试自己的工作，并在实时浏览器中试玩游戏，它可以在很长时间内不需要任何输入。

计划定义得越清楚，第一次迭代后的最终输出就越好。

当你测试它时，可以根据需要提供截图、要求修改玩法或更新视觉资产，持续迭代，直到你满意结果。
