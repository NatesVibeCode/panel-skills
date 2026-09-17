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
    def test_matching_tensions_win(self):
        proc = run_selector("--tensions", "risk,claims")
        self.assertEqual(proc.returncode, 0)
        room = json.loads(proc.stdout)["room"]
        self.assertEqual(room[0]["id"], "assumption-breaker")

    def test_diversity_one_per_family(self):
        proc = run_selector("--tensions", "risk,claims,conflict,decision",
                            "--size", "5")
        self.assertEqual(proc.returncode, 0)
        room = json.loads(proc.stdout)["room"]
        families = [p["family"] for p in room]
        self.assertEqual(len(families), len(set(families)))

    def test_diversity_beats_second_best_score(self):
        # 'human' matches nothing here but must still appear: no family repeats.
        proc = run_selector("--tensions", "measurement,metrics", "--size", "4")
        self.assertEqual(proc.returncode, 0)
        room = json.loads(proc.stdout)["room"]
        self.assertEqual(len(room), 4)
        self.assertEqual(room[0]["id"], "meter-checker")
        self.assertEqual(len({p["family"] for p in room}), 4)

    def test_size_bounds_rejected(self):
        self.assertEqual(run_selector("--tensions", "x", "--size", "2").returncode, 2)
        self.assertEqual(run_selector("--tensions", "x", "--size", "6").returncode, 2)

    def test_out_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "room.json")
            proc = run_selector("--tensions", "effort", "--out", out)
            self.assertEqual(proc.returncode, 0)
            with open(out) as fh:
                room = json.load(fh)["room"]
            self.assertEqual(room[0]["id"], "human")


if __name__ == "__main__":
    unittest.main()
