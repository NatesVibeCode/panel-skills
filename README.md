# Panel skills

Four small skills for thinking with a room instead of alone: **debate**,
**brainstorm**, **reframe**, **review**. Each one seats its room from the
panelist list by semantic match with enforced diversity, runs in rounds, and
writes a short plain-language record.

They are written for people first. Every record must be readable by a smart
stranger in under a minute. No servers, no services, no accounts — the skills
are Markdown files an agent reads and follows.

## The skills

- [debate](skills/debate/SKILL.md) — attack a claim from five sides until only the facing wall stands.
- [brainstorm](skills/brainstorm/SKILL.md) — open the field of approaches before committing.
- [reframe](skills/reframe/SKILL.md) — restate the problem until the shape of the work changes.
- [review](skills/review/SKILL.md) — read back intent, check what was built, give a verdict.

Shared material lives in [skills/_shared](skills/_shared): the
[panel](skills/_shared/panel.md) and the
[recommended runner setup](skills/_shared/running-on-skillflow.md).

Room selection is mechanical, not prose: [panel/panelists.json](panel/panelists.json)
lists the panelists and [panel/select_room.py](panel/select_room.py) matches
them to the situation's tensions with enforced diversity (one per family).
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
