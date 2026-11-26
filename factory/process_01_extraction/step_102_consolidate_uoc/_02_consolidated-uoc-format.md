# Consolidated UoC — format standard

The standard for `<cluster>/consolidated_uoc.md`, the step's deliverable. First needed at execution
item 3, when the draft is written.

## What it is for

The single source of truth for **what the cluster must assess**. Every downstream artefact — the
assessment plan, the AT marking benchmarks, the per-unit mapping documents — traces back to its items
by their `[UNIT SECTION numbering]` reference.

Two properties carry that weight:

- **Completeness** — every item from every source unit present exactly once. The gate enforces it.
- **Verbatim fidelity** — no item re-worded. Guaranteed structurally, by *arranging* the extracted
  lines rather than retyping them. Nothing in this document should ever be typed by hand.

Everything else in the document — which items are grouped together, what a group is called, what
assessment might evidence it — is a **proposal**, and the document says so on its face until the
operator accepts it (see [`_04_consolidation-decisions-format.md`](_04_consolidation-decisions-format.md)).

## Skeleton

```markdown
# <CLUSTER> — Consolidated UoC

> **Status: DRAFT.** The groupings, comments and assessment ideas below are a first-pass analysis.
> Nothing here is approved.

Reference tags take the form `[UNIT SECTION numbering]` — e.g. `[ICTCLD501 PC 1.2]`,
`[ICTCLD501 FS Numeracy]`, `[ICTCLD501 PE 3]`.

## Source units

| Code | Title | Source file |
| --- | --- | --- |

## Group N — <short descriptive name>

**Why grouped:** <one or two sentences naming the shared competency that binds them>

**Assessment idea (TBD):** <one or two sentences on how a single artefact could evidence the group>

## Ungrouped items
```

## The parts

**Title** — `# <Cluster> — Consolidated UoC`.

**Status banner** — a blockquote marking the document DRAFT and saying plainly that nothing is
approved. Not decoration: the consolidation proposes, the course owner disposes.

It changes only when the operator accepts, and it is **what the gate reads to know the step is done**:

```markdown
> **Status: ACCEPTED 2026-09-12 by Tim Baird.** The groupings below are agreed.
```

The banner is the acceptance record because acceptance is a fact about *this* document. The decisions
log holds the discussion around it, and is deliberately not gate-relevant — see
[`_04`](_04_consolidation-decisions-format.md).

**Reference-tag note** — one line showing the `[UNIT SECTION numbering]` form, with the example tags
**wrapped in backticks**. The backticks matter mechanically: the gate strips code spans before counting
references, so a wrapped example is not miscounted as an item.

**Source units table** — Code, Title, Source file. One row per unit.

**The groups** — `## Group N — <name>`, each carrying a `Why grouped:` and an `Assessment idea (TBD):`
before its item lines. Numbered in a sensible delivery-ish order, though the order is itself part of
the proposal.

**Ungrouped items** — `## Ungrouped items`, each with a one-line reason it stands alone. An item that
fits no group belongs here, not forced into the nearest one.

## Item lines

Produced by `scripts/inventory_uoc.py` and moved **unchanged** into groups. Never re-word, re-tag or
tidy them.

| Section | Line |
|---|---|
| PC | `- N.N <verbatim text> [<UNIT> PC N.N]` — the source number stays in the text as well as the tag |
| FS | `- **<Skill name>** — <verbatim description> [<UNIT> FS <Skill name>]` |
| PE / KE / AC | `- <verbatim text> [<UNIT> SEC n]` |

An item with sub-points keeps them as **indented children beneath the one tagged parent line**. The
children are part of that single item, not items of their own — the gate counts tagged lines, and
promoting a child to its own bullet invents an assessable item that the unit does not contain.

## Two conventions the gate depends on

**Assessor-AC alignment.** The trailing "Assessors of this unit must satisfy…" paragraph is an AC item
only when the cluster tags it. `inventory_uoc.py` and the gate must run with the same `--assessor-ac`
setting; if they disagree, the gate reports a phantom missing or extra item. CL1, CL2 and CL3 all tag
it, so both run with the flag on.

**Range references are prose only.** A convenience like `[ICTCLD501 PC 5.1–5.4]` may appear in a
group's *Why grouped* or *Assessment idea*, but every individual item must still appear once as its own
tagged line. The gate counts item lines, not prose ranges.
