import importlib.util
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "plain-english-writing" / "scripts" / "readability.py"
spec = importlib.util.spec_from_file_location("readability", SCRIPT)
readability = importlib.util.module_from_spec(spec)
spec.loader.exec_module(readability)


class ScoreTests(unittest.TestCase):
    def test_known_simple_sentence(self):
        # 6 words, 1 sentence, 6 syllables: the textbook values.
        r = readability.score("The cat sat on the mat.")
        self.assertEqual(r["words"], 6)
        self.assertEqual(r["sentences"], 1)
        self.assertAlmostEqual(r["reading_ease"], 116.1, places=1)
        self.assertAlmostEqual(r["grade"], -1.45, delta=0.1)

    def test_code_and_headings_are_ignored(self):
        md = "# Title\n\nRun the tool.\n\n```\nrm -rf /very/long/command --with many flags\n```\n"
        r = readability.score(md)
        self.assertEqual(r["words"], 3)
        self.assertEqual(r["sentences"], 1)

    def test_inline_code_and_links_count_as_one_word(self):
        r = readability.score("Run `vault-cli key create --name prod` now. See [the guide](https://example.com/x/y).")
        self.assertEqual(r["words"], 6)  # Run, code, now, See, the, guide

    def test_list_items_are_sentences(self):
        r = readability.score("1. Create the key\n2. Copy the key\n3. Save the key\n")
        self.assertEqual(r["sentences"], 3)

    def test_long_sentence_is_flagged(self):
        long = " ".join(["word"] * 30) + "."
        r = readability.score(long + " Short one.")
        self.assertEqual(r["long_sentences"], 1)
        self.assertEqual(r["longest"][0]["words"], 30)

    def test_harder_text_scores_worse(self):
        easy = readability.score("We fixed the bug. It was in the login form. Users can sign in now.")
        hard = readability.score("Notwithstanding considerable organisational complexity, the implementation "
                                 "necessitates comprehensive authentication infrastructure reconfiguration.")
        self.assertLess(hard["reading_ease"], easy["reading_ease"])
        self.assertGreater(hard["grade"], easy["grade"])

    def test_short_text_is_marked_unreliable(self):
        self.assertFalse(readability.score("Short text here.")["reliable"])

    def test_empty_input(self):
        self.assertEqual(readability.score("")["sentences"], 0)


class CliTests(unittest.TestCase):
    def run_cli(self, text, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], input=text,
                              capture_output=True, text=True)

    def test_cli_reports_and_exits_zero(self):
        p = self.run_cli("The cat sat on the mat. It was happy.")
        self.assertEqual(p.returncode, 0)
        self.assertIn("Reading Ease", p.stdout)
        self.assertIn("Longest sentences", p.stdout)

    def test_cli_json(self):
        p = self.run_cli("The cat sat on the mat.", "--json")
        self.assertIn('"reading_ease"', p.stdout)


if __name__ == "__main__":
    unittest.main()
