---
name: map-structures
description: Map project architecture into structure docs — verify base_knowledge, detect tech stack, generate system_overview.
arguments: ["${service_name}"]
allowed-tools: [Read, Write, Grep, Glob]
context: inline
version: 4.0
---

# Map Structures

Output: system_overview.md + per-module architecture docs in base_knowledge/structures/
Input: Optional --module <name> for single module. Default: ALL.

## §0 Prerequisites (USER manual)
Copy base_knowledge/ from git framework to project root

## §1 Verify base_knowledge/
Exists → proceed. !found → HALT: "copy base_knowledge/ from framework"

## §2 Detect Tech Stack
Scan: package.json(→React/deps), vite.config.mts(→Vite), tsconfig.json(→TypeScript), zmp-cli.json(→Zalo Mini App), tailwind.config.js(→Tailwind CSS), app-config.json(→ZMP config)
!hardcode, !guess — only verifiable data

Expected stack for this project:
| Tech | Source | Version |
|------|--------|---------|
| React | package.json | ^18.3.1 |
| TypeScript | tsconfig.json | strict mode |
| Vite | vite.config.mts | ^5.2.13 |
| Jotai | package.json | ^2.12.1 |
| ZMP SDK | package.json | latest |
| ZMP UI | package.json | latest |
| Tailwind CSS | tailwind.config.js | ^3.4.3 |
| SCSS | postcss.config.js | ^1.76.0 |

## §3 Create system_overview.md (MANDATORY)
Sections: Tech Stack table, Architecture Pattern (Component-based SPA), Folder Structure, Build & Deploy (zmp CLI), Route Map

## §4 Document Modules (OPTIONAL)
For each feature module → base_knowledge/structures/<kebab-case-name>.md
Include: responsibilities, component tree, data flow, state management, Mermaid diagrams

## Guardrails
- MUST HALT if base_knowledge/ missing
- !overwrite existing without asking
- ALL component/file names = REAL, !placeholders
- Mermaid blocks use ```mermaid fence
- MUST create system_overview.md BEFORE module files
- !sensitive data
