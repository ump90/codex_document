### 分析数据集并交付报告

Source: [Analyze datasets and ship reports](https://developers.openai.com/codex/use-cases/datasets-and-reports.md)

把杂乱数据转化为清晰的分析和可视化。

#### 概览

使用 Codex 清理数据、联接来源、探索假设、建模结果，并把输出打包成可复用 artifact。

适合：

- 从杂乱文件开始，并应以图表、备忘录、dashboard 或报告结束的数据分析。
- 希望 Codex 协助清理、联接、探索性分析和可复现脚本的分析师。
- 需要可审查 artifact，而不是一次性 notebook 状态的团队。

相关 skill：

- `$spreadsheet`：当公式、导出或快速电子表格检查很重要时，检查 CSV、TSV 和 Excel 文件。
- [`$jupyter-notebook`](https://github.com/openai/skills/tree/main/skills/.curated/jupyter-notebook)：为探索性分析、实验和可复用 walkthrough 创建或重构 notebook。
- [`$doc`](https://github.com/openai/skills/tree/main/skills/.curated/doc)：当版式、表格或批注很重要时，产出可交给利益相关者的 `.docx` 报告。
- [`$pdf`](https://github.com/openai/skills/tree/main/skills/.curated/pdf)：渲染 PDF 输出，并在分享前检查最终分析 artifact。

#### 起始提示

**把数据集转化为可复现分析**

```text
我正在这个 workspace 中做一个数据分析项目。

目标：
- 判断高速公路附近的房屋估值是否更低。

先从以下事项开始：
- 阅读 `AGENTS.md` 并解释推荐的 Python 环境
- 加载 [dataset path] 处的数据集
- 描述每个文件包含什么、可能的 join keys，以及明显的数据质量问题
- 提出一个可复现工作流，从导入和整理，到可视化、建模和报告输出

约束：
- 相比一次性 notebook 状态，优先使用脚本和已保存 artifact
- 不要虚构缺失值或 merge keys
- 建议任何能让工作流更可复现的 skills 或 worktree 拆分

输出：
- 设置计划
- 数据清单
- 分析计划
- 要创建的第一批命令或文件
```

#### 相关链接

- [Agent skills](48-agent-skills.md)
- [Codex app 中的 Worktrees](42-worktrees.md)

#### 技术栈

| 需求 | 推荐默认选择 | 原因 |
| --- | --- | --- |
| 分析栈 | [pandas](https://pandas.pydata.org/) 配合 [matplotlib](https://matplotlib.org/) 或 [seaborn](https://seaborn.pydata.org/) | 对导入、profiling、联接、清理和第一轮图表来说是良好的默认选择。 |
| 建模 | [statsmodels](https://www.statsmodels.org/) 或 [scikit-learn](https://scikit-learn.org/stable/) | 在转向更复杂预测模型前，先从可解释 baseline 开始。 |

## 介绍

数据分析的核心，是用数据为决策提供依据。目标不是为了分析而分析，而是产出能帮助别人行动的 artifact：给领导层看的图表、给产品团队看的实验解读、给研究人员看的模型评估，或指导日常运营的 dashboard。

一个由 _R for Data Science_ 推广的实用框架是一个循环：导入并整理数据，然后在转换、可视化和建模之间迭代，以便在沟通结果前建立理解。编程环绕整个循环。

Codex 很适合这个工作流。它可以帮助你更快地在循环中移动：清理数据、探索假设、生成分析，并产出可复现 artifact。目标不是一次性 notebook，而是其他人可以审查、信任并重新运行的工作流。

## 定义你的用例

选择一个你希望用数据回答的具体问题。

问题越具体越好。这会帮助 Codex 理解你想达成什么，以及如何帮助你到达目标。

### 运行示例：高速公路附近的房产价值

例如，我们将探索以下问题：

> 高速公路附近的房屋估值在多大程度上更低？

假设一个数据集包含房产价值或成交价，另一个数据集包含位置、地块或高速公路距离信息。工作并不只是跑一个模型，而是让输入可信、记录联接方式、压力测试结果，并最终交付一个别人可以使用的 artifact。

## 设置环境

开始一个新的数据分析项目时，你需要设置环境并定义项目规则。

- **环境：** Codex 应知道项目中哪个 Python 环境、包管理器、文件夹和输出约定是权威的。
- **Skills：** notebook 清理、电子表格导出或最终报告打包等重复工作流，应移入可复用 skills，而不是在每个提示里重新解释。
- **Worktrees：** 把探索拆到不同 worktrees 中，这样一个假设、merge 策略或可视化分支就不会污染另一个。

要进一步了解如何安装和使用 skills，请参阅我们的 [skills 文档](48-agent-skills.md)。

### 引导 Codex 的行为

在接触数据之前，告诉 Codex 应如何在仓库中行动。把个人默认设置放在 `~/.codex/AGENTS.md`，把项目规则放在仓库的 `AGENTS.md`。

一个简短的 `AGENTS.md` 通常就足够：

```md
## Data analysis defaults

- Use `uv run` or the project's existing Python environment.
- Keep source data in `data/raw/` and write cleaned data to `data/processed/`.
- Put exploratory notebooks in `analysis/` and final artifacts in `output/`.
- Never overwrite raw files.
- Prefer scripts or checked-in notebooks over unnamed scratch cells.
- Before merging datasets, report candidate keys, null rates, and join coverage.
```

如果仓库尚未定义 Python 环境，请让 Codex 创建一个可复现设置，并解释如何运行它。对数据分析工作来说，这一步比直接跳到图表更重要。

## 导入数据

通常最快的开始方式，是粘贴文件路径并让 Codex 检查它。Codex 在这里会帮助你回答基础但重要的问题：

- 这里有哪些文件格式？
- 每个数据集看起来代表什么？
- 哪些列可能是目标、标识符、日期、位置或度量？
- 明显的质量问题在哪里？

先不要要求结论。先要求清单和解释。

## 整理并合并输入

大多数真实工作从这里开始。你有两个或更多数据集，主键并不清楚，而天真的 merge 可能丢失数据或制造重复。

让 Codex 在真正合并前 profile 这次 merge：

- 检查候选键的唯一性。
- 衡量 null rate 和格式差异。
- 规范化明显的格式问题，例如大小写、空白或地址格式。
- 运行试验性 join 并报告匹配率。
- 在写入最终合并文件前，推荐最安全的 merge 策略。

如果你需要推导最佳键，例如规范化地址、由几列构造的地块标识符，或位置 join，请让 Codex 在你接受 merge 前解释权衡和边界情况。

## 用图表和独立 worktrees 探索

探索性数据分析受益于干净隔离。一个 worktree 可以测试地址清理或特征工程，另一个专注于图表或替代模型方向。这能让每个 diff 可审查，并防止一个长线程混入不兼容的想法。

Codex app 包含内置 worktree 支持。如果你在终端中工作，普通 Git worktrees 也很好用：

```bash
git worktree add ../analysis-highway-eda -b analysis/highway-eda
git worktree add ../analysis-model-comparison -b analysis/highway-modeling
```

在运行示例中，这一步会比较高速公路附近房屋和更远房屋，检查离群点，查看缺失值模式，并判断观察到的影响看起来是真实存在，还是反映了社区构成、房屋大小或其他因素。

## 为问题建模

并非每个分析都需要复杂模型。先从可解释 baseline 开始。

对于高速公路问题，合理的第一步是回归或其他透明模型，在控制大小、房龄和位置等相关因素的同时，估计高速公路距离与房产价值之间的关系。

让 Codex 明确说明：

- 目标变量和特征定义。
- 包含哪些控制变量以及原因。
- 泄漏风险和排除项。
- 它如何选择 split、evaluation 或不确定性估计。
- 结果用普通语言意味着什么。

如果第一个模型很弱，它仍然有用。它会告诉你问题出在模型、特征、join 质量，还是问题本身。

## 沟通结果

只有当别人能消费分析时，分析才有用。让 Codex 产出受众需要的 artifact：

- 给技术合作者的 Markdown 备忘录。
- 给下游运营工作的电子表格或 CSV。
- 当格式和表格重要时，使用 `$doc` 创建 `.docx` brief。
- 使用 `$pdf` 生成渲染后的附录或最终交付物。
- 使用 `$vercel-deploy` 部署轻量 dashboard 或静态报告站点。

这也是你要求列出 caveats 的地方。如果 join 质量不完美、存在采样偏差，或模型假设很脆弱，Codex 应在交付物中直说。

## 可考虑的 Skills

特别适合这个工作流的 curated skills 包括：

- `$spreadsheet` 用于 CSV、TSV 和 Excel 编辑或导出。
- `$jupyter-notebook` 用于交付物应保持 notebook-native 的场景。
- `$doc` 和 `$pdf` 用于面向利益相关者的输出。
- `$vercel-deploy` 用于你希望以 URL 分享结果的场景。

工作流稳定后，为重复部分创建仓库本地 skills，例如 `refresh-data`、`merge-and-qa` 或 `publish-weekly-report`。相比在每个线程中粘贴同一段流程提示，这是更好的长期模式。

## 建议提示

**设置分析环境**

**加载数据集并解释它**

**在 Join 前 Profile Merge**

**打开一个新的探索 Worktree**

**构建可解释的第一个模型**

**为利益相关者打包结果**
