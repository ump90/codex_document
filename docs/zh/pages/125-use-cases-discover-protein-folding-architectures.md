### 发现蛋白质折叠架构

Source: [Discover protein folding architectures](https://developers.openai.com/codex/use-cases/discover-protein-folding-architectures.md)

把蛋白质折叠假设转化为带基准的实验循环。

#### 概览

结合 Goal Mode 使用 Codex，研究并实现对 AlphaFold2 的新型架构修改，以提升蛋白质折叠性能。

适合：

- 计算生物学家在可自动评分基准上探索架构、loss 或 curriculum 变更。
- 已有科学动机假设，并希望压缩从想法到可运行实验 fork 路径的研究人员。
- 运行长期 autoresearch 循环，并需要持久实验跟踪和迭代调试的 ML 工程师。

#### 起始提示

**运行科学家引导的架构搜索**

```text
使用 Goal Mode，在 NanoFold public benchmark 上提升这个 AlphaFold2 风格蛋白质结构模型的 validation lDDT-Cα score。

科学假设是：持久的高阶几何状态可能帮助模型从有限数据中更高效地学习蛋白质几何：

- 保留标准 MSA 和 pairwise representations；
- 为选定 residue triplets 添加稀疏学习的 2-simplex face states；
- 为选定 residue quadruplets 添加稀疏学习的 3-simplex tetrahedral states；
- 只从官方 benchmark inputs 和模型生成的 recycled geometry 构建 topology；
- 在 NanoFold 约束下保持实现具备计算可行性。

维护持久跟踪文件：

1. 在 PLAN.md 中维护当前策略、状态和建议下一步
2. 在 EXPERIMENTS.md 中维护实验和结果的结构化日志
3. 在 EXPERIMENT_NOTES.md 中维护持续更新的笔记和想法 scratchpad

每次迭代：

1. 说明正在测试的假设；
2. 做出最小的连贯代码或配置变更；
3. 运行相关测试和 benchmark slice；
4. 记录 metrics、latency、memory 和 failure modes；
5. 决定保留、回滚或细化该变更；
6. 定期重新评估架构层面的搜索方向，而不是只调本地 hyperparameters。

不要根据 smoke tests 或 single-chain overfit diagnostics 声称 generalization gains。优先使用 matched comparisons，并保持证据边界。
```

建议使用高工作量。

#### 相关链接

- [跟进目标](130-use-cases-follow-goals.md)
- [SimplexFold 仓库](https://github.com/ChrisHayduk/SimplexFold)
- [SimplexFold benchmark 计划](https://github.com/ChrisHayduk/SimplexFold/blob/main/BENCHMARK_PLAN.md)
- [NanoFold 竞赛](https://github.com/ChrisHayduk/nanoFold-Competition)

## 探索蛋白质折叠架构假设

当你的蛋白质折叠假设需要不止一次实现 pass 时，使用 Codex Goal Mode。给 Codex 一个有边界的科学方向、一个可运行 baseline，以及一个可自动评分 benchmark。Codex 可以实现架构 fork、跟踪实验、诊断失败，并在你审查证据的同时持续迭代。

这个示例始于一个具体问题：如果 AlphaFold2 风格模型的 trunk 不只表示 residues 和 residue pairs，而是同时表示显式高阶拓扑对象，它是否能更高效地学习有用的蛋白质几何？

## 定义有边界的实验

AlphaFold2 已经在 Evoformer 中使用强大的 pairwise 和 triangle-style 推理。它的 triangle operations 改进 edge representations，但仍写回 pair tensor。科学家提出测试：在数据受限设置中，为 triangular faces 和 tetrahedral cells 提供持久学习表示，是否能提供有用的 inductive bias。

最终的公开仓库 [SimplexFold](https://github.com/ChrisHayduk/SimplexFold) 在传统 pair representation `Z_ij` 旁边加入稀疏 face states `F_ijk` 和 tetrahedral states `U_ijkl`。

```text
MSA representation M
        <-> pair / edge tensor Z_ij
        <-> sparse face tensor F_ijk
        <-> sparse tetra tensor U_ijkl
        -> structure module
        -> recycled geometry
        loops back into the next pass
```

从本页起始提示、一个最小 AlphaFold2 风格 baseline，以及公开 NanoFold benchmark 开始。这个 benchmark 为结构生物学实验提供了小型、精心整理、固定数据且可自动评分的基底。第一次实现应足够小，能在启动昂贵训练前先用定向 unit tests 和 microbenchmarks 测试。

## 用 Goal Mode 运行搜索

1. 提供一个可证伪的高层科学假设，而不是要求模型从零发明完整研究议程。
2. 在 ChatGPT 中使用 GPT-5.5 Pro，把该方向转换成带明确约束和 ablations 的实现计划。
3. 让 Codex 实现最小可运行的 [SimplexFold](https://github.com/ChrisHayduk/SimplexFold) baseline，然后用定向 unit tests 和 microbenchmarks 验证。
4. 将所得仓库交给 Codex Goal Mode，并指示它在 NanoFold benchmark 上 hill-climb validation `lDDT-Cα`，同时保留实验日志、计划和 artifact 引用。
5. 持续运行 Goal Mode，让它使用 benchmark 反馈迭代架构、训练 recipe 和实验 harness。在这个示例中，该循环运行了超过 150 小时。

使用 `PLAN.md` 记录当前策略和下一步，使用 `EXPERIMENTS.md` 记录结构化结果日志，使用 `EXPERIMENT_NOTES.md` 作为持续更新的 scratchpad。这些 artifact 让长时间搜索可审计，并为你引导下一轮迭代提供稳定位置。

Goal Mode 在这里有用，是因为搜索需要反复实现、测试、实验跟踪、失败诊断和由 benchmark 驱动的迭代。无引导 autoresearch 往往会漂移到常见的本地变更，例如 losses、optimizers 和 hyperparameters。由科学家提供的紧凑架构假设，为 Codex 提供了更有意义的搜索空间，同时仍保留测试、诊断和细化实现的余地。

这个工作流也适用于评估 scientist-in-the-loop 引导如何改变 agentic scientific search 质量的团队。

## 示例结果

这个工作流的结果是 [SimplexFold](https://github.com/ChrisHayduk/SimplexFold)，一个带显式高阶 simplex states 的实验架构。请结合 benchmark logs 审查 topology，以确认每次迭代仍在测试原始科学想法。

![1-simplex、2-simplex 和 3-simplex 蛋白质几何对比。](https://developers.openai.com/codex/use-cases/discover-protein-folding-architectures-simplex.webp)

有用的经验不是 Codex 自主解决了蛋白质折叠。这个工作流展示了 Goal Mode 如何作为持久科学工程循环发挥作用：科学家贡献概念性移动，Codex 压缩实现、实验、调试和后续搜索周期。

把有希望的 diagnostics 视为实现路径有效的证据，而不是 generalization 的证明。定期审查 agent 的轨迹；如果它退化为本地 hyperparameter tuning，就把它拉回科学上有意义的架构问题；只有在 matched public-validation comparisons 和合适 replicates 之后，才提升 claim 的可信度。

## 资源

- [SimplexFold 仓库](https://github.com/ChrisHayduk/SimplexFold)
- [SimplexFold benchmark 计划](https://github.com/ChrisHayduk/SimplexFold/blob/main/BENCHMARK_PLAN.md)
- [NanoFold 竞赛](https://github.com/ChrisHayduk/nanoFold-Competition)
- [NanoFold 竞赛规则](https://github.com/ChrisHayduk/nanoFold-Competition/blob/main/docs/COMPETITION.md)
- [Goal Mode 运行超过 150 小时](https://x.com/ChrisHayduk/status/2055757345506877759?s=20)
- [Goal Mode 文章](https://x.com/ChrisHayduk/status/2053807198870880743?s=20)
