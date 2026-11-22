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


if __name__ == "__main__":
    unittest.main()
