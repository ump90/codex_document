### 排定药物靶点优先级

Source: [Prioritize drug targets](https://developers.openai.com/codex/use-cases/target-prioritization.md)

跨多个证据通道对药物靶点排序。

#### 概览

使用 Codex 搭配 Life Science Research plugin，规范化实体，并行检索 genetics、cohort、clinical、literature 和 expression evidence，为每个 evidence lane 评分，并生成带可复用视觉内容的最终排名。

适合：

- 需要多个证据家族的 target prioritization 问题，例如 genetics、cohort replication、disease context、clinical precedent、literature 和 expression。
- 希望 Codex 跨多个 evidence lanes 执行 scientific research，然后把结果调和成一个结论的团队。
- 希望保存 raw payloads、使用明确 scoring rubric，并获得可在下一次 review 或 decision memo 中复用的 visuals 的科学家。

相关 skill：

- `Life Science Research`：搜索 scientific databases 和 literature，为 pathway、translational、tractability 和 competitive evidence 提供依据。

#### 起始提示

**排定哮喘药物靶点优先级**

```text
使用 Life Science Research plugin，对 TSLP、IL33 和 IL1RL1 进行哮喘 target prioritization 比较。

用 subagents 并行运行这些独立 lanes：
- 人类遗传学和 GWAS：gwas-catalog-skill、opentargets-skill、gnomad-graphql-skill
- Cohort replication 和 PheWAS：finngen-phewas-skill、ukb-topmed-phewas-skill、biobankjapan-phewas-skill、tpmi-phewas-skill
- Target-disease evidence 和疾病上下文：opentargets-skill、efo-ontology-skill
- 临床和监管先例：clinicaltrials-skill、opentargets-skill、chembl-skill、pharmgkb-skill
- 文献和公共数据集上下文：ncbi-entrez-skill、ncbi-pmc-skill、biorxiv-skill、ncbi-datasets-skill、biostudies-arrayexpress-skill
- Expression 和 tissue/cell-type 上下文：human-protein-atlas-skill、gtex-eqtl-skill、cellxgene-skill、bgee-skill

对每个 lane：
- 按 1-5 分给 TSLP、IL33、IL1RL1 评分
- 把 direct asthma evidence 与相邻 allergic/atopic phenotypes 分开
- 在有帮助时保存 raw payloads

然后综合：
- lane-by-target score table
- TSLP、IL33、IL1RL1 的最终排序
- confidence assessment 和主要 caveats
- 两个 visuals：prioritization heatmap，以及包含每个 target 的 lead asthma-linked variants 的 GWAS summary figure
```

建议使用高推理强度。

#### 利用 skills

[Life Science Research plugin](https://github.com/openai/plugins/tree/main/plugins/life-science-research) 包含每个 evidence lane 的 skills：

- 人类遗传学和 GWAS：`gwas-catalog-skill`、`opentargets-skill`、`gnomad-graphql-skill`
- Cohort replication 和 PheWAS：`finngen-phewas-skill`、`ukb-topmed-phewas-skill`、`biobankjapan-phewas-skill`、`tpmi-phewas-skill`
- Target-disease evidence 和疾病上下文：`opentargets-skill`、`efo-ontology-skill`
- 临床和监管先例：`clinicaltrials-skill`、`opentargets-skill`、`chembl-skill`、`pharmgkb-skill`
- 文献和公共数据集上下文：`ncbi-entrez-skill`、`ncbi-pmc-skill`、`biorxiv-skill`、`ncbi-datasets-skill`、`biostudies-arrayexpress-skill`
- Expression 和 tissue/cell-type 上下文：`human-protein-atlas-skill`、`gtex-eqtl-skill`、`cellxgene-skill`、`bgee-skill`

你可以通过明确提到这些 skills 来使用它们，也可以让 Codex 自行决定何时使用。

#### 分步指南

1. 从一个具体比较问题开始，并说明你希望 Codex 覆盖的确切 targets、disease 和 evidence lanes。
2. 调用 `Life Science Research` plugin，并告诉 Codex 用 subagents 并行运行各 lane，让每个 evidence family 保持有边界。
3. 要求 Codex 按固定 1-5 分制给每个 lane 评分，并把 direct disease evidence 与 adjacent phenotypes 分开。
4. 在同一线程中审查保存的 raw payloads、lane-by-target score table 和综合排序。

#### 相关链接

- [申请 GPT-Rosalind 访问权限](https://openai.com/form/life-sciences-access/)
