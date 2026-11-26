# `transcribe_uoc.py` — the style mapping, and what not to "fix"

Companion to the script. The docstrings cover what each function does; this covers what was **observed
across the ICT and BSB unit corpus**, and the behaviours that look like bugs and are not.

Read it when adapting to a training package whose Word template differs. For the failure procedure —
what to do when a transcription does not validate — see [`../_99_gate.md`](../_99_gate.md).

## Style → Markdown mapping

| Source paragraph style | Rendered as |
|---|---|
| `Title`, `Heading1`–`Heading6` | `#`…`######` heading (Title and Heading1 both → `#`) |
| `ListBullet` | top-level `- ` bullet |
| `ListBullet2`, `ListBullet3`, … | nested bullet, indented 2 spaces per level past the first |
| `ListNumber`, `ListParagraph` (+ suffixes) | the same, for numbered and Word's generic list style |
| `SuperHeading`, `Version`, `BodyText`, unstyled | plain paragraph |
| empty / `AllowPageBreak` | dropped (spacer) |
| `w:tbl` (table) | Markdown table; each cell = its non-empty paragraphs joined with `<br>` |

Nesting depth comes from the **style-name suffix** (`ListBullet2` → depth 1), falling back to
`w:numPr`/`w:ilvl` for numbered lists carrying no `List*` style.

Preserving depth as two-space indentation matters downstream: the consolidation validator counts only
top-level `- ` bullets and treats indented sub-bullets as part of their parent item. Flattening them
would inflate the assessable-item inventory.

## Deliberate behaviours — don't "fix" these

1. **Headers and footers are excluded.** Only `word/document.xml` is read; page furniture lives in
   separate zip parts and is correctly absent — it is not unit content.
2. **Horizontal whitespace collapses.** Runs of spaces and tabs become one space. Whitespace only,
   never a word, so the gate's word-level check is unaffected; it keeps output consistent with the
   existing corpus, some of which carries stray double spaces in the source.
3. **Every table gets a header underline.** Row 0 is treated as the header and a `| --- |` separator
   follows it — matching how the gate skips that row when stripping markdown.
4. **Content controls are traversed.** Anything wrapped in a `w:sdt` — or any other container — is
   read rather than skipped, so wrapped content is not lost.

## Why the output round-trips through the gate

The gate's `md_to_text` strips markdown syntax — headings, table pipes, the `| --- |` row, leading
bullets, `<br>` back to newline — and compares the remaining words against the `.docx`. This script is
built so that stripping its output recovers exactly the source words in order, which is why transcribe
then validate yields `EXACT MATCH`.

Both scripts read the source through the same `docx_text` helper, so they agree about *words* by
construction. They are **not** blind together on structure: the gate reads bullet nesting independently,
from the paragraph styles, so a flattened bullet still fails even though the words match.
