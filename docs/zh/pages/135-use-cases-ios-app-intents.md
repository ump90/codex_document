### 添加 iOS App Intents

Source: [Add iOS app intents](https://developers.openai.com/codex/use-cases/ios-app-intents.md)

使用 Codex 让应用动作和内容可用于 Shortcuts、Siri、Spotlight 以及更新的 assistant-driven 系统体验。

#### 概览

将 Codex 与 Build iOS Apps plugin 结合使用，识别应用应通过 App Intents 暴露的动作和实体，把它们接入 Shortcuts、Spotlight 等系统界面，并逐步为更 assistant-driven 的工作流做好准备。

适合：

- 已有有用动作或内容，但对 Shortcuts、Siri、Spotlight 或更广泛系统仍不可见的 iOS 应用。
- 希望现在暴露少数高价值动作，并逐步构建更 assistant-friendly 工作流的团队。
- 拥有 accounts、lists、filters、destinations、drafts 或 media 等清晰对象，并可将其作为 app entities，而不是锁在 UI 内部的应用。

相关 skill：

- [`build-ios-apps`](https://github.com/openai/plugins/tree/main/plugins/build-ios-apps)：使用 iOS build 和 SwiftUI skills 添加 App Intents、app entities 和 App Shortcuts，然后验证应用仍能构建，并且 intent-driven entry points 正确路由。

#### 起始提示

**为系统和 Assistant 界面添加 App Intents**

```text
使用 Build iOS Apps plugin 审计这个 iOS app，并为应暴露给系统的 actions 和 entities 添加 App Intents。

约束：
- 首先识别 app 中最高价值的用户动作和核心对象，它们应在 Shortcuts、Siri、Spotlight、widgets、controls 或更新的 assistant-driven system surfaces 中可用。
- 保持第一轮聚焦。选择一小组真正有用且无需打开完整 app 就能运行的 intents，再加上任何应 deep-link 到特定屏幕或工作流的 open-app intents。
- 只为系统实际需要理解和路由这些动作的数据定义 app entities。如果更小的 entity surface 足够，不要镜像整个内部 model layer。
- 在能提升可发现性时添加 App Shortcuts，并选择在 Siri、Spotlight 和 Shortcuts 中合理的 titles、phrases 和 display representations。
- 如果 app 需要在主 UI 内处理 intent，请把结果干净地路由回 app，并解释 app scene 如何响应这个 handoff。
- 第一轮后构建并验证 app，然后总结现在支持了哪些 actions、entities 和 system surfaces。

交付：
- first release 推荐的 intent 和 entity surface
- 已实现的 intents、entities 和 App Shortcuts
- app 在运行时如何路由或处理这些 intents
- 这现在解锁了哪些 Apple system experiences，以及哪些是合理的下一步
```

#### 相关链接

- [App Intents 概览](https://developer.apple.com/documentation/appintents/making-actions-and-content-discoverable-and-widely-available)
- [Apple 系统体验示例](https://developer.apple.com/documentation/appintents/adopting-app-intents-to-support-system-experiences)

#### 技术栈

| 需求 | 推荐默认选择 | 原因 |
| --- | --- | --- |
| 动作暴露 | [App Intents](https://developer.apple.com/documentation/appintents/making-actions-and-content-discoverable-and-widely-available) | App Intents 是让应用动作出现在 Shortcuts、Siri、Spotlight、widgets、controls 和更新 assistant-facing surfaces 中的系统契约。 |
| 应用数据表面 | `AppEntity`、`EntityQuery` 和 display representations | 小而形状良好的 entity layer 能让系统理解应用对象，而不必暴露整个 model layer。 |
| 可发现性层 | 带清晰 phrases、titles 和 symbols 的 `AppShortcutsProvider` | App Shortcuts 能让第一组已暴露动作更容易被发现和运行，而不要求用户从零构建一切。 |
| 验证循环 | `xcodebuild`、simulator checks 和聚焦 runtime routing verification | 难点不只是编译 intents target，而是证明系统调用 intent 时，应用会打开或路由到正确位置。 |

## 让应用的正确部分对系统可见

App Intents 是让 iOS 应用在自身 UI 之外更有用的最清晰方式之一。不要把应用视为一个封闭目的地，只有用户启动并到处点击后才可使用；使用 Codex 暴露应可用于 Shortcuts、Siri、Spotlight、widgets、controls 和更新 assistant-driven 系统体验的动作与对象。

这对今天的可发现性和自动化有用，也是在为更 assistant-driven 的未来做准备。如果你的应用已经知道如何 compose、open、filter、route 或 summarize 有价值的内容，App Intents 会给系统一种结构化方式来请求这种能力。

## 从动作和实体开始，而不是每个屏幕

最佳的第一轮 App Intents 通常不是“镜像整个应用”。让 Codex 识别：

- 用户希望在不导航完整界面时触发的少数动作。
- 系统需要理解哪些应用对象，才能正确路由这些动作。
- 哪些工作流应以特定状态打开应用，哪些可以直接从系统界面完成。

Apple 的 App Intents 指南是一个很好的框架：定义动作，定义系统需要的 entity surface，然后让这些动作在系统体验中可发现且可复用。最有用的参考包括 [Making actions and content discoverable and widely available](https://developer.apple.com/documentation/appintents/making-actions-and-content-discoverable-and-widely-available)、[Creating your first app intent](https://developer.apple.com/documentation/appintents/creating-your-first-app-intent)，以及系统体验示例 [Adopting App Intents to support system experiences](https://developer.apple.com/documentation/appintents/adopting-app-intents-to-support-system-experiences)。

## 按系统界面思考，而不只是 shortcuts

机会比“添加一个 shortcut”更大。一个好的 App Intents surface 可以让你的应用在多个地方有用：

- Shortcuts，用户可以直接运行动作，或把它们组合成更大的自动化。
- Siri，应用可以暴露有意义的 verbs 和 deep links，而不只是泛泛打开。
- Spotlight，app entities 和 app shortcuts 会成为可发现的系统入口点。
- widgets、Live Activities、controls 和其他 intent-driven UI surfaces。
- 更新的 assistant-facing experiences，其中结构化动作和实体比任意 UI flows 更容易被系统理解。

## 遵循真实应用模式

当应用采用类似以下结构时，效果通常最好：

- 使用专用 App Intents target，而不是把 intent types 分散到无关应用文件中。
- 为 compose a post 或在特定 tab 打开应用等高价值用户动作创建 `AppShortcutsProvider` entries。
- 为系统需要推理的内容创建小型 `AppEntity` types，例如 accounts、lists 和 timeline filters。
- intent handling 能干净地路由回主 app scene，让被调用的 intent 可以打开正确 compose flow，或把 app 切换到正确 tab。

对于大多数应用，我会要求 Codex 遵循这种模式：从小型 system-facing action layer 开始，保持 entity surface 狭窄，并在 intent 需要主 UI 时，将可预测的 runtime handoff 接回应用。

## 让 Codex 设计第一版 intent surface

这里最强的提示，是给 Codex 你的应用核心对象和顶级用户动作，然后要求它选择最小有用的第一版 App Intents surface，而不是盲目暴露所有内容。

## 实用技巧

### 暴露用户真正想在应用外部使用的 verbs

好的第一批 intents 通常是 compose、open、find、filter、start、continue 或 inspect 等。如果某个动作只有在很长的应用内设置流程之后才有用，它可能不属于第一轮 App Intents。

### 让 entities 小于你的 model layer

系统通常不需要你的完整持久化模型。让 Codex 定义最小 app entity surface，只要能给 Siri、Shortcuts 和 Spotlight 足够上下文来正确路由和展示动作即可。

### 把它视为 assistant 基础设施，而不只是 shortcuts 功能

即使第一版只明显改善 Shortcuts 或 Siri，更深层的收益是你的应用开始用结构化动作和实体表达能力。相比只把能力编码在点击和 view hierarchies 中的应用，这更容易参与未来系统和 AI-driven 入口点。
