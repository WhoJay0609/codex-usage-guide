from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_site import PageParser, check_local_link, parse_page


class CheckSiteTests(unittest.TestCase):
    def test_parser_collects_shared_assets_and_navigation(self) -> None:
        parser = PageParser()
        parser.feed('<title>T</title><h1>H</h1><nav><a data-nav href="index.html">首页</a></nav><link rel="stylesheet" href="assets/site.css"><script src="assets/site.js"></script>')
        self.assertEqual(parser.text("title"), "T")
        self.assertEqual(parser.text("h1"), "H")
        self.assertIn("index.html", parser.nav_links)
        self.assertIn("assets/site.css", parser.stylesheets)
        self.assertIn("assets/site.js", parser.scripts)

    def test_local_fragment_check_reports_missing_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.html"
            target = root / "target.html"
            source.write_text("<a href='target.html#missing'>x</a>", encoding="utf-8")
            target.write_text("<h1 id='present'>x</h1>", encoding="utf-8")
            pages = {"target.html": parse_page(target)}
            import scripts.check_site as checker
            old_root = checker.ROOT
            checker.ROOT = root
            try:
                errors = check_local_link(source, "target.html#missing", pages)
            finally:
                checker.ROOT = old_root
            self.assertEqual(errors, ["source.html: missing anchor #missing in target.html"])


if __name__ == "__main__":
    unittest.main()
