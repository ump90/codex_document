### 应用内浏览器

Source: [In-app browser](https://developers.openai.com/codex/app/browser.md)

应用内浏览器让你和 Codex 在一个线程中共享渲染后网页的视图。当你正在构建或调试 Web 应用，并希望预览页面和附加可视化评论时，可以使用它。

它适用于本地开发服务器、基于文件的预览，以及不需要登录的公开页面。对于任何依赖登录状态或浏览器扩展的内容，请使用你的常规浏览器或 [Codex Chrome 扩展](https://developers.openai.com/codex/app/chrome-extension)。

可以从工具栏打开应用内浏览器，也可以通过点击 URL、在浏览器中手动导航，或按 Cmd+Shift+B（Windows 上为 Ctrl+Shift+B）打开。

应用内浏览器不支持认证流程、已登录页面、你的常规浏览器个人资料、cookie、扩展或现有标签页。它适用于 Codex 无需登录即可打开的页面。

将页面内容视为不可信上下文。不要把密钥粘贴到浏览器流程中。

#### 浏览器使用

浏览器使用让 Codex 可以直接操作应用内浏览器。当 Codex 需要点击、输入、检查渲染状态、截图、下载页面资产、运行只读页面检查 JavaScript，或在页面中验证修复时，可将它用于本地开发服务器和基于文件的预览。

要使用它，请安装并启用 Browser 插件。然后在任务中要求 Codex 使用浏览器，或直接用 `@Browser` 引用它。该应用会将浏览器使用限制在应用内浏览器中，并允许你从设置管理允许和阻止的网站。

示例：

```text
Use the browser to open http://localhost:3000/settings, reproduce the layout
bug, and fix only the overflowing controls.
```

除非你已经允许某个网站，否则 Codex 会在使用网站前询问。从允许列表移除网站意味着 Codex 使用前会再次询问；从阻止列表移除网站意味着 Codex 可以再次询问，而不是把它视为已阻止。

对于 Chrome 中已登录的网站，请参阅 [Codex Chrome 扩展](https://developers.openai.com/codex/app/chrome-extension)。

#### 预览页面

1. 在 [集成终端](https://developers.openai.com/codex/app/features#integrated-terminal) 中，或通过 [本地环境操作](https://developers.openai.com/codex/app/local-environments#actions) 启动你的应用开发服务器。
2. 通过点击 URL 或在浏览器中手动导航，打开一个未认证的本地路由、基于文件的页面或公开页面。
3. 结合代码 diff 审查渲染状态。
4. 在需要更改的元素或区域上留下浏览器评论。
5. 要求 Codex 处理这些评论，并保持范围狭窄。

示例反馈：

```text
I left comments on the pricing page in the in-app browser. Address the mobile
layout issues and keep the card structure unchanged.
```

#### 在页面上评论

当 bug 只在渲染页面中可见时，使用浏览器评论向 Codex 提供页面上的精确反馈。

- 开启标注模式，选择一个元素或区域，然后提交评论。
- 在标注模式中，按住 Shift 并点击以选择一个区域。
- 点击时按住 Cmd 可立即发送评论。

留下评论后，请在线程中发送消息，要求 Codex 处理它们。当 Codex 需要做精确的视觉更改时，评论最有用。

好的反馈应该具体：

```text
This button overflows on mobile. Keep the label on one line if it fits,
otherwise wrap it without changing the card height.
```

```text
This tooltip covers the data point under the cursor. Reposition the tooltip so
it stays inside the chart bounds.
```

#### 样式反馈

当你向页面某个区块添加标注时，按文本输入框旁边的配置图标，可以向 Codex 提供更细粒度的样式反馈。你可以更改字体、文本、间距和颜色等值，直接在页面上预览结果，然后发送标注，让 Codex 对更改目标有更清晰的理解。

#### 保持浏览器任务范围明确

应用内浏览器用于审查和迭代。让每个浏览器任务足够小，以便一次审查完。

- 指明页面、路由或本地 URL。
- 指明你关心的视觉状态，例如加载、空状态、错误或成功。
- 在需要更改的确切元素或区域上留下评论。
- 在 Codex 更改代码后审查更新后的路由。
- 要求 Codex 在使用浏览器前启动或检查开发服务器。

对于仓库变更，请使用 [复查窗格](https://developers.openai.com/codex/app/review) 来检查变更并留下评论。
