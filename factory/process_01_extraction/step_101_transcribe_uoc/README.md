# Step 101 — Transcribe the units of competency

*(loop per unit)* · Run-sheet: [process-assessment.md](../../../docs/process-assessment.md)

Lift each official UoC Word document into Markdown **verbatim** — reconstructed from the document XML,
never retyped. The first step of the first process: nothing upstream, everything downstream.

## Contents

Numbered in the order they are needed, working through the step.

| | Document | |
|---|---|---|
| `_00` | [prerequisites](_00_prerequisites.md) | **entry condition** — no previous gate; the source `.docx` are in place |
| `_01` | [execution](_01_execution.md) | the step performed, item by item |
| `_99` | [gate](_99_gate.md) | **exit condition** — every unit validates verbatim, and what to do when one doesn't |
| | [`scripts/`](scripts/) | the transcriber, and its companion `.md` on the style mapping |

## Tooling

| What | Where |
|---|---|
| transcriber [`scripts/transcribe_uoc.py`](scripts/transcribe_uoc.py) + [`.md`](scripts/transcribe_uoc.md) | **in this folder** |
| gate validator [`scripts/validate_uoc.py`](scripts/validate_uoc.py) + [`.md`](scripts/validate_uoc.md) | **in this folder** |
| docx reader `docx_text.py` | [`common/helpers/`](../../common/helpers/docx_text.py) — the one reader both scripts go through |
| cosmetic folding `cosmetic.py` | [`common/helpers/`](../../common/helpers/cosmetic.py) |

## Status

Both scripts are covered by `TU-01…30` and `VU-01…46` in [`factory/docs/test-plan.md`](../../docs/test-plan.md).
Neither step holds judgement — the scripts run and the gate reads a verdict — so there is no skill: the
procedure is `_01_execution.md` and `_99_gate.md`, and each script's detail is in its companion `.md`.
