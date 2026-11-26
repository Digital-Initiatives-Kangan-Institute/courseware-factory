# Process 01 — Extraction

Getting source material into validated, machine-readable form. Everything here is **faithful lifting**,
not editorial judgement: the unit-of-competency documents are transcribed verbatim, every assessable item
is extracted pre-tagged, and — where any exists — pre-existing assessment material is surveyed. Nothing
in this process *decides* anything; that starts at `process_02_assessment`.

Steps 101 and 102 run on every build. Step 103 runs only on a brownfield build (see below).

Run-sheet: [docs/process-assessment.md](../../docs/process-assessment.md) (its first three steps).

## Steps

| Step | Name | Tooling |
|---|---|---|
| 101 | Transcribe the units of competency | `step_101_transcribe_uoc/scripts/`: `transcribe_uoc.py` + `validate_uoc.py` |
| 102 | Consolidate the cluster's UoCs | `step_102_consolidate_uoc/scripts/`: `inventory_uoc.py` + `validate_consolidated_items.py`; skill `consolidate-uocs` points at the step (phase 2 is judgement) |
| 103 | Audit source assessments — **OPTIONAL, brownfield only** | agent `.claude/agents/evaluate-legacy-materials.md` (no script) |

**Step 103 is the factory's one optional step.** It runs only when pre-existing assessment materials
exist and might be reused. Greenfield — the common case for new courseware — skips it entirely and goes
straight to step 201. Which it is cannot be inferred, so **ask the operator** rather than guessing from
whether a folder happens to be present.

## Status

A step gets a skill only when it holds judgement a script cannot make — which is why 102 has one and 101
does not. Step 102's format gate, `validate_consolidated_format.py`, is not built yet.
