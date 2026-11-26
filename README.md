# courseware-factory
Course-agnostic machinery for building VET courseware. Step-by-step processes with validated gates take units of competency through to assessments, mappings, teaching decks and delivery plans. Course repos are cloned into courses/.

## Setup

```bash
git clone https://github.com/Digital-Initiatives-Kangan-Institute/courseware-factory.git
cd courseware-factory/courses
git clone <course-repo-url>
```

Launch Claude from the `courseware-factory` root, never from inside a course.

## Layout

```
courseware-factory/
├── .claude/        settings, hooks, memory, rules, agents, skills
├── docs/           factory-level docs
├── factory/        the engine — common/, process_NN_<name>/step_PNN_<name>/, tests/
├── institutions/   institution packs (branding, templates)
├── scaffold/       starter files for a new course repo
└── courses/        course repos, cloned here (gitignored)
```
