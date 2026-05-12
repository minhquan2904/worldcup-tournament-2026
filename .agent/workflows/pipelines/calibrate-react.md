---
description: Calibrate React knowledge - scan source code, compare vs conventions, and deep-learn UI architecture patterns.
version: 4.0
---

# /calibrate-knowledge --react

$ARGUMENTS

## Task
Hiệu chỉnh base_knowledge/ cho khớp React/Zalo Mini App source.

| Phase | Flag | Steps |
|-------|------|-------|
| SCAN | --scan | 0→1→2→3→[Gate]→4 |
| LEARN | --learn | 0→5 |

> !auto-detect default — PHẢI có --scan hoặc --learn
> React LEARN đủ nhẹ 1 conversation — !cần --group

## Syntax
```
/calibrate-knowledge --react --scan
/calibrate-knowledge --react --learn
/calibrate-knowledge --react --map
```

## Learn Sub-Skills (8 total)
| Sub-Skill | Output |
|-----------|--------|
| learn-react-architecture | knowledge_react_architecture.md |
| learn-react-component | knowledge_react_component.md |
| learn-react-state-service | knowledge_react_state_service.md |
| learn-react-shared-component | knowledge_react_shared_component.md |
| learn-react-hook-helper | knowledge_react_hook_helper.md |
| learn-react-util | knowledge_react_util.md |
| learn-zmp-sdk | knowledge_zmp_sdk.md |
| learn-error-debug | knowledge_error_debug.md |

## Steps

### Step 0 — Prerequisite Gate
base_knowledge/ exists? system_overview.md exists?
Case A (exists, !--map) → skip
Case B (!exists or --map) → delegate /map-structures → END conversation

### Step 1 — Scan (delegate react-scan workflow, READ-ONLY)
Apply PRJ-07-react-scan-rule.md:
- Scan scope: src/pages/, src/components/, src/hooks/, src/stores/, src/services/, src/utils/, src/types/
- Check: function components, TypeScript props, hook rules, Jotai atoms, Tailwind classes, ZMP SDK usage

### Step 2 — Compare vs base_knowledge
Scope: common_rules/PRJ-*, learn-react-*/SKILL.md
Cross-check: learn-react-*/SKILL.md Guardrails vs project patterns:
- Function components → BẮT BUỘC (!class components)
- Jotai atoms → BẮT BUỘC (!Redux, !Context API for global state)
- useState → CHO PHÉP (local state only)
- useEffect cleanup → BẮT BUỘC
- react-router-dom MemoryRouter → BẮT BUỘC (!BrowserRouter, !HashRouter, !ZMPRouter)
- Tailwind CSS → BẮT BUỘC (!CSS Modules, !styled-components)
- Dark mode via [zaui-theme="dark"] → BẮT BUỘC

### Step 3 — Drift Report (2 tables: conventions + learn-react-* guardrails)
### [Gate] — User approve/reject
### Step 4 — Apply updates to base_knowledge/ + learn-react-* guardrails

### Step 5 — Learn (--learn flag, skip 1-4)
Run all 8 sub-skills in order. Smart detect: !exists→GENERATE, exists→COMPARE+update

## Guardrails
- MUST cite actual component names + file paths
- !guess, !placeholders
- Knowledge files MUST be self-contained
