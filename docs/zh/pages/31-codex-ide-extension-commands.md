### Codex IDE 扩展命令

Source: [Codex IDE extension commands](https://developers.openai.com/codex/ide/commands.md)

使用这些命令从 VS Code 命令面板控制 Codex。你也可以把它们绑定到键盘快捷键。

#### 分配键绑定

要为 Codex 命令分配或更改键绑定：

1. 打开命令面板（macOS 上为 **Cmd+Shift+P**，Windows/Linux 上为 **Ctrl+Shift+P**）。
2. 运行 **Preferences: Open Keyboard Shortcuts**。
3. 搜索 `Codex` 或命令 ID（例如 `chatgpt.newChat`）。
4. 选择铅笔图标，然后输入你想要的快捷键。

#### 扩展命令

| 命令                      | 默认键绑定          | 说明                                       |
| ------------------------- | ------------------- | ------------------------------------------ |
| `chatgpt.addToThread`     | -                   | 将选中的文本范围作为当前线程的上下文添加   |
| `chatgpt.addFileToThread` | -                   | 将整个文件作为当前线程的上下文添加         |
| `chatgpt.newChat`         | macOS: `Cmd+N`      |
| Windows/Linux: `Ctrl+N`   | 创建一个新线程      |
| `chatgpt.implementTodo`   | -                   | 要求 Codex 处理选中的 TODO 注释            |
| `chatgpt.newCodexPanel`   | -                   | 创建新的 Codex 面板                        |
| `chatgpt.openSidebar`     | -                   | 打开 Codex 侧边栏面板                      |
