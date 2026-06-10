### 为 AI 应用添加 evals

Source: [Add evals to your AI application](https://developers.openai.com/codex/use-cases/ai-app-evals.md)

使用 Codex 把预期行为转成 Promptfoo eval suite。

#### 概览

让 Codex 检查你的 AI 应用，识别你想评估的行为，并添加可运行的 Promptfoo eval suite。

适合：

- 已有 prompts、模型调用、工具、检索、agents 或产品需求，但还没有可重复 eval suite 的 AI 应用。
- 正在准备模型、prompt、检索或 agent 变更，并希望 pull request 合并前有回归测试的团队。
- 希望把重复手工检查变成已提交 eval case 的质量审查。

相关 skill：

- `promptfoo`：包含 `$promptfoo-evals` 和 `$promptfoo-provider-setup` 的 plugin，用于创建、连接、运行和 QA eval suite。

#### 起始提示

```text
使用 $promptfoo-evals 为这个 AI 应用添加一个 Promptfoo eval suite。如果还没有可用的 Promptfoo provider 或 target adapter，请先使用 $promptfoo-provider-setup。

要评估的行为：[支持回答质量 / tool-call 正确性 / 检索 grounding / 业务规则 / agent 任务完成]

编辑前：
- 检查用户实际访问的 app path，以及任何现有 evals 或测试。
- 提出最小但有用的 eval 计划：target adapter、seed cases、assertions、文件、命令，以及所需 env vars 或本地服务。
- 在 baseline eval 存在并已运行前，不要更改生产 prompts、模型设置或应用行为。

要求：
- 可行时，测试用户实际访问的应用路径，而不仅是原始模型 prompt。
- fixtures 不得包含 secrets、客户数据和敏感个人数据。
- 添加本地 eval 命令，例如 `npm run evals`，或记录要运行的确切命令。

结束时给出：
- 变更文件
- 已运行的 eval 命令
- 通过和失败的 cases
- 建议下一步添加的 evals
```

建议使用中等工作量。

#### 相关链接

- [Promptfoo 配置](https://www.promptfoo.dev/docs/configuration/guide/)
- [评估最佳实践](https://developers.openai.com/api/docs/guides/evaluation-best-practices)

#### 引言

当你构建 AI 应用，或修改已有 AI 应用时，需要确保它按预期运行。Evals 是一种系统化测试一组场景、并在发布前捕捉回归的方法。

你可以使用 Promptfoo 在 AI 应用上运行 evals，并使用 Codex 帮你创建和维护这些 evals。

#### 如何使用

将 Codex 与 Promptfoo plugin 的 `$promptfoo-evals` skill 一起使用，把一个 AI 应用行为转成可重复的 eval suite。当应用还没有可用的 Promptfoo target 时，`$promptfoo-provider-setup` 可以帮助把 suite 连接到你要测试的应用路径。

Codex 可以检查应用、提出高信号 case、添加 Promptfoo 配置和测试数据、在本地运行 suite，并给出一个可持续使用的命令。

当行为足够具体时，这个使用场景效果最好：支持回答质量、检索 grounding、分类器标签、tool call、JSON 形状、业务规则，或 prompt 和模型迁移信心。

强有力的第一版应是可审查代码和测试数据：`promptfooconfig.yaml` 或等效配置，一个小型 `evals/` 目录、测试用例、调用应用所需的 target adapter，以及本地命令，例如 `npm run evals`。

#### 选择要评估的内容

从一个用户可见承诺开始。避免要求 Codex 一次性评估整个 AI 系统。较小的 suite 更容易信任、审查和持续运行。

好的第一批目标包括：

- **正确性：** 分类、抽取、总结、路由或转换。
- **Grounding：** 应与检索文档或引用来源保持绑定的回答。
- **工具使用：** 选择正确工具、传递有效参数，并处理工具错误。
- **格式或业务规则：** JSON schema、字段名、业务规则限制，或面向 UI 的文案契约。
- **Prompt 或模型迁移：** 确保新的 prompt、模型、system message 或检索设置不会破坏重要 case。

从产品需求、bug 报告、支持升级，或团队愿意提交到仓库的脱敏示例开始。

#### 请求 eval 计划

Codex 应先检查再编辑。要求它给出一个计划，点明 target path、fixtures、assertions、adapter 和命令。这样你可以在添加文件前发现错误 target 或薄弱测试 case。

实现前审查计划。计划应点明 Promptfoo 将调用的应用路径或 endpoint、第一批 seed cases、assertions、Codex 将创建的文件、本地命令，以及任何所需 secrets 或服务。如果计划测试的是原始模型，而不是用户实际访问的应用路径，请询问 Codex 这是否是有意选择。

#### 实现、运行和迭代

计划正确后，要求 Codex 实现它。第一版实现应该朴素：配置、cases、fixtures、必要时的 target adapter、命令，以及命令已运行的证明。

一个小型、由应用支撑的 suite 可能如下：

```text
evals/
  promptfooconfig.yaml
  tests/
    cases.yaml
  providers/
    provider.js  # 仅当内置 provider 无法直接调用应用时需要
```

在改变行为前运行 suite。Baseline 会告诉你应用是否已经在这些 case 上失败、assertions 是否需要调优，或 target adapter 是否错误。当 assertions 过于脆弱或模糊时进行调优，但要让真实产品失败保持可见。

第一次运行后，在发布前使用 suite 比较应用变更。每当 bug、发布需求或产品审查揭示你想保持稳定的行为时，就添加新 case。当本地命令稳定后，要求 Codex 把它加入 CI 或发布检查清单。
