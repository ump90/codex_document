### 从想法到概念验证

Source: [Get from idea to proof of concept](https://developers.openai.com/codex/use-cases/idea-to-proof-of-concept.md)

用 ImageGen 以视觉方式探索概念，并构建想法的第一版。

#### 概览

将 Codex 与 ImageGen 结合使用，把粗略想法转化为视觉方向，实现最小可用原型，并在浏览器中验证。

适合：

- 早期产品想法，其中可运行原型比书面计划更能回答问题。
- 在实现前需要视觉探索的 Web 应用、dashboard 和工具。
- 希望在进一步投入前用可运行原型验证产品想法的团队。

相关 skill：

- `$imagegen`：在 Codex 实现选定方向前，使用 `gpt-image-2` 生成视觉概念、UI mockups、资产方向和 variants。
- [`$playwright`](https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive)：在真实浏览器中打开运行中的应用，检查已变更 route，并在下一轮迭代前验证每个小 UI 调整。
- [`build-web-apps`](https://github.com/openai/plugins/tree/main/plugins/build-web-apps)：为新 Web 应用、dashboards、sites 和前端原型使用 concept-first 工作流，然后在浏览器中验证实现。
- [`game-studio`](https://github.com/openai/plugins/tree/main/plugins/game-studio)：当概念验证是浏览器游戏，并需要可玩循环、资产工作流、HUD、引擎选择和 playtest pass 时，使用 Game Studio。

#### 起始提示

**构建概念验证**

```text
使用 ImageGen 为以下想法生成高质量 UI mockup，然后使用 [Build Web Apps plugin/Game studio plugin] 实现它：

[describe the idea, target user, and the main workflow]
```

建议使用高工作量。

#### 相关链接

- [图像生成指南](https://developers.openai.com/api/docs/guides/image-generation)
- [Codex plugins](78-plugins.md)

## 从视觉方向开始

GPT Image 2 非常适合生成高质量 UI mockups。探索新想法时，你可以利用图像生成获得视觉方向，而不是从空白开始。

你可以通过两种方式完成：

- 使用 ImageGen skill 迭代视觉方向；当你对建议的 UI 满意后，让 Codex 构建匹配这些视觉的原型。在这种情况下，请务必在新的回合中复制你希望实现的最终图像，而不是直接继续对话，因为 Codex 在能引用用户附件时效果更好。
- 使用 plugin 并直接描述你的想法：plugin 会为你生成视觉方向并处理后续步骤。

## 利用 plugin

如果你在开始实现前不需要迭代视觉方向，可以使用 plugin 并描述你的想法。

对 Web 应用、dashboards、创意网站和前端较重的工具，使用 [Build Web Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-web-apps)。它的工作流会推动 Codex 先生成设计，在代码中匹配设计，并使用浏览器将结果与概念对照。

当概念验证是浏览器游戏时，使用 [Game Studio plugin](https://github.com/openai/plugins/tree/main/plugins/game-studio)。这条路径应在扩展游戏前定义 player verbs、first playable loop、engine、asset workflow、HUD、controls 和 browser test。

## 迭代工作流

好的概念验证应限定在一个能快速实现并与团队验证的 MVP 范围内。
如果你想确保 MVP 按预期运行，可以使用 Playwright interactive 让 Codex 验证自己的工作。

当你有了可运行的第一版后，可以在同一对话中要求有边界的变更来迭代它：
