---
description: CR pipeline — change request analysis and implementation for React/Zalo Mini App.
version: 4.0
---

# /cr-pipeline <name>

$ARGUMENTS

## Syntax
```
/cr-pipeline <name>
/cr-pipeline <name> --frontend
```

## Pipeline Flow
```
  1.cr-analyze ──▸ 2.srs ──▸ 3.specs ──GATE──▸
  --frontend: 4.design-fe ──▸ 5.tasks-fe ──GATE──▸ 6.react-gen ──▸ 7.review-fe
  ──▸ 8.archive
```

> Default: --frontend (React-only project)

## Steps
| # | Step | Output |
|---|------|--------|
| 1 | cr-analyze | metadata.yaml + current-code-logic.md + compare-logic.md + proposal.md |
| 2 | srs | srs.md |
| 3 | specs | specs/**/*.md |
| 4 | design-fe | design-fe.md |
| 5 | tasks-fe | tasks-fe.md |
| 6 | react-gen | .tsx, .ts source (via apply skill) |
| 7 | review-fe | todo-uncover-fe.md + delta-spec-fe.md |
| 8 | archive | changelog.md + updated compare-logic.md + archived |

## Smart Resume
```
--frontend: !design-fe.md → 4 | !tasks-fe.md → 5 | incomplete → 6 | !todo-uncover-fe.md → 7
```

## Guardrails
- cr-analyze MUST complete before srs
- MUST follow pipeline order strictly
- Each GATE = stop + user approval
- !skip steps without existing output
- CR variant: archive also updates compare-logic.md + generates changelog.md
