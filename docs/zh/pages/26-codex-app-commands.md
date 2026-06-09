### Codex 应用命令

Source: [Codex app commands](https://developers.openai.com/codex/app/commands.md)

使用这些命令和键盘快捷键在 Codex app 中导航。

#### 键盘快捷键

|             | 操作               | macOS 快捷键               |
| ----------- | ------------------ | -------------------------- |
| **General** |                    |                            |
|             | 命令菜单           | Cmd + Shift + P or Cmd + K |
|             | 设置               | Cmd + ,                    |
|             | 键盘快捷键         | Cmd + /                    |
|             | 打开文件夹         | Cmd + O                    |
|             | 后退               | Cmd + [                    |
|             | 前进               | Cmd + ]                    |
|             | 增大字号           | Cmd + + or Cmd + =         |
|             | 减小字号           | Cmd + - or Cmd + \_        |
|             | 切换侧边栏         | Cmd + B                    |
|             | 切换 diff 面板     | Cmd + Option + B           |
|             | 切换终端           | Cmd + J                    |
|             | 清空终端           | Ctrl + L                   |
| **Thread**  |                    |                            |
|             | 新建线程           | Cmd + N or Cmd + Shift + O |
|             | 搜索线程           | Cmd + G                    |
|             | 在线程中查找       | Cmd + F                    |
|             | 上一个线程         | Cmd + Shift + [            |
|             | 下一个线程         | Cmd + Shift + ]            |
|             | 听写               | Ctrl + M                   |

要查找、自定义或重置快捷键，请打开 **Settings > Keyboard Shortcuts**。你可以按命令名称搜索，或将搜索字段切换到按键模式，然后按下你想查找的快捷键。

#### 搜索过去的线程并在线程中查找

使用线程搜索 (Cmd/Ctrl + G) 重新打开过去的对话。当你的 Codex 桌面 app 中可用扩展匹配时，它也可以匹配对话内容和 Git 分支名，因此你可以搜索线程中的短语，或搜索 `fix/login-redirect` 这样的分支。

打开线程后，使用 **Find in thread** (Cmd + F) 在当前对话中查找文本。它不会跨其它线程搜索。

#### 斜杠命令

Slash commands 让你无需离开线程输入框即可控制 Codex。可用命令会因你的环境和访问权限而异。

#### 使用斜杠命令

1. 在线程输入框中输入 `/`。
2. 从列表中选择命令，或继续输入以过滤（例如 `/status`）。

你也可以通过在线程输入框中输入 `$` 显式调用 skills。请参阅 [Skills](https://developers.openai.com/codex/skills)。

已启用的 skills 也会出现在 slash command 列表中。

#### 可用斜杠命令

| Slash command | 说明                                                                                   |
| ------------- | -------------------------------------------------------------------------------------- |
| `/feedback`   | 打开反馈对话框，以提交反馈并可选择包含日志。                                           |
| `/goal`       | 为 Codex 设置要持续推进的持久目标；先用 `/plan` 细化它。                               |
| `/mcp`        | 打开 MCP 状态以查看已连接服务器。                                                      |
| `/plan`       | 切换计划模式，用于多步骤规划。                                                         |
| `/review`     | 启动代码审查模式，以审查未提交更改或与基础分支比较。                                   |
| `/status`     | 显示线程 ID、上下文用量和速率限制。                                                     |

#### 使用 `/goal` 设置或管理目标

在 app 输入框中使用 `/goal` 启动 Goal mode。Goal 是 Codex 持续推进的持久目标，直到完成任务、暂停或需要更多输入。若要先与 Codex 一起定义目标，请先使用 `/plan`，然后用 `/goal` 设置细化后的目标。

如果 `/goal` 未出现在 slash command 列表中，请在 `config.toml` 中启用 `features.goals`：

```toml
[features]
goals = true
```

你也可以从 CLI 运行 `codex features enable goals`，或让 Codex 运行它。

当 goal 处于活动状态时，app 会在输入框上方显示进度。使用该进度行中的按钮暂停或恢复目标、编辑目标文本，或清除目标，而不是输入另一个 slash command。Goal 运行时，你仍可以用后续消息继续引导 Codex。

有关编写有效目标的指导，请参阅 [Goal mode](https://developers.openai.com/codex/prompting#goal-mode)。

#### 深度链接

Codex app 注册了 `codex://` URL scheme，因此链接可以直接打开 app 的特定部分。

#### 常见链接

当你只需要打开常见 app 目标位置时，请使用这些链接。下面各部分按链接类型列出完整参考。

| Deep link             | 打开                                                  |
| --------------------- | ----------------------------------------------------- |
| `codex://threads/new` | 新的本地线程。                                        |
| `codex://threads/<session-id>` | 本地线程。`<session-id>` 必须是该线程的会话 UUID。            |
| `codex://settings`    | Settings。                                             |
| `codex://skills`      | Skills。                                               |
| `codex://automations` | 打开创建流程的 Automations 页面。                     |

#### 线程

当你需要打开现有本地线程或启动新线程时，请使用这些链接。

| Deep link             | 打开                                                  |
| --------------------- | ----------------------------------------------------- |
| `codex://threads/<session-id>` | 本地线程。`<session-id>` 必须是该线程的会话 UUID。            |
| `codex://threads/new` | 新的本地线程。                                        |

对于 `codex://threads/new`，可按需添加以下查询参数；你可以在同一 URL 中组合它们。

| Query parameter | Required | 作用                                                                                                                                                            |
| --------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prompt=`       | No       | 设置初始输入框文本。                                                                                                                                            |
| `path=`         | No       | 在本地工作区中打开新线程。`path` 必须是指向本地目录的绝对路径。有效时，Codex 会将该目录用作活动工作区。                                                          |
| `originUrl=`    | No       | 通过 Git remote URL 匹配你当前工作区根目录之一。如果同时存在 `path`，Codex 会先解析 `path`。                                                                    |

示例：[Show me some fun stats about how I've been using Codex](codex://threads/new?prompt=Show%20me%20some%20fun%20stats%20about%20how%20I%27ve%20been%20using%20Codex)

#### 设置

当你需要打开 Settings 或特定设置页面时，请使用这些链接。

| Deep link                                     | 打开                                     |
| --------------------------------------------- | ---------------------------------------- |
| `codex://settings`                            | Settings。                                |
| `codex://settings/browser-use`                | Browser use 设置。                       |
| `codex://settings/computer-use/google-chrome` | 用于 computer use 的 Google Chrome 设置。 |
| `codex://settings/connections`                | Remote connections 设置。                |

#### 技能

当你需要打开 Skills 时，请使用这些链接。

| Deep link        | 打开    |
| ---------------- | ------- |
| `codex://skills` | Skills。 |

#### 自动化

当你需要打开 Automations 时，请使用这些链接。

| Deep link             | 打开                                   |
| --------------------- | -------------------------------------- |
| `codex://automations` | 打开创建流程的 Automations 页面。 |

#### 插件

Plugin links 会根据你是在打开插件、从 marketplace 安装，还是使用本地 `marketplace.json` 而采用不同形式。有关插件基础，请参阅 [Plugins](https://developers.openai.com/codex/plugins)。有关本地或仓库 marketplace 设置，请参阅 [Build plugins](https://developers.openai.com/codex/plugins/build#build-your-own-curated-plugin-list)。

#### 插件详情

| Deep link          | 打开                  |
| ------------------ | --------------------- |
| `codex://plugins/` | 插件详情页。          |

`` 必须标识插件。对于 OpenAI-curated 插件，请使用 `@openai-curated` 形式。

Codex 生成的 plugin links 也可以包含这些查询参数。手写链接时省略两者。

| Query parameter | Required | 作用                                                                                                                                             |
| --------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `hostId=`       | No       | 标识拥有插件上下文的 Codex host，例如 `local` 或你配置的 remote connection 之一。Codex 会提供这些 ID。        |
| `source=manage` | No       | 保留 app 的插件管理入口点。它不是仅管理员可用。                                                                                         |

示例：[Open the OpenAI Developers plugin](codex://plugins/openai-developers@openai-curated)

#### 本地插件

有关本地或仓库 marketplace 设置，请参阅 [Build plugins](https://developers.openai.com/codex/plugins/build#build-your-own-curated-plugin-list)。

| Deep link                           | 打开                                                 |
| ----------------------------------- | ---------------------------------------------------- |
| `codex://plugins/?marketplacePath=` | 来自本地 marketplace 的本地插件详情页。              |

| Query parameter    | Required | 作用                                                                                                       |
| ------------------ | -------- | ---------------------------------------------------------------------------------------------------------- |
| `marketplacePath=` | Yes      | 指向本地 `marketplace.json` 的绝对路径，例如 `/Users/alex/.agents/plugins/marketplace.json`。       |
| `mode=share`       | No       | 打开该本地插件的分享流程。                                                                          |

#### 宠物

当该功能启用时，使用这些链接打开 pet 安装流程。

| Deep link                              | 打开                  |
| -------------------------------------- | --------------------- |
| `codex://pets/install?name=&imageUrl=` | pet 安装流程。     |

| Query parameter | Required | 作用                                              |
| --------------- | -------- | ------------------------------------------------- |
| `name=`         | Yes      | 设置 pet 名称。                                  |
| `imageUrl=`     | Yes      | 设置 pet 图像 URL。`imageUrl` 必须是 HTTPS。     |
| `description=`  | No       | 设置可选 pet 描述。                              |

#### App 命令参考

- [Features](https://developers.openai.com/codex/app/features)
- [Settings](https://developers.openai.com/codex/app/settings)
