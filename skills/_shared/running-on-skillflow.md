# Running on skillflow

The four skills are written to be run, round by round, on
[skillflow](https://github.com/NatesVibeCode/skillflow). This is the
recommended setup because it enforces what the skills need most: breaks and
stoppage. A run cannot proceed past a gate node until a person has read the
round's record and said so.

## The pattern

Map each round to a node. Put a gate node between rounds. The gate's command
asks a person for approval and exits nonzero on anything but yes — skillflow
stops the run there, and nothing downstream executes.

```sh
skillflow init
skillflow add-node round-1 --cmd "produce round 1 record"
skillflow add-node gate-1 --cmd 'read -p "Approve round 1? [y/N] " a; [ "$a" = "y" ]'
skillflow add-node round-2 --cmd "produce round 2 record"
skillflow add-edge round-1 gate-1
skillflow add-edge gate-1 round-2
skillflow run
```

## Rules

- One round per node. Never bundle two rounds into one command.
- One gate per boundary. No round starts until the previous record is read.
- A failed gate is a verdict, not an error: read the record, fix the work,
  run again.
- Every record lands on disk before its gate, so `skillflow status` always
  shows what the person approved and what stopped.
