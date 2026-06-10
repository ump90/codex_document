### 在 iOS Simulator 中调试

Source: [Debug in iOS simulator](https://developers.openai.com/codex/use-cases/ios-simulator-bug-debugging.md)

使用 Codex 和 XcodeBuildMCP 驱动应用在 iOS Simulator 中运行、捕获证据，并迭代到修复。

#### 概览

使用 Codex 发现正确的 Xcode scheme 和 simulator，启动应用，检查 UI tree，执行 tap、type、swipe，捕获 screenshots 和 logs，必要时附加 LLDB，并把模糊 bug 报告转化为小而已验证的修复。

适合：

- 只在 Simulator 中经过特定 tap、scroll 或表单输入路径后出现的 UI bugs。
- Codex 需要 logs、screenshots、view hierarchy state 和 debugger backtrace 后才编辑代码的 crashes、hangs 或 broken navigation。
- 希望 Codex 负责 reproduce-fix-verify 循环，而不是让人手动点击每个状态的团队。

相关 skill：

- [`build-ios-apps`](https://github.com/openai/plugins/tree/main/plugins/build-ios-apps)：使用 iOS debugger agent 通过 XcodeBuildMCP 在 simulator 上构建、启动、检查并驱动 app，然后在 Codex 缩小 bug 范围时捕获 logs、screenshots 和 stack traces。

#### 起始提示

**复现、诊断并修复一个 Simulator Bug**

```text
使用 Build iOS Apps plugin 和 XcodeBuildMCP，直接在 Simulator 中复现这个 bug，诊断根因，并实现一个小修复。

Bug report:

[Describe the expected behavior, the actual bug, and any known screen or account setup.]

约束：
- 首先检查是否已选择 project、scheme 和 simulator。如果没有，请发现正确的 Xcode project 或 workspace，选择 app scheme，选择 simulator，并在本 session 剩余部分复用该设置。
- 在 Simulator 中构建并启动 app，然后在开始交互前，通过 UI snapshot 或 screenshot 确认正确屏幕可见。
- 自己通过在 simulator 中 tapping、typing、scrolling 和 swiping 驱动精确复现路径。优先使用 accessibility labels 或 IDs，而不是原始坐标；当 layout 变化时，在下一步操作前重新读取 UI hierarchy。
- 调试时捕获证据：用于视觉状态的 screenshots、失败附近的 simulator logs，以及如果 bug 看起来像 crash 或 hang 时的 LLDB stack frames 或 variables。
- 如果 simulator 尚未启动，请启动一个，并告诉我你选择了哪个 device 和 OS。如果需要 credentials 或特殊 fixture，请暂停并只询问缺失输入。
- 做出解决 bug 的最小代码变更，然后重新运行 simulator flow，并告诉我你如何精确验证修复。

交付：
- Codex 执行的 reproduction steps
- 解释 bug 的关键 screenshots、logs 或 stack details
- code fix 以及它为什么有效
- 最终验证使用的 simulator 和 scheme
```

#### 相关链接

- [Build iOS Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-ios-apps)
- [Model Context Protocol](53-model-context-protocol.md)
- [Agent skills](48-agent-skills.md)

#### 技术栈

| 需求 | 推荐默认选择 | 原因 |
| --- | --- | --- |
| Simulator 自动化 | [XcodeBuildMCP](https://www.xcodebuildmcp.com/) | 当前工具表面覆盖 simulator setup、build and launch、UI snapshots、taps、typing、gestures、screenshots、log capture 和 debugger attachment。 |
| Agent 工作流 | [Build iOS Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-ios-apps) | 该 plugin 的 iOS debugger agent 为 Codex 提供清晰的 simulator-first 循环，用于复现 bug、收集证据，并在每次变更后验证修复。 |
| 应用可观测性 | `Logger`、`OSLog`、LLDB 和 Simulator screenshots | Codex 可以使用 logs 和 debugger state 解释哪里坏了，然后保存 screenshots 证明修复前后的精确 UI 状态。 |

## 给 Codex 完整 simulator 循环

当 Codex 负责完整循环时，这个用例效果最好：选择正确 app target，在 Simulator 中启动应用，检查当前屏幕，执行复现步骤，收集 logs 和 screenshots，必要时检查 stack trace，修补代码，并重新运行同一路径证明 bug 已消失。

当你希望该循环保持 agentic 时，使用 [Build iOS Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-ios-apps)。它的 iOS debugger 工作流围绕 XcodeBuildMCP 构建，这意味着 Codex 可以与已启动的 simulator 交互，并收集人类通常会手工收集的同类证据。

当 XcodeBuildMCP 配置了 simulator automation、UI automation、debugging 和 logging workflows 时，Codex 可以负责完整 reproduce-debug-verify 循环。如果 Codex 尚未选择 project、scheme 和 simulator，请先让它发现这些内容，并在 session 剩余部分复用该设置。

## 利用 XcodeBuildMCP 的能力

这些是值得提示 Codex 使用的实用能力组：

- Project 和 simulator discovery：检查 Codex 是否已知道应使用哪个 app target 和 simulator，发现 Xcode project 或 workspace，枚举 schemes，查找或启动 simulator，并让该设置在后续 build/run 步骤中保持稳定。
- Build 和 launch control：构建 active app target，安装并启动 simulator build，在需要时带 log capture 重新启动，并在 Codex 需要检查 app-specific runtime logs 时解析 app bundle id。
- UI inspection 和 interaction：读取屏幕上的 accessibility hierarchy、截图、tap controls、向 fields 输入、滚动 lists，并执行 edge swipes 或其他 simulator gestures。
- Logs 和 debugger state：流式读取 simulator logs，将 LLDB 附加到运行中的 app，设置 breakpoints，检查 stack frames 和 local variables，并在 crash 或 hang 需要更深入检查时运行 debugger commands。

关键习惯是要求 Codex 在 tap 前检查 view tree。XcodeBuildMCP 暴露 accessibility hierarchy 和坐标，因此 Codex 可以优先使用稳定 labels 或 element IDs，而不是猜测原始屏幕位置。

## 将模糊 bug 转化为可复现脚本

当你的提示给出一个具体 bug 和一个预期结果，然后让 Codex 自主驱动 app 并收集证据时，iOS debugger skill 最有效。如果需要登录、deep link 或 test fixture，请一次说明，并让 Codex 只有在缺失输入阻塞进度时才暂停。

## 实用技巧

### 要求证据，而不只是修复

要求 Codex 给出用于解释 bug 的确切 simulator、scheme、screenshots、log snippets 和 stack details。相比“我觉得这能修复”，这会让最终 patch 容易审查得多。

### 优先使用 accessibility labels 而不是坐标

如果 Codex 因为某个 control 没有稳定 label 或 accessibility identifier 而必须按坐标 tap，请让它指出这一点。这通常也意味着 bug 修复应包含小的 UI testability 改进。

### 每次运行只处理一个 bug

Simulator-driven debugging 循环很强大，但当一个提示只针对一种 failure mode 时，仍然更容易信任。让 Codex 先完成一个 reproduce-fix-verify 循环，再扩展到相邻问题。
