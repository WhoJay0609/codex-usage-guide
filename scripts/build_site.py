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
from urllib.parse import urljoin, urlparse

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


def _read_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def load_heading_fragments(root: Path) -> dict[str, dict[str, dict[str, object]]]:
    path = root / "data/heading-fragments.json"
    data = _read_json(path)
    if data.get("schema_version") != 1 or not isinstance(data.get("pages"), dict):
        raise ValueError(f"{path}: expected schema_version 1 and pages object")
    pages = data["pages"]
    assert isinstance(pages, dict)
    normalized: dict[str, dict[str, dict[str, object]]] = {}
    for page, raw_entries in pages.items():
        if not isinstance(page, str) or not isinstance(raw_entries, dict):
            raise ValueError(f"{path}: invalid page fragment registry")
        entries: dict[str, dict[str, object]] = {}
        canonicals: set[str] = set()
        for identity, raw_entry in raw_entries.items():
            if not isinstance(identity, str) or not isinstance(raw_entry, dict):
                raise ValueError(f"{path}: invalid fragment entry for {page}")
            canonical = raw_entry.get("canonical")
            legacy = raw_entry.get("legacy", [])
            if not isinstance(canonical, str) or not canonical or not isinstance(legacy, list):
                raise ValueError(f"{path}: invalid fragment entry {page}#{identity}")
            if canonical in canonicals:
                raise ValueError(f"{path}: duplicate canonical fragment {page}#{canonical}")
            if any(not isinstance(value, str) or not value for value in legacy):
                raise ValueError(f"{path}: invalid legacy fragment {page}#{identity}")
            canonicals.add(canonical)
            entries[identity] = {"canonical": canonical, "legacy": list(dict.fromkeys(legacy))}
        normalized[page] = entries
    return normalized


def load_publication_policy(root: Path) -> dict[str, object]:
    path = root / "data/publication-policy.json"
    data = _read_json(path)
    if data.get("schema_version") != 1:
        raise ValueError(f"{path}: expected schema_version 1")
    if not isinstance(data.get("search"), dict) or not isinstance(data.get("sensitive_patterns"), list):
        raise ValueError(f"{path}: expected search and sensitive_patterns")
    for item in data["sensitive_patterns"]:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str) or not isinstance(item.get("pattern"), str):
            raise ValueError(f"{path}: invalid sensitive pattern")
        re.compile(item["pattern"])
    return data


def _fragment_lookup(entries: dict[str, dict[str, object]]) -> dict[str, dict[str, object]]:
    lookup: dict[str, dict[str, object]] = {}
    for identity, entry in entries.items():
        for value in [identity, str(entry["canonical"]), *[str(item) for item in entry["legacy"]]]:
            if value in lookup and lookup[value] is not entry:
                raise ValueError(f"fragment identity is ambiguous: {value}")
            lookup[value] = entry
    return lookup


ALIAS_RE = re.compile(
    r'<span\s+class=["\']fragment-alias["\'][^>]*data-canonical-fragment=["\'][^"\']+["\'][^>]*></span>\s*',
    re.IGNORECASE,
)
PERMALINK_RE = re.compile(
    r'<a\s+class=["\']heading-permalink["\'][^>]*data-heading-permalink[^>]*>.*?</a>',
    re.IGNORECASE | re.DOTALL,
)
EXTERNAL_INDICATOR_RE = re.compile(
    r'<span\s+class=["\']external-link-indicator["\'][^>]*>.*?</span>'
    r'(?:<span\s+class=["\']sr-only["\'][^>]*>.*?</span>)?',
    re.IGNORECASE | re.DOTALL,
)
RUNTIME_SCRIPT_RE = re.compile(
    r'\s*<script\b[^>]*src=["\'](?:https://cdn\.jsdelivr\.net/npm/(?:gsap|mermaid)[^"\']*|assets/site\.js)["\'][^>]*></script>',
    re.IGNORECASE,
)
MERMAID_SRC = "https://cdn.jsdelivr.net/npm/mermaid@11.14.0/dist/mermaid.min.js"
MERMAID_INTEGRITY = "sha384-1CMXl090wj8Dd6YfnzSQUOgWbE6suWCaenYG7pox5AX7apTpY3PmJMeS2oPql4Gk"
BUILD_PLACEHOLDER = "__GUIDE_BUILD__"
SKILL_REPOSITORY_NAV = (
    ("compound-engineering", "Compound Engineering"),
    ("mattpocock-skills", "Matt Pocock skills"),
    ("academic-research-skills-codex", "ARS"),
    ("aris-auto-claude-code-research-in-sleep", "ARIS"),
)


def _assign_heading_ids(
    source: str,
    page: Page,
    entries: dict[str, dict[str, object]] | None = None,
) -> str:
    source = PERMALINK_RE.sub("", ALIAS_RE.sub("", source))
    used = set(re.findall(r'\bid=["\']([^"\']+)', source))
    lookup = _fragment_lookup(entries or {})
    counter = 0

    def add_id(match: re.Match[str]) -> str:
        nonlocal counter
        level, attrs, body = match.groups()
        id_match = re.search(r'\bid\s*=\s*["\']([^"\']+)["\']', attrs)
        current = id_match.group(1) if id_match else ""
        entry = lookup.get(current)
        if entries is not None and entry is None:
            raise ValueError(f"{page.path}: unregistered h{level} fragment #{current or '(missing)'}")
        if entry is None:
            counter += 1
            candidate = f"heading-{Path(page.path).stem}-{counter}"
            while candidate in used:
                counter += 1
                candidate = f"heading-{Path(page.path).stem}-{counter}"
            if id_match:
                return match.group(0)
            used.add(candidate)
            return f'<h{level}{attrs} id="{candidate}">{body}</h{level}>'

        canonical = str(entry["canonical"])
        aliases = [str(value) for value in entry["legacy"] if str(value) != canonical]
        if current and current != canonical and current not in aliases:
            aliases.append(current)
        occupied = used - ({current} if current else set())
        collisions = [value for value in [canonical, *aliases] if value in occupied]
        if collisions:
            raise ValueError(f"{page.path}: fragment collides with structural target #{collisions[0]}")
        used.discard(current)
        used.add(canonical)
        used.update(aliases)
        if id_match:
            attrs = attrs[: id_match.start()] + f'id="{canonical}"' + attrs[id_match.end() :]
        else:
            attrs += f' id="{canonical}"'
        alias_markup = "".join(
            f'<span class="fragment-alias" id="{html.escape(alias)}" '
            f'data-canonical-fragment="{html.escape(canonical)}" aria-hidden="true"></span>'
            for alias in aliases
        )
        return f'{alias_markup}<h{level}{attrs}>{body}</h{level}>'

    return re.sub(r"<h([23])(\b[^>]*)>(.*?)</h\1>", add_id, source, flags=re.DOTALL | re.IGNORECASE)


def _add_heading_permalinks(source: str) -> str:
    anchor_depth = 0
    previous_end = 0

    def advance_anchor_depth(segment: str) -> None:
        nonlocal anchor_depth
        for tag in re.finditer(r"<(/?)a\b[^>]*>", segment, flags=re.IGNORECASE):
            if tag.group(1):
                anchor_depth = max(0, anchor_depth - 1)
            elif not tag.group(0).rstrip().endswith("/>"):
                anchor_depth += 1

    def add_permalink(match: re.Match[str]) -> str:
        nonlocal previous_end
        advance_anchor_depth(source[previous_end:match.start()])
        previous_end = match.end()
        level, attrs, body = match.groups()
        id_match = re.search(r'\bid\s*=\s*["\']([^"\']+)["\']', attrs)
        if not id_match or anchor_depth:
            return match.group(0)
        fragment = id_match.group(1)
        permalink = (
            f'<a class="heading-permalink" data-heading-permalink data-search-exclude '
            f'href="#{html.escape(fragment)}" aria-label="本节永久链接">'
            '<span aria-hidden="true">#</span></a>'
        )
        return f'<h{level}{attrs}>{body}{permalink}</h{level}>'

    return re.sub(
        r"<h([23])(\b[^>]*)>(.*?)</h\1>",
        add_permalink,
        source,
        flags=re.DOTALL | re.IGNORECASE,
    )


def _set_attribute(attrs: str, name: str, value: str) -> str:
    pattern = re.compile(rf'\s+{re.escape(name)}\s*=\s*["\'][^"\']*["\']', re.IGNORECASE)
    attrs = pattern.sub("", attrs)
    return f'{attrs} {name}="{html.escape(value, quote=True)}"'


def _decorate_external_links(source: str, base_url: str) -> str:
    base = urlparse(base_url)
    base_origin = (base.scheme.lower(), base.hostname or "", base.port)
    source = EXTERNAL_INDICATOR_RE.sub("", source)

    def decorate(match: re.Match[str]) -> str:
        attrs, body = match.groups()
        href_match = re.search(r'\bhref\s*=\s*["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        if not href_match:
            return match.group(0)
        target = urlparse(html.unescape(href_match.group(1)))
        if target.scheme.lower() not in {"http", "https"}:
            return match.group(0)
        target_origin = (target.scheme.lower(), target.hostname or "", target.port)
        if target_origin == base_origin:
            return match.group(0)
        class_match = re.search(r'\bclass\s*=\s*["\']([^"\']*)["\']', attrs, re.IGNORECASE)
        classes = class_match.group(1).split() if class_match else []
        if "external-link" not in classes:
            classes.append("external-link")
        attrs = _set_attribute(attrs, "class", " ".join(classes))
        attrs = _set_attribute(attrs, "target", "_blank")
        attrs = _set_attribute(attrs, "rel", "noopener noreferrer")
        attrs = _set_attribute(attrs, "referrerpolicy", "no-referrer")
        indicator = (
            '<span class="external-link-indicator" data-search-exclude aria-hidden="true">↗</span>'
            '<span class="sr-only" data-search-exclude>（外部链接）</span>'
        )
        return f"<a{attrs}>{indicator}{body}</a>"

    return re.sub(r"<a(\b[^>]*)>(.*?)</a>", decorate, source, flags=re.IGNORECASE | re.DOTALL)


def _render_metadata(source: str, model: SiteModel, page: Page) -> str:
    canonical = urljoin(model.site["base_url"], page.path)
    preview = urljoin(model.site["base_url"], model.site["social_preview"])
    locale = model.site["language"].replace("-", "_")
    values = {
        "title": html.escape(page.title, quote=True),
        "description": html.escape(page.description, quote=True),
        "canonical": html.escape(canonical, quote=True),
        "preview": html.escape(preview, quote=True),
        "site": html.escape(model.site["title"], quote=True),
        "locale": html.escape(locale, quote=True),
    }
    metadata = (
        f'<meta name="description" content="{values["description"]}">\n'
        f'<meta name="guide-build" content="{BUILD_PLACEHOLDER}">\n'
        '<link rel="icon" href="favicon.svg" type="image/svg+xml">\n'
        f'<link rel="canonical" href="{values["canonical"]}">\n'
        '<meta property="og:type" content="website">\n'
        f'<meta property="og:locale" content="{values["locale"]}">\n'
        f'<meta property="og:site_name" content="{values["site"]}">\n'
        f'<meta property="og:title" content="{values["title"]}">\n'
        f'<meta property="og:description" content="{values["description"]}">\n'
        f'<meta property="og:url" content="{values["canonical"]}">\n'
        f'<meta property="og:image" content="{values["preview"]}">\n'
        '<meta property="og:image:width" content="1200">\n'
        '<meta property="og:image:height" content="630">\n'
        f'<meta property="og:image:alt" content="{values["site"]}">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{values["title"]}">\n'
        f'<meta name="twitter:description" content="{values["description"]}">\n'
        f'<meta name="twitter:image" content="{values["preview"]}">\n'
        f'<meta name="twitter:image:alt" content="{values["site"]}">'
    )
    description_pattern = re.compile(
        r'\s*<meta\s+name=["\']description["\']\s+content=["\'][^"\']*["\']\s*/?>',
        re.IGNORECASE,
    )
    if _markers("metadata")[0] in source:
        start, end = _markers("metadata")
        before, remainder = source.split(start, 1)
        _, after = remainder.split(end, 1)
        before = description_pattern.sub("", before)
        after = description_pattern.sub("", after)
        return before + _block("metadata", metadata) + after
    source = description_pattern.sub("", source)
    source, count = re.subn(
        r"(?=</head>)",
        "  " + _block("metadata", metadata) + "\n",
        source,
        count=1,
        flags=re.IGNORECASE,
    )
    if count != 1:
        raise ValueError(f"{page.path}: expected closing </head>")
    return source


def _render_head_and_runtime(source: str, model: SiteModel, page: Page) -> str:
    source = _render_metadata(source, model, page)
    theme = '<script src="assets/theme.js"></script>'
    if _markers("theme-bootstrap")[0] in source:
        source = _replace_named(source, "theme-bootstrap", theme)
    else:
        source, count = re.subn(
            r'(?=<link\s+rel=["\']stylesheet["\']\s+href=["\']assets/site\.css["\'])',
            _block("theme-bootstrap", theme) + "\n  ",
            source,
            count=1,
            flags=re.IGNORECASE,
        )
        if count != 1:
            raise ValueError("expected shared stylesheet in <head>")

    main_match = re.search(r"<main\b.*?</main>", source, flags=re.IGNORECASE | re.DOTALL)
    has_mermaid = bool(main_match and re.search(r'class=["\'][^"\']*\bmermaid\b', main_match.group(0)))
    runtime_parts = []
    if has_mermaid:
        runtime_parts.append(
            f'<script src="{MERMAID_SRC}" integrity="{MERMAID_INTEGRITY}" '
            'crossorigin="anonymous" referrerpolicy="no-referrer"></script>'
        )
    runtime_parts.append('<script src="assets/site.js"></script>')
    runtime = "\n".join(runtime_parts)
    if _markers("runtime")[0] in source:
        source = _replace_named(source, "runtime", runtime)
    else:
        source = RUNTIME_SCRIPT_RE.sub("", source)
        source, count = re.subn(
            r"(?=</body>)",
            "  " + _block("runtime", runtime) + "\n",
            source,
            count=1,
            flags=re.IGNORECASE,
        )
        if count != 1:
            raise ValueError("expected closing </body>")
    return source


def _headings(source: str) -> list[dict[str, str]]:
    parser = HeadingParser()
    parser.feed(source)
    return parser.headings


def _article_headings(source: str) -> list[dict[str, str]]:
    match = re.search(r"<main\b.*?</main>", source, flags=re.DOTALL | re.IGNORECASE)
    return _headings(match.group(0) if match else source)


def render_page(
    model: SiteModel,
    page: Page,
    source: str,
    fragment_registry: dict[str, dict[str, dict[str, object]]] | None = None,
) -> str:
    """Render generated chrome around authored page content."""
    if fragment_registry is None:
        registry_path = model.root / "data/heading-fragments.json"
        fragment_registry = load_heading_fragments(model.root) if registry_path.exists() else None
    entries = fragment_registry.get(page.path) if fragment_registry is not None else None
    source = _decorate_external_links(source, model.site["base_url"])
    source = _add_heading_permalinks(_assign_heading_ids(source, page, entries))
    page_map = {item.path: item for item in model.pages}
    flat_order = [path for group in model.navigation for path in group.pages]
    current_index = flat_order.index(page.path)

    nav_groups: list[str] = []
    for group in model.navigation:
        links = []
        for path in group.pages:
            target = page_map[path]
            current = ' aria-current="page"' if path == page.path else ""
            if path == "skills-repositories.html":
                repository_links = "".join(
                    f'<a href="{html.escape(path)}#{html.escape(fragment)}">{html.escape(label)}</a>'
                    for fragment, label in SKILL_REPOSITORY_NAV
                )
                open_attribute = " open" if path == page.path else ""
                links.append(
                    f'<details class="global-nav-disclosure"{open_attribute}>'
                    f'<summary>{html.escape(target.nav_label)}</summary>'
                    f'<a data-nav href="{html.escape(path)}"{current}>全部仓库</a>'
                    f'{repository_links}</details>'
                )
                continue
            links.append(f'<a data-nav href="{html.escape(path)}"{current}>{html.escape(target.nav_label)}</a>')
        nav_groups.append(f'<section class="global-nav-group"><strong>{html.escape(group.label)}</strong>{"".join(links)}</section>')
    global_nav = '<aside class="global-nav" id="global-nav" aria-label="全站导航">' + "".join(nav_groups) + "</aside>"

    toc_links = []
    for heading in _article_headings(source):
        if not heading["id"]:
            continue
        toc_links.append(f'<a class="toc-{heading["level"]}" href="#{html.escape(heading["id"])}">{html.escape(heading["text"])}</a>')
    toc = '<aside class="page-toc" aria-label="本页目录"><details><summary>本页目录</summary><nav>' + "".join(toc_links) + "</nav></details></aside>"

    previous_link = ""
    next_link = ""
    if current_index:
        previous = page_map[flat_order[current_index - 1]]
        previous_link = f'<a rel="prev" href="{previous.path}">← {html.escape(previous.nav_label)}</a>'
    if current_index + 1 < len(flat_order):
        following = page_map[flat_order[current_index + 1]]
        next_link = f'<a rel="next" href="{following.path}">{html.escape(following.nav_label)} →</a>'

    header = (
        '<script src="assets/site-data.js"></script>'
        '<a class="skip-link" href="#main-content">跳到正文</a>'
        '<header class="topbar"><div class="topbar-inner">'
        '<a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true"></span><span>Codex 使用指南</span></a>'
        '<div class="topbar-actions"><label class="theme-control"><span class="sr-only">主题</span>'
        '<select class="theme-select" id="theme-select" name="theme" aria-label="主题">'
        '<option value="light" selected>浅色</option>'
        '<option value="dark">深色</option></select></label>'
        '<span class="theme-status sr-only" aria-live="polite"></span>'
        '<button class="search-trigger" type="button" '
        'aria-haspopup="dialog" aria-controls="site-search-dialog">搜索</button>'
        '<button class="menu-toggle" type="button" aria-controls="global-nav" aria-expanded="false">目录</button></div>'
        '</div></header>'
        '<dialog class="search-dialog" id="site-search-dialog" role="dialog" '
        'aria-modal="true" aria-labelledby="site-search-title">'
        '<div class="search-dialog-panel"><div class="search-dialog-head">'
        '<p class="search-title" id="site-search-title">搜索全站</p>'
        '<button class="search-close" type="button" aria-label="关闭搜索">关闭</button></div>'
        '<label class="search-label" for="site-search-input">搜索标题、正文和可复用 prompt</label>'
        '<input class="search-input" id="site-search-input" type="search" role="combobox" '
        'autocomplete="off" aria-autocomplete="list" aria-controls="site-search-results" '
        'aria-describedby="site-search-status" aria-expanded="false">'
        '<p class="search-message" id="site-search-status" aria-live="polite">输入关键词开始搜索。</p>'
        '<ul class="search-results" id="site-search-results" role="listbox" '
        'aria-label="搜索结果"></ul></div></dialog>'
    )
    group_label = next(group.label for group in model.navigation if page.path in group.pages)
    shell_open = (
        '<div class="toolbook-shell">' + global_nav + '<div class="toolbook-main">'
        f'<nav class="breadcrumbs" aria-label="面包屑"><a href="index.html">首页</a>'
        f'<span aria-hidden="true">/</span><span>{html.escape(group_label)}</span>'
        f'<span aria-hidden="true">/</span><span aria-current="page">{html.escape(page.nav_label)}</span></nav>'
        f'<div class="page-freshness"><span>页面更新：<time datetime="{page.modified}">{page.modified}</time></span>'
        f'<span>事实核验：<time datetime="{page.facts_verified}">{page.facts_verified}</time></span></div>{toc}'
    )
    shell_close = f'<nav class="page-sequence" aria-label="前后页">{previous_link}{next_link}</nav></div></div>'

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
    source = re.sub(r'<main(?![^>]*\bid=)(\b[^>]*)>', r'<main id="main-content"\1>', source, count=1)
    return _render_head_and_runtime(source, model, page)


class HeadingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.current_heading: dict[str, object] | None = None
        self.headings: list[dict[str, str]] = []
        self.ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if self.ignored_depth:
            self.ignored_depth += 1
            return
        if self.current_heading is not None and "data-heading-permalink" in attr:
            self.ignored_depth = 1
            return
        if tag in {"h2", "h3"}:
            self.current_heading = {"level": tag, "id": attr.get("id") or "", "text": []}

    def handle_endtag(self, tag: str) -> None:
        if self.ignored_depth:
            self.ignored_depth -= 1
            return
        if tag in {"h2", "h3"} and self.current_heading:
            text = " ".join("".join(self.current_heading["text"]).split())
            if text:
                self.headings.append({"level": str(self.current_heading["level"]), "id": str(self.current_heading["id"]), "text": text})
            self.current_heading = None

    def handle_data(self, data: str) -> None:
        if self.current_heading and not self.ignored_depth:
            self.current_heading["text"].append(data)


class SectionSearchParser(HTMLParser):
    def __init__(self, policy: dict[str, object]) -> None:
        super().__init__(convert_charrefs=True)
        search = policy.get("search", {})
        assert isinstance(search, dict)
        self.excluded_tags = set(search.get("excluded_tags", []))
        self.excluded_attributes = set(search.get("excluded_attributes", []))
        self.excluded_classes = set(search.get("excluded_classes", []))
        self.in_main = 0
        self.excluded_depth = 0
        self.stack: list[tuple[str, bool]] = []
        self.heading: dict[str, object] | None = None
        self.current: dict[str, object] | None = None
        self.records: list[dict[str, object]] = []
        self.pre_depth = 0
        self.prompt: list[str] | None = None

    def _finish_current(self) -> None:
        if self.current is None:
            return
        chunks = [str(value) for value in self.current.pop("chunks")]
        self.current["text"] = " ".join("".join(chunks).split())
        self.records.append(self.current)
        self.current = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if tag == "main":
            self.in_main += 1
        classes = set(attr.get("class", "").split())
        excluded = bool(
            self.in_main
            and (
                tag in self.excluded_tags
                or any(name in attr for name in self.excluded_attributes)
                or bool(classes & self.excluded_classes)
            )
        )
        self.stack.append((tag, excluded))
        if excluded:
            self.excluded_depth += 1
        if not self.in_main or self.excluded_depth:
            return
        if tag in {"h2", "h3"}:
            self._finish_current()
            self.heading = {"level": tag, "fragment": attr.get("id", ""), "text": []}
        elif tag == "pre":
            self.pre_depth += 1
        elif tag == "code" and self.pre_depth:
            self.prompt = []

    def handle_endtag(self, tag: str) -> None:
        if self.in_main and not self.excluded_depth:
            if tag in {"h2", "h3"} and self.heading is not None:
                heading_text = " ".join("".join(self.heading["text"]).split())
                self.current = {
                    "level": self.heading["level"],
                    "section": heading_text,
                    "fragment": self.heading["fragment"],
                    "chunks": [],
                    "prompts": [],
                }
                self.heading = None
            elif tag == "code" and self.prompt is not None:
                if self.current is not None:
                    self.current["prompts"].append("".join(self.prompt))
                self.prompt = None
            elif tag == "pre" and self.pre_depth:
                self.pre_depth -= 1
        if self.stack:
            _, excluded = self.stack.pop()
            if excluded and self.excluded_depth:
                self.excluded_depth -= 1
        if tag == "main" and self.in_main:
            self._finish_current()
            self.in_main -= 1

    def handle_data(self, data: str) -> None:
        if not self.in_main or self.excluded_depth:
            return
        if self.heading is not None:
            self.heading["text"].append(data)
        elif self.current is not None:
            self.current["chunks"].append(data)
            if self.prompt is not None:
                self.prompt.append(data)


def extract_search_records(
    page: str,
    title: str,
    description: str,
    source: str,
    policy: dict[str, object],
) -> list[dict[str, object]]:
    parser = SectionSearchParser(policy)
    parser.feed(source)
    records: list[dict[str, object]] = [
        {"page": page, "title": title, "section": "", "fragment": "", "level": "page", "text": description, "prompts": []}
    ]
    for record in parser.records:
        record.update({"page": page, "title": title})
        records.append(record)
    for record in records:
        searchable = "\n".join(
            [str(record["section"]), str(record["text"]), *[str(value) for value in record["prompts"]]]
        )
        for item in policy.get("sensitive_patterns", []):
            assert isinstance(item, dict)
            if re.search(str(item["pattern"]), searchable, flags=re.IGNORECASE):
                raise ValueError(
                    f"{page}#{record['fragment']}: public search corpus matches sensitive pattern {item['name']}"
                )
    return records


def _payloads(
    model: SiteModel,
    rendered_pages: dict[str, str],
    policy: dict[str, object],
) -> dict[str, str]:
    source = {
        "site": model.site,
        "navigation": [{"label": group.label, "pages": list(group.pages)} for group in model.navigation],
        "pages": [page.__dict__ for page in model.pages],
        "fragments": {
            page.path: [heading["id"] for heading in _article_headings(rendered_pages[page.path])]
            for page in model.pages
        },
        "changelog": list(model.changelog),
    }
    search: list[dict[str, object]] = []
    for page in model.pages:
        search.extend(extract_search_records(page.path, page.title, page.description, rendered_pages[page.path], policy))

    search_payload = {"schema_version": 1, "records": search}
    fingerprint_assets = {}
    for relative in (
        "assets/site.css",
        "assets/site.js",
        "assets/theme.js",
        model.site["social_preview"],
    ):
        fingerprint_assets[relative] = hashlib.sha256((model.root / relative).read_bytes()).hexdigest()
    source["asset_fingerprints"] = fingerprint_assets
    fingerprint_input = {
        "site_data": source,
        "pages": rendered_pages,
        "search": search_payload,
        "assets": fingerprint_assets,
    }
    canonical = json.dumps(fingerprint_input, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    source["build_id"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:12]

    pretty_source = json.dumps(source, ensure_ascii=False, sort_keys=True, indent=2)
    pretty_search = json.dumps(search_payload, ensure_ascii=False, sort_keys=True, indent=2)
    return {
        "assets/site-data.js": f"window.GUIDE_SITE_DATA = {pretty_source};\n",
        "assets/search-index.js": f"window.GUIDE_SEARCH_INDEX = {pretty_search};\n",
    }


def build_publication_graph(
    model: SiteModel,
    fragment_registry: dict[str, dict[str, dict[str, object]]] | None = None,
    policy: dict[str, object] | None = None,
) -> tuple[dict[str, str], dict[str, str]]:
    if fragment_registry is None:
        fragment_registry = load_heading_fragments(model.root)
    if policy is None:
        policy = load_publication_policy(model.root)
    rendered_pages = {
        page.path: render_page(
            model,
            page,
            (model.root / page.path).read_text(encoding="utf-8"),
            fragment_registry,
        )
        for page in model.pages
    }
    payloads = _payloads(model, rendered_pages, policy)
    build_match = re.search(r'"build_id":\s*"([^"]+)"', payloads["assets/site-data.js"])
    if not build_match:
        raise ValueError("generated site data is missing build_id")
    build_id = build_match.group(1)
    rendered_pages = {
        path: source.replace(BUILD_PLACEHOLDER, build_id)
        for path, source in rendered_pages.items()
    }
    return rendered_pages, payloads


def generate(root: Path = ROOT, check: bool = False) -> list[str]:
    model = load_site_model(root)
    rendered_pages, payloads = build_publication_graph(model)
    stale: list[str] = []
    for page in model.pages:
        path = root / page.path
        actual = path.read_text(encoding="utf-8")
        expected = rendered_pages[page.path]
        if actual == expected:
            continue
        if check:
            stale.append(page.path)
        else:
            path.write_text(expected, encoding="utf-8")
    for relative, expected in payloads.items():
        path = root / relative
        actual = path.read_text(encoding="utf-8") if path.exists() else None
        if actual == expected:
            continue
        if check:
            stale.append(relative)
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
