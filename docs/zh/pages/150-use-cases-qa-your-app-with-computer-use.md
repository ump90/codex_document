### 使用 Computer Use 对 app 做 QA

Source: [QA your app with Computer Use](https://developers.openai.com/codex/use-cases/qa-your-app-with-computer-use.md)

点击真实产品流程，并记录哪里出错。

#### 概览

使用 Computer Use 执行关键流程、发现问题，并以 bug report 收尾。

适合：

- 发布前验证真实用户流程的团队。
- 需要以 severity、repro steps 和简短 triage summary 结束的 QA loops。

#### 起始提示

**运行结构化 QA pass**

```text
@Computer Test my app in [environment].

Test these flows:
- [hero use case 1]
- [hero use case 2]
- [hero use case 3]

For every bug you find, include:
- repro steps
- expected result
- actual result
- severity

Keep going past non-blocking issues and end with a short triage summary.
```

#### 简介

Computer Use 非常适合 QA passes，因为它可以看到界面、点击流程、在字段中输入，并记录失败之处。这让它能在真实用户旅程中捕获功能 bug 和 UI 问题。

关键是告诉 Codex 要测试什么环境、哪些流程最重要，以及你希望返回什么报告。

#### 如何使用

1. 安装 [Computer Use plugin](35-computer-use.md)。
2. 告诉 Codex 要测试哪个 app、build 或 environment。
3. 说明你最关心的 flows 或 hero use cases。
4. 要求结构化报告，方便 triage 或 hand off。

你可以保持宽泛：

- `@Computer Test my app. Find any major issues and give me a report.`

也可以更明确：

- `@Computer Test my app in staging. Cover signup, invite a teammate, and upgrade billing. Log every bug with repro steps, expected result, actual result, and severity.`

如果 repo 中已有 test-plan 文件，请把它附到线程，或指向它，让 QA pass 遵循现有 flows。

#### 实用提示

##### 明确说明设置

如果 account state、test data、feature flags 或 environment choice 会影响流程，请在一开始就说明。Codex 知道自己是在测试 local、staging 还是 production-like behavior 时，会产生更好的结果。

##### 说明你关心的问题类型

明确你希望 Codex 聚焦 broken functionality、layout issues、confusing copy、visual regressions，还是全部都要。

##### 决定停止还是继续

如果一个 blocking issue 应终止本轮运行，请说明。否则告诉 Codex 继续完成剩余 flow，并在总结前收集所有 non-blocking issues。

#### 好的后续操作

QA pass 之后，保持同一线程打开，并要求 Codex 修复它发现的某个 bug，把 findings 转成 Linear 或 GitHub-ready drafts，或把下一轮 pass 缩小到一个具体 failing flow。

#### 建议提示

**运行结构化 QA pass**

#### 相关链接

- [Computer Use](35-computer-use.md)
- [Codex skills](48-agent-skills.md)
