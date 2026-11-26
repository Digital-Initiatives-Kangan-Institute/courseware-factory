# Docs index

The factory-level docs. Each has a one-line description; read this index at the start of a session and
load the relevant doc before related work. Add a line here whenever you add a doc — an un-indexed
document is invisible. Course docs live in each course repo's own `docs/INDEX.md`.

## Meta
- [test-first-process.md](test-first-process.md) — the **test-first development process**: the fixed order (plan → tests → red → code), the `docs/test-plan.md` format, and the standardized visible `venvs/test/` location. Enforced by the `test-first` rule (`.claude/rules/`) and checked by the `test-plan-linter-python` skill.
- [test-plan-template.md](test-plan-template.md) — **copy-pastable** test-plan skeleton (seeded with two smoke cases): copy it to a unit's `docs/test-plan.md`, rename, and fill in.
