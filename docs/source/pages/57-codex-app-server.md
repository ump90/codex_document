### Codex App Server

Source: [Codex App Server](/codex/app-server.md)

Codex app-server is the interface Codex uses to power rich clients (for example, the Codex VS Code extension). Use it when you want a deep integration inside your own product: authentication, conversation history, approvals, and streamed agent events. The app-server implementation is open source in the Codex GitHub repository ([openai/codex/codex-rs/app-server](https://github.com/openai/codex/tree/main/codex-rs/app-server)). See the [Open Source](/codex/open-source) page for the full list of open-source Codex components.

If you are automating jobs or running Codex in CI, use the
Codex SDK instead.

#### Protocol

Like [MCP](https://modelcontextprotocol.io/), `codex app-server` supports bidirectional communication using JSON-RPC 2.0 messages (with the `"jsonrpc":"2.0"` header omitted on the wire).

Supported transports:

- `stdio` (`--listen stdio://`, default): newline-delimited JSON (JSONL).
- `websocket` (`--listen ws://IP:PORT`, experimental and unsupported): one
  JSON-RPC message per WebSocket text frame.
- Unix socket (`--listen unix://` or `--listen unix://PATH`): WebSocket
  connections over Codex's default app-server control socket or a custom Unix
  socket path, using the standard HTTP Upgrade handshake.
- `off` (`--listen off`): don't expose a local transport.

When you run with `--listen ws://IP:PORT`, the same listener also serves basic
HTTP health probes:

- `GET /readyz` returns `200 OK` once the listener accepts new connections.
- `GET /healthz` returns `200 OK` when the request doesn't include an `Origin`
  header.
- Requests with an `Origin` header are rejected with `403 Forbidden`.

WebSocket transport is experimental and unsupported. Local listeners such as
`ws://127.0.0.1:PORT` are appropriate for localhost and SSH port-forwarding
workflows. Non-loopback WebSocket listeners currently allow unauthenticated
connections by default during rollout, so configure WebSocket auth before
exposing one remotely.

Supported WebSocket auth flags:

- `--ws-auth capability-token --ws-token-file /absolute/path`
- `--ws-auth capability-token --ws-token-sha256 HEX`
- `--ws-auth signed-bearer-token --ws-shared-secret-file /absolute/path`

For signed bearer tokens, you can also set `--ws-issuer`, `--ws-audience`, and
`--ws-max-clock-skew-seconds`. Clients present the credential as
`Authorization: Bearer ` during the WebSocket handshake, and app-server
enforces auth before JSON-RPC `initialize`.

Prefer `--ws-token-file` over passing raw bearer tokens on the command line. Use
`--ws-token-sha256` only when the client keeps the raw high-entropy token in a
separate local secret store; the hash is only a verifier, and clients still need
the original token.

In WebSocket mode, app-server uses bounded queues. When request ingress is full,
the server rejects new requests with JSON-RPC error code `-32001` and message
`"Server overloaded; retry later."` Clients should retry with an exponentially
increasing delay and jitter.

#### Message schema

Requests include `method`, `params`, and `id`:

```json
{ "method": "thread/start", "id": 10, "params": { "model": "gpt-5.4" } }
```

Responses echo the `id` with either `result` or `error`:

```json
{ "id": 10, "result": { "thread": { "id": "thr_123" } } }
```

```json
{ "id": 10, "error": { "code": 123, "message": "Something went wrong" } }
```

Notifications omit `id` and use only `method` and `params`:

```json
{ "method": "turn/started", "params": { "turn": { "id": "turn_456" } } }
```

You can generate a TypeScript schema or a JSON Schema bundle from the CLI. Each output is specific to the Codex version you ran, so the generated artifacts match that version exactly:

```bash
codex app-server generate-ts --out ./schemas
codex app-server generate-json-schema --out ./schemas
```

#### App-server quickstart

1. Start the server with `codex app-server` (default stdio transport),
   `codex app-server --listen ws://127.0.0.1:4500` (TCP WebSocket), or
   `codex app-server --listen unix://` (default Unix socket).
2. Connect a client over the selected transport, then send `initialize` followed by the `initialized` notification.
3. Start a thread and a turn, then keep reading notifications from the active transport stream.

Example (Node.js / TypeScript):

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

#### Core primitives

- **Thread**: A conversation between a user and the Codex agent. Threads contain turns.
- **Turn**: A single user request and the agent work that follows. Turns contain items and stream incremental updates.
- **Item**: A unit of input or output (user message, agent message, command runs, file change, tool call, and more).

Use the thread APIs to create, list, or archive conversations. Drive a conversation with turn APIs and stream progress via turn notifications.

#### Lifecycle overview

- **Initialize once per connection**: Immediately after opening a transport connection, send an `initialize` request with your client metadata, then emit `initialized`. The server rejects any request on that connection before this handshake.
- **Start (or resume) a thread**: Call `thread/start` for a new conversation, `thread/resume` to continue an existing one, or `thread/fork` to branch history into a new thread id.
- **Begin a turn**: Call `turn/start` with the target `threadId` and user input. Optional fields override model, personality, `cwd`, sandbox policy, and more.
- **Steer an active turn**: Call `turn/steer` to append user input to the currently in-flight turn without creating a new turn.
- **Stream events**: After `turn/start`, keep reading notifications on stdout: `thread/archived`, `thread/unarchived`, `item/started`, `item/completed`, `item/agentMessage/delta`, tool progress, and other updates.
- **Finish the turn**: The server emits `turn/completed` with final status when the model finishes or after a `turn/interrupt` cancellation.

#### Initialization

Clients must send a single `initialize` request per transport connection before invoking any other method on that connection, then acknowledge with an `initialized` notification. Requests sent before initialization receive a `Not initialized` error, and repeated `initialize` calls on the same connection return `Already initialized`.

The server returns the user agent string it will present to upstream services plus `platformFamily` and `platformOs` values that describe the runtime target. Set `clientInfo` to identify your integration.

`initialize.params.capabilities` also supports per-connection notification opt-out via `optOutNotificationMethods`, which is a list of exact method names to suppress for that connection. Matching is exact (no wildcards/prefixes). Unknown method names are accepted and ignored.

**Important**: Use `clientInfo.name` to identify your client for the OpenAI Compliance Logs Platform. If you are developing a new Codex integration intended for enterprise use, please contact OpenAI to get it added to a known clients list. For more context, see the [Codex logs reference](https://chatgpt.com/admin/api-reference#tag/Logs:-Codex).

Example (from the Codex VS Code extension):

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

Example with notification opt-out:

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

#### Experimental API opt-in

Some app-server methods and fields are intentionally gated behind `experimentalApi` capability.

- Omit `capabilities` (or set `experimentalApi` to `false`) to stay on the stable API surface, and the server rejects experimental methods/fields.
- Set `capabilities.experimentalApi` to `true` to enable experimental methods and fields.

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

If a client sends an experimental method or field without opting in, app-server rejects it with:

` requires experimentalApi capability`

