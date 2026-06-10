### 采用 Liquid Glass

Source: [Adopt liquid glass](https://developers.openai.com/codex/use-cases/ios-liquid-glass.md)

使用 Codex 通过 iOS 26 APIs 和 Xcode 26 将现有 SwiftUI 应用迁移到 Liquid Glass。

#### 概览

将 Codex 与 Build iOS Apps plugin 结合使用，审计现有 iPhone 和 iPad UI，把自定义 blur 或 material stacks 替换为原生 Liquid Glass，并通过 iOS 26 availability checks 和 simulator-driven validation 保持迁移安全。

适合：

- 需要实际 iOS 26 Liquid Glass 迁移计划，而不是模糊 redesign brief 的现有 SwiftUI 应用。
- 希望 Codex 审计 custom cards、sheets、tab bars、toolbars 和 action buttons，然后逐片实现迁移的团队。
- 仍支持旧 iOS 版本，并需要 `#available(iOS 26, *)` fallbacks，而不是单向视觉重写的应用。

相关 skill：

- [`build-ios-apps`](https://github.com/openai/plugins/tree/main/plugins/build-ios-apps)：使用 SwiftUI Liquid Glass、SwiftUI UI patterns 和 simulator debugging skills 现代化 iOS 屏幕，采用原生 glass effects，并在 iOS 26 simulators 上验证结果。

#### 起始提示

**将一个流程迁移到 Liquid Glass**

```text
使用 Build iOS Apps plugin 及其 SwiftUI Liquid Glass skill，将此 app 中一个高流量 flow 迁移到 Liquid Glass。

约束：
- 将其视为 iOS 26 + Xcode 26 迁移，但通过 `#available(iOS 26, *)` 为更早 deployment targets 保留非 glass fallback。
- 先审计该 flow。指出应变为原生 Liquid Glass 的 custom backgrounds、blur stacks、chips、buttons、sheets 和 toolbars，并指出应保持 plain content 的 surfaces。
- 优先使用 system controls 和原生 APIs，例如 `glassEffect`、`GlassEffectContainer`、`glassEffectID`、`.buttonStyle(.glass)` 和 `.buttonStyle(.glassProminent)`，而不是 custom blurs。只有当真实 morphing transition 改善流程时，才将 `glassEffectID` 与 `@Namespace` 一起使用。
- 在 layout 和 visual modifiers 之后应用 `glassEffect`，保持 shapes 一致，并且只在真正响应触摸的 controls 上使用 `.interactive()`。
- 使用 XcodeBuildMCP 在 iOS 26 simulator 上构建并运行，为迁移后的 flow 截图，并说明你使用的确切 scheme、simulator 和 checks。

交付：
- 该 flow 的简洁迁移计划
- 已实现的 Liquid Glass slice
- pre-iOS 26 devices 的 fallback behavior
- 你使用的 simulator validation steps 和 screenshots
```

#### 相关链接

- [Codex plugins](78-plugins.md)
- [Agent skills](48-agent-skills.md)

#### 技术栈

| 需求 | 推荐默认选择 | 原因 |
| --- | --- | --- |
| Liquid Glass UI APIs | [SwiftUI](https://developer.apple.com/documentation/swiftui/) 配合 `glassEffect`、`GlassEffectContainer` 和 glass button styles | 这些是 skill 应优先使用的原生 APIs，因此 Codex 会移除 custom blur layers，而不是重新发明 material system。 |
| 平台基线 | iOS 26 和 Xcode 26 | Liquid Glass 随 iOS 26 SDK 落地。Codex 应使用 Xcode 26 编译，并为早期 OS 支持添加显式 fallbacks。 |
| Simulator 验证 | [XcodeBuildMCP](https://www.xcodebuildmcp.com/) | 在视觉迁移中，build、launch、screenshot 和 log inspection 很重要，尤其是审查多个 states 和 device sizes 时。 |

## 从 iOS 26 基线开始

先把 Liquid Glass 视为 iOS 26 和 Xcode 26 迁移项目。用 iOS 26 SDK 重新构建应用，检查标准 SwiftUI controls 自动带来了什么，然后再让 Codex 重新设计那些仍显得过平、过重或与 system chrome 脱节的自定义部分。

如果应用仍支持更早 iOS 版本，请在一开始明确该约束。[Build iOS Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-ios-apps) 中的 SwiftUI Liquid Glass skill 应使用 `#available(iOS 26, *)` gate 新的 glass-only APIs，并保留一条在旧设备上仍清晰可读的 fallback path。

## 利用 iOS plugin

当你希望 Codex 将 SwiftUI UI 变更与 simulator-backed verification 结合起来时，使用 [Build iOS Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-ios-apps)。对于 Liquid Glass 工作，有用做法是让 Codex 审计一个 flow，迁移一小组 surfaces，在 iOS 26 simulator 上启动结果，并在扩大范围前截图。

该 plugin 包含一个 SwiftUI Liquid Glass skill，其中有一组值得写入提示的简单默认规则：

- 优先使用原生 `glassEffect`、`GlassEffectContainer`、glass button styles 和 `glassEffectID` transitions，而不是 custom blur views。
- 在 layout 和 visual modifiers 之后应用 `.glassEffect(...)`，让 material 包裹你真正想要的最终形状。
- 当多个 glass elements 一起出现时，用 `GlassEffectContainer` 包裹相关元素。
- 只在真正响应触摸的 buttons、chips 和 controls 上使用 `.interactive()`。
- 在整个 feature 中保持 corner shapes、tinting 和 spacing 一致，而不是混用一次性的 glass treatments。
- 为 pre-iOS 26 targets 保留非 glass fallback。

要进一步了解如何安装 plugins 和 skills，请参阅我们的 [plugins](78-plugins.md) 和 [skills](48-agent-skills.md) 文档。

## 观看 WWDC sessions

在让 Codex 重构真实生产 flow 前，这些 WWDC25 sessions 是很好的参考集：

- [认识 Liquid Glass](https://developer.apple.com/videos/play/wwdc2025/219/)
- [了解新设计系统](https://developer.apple.com/videos/play/wwdc2025/356/)
- [使用新设计构建 SwiftUI app](https://developer.apple.com/videos/play/wwdc2025/323/)
- [使用新设计构建 UIKit app](https://developer.apple.com/videos/play/wwdc2025/284/)
- [SwiftUI 新变化](https://developer.apple.com/videos/play/wwdc2025/256/)

## 先提示迁移计划，再提示一个 slice

当 Codex 把“哪里应该出现 glass？”和“现在写所有代码”分开时，Liquid Glass 迁移会更顺利。先要求快速审计，再让 agent 实现一个自包含 slice，并用 simulator 验证。

## 实用技巧

### 不要把所有东西都 glass 化

Liquid Glass 应在内容上方创建清晰的 control layer，而不是把每张 card 都变成发光面板。让 Codex 移除与 system materials 冲突的装饰背景，在可读性最重要的地方保留 plain content，并把 tinting 留给语义强调或主要操作。

### 从一个高流量 flow 开始

tab root、detail screen、sheet、search surface 或 onboarding flow 通常比一次全应用 sweep 更适合作为第一迁移目标。这会让审查更容易，也更清楚哪些 Liquid Glass 决策应成为可复用 component patterns。

### 有意审查 fallback behavior

如果你的 deployment target 低于 iOS 26，请让 Codex 同时展示 fallback implementation 和 Liquid Glass version。这个审查步骤能捕获意外 API availability 回归，并避免发布只在最新 simulator 上可用的迁移。
