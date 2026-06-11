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
EN_BUNDLE = ROOT / "docs" / "source" / "codex-manual.en.md"
OUTLINE = ROOT / "docs" / "source" / "codex-manual.outline.md"

LINK_RE = re.compile(r"(?<!!)\[((?:[^\]\\]|\\.)+?)\]\(([^)\s]+)([^)]*)\)", re.DOTALL)
BARE_CODEX_URL_RE = re.compile(
    r"(?<![\(])https://developers\.openai\.com/codex/[^\s<>)\"']+"
)
SOURCE_RE = re.compile(r"^Source:\s+\[[^\]]+\]\(([^)]+)\)", re.MULTILINE)
CODEX_ALIASES = {
    "guides/slash-commands": "39-slash-commands-in-codex-cli.md",
    "ide/cloud-tasks": "32-codex-ide-extension-features.md",
    "skills/create-skill": "48-agent-skills.md",
}

SECTIONS = [
    ("界面与模式", "Surfaces and Modes", 1, 4),
    ("执行模型与工作流", "Execution Model and Workflows", 5, 8),
    ("审批、沙盒与安全", "Approvals, Sandboxing, and Security", 9, 15),
    ("配置、认证与模型", "Configuration, Authentication, and Models", 16, 21),
    ("CLI、IDE、应用与云行为", "CLI, IDE, App, and Cloud Behavior", 22, 47),
    ("自定义、技能、规则、MCP 与集成", "Customization, Skills, Rules, MCP, and Integrations", 48, 56),
    ("非交互和编程接口", "Noninteractive and Programmatic Interfaces", 57, 61),
    ("平台、企业与注意事项", "Platform, Enterprise, and Caveats", 62, 83),
    ("补充官方链接页面", "Supplemental Official Linked Pages", 84, 87),
    ("官方站点、用例、集合与路线", "Official Site, Use Cases, Collections, and Tracks", 88, 164),
]


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip("\"'")
    return meta, text[end + 5 :]


def title_from_page(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    meta, body = split_front_matter(text)
    if meta.get("title"):
        return meta["title"]

    for line in body.splitlines():
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
        if not parsed.scheme and not parsed.netloc and parsed.path.startswith("/"):
            return f"[{label}](https://developers.openai.com{target}{title})"
        return match.group(0)

    return LINK_RE.sub(replace_link, text)


def localize_bare_codex_urls(text: str, current_file: Path, link_map: dict[str, Path]) -> str:
    def replace_url(match: re.Match[str]) -> str:
        if starts_on_source_line(text, match.start()):
            return match.group(0)

        target = match.group(0)
        parsed = urlsplit(target)
        for key in codex_keys(target):
            local_target = link_map.get(key)
            if local_target:
                title = title_from_page(local_target)
                replacement = relative_link(local_target, current_file, parsed.fragment)
                return f"[{title}]({replacement})"
        return target

    return BARE_CODEX_URL_RE.sub(replace_url, text)


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


def line_number(lines: list[str], needle: str, start: int = 0) -> int:
    for index in range(start, len(lines)):
        if lines[index] == needle:
            return index + 1
    raise ValueError(f"cannot find line: {needle}")


def write_english_bundle(source_pages: list[Path]) -> None:
    sectioned_pages = []
    for _section_zh, section_en, start, end in SECTIONS:
        section_pages = [p for p in source_pages if start <= page_number(p) <= end]
        sectioned_pages.append((section_en, section_pages))

    parts = [
        "# Codex Official Documentation English Snapshot\n\n",
        "> Generated from `docs/source/pages/`. Chinese translations live in `docs/zh/pages/`.\n\n",
        "## Contents\n\n",
    ]
    for section, section_pages in sectioned_pages:
        parts.append(f"### {section}\n\n")
        for page in section_pages:
            title = title_from_page(page)
            rel = page.relative_to(EN_BUNDLE.parent)
            parts.append(f"- [{title}]({rel.as_posix()})\n")
        parts.append("\n")

    parts.append("---\n\n")
    for section, section_pages in sectioned_pages:
        parts.append(f"## {section}\n\n")
        for page in section_pages:
            parts.append(page.read_text(encoding="utf-8").strip())
            parts.append("\n\n")

    text = "".join(parts).rstrip() + "\n"
    EN_BUNDLE.write_text(text, encoding="utf-8")
    write_outline(text, sectioned_pages)


def write_outline(bundle_text: str, sectioned_pages: list[tuple[str, list[Path]]]) -> None:
    lines = bundle_text.splitlines()
    outline_lines = ["# Codex Official Documentation Outline\n"]
    cursor = 0
    for index, (section, section_pages) in enumerate(sectioned_pages):
        if not section_pages:
            continue
        section_start = line_number(lines, f"## {section}", cursor) 
        next_section_start = None
        for later_section, later_pages in sectioned_pages[index + 1 :]:
            if later_pages:
                next_section_start = line_number(lines, f"## {later_section}", section_start)
                break
        section_end = (next_section_start - 1) if next_section_start else len(lines)
        outline_lines.append(f"- {section} (lines {section_start}-{section_end})\n")

        page_cursor = section_start
        page_starts = []
        for page in section_pages:
            title = title_from_page(page)
            page_start = line_number(lines, f"### {title}", page_cursor)
            page_starts.append((title, page_start))
            page_cursor = page_start
        for page_index, (title, page_start) in enumerate(page_starts):
            page_end = (
                page_starts[page_index + 1][1] - 1
                if page_index + 1 < len(page_starts)
                else section_end
            )
            outline_lines.append(f"  - {title} (lines {page_start}-{page_end})\n")
        cursor = section_end

    OUTLINE.write_text("".join(outline_lines), encoding="utf-8")


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
        localized = localize_bare_codex_urls(localized, page, link_map)
        if localized != text:
            page.write_text(localized, encoding="utf-8")
            normalized_count += 1

    sectioned_pages = []
    for section_zh, _section_en, start, end in SECTIONS:
        section_pages = [p for p in pages if start <= page_number(p) <= end]
        sectioned_pages.append((section_zh, section_pages))

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
        _meta, text = split_front_matter(text)
        text = text.strip()
        text = retarget_local_page_links(text, page, BUNDLE)
        if not text.startswith("### "):
            text = f"### {title_from_page(page)}\n\n{text}"
        bundle_parts.append(text)
        bundle_parts.append("\n\n")

    INDEX.write_text("".join(index_lines), encoding="utf-8")
    BUNDLE.write_text("".join(bundle_parts).rstrip() + "\n", encoding="utf-8")
    write_english_bundle(source_pages)
    SITE_INDEX.write_text(
        """<div class="codex-home">
  <section class="codex-hero">
    <p class="codex-kicker">OpenAI Developers / Codex</p>
    <h1>Codex</h1>
    <p class="codex-tagline">一个可以在所有编码场景中协作的智能体。</p>
    <p class="codex-intro">
      这里是 OpenAI Codex 官方文档的简体中文翻译站点，覆盖官方文档、使用场景、集合、路线和更新日志。
    </p>
    <div class="codex-actions">
      <a class="codex-button codex-button-primary" href="zh/README.md">开始阅读</a>
      <a class="codex-button" href="codex-manual.zh.md">打开中文合订版</a>
    </div>
  </section>

  <section class="codex-product">
    <div class="codex-summary">
      <p>
        Codex 是 OpenAI 面向软件开发的 coding agent。它可以帮助你：
      </p>
      <ul class="codex-feature-list">
        <li><strong>编写代码：</strong>描述你想构建什么，Codex 会生成符合项目结构和约定的代码。</li>
        <li><strong>理解代码库：</strong>阅读并解释复杂或遗留系统，帮助你快速把握组织方式。</li>
        <li><strong>审查代码：</strong>分析变更，发现潜在 bug、逻辑错误和未处理的边界情况。</li>
        <li><strong>调试和修复：</strong>追踪失败、诊断根因，并提出有针对性的修复。</li>
        <li><strong>自动化任务：</strong>运行 refactor、测试、迁移和设置等重复开发工作流。</li>
      </ul>
    </div>
    <figure class="codex-showcase" aria-label="Codex app preview">
      <img class="codex-showcase-light" src="https://developers.openai.com/images/codex/app/codex-app-basic-light.webp" alt="Codex app showing a project sidebar, thread list, and review pane" loading="lazy">
      <img class="codex-showcase-dark" src="https://developers.openai.com/images/codex/app/codex-app-basic-dark.webp" alt="Codex app showing a project sidebar, thread list, and review pane" loading="lazy">
    </figure>
  </section>

  <section class="codex-card-grid" aria-label="Reading entry points">
    <a class="codex-card" href="zh/README.md">
      <span class="codex-card-label">Docs</span>
      <strong>中文分页目录</strong>
      <span>按官方章节分组，适合逐页阅读和跳转。</span>
    </a>
    <a class="codex-card" href="codex-manual.zh.md">
      <span class="codex-card-label">Manual</span>
      <strong>中文合订版</strong>
      <span>单文件完整译文，适合全文搜索和离线保存。</span>
    </a>
    <a class="codex-card" href="source/codex-manual.en.md">
      <span class="codex-card-label">Snapshot</span>
      <strong>英文官方快照</strong>
      <span>翻译所依据的官方 Codex manual 聚合快照。</span>
    </a>
    <a class="codex-card" href="source/codex-manual.outline.md">
      <span class="codex-card-label">Outline</span>
      <strong>官方快照目录轮廓</strong>
      <span>英文快照的章节索引和行号定位。</span>
    </a>
  </section>

  <section class="codex-note">
    中文译文保留产品名、命令、配置键、模型名和必要 UI 标签的英文写法；说明性正文和章节标题尽量使用自然中文。产品价格、模型名称、功能可用性和企业策略可能变化，需要最新信息时请以官方文档为准。
  </section>
</div>
""",
        encoding="utf-8",
    )
    print(f"wrote {SITE_INDEX}")
    print(f"wrote {INDEX}")
    print(f"wrote {BUNDLE}")
    print(f"wrote {EN_BUNDLE}")
    print(f"wrote {OUTLINE}")
    if normalized_count:
        print(f"normalized local Codex links in {normalized_count} translated pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
