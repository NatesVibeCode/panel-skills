# Panel skills

Four small skills for thinking with a room instead of alone: **debate**,
**brainstorm**, **reframe**, **review**. Each one seats its room from the
panelist list by semantic match with enforced diversity, runs in rounds, and
writes a short plain-language record.

They are written for people first. Every record must be readable by a smart
stranger in under a minute. No servers, no services, no accounts — the skills
are Markdown files an agent reads and follows.

## Requirements

[skillflow](https://github.com/NatesVibeCode/skillflow) is required. Every
skill runs on it: room selection, rounds, gates, and stoppage are all DAG
nodes, not prose. Install it first, then run sessions with
`panel/room.sh "tension1,tension2" <rounds> <session-dir>`.

## Install

```sh
git clone https://github.com/NatesVibeCode/panel-skills.git
cd panel-skills
pip install git+https://github.com/NatesVibeCode/skillflow.git
```

Then either copy a skill directory (e.g. `skills/debate`) into your agent's
skills folder, or install directly if your harness supports it:

```sh
muse skills install skills/debate
```

`panel/` stays with the repo checkout — `room.sh` resolves its own location,
so run it from anywhere.

## The skills

- [debate](skills/debate/SKILL.md) — attack a claim from five sides until only the facing wall stands.
- [brainstorm](skills/brainstorm/SKILL.md) — open the field of approaches before committing.
- [reframe](skills/reframe/SKILL.md) — restate the problem until the shape of the work changes.
- [review](skills/review/SKILL.md) — read back intent, check what was built, give a verdict.

Shared material lives in [skills/_shared](skills/_shared): the
[panel](skills/_shared/panel.md) and the
[recommended runner setup](skills/_shared/running-on-skillflow.md).

Room selection is mechanical, not prose: the 128 panelists live in a
`panelists` table in the session DB (seeded from
[panel/panelists.json](panel/panelists.json) by
[panel/seed.py](panel/seed.py)),
[panel/select_room.py](panel/select_room.py) matches
them to the situation's tensions with enforced diversity (one per family),
and [panel/room.sh](panel/room.sh) runs the whole session as a skillflow DAG:

```sh
panel/room.sh "risk,measurement" 2 ./session1
```

Tests: `cd panel && python -m unittest test_select`.

## Recommended runner: skillflow

These skills work best on [skillflow](https://github.com/NatesVibeCode/skillflow):
run each round as a node in a graph, with a human gate node between rounds.
The gate stops the run until a person has read the round's record and approved
the next one. That is what enforces breaks and stoppage — the work cannot run
away from its reader. See
[running on skillflow](skills/_shared/running-on-skillflow.md) for the pattern.

## License

MIT. See [LICENSE](LICENSE).
