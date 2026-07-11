from __future__ import annotations

import unittest

from scripts.check_published_site import validate_snapshot


class PublishedSiteTests(unittest.TestCase):
    def test_snapshot_accepts_current_marker_and_assets(self) -> None:
        html = '<meta name="guide-build" content="abc123"><script src="assets/site-data.js"></script>'
        self.assertEqual(validate_snapshot(html, "abc123", {"assets/site-data.js": True}), [])

    def test_snapshot_reports_stale_marker_and_missing_asset(self) -> None:
        errors = validate_snapshot("<html></html>", "abc123", {"assets/site-data.js": False})
        self.assertTrue(any("build marker" in error for error in errors))
        self.assertTrue(any("missing published asset" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
