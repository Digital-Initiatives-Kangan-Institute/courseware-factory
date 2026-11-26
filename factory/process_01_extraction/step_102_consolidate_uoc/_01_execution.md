# Step 102 — Execution

The step performed, in order. Before starting, confirm every item in
[`_00_prerequisites.md`](_00_prerequisites.md) holds.

**Three phases, three actors.** → [A](#a--the-phases-and-who-acts)

| Phase | | Who |
|---|---|---|
| 1 | extract every item, pre-tagged and verbatim | a script |
| 2 | group them into a draft, logging the calls | the LLM |
| 3 | negotiate that draft to acceptance | the operator, with the LLM offering options |

## The sequence

1. **Confirm the frame.** The cluster's units (P1) and the assessor-AC setting (P2). The same setting is
   used again at the gate; if they disagree, the gate reports a phantom item.
2. **Extract the inventory.** Run **[`scripts/inventory_uoc.py`](scripts/inventory_uoc.py)** over every
   unit. → [B](#b--running-the-extractor)
3. **Group the extracted lines into a draft**, per
   **[`_03_grouping-guide.md`](_03_grouping-guide.md)**, written to the shape in
   **[`_02_consolidated-uoc-format.md`](_02_consolidated-uoc-format.md)**. Move each line unchanged —
   never retype one.
4. **Log each real decision as it is made**, per
   **[`_04_consolidation-decisions-format.md`](_04_consolidation-decisions-format.md)**. Written in the
   moment or not at all. → [C](#c--logging-as-you-go-not-afterwards)
5. **Check the draft before showing anyone** — both gate scripts. A malformed document or a dropped
   item is a defect in the draft, not something to negotiate over.
   → [D](#d--the-validators-are-instruments-before-they-are-gates)
6. **Present the draft as a proposal.** Phase 3 begins. Nothing in it is settled, and it should be
   handed over saying so.
7. **Negotiate.** Offer options with reasons and let the operator choose; log every change; expect
   earlier decisions to reopen. → [E](#e--offering-options-rather-than-defending-a-draft)
8. **Re-run the item check after each reorganisation.** Seconds to run, and it names the item you just
   lost while you still remember moving it.
9. **Record the acceptance** — flip the deliverable's status banner to `ACCEPTED <date> by <who>`, and
   log what the operator attached to it.

Then the step's exit condition: [`_99_gate.md`](_99_gate.md).

---

## Detail

### A — The phases and who acts

A phase is a stretch of work inside this step, distinguished by **who or what does it**. They are not
steps: they share one artefact and one exit condition, so splitting them would create gates with nothing
to check.

Phase 2 runs in the **main session, not a sub-agent**. The reason is phase 3: offering the operator "it
could go here for this reason, or here for that" needs the alternatives that were weighed and set aside
while drafting. An agent returns the document, not its deliberation, so phase 3 would open having to
reverse-engineer a classification it did not make. Delegating also saves no context — the draft comes
straight back to be negotiated either way.

### B — Running the extractor

```bash
python3 factory/process_01_extraction/step_102_consolidate_uoc/scripts/inventory_uoc.py \
  --unit <CODE>=<cluster>/units_of_competency/<CODE>_Complete_R<N>.md \
  --unit <CODE>=<cluster>/units_of_competency/<CODE>_Complete_R<N>.md \
  [--assessor-ac] > /tmp/<cluster>_inventory.md
```

Every item comes out as a house-style line — `- <verbatim text> [<UNIT> <SEC> <num>]`, FS as
`- **<Skill>** — <desc> [<tag>]`, nested children indented under their tagged parent.

**This is the raw material to arrange.** Moving these pre-tagged lines into groups is what makes the
consolidation verbatim by construction: an item cannot be altered by a process that only cuts and
pastes. Retyping one — even to fix what looks like a typo in the source — breaks that, and the gate
catches it as a mistranscription.

### C — Logging as you go, not afterwards

An entry can only be true if it is written when the decision is made. A decision made and not logged is
gone: what could be written later is a reconstruction from the outcome, and the outcome is already in
the deliverable.

Back-filling does not produce a weaker log, it produces an invalid one — nothing on the page separates
a genuine entry from an invented one, so one reconstruction costs the reader their trust in all of them.
Nothing checks this; it rests on whoever is writing. The full rule is in
[`_04`](_04_consolidation-decisions-format.md).

Not every group needs an entry. A group that was obvious was not a decision.

### D — The validators are instruments before they are gates

Two scripts, because they need different inputs — and that difference is what makes them useful at
different moments:

| | Reads | Run it |
|---|---|---|
| `validate_consolidated_format.py` | the deliverable and its format standard, nothing else | once, at the end of phase 2 — is this well-formed enough to negotiate over? |
| `validate_consolidated_items.py` | the deliverable plus every source unit | constantly, after every reorganisation |

The item check is cheap, and run often it names the item a reorganisation just dropped while the move is
still in mind. Left to the end, finding it means reconstructing which of twenty moves lost it.

Its failures are worth reading as categories rather than as errors: a `MISSING` item was dropped during
grouping; `UNEXPECTED` or `DUPLICATED` means a reference was mistyped or an item placed in two groups;
`MISTRANSCRIBED` means an item's text no longer matches its source — which should be impossible if lines
were moved rather than typed, so it is really a report that someone retyped one.

The same PASSes are the gate's first two conditions. Nothing changes at the exit except that they must
both hold at once.

### E — Offering options rather than defending a draft

Phase 3 is the operator's. The LLM's job is to make choosing easy: where an item could plausibly sit in
more than one group, say so and give the reason each way, rather than presenting one answer and waiting
to be corrected.

Expect the discussion to loop, and expect earlier decisions to be reopened — a grouping that made sense
in isolation often stops making sense once three more are on the page. When something is reopened, log
the new decision and move on. Do not defend the earlier entry, do not ask for a justification, and do
not preface the change with what was previously agreed. The log exists to make revision cheap; used to
argue against a revision, it is being read exactly backwards.
