"""The `SR-<CLUSTER>-NN` reference: something the scenario must supply.

The system's second reference type, deliberately shaped like the first. `[ICTCLD501 PC 1.2]` names
something a UNIT requires; `SR-CL2-01` names something the SCENARIO must provide so an assessment can
be attempted at all — an intranet page, a lab artefact, a named stakeholder.

They travel together through the run-sheet: an assessment plan's §6 defines them, its §3 references
them, the scenario plan's build checklist claims to satisfy them, and the consolidated plan unions
them into the contract the scenario is validated against.

Behaviour is specified by cases HSR-01 .. HSR-10 in factory/docs/test-plan.md.
"""
import re

#: A cluster token is letters then digits (CL2, CL10), so ten clusters do not break the format.
PATTERN = re.compile(r"\bSR-([A-Z]+)(\d+)-(\d+)\b")


def find_all(text: str) -> list[str]:
    """Every SR reference in ``text``, in document order, one entry per occurrence.

    Returned exactly as written — padding included, because how an author numbers their register is
    theirs. Not de-duplicated: callers compare a set of references against a set of definitions, and
    build those sets themselves.
    """
    return [f"SR-{cluster}{number}-{sequence}"
            for cluster, number, sequence in PATTERN.findall(text)]


def parse(sr_id: str):
    """``(cluster_prefix, cluster_number, sequence)`` for an id, or None if it is not one.

    Also the canonical ordering: ``sorted(refs, key=parse)``. That matters because the parts are
    numbers wearing a string. Sorted lexically, `SR-CL10-01` lands before `SR-CL2-01`, so a
    consolidated register spanning ten clusters comes out silently mis-ordered.
    """
    match = PATTERN.search(sr_id)
    if match is None:
        return None
    cluster, number, sequence = match.groups()
    return cluster, int(number), int(sequence)
