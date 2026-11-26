# CLAUDE.md — courseware-factory

Course-agnostic machinery for building VET courseware. The factory holds process and tooling only;
each course lives in its own repo, cloned into `courses/` and gitignored here.

**Launch Claude from this folder** — settings, agents, hooks and memory load only from the launch
folder. A course's own `CLAUDE.md` loads when you work on files inside it.

## Read first
- [docs/INDEX.md](docs/INDEX.md) — the catalogue of factory docs. Read it every session; load the
  relevant doc before related work.

## Layout
| Path | Holds |
|---|---|
| `.claude/` | settings, hooks, memory (principles only), rules, agents, skills |
| `docs/` | factory-level docs |
| `factory/` | the engine: `common/`, `process_NN_<name>/step_PNN_<name>/`, `tests/` |
| `institutions/` | institution packs (branding, templates) |
| `scaffold/` | starter files for a new course repo |
| `courses/` | course repos (gitignored) |

## Status
Being populated from the pilot (`diploma-cloud-cyber-umbrella`), one piece at a time: check it,
copy it here, test it.
