#!/usr/bin/env python3
"""Generate deterministic static assets without rewriting authored articles."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from html.parser import HTMLParser
from pathlib import Path

try:
    from .site_model import SiteModel, load_site_model
except ImportError:  # Direct script execution.
    from site_model import SiteModel, load_site_model


ROOT = Path(__file__).resolve().parents[1]
GENERATED_START = "<!-- guide:generated:start -->"
GENERATED_END = "<!-- guide:generated:end -->"


def replace_generated_block(source: str, generated: str) -> str:
    if source.count(GENERATED_START) != 1 or source.count(GENERATED_END) != 1:
        raise ValueError("generated content requires exactly one sentinel pair")
    before, remainder = source.split(GENERATED_START, 1)
    _, after = remainder.split(GENERATED_END, 1)
    return f"{before}{GENERATED_START}{generated}{GENERATED_END}{after}"


class HeadingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.section_ids: list[str] = []
        self.current_heading: dict[str, object] | None = None
        self.headings: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == "section":
            self.section_ids.append(attr.get("id") or "")
        if tag in {"h2", "h3"}:
            self.current_heading = {"level": tag, "id": attr.get("id") or next((value for value in reversed(self.section_ids) if value), ""), "text": []}

    def handle_endtag(self, tag: str) -> None:
        if tag in {"h2", "h3"} and self.current_heading:
            text = " ".join("".join(self.current_heading["text"]).split())
            if text:
                self.headings.append({"level": str(self.current_heading["level"]), "id": str(self.current_heading["id"]), "text": text})
            self.current_heading = None
        if tag == "section" and self.section_ids:
            self.section_ids.pop()

    def handle_data(self, data: str) -> None:
        if self.current_heading:
            self.current_heading["text"].append(data)


def _payloads(model: SiteModel) -> dict[Path, str]:
    source = {
        "site": model.site,
        "navigation": [{"label": group.label, "pages": list(group.pages)} for group in model.navigation],
        "pages": [page.__dict__ for page in model.pages],
        "changelog": list(model.changelog),
    }
    canonical = json.dumps(source, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    build_id = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:12]
    source["build_id"] = build_id

    search: list[dict[str, str]] = []
    for page in model.pages:
        parser = HeadingParser()
        parser.feed((model.root / page.path).read_text(encoding="utf-8"))
        search.append({"page": page.path, "title": page.title, "section": "", "fragment": "", "text": page.description})
        for heading in parser.headings:
            search.append({"page": page.path, "title": page.title, "section": heading["text"], "fragment": heading["id"], "text": heading["text"]})

    pretty_source = json.dumps(source, ensure_ascii=False, sort_keys=True, indent=2)
    pretty_search = json.dumps(search, ensure_ascii=False, sort_keys=True, indent=2)
    return {
        model.root / "assets/site-data.js": f"window.GUIDE_SITE_DATA = {pretty_source};\n",
        model.root / "assets/search-index.js": f"window.GUIDE_SEARCH_INDEX = {pretty_search};\n",
    }


def generate(root: Path = ROOT, check: bool = False) -> list[str]:
    model = load_site_model(root)
    stale: list[str] = []
    for path, expected in _payloads(model).items():
        actual = path.read_text(encoding="utf-8") if path.exists() else None
        if actual == expected:
            continue
        if check:
            stale.append(path.relative_to(root).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
    return stale


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated assets are stale")
    args = parser.parse_args()
    stale = generate(check=args.check)
    if stale:
        print("Generated site assets are stale:")
        for path in stale:
            print(f"- {path}")
        return 1
    print("Generated site assets are current." if args.check else "Generated site assets updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
