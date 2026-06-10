### 让 Codex 使用你的电脑

Source: [Use your computer with Codex](https://developers.openai.com/codex/use-cases/use-your-computer-with-codex.md)

让 Codex 在你的 Mac 上点击、输入并浏览 apps。

#### 概览

使用 Computer Use，把跨 Mac apps、windows 和 files 的多步骤任务交给 Codex。

适合：

- 跨 app、windows、browser sessions 或 Mac 本地文件移动的任务。
- 你想交出去，并让 Codex 在后台继续处理的工作。

#### 起始提示

**交出一个电脑任务**

```text
@Computer [do the task you want completed across your Mac]

例如：
- Play some music to help me focus.
- Help me add my interview notes from Notes to Ashby.
- Look through my Messages app for the trip ideas Brooke sent me this week, add the best options to a new note called "Yosemite ideas", and draft a reply back to her.
```

#### 简介

你可以让 Codex 像你一样操作 app：点击、查看和输入。[Computer Use](35-computer-use.md) 适用于任务存在于普通 app UI 中的情况，即使该 app 没有专用 plugin。

它特别适合会在多个 apps 或 windows 之间跳转的任务，例如收集 notes、更新 system of record、把细节从一个地方复制到另一个地方，或在几个不同 apps 中检查上下文后起草回复。

#### 如何使用

1. 安装 [Computer Use plugin](35-computer-use.md)。
2. 以 `@Computer` 开始请求，或提到具体 app，例如 `@Slack` 或 `@Messages`。
3. 描述任务和你想要的结果。
4. 当 Codex 需要访问权限时批准，然后让它在后台继续任务。

如果你提到具体 app，且该 app 存在 plugin，Codex 可能会优先使用 plugin，而不是 Computer Use。这通常是你想要的。如果没有 plugin，Codex 可以回退到 Computer Use，并直接操作 app。

例如：

- `@Computer Play some music to help me focus.`
- `@Computer Help me add my interview notes from Notes to Ashby.`
- `@Computer Go through my Slack and add reminders for everything I need to do by end of day.`

#### 实用提示

##### 选择 Codex 应使用的浏览器

Computer Use 会控制它正在操作的 app。如果你想在一个浏览器中继续工作，而让 Codex 在另一个浏览器中浏览，请告诉它使用哪个浏览器。你也可以在 [customization](52-customization.md) 中设置默认值，例如：“When using Computer Use for web browsing tasks, default to Chrome instead of Safari.”

##### 避免在同一 app 中并行运行

不要让两个 Computer Use tasks 同时操作同一个 app。这样会让 Codex 更难保持关于当前 window 和 state 的稳定上下文。

##### 保持已登录

为了让运行更顺畅，请确保你已经登录希望 Codex 使用的 apps 和 services。如果你的 Mac 在 Computer Use 运行时锁屏，活动会停止。

#### 好的后续操作

任务完成后，如果你希望 Codex 总结它改了什么、再次检查结果，或通过 [customization](52-customization.md) 把工作流转成更可重复的模式，请保持同一线程打开。

#### 建议提示

**交出一个电脑任务**

#### 相关链接

- [Computer Use](35-computer-use.md)
- [Plugins](78-plugins.md)
- [Customize Codex](52-customization.md)
