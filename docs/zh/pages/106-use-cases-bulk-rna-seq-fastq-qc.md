### 验证 bulk RNA-seq 输入

Source: [Validate bulk RNA-seq inputs](https://developers.openai.com/codex/use-cases/bulk-rna-seq-fastq-qc.md)

在差异表达分析前验证 bulk RNA-seq 输入。

#### 概览

将 Codex 与 NGS Analysis plugin 一起使用，验证 sample sheets、FASTQs 和 references，然后在差异表达分析前返回 MultiQC、Salmon matrices、provenance 和简短 QC 解读。

适合：

- 在差异表达分析前验证 bulk RNA-seq 输入的生物信息学团队。
- 希望在一个 thread 中获得 transcript 和 gene-level quantification 以及 QC 的研究人员。
- 需要审查 mapping-rate、duplication、library-type 和 resource-readiness 的团队。

相关 skill：

- `NGS Analysis`：验证测序输入，运行 bulk RNA-seq counts 和 QC，并返回可审计 artifact。

#### 起始提示

```text
使用 NGS Analysis plugin。

对提供的 sample sheet、FASTQ root、transcriptome FASTA、genome FASTA 和 GTF 运行 bulk RNA-seq FASTQ-to-count QC。

返回：
- run_manifest.json
- MultiQC 以及 browser-safe review links
- Salmon transcript- 和 gene-level matrices
- validation 和 resource-readiness artifacts
- 简短 QC 解读，指出 mapping rate、duplication、library-type agreement、outlier samples，以及任何会阻塞下游差异表达分析的问题
```

建议使用高工作量。

#### 相关链接

- [申请 GPT-Rosalind 访问权限](https://openai.com/form/life-sciences-access/)

#### 利用 skills

NGS Analysis plugin 包含：

- `ngs-analysis-router`
- `ngs-bulk-rnaseq-counts-qc`
- `ngs-runtime-env`

使用该 plugin 时，Codex 可以使用这些打包好的 skills。

#### 分步指南

1. 将 Codex 指向包含 sample sheet、FASTQs、transcriptome FASTA、genome FASTA 和 GTF 的目录，或提供确切文件引用。
2. 运行起始提示，让 Codex 在执行前验证 strandedness、reference consistency 和 tool readiness。
3. 在 Codex 中打开生成的 MultiQC 和 matrix artifacts，审查 mapping rate、duplication、library-type agreement 和 resource readiness。
4. 在同一个 thread 中继续修复 blockers、使用更新后的 metadata 重跑，或把生成的 gene-level matrices 交给下游差异表达分析。

#### 结果

运行返回的是经过 QC 审查的 counts bundle，而不是裸 quantification 输出。先查看 MultiQC 报告，识别可能影响下游解读的 warnings。在这个示例中，Codex 会把 FastQC sequence-content warnings 与运行摘要一起浮现出来，方便团队判断观察到的模式是否符合 library preparation 预期。

![在 bulk RNA-seq 运行摘要旁审查 FastQC sequence-content warnings。](https://developers.openai.com/codex/use-cases/bulk-rna-seq-fastq-qc-screenshot-1.webp)

接下来，在同一份报告中审查 Salmon 统计信息。Mapping rates、library-type assignments 和 duplication signals 会在差异表达分析前提供一个紧凑的就绪检查。

![从生成的 MultiQC 报告中检查 Salmon alignment 和 library-type statistics。](https://developers.openai.com/codex/use-cases/bulk-rna-seq-fastq-qc-screenshot-2.webp)

生成的 gene-level count matrix 会保存为可复用 artifact。在 Codex 中打开它，确认预期 samples 和 features 都存在，然后将它与 run provenance 一起保留，供下游分析使用。

![打开生成的 gene-level count matrix 进行下游审查。](https://developers.openai.com/codex/use-cases/bulk-rna-seq-fastq-qc-screenshot-3.webp)
