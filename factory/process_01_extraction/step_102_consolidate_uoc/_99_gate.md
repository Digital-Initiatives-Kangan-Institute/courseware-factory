# Step 102 — Gate

**Exit condition.** What gives permission to leave step 102 and begin step 103. The step's *entry*
condition is a different thing — see [`_00_prerequisites.md`](_00_prerequisites.md).

## Gate 102 → 103

Both conditions must hold. They answer different questions: the first that the document is **faithful**,
the second that it is **agreed**.

| # | Kind | Condition | Status |
|---|---|---|---|
| 1 | script | `validate_consolidated_format.py` reports **PASS** — the deliverable conforms to [`_02`](_02_consolidated-uoc-format.md): title, status banner, source-units table, every group carrying its `Why grouped:` and `Assessment idea (TBD):`, every ungrouped item carrying a reason | **not built** |
| 2 | script | [`scripts/validate_consolidated_items.py`](scripts/validate_consolidated_items.py) reports **PASS** — every item from every source unit appears exactly once, verbatim, nothing extra | **built + ported**, 26 cases (VCI-01…26) green |
| 3 | banner | `consolidated_uoc.md`'s status banner reads `ACCEPTED <date> by <who>` | human today; machine-checkable when condition 1 is built |

Two scripts rather than one because they need **different inputs**. Condition 1 reads the deliverable and
its format standard, nothing else — so it can run at the end of phase 2, on the document alone, before
the operator sees it. Condition 2 reads the deliverable plus every source unit, and gets re-run after
every reorganisation in phase 3.

```bash
python3 factory/process_01_extraction/step_102_consolidate_uoc/scripts/validate_consolidated_items.py \
  --cluster <cluster> \
  --unit <CODE>=units_of_competency/<CODE>_Complete_R<N>.md \
  --unit <CODE>=units_of_competency/<CODE>_Complete_R<N>.md \
  [--assessor-ac]
```

The `--assessor-ac` setting **must match the one used at execution item 2**. If they disagree, the gate
reports a phantom missing or extra item and the failure is in the invocation, not the document.

## Reading the verdict

| Verdict | Means | Do |
|---|---|---|
| **PASS** | complete and verbatim | condition 1 met |
| **MISSING** | an item was dropped during grouping | find it in the inventory and place it |
| **UNEXPECTED** / **DUPLICATED** | a reference was mistyped, or an item placed in two groups | fix the reference, or remove one copy |
| **MISTRANSCRIBED** | an item's text no longer matches its source | an item was retyped rather than moved — restore it from the inventory |

**Never edit the deliverable away from the source to force a PASS.** The document's fidelity is
structural: it holds because lines were arranged rather than authored. Reworking an item's text to
satisfy the gate destroys the only property the gate is protecting.

## On condition 2

The consolidation is a **proposal until the operator accepts it**, and nothing else in the repository
records that they did. The banner is the acceptance because acceptance is a fact about that document.

A PASS on condition 1 says the grouping is complete and faithful — not that it is *good*. Whether these
items belong together is assessment design, and it stays the operator's call. That is what condition 2
is for, and it is why a green validator alone does not open the gate.

## What the gate does not check

**`consolidation-decisions.md` is deliberately not gate-relevant** — not its content, and not its
existence. No script can check whether it records what was actually discussed rather than a plausible
reconstruction, and an existence check would fire only after every decision had been made, when the
sole way to clear a failure would be to fabricate entries. The reasoning is in
[`_04_consolidation-decisions-format.md`](_04_consolidation-decisions-format.md).

Nothing yet checks the deliverable's **format** — condition 1 is decided but not built, so a group
missing its `Why grouped:`, or an absent source-units table, passes today. It is driven by
[`_02`](_02_consolidated-uoc-format.md)'s `## Skeleton` block through `common/helpers/format_contract.py`,
the way the delivery-plan validator is, so changing the skeleton moves the checks without a code edit.

Its acceptance evidence, when built: the three existing `consolidated_uoc.md` files for S1 CL1–CL3 were
authored to this convention and should PASS. One that does not is a finding either way — the document
drifted, or the standard describes something nobody actually does.
