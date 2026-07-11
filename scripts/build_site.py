#!/usr/bin/env python3
"""Generate deterministic static assets without rewriting authored articles."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

try:
    from .site_model import Page, SiteModel, load_site_model
except ImportError:  # Direct script execution.
    from site_model import Page, SiteModel, load_site_model


ROOT = Path(__file__).resolve().parents[1]
GENERATED_START = "<!-- guide:generated:start -->"
GENERATED_END = "<!-- guide:generated:end -->"


def replace_generated_block(source: str, generated: str) -> str:
    if source.count(GENERATED_START) != 1 or source.count(GENERATED_END) != 1:
        raise ValueError("generated content requires exactly one sentinel pair")
    before, remainder = source.split(GENERATED_START, 1)
    _, after = remainder.split(GENERATED_END, 1)
    return f"{before}{GENERATED_START}{generated}{GENERATED_END}{after}"


def _markers(name: str) -> tuple[str, str]:
    return f"<!-- guide:{name}:start -->", f"<!-- guide:{name}:end -->"


def _block(name: str, content: str) -> str:
    start, end = _markers(name)
    return f"{start}\n{content}\n{end}"


def _replace_named(source: str, name: str, content: str) -> str:
    start, end = _markers(name)
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if len(pattern.findall(source)) != 1:
        raise ValueError(f"generated block {name} requires exactly one sentinel pair")
    return pattern.sub(_block(name, content), source)


def _assign_heading_ids(source: str, page: Page) -> str:
    used = set(re.findall(r'\bid=["\']([^"\']+)', source))
    counter = 0

    def add_id(match: re.Match[str]) -> str:
        nonlocal counter
        level, attrs, body = match.groups()
        if re.search(r'\bid\s*=', attrs):
            return match.group(0)
        counter += 1
        candidate = f"heading-{Path(page.path).stem}-{counter}"
        while candidate in used:
            counter += 1
            candidate = f"heading-{Path(page.path).stem}-{counter}"
        used.add(candidate)
        return f'<h{level}{attrs} id="{candidate}">{body}</h{level}>'

    return re.sub(r"<h([23])(\b[^>]*)>(.*?)</h\1>", add_id, source, flags=re.DOTALL | re.IGNORECASE)


def _headings(source: str) -> list[dict[str, str]]:
    parser = HeadingParser()
    parser.feed(source)
    return parser.headings


def _article_headings(source: str) -> list[dict[str, str]]:
    match = re.search(r"<main\b.*?</main>", source, flags=re.DOTALL | re.IGNORECASE)
    return _headings(match.group(0) if match else source)


def render_page(model: SiteModel, page: Page, source: str) -> str:
    """Render generated chrome around authored page content."""
    source = _assign_heading_ids(source, page)
    page_map = {item.path: item for item in model.pages}
    flat_order = [path for group in model.navigation for path in group.pages]
    current_index = flat_order.index(page.path)

    nav_groups: list[str] = []
    for group in model.navigation:
        links = []
        for path in group.pages:
            target = page_map[path]
            current = ' aria-current="page"' if path == page.path else ""
            links.append(f'<a data-nav href="{html.escape(path)}"{current}>{html.escape(target.nav_label)}</a>')
        nav_groups.append(f'<section class="global-nav-group"><strong>{html.escape(group.label)}</strong>{"".join(links)}</section>')
    global_nav = '<aside class="global-nav" id="global-nav" aria-label="全站导航">' + "".join(nav_groups) + "</aside>"

    toc_links = []
    for heading in _article_headings(source):
        if not heading["id"]:
            continue
        toc_links.append(f'<a class="toc-{heading["level"]}" href="#{html.escape(heading["id"])}">{html.escape(heading["text"])}</a>')
    toc = '<aside class="page-toc" aria-label="本页目录"><details open><summary>本页目录</summary><nav>' + "".join(toc_links) + "</nav></details></aside>"

    previous_link = ""
    next_link = ""
    if current_index:
        previous = page_map[flat_order[current_index - 1]]
        previous_link = f'<a rel="prev" href="{previous.path}">← {html.escape(previous.nav_label)}</a>'
    if current_index + 1 < len(flat_order):
        following = page_map[flat_order[current_index + 1]]
        next_link = f'<a rel="next" href="{following.path}">{html.escape(following.nav_label)} →</a>'

    header = (
        '<header class="topbar"><div class="topbar-inner">'
        '<a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true"></span><span>Codex 使用指南</span></a>'
        '<div class="topbar-actions"><span class="search-status">全站搜索将在下一阶段启用</span>'
        '<button class="menu-toggle" type="button" aria-controls="global-nav" aria-expanded="false">目录</button></div>'
        '</div></header>'
    )
    shell_open = (
        '<div class="toolbook-shell">' + global_nav + '<div class="toolbook-main">'
        f'<nav class="breadcrumbs" aria-label="面包屑"><a href="index.html">首页</a><span aria-hidden="true">/</span><span>{html.escape(page.nav_label)}</span></nav>'
        f'<div class="page-freshness"><span>页面更新：<time datetime="{page.modified}">{page.modified}</time></span>'
        f'<span>事实核验：<time datetime="{page.facts_verified}">{page.facts_verified}</time></span></div>'
    )
    shell_close = f'<nav class="page-sequence" aria-label="前后页">{previous_link}{next_link}</nav></div>{toc}</div>'

    header_pattern = re.compile(r'<header\s+class=["\']topbar["\'].*?</header>', re.DOTALL)
    if _markers("header")[0] in source:
        source = _replace_named(source, "header", header)
    else:
        source, count = header_pattern.subn(_block("header", header), source, count=1)
        if count != 1:
            raise ValueError(f"{page.path}: expected one topbar header")

    source = re.sub(r'<aside\s+class=["\']side-nav["\'].*?</aside>', "", source, flags=re.DOTALL)
    if _markers("shell-open")[0] in source:
        source = _replace_named(source, "shell-open", shell_open)
        source = _replace_named(source, "shell-close", shell_close)
    else:
        source, count = re.subn(r"(?=<main\b)", _block("shell-open", shell_open) + "\n", source, count=1)
        if count != 1 or "</main>" not in source:
            raise ValueError(f"{page.path}: expected one main region")
        before, after = source.rsplit("</main>", 1)
        source = before + "</main>\n" + _block("shell-close", shell_close) + after
    return source


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
            self.current_heading = {"level": tag, "id": next((value for value in reversed(self.section_ids) if value), "") or attr.get("id") or "", "text": []}

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
    for page in model.pages:
        path = root / page.path
        actual = path.read_text(encoding="utf-8")
        expected = render_page(model, page, actual)
        if actual == expected:
            continue
        if check:
            stale.append(page.path)
        else:
            path.write_text(expected, encoding="utf-8")
    if not check:
        model = load_site_model(root)
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
