#!/usr/bin/env python3
"""Validate the static Codex usage guide before publishing."""

from __future__ import annotations

import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urldefrag, urlparse

try:
    from .build_site import generate, load_heading_fragments
    from .site_model import SiteModelError
except ImportError:  # Direct script execution.
    from build_site import generate, load_heading_fragments
    from site_model import SiteModelError


ROOT = Path(__file__).resolve().parents[1]
IGNORED_HTML_DIRS = {".git", ".worktrees", "build", "node_modules"}
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
LOOP_STAGES = [
    ("choose", "task-entry"),
    ("practice", "bounded-practice"),
    ("evidence", "acceptance-evidence"),
    ("recover", "recovery"),
    ("receipt", "task-receipt"),
]
CASE_LABELS = {
    "historical": "历史案例",
    "composite": "历史复合案例",
    "demo": "演示场景",
}
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}
REQUIRED_BACKLINKS = {
    "workflows.html": {"engineering.html#team-flow"},
    "subagents.html": {"engineering.html#issue-lanes", "engineering.html#team-case"},
    "goal.html": {"engineering.html#team-case"},
    "agents-md.html": {"engineering.html#team-case"},
    "compound-engineering.html": {"engineering.html#team-flow"},
    "skills-repositories.html": {"engineering.html#team-flow"},
    "engineering.html": {
        "workflows.html#task-entry",
        "subagents.html#worktree-subagent",
        "goal.html#real-example",
        "agents-md.html#real-example",
    },
}
CASE_ANCHOR_RE = re.compile(
    r"^(?P<page>[A-Za-z0-9_./-]+\.html)#(?P<fragment>[A-Za-z][A-Za-z0-9_.:-]*)$"
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.id_counts: Counter[str] = Counter()
        self.duplicate_attributes: list[tuple[str, str]] = []
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
        self.loop_stages: list[tuple[str, str]] = []
        self.heading_ids: list[str] = []
        self.fragment_aliases: dict[str, str] = {}
        self.cases: list[dict[str, str]] = []
        self._case_stack: list[dict[str, object]] = []
        self._depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attribute_counts = Counter(key for key, _ in attrs)
        self.duplicate_attributes.extend(
            (tag, key) for key, count in attribute_counts.items() if count > 1
        )
        attr = {key: value or "" for key, value in attrs}
        if tag not in VOID_TAGS:
            self._depth += 1
        if tag in {"script", "style"}:
            self._ignored_depth += 1
        if "id" in attr:
            self.ids.add(attr["id"])
            self.id_counts[attr["id"]] += 1
        if tag in {"h2", "h3"}:
            self.heading_ids.append(attr.get("id", ""))
        if "fragment-alias" in attr.get("class", "").split():
            self.fragment_aliases[attr.get("id", "")] = attr.get("data-canonical-fragment", "")
        if "data-loop-stage" in attr:
            self.loop_stages.append((attr["data-loop-stage"], attr.get("id", "")))
        if "data-case-type" in attr:
            self._case_stack.append(
                {
                    "tag": tag,
                    "type": attr["data-case-type"],
                    "id": attr.get("id", ""),
                    "case_id": attr.get("data-case-id", ""),
                    "text": [],
                    "depth": self._depth,
                }
            )
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
        if (
            self._case_stack
            and self._case_stack[-1]["tag"] == tag
            and self._case_stack[-1]["depth"] == self._depth
        ):
            case = self._case_stack.pop()
            self.cases.append(
                {
                    "type": str(case["type"]),
                    "id": str(case["id"]),
                    "case_id": str(case["case_id"]),
                    "text": " ".join(case["text"]),
                }
            )
        if tag in {"script", "style"} and self._ignored_depth:
            self._ignored_depth -= 1
        if tag == self._current_tag:
            self._current_tag = None
        if tag == "a":
            self._current_nav_href = None
        if tag not in VOID_TAGS and self._depth:
            self._depth -= 1

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        stripped = data.strip()
        if stripped:
            self._visible_chunks.append(stripped)
            for case in self._case_stack:
                case["text"].append(stripped)
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


def validate_semantic_contracts(pages: dict[str, PageParser]) -> list[str]:
    errors: list[str] = []
    seen_case_ids: dict[str, str] = {}

    for rel, parser in pages.items():
        for tag, attribute in parser.duplicate_attributes:
            errors.append(f"{rel}: duplicate {attribute} attribute on <{tag}>")
        for case in parser._case_stack:
            case_id = f"#{case['id']}" if case["id"] else "without id"
            errors.append(f"{rel}: unclosed case container {case_id}")
        for identifier, count in parser.id_counts.items():
            if count > 1:
                errors.append(f"{rel}: duplicate id #{identifier} appears {count} times")

    workflow_stages: list[tuple[str, str]] = []
    for rel, parser in pages.items():
        if rel == "workflows.html":
            workflow_stages.extend(parser.loop_stages)
        elif parser.loop_stages:
            errors.append(f"{rel}: loop stage belongs on workflows.html")

    if "workflows.html" in pages:
        expected_names = [stage for stage, _ in LOOP_STAGES]
        actual_names = [stage for stage, _ in workflow_stages]
        for stage, anchor in LOOP_STAGES:
            count = actual_names.count(stage)
            if count == 0:
                errors.append(f"workflows.html: missing loop stage: {stage}")
            elif count > 1:
                errors.append(f"workflows.html: duplicate loop stage: {stage}")
            for actual_stage, actual_anchor in workflow_stages:
                if actual_stage == stage and actual_anchor != anchor:
                    errors.append(
                        f"workflows.html: loop stage {stage} must use anchor #{anchor}"
                    )
        if actual_names != expected_names:
            errors.append("workflows.html: loop stages must appear in canonical order")

    for rel, parser in pages.items():
        for case in parser.cases:
            case_type = case["type"]
            case_id = f"#{case['id']}" if case["id"] else "without id"
            stable_case_id = case["case_id"]
            if not stable_case_id:
                errors.append(f"{rel}: case {case_id} missing data-case-id")
            elif stable_case_id in seen_case_ids:
                errors.append(
                    f"{rel}: duplicate data-case-id {stable_case_id}; "
                    f"first used by {seen_case_ids[stable_case_id]}"
                )
            else:
                seen_case_ids[stable_case_id] = f"{rel}{case_id}"
            if case_type not in CASE_LABELS:
                errors.append(f"{rel}: unknown case type: {case_type}")
                continue
            label = CASE_LABELS[case_type]
            if label not in case["text"]:
                errors.append(f"{rel}: case {case_id} must visibly include {label}")

    for rel, required in REQUIRED_BACKLINKS.items():
        if rel not in pages:
            continue
        missing = required - set(pages[rel].hrefs)
        for href in sorted(missing):
            errors.append(f"{rel}: missing required backlink: {href}")

    return errors


def validate_fragment_registry(
    pages: dict[str, PageParser],
    registry: dict[str, dict[str, dict[str, object]]],
) -> list[str]:
    errors: list[str] = []
    for rel, entries in registry.items():
        parser = pages.get(rel)
        if parser is None:
            errors.append(f"fragment registry references missing page: {rel}")
            continue
        expected = {str(entry["canonical"]) for entry in entries.values()}
        actual = set(parser.heading_ids)
        for fragment in sorted(expected - actual):
            errors.append(f"{rel}: missing canonical heading #{fragment}")
        for fragment in sorted(actual - expected):
            errors.append(f"{rel}: unregistered canonical heading #{fragment}")
        for entry in entries.values():
            canonical = str(entry["canonical"])
            for legacy in entry["legacy"]:
                legacy = str(legacy)
                if legacy == canonical:
                    continue
                if parser.fragment_aliases.get(legacy) != canonical:
                    errors.append(f"{rel}: legacy fragment #{legacy} must alias #{canonical}")
    return errors


def validate_case_index(pages: dict[str, PageParser], index_text: str) -> list[str]:
    errors: list[str] = []
    rows: dict[str, list[str]] = {}
    case_ids: set[str] = set()
    for line in index_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        first_cell = cells[0] if cells else ""
        if first_cell == "Case ID" or (first_cell and set(first_cell) == {"-"}):
            continue
        if len(cells) != 8:
            errors.append(f"evidence index: malformed row has {len(cells)} columns: {line}")
            continue
        case_id, anchor, case_label, _, review_status, freshness, role, _ = cells
        if case_id in case_ids:
            errors.append(f"evidence index: duplicate Case ID: {case_id}")
        case_ids.add(case_id)
        if anchor in rows:
            errors.append(f"evidence index: duplicate page anchor: {anchor}")
        rows[anchor] = cells
        if not CASE_ANCHOR_RE.fullmatch(anchor):
            errors.append(f"evidence index: invalid page anchor: {anchor}")
        for field_name, value in {
            "Case ID": case_id,
            "page anchor": anchor,
            "type": case_label,
            "review status": review_status,
            "freshness": freshness,
            "responsible role": role,
        }.items():
            if not value:
                errors.append(f"evidence index: {anchor or case_id} missing {field_name}")

    actual_anchors: set[str] = set()
    for rel, parser in pages.items():
        for case in parser.cases:
            if not case["id"]:
                errors.append(f"{rel}: indexed case is missing an id")
                continue
            anchor = f"{rel}#{case['id']}"
            actual_anchors.add(anchor)
            if anchor not in rows:
                errors.append(f"{rel}: case #{case['id']} missing from evidence index")
                continue
            if rows[anchor][0] != case["case_id"]:
                errors.append(
                    f"{rel}: case #{case['id']} index Case ID must be {case['case_id']}"
                )
            expected_label = CASE_LABELS.get(case["type"])
            if expected_label is None:
                continue
            if rows[anchor][2] != expected_label:
                errors.append(
                    f"{rel}: case #{case['id']} index type must be {expected_label}"
                )
    for anchor in sorted(set(rows) - actual_anchors):
        if CASE_ANCHOR_RE.fullmatch(anchor):
            errors.append(f"evidence index: orphan page anchor: {anchor}")
    return errors


def validate_required_pages(pages: dict[str, PageParser]) -> list[str]:
    errors: list[str] = []
    for rel in sorted(CONCEPT_PAGES):
        if rel not in pages:
            errors.append(f"{rel}: missing required concept page")
            continue
        missing = {"what", "when", "examples", "real-example"} - pages[rel].ids
        if missing:
            errors.append(f"{rel}: concept page missing anchors: {', '.join(sorted(missing))}")
    for rel in sorted(TASK_PAGES):
        if rel not in pages:
            errors.append(f"{rel}: missing required task/resource page")
            continue
        if "真实实例" not in pages[rel].source_text:
            errors.append(f"{rel}: task/resource page should include a 真实实例 section")
    return errors


def main() -> int:
    html_paths = sorted(
        path
        for path in ROOT.rglob("*.html")
        if not (set(path.relative_to(ROOT).parts) & IGNORED_HTML_DIRS)
    )
    pages = {path.relative_to(ROOT).as_posix(): parse_page(path) for path in html_paths}
    errors = validate_semantic_contracts(pages)
    try:
        errors.extend(validate_fragment_registry(pages, load_heading_fragments(ROOT)))
    except (OSError, ValueError) as error:
        errors.append(f"heading fragment registry invalid: {error}")
    errors.extend(validate_required_pages(pages))
    evidence_index = ROOT / "docs" / "case-evidence-index.md"
    if evidence_index.exists():
        errors.extend(validate_case_index(pages, evidence_index.read_text(encoding="utf-8")))
    else:
        errors.append("docs/case-evidence-index.md: missing case evidence index")

    try:
        stale_assets = generate(ROOT, check=True)
    except SiteModelError as error:
        errors.append(f"site data invalid: {error}")
        stale_assets = []
    for path in stale_assets:
        errors.append(f"generated asset is stale: {path}")

    for rel, parser in pages.items():
        if not parser.text("title"):
            errors.append(f"{rel}: missing non-empty <title>")
        if not parser.text("h1"):
            errors.append(f"{rel}: missing non-empty <h1>")
        if "/" in rel:
            for href in parser.hrefs:
                errors.extend(check_local_link(ROOT / rel, href, pages))
            for src in parser.images:
                errors.extend(check_local_link(ROOT / rel, src, pages))
            continue
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

    if errors:
        print("Site check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Site check passed: {len(pages)} HTML pages, local links, anchors, and required sections are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
