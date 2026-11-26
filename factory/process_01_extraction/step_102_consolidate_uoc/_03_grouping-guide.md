# Grouping — the judgement

How to make the classification in phase 2. The mechanical layers either side of it — extracting the
items, proving the result is complete — are scripts; this is the part no script can do.

Read with [`_02_consolidated-uoc-format.md`](_02_consolidated-uoc-format.md), which says what the
document you are filling looks like.

## The test

Group items where the underlying competency or topic is similar enough that **one assessment artefact
could plausibly evidence every member**.

The test is assessment-design plausibility, not keyword overlap. Ask: *could a single task,
observation or question set produce evidence for all of these at once?* Two items can share vocabulary
and need entirely different evidence; two items can be worded quite differently and fall out of the
same piece of work.

## Guidance that has held up across clusters

- **Cross-unit groups are good.** Where two units carry the same competency — both naming the shared
  security responsibility model, say — grouping their items shows the overlap and avoids
  double-assessing the student for one piece of work.
- **A Foundation Skill often rides along** with a deliverable rather than meriting its own task. It is
  perfectly good for a group's assessment idea to say "evidenced through the documentation in Group 4
  — no dedicated item."
- **If the *why* needs more than two sentences, it is probably two groups.** A group whose binding
  competency cannot be named briefly usually is not one competency.
- **An item that fits nowhere goes to `## Ungrouped items`** with a one-line reason. Forcing it into
  the nearest group is worse than leaving it out — the group's *why* stops being true, and the
  assessment idea quietly stops covering it.
- **Group order is part of the proposal.** Number them in a sensible delivery-ish order, and expect
  the operator to move them.

## Moving, never typing

The items come from `scripts/inventory_uoc.py` already verbatim and already tagged. Move each line
**unchanged** into exactly one group. Do not re-word, re-tag or tidy it.

This is what makes the fidelity structural rather than careful: an item cannot be altered by a process
that only cuts and pastes. Retyping one — even to fix what looks like a typo in the source — breaks
that guarantee and the gate will catch it as a mistranscription.

## Recording the calls as you make them

Grouping is where the reasoning is generated, and phase 3 is where it is needed. Log each real
decision in `consolidation-decisions.md` **as it is made**, per
[`_04_consolidation-decisions-format.md`](_04_consolidation-decisions-format.md).

Two things worth logging, and nothing else:

- a grouping that was a genuine judgement call, with the reason for it;
- an alternative that was actually weighed and set aside, with why it lost.

Not every group needs an entry. A group that was obvious was not a decision — writing it up anyway
manufactures deliberation that did not happen, and buries the entries that matter.

Log them as decisions, not as commitments. Phase 3 will reopen some of them, and several will look
different once the whole picture is on the page — that is what phase 3 is for.

## The output is a proposal

Nothing here is settled by producing it. Every group, name, order and assessment idea is a first-pass
analysis for the operator to react to in phase 3, and the document says so on its face until they
accept it.

Present it that way. Do not describe a group or an assessment idea as settled, and where something is
genuinely open, mark it `[TBD — needs discussion: <what is open>]` rather than choosing quietly.
