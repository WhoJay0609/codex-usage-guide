from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

from scripts.build_site import (
    GENERATED_END,
    GENERATED_START,
    build_publication_graph,
    extract_search_records,
    load_heading_fragments,
    load_publication_policy,
    render_page,
    replace_generated_block,
)
from scripts.site_model import SiteModelError, load_site_model


ROOT = Path(__file__).resolve().parents[1]


class SiteModelTests(unittest.TestCase):
    def test_live_manifest_covers_every_root_page(self) -> None:
        model = load_site_model(ROOT)
        self.assertEqual(sorted(page.path for page in model.pages), sorted(path.name for path in ROOT.glob("*.html")))
        self.assertEqual(len(model.pages), 20)

    def test_manifest_rejects_duplicate_navigation_membership(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text("<title>x</title><h1>x</h1>", encoding="utf-8")
            manifest = {
                "schema_version": 1,
                "site": {"title": "x", "base_url": "https://example.test/", "language": "zh-CN", "social_preview": "figures/social-preview.png"},
                "navigation": [{"label": "a", "pages": ["index.html", "index.html"]}],
                "pages": [{"path": "index.html", "title": "x", "nav_label": "x", "description": "x", "modified": "2026-07-11", "facts_verified": "2026-07-11"}],
            }
            (root / "data").mkdir()
            (root / "data/site-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            (root / "data/changelog.json").write_text('{"schema_version": 1, "entries": []}', encoding="utf-8")
            with self.assertRaisesRegex(SiteModelError, "duplicate navigation page"):
                load_site_model(root)

    def test_generated_block_replacement_preserves_authored_bytes(self) -> None:
        source = f"before\n{GENERATED_START}old{GENERATED_END}\nafter"
        actual = replace_generated_block(source, "new")
        self.assertEqual(actual, f"before\n{GENERATED_START}new{GENERATED_END}\nafter")
        self.assertEqual(actual.split(GENERATED_START)[0], "before\n")
        self.assertEqual(actual.split(GENERATED_END)[1], "\nafter")

    def test_generated_block_requires_exactly_one_sentinel_pair(self) -> None:
        with self.assertRaisesRegex(ValueError, "exactly one"):
            replace_generated_block("authored only", "new")

    def test_toolbook_shell_is_static_complete_and_idempotent(self) -> None:
        model = load_site_model(ROOT)
        page = next(page for page in model.pages if page.path == "permissions.html")
        source = (ROOT / page.path).read_text(encoding="utf-8")
        rendered = render_page(model, page, source)
        self.assertEqual(render_page(model, page, rendered), rendered)
        self.assertIn('class="toolbook-shell"', rendered)
        self.assertIn('class="global-nav"', rendered)
        self.assertIn('class="page-toc"', rendered)
        self.assertIn('href="#matrix"', rendered)
        self.assertIn('<details><summary>本页目录</summary>', rendered)
        self.assertNotIn('<details open><summary>本页目录</summary>', rendered)
        self.assertLess(rendered.index('class="page-toc"'), rendered.index('<main'))
        self.assertNotIn('class="side-nav"', rendered)
        self.assertEqual(rendered.count('aria-current="page"'), 2)

    def test_skills_repository_navigation_lists_each_repository_on_demand(self) -> None:
        model = load_site_model(ROOT)
        page = next(page for page in model.pages if page.path == "skills-repositories.html")
        rendered = render_page(model, page, (ROOT / page.path).read_text(encoding="utf-8"))
        self.assertIn('<details class="global-nav-disclosure" open>', rendered)
        self.assertIn('<summary>Skills 仓库</summary>', rendered)
        self.assertIn('href="skills-repositories.html#compound-engineering"', rendered)
        self.assertIn('href="skills-repositories.html#mattpocock-skills"', rendered)
        self.assertIn('href="skills-repositories.html#academic-research-skills-codex"', rendered)
        self.assertIn('href="skills-repositories.html#aris-auto-claude-code-research-in-sleep"', rendered)

    def test_toolbook_shell_assigns_ids_to_every_reader_heading(self) -> None:
        model = load_site_model(ROOT)
        page = next(page for page in model.pages if page.path == "index.html")
        rendered = render_page(model, page, (ROOT / page.path).read_text(encoding="utf-8"))
        headings = re.findall(r"<h[23]\b([^>]*)>", rendered)
        self.assertTrue(headings)
        self.assertTrue(all(re.search(r'\bid="[^"]+"', attrs) for attrs in headings))

    def test_source_card_headings_keep_ids_without_nested_permalinks(self) -> None:
        model = load_site_model(ROOT)
        page = next(page for page in model.pages if page.path == "index.html")
        rendered = render_page(model, page, (ROOT / page.path).read_text(encoding="utf-8"))
        source_card = re.search(
            r'<a\b[^>]*class="[^"]*source-card[^"]*"[^>]*>.*?</a>',
            rendered,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(source_card)
        assert source_card is not None
        self.assertRegex(source_card.group(0), r'<h3\b[^>]*\bid="[^"]+"')
        self.assertNotIn("data-heading-permalink", source_card.group(0))

    def test_toolbook_shell_generates_search_dialog_and_heading_permalinks(self) -> None:
        model = load_site_model(ROOT)
        page = next(page for page in model.pages if page.path == "permissions.html")
        rendered = render_page(model, page, (ROOT / page.path).read_text(encoding="utf-8"))
        self.assertIn('src="assets/site-data.js"', rendered)
        self.assertNotIn('src="assets/search-index.js"', rendered)
        self.assertIn('class="skip-link" href="#main-content"', rendered)
        self.assertIn('<main id="main-content"', rendered)
        self.assertIn('<span>基础概念</span>', rendered)
        self.assertIn('<span aria-current="page">权限</span>', rendered)
        self.assertIn('class="search-trigger"', rendered)
        self.assertIn('role="dialog"', rendered)
        self.assertIn('role="combobox"', rendered)
        self.assertIn('role="listbox"', rendered)
        article = rendered.split("<main", 1)[1].split("</main>", 1)[0]
        self.assertEqual(
            article.count('data-heading-permalink'),
            article.count("<h2") + article.count("<h3"),
        )
        self.assertEqual(render_page(model, page, rendered), rendered)

    def test_theme_bootstrap_precedes_css_and_runtime_is_page_scoped(self) -> None:
        model = load_site_model(ROOT)
        mermaid_page = next(page for page in model.pages if page.path == "install-desktop.html")
        plain_page = next(page for page in model.pages if page.path == "permissions.html")
        mermaid_rendered = render_page(model, mermaid_page, (ROOT / mermaid_page.path).read_text(encoding="utf-8"))
        plain_rendered = render_page(model, plain_page, (ROOT / plain_page.path).read_text(encoding="utf-8"))
        self.assertLess(mermaid_rendered.index('src="assets/theme.js"'), mermaid_rendered.index('href="assets/site.css"'))
        self.assertIn('class="theme-select" id="theme-select" name="theme"', mermaid_rendered)
        self.assertIn('<option value="light" selected>浅色</option>', mermaid_rendered)
        self.assertNotIn('<option value="system">', mermaid_rendered)
        self.assertIn('<link rel="icon" href="favicon.svg" type="image/svg+xml">', plain_rendered)
        self.assertIn('mermaid@11.14.0/dist/mermaid.min.js', mermaid_rendered)
        self.assertIn('integrity="sha384-1CMXl090wj8Dd6YfnzSQUOgWbE6suWCaenYG7pox5AX7apTpY3PmJMeS2oPql4Gk"', mermaid_rendered)
        self.assertIn('crossorigin="anonymous"', mermaid_rendered)
        self.assertNotIn("gsap", mermaid_rendered.lower())
        self.assertNotIn("mermaid.min.js", plain_rendered)
        self.assertEqual(render_page(model, mermaid_page, mermaid_rendered), mermaid_rendered)

    def test_manifest_metadata_generates_complete_same_origin_social_head(self) -> None:
        model = load_site_model(ROOT)
        page = next(page for page in model.pages if page.path == "permissions.html")
        rendered = render_page(model, page, (ROOT / page.path).read_text(encoding="utf-8"))
        canonical = "https://whojay0609.github.io/codex-usage-guide/permissions.html"
        preview = "https://whojay0609.github.io/codex-usage-guide/figures/social-preview.png"
        self.assertIn(f'<link rel="canonical" href="{canonical}">', rendered)
        self.assertIn(
            '<meta name="description" content="理解 Desktop 四个权限选择及底层 sandbox、approval、network 与 secret 边界。">',
            rendered,
        )
        self.assertIn('<meta property="og:title" content="权限与安全">', rendered)
        self.assertIn(f'<meta property="og:url" content="{canonical}">', rendered)
        self.assertIn(f'<meta property="og:image" content="{preview}">', rendered)
        self.assertIn('<meta name="twitter:card" content="summary_large_image">', rendered)
        self.assertIn(f'<meta name="twitter:image" content="{preview}">', rendered)
        self.assertEqual(render_page(model, page, rendered), rendered)

    def test_only_cross_origin_http_links_receive_safe_visible_external_semantics(self) -> None:
        model = load_site_model(ROOT)
        page = next(page for page in model.pages if page.path == "permissions.html")
        source = (ROOT / page.path).read_text(encoding="utf-8")
        source = source.replace(
            "</main>",
            '<p><a id="outside" href="https://example.com/docs">外部</a>'
            '<a id="same" href="https://whojay0609.github.io/codex-usage-guide/index.html">站内绝对</a>'
            '<a id="mail" href="mailto:test@example.com">邮件</a></p></main>',
        )
        rendered = render_page(model, page, source)
        outside = re.search(r'<a id="outside"([^>]*)>(.*?)</a>', rendered).group(0)
        self.assertIn('target="_blank"', outside)
        self.assertIn('rel="noopener noreferrer"', outside)
        self.assertIn('referrerpolicy="no-referrer"', outside)
        self.assertIn('class="external-link-indicator"', outside)
        self.assertNotIn('target="_blank"', re.search(r'<a id="same"[^>]*>.*?</a>', rendered).group(0))
        self.assertNotIn('target="_blank"', re.search(r'<a id="mail"[^>]*>.*?</a>', rendered).group(0))

    def test_canonical_heading_preserves_legacy_and_structural_fragments(self) -> None:
        model = load_site_model(ROOT)
        page = next(page for page in model.pages if page.path == "permissions.html")
        source = (
            '<html><head><link rel="stylesheet" href="assets/site.css"></head><body>'
            '<header class="topbar"></header><main><section id="matrix">'
            '<h2 id="heading-permissions-1">审批决策矩阵</h2><p>解释正文</p>'
            '</section></main><script src="assets/site.js"></script></body></html>'
        )
        registry = {
            "permissions.html": {
                "heading-permissions-1": {"canonical": "审批决策矩阵", "legacy": ["heading-permissions-1"]}
            }
        }
        rendered = render_page(model, page, source, registry)
        self.assertIn('<section id="matrix">', rendered)
        self.assertIn('id="审批决策矩阵"', rendered)
        self.assertIn('class="fragment-alias" id="heading-permissions-1"', rendered)
        self.assertIn('href="#审批决策矩阵"', rendered)
        self.assertEqual(render_page(model, page, rendered, registry), rendered)

    def test_section_search_records_include_prose_and_exact_prompt_but_exclude_private_content(self) -> None:
        source = (
            '<main><section><h2 id="stable">标题 <code>AGENTS.md</code></h2>'
            '<p>解释正文。</p><pre><code>第一行\n第二行</code></pre>'
            '<p hidden>隐藏秘密</p><aside data-search-exclude>内部账本</aside>'
            '<script>private()</script></section></main><footer>页脚</footer>'
        )
        policy = {
            "search": {
                "excluded_tags": ["script", "style", "template", "noscript"],
                "excluded_attributes": ["hidden", "data-search-exclude"],
                "excluded_classes": ["fragment-alias"],
            },
            "sensitive_patterns": [],
        }
        records = extract_search_records("sample.html", "示例", "描述", source, policy)
        self.assertEqual(records[0]["fragment"], "")
        section = records[1]
        self.assertEqual(section["fragment"], "stable")
        self.assertEqual(section["section"], "标题 AGENTS.md")
        self.assertIn("解释正文", section["text"])
        self.assertIn("第一行 第二行", section["text"])
        self.assertEqual(section["prompts"], ["第一行\n第二行"])
        self.assertNotIn("隐藏秘密", section["text"])
        self.assertNotIn("内部账本", section["text"])
        self.assertNotIn("页脚", section["text"])

    def test_publication_graph_derives_payloads_from_rendered_pages(self) -> None:
        model = load_site_model(ROOT)
        pages, payloads = build_publication_graph(
            model,
            load_heading_fragments(ROOT),
            load_publication_policy(ROOT),
        )
        permissions = pages["permissions.html"]
        self.assertIn('href="#审批决策矩阵"', permissions)
        self.assertIn('"schema_version": 1', payloads["assets/search-index.js"])
        self.assertIn('"records"', payloads["assets/search-index.js"])


if __name__ == "__main__":
    unittest.main()
