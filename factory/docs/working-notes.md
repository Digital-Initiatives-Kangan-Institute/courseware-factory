# Working notes — temporary

> **This document is scaffolding, not part of the factory.** It holds ideas and decisions-to-make that
> come up while the factory is being built, so they are not lost and do not derail the work in front of
> us. **Delete it when the factory is feature-complete** — anything still here at that point either
> became a real document or was not worth doing.

Add a note when something surfaces that matters but is not this task. Keep each one short enough to be
picked up cold: what it is, why it matters, and what a decision would need to cover.

---

## 1 · The `[TBD]` marker needs a home in the factory

**What it is.** `[TBD — needs discussion: <what is open>]` marks something **nobody has decided yet**.
It is how an LLM makes its own uncertainty visible instead of quietly choosing and presenting the choice
as settled. `CLAUDE.md` asks for it; no factory document defines it, and no gate checks for it.

**Why it matters.** It is the difference between a document that is honest about what is unresolved and
one that reads as agreed throughout. It also gives gates something checkable: **zero TBD markers** is a
completeness condition a script can enforce, and a stronger one than "no empty fields" — an empty field
is obvious, an unstated assumption is not.

**What a standard would need to cover.**
- The marker's exact form, and that it means *undecided* — not *deferred*, not *low priority*.
- That an LLM is expected to use it rather than pick and move on.
- Its relationship to a deliberately deferred item (a plan's "open questions" section holds things
  consciously postponed, which is a different state and should read differently).
- That a step's gate may require none to remain — and whether that check is one shared script every
  planning step calls, rather than one each step owns.
