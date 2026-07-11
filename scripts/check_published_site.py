#!/usr/bin/env python3
"""Read-only validation for a deployed copy of the guide."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]


class HeadMetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title: list[str] = []
        self.in_title = False
        self.metas: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            self.metas.append(attr)
        elif tag == "link":
            self.links.append(attr)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title.append(data)


def validate_page_metadata(
    html: str,
    title: str,
    description: str,
    canonical: str,
    preview: str,
) -> list[str]:
    parser = HeadMetadataParser()
    parser.feed(html)
    errors: list[str] = []
    if "".join(parser.title).strip() != title:
        errors.append(f"published title does not match {title}")
    canonical_links = [item.get("href", "") for item in parser.links if item.get("rel") == "canonical"]
    if canonical_links != [canonical]:
        errors.append(f"published canonical does not match {canonical}")
    expected = {
        ("name", "description"): description,
        ("property", "og:title"): title,
        ("property", "og:description"): description,
        ("property", "og:url"): canonical,
        ("property", "og:image"): preview,
        ("name", "twitter:card"): "summary_large_image",
        ("name", "twitter:title"): title,
        ("name", "twitter:description"): description,
        ("name", "twitter:image"): preview,
    }
    for (key, name), value in expected.items():
        actual = [item.get("content", "") for item in parser.metas if item.get(key) == name]
        if actual != [value]:
            errors.append(f"published metadata {name} does not match")
    return errors


def validate_snapshot(html: str, expected_build: str, assets: dict[str, bool]) -> list[str]:
    errors: list[str] = []
    marker = re.search(r'<meta\s+name=["\']guide-build["\']\s+content=["\']([^"\']+)', html)
    if not marker or marker.group(1) != expected_build:
        errors.append(f"published build marker does not match {expected_build}")
    for path, exists in assets.items():
        if not exists:
            errors.append(f"missing published asset: {path}")
    return errors


def _fetch(url: str) -> tuple[bool, str]:
    request = Request(url, headers={"User-Agent": "codex-usage-guide-check/1"})
    try:
        with urlopen(request, timeout=15) as response:
            return response.status == 200, response.read().decode("utf-8", errors="replace")
    except (HTTPError, URLError, TimeoutError):
        return False, ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    args = parser.parse_args()
    if not args.base_url.startswith(("http://", "https://")):
        parser.error("--base-url must be an HTTP(S) URL")
    base_url = args.base_url.rstrip("/") + "/"
    manifest = json.loads((ROOT / "data/site-manifest.json").read_text(encoding="utf-8"))
    configured_base = manifest["site"]["base_url"]
    preview_path = manifest["site"]["social_preview"]
    preview_url = urljoin(configured_base, preview_path)
    site_data_text = (ROOT / "assets/site-data.js").read_text(encoding="utf-8")
    match = re.search(r'"build_id":\s*"([^"]+)"', site_data_text)
    if not match:
        print("Cannot determine local build marker.")
        return 2
    expected_build = match.group(1)
    published_pages = {item["path"]: _fetch(urljoin(base_url, item["path"])) for item in manifest["pages"]}
    index_ok, html = published_pages["index.html"]
    assets = {path: _fetch(urljoin(base_url, path))[0] for path in ("assets/site.css", "assets/site.js", "assets/site-data.js", "assets/search-index.js", preview_path)}
    errors = [] if index_ok else ["missing published page: index.html"]
    errors.extend(validate_snapshot(html, expected_build, assets))
    for item in manifest["pages"]:
        ok, page_html = published_pages[item["path"]]
        if not ok:
            errors.append(f"missing published page: {item['path']}")
            continue
        errors.extend(
            validate_page_metadata(
                page_html,
                item["title"],
                item["description"],
                urljoin(configured_base, item["path"]),
                preview_url,
            )
        )
    if errors:
        print("Published site check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Published site matches build {expected_build}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
