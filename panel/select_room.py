"""Select a panel room by semantic tag match with enforced diversity.

Reads the panelists table from the skillflow session DB (SKILLFLOW_DB),
ranks panelists by token-overlap between the situation's tensions and each
panelist's tags, then enforces diversity: at most one panelist per family,
three to five seats. Score proposes; diversity disposes.

Usage:
    SKILLFLOW_DB=./session1/skillflow.db python3 select_room.py --tensions risk,measurement
"""

import argparse
import json
import os
import sqlite3
import sys

MIN_SEATS, MAX_SEATS = 3, 5


def tokens(text: str) -> set:
    return {t for t in text.lower().replace("-", " ").replace("_", " ").split() if t}


def score(tensions: list, tags: list) -> int:
    tension_tokens = set()
    for t in tensions:
        tension_tokens |= tokens(t)
    hits = 0
    for tag in tags:
        tag_tokens = tokens(tag)
        if tag_tokens & tension_tokens:
            hits += len(tag_tokens & tension_tokens)
    return hits


def select(panelists: list, tensions: list, size: int) -> list:
    ranked = sorted(
        panelists,
        key=lambda p: (-score(tensions, p["tags"]), p["id"]),
    )
    room, used_families = [], set()
    for candidate in ranked:
        if len(room) >= size:
            break
        if candidate["family"] in used_families:
            continue
        room.append(candidate)
        used_families.add(candidate["family"])
    return room


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Select a panel room.")
    parser.add_argument("--tensions", default="",
                        help="comma-separated situation tensions")
    parser.add_argument("--size", type=int, default=4)
    parser.add_argument("--db", default=os.environ.get("SKILLFLOW_DB"),
                        help="skillflow session DB (default: $SKILLFLOW_DB)")
    parser.add_argument("--out", default=None, help="write room JSON here")
    args = parser.parse_args(argv)

    if not (MIN_SEATS <= args.size <= MAX_SEATS):
        print(f"error: --size must be {MIN_SEATS}-{MAX_SEATS}", file=sys.stderr)
        return 2
    if not args.db:
        print("error: no session DB; set SKILLFLOW_DB or pass --db",
              file=sys.stderr)
        return 2
    try:
        conn = sqlite3.connect(args.db)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, name, lens, attributes, family, tags FROM panelists"
        ).fetchall()
        conn.close()
    except sqlite3.Error as exc:
        print(f"error: cannot load panelists (run seed.py first?): {exc}",
              file=sys.stderr)
        return 2
    if not rows:
        print("error: panelists table is empty (run seed.py first?)",
              file=sys.stderr)
        return 2
    panelists = [
        {"id": r["id"], "name": r["name"], "lens": r["lens"],
         "attributes": json.loads(r["attributes"]), "family": r["family"],
         "tags": json.loads(r["tags"])}
        for r in rows
    ]

    tensions = [t.strip() for t in args.tensions.split(",") if t.strip()]
    room = select(panelists, tensions, args.size)
    result = {
        "tensions": tensions,
        "room": [
            {"name": p["name"], "id": p["id"], "family": p["family"],
             "lens": p["lens"], "score": score(tensions, p["tags"])}
            for p in room
        ],
    }
    text = json.dumps(result, indent=2)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text + "\n")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
