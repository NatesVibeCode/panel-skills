# Running on skillflow

The four skills run on [skillflow](https://github.com/NatesVibeCode/skillflow),
and the graph does the enforcing — not prose. Room selection, diversity, and
stoppage are all nodes and gates: the selector picks the room mechanically,
and a gate between rounds stops the run until a person has read the record
and approved the next round.

## The room-forming graph

One command builds and runs the whole session:

```sh
panel/room.sh "risk,measurement,human-cost" 2 ./session1
```

That builds the graph — tensions → select → gate → round, per round — and
runs it. `panel/select_room.py` seats each room mechanically (semantic match,
diversity enforced: at most one per family, three to five seats). Each gate
stops until a person has collided, written the round record, and updated the
tensions for the next round's selection. New tensions re-form the room every
round.

## Rules

- The selector seats the room. Nobody hand-picks panelists in prose.
- One gate per boundary. No round starts until the previous record is read.
- A failed gate is a verdict, not an error: read the record, fix the work,
  run again.
- Every record and every `room.json` lands on disk before its gate, so
  `skillflow status` always shows what the person approved and what stopped.
