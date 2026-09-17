import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


def run_selector(*args):
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "select_room.py"), *args],
        capture_output=True, text=True,
    )
    return proc


class SelectTest(unittest.TestCase):
    def test_roster_loads(self):
        with open(os.path.join(HERE, "panelists.json")) as fh:
            panelists = json.load(fh)["panelists"]
        self.assertGreater(len(panelists), 100)
        for p in panelists:
            for key in ("name", "id", "lens", "attributes", "family", "tags"):
                self.assertIn(key, p)
        ids = [p["id"] for p in panelists]
        self.assertEqual(len(ids), len(set(ids)))

    def test_matching_tensions_win(self):
        proc = run_selector("--tensions", "threat,model,attacker")
        self.assertEqual(proc.returncode, 0)
        room = json.loads(proc.stdout)["room"]
        self.assertEqual(room[0]["name"], "Aisha Rahman")
        self.assertEqual(room[0]["score"], 3)

    def test_diversity_one_per_family(self):
        proc = run_selector("--tensions", "risk", "--size", "5")
        self.assertEqual(proc.returncode, 0)
        room = json.loads(proc.stdout)["room"]
        families = [p["family"] for p in room]
        self.assertEqual(len(families), len(set(families)))

    def test_diversity_fills_beyond_matches(self):
        proc = run_selector("--tensions", "threat,model,attacker",
                            "--size", "4")
        self.assertEqual(proc.returncode, 0)
        room = json.loads(proc.stdout)["room"]
        self.assertEqual(len(room), 4)
        self.assertEqual(len({p["family"] for p in room}), 4)

    def test_size_bounds_rejected(self):
        self.assertEqual(run_selector("--tensions", "x", "--size", "2").returncode, 2)
        self.assertEqual(run_selector("--tensions", "x", "--size", "6").returncode, 2)

    def test_out_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "room.json")
            proc = run_selector("--tensions", "risk", "--out", out)
            self.assertEqual(proc.returncode, 0)
            with open(out) as fh:
                room = json.load(fh)["room"]
            self.assertTrue(room)
            self.assertIn("name", room[0])


if __name__ == "__main__":
    unittest.main()
