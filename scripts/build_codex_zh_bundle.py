#!/usr/bin/env python3
"""Build the Chinese Codex manual bundle from translated page files."""

from __future__ import annotations

import re
import os
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
PAGES_DIR = ROOT / "docs" / "zh" / "pages"
SOURCE_DIR = ROOT / "docs" / "source" / "pages"
BUNDLE = ROOT / "docs" / "codex-manual.zh.md"
INDEX = ROOT / "docs" / "zh" / "README.md"
SITE_INDEX = ROOT / "docs" / "index.md"

LINK_RE = re.compile(r"(?<!!)\[((?:[^\]\\]|\\.)+?)\]\(([^)\s]+)([^)]*)\)", re.DOTALL)
SOURCE_RE = re.compile(r"^Source:\s+\[[^\]]+\]\(([^)]+)\)", re.MULTILINE)
CODEX_ALIASES = {
    "guides/slash-commands": "39-slash-commands-in-codex-cli.md",
    "ide/cloud-tasks": "32-codex-ide-extension-features.md",
}

SECTIONS = [
    ("界面与模式", 1, 4),
    ("执行模型与工作流", 5, 8),
    ("审批、沙盒与安全", 9, 15),
    ("配置、认证与模型", 16, 21),
    ("CLI、IDE、应用与云行为", 22, 47),
    ("自定义、技能、规则、MCP 与集成", 48, 56),
    ("非交互和编程接口", 57, 61),
    ("平台、企业与注意事项", 62, 83),
    ("补充官方链接页面", 84, 87),
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


def codex_keys(url: str) -> list[str]:
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme not in {"http", "https"}:
            return []
        if parsed.netloc != "developers.openai.com":
            return []

    path = parsed.path
    if not path.startswith("/codex"):
        return []

    rest = path.removeprefix("/codex").strip("/")
    if rest.endswith(".md"):
        rest = rest[:-3]

    keys = [rest]
    if rest.endswith("/index"):
        keys.append(rest.removesuffix("/index"))
    if rest == "overview":
        keys.append("")
    return [key for key in keys if key]


def relative_link(target: Path, current_file: Path, fragment: str = "") -> str:
    rel = os.path.relpath(target, current_file.parent).replace(os.sep, "/")
    return f"{rel}#{fragment}" if fragment else rel


def build_codex_link_map(source_pages: list[Path]) -> dict[str, Path]:
    link_map: dict[str, Path] = {}
    for source_page in source_pages:
        match = SOURCE_RE.search(source_page.read_text(encoding="utf-8"))
        if not match:
            continue
        translated_page = PAGES_DIR / source_page.name
        for key in codex_keys(match.group(1)):
            link_map.setdefault(key, translated_page)
    for key, filename in CODEX_ALIASES.items():
        link_map.setdefault(key, PAGES_DIR / filename)
    return link_map


def starts_on_source_line(text: str, index: int) -> bool:
    line_start = text.rfind("\n", 0, index) + 1
    return text.startswith("Source: ", line_start)


def localize_codex_links(text: str, current_file: Path, link_map: dict[str, Path]) -> str:
    def replace_link(match: re.Match[str]) -> str:
        if starts_on_source_line(text, match.start()):
            return match.group(0)

        label, target, title = match.groups()
        parsed = urlsplit(target)
        for key in codex_keys(target):
            local_target = link_map.get(key)
            if local_target:
                replacement = relative_link(local_target, current_file, parsed.fragment)
                return f"[{label}]({replacement}{title})"
        return match.group(0)

    return LINK_RE.sub(replace_link, text)


def retarget_local_page_links(text: str, source_file: Path, output_file: Path) -> str:
    def replace_link(match: re.Match[str]) -> str:
        if starts_on_source_line(text, match.start()):
            return match.group(0)

        label, target, title = match.groups()
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            return match.group(0)

        target_path = (source_file.parent / parsed.path).resolve()
        try:
            target_path.relative_to(PAGES_DIR.resolve())
        except ValueError:
            return match.group(0)
        if not target_path.exists():
            return match.group(0)

        replacement = relative_link(target_path, output_file, parsed.fragment)
        return f"[{label}]({replacement}{title})"

    return LINK_RE.sub(replace_link, text)


def main() -> int:
    pages = sorted(PAGES_DIR.glob("*.md"), key=page_number)
    source_pages = sorted(SOURCE_DIR.glob("*.md"), key=page_number)
    missing = sorted({p.name for p in source_pages} - {p.name for p in pages})
    if missing:
        raise SystemExit("Missing translated pages:\n" + "\n".join(missing))

    link_map = build_codex_link_map(source_pages)
    normalized_count = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        localized = localize_codex_links(text, page, link_map)
        if localized != text:
            page.write_text(localized, encoding="utf-8")
            normalized_count += 1

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
        text = retarget_local_page_links(text, page, BUNDLE)
        bundle_parts.append(text)
        bundle_parts.append("\n\n")

    INDEX.write_text("".join(index_lines), encoding="utf-8")
    BUNDLE.write_text("".join(bundle_parts).rstrip() + "\n", encoding="utf-8")
    SITE_INDEX.write_text(
        "# Codex 官方文档中文翻译\n\n"
        "这里是 OpenAI Codex 官方文档的简体中文翻译站点。\n\n"
        "## 阅读入口\n\n"
        "- [中文分页目录](zh/README.md)：按官方章节分组，适合逐页阅读。\n"
        "- [中文合订版](codex-manual.zh.md)：单文件完整译文，适合全文搜索。\n"
        "- [英文官方快照](source/codex-manual.en.md)：翻译所依据的官方 Codex manual 聚合快照。\n"
        "- [官方快照目录轮廓](source/codex-manual.outline.md)：英文快照的章节索引。\n\n"
        "## 说明\n\n"
        "中文译文保留产品名、命令、配置键、模型名和必要 UI 标签的英文写法；"
        "说明性正文和章节标题尽量使用自然中文。产品价格、模型名称、功能可用性"
        "和企业策略可能变化，需要最新信息时请以官方文档为准。\n",
        encoding="utf-8",
    )
    print(f"wrote {SITE_INDEX}")
    print(f"wrote {INDEX}")
    print(f"wrote {BUNDLE}")
    if normalized_count:
        print(f"normalized local Codex links in {normalized_count} translated pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
