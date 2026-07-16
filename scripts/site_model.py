#!/usr/bin/env python3
"""Load and validate the static guide's source-of-truth data."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urldefrag, urlparse


class SiteModelError(ValueError):
    """Raised when source data cannot describe a deterministic site."""


OFFICIAL_SOURCE_HOSTS = {
    "developers.openai.com",
    "learn.chatgpt.com",
    "help.openai.com",
    "openai.com",
    "platform.openai.com",
}


@dataclass(frozen=True)
class PageSource:
    label: str
    url: str
    kind: str


@dataclass(frozen=True)
class Page:
    path: str
    title: str
    nav_label: str
    description: str
    modified: str
    facts_verified: str
    sources: tuple[PageSource, ...]


@dataclass(frozen=True)
class NavigationGroup:
    label: str
    pages: tuple[str, ...]


@dataclass(frozen=True)
class SiteModel:
    root: Path
    site: dict[str, str]
    pages: tuple[Page, ...]
    navigation: tuple[NavigationGroup, ...]
    changelog: tuple[dict[str, str], ...]


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SiteModelError(f"cannot read {path}: {error}") from error
    if not isinstance(data, dict):
        raise SiteModelError(f"{path} must contain a JSON object")
    return data


def _required_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SiteModelError(f"{field} must be a non-empty string")
    return value.strip()


def _iso_date(value: Any, field: str) -> str:
    text = _required_text(value, field)
    try:
        date.fromisoformat(text)
    except ValueError as error:
        raise SiteModelError(f"{field} must use YYYY-MM-DD: {text}") from error
    return text


def load_site_model(root: Path) -> SiteModel:
    root = root.resolve()
    manifest = _read_json(root / "data/site-manifest.json")
    changelog_data = _read_json(root / "data/changelog.json")
    if manifest.get("schema_version") != 1 or changelog_data.get("schema_version") != 1:
        raise SiteModelError("site data schema_version must be 1")

    site_raw = manifest.get("site")
    if not isinstance(site_raw, dict):
        raise SiteModelError("site must be an object")
    site = {
        "title": _required_text(site_raw.get("title"), "site.title"),
        "base_url": _required_text(site_raw.get("base_url"), "site.base_url"),
        "language": _required_text(site_raw.get("language"), "site.language"),
        "social_preview": _required_text(site_raw.get("social_preview"), "site.social_preview"),
    }
    if urlparse(site["base_url"]).scheme != "https" or not site["base_url"].endswith("/"):
        raise SiteModelError("site.base_url must be an absolute HTTPS URL ending in /")
    preview = Path(site["social_preview"])
    if preview.is_absolute() or ".." in preview.parts or preview.suffix.lower() != ".png":
        raise SiteModelError("site.social_preview must be a root-relative PNG path")

    pages_raw = manifest.get("pages")
    if not isinstance(pages_raw, list) or not pages_raw:
        raise SiteModelError("pages must be a non-empty list")
    pages: list[Page] = []
    page_paths: set[str] = set()
    for index, item in enumerate(pages_raw):
        if not isinstance(item, dict):
            raise SiteModelError(f"pages[{index}] must be an object")
        sources_raw = item.get("sources", [])
        if not isinstance(sources_raw, list):
            raise SiteModelError(f"pages[{index}].sources must be a list")
        sources: list[PageSource] = []
        seen_source_urls: set[str] = set()
        for source_index, source_item in enumerate(sources_raw):
            if not isinstance(source_item, dict):
                raise SiteModelError(f"pages[{index}].sources[{source_index}] must be an object")
            source = PageSource(
                label=_required_text(source_item.get("label"), f"pages[{index}].sources[{source_index}].label"),
                url=_required_text(source_item.get("url"), f"pages[{index}].sources[{source_index}].url"),
                kind=_required_text(source_item.get("kind"), f"pages[{index}].sources[{source_index}].kind"),
            )
            if source.kind not in {"official", "third_party"}:
                raise SiteModelError(
                    f"pages[{index}].sources[{source_index}].kind must be official or third_party"
                )
            parsed_source_url = urlparse(source.url)
            if parsed_source_url.scheme != "https" or not parsed_source_url.netloc:
                raise SiteModelError(f"pages[{index}].sources[{source_index}].url must be absolute HTTPS")
            if source.kind == "official" and parsed_source_url.hostname not in OFFICIAL_SOURCE_HOSTS:
                raise SiteModelError(
                    f"pages[{index}].sources[{source_index}] labels a non-OpenAI host as official"
                )
            if source.url in seen_source_urls:
                raise SiteModelError(f"pages[{index}] has duplicate source URL: {source.url}")
            seen_source_urls.add(source.url)
            sources.append(source)
        page = Page(
            path=_required_text(item.get("path"), f"pages[{index}].path"),
            title=_required_text(item.get("title"), f"pages[{index}].title"),
            nav_label=_required_text(item.get("nav_label"), f"pages[{index}].nav_label"),
            description=_required_text(item.get("description"), f"pages[{index}].description"),
            modified=_iso_date(item.get("modified"), f"pages[{index}].modified"),
            facts_verified=_iso_date(item.get("facts_verified"), f"pages[{index}].facts_verified"),
            sources=tuple(sources),
        )
        if page.path in page_paths:
            raise SiteModelError(f"duplicate page path: {page.path}")
        if Path(page.path).name != page.path or not page.path.endswith(".html"):
            raise SiteModelError(f"page path must be a root HTML file: {page.path}")
        page_paths.add(page.path)
        pages.append(page)

    actual_pages = {path.name for path in root.glob("*.html")}
    if page_paths != actual_pages:
        missing = sorted(actual_pages - page_paths)
        unknown = sorted(page_paths - actual_pages)
        raise SiteModelError(f"manifest page coverage mismatch; missing={missing}, unknown={unknown}")

    navigation_raw = manifest.get("navigation")
    if not isinstance(navigation_raw, list) or not navigation_raw:
        raise SiteModelError("navigation must be a non-empty list")
    navigation: list[NavigationGroup] = []
    nav_pages: set[str] = set()
    for index, item in enumerate(navigation_raw):
        if not isinstance(item, dict) or not isinstance(item.get("pages"), list):
            raise SiteModelError(f"navigation[{index}] must contain a pages list")
        group_pages: list[str] = []
        for raw_path in item["pages"]:
            path = _required_text(raw_path, f"navigation[{index}].pages")
            if path in nav_pages:
                raise SiteModelError(f"duplicate navigation page: {path}")
            if path not in page_paths:
                raise SiteModelError(f"unknown navigation page: {path}")
            nav_pages.add(path)
            group_pages.append(path)
        navigation.append(NavigationGroup(_required_text(item.get("label"), f"navigation[{index}].label"), tuple(group_pages)))
    if nav_pages != page_paths:
        raise SiteModelError(f"navigation does not cover pages: {sorted(page_paths - nav_pages)}")

    entries_raw = changelog_data.get("entries")
    if not isinstance(entries_raw, list):
        raise SiteModelError("changelog entries must be a list")
    changelog: list[dict[str, str]] = []
    previous_date: str | None = None
    for index, item in enumerate(entries_raw):
        if not isinstance(item, dict):
            raise SiteModelError(f"changelog entries[{index}] must be an object")
        entry = {
            "date": _iso_date(item.get("date"), f"changelog.entries[{index}].date"),
            "category": _required_text(item.get("category"), f"changelog.entries[{index}].category"),
            "title": _required_text(item.get("title"), f"changelog.entries[{index}].title"),
            "summary": _required_text(item.get("summary"), f"changelog.entries[{index}].summary"),
            "target": _required_text(item.get("target"), f"changelog.entries[{index}].target"),
        }
        target_path, _ = urldefrag(entry["target"])
        if target_path not in page_paths:
            raise SiteModelError(f"changelog entry has unknown target: {entry['target']}")
        if previous_date is not None and entry["date"] > previous_date:
            raise SiteModelError("changelog entries must be newest first")
        previous_date = entry["date"]
        changelog.append(entry)

    return SiteModel(root, site, tuple(pages), tuple(navigation), tuple(changelog))
