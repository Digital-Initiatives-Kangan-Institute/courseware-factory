# Step 201 — Prerequisites

**Entry condition.** What must hold before the step starts. The step's *exit* condition is a different
thing entirely — see [`_99_gate.md`](_99_gate.md).

## 1. The previous gate has passed

**Gate 103 → 201.** On a greenfield build step 103 is skipped, so the gate that actually guarantees the
input is **102 → 103**: the consolidated UoC is complete, verbatim, and **accepted by the operator**.

| Input | Produced by | Guaranteed by |
|---|---|---|
| `consolidated_uoc.md` — every assessable item, grouped, accepted | step 102 | Gate 102 → 103 |
| reusable-material candidates *(brownfield only)* | step 103 | Gate 103 → 201 |

The acceptance matters more here than the completeness. This step allocates the consolidated items
across ATs, and its groups are the starting point for that allocation — so a consolidation the operator
has not agreed to is a set of groupings this step would build on and then have to unpick.

## 2. The operator is available to decide the frame

**Not an artefact, and not optional.** The first three decisions are theirs, and nothing downstream can
be drafted without them:

| # | Decision | Why it cannot be derived |
|---|---|---|
| P1 | The shape of the engagement — the thread and its approval moments | The units say what must be evidenced, never in what order or as one engagement |
| P2 | Individual or group, and which job is divisible | A property of the cohort and the teaching, not of the units |
| P3 | The scenario vehicle, and the provided-versus-authored boundary | Often inherited from a scenario shared with other clusters |

An LLM can bring candidates to each — approval criteria found in the consolidated UoC, a teamwork unit
that suggests where group work belongs — but bringing candidates is not deciding.

Starting without the operator is fine: the consolidated UoC can be read and the candidates assembled.
Reaching the gate is not.

## 3. What is NOT a prerequisite

**The scenario plan.** It is step 203, and it is developed **from** this plan's `SR-*` register — not
the other way round. This step declares what the scenario must supply; the scenario is designed to
supply it. Waiting for a scenario plan here would invert the run-sheet.

**A delivery frame.** Session counts and the online/classroom split belong to process 03. They shape how
an assessment is *run*, not what it assesses. Where cohort size genuinely constrains a design — an
observation or a presentation scales with headcount — that surfaces as a consideration in P2, not as a
dependency on a document that does not exist yet.

→ Next: [`_01_execution.md`](_01_execution.md)
