---
name: debate
description: Attack a claim from five sides in rounds until only what survives stands. Use when a decision matters and someone should try to break it first.
---

# Debate

**Requires:** [skillflow](https://github.com/NatesVibeCode/skillflow) — run via `panel/room.sh`.

Put one claim in the room and let the panel try to break it. What survives,
in smaller and harder form, is the outcome.

## When to use

- A decision matters and nobody has attacked it yet.
- Two approaches collide and the collision needs a referee.
- Someone says "this is obviously right" — that sentence is the trigger.

## Procedure

1. State the claim in one paragraph, plain words. It must be restatable by
   a stranger in six seconds before the first round seats.
2. Run rounds. Each round, the DAG forms the room: name the live tensions,
   run the selector, and let the selected room collide over the claim (see
   `../_shared/panel.md`) — no turn order, no checklist of voices.
3. End each round with collisions: where the claim moved, what died, what is
   still standing — plus the new tags the round raised. Write it down before
   the next round.
4. Stop when a round changes nothing, or after three rounds — whichever comes
   first. More rounds polish; they rarely cut.

## Record

Write a short record: the claim, the panel, one section per round with
collisions, and the outcome — what survived, what died, and what the room
would still attack. A stranger reads it in under a minute.

## Runner

Run on skillflow (see `../_shared/running-on-skillflow.md`): one node per
round, one gate node between rounds. No next round until a person approves
the record — the gates enforce the stoppage, the Human just asks for it.
