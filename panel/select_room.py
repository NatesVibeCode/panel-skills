"""Select a panel room by semantic tag match with enforced diversity.

Reads panel/panelists.json, ranks panelists by token-overlap between the
situation's tensions and each panelist's tags, then enforces diversity:
at most one panelist per family, three to five seats. Score proposes;
diversity disposes.

Usage:
    python3 select_room.py --tensions risk,measurement,human-cost [--size 4]
    python3 select_room.py --tensions "risk" --out room.json
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
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
    parser.add_argument("--panelists", default=os.path.join(HERE, "panelists.json"))
    parser.add_argument("--out", default=None, help="write room JSON here")
    args = parser.parse_args(argv)

    if not (MIN_SEATS <= args.size <= MAX_SEATS):
        print(f"error: --size must be {MIN_SEATS}-{MAX_SEATS}", file=sys.stderr)
        return 2
    try:
        with open(args.panelists) as fh:
            panelists = json.load(fh)["panelists"]
    except (OSError, ValueError, KeyError) as exc:
        print(f"error: cannot load panelists: {exc}", file=sys.stderr)
        return 2

    tensions = [t.strip() for t in args.tensions.split(",") if t.strip()]
    room = select(panelists, tensions, args.size)
    result = {
        "tensions": tensions,
        "room": [
            {"id": p["id"], "family": p["family"],
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
