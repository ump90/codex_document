### 进行细粒度 UI 修改

Source: [Make granular UI changes](https://developers.openai.com/codex/use-cases/make-granular-ui-changes.md)

使用 Codex-Spark 在现有 app 中快速进行聚焦 UI 迭代。

#### 概览

使用 Codex 在现有 app 中一次做一个小 UI 调整，在浏览器中验证，并把弹出的聊天窗口放在 preview 附近，保持快速迭代。

适合：

- 主体结构已经建好、只需要小型视觉调整的现有 app。
- 快速产品或设计审查循环，其中每条反馈都应变成一个聚焦代码改动。
- 需要浏览器验证，但不应演变为大范围重新设计的 UI polish pass。

相关 skill：

- `$playwright`：在真实浏览器中打开正在运行的 app，检查改动过的 route，并在下一轮迭代前验证每个小 UI 调整。

#### 起始提示

**做一个 UI 改动**

```text
在现有 app 中做这个 UI 改动：

[describe the exact spacing, alignment, color, copy, responsive, or component-state adjustment]

约束：
- 只修改这个 UI 调整所需的文件。
- 复用现有 components、tokens、icons 和 layout patterns。
- 除非我明确要求，否则保持 behavior、data flow 和 routing 不变。
- 启动或复用 dev server，在浏览器中检查当前 UI，做最小 patch，并可视化验证结果。

完成这一个改动后停止，并总结修改的文件以及你运行的浏览器检查。
```

建议使用 `gpt-5.3-codex-spark`，低推理强度。

#### 简介

当你有一个现有 app，并希望快速迭代 UI 时，可以使用 `gpt-5.3-codex-spark` 对 UI 做小而聚焦的修改。Codex-Spark 是我们最快的模型，针对近乎即时的实时编码迭代进行了优化。

它最适合紧密循环：一条视觉反馈、一次聚焦编辑、一次浏览器检查，然后再进入下一条反馈。

你可以使用 [Codex Spark model](20-model-selection.md#gpt-53-codex-spark) 完成这类任务。它在 Pro plans 中可用。

#### 选择模型

如果你有访问权限，快速 UI 迭代建议从 `gpt-5.3-codex-spark` 开始。它不如我们的通用模型强，但专为实时编码迭代设计。如果没有访问权限，请使用 `gpt-5.5`，并配合 `medium` 或 `low` reasoning effort。

这个取舍对细粒度 UI 工作很有用。你通常不需要最深的模型来移动按钮、调 breakpoint 或调整 component state。你需要的是一个响应快、理解本地代码、编辑正确文件，并能反复执行循环而不会让迭代显得沉重的模型。

#### 开发流程

1. 打开现有 app，并让相关 route 或 component 可见。
2. 把当前 Codex 对话弹出到 [floating window](27-codex-app-features.md#floating-pop-out-window)，放在浏览器、编辑器或设计 preview 附近。
3. 每次给 Codex 一个具体 UI 改动。如果有 route、viewport、当前截图、目标截图或准确产品反馈，请一并提供。
4. 要求 Codex 检查当前实现，做最小且合理的编辑，并保留 app 现有 components、tokens、layout primitives 和 data flow。
5. 审查结果，然后在同一线程中发送下一条小调整。

#### 写小提示

细粒度 UI prompt 应直接且狭窄。好的 prompt 会说明 surface、目标改动和你期待的验证。

如果结果接近但还不完全正确，后续提示也保持同样具体：

#### 什么时候慢下来

如果任务不再是细粒度改动，就不要继续使用这个快速循环。需要大范围重构、新的 design system primitive、非平凡的 accessibility behavior，或影响多个 screen 的产品决策时，请切换到更强模型和更审慎的 prompt。

快速 UI 迭代最适合让 Codex 调整已经理解的 surface，而不是从零重新设计 app。

#### 相关链接

- [Codex-Spark](08-speed.md#codex-spark)
- [浮动弹出窗口](27-codex-app-features.md#floating-pop-out-window)
