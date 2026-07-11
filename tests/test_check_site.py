import unittest
from pathlib import Path
import sys
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_site import (  # noqa: E402
    PageParser,
    check_local_link,
    validate_case_index,
    validate_fragment_registry,
    validate_required_pages,
    validate_semantic_contracts,
)


def parse(markup: str) -> PageParser:
    parser = PageParser()
    parser.source_text = markup
    parser.feed(markup)
    return parser


class SemanticContractTests(unittest.TestCase):
    def test_fragment_registry_requires_canonical_heading_and_legacy_alias(self) -> None:
        pages = {
            "sample.html": parse(
                '<main><span class="fragment-alias" id="old" '
                'data-canonical-fragment="wrong" aria-hidden="true"></span>'
                '<h2 id="canonical">标题</h2></main>'
            )
        }
        registry = {
            "sample.html": {
                "old": {"canonical": "canonical", "legacy": ["old"]}
            }
        }
        errors = validate_fragment_registry(pages, registry)
        self.assertTrue(any("legacy fragment #old must alias #canonical" in error for error in errors), errors)

    def test_duplicate_id_is_reported(self) -> None:
        pages = {"sample.html": parse('<main id="same"><section id="same"></section></main>')}
        errors = validate_semantic_contracts(pages)
        self.assertTrue(any("duplicate id #same" in error for error in errors), errors)

    def test_duplicate_html_attribute_is_reported(self) -> None:
        pages = {
            "sample.html": parse(
                '<article id="case-a" data-case-type="demo" '
                'data-case-id="first" data-case-id="second">演示场景</article>'
            )
        }
        errors = validate_semantic_contracts(pages)
        self.assertTrue(any("duplicate data-case-id attribute" in error for error in errors), errors)

    def test_loop_stage_wrong_page_and_order_are_reported(self) -> None:
        pages = {
            "engineering.html": parse('<section id="task-entry" data-loop-stage="choose">选择</section>'),
            "workflows.html": parse(
                '<section id="bounded-practice" data-loop-stage="practice">实践</section>'
                '<section id="task-entry" data-loop-stage="choose">选择</section>'
            ),
        }
        errors = validate_semantic_contracts(pages)
        self.assertTrue(any("loop stage belongs on workflows.html" in error for error in errors), errors)
        self.assertTrue(any("loop stages must appear in canonical order" in error for error in errors), errors)

    def test_missing_loop_stage_is_reported(self) -> None:
        pages = {
            "workflows.html": parse(
                '<section id="task-entry" data-loop-stage="choose">选择</section>'
                '<section id="bounded-practice" data-loop-stage="practice">实践</section>'
            )
        }
        errors = validate_semantic_contracts(pages)
        self.assertTrue(any("missing loop stage: evidence" in error for error in errors), errors)

    def test_duplicate_stage_and_wrong_anchor_are_reported(self) -> None:
        pages = {
            "workflows.html": parse(
                '<section id="wrong" data-loop-stage="choose">选择</section>'
                '<section id="task-entry-copy" data-loop-stage="choose">再次选择</section>'
                '<section id="bounded-practice" data-loop-stage="practice">实践</section>'
                '<section id="acceptance-evidence" data-loop-stage="evidence">证据</section>'
                '<section id="recovery" data-loop-stage="recover">恢复</section>'
                '<section id="task-receipt" data-loop-stage="receipt">回执</section>'
            )
        }
        errors = validate_semantic_contracts(pages)
        self.assertTrue(any("duplicate loop stage: choose" in error for error in errors), errors)
        self.assertTrue(any("loop stage choose must use anchor #task-entry" in error for error in errors), errors)

    def test_unknown_case_type_and_label_mismatch_are_reported(self) -> None:
        pages = {
            "sample.html": parse(
                '<article id="case-a" data-case-type="story" data-case-id="case-a"><p>历史案例</p></article>'
                '<article id="case-b" data-case-type="demo" data-case-id="case-b"><p>历史案例</p></article>'
            )
        }
        errors = validate_semantic_contracts(pages)
        self.assertTrue(any("unknown case type: story" in error for error in errors), errors)
        self.assertTrue(any("case #case-b must visibly include 演示场景" in error for error in errors), errors)

        index_text = "| case-a | `sample.html#case-a` | 历史案例 | Git | 已复核 | 2026-07-11 | A3 | 边界 |"
        index_errors = validate_case_index(pages, index_text)
        self.assertFalse(any("case #case-a index type" in error for error in index_errors), index_errors)

    def test_case_label_must_be_inside_the_case_container(self) -> None:
        pages = {
            "sample.html": parse(
                '<p>历史案例</p><article id="case-a" data-case-type="historical" data-case-id="case-a">无标签正文</article>'
            )
        }
        errors = validate_semantic_contracts(pages)
        self.assertTrue(any("case #case-a must visibly include 历史案例" in error for error in errors), errors)

    def test_nested_same_tag_does_not_close_case_early(self) -> None:
        pages = {
            "sample.html": parse(
                '<section id="case-a" data-case-type="historical" data-case-id="case-a">'
                '<section>案例正文</section><p>历史案例</p></section>'
            )
        }
        errors = validate_semantic_contracts(pages)
        self.assertFalse(any("case #case-a" in error for error in errors), errors)

    def test_unclosed_and_mismatched_case_containers_are_reported(self) -> None:
        unclosed = {"sample.html": parse('<article id="case-a" data-case-type="demo" data-case-id="case-a">演示场景')}
        mismatched = {
            "sample.html": parse('<section id="case-b" data-case-type="historical" data-case-id="case-b">历史案例</article>')
        }
        self.assertTrue(
            any("unclosed case container #case-a" in error for error in validate_semantic_contracts(unclosed))
        )
        self.assertTrue(
            any("unclosed case container #case-b" in error for error in validate_semantic_contracts(mismatched))
        )

    def test_case_index_requires_one_exact_page_anchor(self) -> None:
        pages = {
            "sample.html": parse(
                '<article id="case-a" data-case-type="historical" data-case-id="case-a">历史案例</article>'
            )
        }
        row = "| case-a | `sample.html#case-a` | 历史案例 | Git | 已复核 | 2026-07-11 | A3 | 边界 |"
        missing = validate_case_index(pages, "")
        duplicate = validate_case_index(pages, f"{row}\n{row}")
        self.assertTrue(any("missing from evidence index" in error for error in missing), missing)
        self.assertTrue(any("duplicate page anchor" in error for error in duplicate), duplicate)

    def test_case_index_rejects_type_mismatch_and_orphan(self) -> None:
        pages = {
            "sample.html": parse(
                '<article id="case-a" data-case-type="demo" data-case-id="case-a">演示场景</article>'
            )
        }
        index_text = (
            "| case-a | `sample.html#case-a` | 历史案例 | Git | 已复核 | 2026-07-11 | A3 | 边界 |\n"
            "| orphan | `sample.html#missing` | 演示场景 | 上游说明 | 不需历史复核 | 2026-07-11 | A3 | 边界 |"
        )
        errors = validate_case_index(pages, index_text)
        self.assertTrue(any("index type must be 演示场景" in error for error in errors), errors)
        self.assertTrue(any("orphan page anchor" in error for error in errors), errors)

    def test_case_index_rejects_case_id_mismatch_and_invalid_anchor(self) -> None:
        pages = {
            "sample.html": parse(
                '<article id="case-a" data-case-type="historical" data-case-id="case-a">历史案例</article>'
            )
        }
        index_text = (
            "| wrong-id | `sample.html#case-a` | 历史案例 | Git | 已复核 | 2026-07-11 | A3 | 边界 |\n"
            "| malformed | `sample.htm#missing` | 演示场景 | 上游 | 不需历史复核 | 2026-07-11 | A3 | 边界 |"
        )
        errors = validate_case_index(pages, index_text)
        self.assertTrue(any("index Case ID must be case-a" in error for error in errors), errors)
        self.assertTrue(any("invalid page anchor" in error for error in errors), errors)

    def test_case_index_rejects_malformed_column_count(self) -> None:
        malformed = (
            "| extra | `sample.html#case-a` | 历史案例 | Git | 已复核 | "
            "2026-07-11 | A3 | 边界 | unexpected |"
        )
        errors = validate_case_index({}, malformed)
        self.assertTrue(any("malformed row has 9 columns" in error for error in errors), errors)

    def test_nested_html_fragment_is_checked(self) -> None:
        docs_dir = ROOT / "docs"
        with TemporaryDirectory(dir=docs_dir) as directory:
            target = Path(directory) / "nested.html"
            target.write_text('<html><body><h1 id="present">Nested</h1></body></html>', encoding="utf-8")
            rel = target.relative_to(ROOT).as_posix()
            pages = {rel: parse(target.read_text(encoding="utf-8"))}
            errors = check_local_link(ROOT / "index.html", f"{rel}#missing", pages)
        self.assertTrue(any("missing anchor #missing" in error for error in errors), errors)

    def test_required_fragment_backlink_is_reported(self) -> None:
        pages = {
            "engineering.html": parse('<section id="team-flow"></section><section id="team-case"></section>'),
            "goal.html": parse('<section id="real-example"></section>'),
        }
        errors = validate_semantic_contracts(pages)
        self.assertTrue(any("goal.html: missing required backlink" in error for error in errors), errors)

    def test_missing_required_page_is_reported_without_exception(self) -> None:
        errors = validate_required_pages({})
        self.assertTrue(any("missing required concept page" in error for error in errors), errors)
        self.assertTrue(any("missing required task/resource page" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
