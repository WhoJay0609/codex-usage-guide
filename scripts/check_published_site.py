#!/usr/bin/env python3
"""Read-only validation for a deployed copy of the guide."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]


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
    site_data_text = (ROOT / "assets/site-data.js").read_text(encoding="utf-8")
    match = re.search(r'"build_id":\s*"([^"]+)"', site_data_text)
    if not match:
        print("Cannot determine local build marker.")
        return 2
    expected_build = match.group(1)
    index_ok, html = _fetch(urljoin(base_url, "index.html"))
    assets = {path: _fetch(urljoin(base_url, path))[0] for path in ("assets/site.css", "assets/site.js", "assets/site-data.js", "assets/search-index.js")}
    errors = [] if index_ok else ["missing published page: index.html"]
    errors.extend(validate_snapshot(html, expected_build, assets))
    if errors:
        print("Published site check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Published site matches build {expected_build}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
