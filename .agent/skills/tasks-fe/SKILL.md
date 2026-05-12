---
name: tasks-fe
description: Generate frontend implementation tasks ordered by dependency (Types → Service → Store → Routing → Component).
arguments: ["${change_name}"]
allowed-tools: [Read, Write, Grep, Glob, Bash]
context: inline
version: 4.0
---

# Tasks Frontend

Output: tasks-fe.md in openspec/changes/<name>/
Input: Change name. srs.md + specs/ + design-fe.md must exist.

## §1 Verify
srs.md + design-fe.md + specs/ exist

## §2 Read Dependencies
srs.md → business requirements | specs/ → UI requirements | design-fe.md → components, state, services

## §3 Load Context
artifact_context_modular.yml → section tasks-fe

## §4 Generate tasks-fe.md — Structured NL Format
Output format: **Structured NL** (AI-optimized)

Layer order + task numbering:
```
## L{N}: Layer Name
- [ ] **T{N}.{M}: title** → `file_path` [NEW]
  purpose | props/params | dependencies
```

L0=Types/Interfaces → L1=API Services → L2=Jotai Atoms/Store → L3=Custom Hooks → L4=Routing → L5=Page Components → L6=Shared Components → L7=Styling

Each task: 1-line title + file path [NEW] + 1-2 lines properties
- Component props inline: `title(string,required), onClick(()=>void), className?(string)`
- Atom definition inline: `featureListAtom: atom<Feature[]>([])`
- Hook returns inline: `{ data, loading, error, refresh }`
- !verbose paragraphs

## §5 Verify Traceability
- ✓ every design component → task
- ✓ no orphan tasks

## Guardrails
- MUST follow dependency layer order strictly (Types → API → State → Hooks → UI)
- State: Jotai atoms for global state, useState for local
- Routing: `MemoryRouter + Routes + Route` from `react-router-dom` | route paths từ `src/constants/routes.ts` | navigation via `useNavigate()`
- Components: function components, TypeScript props
- !Angular patterns (NgModule, inject(), signal(), GeneralService, FormGroup)
