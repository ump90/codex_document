### 重构 SwiftUI 屏幕

Source: [Refactor SwiftUI screens](https://developers.openai.com/codex/use-cases/ios-swiftui-view-refactor.md)

使用 Codex 在不改变行为或布局的前提下，把过大的 SwiftUI 屏幕拆分为小 subviews。

#### 概览

将 Codex 与 Build iOS Apps plugin 结合使用，把很长的 SwiftUI view 拆成专用 section views，将 side effects 移出 `body`，稳定 state 和 Observation 用法，并保持重构以 MV 优先，而不是引入不必要的 view models。

适合：

- 巨大的 SwiftUI 文件，其中 `body` 把 layout、branching、async work 和 inline actions 混在一个难以审查的屏幕里。
- 需要在保持视觉和行为一致的同时，让内部更易维护的现有 iOS features。
- 包含 computed `some View` fragments、optional view models 或 state plumbing，并应简化为显式 subview inputs 和 callbacks 的屏幕。

相关 skill：

- [`build-ios-apps`](https://github.com/openai/plugins/tree/main/plugins/build-ios-apps)：使用 SwiftUI view refactor skill 提取专用 subviews、保留稳定 data flow、简化 Observation 用法，并在 Codex 编辑大型 SwiftUI 屏幕时保持行为不变。

#### 起始提示

**在不改变行为的前提下重构一个大型屏幕**

```text
使用 Build iOS Apps plugin 及其 SwiftUI view refactor skill 清理 [NameOfScreen.swift]，不改变屏幕行为或外观。

约束：
- 保留 behavior、layout、navigation 和 business logic，除非你发现必须单独指出的 bug。
- 默认使用 MV，而不是 MVVM。优先使用 `@State`、`@Environment`、`@Query`、`.task`、`.task(id:)` 和 `onChange`，再考虑引入新的 view model；只有当该 feature 明确需要时才保留 view model。
- 重新排序 view，让 stored properties、computed state、`init`、`body`、view helpers 和 helper methods 从上到下易于浏览。
- 将有意义的 sections 提取为专用 `View` types，带小而显式的 inputs、`@Binding`s 和 callbacks。不要把一个巨大的 `body` 替换成一堆大型 computed `some View` properties。
- 将非琐碎 button actions 和 side effects 从 `body` 移到小方法中，并把真实 business logic 移到 services 或 models 中。
- 保持 root view tree 稳定。避免使用 top-level `if/else` branches 来切换完全不同的 screens；当局部 conditional sections 或 modifiers 足够时，优先使用它们。
- 重构时修复 Observation ownership：在 iOS 17+ 上，对 root `@Observable` models 使用 `@State`；除非 UI 真正需要这种 state shape，否则避免 optional 或 delayed-initialized view models。
- 每次 extraction 后，运行最小有用的 build 或 test check，证明屏幕行为仍相同。

交付：
- 重构后的 screen 和任何已提取 subviews
- 关于新 subview boundaries 和 data flow 的简短说明
- 任何你有意保留 view model 的位置及原因
- 你运行了哪些 validation checks 来证明行为保持不变
```

#### 相关链接

- [Build iOS Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-ios-apps)
- [Agent skills](48-agent-skills.md)

#### 技术栈

| 需求 | 推荐默认选择 | 原因 |
| --- | --- | --- |
| UI 架构 | SwiftUI，采用 MV-first 切分，跨 `@State`、`@Environment` 和小型专用 `View` types | 在引入另一个 view model layer 前，Codex 先简化 view tree 和 state flow，通常会让大型屏幕更易维护。 |
| 重构工作流 | [Build iOS Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-ios-apps) | 该 plugin 的 SwiftUI view refactor skill 为 Codex 提供关于 extraction、Observation 和 side-effect cleanup 的清晰规则，同时保持行为。 |
| 验证 | `xcodebuild`、previews 和聚焦 UI checks | 每次 extraction 后进行小型 build 或 simulator checks，比一次性重写更容易让人信任行为保持不变的重构。 |

## 在不改变行为的前提下重构一个屏幕

这个用例适用于 SwiftUI 文件已经膨胀成一个巨大屏幕，任何小修改都让人觉得有风险的时候。目标不是重新设计 feature，也不是发明新架构。让 Codex 保留行为和布局，然后把屏幕拆成带显式 data flow 的小 subviews，让下一次变更更容易审查。

使用 [Build iOS Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-ios-apps) 做这种清理。它的 SwiftUI view refactor skill 有一组有用的明确偏好：默认使用 MV 而不是 MVVM，把 business logic 放在 services 或 models 中，优先使用本地 view state 和 environment dependencies，并且只有 feature 明确需要时才保留 view model。

## 要求 Codex 做什么

先命名一个具体 screen 文件，并要求 Codex 在保留行为的同时改善结构。以下重构规则值得直接放入提示：

- 重新排序文件，让 environment dependencies、stored properties、computed non-view state、`init`、`body`、view helpers 和 helper methods 从上到下易于浏览。
- 将有意义的 sections 提取为专用 `View` types，带小而显式的 inputs、`@Binding`s 和 callbacks。
- 让 computed `some View` helpers 保持少而小。不要把一个巨型屏幕重建成一长串 private computed view fragments。
- 将非琐碎 button actions 和 side effects 移出 `body`，并把真实 business logic 移到 services 或 models 中。
- 保持 root view tree 稳定。相比 top-level `if/else` branches 切换整个 screens，优先使用 sections 或 modifiers 中的局部 conditionals。
- 边重构边修复 Observation ownership。对于 iOS 17+ 上的 root `@Observable` models，拥有它们的 view 应把它们存入 `@State`；只有 deployment target 要求时才使用 legacy observable wrappers。

## 要求小型验证循环

行为保持型重构应带有证明。让 Codex 在每次有意义 extraction 后运行最小 build、preview、test 或 simulator check，然后总结结构上改了什么，以及哪些内容有意保持不变。

## 实用技巧

### 先拆分，再讨论架构

如果屏幕太大，请先让 Codex 提取 section views，再引入新的抽象层。更短、更显式的 view tree 往往会消除添加 view model 的压力。

### 给每个 subview 传入尽可能小的接口

优先使用 `let` values、`@Binding`s 和单一用途 callbacks，而不是把整个 parent model 交给每个 child view。这会让每个已提取 section 更容易 preview，也更难意外耦合回整个屏幕。

### 让 Codex 指出有意不变的内容

对于安全重构，当 Codex 明确列出它没有改变的内容时很有帮助：business rules、navigation behavior、persistence、analytics semantics 和 user-visible layout。这会让审查快得多。
