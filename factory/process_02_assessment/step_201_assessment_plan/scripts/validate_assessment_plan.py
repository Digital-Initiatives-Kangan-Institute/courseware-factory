#!/usr/bin/env python3
"""Validate a cluster's assessment_plan.md — the Gate 201 -> 202 check.

Two questions, answered separately:

  FORMAT    the plan is well-formed: the sections the standard names, present and in order; a header
            carrying STATUS and a scenario binding; every AT declaring both what it evidences and what
            the scenario must supply; an SR-* register that its own section 3 references consistently.

  COVERAGE  every PC/PE/KE/FS item in the cluster's consolidated_uoc.md is claimed by at least one AT,
            and nothing is claimed that no unit contains. AC items are discharged through the SR
            register rather than by direct coverage, so they are reported as information.

This is where a cluster decides WHAT WILL BE ASSESSED, so an item no AT claims is an item nobody builds
an instrument for -- and it surfaces much later as a coverage gap in a document nobody expected to be
short.

The section list is driven by the `## Skeleton` block of the format standard, so changing the standard
moves the checks with no code edit.

Behaviour is specified by cases VAP-01 .. VAP-28 in factory/docs/test-plan.md.

stdlib only.

Usage:
  validate_assessment_plan.py --cluster <cluster dir> [--plan <path>] [--consolidated <path>]
                              [--format <path>]

Exit 0 = PASS (format valid AND coverage complete), 1 = defects, 2 = inputs unreadable.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common" / "helpers"))

import format_contract  # noqa: E402
import item_reference as ref  # noqa: E402
import md_section  # noqa: E402
import scenario_requirement as sr  # noqa: E402

FORMAT_DOC = "assessment-plan-format.md"
COVERED_SECTIONS = ("PC", "PE", "KE", "FS")

_TITLE = re.compile(r"^#\s+.*Cluster Assessment Plan\b", re.MULTILINE)
_STATUS = re.compile(r"^>\s*\*\*STATUS", re.MULTILINE)
_AT_BLOCK = re.compile(r"^###\s+(AT\d+)\b.*$", re.MULTILINE)
_AT_TABLE_ROW = re.compile(r"^\|.*\bAT\d+\b", re.MULTILINE)


def check_format(text: str, cluster_token: str, headings: list[str]):
    """Return ``(problems, advisories, uoc_refs, sr_refs, sr_defs)``.

    ``headings`` comes from the format standard's skeleton, so the section list is the standard's to
    change. Everything else here is structure the standard describes in prose.
    """
    lines = text.splitlines()
    problems: list[str] = []
    advisories: list[str] = []

    # 1) The sections the standard names, present and in the order it names them.
    last_seen = -1
    for heading in headings:
        pattern = rf"^{re.escape(heading)}\b"
        index = next((i for i, line in enumerate(lines) if re.match(pattern, line)), None)
        if index is None:
            problems.append(f"missing required section: {heading}")
        elif index < last_seen:
            problems.append(f"section out of order: {heading}")
        else:
            last_seen = index

    # 2) Header fields.
    if not _TITLE.search(text):
        problems.append("missing the title — '# … Cluster Assessment Plan'")
    if not _STATUS.search(text):
        problems.append("header missing a '> **STATUS** …' line")
    if "Scenario binding" not in text:
        problems.append("header missing a 'Scenario binding' line")

    # 3) Section 3 — the AT roster table, and a block per AT declaring both of its fields.
    section3 = md_section.span(text, r"^##\s+3\.", [r"^##\s+4\."]) or ""
    if not _AT_TABLE_ROW.search(section3):
        problems.append("§3 has no AT table row (expected a markdown table listing the ATs)")

    labels = _AT_BLOCK.findall(section3)
    if not labels:
        problems.append("§3 has no '### ATn' per-AT detail blocks")

    uoc_refs: set[tuple[str, str, str]] = set()
    sr_refs: set[str] = set()
    for label, chunk in zip(labels, _AT_BLOCK.split(section3)[2::2]):
        if "UoC coverage:" not in chunk:
            problems.append(f"{label} block missing a 'UoC coverage:' field")
        if "Scenario requirements:" not in chunk:
            problems.append(f"{label} block missing a 'Scenario requirements:' field")

        for line in chunk.splitlines():
            if "UoC coverage:" in line:
                for reference, form in ref.resolve(line):
                    if form == "unresolved":
                        problems.append(
                            f"{label} UoC coverage has an unresolved reference: "
                            f"[{reference[1]} {reference[2]}] — no unit to inherit")
                    else:
                        uoc_refs.add(reference)
            if "Scenario requirements:" in line:
                sr_refs.update(sr.find_all(line))

    # 4) Section 6 — the register, cluster-scoped.
    section6 = md_section.span(text, r"^##\s+6\.", [r"^##\s+7\."]) or ""
    sr_defs = set(sr.find_all(section6))
    if not sr_defs:
        problems.append("§6 scenario requirements register defines no SR-… rows")
    for requirement in sorted(sr_defs, key=sr.parse):
        if not requirement.startswith(f"SR-{cluster_token}-"):
            problems.append(f"§6 SR id '{requirement}' is not cluster-scoped "
                            f"(expected SR-{cluster_token}-NN)")

    # 5) The two halves agree: every SR an AT leans on is something the scenario is asked to build.
    for requirement in sorted(sr_refs - sr_defs, key=sr.parse):
        problems.append(f"§3 references {requirement}, which is not defined in §6")
    for requirement in sorted(sr_defs - sr_refs, key=sr.parse):
        advisories.append(f"§6 defines {requirement} but no AT references it")

    return problems, advisories, uoc_refs, sr_refs, sr_defs


def check_coverage(uoc_refs: set, consolidated_text: str):
    """Return ``(missing, phantom, info_ac, required_count)``.

    AC items are deliberately not required: an assessment condition is discharged by the scenario
    supplying something, which the SR register tracks, not by an AT claiming to evidence it.
    """
    valid = ref.valid_set(consolidated_text)
    required = {r for r in valid if r[1] in COVERED_SECTIONS}

    missing = sorted(required - uoc_refs)
    phantom = sorted(uoc_refs - valid)
    info_ac = sorted(r for r in uoc_refs if r[1] == "AC")
    return missing, phantom, info_ac, len(required)


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a cluster assessment plan (format + coverage).")
    ap.add_argument("--cluster", required=True, type=Path)
    ap.add_argument("--plan", type=Path, help="default <cluster>/assessments/assessment_plan.md")
    ap.add_argument("--consolidated", type=Path, help="default <cluster>/consolidated_uoc.md")
    ap.add_argument("--format", dest="format_doc", type=Path, help=f"default: located {FORMAT_DOC}")
    args = ap.parse_args()

    plan_path = args.plan or (args.cluster / "assessments" / "assessment_plan.md")
    consolidated_path = args.consolidated or (args.cluster / "consolidated_uoc.md")

    if not plan_path.is_file():
        print(f"ERROR: no assessment_plan.md at {plan_path}", file=sys.stderr)
        return 2

    located = format_contract.find_format_doc(
        FORMAT_DOC, explicit=args.format_doc, start=Path(__file__).resolve().parent)
    if located is None:
        print(f"ERROR: could not locate {FORMAT_DOC} — pass --format", file=sys.stderr)
        return 2
    headings, _fields, _columns = format_contract.parse_contract(
        located.read_text(encoding="utf-8"))
    if not headings:
        print(f"ERROR: {located} has no '## Skeleton' block to read the contract from",
              file=sys.stderr)
        return 2

    cluster_match = re.search(r"(CL\d+)", args.cluster.name)
    cluster_token = cluster_match.group(1) if cluster_match else "CL?"

    print(f"=== {plan_path} ===")
    problems, advisories, uoc_refs, sr_refs, sr_defs = check_format(
        plan_path.read_text(encoding="utf-8"), cluster_token, headings)

    if problems:
        print(f"  FORMAT: FAIL — {len(problems)} issue(s)")
        for problem in problems:
            print(f"    [FAIL] {problem}")
    else:
        print(f"  FORMAT: PASS — all sections present; "
              f"{len(sr_defs)} SR defined, {len(sr_refs)} referenced")
    for advisory in advisories:
        print(f"    [info] {advisory}")

    coverage_failed = False
    if consolidated_path.is_file():
        missing, phantom, info_ac, required = check_coverage(
            uoc_refs, consolidated_path.read_text(encoding="utf-8"))
        if missing or phantom:
            coverage_failed = True
            print(f"  COVERAGE: FAIL — {len(missing)} missing, {len(phantom)} phantom "
                  f"(of {required} required)")
            for reference in missing:
                print(f"    [MISSING] {ref.format(*reference)} — no AT's UoC coverage references it")
            for reference in phantom:
                print(f"    [PHANTOM] {ref.format(*reference)} — not a real UoC item")
        else:
            extra = f" (+{len(info_ac)} AC via the SR register)" if info_ac else ""
            print(f"  COVERAGE: PASS — all {required} PC/PE/KE/FS items referenced by an AT{extra}")
    else:
        print(f"  COVERAGE: SKIPPED — no consolidated UoC at {consolidated_path}")

    ok = not problems and not coverage_failed
    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
