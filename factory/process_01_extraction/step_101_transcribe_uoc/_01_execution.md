# Step 101 — Execution

The step performed, in order. Before starting, confirm every item in
[`_00_prerequisites.md`](_00_prerequisites.md) holds.

**Loop per unit.** A cluster has several; each is transcribed and validated on its own, and one unit
failing does not block the others.

## The sequence

1. **List the units.** Every `.docx` under `<cluster>/units_of_competency/original/` needs a matching
   `.md` in `units_of_competency/`. A `.docx` with no `.md` is the work.
2. **Transcribe.** Run
   **[`scripts/transcribe_uoc.py`](scripts/transcribe_uoc.py)** over the source, writing the `.md`
   beside the `original/` folder with the same basename. → [A](#a--running-the-transcriber)
3. **Validate — mandatory.** Run the gate over the pair immediately. A transcription is not done until
   it validates; an unvalidated `.md` is an assertion, not a transcription.
   → [`_99_gate.md`](_99_gate.md)
4. **Repeat** for each remaining unit.

Then the step's exit condition: [`_99_gate.md`](_99_gate.md).

---

## Detail

### A — Running the transcriber

```bash
python3 factory/process_01_extraction/step_101_transcribe_uoc/scripts/transcribe_uoc.py \
  <cluster>/units_of_competency/original/<UNIT>_Complete_R<N>.docx \
  <cluster>/units_of_competency/<UNIT>_Complete_R<N>.md
```

Omit the second argument to preview on stdout instead of writing.

The output path is the house convention: the `.md` sits in `units_of_competency/`, beside the
`original/` folder holding the `.docx`, with the same basename. Keeping the release suffix means a
reissued unit lands as a new file rather than silently overwriting the one the assessments were
written against.

**What the script does, in brief.** Text comes straight from the Word runs — never retyped — so the
content is faithful by construction. The only thing it reasons about is structure, from the source
paragraph styles: `Title`/`Heading1..6` become headings, `ListBullet`(`2`,`3`,…) become bullets
indented by nesting depth, tables become Markdown tables with multi-paragraph cells joined by `<br>`,
and empty spacer paragraphs are dropped. Headers, footers and page numbers are excluded automatically,
because only the document body is ever opened.

The full style mapping and the deliberate behaviours are in
[`scripts/transcribe_uoc.md`](scripts/transcribe_uoc.md).

### B — Why this is a script and not freehand work

The guarantee comes from **not retyping**. Copying `w:t` runs in document order means the failure mode
is never "a word changed" — at most "a heading or bullet was mis-shaped", which the gate catches and
which is fixed once, in the script, for every future unit. Hand or LLM transcription has the opposite
failure mode: silent drift, a dropped clause, a "corrected" word, a normalised heading. VET compliance
depends on the unit content being reproduced exactly, so the risk is not acceptable and the script
removes it rather than managing it.
