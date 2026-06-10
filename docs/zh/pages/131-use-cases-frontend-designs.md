### 构建响应式前端设计

Source: [Build responsive front-end designs](https://developers.openai.com/codex/use-cases/frontend-designs.md)

把截图和视觉参考转化为带视觉检查的响应式 UI。

#### 概览

使用 Codex 将截图和设计简述转换成符合仓库设计系统的代码，然后使用 Playwright 在不同屏幕尺寸上将实现与你的参考进行比较，并持续迭代直到看起来正确。

适合：

- 从零创建新的前端项目。
- 在现有代码库中根据截图实现已经设计好的屏幕或流程。

相关 skill：

- [`$playwright`](https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive)：在真实浏览器中打开应用，以验证实现并迭代布局和行为。

#### 起始提示

```text
使用我提供的截图和说明作为 source of truth，在当前项目中实现这个 UI。

要求：
- 复用现有设计系统组件和 tokens。
- 将截图转换为此仓库的 utilities 和 component patterns，而不是发明一套平行系统。
- 紧密匹配 spacing、layout、hierarchy 和 responsive behavior。
- 尊重仓库的 routing、state 和 data-fetch patterns。
- 让页面在 desktop 和 mobile 上响应式。
- 如果截图中的任何细节不明确，选择仍匹配整体方向的最简单实现，并简短说明假设。

验证：
- 对照提供的截图比较最终 UI 的外观和行为。
- 使用 $playwright-interactive 检查 UI 是否匹配 references，并按需迭代直到匹配。
```

建议使用中等工作量。

#### 相关链接

- [Codex skills](48-agent-skills.md)

## 介绍

当你有截图、简短设计简述或一些灵感参考时，Codex 可以把它们转化为响应式 UI，同时不忽略项目中已经建立的模式。

借助 Playwright skill，Codex 可以在真实浏览器中打开应用，将实现与你针对不同屏幕尺寸提供的截图比较，并迭代布局或行为，直到结果更接近目标。

## 从参考开始

给 Codex 你拥有的最清晰 UI 参考。对于窄范围任务，一张截图可能就够；但如果你包含桌面和移动布局、hover 或 selected states，以及任何重要的 empty 或 loading views 等多个状态，交接会更好。

参考不需要是完美的设计交付物。它们只需要让预期层级、间距和方向足够具体，使 Codex 不用猜。

## 具体说明

你对预期交互模式和想要的风格越具体，结果就越好。
模型倾向于默认使用高频模式和风格，因此如果你的参考中没有明显表达其他方向，UI 可能会显得普通。
你提供的输入越多，无论是更多参考灵感还是更具体的指令，就越可能得到有辨识度的 UI。

## 准备设计系统

目标仓库已有清晰组件层时，Codex 效果最好。Codex 可以自动使用你的现有组件和设计系统，而不是从零重新创建。

如果你认为有必要，也就是当你没有使用标准技术栈时，请指定 Codex 应复用哪些 primitives、tokens 位于哪里，以及仓库对 buttons、inputs、cards、typography 和 icons 的 canonical 做法是什么。

如果从现有代码库开始，Codex 很可能能自行理解如何使用你的组件和设计系统；但如果从零开始，明确说明会更好。

让 Codex 把截图视为视觉目标，但将该目标转换为项目实际的 utilities、component wrappers、color system、typography scale、spacing tokens、routing、state management 和 data-fetch patterns。

## 利用 Playwright

Playwright 是帮助 Codex 迭代 UI 的好工具。通过它，Codex 可以在真实浏览器中打开应用，将实现与你提供的截图比较，并迭代布局或行为。

它可以将浏览器窗口调整到不同屏幕尺寸，并在不同 breakpoints 检查布局。

请确保你已在 Codex 中启用 Playwright interactive skill。更多细节请参阅 [skills 文档](48-agent-skills.md)。

## 迭代

第一版应已经在方向上接近截图。对于复杂布局、交互或动画较多的 UI，预计需要几轮调整。

要求 Codex 将实现回看并对照截图，而不只是检查页面是否能构建。出现冲突时，它应优先使用仓库的 design-system tokens，并只做必要的最小间距或尺寸调整，以保留设计的整体外观。

如果额外截图或短说明能帮助澄清单张图片中不明显的状态，请使用它们。

### 建议后续提示
