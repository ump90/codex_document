#!/usr/bin/env python3
"""Audit local Codex docs coverage against the official developers sitemap."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "docs" / "source" / "pages"
ZH_DIR = ROOT / "docs" / "zh" / "pages"
SITEMAP_INDEX_URL = "https://developers.openai.com/sitemap-index.xml"
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

SOURCE_RE = re.compile(r"^Source:\s+\[[^\]]+\]\(([^)]+)\)", re.MULTILINE)
CODEX_ALIASES = {
    "guides/slash-commands": "39-slash-commands-in-codex-cli.md",
    "ide/cloud-tasks": "32-codex-ide-extension-features.md",
}


def fetch_xml(url: str) -> ElementTree.Element:
    request = Request(url, headers={"User-Agent": "Codex docs sitemap audit"})
    with urlopen(request, timeout=30) as response:
        return ElementTree.fromstring(response.read())


def codex_key_from_path(path: str) -> str | None:
    path = path.rstrip("/")
    if path == "/codex":
        return ""
    if not path.startswith("/codex/"):
        return None

    key = path.removeprefix("/codex/")
    if key.endswith(".md"):
        key = key[:-3]
    if key == "overview":
        return ""
    if key.endswith("/index"):
        return key.removesuffix("/index")
    return key


def codex_key_from_url(url: str) -> str | None:
    return codex_key_from_path(urlsplit(url).path)


def sitemap_urls() -> list[str]:
    index = fetch_xml(SITEMAP_INDEX_URL)
    sitemap_locs = [element.text for element in index.findall(f".//{SITEMAP_NS}loc")]
    urls: list[str] = []
    for sitemap in sitemap_locs:
        if not sitemap:
            continue
        root = fetch_xml(sitemap)
        for element in root.findall(f".//{SITEMAP_NS}loc"):
            if element.text and urlsplit(element.text).path.startswith("/codex"):
                urls.append(element.text.rstrip("/"))
    return sorted(set(urls))


def local_source_keys() -> dict[str, Path]:
    keys: dict[str, Path] = {"": SOURCE_DIR / "01-codex.md"}
    for page in sorted(SOURCE_DIR.glob("*.md")):
        text = page.read_text(encoding="utf-8")
        match = SOURCE_RE.search(text)
        if not match:
            continue
        key = codex_key_from_url(match.group(1))
        if key is not None:
            keys.setdefault(key, page)
    for key, filename in CODEX_ALIASES.items():
        keys.setdefault(key, SOURCE_DIR / filename)
    return keys


def category_for(key: str) -> str:
    if key.startswith("use-cases/collections"):
        return "use-cases/collections"
    if key.startswith("use-cases"):
        return "use-cases"
    if key.startswith("tracks"):
        return "tracks"
    if "/" in key:
        return key.split("/", 1)[0]
    return key or "root"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Report missing sitemap URLs but exit successfully.",
    )
    args = parser.parse_args()

    urls = sitemap_urls()
    sitemap_by_key = {
        key: url
        for url in urls
        if (key := codex_key_from_url(url)) is not None
    }
    local_keys = local_source_keys()

    missing = [
        (key, url)
        for key, url in sorted(sitemap_by_key.items(), key=lambda item: item[1])
        if key not in local_keys
    ]
    untranslated = sorted(
        page.name for page in SOURCE_DIR.glob("*.md") if not (ZH_DIR / page.name).exists()
    )
    extras = sorted(key for key in local_keys if key not in sitemap_by_key)

    print(f"official_codex_urls={len(urls)}")
    print(f"local_source_keys={len(local_keys)}")
    print(f"missing_from_repo={len(missing)}")
    print(f"missing_translations={len(untranslated)}")
    print(f"local_not_in_sitemap={len(extras)}")

    if missing:
        grouped: dict[str, list[str]] = defaultdict(list)
        for key, url in missing:
            grouped[category_for(key)].append(url)
        for category in sorted(grouped):
            print(f"\n## {category} ({len(grouped[category])})")
            for url in grouped[category]:
                print(url)

    if untranslated:
        print("\n## missing translated pages")
        for filename in untranslated:
            print(filename)

    if extras:
        print("\n## local source keys not present in sitemap")
        for key in extras:
            print(f"/codex/{key}" if key else "/codex")

    if (missing or untranslated) and not args.allow_missing:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
