#!/usr/bin/env python3
"""Read-only validation for a deployed copy of the guide."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
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
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if attr.get("id"):
            self.ids.add(attr["id"])
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


def validate_published_page(html: str, expected_build: str, fragments: list[str]) -> list[str]:
    errors = validate_snapshot(html, expected_build, {})
    parser = HeadMetadataParser()
    parser.feed(html)
    for fragment in fragments:
        if fragment not in parser.ids:
            errors.append(f"published page is missing fragment #{fragment}")
    return errors


def validate_published_asset(
    path: str,
    ok: bool,
    content_type: str,
    body: bytes,
    expected_content_type: str,
    local_body: bytes,
) -> list[str]:
    if not ok:
        return [f"missing published asset: {path}"]
    errors: list[str] = []
    if expected_content_type not in content_type.lower():
        errors.append(f"published asset has wrong content type: {path} ({content_type or 'missing'})")
    if body != local_body:
        errors.append(f"published asset content fingerprint differs from local: {path}")
    return errors


@dataclass(frozen=True)
class FetchResult:
    ok: bool
    content_type: str
    body: bytes


def _fetch(url: str) -> FetchResult:
    request = Request(url, headers={"User-Agent": "codex-usage-guide-check/1"})
    try:
        with urlopen(request, timeout=15) as response:
            return FetchResult(
                response.status == 200,
                response.headers.get("Content-Type", ""),
                response.read(),
            )
    except (HTTPError, URLError, TimeoutError):
        return FetchResult(False, "", b"")


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
    site_data_path = ROOT / "assets/site-data.js"
    site_data_bytes = site_data_path.read_bytes()
    site_data_text = site_data_bytes.decode("utf-8")
    match = re.search(r'"build_id":\s*"([^"]+)"', site_data_text)
    if not match:
        print("Cannot determine local build marker.")
        return 2
    expected_build = match.group(1)
    data_match = re.search(r"window\.GUIDE_SITE_DATA\s*=\s*(\{.*\});\s*$", site_data_text, re.DOTALL)
    if not data_match:
        print("Cannot parse local site data.")
        return 2
    site_data = json.loads(data_match.group(1))
    errors: list[str] = []
    for item in manifest["pages"]:
        path = item["path"]
        result = _fetch(urljoin(base_url, path))
        errors.extend(
            validate_published_asset(
                path,
                result.ok,
                result.content_type,
                result.body,
                "text/html",
                (ROOT / path).read_bytes(),
            )
        )
        if not result.ok:
            continue
        page_html = result.body.decode("utf-8", errors="replace")
        errors.extend(validate_published_page(page_html, expected_build, site_data["fragments"][path]))
        errors.extend(
            validate_page_metadata(
                page_html,
                item["title"],
                item["description"],
                urljoin(configured_base, item["path"]),
                preview_url,
            )
        )
    asset_types = {
        "assets/site.css": "text/css",
        "assets/site.js": "javascript",
        "assets/theme.js": "javascript",
        "assets/site-data.js": "javascript",
        "assets/search-index.js": "javascript",
        preview_path: "image/png",
    }
    for path, content_type in asset_types.items():
        result = _fetch(urljoin(base_url, path))
        errors.extend(
            validate_published_asset(
                path,
                result.ok,
                result.content_type,
                result.body,
                content_type,
                (ROOT / path).read_bytes(),
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
