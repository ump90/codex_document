# Codex 官方文档中文翻译

本仓库整理 OpenAI Codex 官方文档英文快照，并提供经过校订的简体中文翻译。

## 开始阅读

- [中文分页目录](docs/zh/README.md)：按官方章节分组，适合在 GitHub 上逐页阅读。
- [中文合订版](docs/codex-manual.zh.md)：单文件完整译文，适合搜索。
- [英文官方快照](docs/source/codex-manual.en.md)：翻译所依据的官方 Codex manual 聚合快照。

## GitHub Pages

本仓库已包含 GitHub Pages 发布配置：

- `mkdocs.yml`：MkDocs 站点配置。
- `.github/workflows/pages.yml`：使用 GitHub Actions 构建并部署到 GitHub Pages。
- `docs/index.md`：站点首页。

手工启用时，在 GitHub 仓库设置中将 Pages 的构建来源设为 **GitHub Actions**，
然后运行或等待 `Deploy documentation to GitHub Pages` workflow。

## 内容结构

- `docs/source/codex-manual.en.md`：官方 Codex manual 英文聚合快照。
- `docs/source/codex-manual.outline.md`：官方快照目录轮廓。
- `docs/source/pages/`：按官方页面拆分的英文源文档。
- `docs/zh/pages/`：按页面拆分的中文译文。
- `docs/zh/README.md`：中文页面目录。
- `docs/codex-manual.zh.md`：中文合订版。
- `docs/index.md`：GitHub Pages 站点首页和 `docs/` 目录入口。

## 来源

英文快照来自 OpenAI 官方 Codex manual，由 Codex 的 `openai-docs`
文档流程获取。每个页面片段保留原文中的 `Source:` 链接，便于回溯到官方页面。

中文译文是本仓库维护的翻译版本。文中产品名、命令、配置键、模型名和必要的 UI
标签保留英文；说明性正文和章节标题尽量使用自然中文。

## 维护

重新合并中文译文：

```bash
python3 scripts/build_codex_zh_bundle.py
```

本地构建 Pages 站点：

```bash
python3 -m pip install mkdocs
mkdocs build
```

产品价格、模型名称、功能可用性和企业策略可能变化。更新时应先重新拉取官方
Codex manual，再同步翻译相应页面。
