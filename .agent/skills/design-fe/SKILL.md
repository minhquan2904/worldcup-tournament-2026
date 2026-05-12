---
name: design-fe
description: Generate frontend technical design — React components, route mapping, Jotai state, API integration.
arguments: ["${change_name}"]
allowed-tools: [Read, Write, Grep, Glob, Bash]
context: inline
version: 4.0
---

# Design Frontend

Output: `design-fe.md` in openspec/changes/<name>/
Input: Change name. srs.md + proposal.md + specs/ must exist.

## §1 Verify
srs.md + proposal.md + specs/ exist

## §2 Read Dependencies
srs.md → business requirements | specs/ → UI behaviors

## §3 ⛔ MANDATORY COMPLIANCE (HALT if failed)
artifact_context_modular.yml → section design-fe → load required_rules (HALT) + context (soft)

## §4 Lock Frontend Profile
React pages, Screen types (List/Detail/Form/Modal/Sheet), Jotai atoms, API services

## §5 Generate design-fe.md — Structured NL Format
Output format: **Structured NL** (AI-optimized)

Sections: Context (2-3 lines) | Goals/Non-Goals (✅/❌) | Decisions (D1-D7) | Package Structure | Risks

Decision format:
```
### D{N}: title
Compact summary. Table for structured items (columns, fields, routes).
```

D1=Pages+Routing | D2=Component Tree | D3=State Management (Jotai) | D4=API Services | D5=Types/DTOs | D6=Shared Components | D7=Hooks

Rules:
- Tables for >3 items (page routes, form fields, atom definitions)
- !verbose prose | !repeat info from specs
- State: Jotai atoms for global state, useState for local UI state
- Hooks: custom hooks for reusable logic (useAuth, useFetch, etc.)
- Style: Tailwind CSS classes, dark mode via `[zaui-theme="dark"]`
- Routing: `MemoryRouter → Routes → Route` from `react-router-dom` (Zalo WebView: !BrowserRouter, !HashRouter). Keep `App + SnackbarProvider` from `zmp-ui` outside MemoryRouter. Route paths → `ROUTES` constants in `src/constants/routes.ts`
- !Angular patterns (NgModule, DI inject(), signal(), BehaviorSubject)

## Guardrails
- MUST apply PRJ-10-planning-feature-rule.md + PRJ-07-react-scan-rule.md
- MUST focus ONLY on frontend (React/Zalo Mini App)
