# Consolidation decisions — format standard

The standard for `<cluster>/consolidation-decisions.md`, the log kept alongside the deliverable
`consolidated_uoc.md`. First needed at execution item 4, when phase 2 starts making grouping calls.

## What it is for

Three jobs, in the order they arrive:

1. **Carries phase 2's reasoning into phase 3.** The grouping is judgement; the negotiation is about
   that judgement. Written down, the reasoning survives a session ending between them.
2. **Answers "what were they thinking" later.** Months on, someone looks at a group and wants to know
   why those items are together. This is where that lives.
3. **Records the acceptance discussion** — what the operator attached to their agreement, and anything
   they wanted revisited later.

It is a **log of the discussion**, not a summary of the outcome. The outcome is the deliverable.

## Not validated, by design

Nothing here is checked by the gate — not its content, and not its existence.

This is a **traceability tool**, not a deliverable. Its value is in being useful to a person reading it
later, and no script can check the thing that makes it useful: whether it records what was actually
discussed rather than a plausible reconstruction.

**Existence is not checked either, and that is the more important half.** Consider when such a check
would fire: at the gate, after every decision has already been made. A missing log cannot be filled in
at that point — reconstructing the entries means writing what someone *probably* thought, which is the
one thing this document must never contain. So the only way to clear that failure would be to
fabricate, and a gate whose only available remedy is fabrication is worse than no gate at all.

The opportunity to keep this log passes with each decision as it is made. It is not something a gate
can recover, and pretending otherwise would corrupt the record it is meant to protect.

The gate reads the **deliverable's** status banner to know the consolidation was accepted. That is a
fact about the artefact being gated. This log says what the discussion was; it does not decide whether
the step is done.

So the quality of this document rests on the discipline above, not on a validator. That is the honest
trade — and it is why "record only what was discussed" is stated as the one rule rather than as advice.

## The one rule

**Record only what was actually discussed and decided.**

This is the discipline that keeps the log worth reading. Concretely:

- An entry exists because a decision was made. Not because a group exists and looks like it deserves
  a paragraph.
- The rationale is **the reason that was given**. If nobody stated one, say so — do not construct a
  plausible reason after the fact, and do not improve on a thin one.
- No filling gaps for completeness. A log with entries for four of eleven groups is correct if four
  decisions were discussed.
- Never write something as agreed that was not explicitly agreed. Something still open is
  `[TBD — needs discussion: <what is open>]`, not a decision.
- Two decisions stay two entries. Do not summarise up into one tidy narrative.

Brevity is part of accuracy: the shortest entry that captures what was decided and why is the best
entry. Padding is where invention gets in.

## Never fill it in afterwards

**An entry is written at the moment the decision is made. That is the only time it can be true.**

If a decision was made and not logged, the entry is gone. It cannot be recovered later, because what
would be written is not the reasoning — it is a reconstruction of what someone *probably* thought,
assembled from the outcome. The outcome is already in the deliverable; the whole point of this document
is the part that is not recoverable from it.

**Back-filling does not produce a weaker log. It produces an invalid one.** The document's entire value
rests on a reader being able to trust that an entry says what was actually thought at the time. One
reconstructed entry destroys that for every entry, because nothing on the page distinguishes the
contemporaneous ones from the invented ones. A log that is 90% genuine is not 90% useful — it is
unusable, because the reader cannot tell which 90%.

Nothing catches this. No gate, no reviewer, no later check — see below. It rests entirely on whoever is
writing.

**When you notice a gap, leave it.** A missing entry is an honest absence and costs only that one
decision's reasoning. If the gap matters, say so plainly rather than filling it:

```markdown
### D-11 — 2026-09-10 — [not logged at the time]

The regrouping of the DR items was decided in discussion and not recorded. The reasoning is not
reconstructed here.
```

That entry is worth writing because it is true. An invented one never is.

## The log records; it does not bind

**Expect the discussion to loop, and expect earlier decisions to be reopened.** A grouping that made
sense in isolation often stops making sense once three more are on the page; understanding moves as the
conversation moves. Coming back to something decided ten minutes ago is the negotiation working, not a
failure of the earlier call — and it costs nothing but a new entry.

So an entry records **what was decided at a moment**. It is never a commitment, and being written down
settles nothing.

The failure this guards against is specific: an entry being quoted back at the operator as a reason not
to change something. That is the factory's standing rule — *documentation is never grounds for
declining an idea* (see the working-discipline section of `CLAUDE.md`) — arriving inside a single
session. A log that makes revision cheap and legible is doing its job; a log used to argue against a
revision is being read exactly backwards.

Practically, for whoever is running phase 3: when the operator reopens something, log the new decision
and move on. Do not defend the old entry, do not ask them to justify reopening it, and do not preface
the change with what was previously agreed.

## Shape

**Reverse-chronological — newest at the top.** Read top-down for the current position, bottom-up for how
it got there.

**Nothing is ever edited or deleted.** A decision that changes gets a **new entry at the top**; the
original stays exactly as written. That is what makes the log trustworthy — an entry cannot be quietly
improved later.

**Entry IDs are stable and never reused** (`D-01`, `D-02`, …), numbered in the order written, so a
revision can name what it supersedes. Without that, a reader coming top-down finds two entries saying
different things about the same group and has to reconstruct from dates which one is live.

## Skeleton

```markdown
# <CLUSTER> — Consolidation decisions

> **Status:** <DRAFT — under negotiation | ACCEPTED <date> by <who>>

Log for `consolidated_uoc.md`. Newest first; nothing is edited or removed. A decision that changes
gets a new entry that names the one it supersedes.

## Decisions

### D-NN — <date> — <what was decided, in a few words>

Decided by: <LLM (phase 2) | discussion (phase 3)>
Supersedes: <D-NN, or omit the line entirely>

<What was decided, and the reason that was given for it. A sentence or three.>

Considered and set aside: <the alternative and why — only where an alternative was genuinely weighed>
```

## An entry

| Part | |
|---|---|
| `### D-NN` | stable ID, never reused |
| date | ISO `YYYY-MM-DD`, the day the decision was made |
| subject | what was decided, in a few words — enough to scan the log without opening entries |
| `Decided by:` | `LLM (phase 2)` or `discussion (phase 3)` — see below |
| `Supersedes:` | present only on a revision; names the entry it replaces |
| body | the decision and the reason **given** for it |
| `Considered and set aside:` | only where an alternative was genuinely weighed. Omit it rather than inventing a rejected option — this is exactly the field that invites invention |

### Who decided, and why it matters

The log is written across two phases by two different authorities, and an entry has to say which:

| Value | Means |
|---|---|
| `LLM (phase 2)` | made while drafting, on the LLM's own judgement. **Proposed, not ratified** — no human has seen it yet. |
| `discussion (phase 3)` | arrived at with the operator. **Agreed.** |

The distinction is not bookkeeping. Phase 2's entries are one side of a conversation that has not
happened yet; reading the log later, that is the difference between "this is why we did it" and "this
is what the model thought before anyone checked".

**The acceptance entry ratifies every surviving phase-2 entry.** A phase-2 grouping that the operator
reads and leaves alone is agreed by the acceptance, so there is no need to re-log it as confirmed —
that would bury the entries that record a real change under a wall of "still fine". Only a decision
that actually moved in phase 3 earns a new entry.

Worked example:

```markdown
### D-14 — 2026-09-12 — Group 3 split into design and review

Decided by: discussion (phase 3)
Supersedes: D-06

Splitting because the review criteria cannot be evidenced by the same artefact as the design work —
one is a document, the other is a meeting. Raised by the operator.

### D-06 — 2026-09-09 — ICTCLD501 PE 2 grouped with the DR items

Decided by: LLM (phase 2)

Grouped with the disaster-recovery items because a single DR plan could evidence all four.

Considered and set aside: grouping it with the design items, which would have matched the wording
more closely but split the evidence across two artefacts.
```

## The acceptance entry

Phase 3 ends with one. The **gate** reads the deliverable's status banner, not this — but the banner
records only that acceptance happened, and this records what was said around it:

```markdown
### D-NN — <date> — Consolidation accepted

Decided by: discussion (phase 3)

Accepted by <who>. <Anything they attached to the acceptance — a reservation, a follow-up, a group
they want revisited after the assessment plan exists.>
```

The status banner at the top of the document changes to `ACCEPTED <date> by <who>` at the same time.
Until then it stays `DRAFT — under negotiation`, and the consolidation is a proposal.

## What does not belong here

- The items themselves, or their text. They live in `consolidated_uoc.md`; the log refers to them by
  reference (`[ICTCLD501 PE 2]`).
- A restatement of the grouping. The deliverable already says what is grouped with what — the log says
  *why*, and only where a why was actually given.
- Anything the validator can determine. Completeness is the gate's job; this document is for the
  judgement a script cannot make.
