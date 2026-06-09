### Codex IDE 扩展斜杠命令

Source: [Codex IDE extension slash commands](https://developers.openai.com/codex/ide/slash-commands.md)

斜杠命令让你无需离开聊天输入框即可控制 Codex。使用它们检查状态、在本地和云模式之间切换，或发送反馈。

#### 使用斜杠命令

1. 在 Codex 聊天输入框中输入 `/`。
2. 从列表中选择一个命令，或继续输入以筛选（例如 `/status`）。
3. 按 **Enter**。

#### 可用的斜杠命令

| 斜杠命令             | 说明                                                            |
| -------------------- | --------------------------------------------------------------- |
| `/auto-context`      | 开启或关闭 Auto Context，以自动包含最近文件和 IDE 上下文。      |
| `/cloud`             | 切换到云模式以远程运行任务（需要云访问权限）。                  |
| `/cloud-environment` | 选择要使用的云环境（仅在云模式中可用）。                        |
| `/feedback`          | 打开反馈对话框以提交反馈，并可选择包含日志。                    |
| `/goal`              | 为 Codex 设置一个持续跟踪的持久目标。                           |
| `/local`             | 切换到本地模式，在你的工作区中运行任务。                        |
| `/review`            | 启动代码审查模式，以审查未提交变更或与基准分支比较。            |
| `/status`            | 显示线程 ID、上下文用量和速率限制。                             |

如果 `/goal` 没有出现在斜杠命令列表中，请在 `config.toml` 中启用 `features.goals`：

```toml
[features]
goals = true
```

你也可以从 CLI 运行 `codex features enable goals`，或要求 Codex 运行它。
