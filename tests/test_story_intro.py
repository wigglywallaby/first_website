import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "story.html").read_text()


class StoryIntroTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
