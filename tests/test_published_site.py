from __future__ import annotations

import unittest

from scripts.check_published_site import (
    validate_page_metadata,
    validate_published_asset,
    validate_published_page,
    validate_snapshot,
)


class PublishedSiteTests(unittest.TestCase):
    def test_published_page_requires_build_marker_and_registered_fragments(self) -> None:
        html = '<html><head><meta name="guide-build" content="wrong"></head><body><h2 id="one">One</h2></body></html>'
        errors = validate_published_page(html, "expected", ["one", "two"])
        self.assertTrue(any("build marker" in error for error in errors), errors)
        self.assertTrue(any("missing fragment #two" in error for error in errors), errors)

    def test_published_asset_requires_content_type_and_exact_local_bytes(self) -> None:
        errors = validate_published_asset(
            "assets/search-index.js",
            True,
            "text/html",
            b"remote",
            "application/javascript",
            b"local",
        )
        self.assertTrue(any("content type" in error for error in errors), errors)
        self.assertTrue(any("content fingerprint" in error for error in errors), errors)

    def test_page_metadata_accepts_expected_canonical_and_preview(self) -> None:
        html = (
            '<title>权限与安全</title>'
            '<meta name="description" content="页面描述">'
            '<link rel="canonical" href="https://example.test/permissions.html">'
            '<meta property="og:title" content="权限与安全">'
            '<meta property="og:description" content="页面描述">'
            '<meta property="og:url" content="https://example.test/permissions.html">'
            '<meta property="og:image" content="https://example.test/figures/social-preview.png">'
            '<meta name="twitter:card" content="summary_large_image">'
            '<meta name="twitter:title" content="权限与安全">'
            '<meta name="twitter:description" content="页面描述">'
            '<meta name="twitter:image" content="https://example.test/figures/social-preview.png">'
        )
        self.assertEqual(
            validate_page_metadata(
                html,
                "权限与安全",
                "页面描述",
                "https://example.test/permissions.html",
                "https://example.test/figures/social-preview.png",
            ),
            [],
        )

    def test_snapshot_accepts_current_marker_and_assets(self) -> None:
        html = '<meta name="guide-build" content="abc123"><script src="assets/site-data.js"></script>'
        self.assertEqual(validate_snapshot(html, "abc123", {"assets/site-data.js": True}), [])

    def test_snapshot_reports_stale_marker_and_missing_asset(self) -> None:
        errors = validate_snapshot("<html></html>", "abc123", {"assets/site-data.js": False})
        self.assertTrue(any("build marker" in error for error in errors))
        self.assertTrue(any("missing published asset" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
