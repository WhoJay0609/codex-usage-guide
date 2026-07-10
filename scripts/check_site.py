#!/usr/bin/env python3
"""Validate the static Codex usage guide before publishing."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urlparse


ROOT = Path(__file__).resolve().parents[1]
CORE_NAV = {
    "index.html",
    "codex.html",
    "install-desktop.html",
    "desktop-cli.html",
    "permissions.html",
    "agents-md.html",
    "skills.html",
    "mcp.html",
    "subagents.html",
    "goal.html",
    "workflows.html",
    "resources.html",
}
REQUIRED_TEXT = {
    "index.html": ["Codex Desktop", "Desktop 工作流", "30 秒选择入口", "官方事实"],
    "codex.html": ["Codex Desktop", "Desktop 为主"],
    "install-desktop.html": ["Codex Desktop", "第一次打开桌面版"],
    "desktop-cli.html": ["Codex Desktop", "这份手册只把 Codex Desktop 作为主入口"],
    "daily-workflow.html": ["真实实例", "失败停止"],
    "engineering.html": ["真实实例", "失败停止"],
    "research.html": ["真实实例", "失败停止"],
    "automation.html": ["Codex Desktop Automations", "后台 worktree", "失败停止"],
    "workflows.html": ["先选工作面", "统一案例模板", "坏 prompt 怎么修"],
    "compound-engineering.html": ["Compound Engineering plugin", "在 Codex Desktop 里安装", "核心六步怎么用", "失败停止"],
    "skills-repositories.html": ["高 stars skills 仓库介绍", "Codex Desktop", "Compound Engineering", "mattpocock/skills", "academic-research-skills-codex", "skills/academic-research-suite", "ARIS", "不是 OpenAI 官方功能", "goal-entry 不列入", "效果一般", "真实实例"],
    "goal-entry.html": ["本机自己开发", "效果一般", "非官方", "真实实例"],
    "resources.html": ["Codex Desktop", "本指南只保留 Desktop 读者主线"],
}
FORBIDDEN_VISIBLE_TEXT = {
    "Desktop/CLI",
    "Codex CLI",
    "codex exec",
    "CLI 入门",
    "命令行优先",
    "终端优先",
    "non-interactive",
}
CONCEPT_PAGES = {
    "codex.html",
    "permissions.html",
    "agents-md.html",
    "skills.html",
    "mcp.html",
    "subagents.html",
    "goal.html",
}
TASK_PAGES = {
    "install-desktop.html",
    "desktop-cli.html",
    "daily-workflow.html",
    "engineering.html",
    "research.html",
    "automation.html",
    "workflows.html",
    "resources.html",
    "goal-entry.html",
    "compound-engineering.html",
    "skills-repositories.html",
}
REQUIRED_IMAGES = {
    "skills-repositories.html": {
        "figures/high-stars-chooser.png",
        "figures/high-stars-engineering-research.png",
        "figures/high-stars-automation-loop.png",
    },
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.images: list[str] = []
        self.stylesheets: list[str] = []
        self.scripts: list[str] = []
        self.nav_links: set[str] = set()
        self.nav_text: dict[str, list[str]] = {}
        self.source_text = ""
        self._current_tag: str | None = None
        self._ignored_depth = 0
        self._current_nav_href: str | None = None
        self._text_chunks: dict[str, list[str]] = {"title": [], "h1": []}
        self._visible_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if tag in {"script", "style"}:
            self._ignored_depth += 1
        if "id" in attr:
            self.ids.add(attr["id"])
        if tag == "a" and attr.get("href"):
            href = attr["href"]
            self.hrefs.append(href)
            href_without_fragment = urldefrag(href)[0]
            if "data-nav" in attr:
                self.nav_links.add(href_without_fragment)
                self._current_nav_href = href_without_fragment
        if tag == "link" and attr.get("rel") == "stylesheet" and attr.get("href"):
            self.stylesheets.append(attr["href"])
        if tag == "img" and attr.get("src"):
            self.images.append(attr["src"])
        if tag == "script" and attr.get("src"):
            self.scripts.append(attr["src"])
        if tag in self._text_chunks:
            self._current_tag = tag

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self._ignored_depth:
            self._ignored_depth -= 1
        if tag == self._current_tag:
            self._current_tag = None
        if tag == "a":
            self._current_nav_href = None

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        stripped = data.strip()
        if stripped:
            self._visible_chunks.append(stripped)
            if self._current_nav_href:
                self.nav_text.setdefault(self._current_nav_href, []).append(stripped)
        if self._current_tag:
            self._text_chunks[self._current_tag].append(data)

    def text(self, tag: str) -> str:
        return " ".join(chunk.strip() for chunk in self._text_chunks[tag]).strip()

    def visible_text(self) -> str:
        return " ".join(self._visible_chunks)


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.source_text = path.read_text(encoding="utf-8")
    parser.feed(parser.source_text)
    return parser


def is_external(href: str) -> bool:
    parsed = urlparse(href)
    return parsed.scheme in {"http", "https", "mailto", "tel"}


def check_local_link(source: Path, href: str, pages: dict[str, PageParser]) -> list[str]:
    if not href or href.startswith(("javascript:", "data:")) or is_external(href):
        return []

    target_ref, fragment = urldefrag(href)
    if not target_ref:
        target_ref = source.name
    target = (source.parent / target_ref).resolve()

    if not target.is_relative_to(ROOT):
        return [f"{source.name}: local link escapes site root: {href}"]
    if not target.exists():
        return [f"{source.name}: missing local link target: {href}"]
    if target.suffix == ".html" and fragment:
        rel = target.relative_to(ROOT).as_posix()
        if rel not in pages:
            return []
        if fragment not in pages[rel].ids:
            return [f"{source.name}: missing anchor #{fragment} in {rel}"]
    return []


def main() -> int:
    html_paths = sorted(ROOT.glob("*.html"))
    pages = {path.relative_to(ROOT).as_posix(): parse_page(path) for path in html_paths}
    errors: list[str] = []

    for rel, parser in pages.items():
        if not parser.text("title"):
            errors.append(f"{rel}: missing non-empty <title>")
        if not parser.text("h1"):
            errors.append(f"{rel}: missing non-empty <h1>")
        if "assets/site.css" not in parser.stylesheets:
            errors.append(f"{rel}: missing shared stylesheet assets/site.css")
        if "assets/site.js" not in parser.scripts:
            errors.append(f"{rel}: missing shared script assets/site.js")
        visible_text = parser.visible_text()
        for phrase in sorted(FORBIDDEN_VISIBLE_TEXT):
            if phrase in visible_text:
                errors.append(f"{rel}: forbidden Desktop-first wording remains visible: {phrase}")
        for phrase in REQUIRED_TEXT.get(rel, []):
            if phrase not in visible_text:
                errors.append(f"{rel}: missing required Desktop-first text: {phrase}")
        desktop_nav = " ".join(parser.nav_text.get("desktop-cli.html", []))
        if desktop_nav and desktop_nav != "Desktop":
            errors.append(f"{rel}: desktop navigation label should be Desktop, got: {desktop_nav}")
        missing_nav = sorted(CORE_NAV - parser.nav_links)
        if missing_nav:
            errors.append(f"{rel}: top nav missing links: {', '.join(missing_nav)}")
        for href in parser.hrefs:
            errors.extend(check_local_link(ROOT / rel, href, pages))
        for src in parser.images:
            errors.extend(check_local_link(ROOT / rel, src, pages))
        missing_images = REQUIRED_IMAGES.get(rel, set()) - set(parser.images)
        if missing_images:
            errors.append(f"{rel}: missing required images: {', '.join(sorted(missing_images))}")

    for rel in sorted(CONCEPT_PAGES):
        missing = {"what", "when", "examples", "real-example"} - pages[rel].ids
        if missing:
            errors.append(f"{rel}: concept page missing anchors: {', '.join(sorted(missing))}")
    for rel in sorted(TASK_PAGES):
        if "真实实例" not in pages[rel].source_text:
            errors.append(f"{rel}: task/resource page should include a 真实实例 section")

    if errors:
        print("Site check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Site check passed: {len(pages)} HTML pages, local links, anchors, and required sections are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
