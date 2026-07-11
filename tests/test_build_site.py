from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_site import GENERATED_END, GENERATED_START, render_page, replace_generated_block
from scripts.site_model import SiteModelError, load_site_model


ROOT = Path(__file__).resolve().parents[1]


class SiteModelTests(unittest.TestCase):
    def test_live_manifest_covers_every_root_page(self) -> None:
        model = load_site_model(ROOT)
        self.assertEqual(sorted(page.path for page in model.pages), sorted(path.name for path in ROOT.glob("*.html")))
        self.assertEqual(len(model.pages), 19)

    def test_manifest_rejects_duplicate_navigation_membership(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text("<title>x</title><h1>x</h1>", encoding="utf-8")
            manifest = {
                "schema_version": 1,
                "site": {"title": "x", "base_url": "https://example.test/", "language": "zh-CN"},
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
        self.assertNotIn('class="side-nav"', rendered)
        self.assertEqual(rendered.count('aria-current="page"'), 1)

    def test_toolbook_shell_assigns_ids_to_every_reader_heading(self) -> None:
        model = load_site_model(ROOT)
        page = next(page for page in model.pages if page.path == "index.html")
        rendered = render_page(model, page, (ROOT / page.path).read_text(encoding="utf-8"))
        import re
        headings = re.findall(r"<h[23]\b([^>]*)>", rendered)
        self.assertTrue(headings)
        self.assertTrue(all(re.search(r'\bid="[^"]+"', attrs) for attrs in headings))


if __name__ == "__main__":
    unittest.main()
