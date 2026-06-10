### 升级 API 集成

Source: [Upgrade your API integration](https://developers.openai.com/codex/use-cases/api-integration-migrations.md)

把你的应用升级到最新 OpenAI API 模型。

#### 概览

使用 Codex 将现有 OpenAI API 集成更新到最新推荐模型和 API 功能，同时在发布前检查回归。

适合：

- 从较旧模型或 API surface 升级的团队。
- 需要在显式验证下保持行为不变迁移的仓库。

相关 skill：

- `$openai-docs`：在 Codex 修改你的实现前，拉取当前模型、迁移和 API 指南。

#### 起始提示

```text
使用 $openai-docs 将这个 OpenAI 集成升级到最新推荐模型和 API 功能。

具体来说，请查找此特定模型的最新模型和 prompt 指南。

要求：
- 先盘点仓库中当前模型、endpoint 和工具假设。
- 找到让我们迁移到最新受支持路径的最小迁移计划。
- 除非新 API 或模型要求改变，否则保持行为不变。
- 使用最新模型 prompt 指南更新 prompts。
- 指出需要我们人工审查的任何 prompt、工具或响应形状变化。
```

#### 相关链接

- [最新模型指南](https://developers.openai.com/api/docs/guides/latest-model)
- [提示词指导](https://developers.openai.com/api/docs/guides/prompt-guidance)
- [OpenAI Docs MCP](https://developers.openai.com/learn/docs-mcp)
- [Evals 指南](https://developers.openai.com/api/docs/guides/evals)

#### 引言

随着我们发布新模型和 API 功能，我们建议升级你的集成，以获得最新改进。从一个模型切换到另一个模型，通常不只是更新模型名称那么简单。

API 可能会发生变化。例如，对于 GPT-5.4 模型，我们在 assistant message 中添加了一个新的 `phase` 参数，这个参数很重要，应包含在你的集成中。更重要的是，模型行为可能不同，并需要调整现有 prompts。

迁移到新模型时，你不仅应完成必要代码变更，还应评估它对工作流的影响。

#### 利用 OpenAI Docs skill

关于新 API 功能和模型行为的所有细节都记录在我们的文档中，包括 [latest model](https://developers.openai.com/api/docs/guides/latest-model) 和 [prompt guidance](https://developers.openai.com/api/docs/guides/prompt-guidance) 指南。

OpenAI Docs skill 还包含[具体指导](https://github.com/openai/codex/blob/6323f0104d17d211029faab149231ba787f7da37/codex-rs/skills/src/assets/samples/openai-docs/references/upgrading-to-gpt-5p4.md)，可作为具体迁移参考。对于当前升级目标，请使用 [latest model](https://developers.openai.com/api/docs/guides/latest-model) 指南。

Codex 现在会自动附带 OpenAI Docs skill，因此在使用 OpenAI API 构建时，请务必在提示中提到它，以访问所有最新文档和指南。

#### 构建稳健的 evals 流水线

Codex 可以根据最新 prompt 指南自动更新你的 prompts，但你应有一种方式自动验证集成按预期工作。

请确保构建 evals 流水线，在每次修改集成时运行，以验证行为没有回归。

这篇 [cookbook guide](https://developers.openai.com/cookbook/examples/evaluation/building_resilient_prompts_using_an_evaluation_flywheel) 详细介绍了如何使用我们的 [Evals API](https://developers.openai.com/api/docs/guides/evals) 做到这一点。
