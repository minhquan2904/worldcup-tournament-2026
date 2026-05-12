---
description: Calibrate base_knowledge - 2 phases (SCAN or LEARN) via React pipeline.
---

## Dispatch
Follow .agent/workflows/pipelines/calibrate-knowledge.md

## Phases
- SCAN (default): scan conventions -> compare -> drift report -> update
- LEARN (--learn): deep-learn architecture -> generate/update knowledge files

## Tech Routing
| Flag | Pipeline |
|------|----------|
| --react | calibrate-react.md |

> Default: --react (single-stack project)

## Onboarding
```
1. /calibrate-knowledge --react --map
2. /calibrate-knowledge --react --scan
3. /calibrate-knowledge --react --learn
4. /feature-pipeline <name>
```
