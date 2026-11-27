# Step 201 — Execution

The step performed, in order. Before starting, confirm every item in
[`_00_prerequisites.md`](_00_prerequisites.md) holds.

**Three phases, and the frame comes first.** → [A](#a--the-phases-and-who-acts)

| Phase | | Who |
|---|---|---|
| 1 | elicit the frame — the engagement shape, group/individual, the scenario vehicle, the KE position | the operator, with the LLM offering options |
| 2 | draft everything downstream of it — coverage per AT, the `SR-*` register, the rollups | the LLM |
| 3 | review to acceptance | the operator |

## The sequence

1. **Read the consolidated UoC.** Its groups are already "one artefact could evidence these", so they
   are the starting point for the AT roster rather than a document to re-derive.
2. **Assemble the candidates** the operator will choose between — approval criteria found in the units,
   a teamwork unit suggesting where group work belongs, the scenario constraints already fixed by
   sibling clusters. → [B](#b--bringing-candidates-rather-than-proposals)
3. **Elicit the frame**, per **[`_03_planning-guide.md`](_03_planning-guide.md)** — four conversations,
   one at a time, logging each call as it is made.
4. **Log the framing decisions** as they happen, per
   **[`_04_plan-decisions-format.md`](_04_plan-decisions-format.md)**. Written in the moment or not at
   all. → [C](#c--logging-as-you-go-not-afterwards)
5. **Allocate UoC coverage per AT**, working the consolidated document item by item so nothing is
   dropped.
6. **Write the plan** to `<cluster>/assessments/assessment_plan.md`, conforming to
   **[`_02_assessment-plan-format.md`](_02_assessment-plan-format.md)**.
7. **Derive the `SR-*` register** — for each AT, what the world must supply for it to be attemptable.
   → [D](#d--the-sr-register-is-a-contract-with-a-step-you-have-not-reached)
8. **Run the validator** before showing anyone. A missing item or an unresolved reference is a defect in
   the draft, not something to negotiate over.
   → [E](#e--the-validator-is-an-instrument-before-it-is-a-gate)
9. **Present the draft as a proposal.** Phase 3 begins. The frame is already theirs; what is new is
   everything derived from it.
10. **Negotiate**, re-running the validator after each change, logging every decision that moves.
11. **Resolve every `[TBD]`** — each is either decided in conversation or becomes a consciously deferred
    item in §8, worded as a deferral rather than a marker.
12. **Record the acceptance** — flip the status banner, and log what the operator attached to it.

Then the step's exit condition: [`_99_gate.md`](_99_gate.md).

---

## Detail

### A — The phases and who acts

The frame-first ordering is the thing to get right, and it is the opposite of step 102.

There, the LLM proposed groupings and the operator reacted, because grouping is derivable from the units
in front of you. Here the first three decisions are **not derivable from anything in the repository**:
whether this cluster has a group assessment, whether there is an observation, what world it runs in.
Proposing an AT roster before asking is guessing — and a plausible guess is worse than a question,
because it anchors the conversation on something arbitrary that then has to be argued out of.

Once the frame is set, phase 2 is genuinely derivable and genuinely tedious: allocating a hundred-odd
items across three ATs, and working out what each needs from the world. That is the LLM's half, and it
is where the leverage is.

Phase 2 runs in the **main session**, for the same reason as step 102: phase 3 needs the alternatives
phase 2 weighed, and an agent returns the document rather than its deliberation.

### B — Bringing candidates rather than proposals

There is a difference between *"here are the three criteria in these units that require sign-off before
proceeding, with their references"* and *"I suggest AT1 ends with a design approval"*.

The first is research the operator would otherwise do by hand, and it leaves the decision open. The
second has decided, and now the conversation is about the LLM's proposal rather than about the cluster.

Bring candidates. Name what each would imply. Stop there.

### C — Logging as you go, not afterwards

An entry can only be true if it is written when the decision is made. A decision made and not logged is
gone: what could be written later is a reconstruction from the outcome, and the plan already holds the
outcome.

That matters more in this step than in most, because the frame decisions are made in conversation and
leave no other trace. §1 will record what was chosen; nothing except the log records what else was on
the table.

### D — The `SR-*` register is a contract with a step you have not reached

Each `SR-*` is a promise that the scenario will supply something, checked two steps later at Gate 203 →
204 and again when the scenario is built at 204.

The common error is writing an `SR-*` for something the **student** produces. It reads fine here and
becomes a false gap later — the scenario author looks for a risk register nobody was ever meant to
build. `_02`'s *"what an `SR-*` is NOT"* section is the one to re-read before writing them.

The test: *would the scenario author build this, or does the student?* Only the former is an `SR-*`.

### E — The validator is an instrument before it is a gate

```bash
python3 factory/process_02_assessment/step_201_assessment_plan/scripts/validate_assessment_plan.py \
  --cluster <cluster>
```

Cheap, so run it constantly — after each allocation change it names the item that just lost its
coverage, while the change is still in mind. Left to the end, finding it means re-reading every AT.

Read its failures as categories: `MISSING` is an item no AT claims — a requirement nobody will build an
instrument for. `PHANTOM` is a reference to something no unit contains, so a typo or a number left
behind by a unit reissue. An unresolved reference is an abbreviated tag with no unit to inherit.

The same PASS is the gate's first condition.
