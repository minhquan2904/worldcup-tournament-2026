---
name: learn
description: Learn codebase — 9 sequential analysis steps → 8 knowledge files + 1 features registry
arguments: ["${group_or_step}"]
allowed-tools: [Read, Write, Grep, Glob]
context: fork
tag: "@AI-ONLY"
version: 4.0
---

# Learn Codebase

> 9 sequential steps → structured knowledge. Output = `propose/` + `apply/` + `features.md`

## Groups

| Group | Flag | Steps | Sub-skills | Tech |
|-------|------|-------|------------|------|
| react | `--group react` | 1-4 | react-architecture, react-component, react-state-service, react-shared-component | React/TS |
| utilities | `--group utilities` | 5-6 | react-hook-helper, react-util | React/TS |
| platform | `--group platform` | 7-8 | zmp-sdk, error-debug | ZMP/Shared |
| registry | `--group registry` | 9 | features registry | Shared |

> Run each group in separate conversation. Tech: React 18 / TypeScript / Vite / Jotai / ZMP SDK / ZMP UI / Tailwind CSS 3

## Dirs
- PROPOSE_DIR: `base_knowledge/structures/propose/`
- APPLY_DIR: `base_knowledge/structures/apply/`

---

## Steps — React Knowledge

| Step | Skill | Output | Key Scans |
|------|-------|--------|-----------|
| 1 | learn-react-architecture | `knowledge_react_architecture.md` | vite.config, tsconfig, app-config, routing, entry point, folder structure |
| 2 | learn-react-component | `knowledge_react_component.md` | pages/, components/, function components, props, hooks, ZMP UI |
| 3 | learn-react-state-service | `knowledge_react_state_service.md` | Jotai atoms, API services, constants, data fetching |
| 4 | learn-react-shared-component | `knowledge_react_shared_component.md` | shared components, props interfaces, ZMP UI wrappers |

## Steps — Utilities

| Step | Skill | Output |
|------|-------|--------|
| 5 | learn-react-hook-helper | `knowledge_react_hook_helper.md` |
| 6 | learn-react-util | `knowledge_react_util.md` |

## Steps — Platform

| Step | Skill | Output |
|------|-------|--------|
| 7 | learn-zmp-sdk | `knowledge_zmp_sdk.md` → PROPOSE_DIR |
| 8 | learn-error-debug | `knowledge_error_debug.md` → APPLY_DIR |

## Steps — Registry

| Step | Action | Output |
|------|--------|--------|
| 9 | scan ALL pages + components + stores | `features.md` → `base_knowledge/structures/` |

---

## Cross-Reference Matrix

| Knowledge | References |
|-----------|-----------|
| react_architecture | react_component, react_state_service, zmp_sdk |
| react_component | react_architecture, react_shared_component, react_hook_helper |
| react_state_service | react_component, react_util, zmp_sdk |
| react_shared_component | react_component, react_hook_helper |
| react_hook_helper | react_component, react_util |
| zmp_sdk | react_architecture, react_component |
| error_debug | react_architecture, zmp_sdk |

## Guardrails
- Output format: **Structured NL** for ALL knowledge_*.md — @AI-ONLY, pipeline context
- MUST cite actual component/file names + file paths — !placeholders
- sequential order — each step may depend on previous
- each knowledge file = self-contained (readable standalone)
- MUST reference convention-checker when documenting patterns
- Use cos_convention.md operators (→, !, &&, ||) and abbreviations
