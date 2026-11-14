"""Unit tests for the stdlib parts of the bot. Run: python -m unittest discover -s bot/tests"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
_tmp = tempfile.TemporaryDirectory()
os.environ["REPO_DIR"] = str(Path(_tmp.name) / "repo")
os.environ["STATE_DIR"] = str(Path(_tmp.name) / "state")
sys.path[:0] = [str(HERE.parent / "common"), str(HERE.parent / "publisher")]

import pinstore as ps  # noqa: E402
from validate import secret_findings, validate_reference  # noqa: E402
import build_catalog  # noqa: E402

GOOD_REF = """# x: UI/UX patterns
## Directions
### Calm
- **Seen in:** https://www.pinterest.com/pin/1234567/
## Do / Don't
- Do use #1A1A1A text
## Source pins
- https://www.pinterest.com/pin/1234567/ - card rhythm
"""


class MergeBatch(unittest.TestCase):
    def test_new_pins_are_added_once_with_canonical_url(self):
        store = {"pins": {}}
        new = ps.merge_batch(store, "dashboard", "q1", "2026-11-14",
                             [{"id": "1234567", "title": "This may contain: a  dark   dashboard"}])
        self.assertEqual(new, ["1234567"])
        rec = store["pins"]["1234567"]
        self.assertEqual(rec["url"], "https://www.pinterest.com/pin/1234567/")
        self.assertEqual(rec["title"], "a dark dashboard")

    def test_same_pin_in_second_category_is_merged_not_duplicated(self):
        store = {"pins": {}}
        ps.merge_batch(store, "dashboard", "q1", "d", [{"id": "1234567"}])
        new = ps.merge_batch(store, "dark-mode", "q2", "d", [{"id": "1234567"}])
        self.assertEqual(new, [])
        self.assertEqual(store["pins"]["1234567"]["categories"], ["dashboard", "dark-mode"])

    def test_non_numeric_ids_are_ignored(self):
        store = {"pins": {}}
        new = ps.merge_batch(store, "dashboard", "q", "d",
                             [{"id": "../../etc"}, {"id": "12"}, {"id": None}])
        self.assertEqual(new, [])
        self.assertEqual(store["pins"], {})

    def test_bad_category_is_rejected(self):
        with self.assertRaises(ValueError):
            ps.merge_batch({"pins": {}}, "../x", "q", "d", [])

    def test_long_title_is_truncated(self):
        store = {"pins": {}}
        ps.merge_batch(store, "dashboard", "q", "d", [{"id": "1234567", "title": "a" * 1000}])
        self.assertEqual(len(store["pins"]["1234567"]["title"]), 220)


class Pending(unittest.TestCase):
    def test_only_unanalyzed_pins_with_thumbnails_are_pending(self):
        ps.THUMBS.mkdir(parents=True, exist_ok=True)
        store = {"pins": {}}
        ps.merge_batch(store, "fintech", "q", "d", [{"id": "1111111"}, {"id": "2222222"}, {"id": "3333333"}])
        (ps.THUMBS / "1111111.jpg").write_bytes(b"x")
        (ps.THUMBS / "2222222.jpg").write_bytes(b"x")
        analysis = {"categories": {"fintech": {"analyzed": ["2222222"]}}}
        self.assertEqual(ps.pending_for("fintech", store, analysis), ["1111111"])


class PruneThumbs(unittest.TestCase):
    def setUp(self):
        ps.THUMBS.mkdir(parents=True, exist_ok=True)
        for f in ps.THUMBS.glob("*.jpg"):
            f.unlink()

    def test_preview_kept_until_every_category_has_analyzed_it(self):
        store = {"pins": {}}
        ps.merge_batch(store, "dashboard", "q", "d", [{"id": "5555555"}])
        ps.merge_batch(store, "dark-mode", "q", "d", [{"id": "5555555"}])
        (ps.THUMBS / "5555555.jpg").write_bytes(b"x")
        half = {"categories": {"dashboard": {"analyzed": ["5555555"]}}}
        self.assertEqual(ps.prune_thumbs(store, half), 0)
        self.assertTrue((ps.THUMBS / "5555555.jpg").exists())
        full = {"categories": {"dashboard": {"analyzed": ["5555555"]}, "dark-mode": {"analyzed": ["5555555"]}}}
        self.assertEqual(ps.prune_thumbs(store, full), 1)
        self.assertFalse((ps.THUMBS / "5555555.jpg").exists())

    def test_unknown_files_are_left_alone(self):
        (ps.THUMBS / "6666666.jpg").write_bytes(b"x")
        self.assertEqual(ps.prune_thumbs({"pins": {}}, {"categories": {}}), 0)
        self.assertTrue((ps.THUMBS / "6666666.jpg").exists())


class ValidateReference(unittest.TestCase):
    def test_good_reference_passes(self):
        self.assertEqual(validate_reference(GOOD_REF, {"1234567"}), [])

    def test_missing_section_fails(self):
        problems = validate_reference(GOOD_REF.replace("## Do / Don't", ""), {"1234567"})
        self.assertTrue(any("Do / Don't" in p for p in problems))

    def test_non_pinterest_link_fails(self):
        problems = validate_reference(GOOD_REF + "\nhttps://evil.example/x\n", {"1234567"})
        self.assertTrue(any("non-pin link" in p for p in problems))

    def test_unknown_pin_fails(self):
        problems = validate_reference(GOOD_REF, {"999999"})
        self.assertTrue(any("unknown pin" in p for p in problems))

    def test_secret_shapes_fail(self):
        for leak in ("sk-ant-api03-abcdefghijklmnop", "ghp_" + "a" * 30,
                     "-----BEGIN OPENSSH PRIVATE KEY-----", "x" * 60, "/proc/self/environ"):
            with self.subTest(leak=leak[:12]):
                self.assertTrue(validate_reference(GOOD_REF + leak, {"1234567"}))

    def test_hex_colours_and_pin_ids_are_not_secrets(self):
        self.assertEqual(secret_findings("#0F172A #E60023 pin 1127307350515930552"), [])

    def test_script_tag_fails(self):
        self.assertTrue(validate_reference(GOOD_REF + "<script>x</script>", {"1234567"}))


class Catalog(unittest.TestCase):
    def test_titles_cannot_break_out_of_the_data_script(self):
        ps.DATA.mkdir(parents=True, exist_ok=True)
        ps.write_json(ps.TOPICS, {"categories": [{"category": "dashboard", "queries": ["q"]}]})
        store = {"pins": {}}
        ps.merge_batch(store, "dashboard", "q", "d", [{"id": "1234567", "title": "</script><img src=x onerror=alert(1)>"}])
        ps.write_json(ps.PINS, store)
        build_catalog.build()
        html = (ps.SKILL / "catalog.html").read_text(encoding="utf-8")
        self.assertNotIn("</script><img", html)
        data = html.split('type="application/json">', 1)[1].split("</script>", 1)[0]
        self.assertEqual(json.loads(data)["pins"][0]["title"], "</script><img src=x onerror=alert(1)>")
        index = (ps.REFS / "README.md").read_text(encoding="utf-8")
        self.assertIn("| dashboard (not yet) | 1 | 0 | - |", index)


if __name__ == "__main__":
    unittest.main()
