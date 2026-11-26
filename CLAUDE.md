# CLAUDE.md — courseware-factory

Course-agnostic machinery for building VET courseware. The factory holds process and tooling only;
each course lives in its own repo, cloned into `courses/` and gitignored here.

**Launch Claude from this folder** — settings, agents, hooks and memory load only from the launch
folder. A course's own `CLAUDE.md` loads when you work on files inside it.

## Read first
- [docs/big-picture.md](docs/big-picture.md) — the whole factory in one page. Thirty seconds.
- [docs/INDEX.md](docs/INDEX.md) — the catalogue of factory docs. Read it every session; load the
  relevant doc before related work.
- [docs/doco-structure.md](docs/doco-structure.md) — the doc surfaces and the `CLAUDE.md`⇄`MEMORY` split.

## Layout
| Path | Holds |
|---|---|
| `.claude/` | settings, hooks, memory (principles only), rules, agents, skills |
| `docs/` | factory-level docs |
| `factory/` | the engine: `common/`, `process_NN_<name>/step_PNN_<name>/`, `tests/` |
| `institutions/` | institution packs (branding, templates) |
| `scaffold/` | starter files for a new course repo |
| `courses/` | course repos (gitignored) |

## Working discipline — assumptions & documentation

**Everything we write here is the current working approach, not law.** Docs, standards, conventions and
memory record what we do *now*, open to change when a better path shows up — write *"the current
approach"*, not *"never"* / *"must"* / *"invariant"*. State firmly only a constraint we have no
capability to change (e.g. the Learner Lab refusing IAM creation). Full principle:
[docs/doco-structure.md](docs/doco-structure.md).

Never record anything as *decided / agreed / canonical* unless it was actively discussed **and**
explicitly approved. Flag anything not yet agreed with `[TBD — needs discussion: <what is open>]`
rather than writing it as settled. A thing tried **once** is not a convention — say it is being
trialled, name where, and don't propagate it.

**Documentation is never grounds for declining an idea.** This is the harm the rule above exists to
prevent: Tim proposes improvements to how the work is done, and locking language written today becomes
a later session **quoting the docs back at him** — *"it is written that we do it this way"* — as a
reason not to consider his idea. What is written records how we **currently** understand the job and
**currently** approach it; new understanding, methods and tooling are always possible. When a proposal
touches something already written down, treat the doc as **context, never as an objection**: say what
it says and why, then keep weighing the idea on its merits.

**No check, constraint or finding is ever decisive or a dead end.** Never frame a test, lookup or
investigation as settling a question or blocking the work — *"this decides it"*, *"this means we
can't proceed"*. A check yields **one input**, weighed with everything else. At most it leans us
toward an option or rules out one particular way of doing a thing; the goal stays reachable and there
is room to be creative about how. The framing is always: *we'll check this, and it informs how we
proceed.*

- Capture only what was discussed and agreed; don't extrapolate a principle into unraised specifics.
- Flag open questions explicitly with `[TBD — …]` so a later session picks them up deliberately.
- Distinguish archived/historical material from in-conversation decisions.
- Smaller is better — three faithfully-captured points beat ten padded ones.
- Self-correct — if you catch yourself writing beyond what was discussed, remove it or mark it `[TBD]`.
- Docs describe the **current state only**; what-was lives in git history, not in prose.

## Git safety — destructive operations require explicit approval

Never run a destructive git operation without explicit, in-conversation approval for that specific
action — regardless of any settings allowlist or prior approval. Destructive includes: force push,
hard reset, discarding uncommitted changes, `git clean -f`, force-deleting branches, history rewrites
(`rebase`, `amend` on pushed commits, `filter-branch`/`filter-repo`), dropping stashes, deleting tags,
and any `--no-verify` / `--no-gpg-sign` bypass. Force-pushing a protected branch (`main`/`master`/
`release/*`) must be refused outright. When unsure whether something can lose work or rewrite history,
treat it as destructive and ask.

**Non-destructive git too (this project's convention):** do **not** run state-changing git — in *any*
repo (the factory or any course repo) — on your own. Propose the exact command(s) + rationale and wait
for explicit approval; "go ahead" approves *that* operation only, not a standing licence. Read-only
git (`status`, `diff`, `log`, `show`, …) is always fine.

## Status
Being populated from the pilot (`diploma-cloud-cyber-umbrella`), one piece at a time: check it,
copy it here, test it.
