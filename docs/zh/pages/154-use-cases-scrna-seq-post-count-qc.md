### 注释 scRNA-seq 数据

Source: [Annotate scRNA-seq data](https://developers.openai.com/codex/use-cases/scrna-seq-post-count-qc.md)

在一个线程中审查单细胞 QC、annotations 和 UMAPs。

#### 概览

使用 Codex 搭配 NGS Analysis plugin，把 10x-style matrix bundle 转成经过 QC 过滤的 single-cell artifacts、带阈值理由的 filtering summaries、annotations 和 UMAPs，你可以在同一线程中检查并修订。

适合：

- 在 count generation 后进行 matrix-level QC、annotation 和 visualization 的 single-cell teams。
- 需要有阈值依据的 filtering，以及可审计的 cells removed 或 flagged 记录的研究人员。
- 希望获得便携 review surface，并包含 generated figures、visualization index 和 notebook 或 app handoff 的团队。

相关 skill：

- `NGS Analysis`：运行 single-cell post-count QC，并返回 filtering、visualization、annotation 和 notebook artifacts。

#### 起始提示

**运行 scRNA-seq post-count QC**

```text
使用 NGS Analysis plugin。

使用指定的 10x-style matrix bundle，加上 manifest 和 dataset metadata，把这个 matrix-level input 路由到 scrna-seq-qc。

从观测分布中选择 QC thresholds，保留 raw counts，并生成 global/per-group UMAPs。

返回：
- summary.md
- 每个 filter 对应 cells removed 或 flagged 的 QC summary table
- threshold-justification plots
- filtered .h5ad
```

建议使用高推理强度。

#### 利用 skills

NGS Analysis plugin 包含：

- `ngs-analysis-router`
- `scrna-seq-qc`
- `ngs-scrna-seq`

当你使用该 plugin 时，Codex 可以使用所有这些打包 skills。

#### 分步指南

1. 将 Codex 指向适当的 matrix、barcodes、genes 或 features、manifest 和 dataset metadata，或提供确切 file references。
2. 运行起始提示，让 Codex 从观测分布中选择 QC thresholds，并把依据记录到 run artifacts 中。
3. 打开 visualization index 和 review notebook 或 app，检查 QC pass 或 fail counts、UMAPs 和 annotation confidence。
4. 在同一线程中继续细化 thresholds、提供 matched reference atlas，或在解除 doublet detection 阻塞后重新运行。

#### 结果

这次运行会为 filtering decisions 生成 review surface，而不只是 filtered matrix。先从 threshold-justification plots 和 QC summary 开始，这样你可以看到每个 filter removed 或 flagged 了多少 cells，以及所选 cutoffs 是否匹配观测分布。

![审查单细胞运行的 threshold-justification 图，以及 QC 通过或失败计数。](https://developers.openai.com/codex/use-cases/scrna-seq-post-count-qc-screenshot-1.webp)

然后按 coarse label 和 Leiden cluster 检查生成的 UMAPs。这些视图更容易识别 annotation gaps、可疑 clusters，或需要再做一轮的 threshold choices。

![按 coarse label 和 Leiden cluster 检查 UMAP 图。](https://developers.openai.com/codex/use-cases/scrna-seq-post-count-qc-screenshot-2.webp)

最后，审查 cell-level metrics 和 filtering outcomes。Codex 会把这张表与 filtered `.h5ad` 和 visualization artifacts 一起保留，这样你可以在同一线程中修订 thresholds，而不会丢失第一轮的依据。

![打开 cell-level QC metrics 和 filtering outcomes 进行审查。](https://developers.openai.com/codex/use-cases/scrna-seq-post-count-qc-screenshot-3.webp)

#### 相关链接

- [申请 GPT-Rosalind 访问权限](https://openai.com/form/life-sciences-access/)
