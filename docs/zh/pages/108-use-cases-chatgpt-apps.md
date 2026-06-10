### 把你的应用带到 ChatGPT

Source: [Bring your app to ChatGPT](https://developers.openai.com/codex/use-cases/chatgpt-apps.md)

把你的使用场景转成面向 ChatGPT 的聚焦应用。

#### 概览

端到端构建一个狭窄的 ChatGPT app outcome：定义 tools、搭建 MCP server 和可选 widget、在 ChatGPT 中连接它，并迭代到核心流程可用。

适合：

- 围绕一个用户 outcome 规划第一个 ChatGPT app。
- 搭建 MCP server、tool metadata 和可选 widget，同时避免过度构建。
- 从本地 HTTPS 测试到 ChatGPT developer-mode 验证，运行紧凑迭代循环。

相关 skill：

- `$chatgpt-apps`：规划 tools、接入 MCP resources，并遵循当前 ChatGPT app 构建流程。
- `$openai-docs`：在 Codex 编写代码或建议架构前，拉取当前官方 Apps SDK 指南。
- `vercel`：通过 curated skills 和官方 Vercel MCP server，把 Vercel 生态指南带入 Codex。

#### 起始提示

```text
使用 $chatgpt-apps 和 $openai-docs，在这个 repo 中为 [use case] 规划一个 ChatGPT app。

要求：
- 从一个核心用户 outcome 开始。
- 提出 3-5 个 tools，每个都有清晰 name、description、inputs 和 outputs。
- 建议 v1 是否需要 widget，还是可以从 data-only 开始。
- MCP server 优先使用 TypeScript，widget 优先使用 React。
- 指出 auth、deployment 和 test requirements。

输出：
- Tool plan
- Proposed file tree
- Golden prompt set
- Risks and open questions
```

建议使用中等工作量。

#### 相关链接

- [Apps SDK 快速入门](https://developers.openai.com/apps-sdk/quickstart)
- [构建 MCP server](https://developers.openai.com/apps-sdk/build/mcp-server)
- [测试](https://developers.openai.com/apps-sdk/deploy/testing)

#### 技术栈建议

| 需求 | 推荐默认 | 原因 |
| --- | --- | --- |
| Widget framework | [React](https://react.dev/) | 对有状态 widgets 来说是稳健默认选择，尤其当 UI 需要 filters、tables 或多步骤交互时。 |
| Hosting | [Vercel](https://vercel.com/docs) | 快速部署、preview environments、自动 HTTPS，以及通往 hosted MCP endpoints 的清晰路径。 |

#### 你会构建什么

每个 ChatGPT app 都有三个部分：

- 一个 MCP server，用来定义 tools、返回数据、执行 auth，并把 ChatGPT 指向任何 UI resources。
- 一个可选 web component，渲染在 ChatGPT iframe 内。你可以用 React 构建，也可以用普通 HTML、CSS 和 JavaScript 构建。
- 一个模型，根据你提供的 metadata 决定何时调用 app 的 tools。

当 Codex 负责这些部分周围的重复工程工作时最有用：

- 规划 tool surface 和 metadata。
- 搭建 server 和 widget。
- 接入本地运行 scripts。
- 在聚焦的 pass 中添加 auth 和 deployment 变更。
- 编写验证循环，证明 app 可以在 ChatGPT 中工作。

#### 为什么 Codex 很适合

- ChatGPT apps 本来就清晰拆分为 server、可选 widget 和模型驱动的 tool calls。
- 当任务明确、范围清楚且容易验证时，Codex prompting 效果最好，这与 app 构建工作非常匹配。
- Skills 和 `AGENTS.md` 为 Codex 提供可复用指令和项目规则，帮助它保持扎根。

如需了解如何安装和使用 skills，请参阅我们的 [skills documentation](48-agent-skills.md)。

#### 如何使用

#### 前置条件

- 从一个核心用户 outcome 开始，而不是试图把整个产品搬进聊天中。
- 预先选择技术栈：server 使用 TypeScript 或 Python，widget 使用 React 或普通 HTML、CSS 和 JavaScript。
- 决定开发期间使用哪条 HTTPS 路径，例如 `ngrok` 或 Cloudflare Tunnel。
- 当前文档通常称为 app，但某些较旧页面和设置仍称为 connector。本地测试时，把它们视为同一个 setup object。

1. 从一个狭窄的 app outcome 开始，要求 Codex 提出三到五个 tools，并为每个 tool 给出清晰 name、description、inputs 和 outputs。
2. 决定 v1 可以保持 data-only，还是需要 widget；然后在添加依赖前，使用现有 repo 模式搭建 MCP server 和可选 widget。
3. 在 HTTPS 后本地运行 app，在 ChatGPT developer mode 中连接它，并用一小组 direct、indirect 和 negative prompts 测试。
4. 迭代 metadata、state handling、`structuredContent` 和 `_meta` payloads，直到核心读取流程在 ChatGPT 内可靠运行。
5. 只有在 user-specific data 或 write actions 需要时才添加 OAuth 2.1；可行时保持 anonymous 或 read-only flows 简单。
6. 准备带稳定 `/mcp` endpoint 的 hosted preview，验证 streaming 和 widget asset hosting，并在分享或提交 app 前审查 launch checklist。

#### 建议提示

适合这个工作流的强提示通常包含相同要素：

- 一个清晰 outcome：说明 app 应在 ChatGPT 内帮助用户做什么。
- 一个具体技术栈：说明 server 要 TypeScript 还是 Python，widget 要 React 还是保持轻量。
- 明确 tool boundaries：要求 Codex 提出或构建一小组 tools，每个 tool 只做一件事。
- Auth expectations：说明第一版是否可以 anonymous，还是需要关联账户和写入动作。
- 本地开发路径：提到你希望用于 ChatGPT HTTPS 测试的 tunnel 或 hosting path。
- 验证步骤：告诉 Codex 要运行哪些命令、测试哪些 prompts，以及回报哪些证据。

避免用一个巨大 prompt 一次性要求规划、实现、auth、deployment、submission 和 polish。请把工作拆成较小 milestones。

**先规划 app，再搭建脚手架**

**搭建第一个可运行版本**

**核心流程可用后再添加 auth**

**准备部署和审查 app**

#### 发布就绪

- app 有一个对用户来说显而易见的狭窄 outcome。
- tool set 保持小，并有明确 metadata、inputs 和 outputs。
- MCP server 端到端工作，并返回简洁的 `structuredContent`，把 widget-only 数据保留在 `_meta`。
- 如果需要 widget，它能在 ChatGPT 内正确渲染。
- 本地 HTTPS 测试循环可通过 ChatGPT developer mode 工作。
- 一小组 direct、indirect 和 negative prompts 能以预期对话流程和 tool payloads 通过。
- 只有在 user-specific data 或 write actions 需要时才添加 auth。
- 在 app 分享或提交前，deployment plan 和 launch-readiness review 覆盖 metadata、tool hints、privacy 和 test prompts。

#### 常见陷阱

- 要求 Codex 把整个产品搬进 ChatGPT。更好的做法：要求一个核心用户 outcome、三到五个 tools，以及一个狭窄 widget。
- 从一个巨大实现 prompt 开始。更好的做法：把工作拆成 planning、scaffold、auth、deployment 和 review passes。
- 在 tool contract 清晰前编写 UI。更好的做法：先规划 tool surface 和 response schema，再构建 widget。
- 跳过官方文档 grounding。更好的做法：把 `$chatgpt-apps` 与 `$openai-docs` 配对，让脚手架遵循当前 Apps SDK 指南。
- 把 metadata 当成事后补充。更好的做法：尽早编写 tool descriptions 和 parameter docs，然后用 prompt set 回放测试。
- 在证明 anonymous 或 read-only 路径可用前添加 auth。更好的做法：先让核心 tool flow 工作，再为真正需要的 tools 添加 OAuth。
- 在 ChatGPT 内测试前就宣布 app 完成。更好的做法：在 developer mode 中连接 app、检查 tool payloads，并验证真实对话流程。
