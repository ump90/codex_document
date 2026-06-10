### 将 Figma 设计转化为代码

Source: [Turn Figma designs into code](https://developers.openai.com/codex/use-cases/figma-designs-to-code.md)

通过结构化设计上下文和视觉检查，把 Figma 选区转化为打磨好的 UI。

#### 概览

使用 Codex 从 Figma 拉取设计上下文、资产和变体，把它们转换成符合仓库设计系统的代码，然后使用 Playwright 将实现与 Figma 参考进行比较，并持续迭代直到看起来正确。

适合：

- 在现有代码库中实现已经由 Figma 设计好的屏幕或流程。
- 希望 Codex 基于结构化设计上下文工作的团队。

相关 skill：

- [`figma`](https://github.com/openai/plugins/tree/main/plugins/figma)：用代码实现设计，在已发布组件和源文件之间创建 Code Connect mappings，并为可重复的 Figma-to-code 工作生成项目特定设计系统规则。
- [`$playwright`](https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive)：在真实浏览器中检查响应式行为并验证已实现 UI。

#### 起始提示

**实现了解设计系统的 UI**

```text
使用 Figma skill，在当前项目中实现这个 Figma 设计。

要求：
- 从精确 node 或 frame 的 `get_design_context` 开始。
- 如果响应被截断，使用 `get_metadata` 映射文件，然后只用 `get_design_context` 重新获取所需 nodes。
- 在开始编码前，为精确 variant 运行 `get_screenshot`。
- 复用现有设计系统组件和 tokens。
- 将 Figma 输出转换为此仓库的 utilities 和 component patterns，而不是发明一套平行系统。
- 紧密匹配 spacing、layout、hierarchy 和 responsive behavior。
- 尊重仓库的 routing、state 和 data-fetch patterns。
- 让页面在 desktop 和 mobile 上响应式。
- 如果 Figma 返回 localhost image 或 SVG sources，直接使用它们，不要创建 placeholders，也不要添加新的 icon packages。

验证：
- 对照 Figma reference 比较最终 UI 的外观和行为。
- 使用 Playwright 检查 UI 是否匹配 reference，并按需迭代直到匹配。
```

建议使用中等工作量。

#### 相关链接

- [Codex skills](48-agent-skills.md)
- [Model Context Protocol](53-model-context-protocol.md)

#### 技术栈

| 需求 | 推荐默认选择 | 原因 |
| --- | --- | --- |
| 设计来源 | [Figma](https://www.figma.com/) | 一个具体 frame 或 component 选区能让实现有可靠依据。 |

## 介绍

当你有精确的 Figma 选区时，Codex 可以把它转化为打磨好的 UI，同时不忽略项目中已经建立的模式。

借助 Figma skill，Codex 可以使用 Figma MCP server 拉取结构化设计上下文、变量、资产，以及它应该实现的精确 variant。

借助 Playwright interactive skill，Codex 可以在真实浏览器中打开应用，将实现与 Figma 参考比较，并迭代布局或行为，直到结果更接近目标。

## 设置你的 Figma 项目

Figma 文件越干净，第一次实现就越好。为了改善交接：

- 尽可能使用 variables 或 design tokens，尤其是颜色、排版和间距。
- 为可复用 UI 元素创建 components，而不是重复 detached layers。
- 尽可能使用 auto layout，而不是手动定位。
- 保持 frame 和 layer 名称足够清晰，让主屏幕、状态和 variants 显而易见。
- 尽可能在文件中保留真实 icons 和 images，这样 Codex 不需要猜。

这会给 Codex 更好的结构，便于转换成稳健、可用于生产的 UI。

## 具体说明

你对预期交互模式和想要的风格越具体，结果就越好。

如果某个状态、breakpoint 或交互很重要，请明确指出。如果文件包含多个相近 variants，请告诉 Codex 哪一个应作为 source of truth。

你越明确说明哪些地方必须精确匹配、哪些地方应遵循仓库约定，Codex 就越容易做出正确权衡。

## 准备设计系统

目标仓库已有清晰组件层时，Codex 效果最好。Codex 可以自动使用你的现有组件和设计系统，而不是从零重新创建。

如果你认为有必要，请指定 Codex 应复用哪些 primitives、tokens 位于哪里，以及仓库对 buttons、inputs、cards、typography 和 icons 的 canonical 做法是什么。

请把 Figma MCP 输出视为结构参考，而不是最终代码风格；这些输出通常看起来像 React 加 Tailwind。让 Codex 将该输出转换为项目实际的 utilities、component wrappers、color system、typography scale、spacing tokens、routing、state management 和 data-fetch patterns。

## 工作流

### 从 Figma 选区开始

复制你希望实现的精确 Figma frame、component 或 variant 链接。Figma MCP 流程基于链接，因此链接需要指向你要的精确 node，而不是附近的父 frame。

### 提示 Codex 使用 Figma

Figma 应驱动第一轮实现。让 Codex 在开始实现前先遵循 Figma MCP 流程。

提示中应包含的内容：

第一版实现完成后，Codex 会使用 Playwright 在真实浏览器中验证 UI，并收紧剩余视觉或交互不匹配之处。
