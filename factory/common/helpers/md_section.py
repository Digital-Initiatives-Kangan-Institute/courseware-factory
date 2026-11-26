"""The lines of one section of a markdown document.

A validator that checks a document section by section needs to isolate one section before looking
inside it — "does §3 carry an AT table", "does §6 define any SR rows". Two validators carried a
byte-identical copy of this; here it is once.

Distinct from `md_table.rows_under_heading`, which returns table *rows* under a heading and ends at the
next heading of any level. This returns raw *lines* and takes explicit end patterns, because a numbered
section ends at the next numbered section, not at a `###` subheading inside it.

Behaviour is specified by cases HMS-01 .. HMS-07 in factory/docs/test-plan.md.
"""
import re


def span(text: str, start: str, until) -> str | None:
    """The section beginning at the line matching ``start``, up to the first line matching ``until``.

    ``start`` and ``until`` are regular expressions matched at the beginning of a line; ``until`` is a
    sequence, because a section may be ended by more than one thing.

    The start line is **included** — a caller checking §3 usually wants the heading too. The end line
    is excluded: it belongs to the next section.

    Returns **None** when no line matches ``start``, which is not the same as an empty section. A
    caller writing ``span(...) or ""`` is treating "the document has no §3 at all" as a format failure
    and "§3 exists and is empty" as something to look inside; both need to be sayable.
    """
    lines = text.splitlines()

    first = next((i for i, line in enumerate(lines) if re.match(start, line)), None)
    if first is None:
        return None

    last = len(lines)
    for i in range(first + 1, len(lines)):
        if any(re.match(pattern, lines[i]) for pattern in until):
            last = i
            break

    return "\n".join(lines[first:last])
