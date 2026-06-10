### 构建 iOS app

Source: [Build for iOS](https://developers.openai.com/codex/use-cases/native-ios-apps.md)

使用 Codex 为 iPhone 和 iPad scaffold、build 和 debug SwiftUI apps。

#### 概览

使用 Codex scaffold iOS SwiftUI projects，通过 `xcodebuild` 或 Tuist 保持 build loop CLI-first；当工作更深入时，添加 XcodeBuildMCP 或聚焦的 SwiftUI skills。

适合：

- 希望 Codex 从零 scaffold app 和 build loop 的 greenfield iOS SwiftUI apps。
- Codex 需要 schemes、simulator output、screenshots 或 UI automation 才能完成工作的现有 iPhone 和 iPad projects。
- 希望长时间 iOS UI tasks 保持 agentic 和 CLI-first，而不是依赖 Xcode GUI 的团队。

相关 skill：

- `build-ios-apps`：构建或重构 SwiftUI UI，采用 Liquid Glass 等现代 iOS patterns，审计 runtime performance，并通过 XcodeBuildMCP-backed workflows 在 simulators 上 debug apps。

#### 起始提示

**Scaffold app 和 build loop**

```text
Scaffold 一个 starter SwiftUI app，并添加一个 build-and-launch script，我可以把它接到本地环境中的 `Build` action。

约束：
- 保持 CLI-first。优先使用 Apple 的 `xcodebuild`；如果更干净的设置有帮助，可以使用 Tuist。
- 如果这个 repo 已经包含完整 Xcode project，请使用 XcodeBuildMCP 列出 targets，选择正确 scheme，build、launch，并在迭代时捕获 screenshots。
- 当现有 models、navigation patterns 和 shared utilities 已经存在时，复用它们。
- 除非我明确要求 shared Apple-platform implementation，否则让 app 聚焦 iPhone 和 iPad。
- 每次修改后使用小而可信的 validation loop，只有在较窄检查通过后才扩展到更广泛 builds。
- 告诉我你把它当成 greenfield scaffold 还是 existing-project change。

交付：
- app scaffold 或请求的 feature slice
- 带有确切命令的小型 build-and-launch script
- 你运行的最小相关验证步骤
- 你使用的确切 scheme、simulator 和 checks
```

#### 技术栈建议

| 需求 | 推荐默认项 | 原因 |
| --- | --- | --- |
| UI framework | [SwiftUI](https://developer.apple.com/documentation/swiftui/) | 在保持 UI code 可读的同时，为 iPhone 和 iPad 快速 prototype views、navigation 和 shared state。 |
| Build tooling | xcodebuild 或 [Tuist](https://docs.tuist.dev/) | 两者都能把 native build loop 留在终端中，而不是依赖 Xcode GUI。 |
| Project automation | [XcodeBuildMCP](https://www.xcodebuildmcp.com/) | 当你需要 Codex 检查 schemes 和 targets、启动 app、捕获 screenshots，并在不离开 agentic loop 的情况下持续迭代时，这是很强的选择。 |
| Distribution tooling | [App Store Connect CLI](https://asccli.sh/) | 让 agent 完全留在循环中，并直接把 app build 发送到 App Store。 |

#### Scaffold app 和 build loop

对于 greenfield 工作，先从普通提示开始。要求 Codex scaffold 一个 starter iOS SwiftUI app，并写一个小型 build-and-launch script，你可以把它接到 [local environment](37-local-environments.md) 中的 `Build` action。

保持循环 CLI-first。Apple 的 `xcodebuild` 可以从终端列出 schemes，并处理 build、test、archive、`build-for-testing` 和 `test-without-building` actions，让 Codex 留在 agentic loop 中，而不是跳进 Xcode GUI。

如果你想要更干净的项目生成器，并且愿意使用第三方工具，[Tuist](https://tuist.dev/) 是不错的下一步。它可以在不需要 GUI 的情况下生成并构建 Xcode projects，同时仍让 Codex 从终端 build 和 launch app。

当你已经进入完整 Xcode project 并需要更深入自动化时，使用 [XcodeBuildMCP](https://www.xcodebuildmcp.com/)。当 schemes、targets、simulator control、screenshots、logs 和 UI interaction 重要到普通 shell commands 不再够用时，就到了使用它的时候。

#### 利用 skills

第一版通常不需要 skill 或 MCP server。当工作变得专门，或你希望更强的 SwiftUI conventions 固化到运行中时，再添加 skills。

- [SwiftUI expert](https://github.com/AvdLee/SwiftUI-Agent-Skill) 是一个强通用 SwiftUI skill，内置大量最佳实践。
- [SwiftUI Pro](https://github.com/twostraws/SwiftUI-Agent-Skill/blob/main/swiftui-pro/SKILL.md) 是一个广泛的 SwiftUI review skill，覆盖现代 APIs、maintainability、accessibility 和 performance。
- [Liquid Glass expert](https://github.com/Dimillian/Skills/blob/main/swiftui-liquid-glass/SKILL.md) 帮助 Codex 采用新的 iOS 26 Liquid Glass APIs，并调整 custom components，使其符合最新系统设计。
- [SwiftUI performance](https://github.com/Dimillian/Skills/blob/main/swiftui-performance-audit/SKILL.md) 适用于功能感觉慢，或 SwiftUI view update path 看起来可疑的情况。它会扫描常见 SwiftUI 错误，并生成按优先级排序的修复位置和收益报告。
- [Swift concurrency expert](https://github.com/Dimillian/Skills/blob/main/swift-concurrency-expert/SKILL.md) 适用于难懂错误和 compiler warnings 开始阻碍你想做的改动时。在 GPT-5.4 上你可能不常需要它，但当 Swift concurrency diagnostics 变得嘈杂时，它仍有用。
- [SwiftUI view refactor](https://github.com/Dimillian/Skills/blob/main/swiftui-view-refactor/SKILL.md) 帮助保持文件更小，并让 SwiftUI code 在 repo 中更一致。
- [SwiftUI patterns](https://github.com/Dimillian/Skills/blob/main/swiftui-ui-patterns/SKILL.md) 随着 app 增长，帮助采用可预测的 `@Observable` 和 `@Environment` architecture patterns。

要了解如何安装和使用 skills，请参阅我们的 [skills documentation](48-agent-skills.md)。

#### 迭代

当第一版已经工作，或者你从现有项目开始，就可以开始迭代 UI 或 behavior。

这一部分要具体说明你想改什么，以及想怎么改。

把提示层说清楚：告诉 Codex 它是在 greenfield repo 还是现有 Xcode project 中工作，哪些 iOS devices 或 deployment targets 必须继续可用，以及你期待什么 validation loop。

##### 示例提示

例如，如果你想给现有 app 添加一个功能，可以这样要求 Codex 做变更：

#### 实用提示

##### 从基础开始

对于 greenfield 工作，从普通提示开始。要求 Codex scaffold 一个 starter SwiftUI app，并写一个小型 build-and-launch script，你可以把它接到 [local environment](37-local-environments.md) 中的 `Build` action。第一版通常不需要任何 skill 或 MCP server。

##### 使用小而可信的 validation loop

每次改动后，告诉 Codex 运行能真正证明你触碰契约的最窄命令。之后再扩展到更广泛 builds。这样可以保持 Codex 快速，而不是假装每次编辑都需要完整 app build。

##### 保持循环 CLI-first

保持循环 CLI-first。Apple 的 `xcodebuild` 工具可以从终端列出 schemes，并运行 build、test、archive、`build-for-testing` 和 `test-without-building` actions，让 Codex 留在 agentic loop 中，而不是跳进 Xcode GUI。

##### 利用 XcodeBuildMCP

一旦你在完整 Xcode project 中并需要更深入自动化，就使用 XcodeBuildMCP。到了 schemes、targets、simulator control、screenshots、logs 和 UI interaction 足够重要，普通 shell commands 不再能覆盖全部需求时，它就派上用场了。

#### 相关链接

- [Model Context Protocol](53-model-context-protocol.md)
- [Agent skills](48-agent-skills.md)
