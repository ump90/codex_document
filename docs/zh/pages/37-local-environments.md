### 本地环境

Source: [Local environments](https://developers.openai.com/codex/app/local-environments.md)

本地环境让你可以为工作树配置设置步骤，也可以为项目配置常用操作。

你可以通过 [Codex app 设置](codex://settings) 面板配置本地环境。你可以把生成的文件提交到项目的 Git 仓库，以便与他人共享。

Codex 会把此配置存储在项目根目录的 `.codex` 文件夹中。如果你的仓库包含多个项目，请打开包含共享 `.codex` 文件夹的项目目录。

#### 设置脚本

由于工作树运行在不同于本地任务的目录中，你的项目可能尚未完全设置好，可能缺少依赖项或未签入仓库的文件。设置脚本会在 Codex 于新线程开始时创建新工作树时自动运行。

使用此脚本运行配置环境所需的任何命令，例如安装依赖或运行构建流程。

例如，对于 TypeScript 项目，你可能希望使用设置脚本安装依赖并执行初始构建：

```bash
npm install
npm run build
```

如果你的设置与平台相关，请为 macOS、Windows 或 Linux 定义设置脚本，以覆盖默认脚本。

#### 操作

使用操作定义常见任务，例如启动应用的开发服务器或运行测试套件。这些操作会显示在 Codex app 顶栏中，便于快速访问。操作会在 app 的 [集成终端](https://developers.openai.com/codex/app/features#integrated-terminal) 中运行。

操作有助于避免重复输入常见命令，例如触发项目构建或启动开发服务器。对于一次性的快速调试，你可以直接使用集成终端。

例如，对于 Node.js 项目，你可能会创建一个包含以下脚本的 "Run" 操作：

```bash
npm start
```

如果操作的命令与平台相关，请为 macOS、Windows 和 Linux 定义平台特定脚本。

为了识别你的操作，请为每个操作选择一个关联图标。
