# `validate_uoc.py` — what it compares, and what not to "fix"

Companion to the script. The docstrings cover what each function does; this covers the shape of the
comparison and the deliberate decisions that look like bugs when a result surprises you.

For what to do when a unit fails, see [`../_99_gate.md`](../_99_gate.md).

## What it compares

For each `<docx> <md>` pair the script builds two word sequences and diffs them.

**From the `.docx`** — `docx_text.docx_to_text`: textual content in document order, read straight from
`word/document.xml`. Paragraphs and table-cell paragraphs, with `w:t` → text, `w:tab` → tab,
`w:br`/`w:cr` → newline, `w:sym` → the character in its attribute, `w:noBreakHyphen` → a hyphen, and
any container element descended into. Table cells come out in row/column order with intra-cell line
breaks preserved, so they line up with the `<br>` markers inside markdown table cells.

**From the `.md`** — `md_to_text`: the prose with markdown *syntax* removed. Heading markers, table
pipe borders and `| --- |` separator rows, leading list markers (`-`/`*`/`+`/`N.`), and `<br>` back to
a newline. Table rows split into their cell contents. Only syntax is stripped, never content.

Both sides are then tokenised on whitespace and compared as word lists.

## The two tiers

| Tier | Means | Verdict |
|---|---|---|
| **Substantive** | a real word added, removed or changed. Computed on cosmetically-normalised text, so it never fires on punctuation style alone | `SUBSTANTIVE DIFFERENCES FOUND`, exit 1 |
| **Cosmetic** | the normalised sequences match but the raw ones differ — curly quotes, en/em dashes, non-breaking space, ellipsis, soft hyphen, BOM, NFC composition | `VERBATIM after cosmetic normalisation`, exit 0 |

The substitutions themselves live in `common/helpers/cosmetic.py`.

## Deliberate behaviours — don't "fix" these

1. **Headers and footers are excluded.** `word/header*.xml` and `word/footer*.xml` carry
   training-package attribution, the unit code and page numbers. They are not part of the
   transcription and are never compared, so content living only in a header will not show as missing.
2. **Markdown list markers are syntax, not content.** A leading `- ` is stripped before comparison.
   If it were not, every bulleted PE/KE/AC line would read as a spurious insertion.
3. **Foundation-skill names keep their exact casing and spacing.** The source documents are
   inconsistent — `Oral communication` in one unit, `Oral Communication` in another. The transcription
   preserves the source verbatim, and the diff catches a "correction".
4. **Nested structures are quoted whole.** A parent bullet with indented children — a KE item listing
   IaaS/PaaS/SaaS sub-points, say — is one block of text on both sides, and the word diff sees the
   combined words. Their *shape* is what the list check looks at separately.

## Where the independence sits

Both this script and the transcriber read words through `docx_text`, so the word diff is not a second
opinion on extraction — it checks that every extracted word survived into the right structural place.

`docx_list_shape` is the independent half. It reads bullet nesting from the source **paragraph styles**,
which the transcription never touches, and it counts **any** style starting `List` — wider than the
transcriber's `List(Bullet|Number|Paragraph)` rule on purpose, so a style the transcriber does not
handle surfaces as a mismatch instead of silently flattening.

That check earns its place downstream: step 102 itemises PE/KE/AC by counting top-level bullets, so a
flattened bullet is a lost assessable item, not a formatting difference.

## Adapting to a new course

The comparison is content-agnostic — any `<docx>`/`<md>` pair, any unit code, any training package. The
only assumptions are the OOXML structure of a standard `.docx` and ordinary markdown in the `.md`.

If a new course's markdown introduces syntax this script does not strip — an unusual table style,
footnotes, embedded HTML beyond `<br>` — **extend `md_to_text` rather than loosening the diff.** Keeping
the comparison strict is the whole point of the gate.
