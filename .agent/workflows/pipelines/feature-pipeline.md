---
description: Feature pipeline — end-to-end feature generation for React/Zalo Mini App.
version: 4.0
---

# /feature-pipeline <name>

$ARGUMENTS

## Syntax
```
/feature-pipeline <name>
/feature-pipeline <name> --frontend
```

## Pipeline Flow
```
  1.preprocess ──▸ 2.srs ──▸ 3.specs ──GATE──▸
  --frontend: 4.design-fe ──GATE──▸ 5.tasks-fe ──GATE──▸ 6.react-gen ──▸ 7.review-fe
  ──▸ 8.archive
```

> Default: --frontend (React-only project, no backend pipeline)

## Steps

| # | Step | Skill/Workflow | Output | Flag | Gate? |
|---|------|------|--------|------|:-----:|
| 1 | preprocess | SKILL preprocess | pre_process.md | always | |
| 2 | srs | SKILL srs | srs.md | always | |
| 3 | specs | SKILL specs | specs/**/*.md | always | ✅ |
| 4 | design-fe | SKILL design-fe | design-fe.md | --frontend | ✅ |
| 5 | tasks-fe | SKILL tasks-fe | tasks-fe.md | --frontend | ✅ |
| 6 | react-gen | SKILL apply | .tsx, .ts source | --frontend | |
| 7 | review-fe | SKILL review-fe | todo-uncover-fe.md | --frontend | |
| 8 | archive | SKILL archive | archived change | always | |

## Smart Resume
Detect existing artifacts → skip completed steps:
```
preprocess: !pre_process.md → 1
srs: !srs.md → 2
specs: !specs/ → 3
design-fe: !design-fe.md → 4
tasks-fe: !tasks-fe.md → 5
react-gen: tasks-fe exists + incomplete → 6
review-fe: !todo-uncover-fe.md → 7
all done → 8
```

## Gate Rules
- Specs Gate: user reviews spec scenarios before design
- Design Gate: user reviews component tree + state architecture before tasks
- Tasks Gate: user reviews task list before code generation

## Guardrails
- MUST follow pipeline order strictly
- Each GATE = stop + user approval before next step
- Smart resume: detect + skip completed steps
- !skip steps without existing output
- !run backend steps — React-only project
