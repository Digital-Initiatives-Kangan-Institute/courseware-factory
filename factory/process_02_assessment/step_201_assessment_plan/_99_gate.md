# Step 201 — Gate

**Exit condition.** What gives permission to leave step 201 and begin step 202. The step's *entry*
condition is a different thing — see [`_00_prerequisites.md`](_00_prerequisites.md).

## Gate 201 → 202

All conditions must hold. They answer different questions: the first two that the plan is **complete**,
the third that it is **agreed**.

| # | Kind | Condition | Status |
|---|---|---|---|
| 1 | script | [`scripts/validate_assessment_plan.py`](scripts/validate_assessment_plan.py) reports **PASS** — every section the standard names, present and in order; the header fields filled; each AT declaring its coverage and its scenario requirements; a cluster-scoped `SR-*` register that §3 references consistently; and every PC/PE/KE/FS item claimed by at least one AT, with no phantoms | **built + ported**, 28 cases (VAP-01…28) green |
| 2 | script | **no `[TBD — …]` markers remain** in the plan | **not built** — see below |
| 3 | human | the operator has **explicitly accepted** the plan, and the status banner records it | human, by design |

```bash
python3 factory/process_02_assessment/step_201_assessment_plan/scripts/validate_assessment_plan.py \
  --cluster <cluster>
```

## Reading the verdict

| Verdict | Means | Do |
|---|---|---|
| **FORMAT: FAIL** | a section, field or AT block the standard requires is absent, out of order, or empty | each failure names the thing; fix and re-run |
| **MISSING** | an item no AT claims | decide which AT evidences it — this is a design decision, not a formatting one |
| **PHANTOM** | a reference to something no unit contains | a typo, or a number left behind by a unit reissue |
| **unresolved reference** | an abbreviated tag with no unit to inherit on its line | name the unit |
| **COVERAGE: SKIPPED** | no consolidated UoC found | the prerequisite is not met; do not proceed on a skipped coverage check |

A `MISSING` item is the one worth pausing on. It is not a document defect — it is a requirement that
nothing currently assesses, and the fix is a decision about which AT should carry it.

## On condition 2 — no TBDs remaining

`[TBD — needs discussion: …]` means **nobody has decided this yet**. It is how the LLM makes its own
uncertainty visible instead of choosing quietly and presenting the choice as agreed, and it is used
freely while the plan is being drafted.

Leaving the step clears them all. Each is either resolved in conversation, or becomes a consciously
deferred item in §8 — worded as a deferral ("revisit once the scenario plan exists") rather than as a
marker, so the marker keeps meaning exactly one thing.

**Not yet built.** A scan for the marker is trivial; it is not written because it should probably be a
shared check across every planning step rather than one this step owns. See
[`factory/docs/working-notes.md`](../../docs/working-notes.md).

## On condition 3 — acceptance

A PASS on conditions 1 and 2 says the plan is **complete**: nothing unassessed, nothing invented,
nothing undecided. It says nothing about whether the assessment design is any good — whether three ATs
is right, whether the approval moment falls in a sensible place, whether the group job is genuinely
divisible.

That is assessment design, and it stays the operator's call. Everything downstream is built on this
plan: the instruments at step 205, the scenario at 203 and 204, the mapping documents at 207. Accepting
it is accepting that shape.

The banner records it, because acceptance is a fact about the plan:

```markdown
> **STATUS: ACCEPTED 2026-09-12 by <who>.** The AT structure below is agreed.
```

The decisions log holds what was said around the acceptance — reservations, anything to revisit — and is
[deliberately not gate-relevant](_04_plan-decisions-format.md).

## What the gate does not check

**Whether the plan is a good assessment design.** Condition 3 exists because nothing mechanical can.

**Whether the `SR-*` register is satisfiable.** That is checked at Gate 203 → 204, when the scenario plan
is cross-checked against this register. An `SR-*` written for something the *student* produces passes
here and becomes a false gap there — which is why `_02`'s *"what an `SR-*` is NOT"* matters at authoring
time.

`[TBD — needs discussion: §1 structure]` — the validator checks that §1 is present and non-empty, not
that it states all four of the parts `_02` requires (goal, shape, thread and approvals, KE approach). A
plan whose §1 is one paragraph of prose passes today. Whether that is worth machine-checking, and
whether the approval references should be required to resolve, is undecided.
