---
description: Map project architecture into structure docs — verify base_knowledge, detect tech stack, generate system_overview.
version: 4.0
---

# /map-structures

$ARGUMENTS

> base_knowledge/ MUST already exist (copied from framework). HALT if not found.

## Input
| Command | What runs |
|---------|----------|
| /map-structures | system_overview.md + ALL modules |
| /map-structures --module <name> | ONE specific module (requires system_overview.md) |

## Steps

### 0. Prerequisites (USER manual)
Copy base_knowledge/ from framework → project root

### 1. Verify base_knowledge/
Exists → proceed. !found → HALT

### 2. Detect Tech Stack
package.json→React/deps, vite.config.mts→Vite, tsconfig.json→TypeScript, zmp-cli.json→Zalo Mini App, tailwind.config.js→Tailwind CSS
!hardcode, !guess — only verifiable data

### 3a. Create system_overview.md (MANDATORY first)
Sections: Tech Stack table, Architecture Pattern, Folder Structure, Build & Deploy, Route Map

### 3b. Document modules
For each → base_knowledge/structures/<kebab-case-name>.md with:
1. Primary Responsibilities
2. Dependencies (components, hooks, atoms, services)
3. Key Processing Flow (data flow)
4. Visual Diagrams (Mermaid component tree + data flow)

## Guardrails
- MUST HALT if base_knowledge/ missing
- !overwrite existing without asking
- REAL component/file names only, !placeholders
- Mermaid fenced with ```mermaid
- system_overview.md BEFORE module files
- !sensitive data
- self-contained files (readable alone)
