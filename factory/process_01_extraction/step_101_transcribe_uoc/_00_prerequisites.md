# Step 101 — Prerequisites

**Entry condition.** What must hold before the step starts. The step's *exit* condition is a different
thing entirely — see [`_99_gate.md`](_99_gate.md).

## 1. There is no previous gate

This is the first step of the first process, so the usual "the previous gate has passed" half is empty.
Nothing upstream guarantees anything here; everything the step needs is supplied from outside the
factory.

## 2. The source documents are in place

| # | Required | Where |
|---|---|---|
| P1 | The official unit-of-competency `.docx` for every unit in the cluster | `<cluster>/units_of_competency/original/` |
| P2 | Each file named for its unit code and release | `<UNIT>_Complete_R<N>.docx` — the release matters; a unit reissued at a new release is a different document |

**Nothing else.** No decision, no operator input, no course context. The step is a faithful lift: it
reads the documents it is given and writes what they say.

The units themselves are downloaded from training.gov.au, which is outside this process. If a `.docx`
is missing, the answer is to fetch it — not to transcribe what is there and note a gap.

→ Next: [`_01_execution.md`](_01_execution.md)
