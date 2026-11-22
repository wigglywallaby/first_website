import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "story.html").read_text()


class StoryIntroTest(unittest.TestCase):
    def test_production_line_captions_are_removed(self):
        self.assertEqual(
            HTML.count("Illustrative story with made-up data."),
            0,
        )

    def test_production_line_check_forms_are_visible(self):
        line_step = re.search(r"\.line-step\s*\{([^}]*)\}", HTML, re.DOTALL)
        self.assertIsNotNone(line_step)
        self.assertIn("display: grid", line_step.group(1))
        self.assertIn(".paper-form", HTML)
        self.assertEqual(
            len(re.findall(r'<div class="paper-form(?:\s[^"]*)?"', HTML)),
            6,
        )

    def test_production_line_layout_and_stations(self):
        problem_list = re.search(r"\.problem-list\s*\{([^}]*)\}", HTML, re.DOTALL)
        self.assertIsNotNone(problem_list)
        self.assertIn(
            "grid-template-columns: repeat(3, minmax(0, 1fr))",
            problem_list.group(1),
        )

        mobile_media = re.search(
            r"@media\s*\(max-width:\s*700px\)\s*\{",
            HTML,
        )
        self.assertIsNotNone(mobile_media)
        mobile_problem_list = re.search(
            r"\.problem-list\s*\{([^}]*)\}",
            HTML[mobile_media.start():],
            re.DOTALL,
        )
        self.assertIsNotNone(mobile_problem_list)
        self.assertIn(
            "grid-template-columns: 1fr",
            mobile_problem_list.group(1),
        )

        for station in ("incoming", "fill", "seal", "bestby", "packaging", "finished"):
            with self.subTest(station=station):
                self.assertIn(f'data-station="{station}"', HTML)

    def test_intro_has_six_stage_paper_stack_and_accessible_copy(self):
        intro = re.search(r'<section[^>]+id="intro"[^>]*>(.*?)</section>', HTML, re.DOTALL)
        self.assertIsNotNone(intro)

        markup = intro.group(1)
        self.assertIn('class="paper-stack-intro"', markup)
        self.assertIn('aria-label="Six paper checks from a production line"', markup)
        self.assertIn('href="#the-line"', markup)

        stages = re.findall(r'data-stage="([^"]+)"', markup)
        self.assertEqual(
            stages,
            ["Incoming", "Fill", "Seal", "Best By", "Packaging", "Finished Case"],
        )

    def test_intro_has_reduced_motion_fallback(self):
        self.assertRegex(
            HTML,
            r"@media\s*\(prefers-reduced-motion:\s*reduce\)",
        )
        self.assertIn(".paper-stack-copy", HTML)
        self.assertIn(".paper-sheet", HTML)
        reduced_motion = re.search(
            r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{(.*)",
            HTML,
            re.DOTALL,
        )
        self.assertIsNotNone(reduced_motion)
        fallback = reduced_motion.group(1)
        sheet_fallback = re.search(
            r"\.js\s+\.(?:paper-sheet|paper-stack-copy)[^}]*",
            fallback,
        )
        self.assertIsNotNone(sheet_fallback)
        self.assertNotIn("transform: none", sheet_fallback.group(0))

    def test_line_markers_keep_scroll_rhythm_and_articles_are_hidden(self):
        marker = re.search(r"\.step-marker\s*\{([^}]*)\}", HTML, re.DOTALL)
        self.assertIsNotNone(marker)
        self.assertIn("height: 58vh", marker.group(1))
        self.assertEqual(HTML.count('data-step-marker="incoming"'), 1)
        self.assertEqual(HTML.count('data-step-marker="fill"'), 1)
        self.assertEqual(HTML.count('data-step-marker="seal"'), 1)
        self.assertEqual(HTML.count('data-step-marker="bestby"'), 1)
        self.assertEqual(HTML.count('data-step-marker="packaging"'), 1)
        self.assertEqual(HTML.count('data-step-marker="finished"'), 1)

    def test_paper_handoff_and_bullet_layout_are_present(self):
        self.assertIn('lineSection.classList.add("is-transitioned")', HTML)
        self.assertIn('clone.className = "paper-handoff-clone"', HTML)
        self.assertIn('const source = sheet.getBoundingClientRect()', HTML)
        self.assertIn('const destination = icon.getBoundingClientRect()', HTML)

        problem_li = re.search(r"\.problem-list li\s*\{([^}]*)\}", HTML, re.DOTALL)
        self.assertIsNotNone(problem_li)
        self.assertIn("text-align: left", problem_li.group(1))
        self.assertIn("white-space: normal", problem_li.group(1))

    def test_opening_and_line_layout_enter_earlier(self):
        intro = re.search(r"#intro\s*\{([^}]*)\}", HTML, re.DOTALL)
        self.assertIsNotNone(intro)
        self.assertIn("min-height: 90svh", intro.group(1))

        line_story = re.search(r"\.line-story\s*\{([^}]*)\}", HTML, re.DOTALL)
        self.assertIsNotNone(line_story)
        self.assertIn("min-height: auto", line_story.group(1))

        line_heading = re.search(r"\.line-heading\s*\{([^}]*)\}", HTML, re.DOTALL)
        self.assertIsNotNone(line_heading)
        self.assertRegex(line_heading.group(1), r"padding-top:\s*24px")
        self.assertRegex(line_heading.group(1), r"padding-bottom:\s*8px")

        mobile = re.search(r"@media\s*\(max-width:\s*700px\)\s*\{", HTML)
        self.assertIsNotNone(mobile)
        mobile_heading = re.search(
            r"\.line-heading\s*\{([^}]*)\}",
            HTML[mobile.start():],
            re.DOTALL,
        )
        self.assertIsNotNone(mobile_heading)
        self.assertRegex(mobile_heading.group(1), r"padding-top:\s*24px")

    def test_reverse_paper_handoff_function_and_stage_mappings_exist(self):
        reverse_function = re.search(
            r"function\s+runPaperReverseHandoff\s*\(\s*\)\s*\{(.*?)\n      }",
            HTML,
            re.DOTALL,
        )
        self.assertIsNotNone(reverse_function)
        reverse_logic = reverse_function.group(1)

        mappings = (
            ("Incoming", "incoming"),
            ("Fill", "fill"),
            ("Seal", "seal"),
            ("Best By", "bestby"),
            ("Packaging", "packaging"),
            ("Finished Case", "finished"),
        )
        for stage, station in mappings:
            with self.subTest(stage=stage, station=station):
                self.assertRegex(
                    reverse_logic,
                    rf'["\']{re.escape(stage)}["\']\s*,\s*["\']{re.escape(station)}["\']',
                )
        self.assertIn('if (reducedMotion)', reverse_logic)
        self.assertIn('.station[data-station="${station}"] .form-icon', reverse_logic)
        self.assertIn('.paper-sheet[data-stage="${stage}"]', reverse_logic)
        self.assertIn('clone.style.position = "fixed"', reverse_logic)
        self.assertIn('fill: "both"', reverse_logic)
        self.assertIn("animation.finished", reverse_logic)
        self.assertIn(".catch(() => clone.remove())", reverse_logic)
        self.assertIn("clone.remove();", reverse_logic)

    def test_reverse_handoff_observer_reverses_on_upward_entry_before_forward_entry(self):
        observer = re.search(
            r"const\s+lineTransitionObserver\s*=\s*new\s+IntersectionObserver"
            r"\s*\(\s*\(entries(?:,\s*observer)?\)\s*=>\s*\{"
            r"(.*?)\n\s*\}\s*,\s*\{\s*threshold",
            HTML,
            re.DOTALL,
        )
        self.assertIsNotNone(observer)
        observer_logic = observer.group(1)

        entry_logic = re.search(
            r"if\s*\(\s*entry\.isIntersecting\s*\)\s*\{(.*?)\n\s*\}",
            observer_logic,
            re.DOTALL,
        )
        self.assertIsNotNone(entry_logic)
        entry_branch = entry_logic.group(1)
        upward_entry = re.search(
            r"if\s*\([\s\S]*?window\.scrollY\s*<\s*previousScrollY"
            r"[\s\S]*?lineEntered"
            r"[\s\S]*?entry\.boundingClientRect\.top\s*>\s*0"
            r"[\s\S]*?\)\s*\{",
            entry_branch,
        )
        self.assertIsNotNone(upward_entry)
        self.assertIn('lineSection.classList.remove("is-transitioned")', entry_branch)
        self.assertIn("handoffStarted = false;", entry_branch)
        self.assertIn("lineEntered = false;", entry_branch)
        self.assertRegex(
            entry_branch,
            r"if\s*\(\s*!reducedMotion\s*\)\s*\{",
        )
        self.assertIn("runPaperReverseHandoff()", entry_branch)
        self.assertRegex(
            observer_logic,
            r"\belse\s*\{\s*"
            r"lineEntered\s*=\s*true;\s*"
            r'lineSection\.classList\.add\("is-transitioned"\);\s*'
            r"if\s*\(\s*!handoffStarted\s*\)",
        )

    def test_reverse_handoff_observer_and_scroll_listener_reverse_at_boundaries(self):
        threshold = re.search(
            r"const\s+lineTransitionObserver\s*=\s*new\s+IntersectionObserver"
            r".*?\{\s*threshold\s*:\s*([0-9.]+)\s*\}",
            HTML,
            re.DOTALL,
        )
        self.assertIsNotNone(threshold)
        self.assertLessEqual(float(threshold.group(1)), 0.01)

        observer = re.search(
            r"const\s+lineTransitionObserver\s*=\s*new\s+IntersectionObserver"
            r"\s*\(\s*\(entries(?:,\s*observer)?\)\s*=>\s*\{"
            r"(.*?)\n\s*\}\s*,\s*\{\s*threshold",
            HTML,
            re.DOTALL,
        )
        self.assertIsNotNone(observer)
        observer_logic = observer.group(1)

        self.assertIn("entry.isIntersecting", observer_logic)
        self.assertIn("runPaperReverseHandoff()", observer_logic)
        self.assertIn("previousScrollY", HTML)
        self.assertIn("handoffStarted", HTML)
        self.assertIn("lineEntered", HTML)
        self.assertRegex(
            observer_logic,
            r"entry\.boundingClientRect\.bottom\s*<=\s*0",
        )
        self.assertRegex(observer_logic, r"window\.scrollY\s*<\s*previousScrollY")
        self.assertRegex(observer_logic, r"previousScrollY\s*=\s*window\.scrollY")
        self.assertIn('lineSection.classList.remove("is-transitioned")', observer_logic)
        self.assertNotIn("unobserve(lineSection)", observer_logic)
        self.assertIn('lineSection.classList.add("is-transitioned")', observer_logic)
        self.assertRegex(observer_logic, r"if\s*\(!reducedMotion\)\s*\{\s*runPaperHandoff\(\);")

        exit_logic_match = re.search(
            r"if\s*\(\s*!entry\.isIntersecting\s*\)\s*\{(.*?)\n\s*\}",
            observer_logic,
            re.DOTALL,
        )
        self.assertIsNotNone(exit_logic_match)
        exit_logic = exit_logic_match.group(1)
        captured_line_entered = re.search(
            r"(?:const|let)\s+(\w+)\s*=\s*lineEntered",
            exit_logic,
        )
        self.assertIsNotNone(captured_line_entered)
        prior_line_entered = captured_line_entered.group(1)
        reset_handoff = re.search(r"handoffStarted\s*=\s*false", exit_logic)
        reset_line = re.search(r"lineEntered\s*=\s*false", exit_logic)
        reverse_decision = re.search(
            rf"if\s*\([^)]*\b{re.escape(prior_line_entered)}\b[^)]*"
            r"entry\.boundingClientRect\.bottom\s*<=\s*0"
            r"[^)]*window\.scrollY\s*<\s*previousScrollY",
            exit_logic,
            re.DOTALL,
        )
        self.assertIsNotNone(reset_handoff)
        self.assertIsNotNone(reset_line)
        self.assertIsNotNone(reverse_decision)
        self.assertLess(captured_line_entered.start(), reset_handoff.start())
        self.assertLess(captured_line_entered.start(), reset_line.start())
        self.assertLess(reset_handoff.start(), reverse_decision.start())
        self.assertLess(reset_line.start(), reverse_decision.start())
        self.assertIn("runPaperReverseHandoff()", exit_logic[reverse_decision.start():])
        self.assertIn(
            'lineSection.classList.remove("is-transitioned")',
            exit_logic[reverse_decision.start():],
        )

        no_observer_fallback = re.search(
            r"\}\s*else\s*\{\s*lineSection\.classList\.add\(\"is-transitioned\"\);\s*\}",
            HTML,
        )
        self.assertIsNotNone(no_observer_fallback)

        listener = re.search(
            r"window\.addEventListener\(\s*\"scroll\",\s*\(\)\s*=>\s*\{"
            r"(.*?)\n\s*\},\s*\{\s*passive:\s*true\s*\}\s*,?\s*\)",
            HTML,
            re.DOTALL,
        )
        self.assertIsNotNone(listener)
        listener_logic = listener.group(1)
        self.assertRegex(
            listener_logic,
            r"lineEntered\s*&&\s*scrollingUp\s*&&\s*window\.scrollY\s*<\s*200",
        )
        self.assertIn('lineSection.classList.remove("is-transitioned")', listener_logic)
        self.assertIn("runPaperReverseHandoff()", listener_logic)
        self.assertIn("handoffStarted = false;", listener_logic)
        self.assertIn("lineEntered = false;", listener_logic)
        self.assertRegex(HTML, r"let\s+lineEntered\s*=\s*false")
        self.assertRegex(HTML, r"let\s+handoffStarted\s*=\s*false")
        self.assertRegex(HTML, r"let\s+previousScrollY\s*=\s*window\.scrollY")
        observer_start = HTML.index("const lineTransitionObserver")
        for declaration in (
            "let previousScrollY = window.scrollY;",
            "let handoffStarted = false;",
            "let lineEntered = false;",
        ):
            with self.subTest(declaration=declaration):
                self.assertLess(HTML.index(declaration), observer_start)
        self.assertRegex(
            listener_logic,
            r"if\s*\(!reducedMotion\)\s*\{\s*"
            r'lineSection\.classList\.remove\("is-transitioned"\);\s*'
            r"runPaperReverseHandoff\(\);",
        )

    def test_reverse_handoff_respects_reduced_motion(self):
        reverse_function = re.search(
            r"function\s+runPaperReverseHandoff\s*\(\s*\)\s*\{(.*?)\n      }",
            HTML,
            re.DOTALL,
        )
        self.assertIsNotNone(reverse_function)
        reverse_logic = reverse_function.group(1)

        guard = re.search(
            r"\bif\s*\(\s*reducedMotion\s*\)\s*\{\s*return;\s*\}",
            reverse_logic,
        )
        self.assertIsNotNone(guard)

        observer = re.search(
            r"const\s+lineTransitionObserver\s*=\s*new\s+IntersectionObserver"
            r"\s*\(\s*\(entries(?:,\s*observer)?\)\s*=>\s*\{"
            r"(.*?)\n\s*\}\s*,\s*\{\s*threshold",
            HTML,
            re.DOTALL,
        )
        self.assertIsNotNone(observer)
        exit_logic = re.search(
            r"if\s*\(\s*!entry\.isIntersecting\s*\)\s*\{(.*?)\n\s*\}",
            observer.group(1),
            re.DOTALL,
        )
        self.assertIsNotNone(exit_logic)
        self.assertRegex(
            exit_logic.group(1),
            r"if\s*\(\s*wasLineEntered\s*&&"
            r"\s*entry\.boundingClientRect\.bottom\s*<=\s*0"
            r"\s*&&\s*window\.scrollY\s*<\s*previousScrollY\s*\)\s*\{"
            r"\s*if\s*\(\s*!reducedMotion\s*\)\s*\{"
            r"\s*lineSection\.classList\.remove\(\"is-transitioned\"\);"
            r"\s*runPaperReverseHandoff\(\);",
        )

if __name__ == "__main__":
    unittest.main()
