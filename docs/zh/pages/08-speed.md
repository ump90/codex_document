### 速度

Source: [Speed](https://developers.openai.com/codex/speed.md)

#### 快速模式

Codex 提供了提高模型速度的能力，但会增加
点数消耗。

Fast mode 将受支持模型的速度提高 1.5 倍，并以比 Standard mode 更高的
速率消耗点数。它目前支持 GPT-5.5 和 GPT-5.4，
GPT-5.5 按 Standard 速率的 2.5 倍消耗点数，GPT-5.4 按 Standard
速率的 2 倍消耗点数。

在 CLI 中使用 `/fast on`、`/fast off` 或 `/fast status` 来更改或查看
当前设置。你也可以在 `config.toml` 中使用 `service_tier =
"fast"` 加上 `[features].fast_mode = true` 持久化默认值。当你
使用 ChatGPT 登录时，Codex IDE 扩展、Codex CLI 和 Codex app 均
可使用 Fast mode。使用 API key 时，Codex 会改用标准 API 定价，
且你无法使用 Fast mode 点数。

#### Codex-Spark

GPT-5.3-Codex-Spark 是一个独立、快速、能力较弱的 Codex 模型，针对
近乎即时的实时编码迭代进行了优化。不同于以更高点数消耗速率加速
受支持模型的 fast mode，Codex-Spark 是一个独立模型选择，
并有自己的使用限制。

在研究预览期间，Codex-Spark 仅向 ChatGPT Pro 订阅者开放。

## 审批、沙箱和安全

<a id="approvals-sandboxing-and-security"></a>

沙箱行为、审批、网络安全，以及安全相关的专项指导。
