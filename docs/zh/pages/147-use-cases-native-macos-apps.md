### 构建 macOS app

Source: [Build for macOS](https://developers.openai.com/codex/use-cases/native-macos-apps.md)

使用 Codex scaffold、build 和 debug 原生 Mac apps，采用 SwiftUI。

#### 概览

使用 Codex 构建 macOS SwiftUI apps，接入 shell-first build-and-run loop，并随着 app 成熟添加 desktop-native scene、window、AppKit 和 signing workflows。

适合：

- 希望 Codex scaffold desktop-native app shell 和可重复 build script 的 greenfield macOS SwiftUI apps。
- Codex 需要处理 windows、menus、sidebars、settings、AppKit interop 或 signing issues 的现有 Mac apps。
- 希望 macOS 工作保持 shell-first，同时尊重原生 desktop UX conventions 的团队。

相关 skill：

- `build-macos-apps`：用 shell-first workflows 构建和 debug macOS apps，设计 desktop-native SwiftUI scenes 和 windows，在需要时 bridge 到 AppKit，并准备 signing 和 notarization paths。

#### 起始提示

**Scaffold 原生 Mac app**

```text
使用 Build macOS Apps plugin scaffold 一个 starter macOS SwiftUI app，并添加一个 project-local `script/build_and_run.sh` entrypoint，我可以把它接到 `Run` action。

约束：
- 保持 shell-first。Xcode projects 优先使用 `xcodebuild`，package-first apps 优先使用 `swift build`。
- 明确建模 Mac scenes：主窗口加 `Settings`、`MenuBarExtra` 或 utility windows，但仅在它们适合产品时添加。
- 优先使用 desktop-native sidebars、toolbars、menus、keyboard shortcuts 和 system materials，而不是 iOS-style push navigation。
- 仅当 SwiftUI 无法干净表达桌面行为时，才使用狭窄的 AppKit bridge。
- 每次改动保留一个小 validation loop，并告诉我你运行的确切 build、launch 或 log commands。

交付：
- app scaffold 或请求的 Mac feature slice
- 可复用 build-and-run script
- 你运行的最小验证步骤
- 你建议的任何 desktop-specific follow-up work
```

#### 技术栈建议

| 需求 | 推荐默认项 | 原因 |
| --- | --- | --- |
| UI framework | [SwiftUI](https://developer.apple.com/documentation/swiftui/) | 对 windows、sidebars、toolbars、settings 和 scene-driven Mac app structure 来说是强默认选择。 |
| AppKit bridge | [AppKit](https://developer.apple.com/documentation/appkit) | 当 SwiftUI 无法覆盖你需要的桌面行为时，使用小型 `NSViewRepresentable`、`NSViewControllerRepresentable` 或 `NSWindow` bridges。 |
| Build and packaging | `xcodebuild`、`swift build` 和 [App Store Connect CLI](https://asccli.sh/) | 让本地 builds、manual archives、script-based notarization 和 App Store uploads 保持在可重复的 terminal-first loop 中。 |

#### Scaffold app 和 build loop

对于新的 Mac app，请要求 Codex 先选择正确 scene model：`WindowGroup`、`Window`、`Settings`、`MenuBarExtra` 或 `DocumentGroup`。这样从第一版开始就是 desktop-native，而不是从 iOS-style `ContentView` 生长出来。

保持执行循环 shell-first。对于 Xcode projects，使用 `xcodebuild`。对于 package-first apps，使用 `swift build` 和 project-local `script/build_and_run.sh` wrapper，让它停止旧进程、构建 app、启动新 artifact，并可选择暴露 logs 或 telemetry。

如果纯 SwiftPM app 是 GUI app，请把它打包并作为 `.app` 启动，而不是直接运行 raw executable。这样可以避免本地验证时缺少 Dock、activation 和 bundle-identity 的问题。

#### 利用 skills

当工作变得更 desktop-specific 时，添加 [Build macOS Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-macos-apps)。它覆盖 shell-first build 和 debug loops、SwiftPM app packaging、原生 SwiftUI scene 和 window patterns、AppKit interop、unified logging、test triage，以及 signing/notarization workflows。

要了解如何安装和使用 plugins 与 skills，请参阅 [Codex plugins documentation](78-plugins.md) 和 [skills documentation](48-agent-skills.md)。

#### 构建 desktop-native UI

优先采用 Mac conventions，而不是 iOS navigation patterns。使用 `NavigationSplitView` 实现 sidebar/detail layouts，为 preferences 使用明确的 `Settings` scenes，为可发现 actions 使用 toolbars 和 commands，并为轻量、随时可用的 utilities 使用 menu bar extras。

先使用 system materials、semantic colors 和 standard controls。只有当产品需要独特桌面表面时，才添加 custom window styling、drag regions 或 Liquid Glass surfaces。

如果 SwiftUI 已经接近但还不够，请添加尽可能小的 AppKit bridge。好的例子包括 open/save panels、first-responder control、menu validation、drag-and-drop edges，以及为一个专门控件包装 `NSView`。

#### Debug、test 并准备发布

对于 runtime behavior，要求 Codex 在 window opening、sidebar selection、menu commands 或 background sync 周围添加几条 `Logger` 事件，然后在 app 启动后用 `log stream` 验证这些事件。

对于 failing tests，让 Codex 先运行最小有用的 `xcodebuild test` 或 `swift test` scope，并分类问题是 compilation、assertion failure、crash、flake，还是 environment/setup problem。

当工作从本地迭代转向分发时，要求 Codex 同时准备 Xcode 中的 manual archive path，以及用于可重复 shipping 的 script-based archive 和 notarization path。让它用 `codesign` 和 `plutil` 检查 app bundle、entitlements 和 hardened runtime；当你希望 uploads 也留在终端中时，使用 [App Store Connect CLI](https://asccli.sh/)。

#### 示例提示

#### 实用提示

##### 保持 scenes 明确

把主窗口、settings window、utility windows 和 menu bar extras 建模为分开的 scene roots，而不是把整个 app 藏进一个巨大的 view。

##### 让 system chrome 做更多工作

在创建自定义 sidebars、toolbars 或 materials 之前，先检查标准 SwiftUI scene 和 window APIs 是否已经提供你想要的 Mac behavior。

##### 把 AppKit 当作狭窄边缘

使用 `NSViewRepresentable`、`NSViewControllerRepresentable` 或聚焦的 `NSWindow` helper 补齐一个缺失的桌面能力，但保持 SwiftUI 作为 selection 和 app state 的事实来源。

##### 把 signing 和 notarization 验证与本地 build 成功分开

本地成功启动并不能证明 app 已签名或已准备好 notarization。为一次性 release checks 保留 manual Xcode archive flow，为可重复分发添加 scripted archive 和 notarization flow，并在任务与 shipping 相关而不只是本地迭代时运行 `codesign` 和 `plutil` checks。

#### 相关链接

- [Model Context Protocol](53-model-context-protocol.md)
- [Agent skills](48-agent-skills.md)
