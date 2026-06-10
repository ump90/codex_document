### 添加 Mac telemetry

Source: [Add Mac telemetry](https://developers.openai.com/codex/use-cases/macos-telemetry-logs.md)

使用 Codex 为一个 Mac 功能接入 Logger，运行 app，并从 unified logs 验证该操作。

#### 概览

使用 Codex 和 Build macOS Apps plugin，在窗口、sidebars、commands 或 sync flows 周围添加少量高信号 `Logger` 事件，然后运行 app，并从 Console 或 `log stream` 证明正确操作已触发。

适合：

- Codex 需要可靠追踪窗口打开、sidebar selection、menu commands、menu bar actions、sync milestones 或 fallback paths 的 Mac app 功能。
- 需要 Codex patch 代码、重新运行 app、检查日志，并根据证据决定下一处修复，而不是靠猜测的 agentic debugging loops。
- 本地 app-session collection loops，用于收集紧凑的用户操作和 app lifecycle events 序列，并在重复运行之间比较。

相关 skill：

- `build-macos-apps`：使用 macOS telemetry 和 build/run skills 添加结构化 `OSLog` instrumentation，启动 app，执行 UI 路径，并从 Console 或 `log stream` 验证发出的事件。

#### 起始提示

**为一个功能加 instrumentation，并从日志验证**

```text
使用 Build macOS Apps plugin，为 [name one Mac feature or action flow] 添加轻量 unified logging，然后运行 app，并从日志验证这些事件按预期顺序触发。

约束：
- 优先使用来自 `OSLog` 的 `Logger`，不要使用 `print`，并为这个功能创建清晰的 subsystem/category pair，方便过滤日志。
- 为每个重要 action boundary 或 state transition 记录一行简洁日志：例如 window opened、sidebar selection changed、menu command invoked、sync started、sync finished 或 fallback path taken。
- 保持永久 `info` logs 稳定且高信号。仅把 `debug` 用于嘈杂的本地细节，并在完成前移除或降级临时 instrumentation。
- 不要记录 secrets、auth tokens、personal data 或 raw document contents。如果必须记录 identifier，请选择最安全的 privacy annotation，并解释原因。
- 构建并运行 app，亲自执行功能路径，并通过 Console 或聚焦的 `log stream` predicate 验证事件。
- 如果 flow 很长、不稳定，或更适合手动复现，请把过滤后的 log stream 保存到一个小型本地 session trace file；如有需要，让我手动操作 app，然后读取该文件并总结 event timeline。
- 如果预期事件没有出现，把 log 移到更接近疑似 control path 的位置，重新运行 flow，并持续推进，直到日志解释发生了什么。

交付：
- 新的 logger setup 和你添加的确切 events
- 你使用的 Console filter 或 `log stream` predicate
- 日志现在让哪些内容可观察的简短 before/after 总结
- 如果这变成了较长的 capture session，提供保存的 trace file 和 timeline summary
- 一两行代表性 log lines，用来证明 flow 已正确接入 instrumentation
```

#### 技术栈建议

| 需求 | 推荐默认项 | 原因 |
| --- | --- | --- |
| App logging | [OSLog Logger](https://developer.apple.com/documentation/os/logger) | 结构化 unified logging 给 Codex 一个狭窄、可过滤的反馈循环，而不会把代码库变成一墙 `print` 语句。 |
| Agent workflow | [Build macOS Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-macos-apps) | 该 plugin 的 telemetry 和 build/run skills 被设计为协同工作：为一个 flow 添加 instrumentation，启动 app，检查日志，并收紧 event set。 |
| Runtime verification | Console.app 和 `log stream --predicate ...` | 具体的 log filter 加 sample output 给 agent 一个可重复交接点，也让新 instrumentation 易于跨运行验证。 |

#### 在调试变模糊的地方添加一个 Logger

这个用例适用于那些仅靠代码审查无法调试的 Mac app flow，因为“发生了某件事”太模糊。让 Codex 围绕一个行为添加几条高信号 unified logs，运行 app，触发该行为，并从 Console 或 `log stream` 验证预期事件已经触发。

这个循环可以使用 [Build macOS Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-macos-apps)。它的 macOS telemetry skill 刻意保持轻量：使用 Apple 的 `Logger`，选择清晰的 subsystem/category pair，记录 action boundaries 和 state transitions，避免敏感 payload，并在本地 build/run 后验证事件，而不是假设 instrumentation 已正确接入。

#### telemetry 为什么对 agentic engineering 有用

好日志会在每次 patch 后给 Codex 一个可重复反馈循环。你不需要手动检查每个窗口、菜单操作或 sync transition；agent 可以运行 app、执行 flow、检查过滤后的日志，并根据证据决定下一处代码改动。

这对三类 agentic loops 尤其有用：

- **Hands-free debug loop：** Codex 为可疑 flow 添加 instrumentation，启动 app，点击 sidebar 或触发 command，读取发出的日志序列，patch state update path，并重新运行同一 flow，直到日志和 UI 行为一致。
- **App session collection loop：** Codex 为 app launch、window open、sidebar selection、import started、import finished 和 import failed 各加一个事件，然后运行本地 session 并总结 timeline，让缺失或乱序的 transitions 变得明显。
- **Human-driven capture loop：** Codex 在启用 logging 的情况下启动 app，在你手动执行棘手 flow 时保持一个聚焦 log stream 运行，然后在捕获 session 后检查它，并根据 trace 提出下一处 patch。

#### 保持 instrumentation 小而可过滤

要求 Codex 为每个 feature area 添加一个 logger，而不是为每个 state mutation 添加一条永久日志。`Windowing`、`Commands`、`MenuBar`、`Sidebar`、`Sync` 或 `Import` 这样的 feature categories，会让下一轮调试时的日志过滤简单得多。

```swift
import OSLog

private let logger = Logger(
  subsystem: Bundle.main.bundleIdentifier ?? "SampleApp",
  category: "Sidebar"
)

@MainActor
func selectItem(_ item: SidebarItem) {
  logger.info("Selected sidebar item: \(item.id, privacy: .public)")
  selection = item.id
}
```

使用 `info` 记录随时间仍有用的简洁 action 和 lifecycle events；使用 `debug` 记录更嘈杂的本地 state details，它们可以在任务完成前移除或降级。只有在测量 timing span 时才添加 signposts，不要默认添加。

#### 要求 Codex 从日志证明事件

有用的部分不只是添加 `Logger` 调用。要求 Codex 运行 app、触发已接入 instrumentation 的 flow，并给出它使用的确切 Console filter 或 `log stream` predicate，以及一两行代表性日志。

```bash
log stream --style compact --predicate 'subsystem == "com.example.app" && category == "Sidebar"'
```

如果预期事件没有出现，要求 Codex 把日志移到更接近疑似 control path 的位置，重新运行同一 flow，并持续迭代，直到日志解释发生了什么。如果任务转成 crash 或 backtrace 分析，请切换到 plugin 的 build/run debugging workflow，并让 telemetry 继续聚焦在 action boundaries 上。

#### 为后续 Codex pass 保存 session trace

对于更长或间歇性 bug，要求 Codex 把聚焦 log stream 保存到一个小型本地 trace file，总结 timeline，并把该 artifact 留在 workspace 中。这样后续 Codex 运行可以检查同一证据，而不用凭记忆重放整个 session。这会让多轮 debugging 更容易，尤其是你希望一个 agent run 收集 trace，另一个 run 比较 patch 前后行为时。

当人类需要驱动 session 的一部分时，这也很好用。要求 Codex 在 logging-friendly debug loop 中启动 app，开始过滤捕获，在你手动复现问题时等待，然后在你完成后读取保存的 trace file。

#### 实用提示

##### 一次只为一个功能添加 instrumentation

从一个 sidebar、window、command 或 sync path 开始，让日志序列保持易于检查。如果该路径变得可靠，Codex 可以把同样模式扩展到相邻 flows。

##### 把隐私写进提示

要求 Codex 解释每个被记录的 identifier，并避免把 secrets、personal data 或 raw content 写入 unified logs。用于本地调试时，一个很小的 event vocabulary 通常就足够。

##### 在最终总结中保留 sample output

代表性日志行比“已添加 telemetry”更容易信任。要求 Codex 包含 filter predicate 和简短 action timeline，让下一次 agent run 可以复用同一验证循环。

#### 相关链接

- [Build macOS Apps plugin](https://github.com/openai/plugins/tree/main/plugins/build-macos-apps)
- [Agent skills](48-agent-skills.md)
