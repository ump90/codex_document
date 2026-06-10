### 构建 Mac app 外壳

Source: [Build a Mac app shell](https://developers.openai.com/codex/use-cases/macos-sidebar-detail-inspector.md)

使用 Codex 构建包含 sidebar、detail pane、inspector、commands 和 Settings 的 Mac 原生 SwiftUI app 外壳。

#### 概览

使用 Codex 和 Build macOS Apps plugin，把 app 想法转成 desktop-native `NavigationSplitView` app，保持 sidebar selection 稳定，添加菜单、工具栏和键盘快捷键，并把偏好设置移入专门的 `Settings` scene。

适合：

- 新 Mac app 想法，或需要真正桌面外壳的 iPad-first、web-first 概念，包括持久导航、菜单、工具栏和键盘快捷键。
- 编辑器、资料库、管理或审查工具，其中 sidebar selection 驱动 detail pane，inspector 暴露次要元数据或操作。
- 设置应该放在专门偏好设置窗口里，而不是主内容栈中另一个 pushed screen 的 Mac app。

相关 skill：

- `build-macos-apps`：使用 macOS SwiftUI patterns、窗口管理、AppKit interop 和 build/run skills 来创建 sidebar-detail-inspector 布局，接入菜单和设置，并在 shell-first 循环中验证 app。

#### 起始提示

**构建 Mac 原生 Sidebar 和 Inspector 外壳**

```text
使用 Build macOS Apps plugin，把 [describe your app idea] 转成 Mac-native SwiftUI app shell，包含 sidebar、detail pane、inspector、commands 和 Settings。

约束：
- 先选择 scene model。主窗口优先使用 `WindowGroup`，并为偏好设置添加专门的 `Settings` scene。
- 围绕 `NavigationSplitView` 构建主 UI，使用明确的 selection state、原生 `.sidebar` list、detail surface，以及用于次要元数据或控件的 `inspector(isPresented:)` panel。
- 保持 sidebar rows 轻量且原生：一个图标、一行标题，最多一行短 secondary line。除非有很强的产品理由，否则不要把每一行都包进大型自定义 cards。
- 通过 scene-level `commands`、`CommandMenu`、toolbar buttons 和 keyboard shortcuts 暴露重要操作。不要把关键操作的唯一路径藏在手势后面。
- 使用 `@SceneStorage` 存储窗口作用域 UI state，使用 `@AppStorage` 存储 preferences，并使用明确的 parent-owned selection bindings 协调 sidebar/detail。
- 优先使用 system materials、semantic colors 和标准 sidebar backgrounds。只有在需要时，才给 detail 或 inspector content cards 添加自定义样式。
- 仅当 SwiftUI 无法干净表达某个具体桌面行为时，才使用狭窄的 AppKit bridge。
- 创建或更新 `script/build_and_run.sh`，运行最小有用的 build/run 检查，并告诉我你使用的确切命令。

交付：
- scene structure 和主要 sidebar/detail/inspector views
- menu、toolbar 和 keyboard shortcut wiring
- Settings scene 和 preference state model
- 你添加的任何 AppKit bridge，以及它为什么必要
- build/run 验证步骤，以及你建议的任何 desktop UX 后续工作
```

#### 技术栈建议

| 需求 | 推荐默认项 | 原因 |
| --- | --- | --- |
| Split-view app shell | `NavigationSplitView`、`.sidebar` lists 和 `inspector(isPresented:)` | 持久 sidebar、detail pane 和 inspector 比 touch-first push navigation 更符合常见 Mac app 布局。 |
| Desktop actions 和 settings | `commands`、`CommandMenu`、keyboard shortcuts 和 `Settings` scene | 菜单栏操作、快捷键和专门设置窗口会让功能更像真正的 Mac app，而不是被拉伸到桌面的 iOS screen。 |
| State ownership | `@State`、`@SceneStorage`、`@AppStorage` 和明确的 selection bindings | Codex 可以让 sidebar selection、inspector visibility 和用户 preferences 保持可预测，而不是条件反射式添加 view model。 |
| Native escape hatches | 通过狭窄的 `NSViewRepresentable` 或 `NSWindow` bridge 使用 [AppKit](https://developer.apple.com/documentation/appkit) | 只把 AppKit 用于 SwiftUI 无法干净表达的平台行为，同时让 SwiftUI 作为 scene 和 selection state 的事实来源。 |

#### 从 Mac scene model 开始

这个用例用于把 app 想法转成一个感觉专为桌面构建的 Mac app 外壳，而不是从 touch-first stack 拉伸而来。要求 Codex 先选择 scene model，然后围绕稳定的 sidebar selection、detail surface 和用于次要控件或元数据的 inspector 来设计主窗口。

![一个 Mac 原生 sidebar 和 detail app 外壳，sidebar 中有选中项，detail pane 中显示内容。](https://developers.openai.com/images/codex/use-cases/macos-sidebar-detail-inspector.png)

当你希望 Codex 应用这种桌面结构，并保持 build/run loop shell-first 时，请使用 [Build macOS Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-macos-apps)。它的 macOS SwiftUI patterns skill 非常适合 scene 设计、sidebars、inspectors、commands、settings，以及当 SwiftUI 离某个 Mac-specific behavior 只差一步时使用的小型 AppKit bridges。

#### 构建 sidebar、detail pane 和 inspector

当功能受益于持久导航和稳定选中项时，优先使用 `NavigationSplitView`。保持 sidebar rows 原生且轻量，让 sidebar 使用系统背景，把自定义 cards 或密集元数据留给 detail pane 或 inspector。

```swift
struct LibraryRootView: View {
  @SceneStorage("LibraryRootView.selection") private var selection: Item.ID?
  @SceneStorage("LibraryRootView.showInspector") private var showInspector = true

  var body: some View {
    NavigationSplitView {
      List(selection: $selection) {
        ForEach(items) { item in
          Label(item.title, systemImage: item.systemImage)
            .tag(item.id)
        }
      }
      .listStyle(.sidebar)
      .navigationTitle("Library")
    } detail: {
      ItemDetailView(selection: selection)
        .inspector(isPresented: $showInspector) {
          ItemInspectorView(selection: selection)
        }
    }
  }
}
```

如果 app 需要不寻常的 split sizing、底层窗口协调或自定义 responder-chain 行为，请要求 Codex 保持 SwiftUI shell 不变，并只为那一个缺口添加所需的最小 AppKit bridge。

#### 把 commands、toolbars 和 shortcuts 放在桌面层

Mac 用户应该能在菜单栏、工具栏和键盘快捷键中发现重要操作。要求 Codex 围绕同一组 app actions 接入 scene-level `commands`、上下文相关 menu items 和 toolbar buttons，这样桌面用户就不必寻找只存在于手势中的控件。

```swift
@main
struct LibraryApp: App {
  var body: some Scene {
    WindowGroup {
      LibraryRootView()
    }
    .commands {
      CommandMenu("Library") {
        Button("New Item") {
          // Create a new item.
        }
        .keyboardShortcut("n")

        Button("Toggle Inspector") {
          // Route this command to the focused window or selected item state.
        }
        .keyboardShortcut("i", modifiers: [.command, .option])
      }
    }

    Settings {
      LibrarySettingsView()
    }
  }
}
```

当某个 command 应作用于当前 detail item 时，请使用 `FocusedValue`、scene state 或明确的 selection state。如果某个 shortcut 会在多个位置注册，请要求 Codex 合并 ownership，让 app 有一条清晰的 command route。

#### 把偏好设置放在 `Settings`

对于 app preferences，请使用专门的 `Settings` scene，并用 `@AppStorage` 持久化用户选择。这通常比把 settings screen 推入主内容窗口更符合 Mac。

```swift
struct LibrarySettingsView: View {
  @AppStorage("showItemMetadata") private var showItemMetadata = true

  var body: some View {
    TabView {
      Form {
        Toggle("Show Item Metadata", isOn: $showItemMetadata)
      }
      .tabItem { Label("General", systemImage: "gearshape") }
    }
    .frame(width: 460, height: 260)
    .scenePadding()
  }
}
```

#### 先提示 app 概念，再验证外壳

这个页面在你的提示中说清楚 app 概念、主要内容对象和核心操作时效果最好。然后让 Codex 先围绕该工作流构建桌面外壳。让 agent 运行一个小型 build/run 检查，并总结 scene structure、command wiring、state ownership，以及它必须 bridge 的任何 AppKit edge。

#### 实用提示

##### 保持 sidebar 原生

在 sidebar rows 中使用一个图标、一行标题，最多加一行短 secondary line。把更丰富的 cards、counters 和 metadata 移到 detail pane 或 inspector 中，让 source list 保持易于扫描。

##### 不要把设置藏在主栈里

如果某个用户偏好会影响整个 app，请要求 Codex 把该控件放进带有 `@AppStorage` 的 `Settings`，并通过 app menu 暴露入口，而不是再构建一个 pushed settings screen。

##### 只为狭窄的桌面缺口使用 AppKit

如果功能需要 open/save panels、first-responder control 或自定义 `NSView`，请把 AppKit 作为 SwiftUI-owned state model 边缘上的小包装使用，而不是用 AppKit 重写整个窗口。

#### 相关链接

- [Build macOS Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-macos-apps)
- [Agent skills](48-agent-skills.md)
