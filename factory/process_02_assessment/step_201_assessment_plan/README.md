# Step 201 — Assessment plan

*(per cluster)* · Process: [02 — Assessment](../README.md)

Decide what this cluster's assessment **is**: the AT roster, what each AT evidences of the UoC, and what
the scenario must supply for each to be attemptable.

It is the hinge of the whole run-sheet. The instruments at step 205 are built from it, the scenario at
203–204 is designed to satisfy its `SR-*` register, and the mapping documents at 207 trace back through
it. An item no AT claims here is an item nobody ever builds an instrument for.

## Contents

Numbered in the order they are needed, working through the step.

| | Document | |
|---|---|---|
| `_00` | [prerequisites](_00_prerequisites.md) | **entry condition** — an accepted consolidated UoC, and the operator available to decide the frame |
| `_01` | [execution](_01_execution.md) | the step performed, item by item |
| `_02` | [assessment-plan format](_02_assessment-plan-format.md) | the deliverable's shape, including what §1 must state |
| `_03` | [planning guide](_03_planning-guide.md) | how to run the conversation — what to elicit, and what to draft only afterwards |
| `_04` | [plan-decisions format](_04_plan-decisions-format.md) | the decision log kept through phases 1 and 3 |
| `_99` | [gate](_99_gate.md) | **exit condition** — complete, no TBDs remaining, and accepted |
| | [`scripts/`](scripts/) | the validator |

## The three phases

A phase is a stretch of work inside the step, distinguished by **who acts**.

| Phase | | Who |
|---|---|---|
| 1 | elicit the frame — engagement shape, group/individual, scenario vehicle, KE position | the operator, LLM offering options |
| 2 | draft everything downstream — coverage per AT, the `SR-*` register, the rollups | the LLM |
| 3 | review to acceptance | the operator |

**The frame comes first, and that is the opposite of step 102.** There the LLM proposed and the operator
reacted, because grouping is derivable from the units. Here the first three decisions are not derivable
from anything in the repository — whether the cluster is group-assessed, whether there is an
observation, what world it runs in. Proposing an AT roster before asking is guessing, and a plausible
guess anchors the conversation on something arbitrary.

Once the frame is set, the rest is derivable and tedious: a hundred-odd items allocated across three ATs,
and what each needs from the world. That is where the LLM earns its place.

## Two documents come out

**`assessment_plan.md`** is the deliverable — and unlike the consolidated UoC, it **explains itself**:
§1 carries the settled rationale, in prose, where the next reader will look.

**`assessment-plan-decisions.md`** therefore holds what the plan does not: the alternatives weighed and
set aside, the path revisions took, and who decided what. It is deliberately **not validated** — nothing
mechanical can check whether it records what was discussed rather than a plausible reconstruction.

## Tooling

| What | Where |
|---|---|
| validator [`scripts/validate_assessment_plan.py`](scripts/validate_assessment_plan.py) | **in this folder**, on `format_contract`, `md_section`, `item_reference`, `scenario_requirement` |
| format standard [`_02_assessment-plan-format.md`](_02_assessment-plan-format.md) | **in this folder** — its `## Skeleton` drives the validator's section list |
| no-TBDs check | **not built** — probably belongs to every planning step, not this one |

## Status

The validator is covered by `VAP-01…28` in [`factory/docs/test-plan.md`](../../docs/test-plan.md). Its section
list comes from `_02`'s skeleton, so changing the standard moves the checks without a code edit. There is
no skill: the gate runs one script and reads a verdict, so the procedure is `_01_execution.md` and
`_99_gate.md`.

`_02`'s "what §1 must state" is the four-part shape that has held across the plans written so far,
recorded as that rather than as a rule.
