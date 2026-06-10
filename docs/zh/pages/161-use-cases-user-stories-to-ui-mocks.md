### 把用户故事转成 UI mockups

Source: [Turn user stories into UI mocks](https://developers.openai.com/codex/use-cases/user-stories-to-ui-mocks.md)

把产品反馈、issue threads 和设计上下文转成团队可以反馈并实现的 mockups。

#### 概览

使用 Codex 从 Slack、Linear、Google Drive 收集产品反馈，将其规范化为 user stories 和 constraints，然后用 ImageGen 生成 UI mockups。方向确定后，再把 mock 转成 working prototype。

适合：

- 把分散反馈转成某个功能视觉方向的 product teams。
- 希望在构建前基于源材料生成 mockups 的 design 和 engineering teams。
- 希望基于用户反馈快速迭代的团队。

相关 skill：

- `slack`：搜索已批准 feedback channels 和 threads，获取 user stories、pain points、quotes 和 open questions。
- `linear`：把 feature requests、bug reports、labels、priorities 和 project context 拉入 mock brief。
- `google-drive`：读取包含 product feedback 或 design requirements 的 research notes、call summaries、docs、sheets 和 slides。
- `figma`：获取 design context、screenshots 和 design-system references，避免 mocks 偏离产品视觉语言。
- `$imagegen`：根据综合后的 stories 和 design constraints 生成 UI mockups、variations 和 visual truth。
- `build-web-apps`：把选定 mock 转成 working web prototype，并根据 mock 验证实现。

#### 起始提示

**从用户故事创建 mocks**

```text
把这个 [user story/set of user feedbacks] 转成一个 UI mock，用于解决该问题的功能，并使用以下来源作为上下文：

- @slack [channels or thread links]
- @linear [issue links, project, team, or view]
- @google-drive [research notes, survey export, doc, sheet, or slide deck]

执行时请尊重当前 design system 和现有 UI [provide Figma file or screenshot as reference]。
```

建议使用中等推理强度。

#### 简介

产品团队经常从多种来源收集反馈，例如 Slack threads、Linear issues、Google Drive docs 或 sheets，或客户电话 notes。有时他们已经有清晰的 user stories 来说明想解决的问题，有时上下文就分散在这些来源中。

Codex 可以收集这些上下文，把它转成一个能解决问题的功能 UI mock；验证后，还可以把它实现进产品。

#### 生成 visual truth

如果你已经有清晰 user story，可以从那里开始。如果没有，可以先和 Codex 讨论，让它从不同来源收集上下文，并综合成 user story。

然后，你可以要求 Codex 使用 ImageGen 创建几个 mock directions。Mocks 应保留产品的信息架构和 design-system constraints。

如果有帮助，可以提供当前 UI 的 screenshots 或 Figma file 作为参考。

持续这样迭代，直到你对 mock 满意。变更范围越明确，Codex 越有可能生成可直接实现的 mock。

#### 从 mock 转向 prototype

使用你希望 Codex 实现的最终 mock image。请在新的 turn 中重新附上这张图片，而不是直接继续之前的对话。

然后你可以要求 Codex 实现该 mock。如果你正在构建 web app，可以选择使用 Build Web Apps plugin；相关安装和使用方式见 [Codex plugins](78-plugins.md)，它可以把 mock 转成 working prototype：

#### 相关链接

- [Codex plugins](78-plugins.md)
