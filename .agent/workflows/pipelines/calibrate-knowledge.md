---
description: Calibrate base_knowledge - router that delegates to React calibration pipeline.
version: 4.0
---

# /calibrate-knowledge

$ARGUMENTS

## Router Logic
--react → delegate calibrate-react.md (all sub-flags)
no tech flag → default --react (single-stack project)

## Syntax
```
/calibrate-knowledge --react --scan|--learn [--map]
```

## Quick Ref

| Tech | Pipeline | Phases | Scale |
|------|----------|--------|-------|
| React | calibrate-react.md | react-scan→compare→apply | 8 sub-skills, 1 conversation |

## Typical Session Order
```
1. /calibrate-knowledge --react --map                       -> map-structures → END
2. /calibrate-knowledge --react --scan                      -> SCAN React conventions
3. /calibrate-knowledge --react --learn                     -> LEARN React patterns (1 conversation đủ)
```

## Guardrails
- !auto-detect default — PHẢI có --scan hoặc --learn
- !run both phases in 1 command
