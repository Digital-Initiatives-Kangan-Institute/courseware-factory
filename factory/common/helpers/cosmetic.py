"""Folding the character substitutions Word makes on the author's behalf.

A comparison between a Word source and a text copy of it needs to separate two very different things:
*the author wrote something different* and *Word curled a quote*. This folds the second so the first
stands out.

Deliberately narrow — typography only, never whitespace and never a word. Collapsing whitespace here
would hide a respaced compound (`IaaS/PaaS/SaaS` retyped as `IaaS / PaaS / SaaS`), which is a real edit
to a real token, not a cosmetic difference.

Behaviour is specified by cases HCOS-01 .. HCOS-10 in factory/docs/test-plan.md.
"""
import unicodedata

# Word's substitutions, folded to what the author typed. Every replacement's target is a character
# no other entry maps away from, so applying this twice changes nothing (HCOS-10).
SUBSTITUTIONS = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",   # curly / low / reversed singles
    "“": '"', "”": '"', "„": '"', "‟": '"',   # curly / low / reversed doubles
    "–": "-", "—": "-", "−": "-", "‑": "-",   # en / em / minus / non-breaking
    " ": " ",                                                # non-breaking space
    "…": "...",                                              # horizontal ellipsis
    "­": "",                                                 # soft hyphen — invisible in Word
    "﻿": "",                                                 # byte-order mark
}


def normalise(text: str) -> str:
    """Fold Word's typographic substitutions, leaving words and whitespace alone.

    Composition (NFC) comes first, so text carrying a combining accent compares equal to the same
    text written with the precomposed character.
    """
    text = unicodedata.normalize("NFC", text)
    for source, target in SUBSTITUTIONS.items():
        text = text.replace(source, target)
    return text
