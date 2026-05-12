---
name: review-fe
description: Frontend post-implementation review — scan React code, generate tracking artifacts.
arguments: ["${change_name}"]
allowed-tools: [Read, Write, Grep, Glob]
context: inline
version: 4.0
---

# Review Frontend

Output: todo-uncover-fe.md + delta-spec-fe.md
Input: Change name. Frontend impl must be complete.

## §1 ⛔ MANDATORY COMPLIANCE
artifact_context_modular.yml → section review-fe → load required

## §2 Read Context
design-fe.md, specs/, tasks-fe.md, metadata.yaml

## §3 Scan Source Code
Identify all FE files from tasks-fe.md
Scan for: component patterns, hook usage, atom definitions, type safety, Tailwind classes

## §4 Generate Artifacts — Structured NL Format
Output format: **Structured NL** (AI-optimized, dev-reviewable)

### todo-uncover-fe.md
```
## 🔴 CRITICAL / 🟠 WARNING / 🟡 INFO / ✅ PASS
**C{N}: title** — [file#lines](link)
Design: ... | Actual: ... | Action: ...
```
Covers: TODOs, missing error handling, missing loading states, `any` types, missing useEffect cleanup, accessibility, missing key props in lists

### delta-spec-fe.md
```
### Δ{N}: title
Table: Aspect|Spec|Actual
Assessment: ✅/🟠/🟡 + 1-line reason
```
Covers: before/after UI/UX changes + component state

Review Checklist:
- [ ] All components use TypeScript interfaces for props
- [ ] No `any` types in production code
- [ ] useEffect has proper cleanup
- [ ] Lists have unique `key` prop
- [ ] Error boundaries wrap feature pages
- [ ] Loading states for async operations
- [ ] ZMP SDK calls in try/catch
- [ ] Dark mode works via zaui-theme
- [ ] No hardcoded strings (use constants)
- [ ] Responsive layout (mobile-first)

Prompt: "/archive <name>"
