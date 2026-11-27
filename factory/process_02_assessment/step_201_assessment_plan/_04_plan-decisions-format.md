# Plan decisions — format standard

The standard for `<cluster>/assessments/assessment-plan-decisions.md`, the log kept alongside the
deliverable. First needed at execution item 3, when the first framing decision is made.

Structurally identical to
[step 102's decisions log](../../process_01_extraction/step_102_consolidate_uoc/_04_consolidation-decisions-format.md)
— same entry shape, same rules, same reasons. What differs is **what it holds**, because the assessment
plan explains itself in a way the consolidated UoC could not.

## What it is for

The plan's §1 already carries settled rationale: *"Part A before Part B because a DR plan is written for
a designed system."* That belongs there, where the next reader will look.

So this log holds what the plan does **not**:

1. **The alternatives weighed and set aside** — the AT roster that was considered and rejected, the
   grouping that would have worked but split the evidence. A plan states what was decided; only the log
   says what else was on the table and why it lost.
2. **The path** — what changed during the conversation and what prompted it. A decision reversed after
   the third AT came into view is the most useful thing a later reader can find, and the plan shows no
   trace of it.
3. **Who decided** — the operator's calls on the frame, versus what the LLM derived downstream of them.

## The one rule

**Record only what was actually discussed and decided.** The rationale is the reason that was *given*;
if none was, say so rather than constructing a plausible one. No entry because a section exists and
looks like it deserves a paragraph.

## Never fill it in afterwards

**An entry is written at the moment the decision is made. That is the only time it can be true.**

Back-filling does not produce a weaker log, it produces an invalid one: nothing on the page separates a
genuine entry from a reconstruction, so one invented entry costs the reader their trust in all of them.
Nothing checks this — no gate, no reviewer. It rests on whoever is writing.

When you notice a gap, leave it. A missing entry costs one decision's reasoning; an invented one costs
the document.

## The log records; it does not bind

Expect the conversation to loop. An AT roster that made sense before the coverage was allocated often
stops making sense after — that is the work happening, not a failure of the earlier call.

When the operator reopens something, log the new decision and move on. Do not defend the earlier entry,
do not ask them to justify reopening it, and do not preface the change with what was previously agreed.

## Shape

Reverse-chronological, newest at the top. Nothing is edited or deleted: a decision that changes gets a
**new entry**, and the original stays exactly as written. Entry IDs are stable and never reused, so a
revision can name what it supersedes.

## Skeleton

```markdown
# <CLUSTER> — Assessment plan decisions

Log for `assessment_plan.md`. Newest first; nothing is edited or removed. A decision that changes gets a
new entry that names the one it supersedes.

## Decisions

### D-NN — <date> — <what was decided, in a few words>

Decided by: <operator | LLM>
Supersedes: <D-NN, or omit the line entirely>

<What was decided, and the reason that was given for it.>

Considered and set aside: <the alternative and why — only where one was genuinely weighed>
```

## Who decided

| Value | Means |
|---|---|
| `operator` | a framing call — the engagement shape, group vs individual, the scenario vehicle, the KE position. **Agreed.** |
| `LLM` | derived downstream of the frame — a coverage allocation, an `SR-*`. **Proposed until the plan is accepted.** |

The split is not bookkeeping. Reading the log later, it is the difference between "this is what the
course owner wanted" and "this is what fell out of their decision, and nobody has looked at it closely".

**Accepting the plan ratifies every surviving LLM entry**, so there is no need to re-log an allocation
the operator read and left alone. Only a decision that actually moved earns a new entry.

## Not validated, by design

Nothing here is checked by the gate — not its content, not its existence. No script can check whether it
records what was discussed rather than a plausible reconstruction, and an existence check would fire
only after every decision had been made, when the sole way to clear a failure would be to fabricate
entries. A gate whose only available remedy is fabrication is worse than no gate.

The opportunity to keep this log passes with each decision as it is made. It is not something a gate can
recover.
