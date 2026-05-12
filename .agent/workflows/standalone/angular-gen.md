---
description: Generate React/TypeScript source code (Types, Services, Hooks, Atoms, Components, Routes) following scanned conventions.
version: 4.0
---

# /react-gen

$ARGUMENTS

## Mode Detection
| Trigger | Mode | Input |
|---------|------|-------|
| `from change <name>` | Pipeline | tasks.md (FE tasks) + design.md |
| `from swagger`/`Jira`/`confluence`/direct | Standalone | Parse directly |

## Steps

0. **Execution Planning**
   - Pipeline: tasks.md → FE tasks + design.md → Frontend Design
   - Standalone (raw input): auto-call init→design→tasks first
   - ⛔ Load artifact_context_modular.yml → section apply → HALT if missing
   - 🛑 Approval Gate

1. **Types** → src/types/{feature}.ts — TypeScript interfaces/types
2. **Services** → src/services/{feature}.ts — API service functions
3. **Atoms** → src/stores/{feature}.ts — Jotai atom definitions
4. **Hooks** → src/hooks/use{Feature}.ts — Custom hooks
5. **Pages** → src/pages/{feature}/index.tsx — Page components
6. **Components** → src/components/{feature}/ — Shared components
7. **Routes** → Update routing config — ZMPRouter routes
8. **Self-Scan** → PRJ-07-react-scan-rule.md → 0 CRITICAL, 0 WARNING required. Pipeline: mark [x] in tasks.md

## Usage
```
/react-gen from change add-product-listing
/react-gen page product-detail
/react-gen component product-card
```
