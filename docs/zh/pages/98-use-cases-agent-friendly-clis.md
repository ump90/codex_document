### 创建 Codex 可用的 CLI

Source: [Create a CLI Codex can use](https://developers.openai.com/codex/use-cases/agent-friendly-clis.md)

为 API、日志来源、导出或团队脚本提供一个 Codex 可组合使用的命令。

#### 概览

让 Codex 创建一个可组合 CLI：它可以从任何文件夹运行、与仓库脚本组合、用于下载文件，并通过配套 skill 记住用法。

适合：

- Codex 需要重复搜索、读取、下载，或安全写入同一个服务、导出、本地归档或仓库脚本的工作。
- 需要分页搜索、按 ID 精确读取、可预测 JSON、下载文件、本地索引，或先草稿后写入命令的代理工具。

相关 skill：

- `$cli-creator`：设计命令界面，构建 CLI，添加 setup 和 auth 检查，把命令安装到 `PATH`，并从另一个文件夹验证。
- `$skill-creator`：创建配套 skill，告诉后续 Codex 任务应先运行哪些 CLI 命令，以及哪些写入动作需要批准。

#### 起始提示

```text
使用 $cli-creator 创建一个你可以使用的 CLI，并在同一个 thread 中使用 $skill-creator 创建配套 skill。

要学习的来源：[docs URL、OpenAPI spec、已脱敏的 curl 命令、现有脚本路径、日志文件夹、CSV 或 JSON 导出、SQLite 数据库路径，或粘贴的 --help 输出]。

CLI 应支持的第一个任务：[从 build URL 下载失败 CI 日志、搜索支持 ticket 并按 ID 读取一个 ticket、查询 admin API、读取本地数据库，或运行现有脚本中的一个步骤]。

可选写入任务：[创建草稿评论、上传媒体、重试失败 job，或暂时只读]。

命令名：[cli-name，或推荐一个]。

编码前，请展示拟议的命令界面，并且只询问会阻塞构建的缺失细节。
```

#### 相关链接

- [Codex skills](48-agent-skills.md)
- [创建自定义 skills](48-agent-skills.md)

#### 引言

当 Codex 反复使用同一个 API、日志来源、导出的收件箱、本地数据库或团队脚本时，给这类工作一个可组合接口：一个它可以从任何文件夹运行、检查、缩小范围，并与 `git`、`gh`、`rg`、测试和仓库脚本组合的命令。

再添加一个配套 skill，记录 Codex 应何时使用该 CLI、先运行什么、如何保持输出简短、下载文件落在哪里，以及哪些写入命令需要批准。

在这个工作流中，`$cli-creator` 帮助 Codex 构建命令。`$skill-creator` 帮助 Codex 保存可复用 skill，例如 `$ci-logs`，未来任务可以按名称调用。

#### 如何使用

1. [判断这个任务是否需要 CLI](#判断-cli-应做什么)
2. [分享 Codex 应学习的来源](#分享文档文件或命令)
3. [运行 `$cli-creator`](#要求-codex-构建-cli-和-skill)
4. [测试已安装命令](#验证命令可从任何文件夹运行)
5. [以后调用已保存的 skill](#以后使用该-skill)

#### 判断 CLI 应做什么

从你希望 Codex 完成的事情开始，而不是从你希望它编写的技术开始。一个好的 CLI 会把重复的读取、搜索、下载、导出、草稿、上传、轮询或安全写入变成 Codex 可以从任意仓库运行的命令。

| 场景 | Codex 可以用 CLI 做什么 |
| --- | --- |
| **CI 日志藏在 build 页面后面。** | 接收一个 build URL，把失败 job 日志下载到 `./logs`，并返回文件路径和简短片段。 |
| **支持 ticket 以周度导出形式到达。** | 索引最新 CSV 或 JSON 导出，按客户或短语搜索，并按稳定 ID 读取一个 ticket。 |
| **API 响应太大，无法放入上下文。** | 只列出需要的字段，按 ID 读取完整对象，并把完整响应导出到文件。 |
| **Slack 导出里有很长的 thread。** | 使用 `--limit` 搜索，读取一个 thread，并返回邻近上下文，而不是整份归档。 |
| **团队脚本会运行四个不同步骤。** | 把 setup、发现、下载、草稿、上传、轮询和实时写入拆成独立命令。 |
| **plugin 找到了记录，但 Codex 需要一个文件。** | 让 plugin 保留在 thread 中；使用 CLI 下载附件、trace、报告、视频或日志包，并返回路径。 |

#### 分享文档、文件或命令

Codex 需要具体材料来学习：文档或 OpenAPI、已脱敏的 curl 命令、导出或数据库路径、日志文件夹，或现有脚本。如果你希望 CLI 遵循熟悉风格，请粘贴一小段来自 `gh`、`kubectl` 或团队自有工具的 `--help` 输出。

如果命令需要认证，请告诉 Codex 它应支持的环境变量名、配置文件路径或登录流程。请你自己在 shell 或配置文件中设置 secret。不要把 secret 粘贴到 thread。要求 Codex 在缺少认证时让 CLI 的 setup check 给出清晰失败信息。

#### 要求 Codex 构建 CLI 和 skill

使用本页的起始提示。填入 Codex 应学习的来源，以及 CLI 应支持的第一个任务。

在 Codex 写代码之前，它应展示拟议的命令界面，并且只询问会阻塞构建的缺失细节。

#### 验证命令可从任何文件夹运行

Codex 不应在 `cargo run`、`python path/to/script.py` 或未安装的 package 命令后就停下。要求它像后续任务会使用这个命令一样，从另一个仓库或临时文件夹测试已安装命令。

**像未来代理一样测试 CLI**

如果 Codex 返回一个巨大的 JSON blob，要求它缩小默认响应，并为完整 payload 添加文件导出。如果它忘记了批准边界，先让它更新配套 skill，再在另一个 thread 中使用。

#### 以后使用该 skill

当你再次需要这个 CLI 时，调用 skill，而不是再次粘贴文档：

对于重复性工作，先在普通 thread 中测试一次 skill，然后要求 Codex 把同一次调用转成自动化。
