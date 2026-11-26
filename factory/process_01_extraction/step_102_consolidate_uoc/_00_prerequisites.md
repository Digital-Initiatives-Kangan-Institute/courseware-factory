# Step 102 — Prerequisites

**Entry condition.** What must hold before the step starts. The step's *exit* condition is a different
thing entirely — see [`_99_gate.md`](_99_gate.md).

## 1. The previous gate has passed

**Gate 101 → 102** · *script* — `validate_uoc.py` reports EXACT MATCH (or verbatim-after-cosmetic) for
every unit in the cluster.

That transitively guarantees the one input this step reads:

| Input | Produced by | Guaranteed by |
|---|---|---|
| `units_of_competency/<UNIT>_Complete_R<N>.md` — a verbatim transcription per unit | step 01 | Gate 101 → 102 |

The guarantee matters more here than it looks. This step's fidelity is **structural**: it arranges
extracted lines rather than retyping them, so an item cannot be altered by the work. That only holds if
what is being arranged was faithful to begin with — which is exactly what Gate 01 proves.

## 2. The cluster is defined

| # | Required | Notes |
|---|---|---|
| P1 | Which units belong to this cluster | Step 101 loops per unit and never asks what a cluster is. This is the first step that treats the cluster as a whole, so its membership must be settled. See `docs/clusters.md`. |
| P2 | The **assessor-AC** convention for this cluster | Whether the trailing "Assessors of this unit must satisfy…" paragraph counts as the unit's last AC item. A per-cluster call, and the extractor and the gate must both run with the same setting — see [`_02_consolidated-uoc-format.md`](_02_consolidated-uoc-format.md). S1 CL1–CL3 all tag it. |

## 3. The operator is available

Not an artefact, but a real condition: **phase 3 cannot happen without them.**

Phases 1 and 2 can run alone and produce a draft. The step does not *finish* there — the grouping is a
proposal, and it is the operator who turns it into an agreed consolidation. Starting when they are not
reachable is fine; expecting to reach the gate is not.

Ideally phase 3 follows phase 2 without a long gap, while the reasoning is fresh. Where it cannot,
`consolidation-decisions.md` is what carries that reasoning across — see
[`_04_consolidation-decisions-format.md`](_04_consolidation-decisions-format.md).

→ Next: [`_01_execution.md`](_01_execution.md)
