"""The canonical reference to an assessable item: `[ICTCLD501 PC 1.2]`.

Every artefact downstream of extraction trades in these — the consolidated UoC, the assessment plan, the
AT marking benchmarks, the mapping documents. This is the one definition of what one looks like, holding
the **writer and the reader together** so the two cannot drift apart.

Distinct from `scripts/helpers/uoc_tags.py`, which stamps a visual evidence tag into a .docx footer: a
different job that happens to share the word "tag".

**Any correctly-formed unit code, not an allow-list.** The scripts this replaces matched `ICT`, `BSB` or
`VU` only, so a cluster from any other training package crashed the gate on an unmatched search. The
factory is meant to serve any qualification, so the pattern describes the SHAPE of a unit code rather
than enumerating packages.

Two jobs, deliberately in one module because callers need both: **recognising** a reference
(`find_all`, `first`, `format`) and **resolving** one (`expand`, `resolve`, `valid_set`) — turning what
someone wrote into the concrete items it names. A reference may be compressed (`PC 1.1-1.4`),
abbreviated (`[PC 2.1]`, inheriting a unit from earlier on the line) or compound
(`[ICTCLD401 KE 1 · ICTCLD502 KE 1]`), and every coverage check downstream counts ITEMS — so a
compressed reference left unexpanded reads as one item and the register silently shrinks.

Behaviour is specified by cases HIR-01 .. HIR-36 in factory/docs/test-plan.md.
"""
import re

#: The five assessable sections of a unit of competency. The whole vocabulary.
SECTIONS = ("PC", "FS", "PE", "KE", "AC")

#: A unit code by shape, not by name: two or more leading capitals, then alphanumerics, ending in at
#: least three digits. The leading capitals exclude a course code (22603VIC); the trailing digits
#: exclude a bracketed word beside a section keyword ([NOTE PE 1], [AT1 PE 2]).
UNIT_CODE = r"[A-Z]{2,}[A-Z0-9]*[0-9]{3,}"

#: The numbering is whatever remains before the closing bracket — `1.2`, `7`, or a Foundation Skill's
#: verbatim name, which contains spaces.
PATTERN = re.compile(rf"\[({UNIT_CODE}) ({'|'.join(SECTIONS)}) ([^\]]+)\]")

_CODE_SPAN = re.compile(r"`[^`]*`")


def format(unit: str, section: str, numbering: str) -> str:
    """A reference in canonical form."""
    return f"[{unit} {section} {numbering}]"


def first(text: str):
    """The first reference in ``text`` as ``(unit, section, numbering)``, or None.

    None rather than a raise: a body of text with no reference is an ordinary thing for a caller to
    meet, and it should be able to report which line disappointed it rather than die on a match
    object that turned out to be None.
    """
    match = PATTERN.search(text)
    if match is None:
        return None
    unit, section, numbering = match.groups()
    return unit, section, numbering.strip()


def find_all(text: str) -> list[tuple[str, str, str]]:
    """Every reference in ``text``, in document order, **one entry per occurrence**.

    Deliberately not de-duplicated: the consolidation gate counts occurrences to catch an item placed
    in two groups, so collapsing them here would silently disable that check.
    """
    return [(unit, section, numbering.strip())
            for unit, section, numbering in PATTERN.findall(text)]


def strip_code_spans(text: str) -> str:
    """``text`` with backtick-wrapped spans removed — a wrapped reference is a citation, not an item.

    Editorial prose cites references (`` `[ICTCLD501 PC 1.1]` ``) while discussing a group. Counting
    those as items would report a duplicate for every reference an author mentioned in passing.
    """
    return _CODE_SPAN.sub("", text)


# --- Resolution: what a written reference actually names ----------------------------------------

_BRACKET = re.compile(r"\[([^\]]+)\]")
_FULL = re.compile(rf"^({UNIT_CODE})\s+({'|'.join(SECTIONS)})\s+(.+)$")
_ABBR = re.compile(rf"^({'|'.join(SECTIONS)})\s+(.+)$")
_COMPOUND = re.compile(r"\s*·\s*")
_RANGE = re.compile(r"^(\d+(?:\.\d+)?)\s*[–—-]\s*(\d+(?:\.\d+)?)$")
_LEADING_NUMBER = re.compile(r"^(\d+(?:\.\d+)?)\b")
_RANGE_ANYWHERE = re.compile(r"\d\s*[–—-]\s*\d")


def _is_compressed(numbering: str) -> bool:
    """True when a numbering names more than one item."""
    return ("," in numbering) or bool(_RANGE_ANYWHERE.search(numbering))


def expand(numbering: str) -> list[str]:
    """A compressed numbering as its individual members.

    `1-6` is six knowledge-evidence items; `1.1-1.4` is four performance criteria; `3, 4, 6` is three.
    A Foundation Skill's name, or a plain single number, passes through unchanged.

    A dotted range spanning two majors (`1.4-2.1`) yields only its endpoints: how many criteria sit
    between 1.4 and 2.1 is a property of the unit, not of the notation, so inventing the members would
    be guessing.
    """
    numbering = numbering.strip()

    if "," in numbering:
        return [member for part in numbering.split(",") for member in expand(part)]

    ranged = _RANGE.match(numbering)
    if ranged:
        low, high = ranged.groups()
        if "." in low and "." in high:
            low_major, low_minor = low.split(".")
            high_major, high_minor = high.split(".")
            if low_major == high_major and low_minor.isdigit() and high_minor.isdigit():
                return [f"{low_major}.{i}" for i in range(int(low_minor), int(high_minor) + 1)]
            return [low, high]
        if low.isdigit() and high.isdigit():
            return [str(i) for i in range(int(low), int(high) + 1)]
        return [low, high]

    # A numeric item with a trailing qualifier ("4.3 - partial") is still that item; a skill name,
    # which has no leading digit, is itself.
    leading = _LEADING_NUMBER.match(numbering)
    return [leading.group(1)] if leading else [numbering]


def resolve(line: str):
    """Yield ``((unit, section, numbering), form)`` for each item the line references.

    Handles the three ways a reference is written short:

    - **compressed** — `[ICTCLD501 KE 1-3]` names three items; each is yielded separately.
    - **abbreviated** — `[PC 2.1]` inherits the unit from the nearest preceding full reference on the
      line, because authors name the unit once and abbreviate after it.
    - **compound** — `[ICTCLD401 KE 1 · ICTCLD502 KE 1]` names two units in one bracket.

    ``form`` is ``full``, ``abbrev``, ``compressed`` or ``unresolved``, and callers use it: a
    compressed reference covers its members but was not written item by item, which some checks report
    differently. An abbreviated reference with no unit to inherit yields a unit of None and the form
    ``unresolved`` — a defect in the document, reported rather than guessed at.

    Bracketed text that is not a reference at all (`[the appendix]`, `[TBD]`) is ignored: unresolved is
    for a genuine reference missing its unit, not for prose in brackets.
    """
    current_unit = None

    for match in _BRACKET.finditer(line):
        inside = match.group(1).strip()
        for part in _COMPOUND.split(inside):
            part = part.strip()
            compound = part != inside

            full = _FULL.match(part)
            if full:
                unit, section, numbering = full.group(1), full.group(2), full.group(3).strip()
                current_unit = unit
                form = "compressed" if (_is_compressed(numbering) or compound) else "full"
                for member in expand(numbering):
                    yield ((unit, section, member), form)
                continue

            abbreviated = _ABBR.match(part)
            if abbreviated:
                section, numbering = abbreviated.group(1), abbreviated.group(2).strip()
                if current_unit is None:
                    yield ((None, section, numbering), "unresolved")
                    continue
                form = "compressed" if (_is_compressed(numbering) or compound) else "abbrev"
                for member in expand(numbering):
                    yield ((current_unit, section, member), form)


def valid_set(text: str) -> set[tuple[str, str, str]]:
    """Every reference a document defines, de-duplicated, code spans excluded.

    The counterpart to `find_all`: that answers *how often*, this answers *what exists*. A checker
    comparing a plan's coverage against the items a consolidated UoC defines wants this one.
    """
    return set(find_all(strip_code_spans(text)))
