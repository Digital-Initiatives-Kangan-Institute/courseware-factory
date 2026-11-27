# Planning guide — running the conversation

How to get from an accepted consolidated UoC to an agreed assessment plan. The mechanical layers either
side — the coverage check, the SR cross-check — are scripts; this is the part no script can do.

Read with [`_02_assessment-plan-format.md`](_02_assessment-plan-format.md), which says what the document
you are filling looks like.

## The one thing to understand first

**The operator decides the frame; you draft everything downstream of it.**

This is the opposite way round from step 102, where the LLM proposed groupings and the operator reacted.
Here the first three decisions — the integration approach, the scenario vehicle, the AT roster — cannot
be drafted first in any useful way. Whether this cluster has a group assessment, whether there is an
observation, what world it runs in: none of that is derivable from the units. Proposing an AT roster
before asking is guessing, and a plausible guess is worse than a question because it anchors the
conversation on something arbitrary.

Once those are settled, the rest **is** derivable and largely tedious — allocating 106 items across
three ATs, working out what the scenario must supply for each. That is your half.

## How to run it

**Offer options, do not present an answer.** Where a decision has real alternatives, name them with the
consequence of each, then let the operator choose:

> Two ways the units can meet without colliding. Either they are evidenced on **different jobs** — 504
> owns the design and the deploy, 401 owns the team write — or they are evidenced on the **same job at
> different depths**. The first keeps the group work contained to one AT; the second spreads it and
> makes individual attribution harder.

**Ask one thing at a time.** These are decisions the operator is making, often out loud. A list of six
questions gets one answered and five lost.

**When their experience contradicts your reasoning, they are probably right.** The operator has taught
this; you have read the units. Say what you think once, then take their answer.

**Log the calls as they are made**, per
[`_04_plan-decisions-format.md`](_04_plan-decisions-format.md). In the moment or not at all.

## The frame — what to elicit

Four conversations, in this order. Each maps to a part of §1 or §3.

### 1 · The shape of the engagement

*What is the thread that makes this one engagement rather than three tasks in the same setting?*

Usually: an AT produces something, it is **signed off**, and the next AT builds that. So ask what the
natural sequence of work is for this cluster's subject matter — design then build, plan then implement,
assess then improve.

Then find the approval moment in the units themselves. Search the consolidated UoC for criteria about
obtaining sign-off, approval, or authorisation before proceeding; those are the ones that make the
thread UoC-faithful rather than merely tidy. Bring the operator the candidates you found, with their
references.

### 2 · Individual or group

*Is anything here genuinely divisible?*

Group assessment needs a job that can be split without making individual attribution impossible. Ask
which part of the work is naturally collaborative, and note that whatever is group-assessed still needs
per-student evidence somewhere.

If the units include a teamwork unit, it usually owns the group job — the technical units keep the
individual ones. Say so as an observation, not a conclusion.

### 3 · The scenario vehicle

*What world does this cluster assess on, and what does the student inherit versus build?*

The provided-versus-authored boundary is the part worth pushing on, because it decides every `SR-*`
later. A student building from nothing is a different assessment from one improving a system they were
handed.

Where the cluster shares a scenario with others, the constraint is inherited — ask what is already
fixed before proposing anything.

### 4 · Knowledge evidence

*Where does KE ride?*

Two positions, and the operator picks: contextual (students reason about their own design and build
choices) or abstract recall (a question set). Every pilot cluster took the first. Then the practical half:
which section of which workbook holds it, and whether any is verbal.

## Then draft

With the frame agreed, the rest is yours to produce and theirs to check.

**Allocate UoC coverage per AT.** The groups in `consolidated_uoc.md` are already "one artefact could
evidence these", so start from them: a group maps to an AT, or splits across two. Work from the
consolidated document item by item so nothing is dropped — the coverage check will catch a gap, but
finding it now is cheaper than finding it at the gate.

**Derive the scenario requirements.** For each AT ask: *what must the world supply for this to be
attemptable at all?* The format standard's "what an `SR-*` is NOT" section is the one to re-read before
writing them — the common error is writing an `SR-*` for something the **student** produces, which
becomes a false gap at the scenario cross-check two steps later.

**Write §5's coverage verification** as the human-readable rollup, and §7's worklist.

## Marking what is not settled

Use `[TBD — needs discussion: <what is open>]` for anything you have not been told and have not been
able to derive. It is how you make your own uncertainty visible instead of choosing quietly and
presenting the choice as agreed.

Do not use it for something you simply have not asked yet — ask.

**The gate requires none to remain**, so every TBD is either resolved in conversation or becomes a
consciously deferred item in §8, worded as a deferral rather than a marker.
