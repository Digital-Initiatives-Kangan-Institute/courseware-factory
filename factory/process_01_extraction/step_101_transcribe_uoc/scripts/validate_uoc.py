#!/usr/bin/env python3
"""Prove a .md UoC transcription is verbatim against its source .docx — the Gate 01 -> 02 oracle.

Three failure modes must be caught: content in the source MISSING from the transcription, content in
the transcription NOT IN the source, and content MISTRANSCRIBED (changed, renumbered, re-cased,
re-ordered, duplicated). It must equally not cry wolf on what is legitimately different: markdown
syntax, page furniture, whitespace, and the typography Word applies on the author's behalf.

Two checks, either of which blocks the gate:

  WORDS   extract the .docx in document order, strip markdown from the .md, diff the word sequences.
          Reported in two tiers - substantive (a real difference) and cosmetic (quotes, dashes).
  SHAPE   read bullet nesting from the source paragraph STYLES and compare against the markdown's
          indentation. This is the independent half: both scripts now read words through docx_text,
          so the word diff cannot see a fault in the reader itself - but the shape check reads
          something the transcription never touches. A flattened bullet fails here even when every
          word matches, which matters because step 02 itemises PE/KE/AC by counting top-level
          bullets: a flattened bullet is a lost assessable item, not a cosmetic difference.

Behaviour is specified by cases VU-01 .. VU-46 in factory/docs/test-plan.md. What the comparison
covers on each side, and the deliberate behaviours that look like bugs, are in the companion
`validate_uoc.md` beside this file.

stdlib only.

Usage:  python3 validate_uoc.py <docx1> <md1> [<docx2> <md2> ...]
        exit 0 when every pair is verbatim, 1 otherwise, 2 on a usage error.
"""
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common" / "helpers"))

import cosmetic  # noqa: E402
import docx_text as dx  # noqa: E402
import md_table  # noqa: E402

BR = re.compile(r"<br\s*/?>", re.IGNORECASE)
HEADING = re.compile(r"^#{1,6}\s+(.*)$")
LIST_MARKER = re.compile(r"^([-*+]|\d+\.)\s+(.*)$")
MD_BULLET = re.compile(r"^( *)- ")
STYLE_SUFFIX = re.compile(r"(\d+)$")


def md_to_text(md_path: Path) -> str:
    """The .md with its markdown syntax stripped, leaving the words.

    Removes heading markers, list markers, table pipes and the separator row, and turns `<br>` back
    into a line break so a multi-paragraph cell lines up with how the source cell reads.
    """
    lines = []
    for line in md_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            lines.append("")
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            cells = md_table.split_row(stripped)
            if md_table.is_separator(cells):
                continue
            for cell in cells:
                lines.extend(part.strip() for part in BR.split(cell))
            continue

        heading = HEADING.match(stripped)
        if heading:
            lines.append(heading.group(1))
            continue

        marker = LIST_MARKER.match(stripped)
        if marker:
            stripped = marker.group(2)

        lines.extend(part.strip() for part in BR.split(stripped))
    return "\n".join(lines)


def to_words(text: str) -> list[str]:
    """Tokenise to words, ignoring all whitespace and line structure."""
    return text.split()


def docx_list_shape(docx_path: Path) -> list[int]:
    """The source's list structure: one nesting depth per list paragraph, in document order.

    Read from the paragraph STYLES, which is what makes this independent of the transcription and of
    the shared text reader. Any style starting `List` counts — deliberately wider than the
    transcriber's `List(Bullet|Number|Paragraph)` rule, so a style it does not handle shows up as a
    mismatch rather than silently flattening.

    Paragraphs inside a table are excluded, because `iter_blocks` yields a table as one block without
    descending into it. That is not incidental: the real UoC documents style many table-cell
    paragraphs `List`, and those render as table rows, not bullets.
    """
    body = dx.body(docx_path)
    if body is None:
        return []

    depths = []
    for kind, elem in dx.iter_blocks(body):
        if kind != "p":
            continue
        style = dx.para_style(elem)
        if not style or not style.startswith("List"):
            continue
        if not dx.para_text(elem).strip():          # a spacer styled as a bullet is not an item
            continue
        suffix = STYLE_SUFFIX.search(style)
        depths.append(int(suffix.group(1)) - 1 if suffix else 0)
    return depths


def md_list_shape(md_path: Path) -> list[int]:
    """The transcription's list structure — one depth per bullet, from its indentation."""
    depths = []
    for line in md_path.read_text(encoding="utf-8").splitlines():
        match = MD_BULLET.match(line)
        if match:
            depths.append(len(match.group(1)) // 2)
    return depths


def diff_report(label: str, docx_text: str, md_text: str) -> dict:
    """Compare two texts at word level, in a substantive tier and a cosmetic tier."""
    docx_words = to_words(docx_text)
    md_words = to_words(md_text)
    raw_match = docx_words == md_words

    docx_norm = to_words(cosmetic.normalise(docx_text))
    md_norm = to_words(cosmetic.normalise(md_text))
    cosmetic_match = docx_norm == md_norm

    findings = {
        "label": label,
        "docx_word_count": len(docx_words),
        "md_word_count": len(md_words),
        "exact_match": raw_match,
        "cosmetic_match": cosmetic_match,
        "substantive_diff": [],
        "cosmetic_diff": [],
        "structure_diff": [],
        "empty_source": not docx_words,
    }

    if not docx_words:
        # Nothing extracted from the .docx — an empty or unreadable body would otherwise agree with
        # an empty .md and report a verbatim match over zero content. Never a pass.
        findings["exact_match"] = False
        findings["cosmetic_match"] = False
        return findings

    if not cosmetic_match:
        for tag, i1, i2, j1, j2 in _opcodes(docx_norm, md_norm):
            findings["substantive_diff"].append({
                "op": tag,
                "docx_range": (i1, i2),
                "md_range": (j1, j2),
                "docx_words": docx_norm[i1:i2],
                "md_words": md_norm[j1:j2],
            })
    elif not raw_match:
        for tag, i1, i2, j1, j2 in _opcodes(docx_words, md_words):
            findings["cosmetic_diff"].append({
                "op": tag,
                "docx_words": docx_words[i1:i2],
                "md_words": md_words[j1:j2],
            })

    return findings


def _opcodes(a: list, b: list):
    """The non-equal opcodes between two sequences."""
    matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    return [op for op in matcher.get_opcodes() if op[0] != "equal"]


def compare(docx_path: Path, md_path: Path, label: str) -> dict:
    """The full gate over one pair: word content plus list shape."""
    findings = diff_report(label, dx.docx_to_text(docx_path), md_to_text(md_path))

    docx_shape = docx_list_shape(docx_path)
    md_shape = md_list_shape(md_path)
    if docx_shape != md_shape:
        for tag, i1, i2, j1, j2 in _opcodes(docx_shape, md_shape):
            findings["structure_diff"].append({
                "op": tag,
                "at_bullet": i1,
                "docx_depths": docx_shape[i1:i2],
                "md_depths": md_shape[j1:j2],
            })

    findings["docx_bullets"] = len(docx_shape)
    findings["md_bullets"] = len(md_shape)
    return findings


def print_findings(f: dict) -> None:
    """Report one pair's verdict, and enough of the difference to act on."""
    print(f"\n{'=' * 70}")
    print(f"  {f['label']}")
    print(f"{'=' * 70}")
    print(f"  docx words: {f['docx_word_count']}    md words: {f['md_word_count']}")
    print(f"  docx bullets: {f['docx_bullets']}    md bullets: {f['md_bullets']}")

    if f["structure_diff"]:
        print("  RESULT: LIST STRUCTURE DIFFERS — a bullet was flattened, invented, or re-nested")
        for d in f["structure_diff"]:
            print(f"    [{d['op']}] at bullet {d['at_bullet']}  "
                  f"docx depths {d['docx_depths']} != md depths {d['md_depths']}")
        return

    if f["empty_source"]:
        print("  RESULT: FAIL — no extractable text in the .docx (nothing to validate against)")
        return

    if f["exact_match"]:
        print("  RESULT: EXACT MATCH (byte-equivalent at word level)")
        return

    if f["cosmetic_match"]:
        print("  RESULT: VERBATIM after cosmetic normalisation (quotes/dashes/whitespace)")
        if f["cosmetic_diff"]:
            print(f"  Cosmetic-only diffs ({len(f['cosmetic_diff'])} blocks):")
            for d in f["cosmetic_diff"][:10]:
                print(f"    [{d['op']}]  docx: {d['docx_words']!r}")
                print(f"          md:   {d['md_words']!r}")
            if len(f["cosmetic_diff"]) > 10:
                print(f"    ... and {len(f['cosmetic_diff']) - 10} more")
        return

    print("  RESULT: SUBSTANTIVE DIFFERENCES FOUND")
    print(f"  Substantive diff blocks: {len(f['substantive_diff'])}")
    for d in f["substantive_diff"]:
        print(f"\n    [{d['op']}] docx[{d['docx_range'][0]}:{d['docx_range'][1]}]  "
              f"md[{d['md_range'][0]}:{d['md_range'][1]}]")
        print(f"      docx: {' '.join(d['docx_words'])!r}")
        print(f"      md:   {' '.join(d['md_words'])!r}")


def main() -> int:
    pairs = sys.argv[1:]
    if not pairs or len(pairs) % 2 != 0:
        print("Usage: validate_uoc.py <docx1> <md1> [<docx2> <md2> ...]", file=sys.stderr)
        return 2

    failed = False
    for i in range(0, len(pairs), 2):
        docx_path, md_path = Path(pairs[i]), Path(pairs[i + 1])
        findings = compare(docx_path, md_path, f"{docx_path.name}  vs  {md_path.name}")
        print_findings(findings)
        if not findings["cosmetic_match"] or findings["structure_diff"]:
            failed = True

    print()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
