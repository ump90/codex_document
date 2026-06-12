### 云环境

Source: [Cloud environments](https://developers.openai.com/codex/cloud/environments.md)

使用环境控制 Codex 在云任务期间安装和运行什么。例如，你可以添加依赖、安装 linter 和 formatter 等工具，并设置环境变量。

在 [Codex 设置](https://chatgpt.com/codex/settings/environments) 中配置环境。

#### Codex 云任务如何运行 { #how-codex-cloud-tasks-run }

提交任务时会发生以下过程：

1. Codex 创建容器，并在所选分支或 commit SHA 上检出你的仓库。
2. Codex 运行你的设置脚本（setup script），并在恢复缓存容器时运行可选的维护脚本（maintenance script）。
3. Codex 应用你的互联网访问设置。设置脚本会带互联网访问权限运行。智能体互联网访问默认关闭，但如有需要，你可以启用受限或不受限访问。请参阅 [智能体互联网访问](23-agent-internet-access.md)。
4. 智能体循环运行终端命令。它编辑代码、运行检查，并尝试验证其工作。如果你的仓库包含 `AGENTS.md`，智能体会用它查找项目专属的 lint 和测试命令。
5. 智能体完成后，会显示其回答以及它更改过的文件差异。你可以打开 PR 或提出后续问题。

#### 默认 universal 镜像 { #default-universal-image }

Codex 智能体在名为 `universal` 的默认容器镜像中运行，其中预装了常见语言、软件包和工具。

在环境设置中，选择 **Set package versions** 来固定 Python、Node.js 和其它运行时的版本。

有关已安装内容的细节，请参阅 [openai/codex-universal](https://github.com/openai/codex-universal)，其中提供参考 Dockerfile，以及可以在本地拉取和测试的镜像。

虽然 `codex-universal` 为了速度和便利预装了语言，你也可以使用[设置脚本](#manual-setup)将额外软件包安装到容器。

#### 环境变量和密钥 { #environment-variables-and-secrets }

**环境变量（Environment variables）**会在任务的整个持续时间内设置（包括设置脚本和智能体阶段）。

**密钥（Secrets）**类似于环境变量，但有以下区别：

- 它们以额外一层加密存储，并且只在任务执行时解密。
- 它们只对设置脚本可用。出于安全原因，密钥会在智能体阶段开始前移除。

#### 自动设置 { #automatic-setup }

对于使用常见包管理器（`npm`、`yarn`、`pnpm`、`pip`、`pipenv` 和 `poetry`）的项目，Codex 可以自动安装依赖和工具。

#### 手动设置 { #manual-setup }

如果你的开发设置更复杂，也可以提供自定义设置脚本。例如：

```bash
# Install type checker
pip install pyright

# Install dependencies
poetry install --with test
pnpm install
```

设置脚本会在与智能体分离的 Bash 会话中运行，因此 `export` 等命令不会持久化到智能体阶段。要持久化环境变量，请将它们添加到 `~/.bashrc`，或在环境设置中配置它们。

#### 容器缓存 { #container-caching }

Codex 会缓存容器状态最多 12 小时，以加速新任务和后续任务。

当环境被缓存时：

- Codex 克隆仓库并检出默认分支。
- Codex 运行设置脚本，并缓存生成的容器状态。

当缓存容器恢复时：

- Codex 检出为任务指定的分支。
- Codex 运行维护脚本（可选）。当设置脚本在较旧提交上运行且依赖需要更新时，这很有用。

如果你更改设置脚本、维护脚本、环境变量或密钥，Codex 会自动使缓存失效。如果你的仓库发生变化，导致缓存状态不兼容，请在环境页面上选择 **Reset cache**。

对于 Business 和 Enterprise 用户，缓存会在所有有权访问该环境的用户之间共享。使缓存失效会影响你工作区中该环境的所有用户。

#### 互联网访问和网络代理 { #internet-access-and-network-proxy }

互联网访问在设置脚本阶段可用，用于安装依赖。在智能体阶段，互联网访问默认关闭，但你可以配置受限或不受限访问。请参阅 [智能体互联网访问](23-agent-internet-access.md)。

出于安全和防止滥用目的，环境在 HTTP/HTTPS 网络代理后运行。所有出站互联网流量都会通过此代理。
