# Running on skillflow

The four skills run on [skillflow](https://github.com/NatesVibeCode/skillflow),
and the graph does the enforcing — not prose. Room selection, diversity, and
stoppage are all nodes and gates: the selector picks the room mechanically,
and a gate between rounds stops the run until a person has read the record
and approved the next round.

## The room-forming graph

```sh
skillflow init
skillflow add-node tensions --cmd "echo 'risk,measurement,human-cost' > tensions.txt"
skillflow add-node select-room --cmd "python3 panel/select_room.py --tensions $(cat tensions.txt) --out room.json"
skillflow add-node gate-1 --cmd 'read -p "Approve room? [y/N] " a; [ "$a" = "y" ]'
skillflow add-node round-1 --cmd "collide over the question with room.json"
skillflow add-edge tensions select-room
skillflow add-edge select-room gate-1
skillflow add-edge gate-1 round-1
skillflow run
```

`panel/select_room.py` matches panelists to the tensions semantically and enforces
diversity (at most one per family, three to five seats). New tensions from a
round re-run the selector and re-form the room — add another
select → gate → round chain per round.

## Rules

- The selector seats the room. Nobody hand-picks panelists in prose.
- One gate per boundary. No round starts until the previous record is read.
- A failed gate is a verdict, not an error: read the record, fix the work,
  run again.
- Every record and every `room.json` lands on disk before its gate, so
  `skillflow status` always shows what the person approved and what stopped.
