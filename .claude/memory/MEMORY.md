# Memory index

**LLM-only** durable memory for the **courseware-factory**: course-agnostic working principles —
how Claude operates here, for any course. Course working state lives in each course repo, not here.
"Principles, not state" — see [[memory-principles-not-state]]. One line per memory; topic files hold
the detail, loaded on demand.

> **Both-audience knowledge** (process, conventions, format standards) lives in **`docs/`**,
> catalogued in [docs/INDEX.md](../../docs/INDEX.md).

## Working principles
- [memory = principles not state](memory_principles_not_state.md) — record durable decisions/rationale (the non-derivable WHY); never repo-derivable ephemeral state (paths, commits, "what's built") — it goes stale on creation.
- [record current-state only](feedback_process_docs_current_only.md) — record things as they ARE, not how they used to be, in everything (docs, memory, status notes): current method only, no abandoned-path archaeology; git holds it.
- [current practice, not policy](feedback_current_practice_not_policy.md) — never write our own choices up as decided/locked/canonical/never/must; they are the current approach, open to evolution. **Documentation is never grounds for declining an idea.** A thing tried once is not a convention. Sole exception: a constraint we have no capability to change.
- [write deliverables at final confidence](feedback_deliverables_final_confidence.md) — author docs as if open dependencies were done; track the dependency in MEMORY, never as an in-text "draft pending X" hedge.
- [checks inform, they don't decide](feedback_checks_inform_not_decide.md) — never frame a check/lookup as "this decides it", and never as a dead end; it yields a data point weighed against everything else.
- [verify change impact](feedback_verify_change_impact.md) — before side-effecting changes (esp. running file-writing generators), verify where output lands + `git status` what got staged.
- [materials own the failure](feedback_materials_own_the_failure.md) — someone stuck with the run sheet + lab pack in front of them means a **pack defect** or **insufficient detail**, never student error. Mechanical path only; struggling to *decide* something is the assessment working.
