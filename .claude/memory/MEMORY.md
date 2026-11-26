# Memory index

**LLM-only** durable memory for the **courseware-factory**: course-agnostic working principles —
how Claude operates here, for any course. Course working state lives in each course repo, not here.
"Principles, not state" — see [[memory-principles-not-state]]. One line per memory; topic files hold
the detail, loaded on demand.

> **Both-audience knowledge** (process, conventions, format standards) lives in **`docs/`**,
> catalogued in [docs/INDEX.md](../../docs/INDEX.md).

## Working principles
- [one course-agnostic mechanism](one_course_agnostic_mechanism.md) — **the single most important factor:** exactly ONE mechanism per artefact type across all clusters + courses (one source of truth, one engine, one process); unify first-built/legacy paths onto it, never fork; a capability gap becomes a feature of the one engine; reproduce→validate→adopt before retiring the old path.
- [memory = principles not state](memory_principles_not_state.md) — record durable decisions/rationale (the non-derivable WHY); never repo-derivable ephemeral state (paths, commits, "what's built") — it goes stale on creation.
- [record current-state only](feedback_process_docs_current_only.md) — record things as they ARE, not how they used to be, in everything (docs, memory, status notes): current method only, no abandoned-path archaeology; git holds it.
- [current practice, not policy](feedback_current_practice_not_policy.md) — never write our own choices up as decided/locked/canonical/never/must; they are the current approach, open to evolution. **Documentation is never grounds for declining an idea.** A thing tried once is not a convention. Sole exception: a constraint we have no capability to change.
- [write deliverables at final confidence](feedback_deliverables_final_confidence.md) — author docs as if open dependencies were done; track the dependency in MEMORY, never as an in-text "draft pending X" hedge.
- [checks inform, they don't decide](feedback_checks_inform_not_decide.md) — never frame a check/lookup as "this decides it", and never as a dead end; it yields a data point weighed against everything else.
- [verify change impact](feedback_verify_change_impact.md) — before side-effecting changes (esp. running file-writing generators), verify where output lands + `git status` what got staged.
- [draft naming pragmatism](feedback_draft_naming_pragmatism.md) — during drafts, don't fuss over file naming; defer naming discipline to delivery-ready versions. Internal identifiers optimise for maintainer/LLM findability.
- [audit generated docs via the .py builders](feedback_audit_generated_docs.md) — a cross-cutting content sweep must grep the `.py` builders (course generators + factory engine); instruments are generated `.docx`, decks `.pptx`, so you can't grep the binaries; edit the builder, regenerate, verify the regenerated text.

## Assessment design
- [materials own the failure](feedback_materials_own_the_failure.md) — someone stuck with the run sheet + lab pack in front of them means a **pack defect** or **insufficient detail**, never student error. Mechanical path only; struggling to *decide* something is the assessment working.
- [worksheet over template](feedback_worksheet_over_template.md) — everything the student produces is captured in the assessment **worksheet**; a separate fillable template only where a UoC requirement explicitly demands one (quote it). Exemplars follow templates.
- [mark the UoC intent, not the invented settings](feedback_mark_uoc_intent_not_invented_settings.md) — we invent specific values so a task is doable; they are context. Per setting ask "if this were wrong, would the item still be evidenced?" Every element carries `Evidences:` **and** `Satisfactory when`. Companion rule: scaffold the process, never the finding.
- [assessments freeze per delivery cycle](feedback_finalised_assessments_change_control.md) — institutional review PASS freezes instruments **for that delivery** (warn before touching); **delivering spends the approval** → they reopen for a feedback-driven improvement pass, edited **in place in the generators**; the next human review re-freezes for the next intake.
