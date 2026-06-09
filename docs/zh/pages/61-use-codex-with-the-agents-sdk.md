### 将 Codex 与 Agents SDK 配合使用

Source: [Use Codex with the Agents SDK](https://developers.openai.com/codex/guides/agents-sdk.md)

你可以将 Codex 作为 MCP 服务器运行，并从其它 MCP 客户端连接它（例如使用 [OpenAI Agents SDK MCP 集成](https://developers.openai.com/api/docs/guides/agents/integrations-observability#mcp) 构建的代理）。

要将 Codex 作为 MCP 服务器启动，可以使用以下命令：

```bash
codex mcp-server
```

你可以使用 [Model Context Protocol Inspector](https://modelcontextprotocol.io/legacy/tools/inspector) 启动 Codex MCP 服务器：

```bash
npx @modelcontextprotocol/inspector codex mcp-server
```

发送 `tools/list` 请求可看到两个工具：

**`codex`**：运行 Codex 会话。接受与 Codex `Config` 结构体匹配的配置参数。`codex` 工具接受以下属性：

| Property                | Type      | Description                                                                                                |
| ----------------------- | --------- | ---------------------------------------------------------------------------------------------------------- |
| **`prompt`** (required) | `string`  | 用于启动 Codex 对话的初始用户提示。                                                   |
| `approval-policy`       | `string`  | 模型生成的 shell 命令的审批策略：`untrusted`、`on-request` 和 `never`。         |
| `base-instructions`     | `string`  | 用来替代默认指令的一组指令。                                                |
| `config`                | `object`  | 覆盖 `$CODEX_HOME/config.toml` 中内容的单项配置设置。                       |
| `cwd`                   | `string`  | 会话的工作目录。如果是相对路径，则相对于服务器进程的当前目录解析。   |
| `include-plan-tool`     | `boolean` | 是否在对话中包含计划工具。                                                      |
| `model`                 | `string`  | 可选的模型名称覆盖值（例如 `o3`、`o4-mini`）。                                       |
| `profile`               | `string`  | 配置 profile 名称；Codex 会加载 `$CODEX_HOME/profile-name.config.toml` 来指定默认选项。 |
| `sandbox`               | `string`  | 沙箱模式：`read-only`、`workspace-write` 或 `danger-full-access`。                                     |

**`codex-reply`**：通过提供 thread ID 和提示来继续 Codex 会话。`codex-reply` 工具接受以下属性：

| Property                      | Type   | Description                                               |
| ----------------------------- | ------ | --------------------------------------------------------- |
| **`prompt`** (required)       | string | 用于继续 Codex 对话的下一条用户提示。  |
| **`threadId`** (required)     | string | 要继续的线程 ID。                         |
| `conversationId` (deprecated) | string | `threadId` 的已弃用别名（为兼容性保留）。 |

使用 `tools/call` 响应中 `structuredContent.threadId` 的 `threadId`。审批提示（exec/patch）也会在其 `params` payload 中包含 `threadId`。

响应 payload 示例：

```json
{
  "structuredContent": {
    "threadId": "019bbb20-bff6-7130-83aa-bf45ab33250e",
    "content": "`ls -lah` (or `ls -alh`) — long listing, includes dotfiles, human-readable sizes."
  },
  "content": [
    {
      "type": "text",
      "text": "`ls -lah` (or `ls -alh`) — long listing, includes dotfiles, human-readable sizes."
    }
  ]
}
```

注意，现代 MCP 客户端通常只会报告 `"structuredContent"` 作为工具调用的结果（如果存在），不过 Codex MCP 服务器也会返回 `"content"`，以便较旧的 MCP 客户端使用。

Codex CLI 远不止可以运行临时任务。通过将 CLI 作为 [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) 服务器暴露，并用 OpenAI Agents SDK 进行编排，你可以创建确定性、可审查的工作流，其规模可从单个代理扩展到完整的软件交付流水线。

本指南介绍 [OpenAI Cookbook](https://github.com/openai/openai-cookbook/blob/main/examples/codex/codex_mcp_agents_sdk/building_consistent_workflows_codex_cli_agents_sdk.ipynb) 中展示的同一工作流。你将：

- 将 Codex CLI 作为长期运行的 MCP 服务器启动，
- 构建一个聚焦的单代理工作流，用于生成可玩的浏览器游戏，并且
- 编排一个包含交接、护栏和完整跟踪的多代理团队，之后可供审查。

开始之前，请确保你具备：

- 本地已安装 [Codex CLI](45-codex-cli.md)，因此 `codex` 命令可用。
- Python 3.10+ 和 `pip`。
- 如果你想运行上面的 MCP Inspector 示例，需要 Node.js 18+。
- 本地已保存 OpenAI API key。你可以在 [OpenAI dashboard](https://platform.openai.com/account/api-keys) 中创建或管理 key。

为本指南创建工作目录，并将你的 API key 添加到 `.env` 文件：

```bash
mkdir codex-workflows
cd codex-workflows
printf "OPENAI_API_KEY=sk-..." > .env
```

#### 安装依赖

Agents SDK 处理跨 Codex、hand-offs 和 traces 的编排。安装最新 SDK 包：

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade openai openai-agents python-dotenv
```

激活虚拟环境可使 SDK 依赖与
系统其余部分隔离。

#### 将 Codex CLI 初始化为 MCP 服务器

首先将 Codex CLI 转换为 Agents SDK 可以调用的 MCP 服务器。该服务器暴露两个工具（`codex()` 用于开始对话，`codex-reply()` 用于继续对话），并让 Codex 在多个代理轮次之间保持运行。

创建名为 `codex_mcp.py` 的文件，并添加以下内容：

```python
import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStdio

async def main() -> None:
    async with MCPServerStdio(
        name="Codex CLI",
        params={
            "command": "codex",
            "args": ["mcp-server"],
        },
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:
        print("Codex MCP server started.")
        # More logic coming in the next sections.
        return

if __name__ == "__main__":
    asyncio.run(main())
```

运行一次脚本，确认 Codex 成功启动：

```bash
python codex_mcp.py
```

脚本会在打印 `Codex MCP server started.` 后退出。在下一节中，你会在更丰富的工作流内复用同一个 MCP 服务器。

#### 构建单代理工作流

让我们从一个有范围的示例开始，使用 Codex MCP 交付一个小游戏。该工作流依赖两个代理：

1. **Game Designer**：为游戏编写 brief。
2. **Game Developer**：通过调用 Codex MCP 实现游戏。

用以下代码更新 `codex_mcp.py`。它保留上面的 MCP 服务器设置，并添加两个代理。

```python
import asyncio
import os

from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_api
from agents.mcp import MCPServerStdio

load_dotenv(override=True)
set_default_openai_api(os.getenv("OPENAI_API_KEY"))

async def main() -> None:
    async with MCPServerStdio(
        name="Codex CLI",
        params={
            "command": "codex",
            "args": ["mcp-server"],
        },
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:
        developer_agent = Agent(
            name="Game Developer",
            instructions=(
                "You are an expert in building simple games using basic html + css + javascript with no dependencies. "
                "Save your work in a file called index.html in the current directory. "
                "Always call codex with \"approval-policy\": \"never\" and \"sandbox\": \"workspace-write\"."
            ),
            mcp_servers=[codex_mcp_server],
        )

        designer_agent = Agent(
            name="Game Designer",
            instructions=(
                "You are an indie game connoisseur. Come up with an idea for a single page html + css + javascript game that a developer could build in about 50 lines of code. "
                "Format your request as a 3 sentence design brief for a game developer and call the Game Developer coder with your idea."
            ),
            model="gpt-5",
            handoffs=[developer_agent],
        )

        await Runner.run(designer_agent, "Implement a fun new game!")

if __name__ == "__main__":
    asyncio.run(main())
```

执行脚本：

```bash
python codex_mcp.py
```

Codex 会读取设计者的简报，创建 `index.html` 文件，并将完整游戏写入磁盘。在浏览器中打开生成的文件即可游玩。每次运行都会产生不同的设计，并带有独特的玩法变化和打磨细节。

## 平台、企业和注意事项

<a id="platform-enterprise-and-caveats"></a>

影响部署选择的 Windows、企业控制、OSS 说明，以及产品或策略注意事项。
