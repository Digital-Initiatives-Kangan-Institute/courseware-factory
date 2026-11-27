# Assessment-plan format — standard

The standard for `<cluster>/assessments/assessment_plan.md`, the deliverable of step 201. First needed
when the plan is drafted, at execution item 6.

Paths to course content are relative to the **course repo** root.

A cluster's assessment plan (`<cluster>/assessments/assessment_plan.md`) is the **authored source of
truth** for that cluster's assessments: the AT structure, what each AT covers of the UoC, and what each AT
needs from the scenario. It is **one per cluster** — the cross-scenario view (all clusters' coverage + the
full scenario-requirements register) is *derived by tooling* reading across the per-cluster plans, not
hand-maintained (step 202 derives it; see also the scenario plan).

This standard fixes the plan's structure so two checks can run against it:

- **FORMAT** — the sections named below are present and in order, the header fields are filled, and
  every AT declares both of its fields. The section list is read from this document's own
  [Skeleton](#skeleton), so changing the skeleton moves the checks.
- **COVERAGE** — every item in the cluster's `consolidated_uoc.md` is referenced by at least one AT's
  **UoC coverage**.

Both run from [`scripts/validate_assessment_plan.py`](scripts/validate_assessment_plan.py).

A third check lives with the scenario plan — the **scenario cross-check** reads every `SR-*` declared here
and confirms the scenario plan satisfies it.

## Conventions

- **UoC references** use the canonical tag `[<UNIT> <SECTION> <numbering>]` — e.g. `[ICTCLD504 PC 1.1]`,
  `[ICTCLD504 KE 4]`, `[ICTCLD504 FS Reading]`. Ranges/lists allowed (`[ICTCLD504 PC 1.1–1.6]`,
  `[ICTCLD504 PC 2.1, 2.3]`) — the same parser the AT validators use expands them. Tags must appear
  **unwrapped** (not inside backticks) to count. This is the **authoritative coverage notation** — the
  older backtick form (`` `504 PC 1.1` ``) is prose only and is **not** counted.
- **Scenario-requirement IDs** are `SR-<CLUSTER>-NN` — cluster-scoped so they stay unique when the scenario
  cross-check aggregates across clusters (e.g. `SR-CL3-01`). Each is declared once in the register (§6) and
  referenced from the AT that needs it (§3).

## Required sections (in order)

The linter requires these headings and their key fields. Prose within each is free.

1. **Header banner** — title `# <cluster> — Cluster Assessment Plan`; a `> **STATUS:** …` line; and a
   **Scenario binding** line naming the scenario this plan maps to and linking the scenario plan.
2. **`## 1. Integration approach`** — how the cluster's units form one engagement. Four parts, all
   required — see [below](#the-integration-approach--what-it-must-state).
3. **`## 2. Scenario`** — the vehicle and baseline this cluster assesses on, and the provided-vs-authored
   boundary. (Narrative; the testable scenario needs are the `SR-*` in §3/§6.)
4. **`## 3. Assessment structure`** — the AT table, then **per AT** a block containing, as labelled fields:
   - **Mode** (Individual / Group) and **Format** (the parts) and **Unit focus**;
   - **UoC coverage:** the `[UNIT SEC num]` items this AT evidences *(authoritative — the UoC-coverage
     validator reads these)*;
   - **Scenario requirements:** the `SR-*` IDs this AT depends on *(the scenario cross-check reads these)*.
5. **`## 4. Provenance`** — reuse basis (brownfield) and new authoring; `author-fresh` noted where greenfield.
6. **`## 5. Coverage verification`** — the human-readable proof that nothing is unassessed: the per-section
   distribution checks (PE/KE placed) and a one-line verification statement. *(A rollup view of §3's
   coverage; may be generated. The validator's authoritative source is §3's per-AT UoC coverage.)*
7. **`## 6. Scenario requirements register`** — one row per `SR-*`: **ID · description (the condition the
   scenario must enable) · AT(s) that need it · AC link**. The **AC link** names any UoC Assessment
   Condition item the requirement subsumes (`[<UNIT> AC n]`), so the scenario/lab providing the `SR-*` also
   discharges that AC. Requirements with no AC are narrative-only conditions (stakeholders, baseline state,
   constraints) — that is expected.
8. **`## 7. Worklist`** — modifications / additions / authoring to be done.
9. **`## 8. Open questions / TBDs`** — choices awaiting decision (mark `[TBD — …]`).
10. **`## Changelog`** — dated entries; current-state prose above, history here.

## The integration approach — what it must state

§1 is where a cluster stops being three units and becomes one engagement. Four parts, all required. The
structure is not invented here — it is what the pilot course's three delivered clusters independently arrived at, so
treat it as the shape that has held so far rather than as a rule that must hold.

**1 · Goal.** One sentence: this cluster reads as a single engagement — one scenario, one stakeholder
voice, one artefact thread. CL1 words it as *"an ambition, not a constraint"*, which is the right
register: it is what the design aims at, not a promise every unit will co-operate.

**2 · Shape.** The phase → AT sequence, and which unit each part serves. Whatever renders clearly — CL2
uses an ASCII block, CL3 a single arrow sentence, CL1 three named phases. The reader must be able to see
the whole cluster's assessment at a glance.

**3 · The thread, and the approval moments.** What makes this one engagement rather than three tasks
sharing a setting — usually that one AT's output is **signed off** and the next AT builds *that*, not a
fresh start.

Each approval moment is named, tied to the UoC item that requires it, and marked individual or group:

> AT1 Part B = design sign-off, *obtain sign off to proceed* (`[ICTCLD504 PC 2.5]`, individual)

The reference matters: it is the difference between an approval the units demand and one the designer
liked the look of. A validator can confirm it resolves to a real item; only a human can judge whether
the thread is sound.

**4 · Knowledge evidence.** How KE is evidenced, and **where it physically lives** — which section of
which workbook, plus any verbal questioning. All three clusters take the same position (contextual, on
the student's own work, never abstract recall), but the position is stated rather than assumed, because
the alternative is a legitimate choice a different course might make.

Sequencing rationale belongs here too, where it is a decision with a reason: *"Part A before Part B
because a DR plan is written **for** a designed system."* The reasoning that did **not** survive — the
alternatives weighed and set aside — belongs in the decisions log, not here.

## Scenario requirements — what to capture

For each AT, ask: *what must the scenario provide for this assessment to be meaningful and do-able?* Capture
each as an `SR-*`. Typical kinds:

- **Environmental / access** — the lab + tools + data the AT needs. These map to UoC **AC** items (the AC
  link), so the AC conditions are discharged through the `SR-*` set rather than tracked separately.
- **Narrative / situational** — a stakeholder who can role-play a sign-off; a documented procedure to
  follow; a baseline system in a specific state; a constraint that drives the work (e.g. a regulatory
  requirement). No AC link; these are what make the assessment *believable*.

**What an `SR-*` is NOT — write the requirement for what the scenario *provides*, not for what the assessment
*produces or excludes*.** An `SR-*` becomes a false "gap" at the scenario cross-check / realisation step if it
describes something the world is never meant to supply. Do **not** write an `SR-*` for:

- **Student-produced artefacts (the assessed work itself).** If the student authors it, the scenario must not
  "provide" it — provide the *inputs and the format*, not the output. E.g. the **risk register / impact
  analysis** the student writes → the SR is the *data to assess risks from* + the *DR plan template*, not "a
  risk register"; the **deployment IaC** the student authors → the SR is the *provided code/contract to build
  from* + the *deliberately-faulty template to debug*, not "a working template". (If the artefact is a
  *provided* input the student works from, that **is** a valid SR — describe it as provided, and as inline/
  appendix vs lab-pack per its assessed use.)
- **Things deliberately out of scope.** If the assessment scope excludes it, there is no SR. E.g. in the pilot course,
  one cluster's LMS **application** was the client's in-house build (out of scope) → the SR is the *deployable infrastructure with a placeholder
  endpoint*, not "a deployed application".
- **Pure delivery/practice-side needs.** Practice vehicles and teaching aids are owned by the delivery
  run-sheet; they are not assessment `SR-*` (they may appear as advisory, non-`SR` scenario elements).

When in doubt, ask: *would the scenario author build this, or does the student?* Only the former is an `SR-*`.

The register is the contract the scenario plan must satisfy. The scenario cross-check fails if any `SR-*`
declared here is not provided by the scenario plan; the **quality/coherence** of the world stays a human
call.

## Skeleton

```markdown
# <Cluster ID> <Cluster Name> — Cluster Assessment Plan
> **STATUS: DRAFT.** <one line>
> **Scenario binding:** maps to the <scenario> scenario — see <scenario plan link>.

## 1. Integration approach
<the engagement thread; approval moments; KE approach>

## 2. Scenario
<vehicle, baseline, provided-vs-authored boundary>

## 3. Assessment structure
| AT | Working title | Mode | Format | Unit focus |
|----|---|---|---|---|
| AT1 | … | Individual | … | <UNIT> el … |

### AT1 — <title>
- **Mode / Format / Unit focus:** …
- **UoC coverage:** [<UNIT> PC 1.1–1.6] · [<UNIT> PE 1] · [<UNIT> KE 1, 2, 3]
- **Scenario requirements:** SR-CLn-01 · SR-CLn-02

## 4. Provenance
<reuse / new authoring / author-fresh>

## 5. Coverage verification
PE: … (all placed). KE: … (all placed). Verification: every consolidated item is covered by ≥1 AT above.

## 6. Scenario requirements register
| SR | Condition the scenario must enable | AT(s) | AC link |
|----|---|---|---|
| SR-CLn-01 | <e.g. a single-AZ baseline system deployable as a lab-pack> | AT1, AT3 | [<UNIT> AC 1] |
| SR-CLn-02 | <e.g. a stakeholder who role-plays design sign-off> | AT1 | — |

## 7. Worklist
## 8. Open questions / TBDs
## Changelog
```

## See also

- [Process 02 — Assessment](../README.md) — the run-sheet; step 201 produces this plan, step 202
  consolidates the per-cluster plans into the contract, step 203 develops the scenario plan from that
  contract, step 204 builds the scenario materials.
- [cluster-authoring-conventions.md](../../../docs/cluster-authoring-conventions.md) — the UoC traceability rule the tag
  conventions share.
- [scenario-plan-format.md](../../../docs/scenario-plan-format.md) — the scenario-plan format: defines the in-world
  elements the `SR-*` map back to, and the cross-check that confirms every `SR-*` is satisfied.
