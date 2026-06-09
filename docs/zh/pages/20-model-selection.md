### 模型选择

Source: [Codex Models](https://developers.openai.com/codex/models.md)

#### 推荐模型

对于 Codex 中的大多数任务，请从 `gpt-5.5` 开始。它最适合复杂编码、computer use、知识工作和研究工作流。使用 ChatGPT 或 API key 身份验证登录时，GPT-5.5 当前可在 Codex 中使用。当你希望为较轻量的编码任务或 subagent 使用更快、成本更低的选项时，请使用 `gpt-5.4-mini`。`gpt-5.3-codex-spark` 模型面向 ChatGPT Pro 订阅者以 research preview 形式提供，并针对近乎即时的实时编码迭代进行了优化。

#### 其它模型

使用 ChatGPT 登录时，Codex 与上面列出的推荐模型配合效果最佳。

你也可以将 Codex 指向任何支持 [Chat Completions](https://platform.openai.com/docs/api-reference/chat) 或 [Responses APIs](https://platform.openai.com/docs/api-reference/responses) 的模型和提供商，以适配你的具体用例。

对 Chat Completions API 的支持已弃用，并将在 Codex 的未来版本中移除。

#### 已弃用的 Codex 模型

当你使用 ChatGPT 登录时，`gpt-5.2` 和 `gpt-5.3-codex` 模型已在 Codex 中弃用。如果你的脚本、配置文件或 `codex exec --model` 命令仍引用已弃用模型，请将其更新为上面列出的最新模型。

某些对 ChatGPT 登录已弃用的模型可能仍可在 API 中使用。如果你的工作流依赖其中某个模型，请使用 API key 身份验证，并查看 [API 模型页面](https://developers.openai.com/api/docs/models) 了解当前可用性。

#### 配置模型

#### 配置默认本地模型

Codex CLI 和 IDE extension 使用相同的 `config.toml` [配置文件](19-config-basics.md)。要指定模型，请向配置文件添加 `model` 条目。如果你未指定模型，Codex app、CLI 或 IDE Extension 会默认使用推荐模型。

```toml
model = "gpt-5.5"
```

#### 临时选择不同的本地模型

在 Codex CLI 中，你可以在活动线程中使用 `/model` 命令更改模型。在 IDE extension 中，你可以使用输入框下方的模型选择器来选择模型。

要使用特定模型启动新的 Codex CLI 线程，或为 `codex exec` 指定模型，可以使用 `--model`/`-m` 标志：

```bash
codex -m gpt-5.5
```

#### 为云任务选择模型

目前，你无法更改 Codex 云任务的默认模型。
