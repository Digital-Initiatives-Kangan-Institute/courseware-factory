# courses/

Course repos are cloned here. Each is its own git repository with its own remote; the factory
gitignores everything in this folder except this README.

```bash
cd courses
git clone <course-repo-url>
```

Launch Claude from the factory root, not from a course folder — settings, agents, hooks and memory
load only from the launch folder.

Each course repo carries a `course.toml` that tells the factory where its parts are.
`[TBD — needs discussion: course.toml fields]`
