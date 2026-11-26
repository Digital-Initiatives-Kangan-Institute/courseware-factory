---
name: audit-generated-docs-via-py-builders
description: "When sweeping content for a cross-cutting change (rename, rebrand, region/lab change, etc.), the assessment INSTRUMENTS (.docx) and teaching DECKS (.pptx) are GENERATED from .py builders — grep the builders, never just .md/.yaml; you cannot grep the binaries."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
---

**A text grep over `.md`/`.yaml` MISSES most of the deliverables.** The student/assessor assessment
instruments are `.docx` and the teaching decks are `.pptx` — both **generated** from Python builders:
the course's own generators (in the course repo) and the factory's shared engine. The source text lives
in the `.py` builders (sometimes a shared content module imported across builders — e.g. a student
instrument importing its assessor builder as its single source of truth).

**Why:** in the pilot course, during the region-substitution rollout (2026-06-30), the first audit grepped only `.md`/`.yaml`
and reported "done," but the CL2 AT2 `.docx` instruments + a CL1 teaching deck still said the old thing
— invisible because they're generated binaries. Caught only on a completeness sweep of the `.py`.

**How to audit a cross-cutting content change properly:**
1. `grep` the **`.py` builders** — the course's generators and the factory engine (you cannot grep
   `.docx`/`.pptx` directly).
2. Separate the copy that should change from copy that legitimately keeps the old value. In the pilot's
   region change, design-layer copy (solution designs, DR plans) kept real regions; only deploy-layer copy
   (lab/deploy instructions) changed.
3. Edit the builder (or its shared content module), then **regenerate** the artefact with the factory
   engine's Python environment (has `python-docx`/`python-pptx`) `[TBD — needs discussion: engine venv
   location — settles when the engine ports]`. Shared engine helpers live in `factory/common/helpers/`;
   course generators live in the course repo.
4. **Verify the regenerated binary** by extracting its text (python-docx / python-pptx) and asserting the
   new string is present and the stale one is gone — don't trust the source edit alone.
5. `git status` after regenerating: expect only the edited builders + their output artefacts; no phantoms
   (see [[feedback-verify-change-impact]]).

Related: [[one-course-agnostic-mechanism]].
