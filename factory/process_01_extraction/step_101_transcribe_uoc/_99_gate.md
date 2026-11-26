# Step 101 — Gate

**Exit condition.** What must hold before step 102 starts. The step's *entry* condition is a different
thing — see [`_00_prerequisites.md`](_00_prerequisites.md).

## Gate 101 → 102

| # | Kind | Condition | Status |
|---|---|---|---|
| 1 | script | [`scripts/validate_uoc.py`](scripts/validate_uoc.py) reports **EXACT MATCH** (or `VERBATIM after cosmetic normalisation`) for **every** unit in the cluster | **built + ported**, 46 cases (VU-01…46) green |

One condition, and no human review. Whether a transcription is faithful is a mechanical fact about two
files, and the gate is a stronger check than reading would be.

```bash
python3 factory/process_01_extraction/step_101_transcribe_uoc/scripts/validate_uoc.py \
  <cluster>/units_of_competency/original/<UNIT>_Complete_R<N>.docx \
  <cluster>/units_of_competency/<UNIT>_Complete_R<N>.md
```

Pairs are positional, and several may be given at once (`<docx1> <md1> <docx2> <md2> …`). The exit code
is the verdict: 0 when every pair is verbatim, 1 otherwise.

## Reading the verdict

| Verdict | Means | Do |
|---|---|---|
| **EXACT MATCH** | word-for-word identical | done — this is the normal outcome |
| **VERBATIM after cosmetic normalisation** | differs only in quotes, dashes, whitespace | accept, and report the cosmetic diffs — the operator may choose to clean the source |
| **SUBSTANTIVE DIFFERENCES FOUND** | a word landed in the wrong place or was missed | do not accept → [A](#a--when-a-transcription-does-not-validate) |
| **LIST STRUCTURE DIFFERS** | a bullet was flattened, invented or re-nested | do not accept → [A](#a--when-a-transcription-does-not-validate) |

**Never hand-edit the `.md` away from the source to force a pass.** That defeats the point of the step:
the file's value is that nothing in it was typed by a human or a model.

The gate reads the same source through the same `docx_text` helper the transcriber uses, so the two
agree about *words* by construction — the real work the word-level check does is catching a word landing
in the wrong structural place. The list-shape check is deliberately independent, reading bullet nesting
from the paragraph styles rather than from the text, so a flattened bullet fails even when every word is
present. What each side of the comparison covers is in
[`scripts/validate_uoc.md`](scripts/validate_uoc.md).

---

## Detail

### A — When a transcription does not validate

Rare, and it means the source uses a structural style the converter does not yet handle. The fix goes in
the script, once, for every future unit.

**1. Find the mis-shaped region** from the diff the gate prints, then identify the style of the
paragraph that produced it:

```bash
python3 - <<'PY'
import zipfile, xml.etree.ElementTree as ET
W="{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
body=ET.parse(zipfile.ZipFile("<source.docx>").open("word/document.xml")).getroot().find(f"{W}body")
for p in body.iter(f"{W}p"):
    txt="".join(n.text or "" for n in p.iter() if n.tag==f"{W}t")
    pPr=p.find(f"{W}pPr"); s=pPr.find(f"{W}pStyle") if pPr is not None else None
    style=s.get(f"{W}val") if s is not None else None
    if txt.strip(): print(style, "|", txt[:70])
PY
```

**2. Extend the right classifier** in `scripts/transcribe_uoc.py`:

| What is new | Where it goes |
|---|---|
| a heading style | `heading_level` |
| a list style | the `List…` pattern in `list_level` |
| a table shape | `render_table` / `cell_md` |
| a Word element carrying text | `common/helpers/docx_text.py` — `para_text` |

**3. Test-first, not straight to the code.** This is a behaviour change like any other: add the case to
[`factory/docs/test-plan.md`](../../docs/test-plan.md), write the test, watch it fail, then write the
code. See [test-first-process.md](../../../docs/test-first-process.md).

**4. Re-run the corpus sweep** before relying on it — transcribe every existing unit, validate, and diff
against the committed `.md`. A change that fixes one unit and moves another is a regression, and the
sweep is what makes that visible. The port of this script was adopted on exactly that evidence: 19 of 19
units byte-identical.
