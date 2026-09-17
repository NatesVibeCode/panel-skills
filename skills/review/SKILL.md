---
name: review
description: Read back intent, check what was built against it, and give a verdict with the panel. Use when work claims to be done and someone should verify that.
---

# Review

Work says it is done. The panel reads back what was asked, looks at what was
built, and gives a verdict: holds, holds with gaps named, or fails. Soft
passes are lies about ownership — a gap named is a gap ownable; a gap
smoothed over is a debt with no owner.

## When to use

- Something claims to be done and the claim matters.
- A handoff is coming and the receiver should not inherit surprises.
- "Green" appeared fast and nobody can say exactly what was checked.

## Procedure

1. Read back intent in three layers: what was explicitly asked, what bar was
   implied, what constraints were hard. Write them where the builder can see
   them before evidence is discussed.
2. Lay out the evidence: what was built or changed, what was checked, what
   the checks showed. No adjectives — artifacts and observations only.
3. The room collides intent with evidence, voice by voice: the Reader checks
   the record reads plain, the Breaker hunts the untested claim, the
   Meter-Checker asks whether the checks measured the right meter, the
   Incentivist asks what the lazy path through the checks allows, the Human
   asks what the remaining gaps cost a person.
4. Give the verdict in one line — holds, holds with named gaps, or fails —
   followed by the gaps with owners, or the reason for failure. No verdict
   without evidence; no evidence without the intent readback first.

## Record

Write a short record: intent in three layers, evidence, the collision, the
one-line verdict with named gaps and owners. A stranger reads it in under a
minute and knows exactly what is done and what is not.

## Runner

Run on skillflow (see `../_shared/running-on-skillflow.md`): one node for the
intent readback, one gate, one node for evidence and verdict. The builder does
not speak during the readback round — that separation is the whole method.
