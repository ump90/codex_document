### 理解大型代码库

Source: [Understand large codebases](https://developers.openai.com/codex/use-cases/codebase-onboarding.md)

追踪请求流、映射陌生模块，并快速找到合适文件。

#### 概览

使用 Codex 映射陌生代码库、解释不同模块和数据流，并在你编辑前指出接下来值得阅读的文件。

适合：

- 入职新 repo 或服务的新工程师。
- 任何想在修改功能前理解它如何工作的人。

#### 起始提示

```text
解释请求如何流经代码库中的 <name of the system area>。

包含：
- 哪些模块负责什么
- 数据在哪里验证
- 修改前要注意的主要坑

最后列出我接下来应该阅读的文件。
```

建议模型：`gpt-5.3-codex-spark`

建议使用中等工作量。

#### 相关链接

- [Codex app](44-codex-app.md)

#### 引言

当你刚接触一个 repo，或突然要处理一个陌生功能时，Codex 可以帮助你在开始改代码前建立方向感。目标不只是获得高层摘要，而是映射请求流、理解哪些模块负责什么，并识别接下来值得阅读的文件。

#### 如何使用

如果你刚接触一个项目，可以直接先要求 Codex 解释整个代码库。

如果你需要给现有代码库贡献新功能，可以要求 Codex 解释一个具体系统区域。请求范围越好，解释就越具体：

1. 给 Codex 提供你想理解的相关文件、目录或功能区域。
2. 要求它追踪请求流，并解释哪些模块拥有业务逻辑、transport、persistence 或 UI。
3. 在编辑任何内容前，询问 validation、side effects 或 state transitions 发生在哪里。
4. 最后询问你接下来应阅读哪些文件，以及风险点在哪里。

有用的 onboarding 回答应给你一张具体地图，而不只是文件名列表。到最后，Codex 应解释主要流程、突出风险部分，并指出你开始编辑前需要关注的后续文件或 checks。

#### 接下来可以问的问题

Codex 给出第一版后，继续追问，直到解释具体到你相信自己可以完成第一次编辑为止。好的 follow-up questions 通常会迫使它指出假设、隐藏依赖，以及变更后重要的 checks。

- 哪个模块真正拥有业务逻辑，哪些只是 transport 或 UI 层？
- validation 在哪里发生，那里强制了哪些假设？
- 如果我修改这个流程，哪些相关文件或 background jobs 容易被遗漏？
- 编辑这个区域后，我应该运行哪些 tests 或 checks？
