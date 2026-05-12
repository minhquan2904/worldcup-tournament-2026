---
name: apply
description: Implement tasks from change artifacts with React project standards enforcement and Feature Profile cross-checking.
arguments: ["${change_name}"]
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
context: inline
version: 4.0
---

# Apply — Code Generation

Output: Source code files at project location.
Input: Change name (kebab-case). `tasks.md` + `design.md` must exist.

## §1 ⛔ MANDATORY COMPLIANCE (HALT if failed)
Read `openspec/mapping/artifact_context_modular.yml` → section `apply`
- Load required_skills (glob resolve) → HALT if missing, READ if exists
- Load required_rules → HALT if missing
- Load context (soft) → base_knowledge/structures/apply/** + propose/** → WARN if empty
- Load: overview_system.md + common_rules/** → HALT if exists but unreadable

!proceed until ALL required_rules + required_skills confirmed

## §2 Read Change Artifacts
From openspec/changes/<name>/:
- proposal.md → what+why
- srs.md → feature specs, phases
- design.md → component tree, state, API design
- tasks.md → implementation checklist
- specs/**/*.md → behavioral requirements
If CR variant (detect current-code-logic.md): also read compare-logic.md

## §3 Feature Profile
Cross-reference knowledge → lock:
- Mode: LIST | DETAIL | FORM | DASHBOARD
- State: Jotai atoms | useState local | mixed
- Data: API service | static | ZMP SDK
- Type: NEWBUILD | MAINTENANCE
Show locked profile before implementing.

## §4 Implement Tasks
Loop tasks.md unchecked items:
1. Read task spec + convention reference
2. Read convention file BEFORE generating
3. Generate source code following design.md
4. Per-task cross-check:
   - Component (function component, TypeScript props, hooks at top-level)
   - State (Jotai atoms for global, useState for local)
   - Service (typed API functions, error handling)
   - Routing (ZMPRouter, Route from zmp-ui)
   - Style (Tailwind CSS, dark mode support)
   - Types (no `any`, proper interfaces)
5. Mark done [x]

## Guardrails
- MUST load knowledge BEFORE implementing
- MUST determine Feature Profile BEFORE code
- MUST cross-check EVERY task against profile
- design.md conflicts with knowledge → follow knowledge
- !invent logic outside design/specs
- !Angular patterns — React function components ONLY
- !class components, !NgModule, !DI inject()
