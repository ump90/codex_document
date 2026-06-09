### Codex SDK

Source: [Codex SDK](https://developers.openai.com/codex/sdk.md)

如果你通过 Codex CLI、IDE 扩展或 Codex Web 使用 Codex，也可以用编程方式控制它。

当你需要执行以下操作时，请使用 SDK：

- 将 Codex 作为 CI/CD 流水线的一部分进行控制
- 创建你自己的代理，让它可以与 Codex 协作执行复杂工程任务
- 将 Codex 构建到你自己的内部工具和工作流中
- 在你自己的应用内集成 Codex

#### TypeScript 库

TypeScript 库提供了一种从应用内部控制 Codex 的方式，比非交互模式更全面、更灵活。

请在服务器端使用该库；它要求 Node.js 18 或更高版本。

#### 安装

首先，使用 `npm` 安装 Codex SDK：

```bash
npm install @openai/codex-sdk
```

#### 用法

使用 Codex 启动一个线程，并用你的提示运行它。

```ts
const codex = new Codex();
const thread = codex.startThread();
const result = await thread.run(
  "Make a plan to diagnose and fix the CI failures"
);

console.log(result);
```

再次调用 `run()` 可在同一个线程上继续，或通过提供 thread ID 恢复过去的线程。

```ts
// running the same thread
const result = await thread.run("Implement the plan");

console.log(result);

// resuming past thread

const threadId = "";
const thread2 = codex.resumeThread(threadId);
const result2 = await thread2.run("Pick up where you left off");

console.log(result2);
```

更多详情请查看 [TypeScript repo](https://github.com/openai/codex/tree/main/sdk/typescript)。

#### Python 库

Python SDK 通过 JSON-RPC 控制本地 Codex app-server。它要求 Python 3.10 或更高版本。已发布的 SDK 构建包含固定版本的 Codex CLI 运行时依赖。

#### 安装

运行以下命令安装 SDK：

```bash
pip install openai-codex
```

已发布的 SDK 构建会自动使用其固定的运行时。只有当你明确想针对特定本地 app-server 二进制文件运行时，才传入 `AppServerConfig(codex_bin=...)`。

#### 用法

启动 Codex、创建线程，并运行提示：

```python
from openai_codex import Codex, Sandbox

with Codex() as codex:
    thread = codex.thread_start(
        model="gpt-5.4",
        sandbox=Sandbox.workspace_write,
    )
    result = thread.run("Make a plan to diagnose and fix the CI failures")
    print(result.final_response)
```

当你的应用已经是异步的，请使用 `AsyncCodex`：

```python
import asyncio

from openai_codex import AsyncCodex

async def main() -> None:
    async with AsyncCodex() as codex:
        thread = await codex.thread_start(model="gpt-5.4")
        result = await thread.run("Implement the plan")
        print(result.final_response)

asyncio.run(main())
```

#### 沙箱预设

创建线程或为后续轮次更改其文件系统访问权限时，使用相同的 `Sandbox` 预设：

```python
from openai_codex import Codex, Sandbox

with Codex() as codex:
    thread = codex.thread_start(sandbox=Sandbox.workspace_write)
    thread.run("Make the requested change.")
    review = thread.run("Review the diff only.", sandbox=Sandbox.read_only)
```

可用预设：

- `Sandbox.read_only`：读取文件但不允许写入。
- `Sandbox.workspace_write`：读取文件，并在工作区和已配置的可写根目录内写入。
- `Sandbox.full_access`：在没有文件系统访问限制的情况下运行。

当你省略 `sandbox=` 时，app-server 会使用其配置的默认值。传给 `run(...)` 或 `turn(...)` 的沙箱会应用于该轮次以及该线程后续的轮次。

更多详情请查看 [Python repo](https://github.com/openai/codex/tree/main/sdk/python)。
