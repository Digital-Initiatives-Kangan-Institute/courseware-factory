# Step 102 — Consolidate the cluster's units of competency

*(once per cluster)* · Process: [01 — Extraction](../README.md)

Bring every assessable item from every unit in the cluster into one document, quoted verbatim,
source-referenced, and **grouped where one assessment artefact could plausibly evidence the group**.
The bridge from raw units to the assessment plan.

This is the first step where judgement enters the factory. Step 101 lifts; this one decides.

## Contents

Numbered in the order they are needed, working through the step.

| | Document | |
|---|---|---|
| `_00` | [prerequisites](_00_prerequisites.md) | **entry condition** — Gate 01 passed, the cluster defined, the operator available |
| `_01` | [execution](_01_execution.md) | the step performed, item by item |
| `_02` | [consolidated-uoc format](_02_consolidated-uoc-format.md) | the deliverable's shape — what phase 2 produces |
| `_03` | [grouping guide](_03_grouping-guide.md) | the judgement — how phase 2 decides |
| `_04` | [consolidation-decisions format](_04_consolidation-decisions-format.md) | the decision log kept through phases 2 and 3 |
| `_99` | [gate](_99_gate.md) | **exit condition** — complete and verbatim, and accepted |
| | [`scripts/`](scripts/) | the extractor |

## The three phases

A phase is a stretch of work inside the step, distinguished by **who acts**. They are not steps: one
artefact, one exit condition.

| Phase | | Who | Produces |
|---|---|---|---|
| 1 | extract every item, pre-tagged and verbatim | `scripts/inventory_uoc.py` | the inventory |
| 2 | group them into a draft, logging the calls | the LLM, main session | `consolidated_uoc.md` (DRAFT) + `consolidation-decisions.md` |
| 3 | negotiate to acceptance | the operator, LLM offering options | the accepted deliverable |

Phase 2 runs in the main session rather than a sub-agent, because phase 3 needs the alternatives phase 2
weighed and discarded — and an agent returns the document, not its deliberation.

## Two documents come out

**`consolidated_uoc.md`** is the deliverable: the single source of truth for what the cluster must
assess. Every downstream artefact traces to its items by reference.

**`consolidation-decisions.md`** is a decision log, written as the calls are made. It carries phase 2's
reasoning into phase 3, and answers "what were they thinking" long afterwards. It is deliberately **not
validated** — not its content, not its existence — because nothing mechanical can check the property
that makes it valuable, and an existence check would arrive too late to be met by anything but
fabrication.

## Tooling

| What | Where |
|---|---|
| extractor [`scripts/inventory_uoc.py`](scripts/inventory_uoc.py) | **in this folder**, on `md_table` |
| gate 1 — `validate_consolidated_format.py` | **not built** — driven by `_02`'s `## Skeleton` via `format_contract` |
| gate 2 — [`scripts/validate_consolidated_items.py`](scripts/validate_consolidated_items.py) | **in this folder**, on `item_reference` + `cosmetic` |
| skill `consolidate-uocs` | `.claude/skills/` — **a pointer at this folder**, holding no content of its own |

Two validators because they read different things: the format one needs only the deliverable, so it can
run on the draft alone at the end of phase 2; the item one needs every source unit, and gets re-run
through phase 3.

## Status

Both scripts are covered by `IU-01…30` and `VCI-01…26` in [`factory/docs/test-plan.md`](../../docs/test-plan.md).
Gate 1, the format validator, is not built yet. A unit code is matched by **shape**
(`common/helpers/item_reference.py`), so the gate serves any training package.
