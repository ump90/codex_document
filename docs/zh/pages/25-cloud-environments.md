### 云环境

Source: [Cloud environments](https://developers.openai.com/codex/cloud/environments.md)

使用环境控制 Codex 在云任务期间安装和运行什么。例如，你可以添加依赖、安装 linter 和 formatter 等工具，并设置环境变量。

在 [Codex 设置](https://chatgpt.com/codex/settings/environments) 中配置环境。

#### Codex 云任务如何运行

提交任务时会发生以下过程：

1. Codex 创建容器，并在所选分支或 commit SHA 上 checkout 你的仓库。
2. Codex 运行你的 setup script，并在恢复缓存容器时运行可选的 maintenance script。
3. Codex 应用你的互联网访问设置。Setup scripts 会带互联网访问权限运行。智能体互联网访问默认关闭，但如有需要，你可以启用受限或不受限访问。请参阅 [智能体互联网访问](23-agent-internet-access.md)。
4. 智能体循环运行终端命令。它编辑代码、运行检查，并尝试验证其工作。如果你的仓库包含 `AGENTS.md`，智能体会用它查找项目专属的 lint 和 test 命令。
5. 智能体完成后，会显示其回答以及它更改过的任何文件的 diff。你可以打开 PR 或提出后续问题。

#### 默认 universal 镜像

Codex 智能体在名为 `universal` 的默认容器镜像中运行，其中预装了常见语言、软件包和工具。

在环境设置中，选择 **Set package versions** 来固定 Python、Node.js 和其它运行时的版本。

有关已安装内容的细节，请参阅 [openai/codex-universal](https://github.com/openai/codex-universal)，其中提供参考 Dockerfile，以及可以在本地 pull 和测试的镜像。

虽然 `codex-universal` 为了速度和便利预装了语言，你也可以使用 [setup scripts](#manual-setup) 将额外软件包安装到容器。

#### 环境变量和密钥

**Environment variables** 会在任务的整个持续时间内设置（包括 setup scripts 和智能体阶段）。

**Secrets** 类似于 environment variables，但有以下区别：

- 它们以额外一层加密存储，并且只在 task execution 时解密。
- 它们只对 setup scripts 可用。出于安全原因，secrets 会在智能体阶段开始前移除。

#### 自动设置

对于使用常见包管理器（`npm`、`yarn`、`pnpm`、`pip`、`pipenv` 和 `poetry`）的项目，Codex 可以自动安装依赖和工具。

#### 手动设置

如果你的开发设置更复杂，也可以提供自定义 setup script。例如：

```bash
# Install type checker
pip install pyright

# Install dependencies
poetry install --with test
pnpm install
```

Setup scripts 在与智能体分离的 Bash 会话中运行，因此 `export` 等命令不会持久化到智能体阶段。要持久化环境变量，请将它们添加到 `~/.bashrc`，或在环境设置中配置它们。

#### 容器缓存

Codex 会缓存容器状态最多 12 小时，以加速新任务和后续任务。

当环境被缓存时：

- Codex 克隆仓库并 checkout 默认分支。
- Codex 运行 setup script，并缓存生成的容器状态。

当缓存容器恢复时：

- Codex checkout 为任务指定的分支。
- Codex 运行 maintenance script（可选）。当 setup script 在较旧 commit 上运行且依赖需要更新时，这很有用。

如果你更改 setup script、maintenance script、环境变量或 secrets，Codex 会自动使缓存失效。如果你的仓库发生变化，导致缓存状态不兼容，请在环境页面上选择 **Reset cache**。

对于 Business 和 Enterprise 用户，缓存会在所有有权访问该环境的用户之间共享。使缓存失效会影响你工作区中该环境的所有用户。

#### 互联网访问和网络代理

互联网访问在 setup script 阶段可用，用于安装依赖。在智能体阶段，互联网访问默认关闭，但你可以配置受限或不受限访问。请参阅 [智能体互联网访问](23-agent-internet-access.md)。

出于安全和防止滥用目的，环境在 HTTP/HTTPS 网络代理后运行。所有出站互联网流量都会通过此代理。
