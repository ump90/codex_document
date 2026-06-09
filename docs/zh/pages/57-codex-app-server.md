### Codex App Server（应用服务器）

Source: [Codex App Server](https://developers.openai.com/codex/app-server.md)

Codex app-server 是 Codex 用来驱动富客户端的接口（例如 Codex VS Code 扩展）。当你希望在自己的产品中进行深度集成时，可以使用它来处理身份验证、对话历史、审批以及流式代理事件。app-server 的实现已在 Codex GitHub 仓库中开源（[openai/codex/codex-rs/app-server](https://github.com/openai/codex/tree/main/codex-rs/app-server)）。开源 Codex 组件的完整列表请参阅 [Open Source](76-open-source.md) 页面。

如果你要自动化作业或在 CI 中运行 Codex，请改用
Codex SDK。

#### 协议

与 [MCP](https://modelcontextprotocol.io/) 类似，`codex app-server` 支持使用 JSON-RPC 2.0 消息进行双向通信（在线路上传输时省略 `"jsonrpc":"2.0"` 头）。

支持的传输方式：

- `stdio`（`--listen stdio://`，默认）：以换行分隔的 JSON（JSONL）。
- `websocket`（`--listen ws://IP:PORT`，实验性且不受支持）：每个 WebSocket 文本帧包含一条
  JSON-RPC 消息。
- Unix socket（`--listen unix://` 或 `--listen unix://PATH`）：通过 Codex 默认 app-server 控制套接字或自定义 Unix
  套接字路径建立 WebSocket 连接，使用标准 HTTP Upgrade 握手。
- `off`（`--listen off`）：不暴露本地传输。

当你使用 `--listen ws://IP:PORT` 运行时，同一个监听器还会提供基本的
HTTP 健康探测：

- `GET /readyz` 在监听器接受新连接后返回 `200 OK`。
- `GET /healthz` 在请求不包含 `Origin` 头时返回 `200 OK`。
- 带有 `Origin` 头的请求会被拒绝并返回 `403 Forbidden`。

WebSocket 传输是实验性的且不受支持。`ws://127.0.0.1:PORT` 这类本地监听器适合 localhost 和 SSH 端口转发工作流。非回环 WebSocket 监听器在当前推出阶段默认允许未经身份验证的连接，因此在远程暴露前请配置 WebSocket 身份验证。

支持的 WebSocket 身份验证标志：

- `--ws-auth capability-token --ws-token-file /absolute/path`
- `--ws-auth capability-token --ws-token-sha256 HEX`
- `--ws-auth signed-bearer-token --ws-shared-secret-file /absolute/path`

对于签名 bearer token，你还可以设置 `--ws-issuer`、`--ws-audience` 和
`--ws-max-clock-skew-seconds`。客户端在 WebSocket 握手期间以
`Authorization: Bearer ` 的形式提供凭据，app-server 会在 JSON-RPC `initialize` 之前强制执行身份验证。

相比在命令行上传递原始 bearer token，优先使用 `--ws-token-file`。仅当客户端把原始高熵 token 保存在单独的本地密钥存储中时，才使用
`--ws-token-sha256`；该哈希只是验证器，客户端仍然需要原始 token。

在 WebSocket 模式下，app-server 使用有界队列。当请求入口已满时，服务器会拒绝新请求，并返回 JSON-RPC 错误代码 `-32001` 和消息
`"Server overloaded; retry later."`。客户端应使用指数递增延迟和抖动进行重试。

#### 消息架构

请求包含 `method`、`params` 和 `id`：

```json
{ "method": "thread/start", "id": 10, "params": { "model": "gpt-5.4" } }
```

响应会回显 `id`，并包含 `result` 或 `error`：

```json
{ "id": 10, "result": { "thread": { "id": "thr_123" } } }
```

```json
{ "id": 10, "error": { "code": 123, "message": "Something went wrong" } }
```

通知省略 `id`，只使用 `method` 和 `params`：

```json
{ "method": "turn/started", "params": { "turn": { "id": "turn_456" } } }
```

你可以从 CLI 生成 TypeScript 架构或 JSON Schema 包。每种输出都对应你运行的 Codex 版本，因此生成的产物会与该版本完全匹配：

```bash
codex app-server generate-ts --out ./schemas
codex app-server generate-json-schema --out ./schemas
```

#### 应用服务器快速开始

1. 使用 `codex app-server`（默认 stdio 传输）、`codex app-server --listen ws://127.0.0.1:4500`（TCP WebSocket）或
   `codex app-server --listen unix://`（默认 Unix socket）启动服务器。
2. 通过所选传输连接客户端，然后发送 `initialize`，随后发送 `initialized` 通知。
3. 启动一个线程和一个轮次，然后持续从活动传输流中读取通知。

示例（Node.js / TypeScript）：

```ts
const proc = spawn("codex", ["app-server"], {
  stdio: ["pipe", "pipe", "inherit"],
});
const rl = readline.createInterface({ input: proc.stdout });

const send = (message: unknown) => {
  proc.stdin.write(`${JSON.stringify(message)}\n`);
};

let threadId: string | null = null;

rl.on("line", (line) => {
  const msg = JSON.parse(line) as any;
  console.log("server:", msg);

  if (msg.id === 1 && msg.result?.thread?.id && !threadId) {
    threadId = msg.result.thread.id;
    send({
      method: "turn/start",
      id: 2,
      params: {
        threadId,
        input: [{ type: "text", text: "Summarize this repo." }],
      },
    });
  }
});

send({
  method: "initialize",
  id: 0,
  params: {
    clientInfo: {
      name: "my_product",
      title: "My Product",
      version: "0.1.0",
    },
  },
});
send({ method: "initialized", params: {} });
send({ method: "thread/start", id: 1, params: { model: "gpt-5.4" } });
```

#### 核心原语

- **Thread**：用户与 Codex 代理之间的一段对话。Thread 包含 turn。
- **Turn**：一次用户请求以及随后发生的代理工作。Turn 包含 item，并以流式方式提供增量更新。
- **Item**：输入或输出的一个单元（用户消息、代理消息、命令运行、文件变更、工具调用等）。

使用 thread API 创建、列出或归档对话。使用 turn API 驱动对话，并通过 turn 通知流式传输进度。

#### 生命周期概览

- **每个连接初始化一次**：打开传输连接后，立即发送带有客户端元数据的 `initialize` 请求，然后发出 `initialized`。服务器会拒绝该连接上在此握手之前的任何请求。
- **启动（或恢复）线程**：调用 `thread/start` 开始新对话，调用 `thread/resume` 继续现有对话，或调用 `thread/fork` 将历史分支到新的 thread id。
- **开始轮次**：调用 `turn/start`，并传入目标 `threadId` 和用户输入。可选字段可以覆盖模型、personality、`cwd`、沙箱策略等。
- **引导活动轮次**：调用 `turn/steer`，在不创建新 turn 的情况下向当前正在进行的 turn 追加用户输入。
- **流式事件**：在 `turn/start` 之后，持续读取 stdout 上的通知：`thread/archived`、`thread/unarchived`、`item/started`、`item/completed`、`item/agentMessage/delta`、工具进度以及其它更新。
- **结束轮次**：当模型完成时，或在 `turn/interrupt` 取消之后，服务器会发出带有最终状态的 `turn/completed`。

#### 初始化

客户端必须在每个传输连接上发送一次 `initialize` 请求，然后再调用该连接上的任何其它方法，并随后用 `initialized` 通知确认。在初始化之前发送的请求会收到 `Not initialized` 错误，而同一连接上重复的 `initialize` 调用会返回 `Already initialized`。

服务器会返回它将呈现给上游服务的 user agent 字符串，以及描述运行时目标的 `platformFamily` 和 `platformOs` 值。设置 `clientInfo` 以标识你的集成。

`initialize.params.capabilities` 还支持通过 `optOutNotificationMethods` 为每个连接选择退出通知，这是一个精确方法名列表，用于抑制该连接上的通知。匹配是精确的（没有通配符/前缀）。未知方法名会被接受并忽略。

**重要**：使用 `clientInfo.name` 为 OpenAI Compliance Logs Platform 标识你的客户端。如果你正在开发面向企业使用的新 Codex 集成，请联系 OpenAI，将其加入已知客户端列表。更多背景请参阅 [Codex logs reference](https://chatgpt.com/admin/api-reference#tag/Logs:-Codex)。

示例（来自 Codex VS Code 扩展）：

```json
{
  "method": "initialize",
  "id": 0,
  "params": {
    "clientInfo": {
      "name": "codex_vscode",
      "title": "Codex VS Code Extension",
      "version": "0.1.0"
    }
  }
}
```

带有通知选择退出的示例：

```json
{
  "method": "initialize",
  "id": 1,
  "params": {
    "clientInfo": {
      "name": "my_client",
      "title": "My Client",
      "version": "0.1.0"
    },
    "capabilities": {
      "experimentalApi": true,
      "optOutNotificationMethods": ["thread/started", "item/agentMessage/delta"]
    }
  }
}
```

#### 选择启用实验性 API

一些 app-server 方法和字段会被有意置于 `experimentalApi` 能力开关之后。

- 省略 `capabilities`（或将 `experimentalApi` 设置为 `false`）即可停留在稳定 API 范围内，服务器会拒绝实验性方法/字段。
- 将 `capabilities.experimentalApi` 设置为 `true` 可启用实验性方法和字段。

```json
{
  "method": "initialize",
  "id": 1,
  "params": {
    "clientInfo": {
      "name": "my_client",
      "title": "My Client",
      "version": "0.1.0"
    },
    "capabilities": {
      "experimentalApi": true
    }
  }
}
```

如果客户端在未选择加入的情况下发送实验性方法或字段，app-server 会以下列错误拒绝：

` requires experimentalApi capability`
