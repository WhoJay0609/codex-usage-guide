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
    validate_presentation_contracts,
    validate_product_accuracy_contracts,
    validate_interaction_contracts,
    manifest_html_paths,
    validate_metadata_contracts,
    validate_required_pages,
    validate_semantic_contracts,
)


def parse(markup: str) -> PageParser:
    parser = PageParser()
    parser.source_text = markup
    parser.feed(markup)
    return parser


class SemanticContractTests(unittest.TestCase):
    def test_product_accuracy_contract_rejects_obsolete_scheduled_task_terminology(self) -> None:
        pages = {
            "automation.html": parse("<main>Triage inbox</main>"),
        }

        errors = validate_product_accuracy_contracts(pages)

        self.assertTrue(
            any("obsolete Scheduled tasks terminology" in error for error in errors),
            errors,
        )

    def test_product_accuracy_contract_rejects_codex_desktop_automations_terminology(self) -> None:
        pages = {
            "automation.html": parse("<main>Codex Desktop Automations</main>"),
        }

        errors = validate_product_accuracy_contracts(pages)

        self.assertTrue(
            any("obsolete Scheduled tasks terminology" in error for error in errors),
            errors,
        )

    def test_product_accuracy_contract_rejects_plain_automations_product_name(self) -> None:
        for text in ("Automations", "Automation prompt: inspect the diff"):
            with self.subTest(text=text):
                errors = validate_product_accuracy_contracts(
                    {"automation.html": parse(f"<main>{text}</main>")}
                )
                self.assertTrue(
                    any("obsolete Scheduled tasks terminology" in error for error in errors),
                    errors,
                )

    def test_product_accuracy_contract_rejects_one_missing_permission_mode(self) -> None:
        pages = {
            "permissions.html": parse(
                "<main>Ask for approval Approve for me Full access</main>"
            ),
        }

        errors = validate_product_accuracy_contracts(pages)

        self.assertEqual(
            [
                "permissions.html: permission modes missing visible label: "
                "Custom (config.toml)"
            ],
            errors,
        )

    def test_hidden_permission_labels_do_not_count_as_visible(self) -> None:
        pages = {
            "permissions.html": parse(
                "<main>"
                "<section hidden>Ask for approval <span>Approve for me</span></section>"
                '<section aria-hidden="true">Full access '
                "<span>Custom (config.toml)</span></section>"
                "<p>Reader-visible text after hidden containers.</p>"
                "</main>"
            ),
        }

        errors = validate_product_accuracy_contracts(pages)

        self.assertEqual(len(errors), 4, errors)
        for mode in (
            "Ask for approval",
            "Approve for me",
            "Full access",
            "Custom (config.toml)",
        ):
            self.assertTrue(any(mode in error for error in errors), errors)
        self.assertIn("Reader-visible text", pages["permissions.html"].visible_text())

    def test_product_accuracy_contract_checks_visible_decoded_skill_syntax(self) -> None:
        encoded = {"skills.html": parse("<main>&#91;$refine-user-prompt&#93;</main>")}
        split_across_inline_markup = {
            "skills.html": parse("<main>[$<span>refine-user-prompt</span>]</main>")
        }
        commented = {
            "skills.html": parse("<!-- [$refine-user-prompt] --><main>Use $refine-user-prompt.</main>")
        }
        hidden = {
            "skills.html": parse("<main hidden>[$<span>refine-user-prompt</span>]</main>")
        }

        self.assertTrue(
            any(
                "invalid skill mention syntax" in error
                for error in validate_product_accuracy_contracts(encoded)
            )
        )
        self.assertTrue(
            any(
                "invalid skill mention syntax" in error
                for error in validate_product_accuracy_contracts(split_across_inline_markup)
            )
        )
        self.assertEqual(validate_product_accuracy_contracts(commented), [])
        self.assertEqual(validate_product_accuracy_contracts(hidden), [])

    def test_native_recommended_boundaries_are_page_scoped(self) -> None:
        missing = {
            "workflows.html": "receipt",
            "engineering.html": "A2 A3 A4 grant",
            "goal.html": (
                "Goal template: Objective Scope Acceptance Validation Artifacts "
                "Stop Conditions"
            ),
        }
        qualified = {
            "workflows.html": "receipt 是本指南推荐的任务收口实践",
            "engineering.html": (
                "A2/A3/A4 是本指南的教学框架；"
                "grant 是提示词层面的授权约定"
            ),
            "goal.html": "六字段 Goal 模板是本指南推荐的提示词结构",
        }

        for rel, text in missing.items():
            with self.subTest(page=rel, qualifier="missing"):
                errors = validate_product_accuracy_contracts(
                    {rel: parse(f"<main>{text}</main>")}
                )
                self.assertTrue(
                    any("native/recommended boundary" in error for error in errors),
                    errors,
                )

        for rel, text in qualified.items():
            with self.subTest(page=rel, qualifier="present"):
                self.assertEqual(
                    validate_product_accuracy_contracts(
                        {rel: parse(f"<main>{text}</main>")}
                    ),
                    [],
                )

        self.assertEqual(
            validate_product_accuracy_contracts(
                {"historical-example.html": parse("<main>A2 grant receipt</main>")}
            ),
            [],
        )

    def test_native_recommended_boundary_rejects_unrelated_guide_wording(self) -> None:
        unrelated = {
            "workflows.html": "receipt。本指南还有其他建议。",
            "engineering.html": "A2 A3 A4 grant。本指南面向桌面端读者。",
            "goal.html": (
                "Goal template: Objective Scope Acceptance Validation Artifacts "
                "Stop Conditions。本指南提供示例。"
            ),
        }

        for rel, text in unrelated.items():
            with self.subTest(page=rel):
                errors = validate_product_accuracy_contracts(
                    {rel: parse(f"<main>{text}</main>")}
                )
                self.assertTrue(
                    any("native/recommended boundary" in error for error in errors),
                    errors,
                )

    def test_hidden_native_boundary_signal_does_not_satisfy_contract(self) -> None:
        hidden_containers = (
            "<aside hidden>{text}</aside>",
            "<template>{text}</template>",
            '<aside style="display: none">{text}</aside>',
            '<aside style="visibility:hidden">{text}</aside>',
        )
        for container in hidden_containers:
            with self.subTest(container=container):
                pages = {
                    "workflows.html": parse(
                        "<main><p>receipt</p>"
                        + container.format(text="receipt 是本指南推荐的任务收口实践")
                        + "</main>"
                    )
                }
                errors = validate_product_accuracy_contracts(pages)
                self.assertTrue(
                    any("native/recommended boundary" in error for error in errors),
                    errors,
                )

    def test_product_accuracy_contract_rejects_singular_automation_product_name(self) -> None:
        errors = validate_product_accuracy_contracts(
            {"automation.html": parse("<main>Open Automation settings.</main>")}
        )
        self.assertTrue(any("obsolete Scheduled tasks" in error for error in errors), errors)

    def test_product_accuracy_contract_accepts_current_product_terminology(self) -> None:
        pages = {
            "permissions.html": parse(
                "<main>Ask for approval Approve for me Full access "
                "Custom (config.toml)</main>"
            ),
            "automation.html": parse(
                "<main>Scheduled tasks（定时任务）；在 Scheduled 视图查看结果。</main>"
            ),
            "skills.html": parse("<main>Use $refine-user-prompt before execution.</main>"),
        }

        self.assertEqual(validate_product_accuracy_contracts(pages), [])

    def test_manifest_html_paths_excludes_nested_docs_html(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("public", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs/ideation.html").write_text("internal", encoding="utf-8")
            self.assertEqual(manifest_html_paths(root, ["index.html"]), [root / "index.html"])

    def test_metadata_contract_rejects_missing_social_head_and_generic_kicker(self) -> None:
        pages = {
            "sample.html": parse(
                '<html><head><title>示例</title><meta name="description" content="描述"></head>'
                '<body><main><p class="section-kicker">Examples</p><h1>示例</h1></main></body></html>'
            )
        }
        manifest_pages = {"sample.html": {"title": "示例", "description": "描述"}}
        errors = validate_metadata_contracts(
            pages,
            manifest_pages,
            "https://example.test/",
            "figures/social-preview.png",
        )
        self.assertTrue(any("missing canonical metadata" in error for error in errors), errors)
        self.assertTrue(any("generic kicker must be Chinese-first" in error for error in errors), errors)

    def test_presentation_contract_rejects_late_theme_unsafe_external_and_global_mermaid(self) -> None:
        markup = (
            '<link rel="stylesheet" href="assets/site.css"><script src="assets/theme.js"></script>'
            '<select class="theme-select"></select><main>'
            '<a href="https://example.com">外部</a></main>'
            '<script src="https://cdn.jsdelivr.net/npm/mermaid@11.14.0/dist/mermaid.min.js"></script>'
        )
        errors = validate_presentation_contracts(
            {"sample.html": parse(markup)}, {"sample.html"}, "https://guide.example/"
        )
        self.assertTrue(any("theme bootstrap" in error for error in errors), errors)
        self.assertTrue(any("unsafe cross-origin" in error for error in errors), errors)
        self.assertTrue(any("Mermaid runtime" in error for error in errors), errors)

    def test_interaction_contract_requires_search_and_matching_permalinks(self) -> None:
        pages = {
            "sample.html": parse(
                '<script src="assets/site-data.js"></script>'
                '<a href="#main-content">跳到正文</a>'
                '<button class="search-trigger"></button>'
                '<dialog id="site-search-dialog" role="dialog"></dialog>'
                '<input id="site-search-input" role="combobox">'
                '<ul id="site-search-results" role="listbox"></ul>'
                '<main id="main-content"><h2 id="canonical">Title<a data-heading-permalink href="#wrong">#</a></h2></main>'
            )
        }
        errors = validate_interaction_contracts(pages)
        self.assertTrue(any("permalink for #canonical must target #canonical" in error for error in errors), errors)

    def test_interaction_contract_allows_stable_headings_inside_link_cards(self) -> None:
        pages = {
            "sample.html": parse(
                '<script src="assets/site-data.js"></script>'
                '<a href="#main-content">跳到正文</a>'
                '<button class="search-trigger"></button>'
                '<dialog id="site-search-dialog" role="dialog"></dialog>'
                '<input id="site-search-input" role="combobox">'
                '<ul id="site-search-results" role="listbox"></ul>'
                '<main id="main-content"><a class="source-card" href="next.html"><h3 id="card">Title</h3><p>Summary</p></a></main>'
            )
        }
        self.assertEqual(validate_interaction_contracts(pages), [])

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
