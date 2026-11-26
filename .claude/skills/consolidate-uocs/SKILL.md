---
name: consolidate-uocs
version: 2.0.0
updated: 2026-09-09
model: claude-opus-4-8
description: >-
  This skill should be used when a cluster's units of competency need to be consolidated into a
  single consolidated_uoc.md — e.g. "consolidate the CL3 UoCs", "build the consolidated UoC for
  this cluster", "create consolidated_uoc.md", "merge these units' PCs/PEs/KEs into one grouped
  document", or after a cluster's unit .md transcriptions are validated and the next step is to
  group every assessable item. The work is extraction (a script), grouping into topic clusters
  where one assessment artefact could plausibly evidence the group (editorial judgement — a DRAFT
  proposal, never a locked decision), negotiation with the operator, and validation that every item
  appears exactly once (scripts). Use it for any UoC consolidation, even if the user does not name
  the scripts.
---

# Consolidate a cluster's units of competency

**This skill is a pointer.** The work is factory step 102, and everything it needs lives in
that step's folder:

> **`factory/process_01_extraction/step_102_consolidate_uoc/`**

Read the documents there, in order:

| | |
|---|---|
| [`_00_prerequisites.md`](../../../factory/process_01_extraction/step_102_consolidate_uoc/_00_prerequisites.md) | what must hold before starting |
| [`_01_execution.md`](../../../factory/process_01_extraction/step_102_consolidate_uoc/_01_execution.md) | **start here** — the step performed, item by item |
| [`_02_consolidated-uoc-format.md`](../../../factory/process_01_extraction/step_102_consolidate_uoc/_02_consolidated-uoc-format.md) | the deliverable's shape |
| [`_03_grouping-guide.md`](../../../factory/process_01_extraction/step_102_consolidate_uoc/_03_grouping-guide.md) | the judgement — how to decide what groups with what |
| [`_04_consolidation-decisions-format.md`](../../../factory/process_01_extraction/step_102_consolidate_uoc/_04_consolidation-decisions-format.md) | the decision log kept as the calls are made |
| [`_99_gate.md`](../../../factory/process_01_extraction/step_102_consolidate_uoc/_99_gate.md) | what gives permission to leave the step |

## Why a skill at all

The step has three phases, and the middle one is **judgement** — grouping items where one assessment
artefact could plausibly evidence the whole group is assessment design, not something a script can do.
That is why this skill survives where the transcription skills dissolved into their step: those held
nothing but two commands and a verdict.

It holds no content of its own, so there is no second source of truth. Its job is to be findable by
name and to send you to the step.

## Run it in the main session

**Not a sub-agent.** Phase 3 negotiates the draft with the operator, and doing that well needs the
alternatives phase 2 weighed and set aside. An agent returns the document, not its deliberation, so
phase 3 would open having to reverse-engineer a classification it did not make.
