#!/usr/bin/env python3
"""Build the Chinese Codex manual bundle from translated page files."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGES_DIR = ROOT / "docs" / "zh" / "pages"
SOURCE_DIR = ROOT / "docs" / "source" / "pages"
BUNDLE = ROOT / "docs" / "codex-manual.zh.md"
INDEX = ROOT / "docs" / "zh" / "README.md"
DOCS_INDEX = ROOT / "docs" / "README.md"

SECTIONS = [
    ("界面与模式", 1, 4),
    ("执行模型与工作流", 5, 8),
    ("审批、沙盒与安全", 9, 15),
    ("配置、认证与模型", 16, 21),
    ("CLI、IDE、应用与云行为", 22, 47),
    ("自定义、技能、规则、MCP 与集成", 48, 56),
    ("非交互和编程接口", 57, 61),
    ("平台、企业与注意事项", 62, 83),
]


def title_from_page(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            return line[4:].strip()
    return path.stem


def page_number(path: Path) -> int:
    match = re.match(r"(\d+)-", path.name)
    if not match:
        return 9999
    return int(match.group(1))


def main() -> int:
    pages = sorted(PAGES_DIR.glob("*.md"), key=page_number)
    source_pages = sorted(SOURCE_DIR.glob("*.md"), key=page_number)
    missing = sorted({p.name for p in source_pages} - {p.name for p in pages})
    if missing:
        raise SystemExit("Missing translated pages:\n" + "\n".join(missing))

    sectioned_pages = []
    for section, start, end in SECTIONS:
        section_pages = [p for p in pages if start <= page_number(p) <= end]
        sectioned_pages.append((section, section_pages))

    bundle_parts = [
        "# Codex 官方文档中文翻译\n\n",
        "> 本文件由 `docs/zh/pages/` 下的逐页译文合并生成。官方英文快照见 `docs/source/`。\n\n",
        "## 目录\n\n",
    ]
    index_lines = [
        "# Codex 官方文档中文翻译\n\n",
        "本目录按官方 Codex manual 的页面片段提供简体中文译文，适合在 GitHub 上逐页阅读。\n\n",
        "- [中文合订版](../codex-manual.zh.md)\n",
        "- [英文官方快照](../source/codex-manual.en.md)\n",
        "- [官方快照目录轮廓](../source/codex-manual.outline.md)\n\n",
        "## 分组目录\n\n",
    ]

    for section, section_pages in sectioned_pages:
        index_lines.append(f"### {section}\n\n")
        bundle_parts.append(f"### {section}\n\n")
        for page in section_pages:
            title = title_from_page(page)
            rel = page.relative_to(INDEX.parent)
            bundle_parts.append(f"- [{title}](zh/{rel.as_posix()})\n")
            index_lines.append(f"- [{title}]({rel.as_posix()})\n")
        bundle_parts.append("\n")
        index_lines.append("\n")

    bundle_parts.append("---\n\n")

    for page in pages:
        text = page.read_text(encoding="utf-8").strip()
        bundle_parts.append(text)
        bundle_parts.append("\n\n")

    INDEX.write_text("".join(index_lines), encoding="utf-8")
    BUNDLE.write_text("".join(bundle_parts).rstrip() + "\n", encoding="utf-8")
    DOCS_INDEX.write_text(
        "# Codex 文档\n\n"
        "本目录包含 OpenAI Codex 官方文档英文快照和简体中文译文。\n\n"
        "- [中文分页目录](zh/README.md)\n"
        "- [中文合订版](codex-manual.zh.md)\n"
        "- [英文官方快照](source/codex-manual.en.md)\n"
        "- [官方快照目录轮廓](source/codex-manual.outline.md)\n",
        encoding="utf-8",
    )
    print(f"wrote {DOCS_INDEX}")
    print(f"wrote {INDEX}")
    print(f"wrote {BUNDLE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
