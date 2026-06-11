### 快速开始

Source: [Quickstart](https://developers.openai.com/codex/quickstart.md)

每个 ChatGPT 计划都包含 Codex。

你也可以使用 OpenAI API key 登录，通过 API 点数使用 Codex。

#### 设置

##### App

Codex app 可在 macOS 和 Windows 上使用。大多数 Codex app 功能都支持这两个平台。平台特定例外会在相关文档中说明。

1. 下载并安装 Codex app。

   下载 macOS 或 Windows 版 Codex app。如果你使用的是 Intel Mac，请选择 Intel build。Linux 用户可以登记以便在 app 可用时收到通知。

2. 打开 Codex 并登录。

   下载并安装 Codex app 后，打开它并使用 ChatGPT 账户或 OpenAI API key 登录。如果使用 OpenAI API key 登录，某些功能可能不可用。

3. 选择项目。

   选择你希望 Codex 处理的项目文件夹。如果你以前使用过 Codex app、CLI 或 IDE extension，会看到之前处理过的项目。

4. 发送第一条消息。

   选择项目后，确认已选择 **Local**，让 Codex 在你的机器上工作，然后发送第一条消息。你可以询问 Codex 任何与项目或你的电脑相关的问题。

   适合第一次尝试的提示包括：

   - `Tell me about this project`
   - `Build a classic Snake game in this repo.`
   - `Find and fix bugs in my codebase with minimal, high-confidence changes.`

   如果需要更多灵感，请浏览 [Codex 使用场景](97-use-cases.md)。如果你刚开始使用 Codex，请阅读 [最佳实践指南](05-best-practices.md)。

##### IDE extension

为你的 IDE 安装 Codex extension。

1. 安装 Codex extension。

   为你的编辑器下载：

   - [Download for Visual Studio Code](vscode:extension/openai.chatgpt)
   - [Download for Cursor](cursor:extension/openai.chatgpt)
   - [Download for Windsurf](windsurf:extension/openai.chatgpt)
   - [Download for Visual Studio Code Insiders](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt)

2. 打开 Codex 面板。

   安装后，Codex extension 会和其他扩展一起出现在侧边栏中。它可能隐藏在折叠区域里。你也可以按自己的偏好把 Codex 面板移动到编辑器右侧。

3. 登录并启动第一个任务。

   使用 ChatGPT 账户或 API key 登录即可开始。Codex 默认以 Agent mode 启动，这让它可以读取文件、运行命令，并在你的项目目录中写入变更。

4. 使用 Git 检查点。

   Codex 可以修改你的代码库，因此建议在每个任务前后创建 Git 检查点，方便在需要时回退变更。如果你刚开始使用 Codex，请阅读 [最佳实践指南](05-best-practices.md)。

   更多信息请参阅 [Codex IDE extension](46-codex-ide-extension.md)。

##### CLI

Codex CLI 支持 macOS、Windows 和 Linux。

1. 安装 Codex CLI。

   在 macOS 或 Linux 上，使用独立安装器：

   ```bash
   curl -fsSL https://chatgpt.com/codex/install.sh | sh
   ```

   在 Windows 上，运行：

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
   ```

   对于无人值守安装，请在运行已下载安装器的 shell 中设置 `CODEX_NON_INTERACTIVE=1`。详情请参阅 [环境变量](62-environment-variables.md)。

   ```bash
   curl -fsSL https://chatgpt.com/codex/install.sh | CODEX_NON_INTERACTIVE=1 sh
   ```

   ```powershell
   $env:CODEX_NON_INTERACTIVE=1; irm https://chatgpt.com/codex/install.ps1 | iex
   ```

   你也可以用 npm 或 Homebrew 安装 Codex CLI：

   ```bash
   npm install -g @openai/codex
   ```

   ```bash
   brew install --cask codex
   ```

2. 运行 `codex` 并登录。

   在终端中运行 `codex` 开始使用。系统会提示你使用 ChatGPT 账户或 API key 登录。

3. 让 Codex 在当前目录中工作。

   完成身份验证后，你可以要求 Codex 在当前目录中执行任务。

4. 使用 Git 检查点。

   Codex 可以修改你的代码库，因此建议在每个任务前后创建 Git 检查点，方便在需要时回退变更。

   更多信息请参阅 [Codex CLI](45-codex-cli.md)。

##### Cloud

在 [chatgpt.com/codex](https://chatgpt.com/codex) 使用云端 Codex。

1. 在浏览器中打开 Codex。

   访问 [chatgpt.com/codex](https://chatgpt.com/codex)。你也可以在 GitHub pull request 评论中标记 `@codex` 来委派任务给 Codex（需要登录 ChatGPT）。

2. 设置环境。

   启动第一个任务前，请为 Codex 设置环境。打开 [chatgpt.com/codex](https://chatgpt.com/codex/settings/environments) 的环境设置，并按步骤连接 GitHub 仓库。

3. 启动任务并监控进度。

   环境准备好后，从 [Codex 界面](https://chatgpt.com/codex) 启动编码任务。你可以查看日志实时监控进度，也可以让任务在后台运行。

4. 审查变更并创建 pull request。

   任务完成后，在 diff view 中审查建议的变更。你可以继续迭代结果，或直接在 GitHub 仓库中创建 pull request。

   Codex 也会提供变更预览。你可以直接接受 PR，也可以在本地 checkout 分支进行测试：

   ```bash
   git fetch
   git checkout <branch-name>
   ```

   更多信息请参阅 [Codex cloud](47-codex-web.md)。

#### 后续步骤

- [进一步了解 Codex app](44-codex-app.md)
- [迁移到 Codex](75-migrate-to-codex.md)
