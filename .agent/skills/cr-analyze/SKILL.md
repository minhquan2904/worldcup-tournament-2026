---
name: cr-analyze
description: Analyze existing codebase for CR — scan React layers, generate current-code-logic, compare-logic, proposal.
arguments: ["${change_name}"]
allowed-tools: [Read, Write, Grep, Glob, Bash]
context: inline
version: 4.0
---

# CR Analyze

Output: metadata.yaml + current-code-logic.md + compare-logic.md + proposal.md
Input: CR name (kebab-case) + description. User may specify affected components/pages.

## §1 Gather CR Info
If not provided → ask: what changes, which pages/components, Confluence/Jira refs

## §2 Scaffold
`openspec new change "<name>"`

## §3 Deep Scan Existing Codebase
All layers: Pages (routes, layout) → Components (props, state) → Hooks (custom logic) → Atoms (Jotai state) → Services (API calls) → Types (interfaces) → Utils (helpers) → Config (app-config, routes, constants)

## §4 Generate current-code-logic.md
Processing Flow, Component Tree, Atom Dependencies, API Endpoints used, Route Map, Key Files table

## §5 Generate compare-logic.md
| Logic Point | Code State | Doc State | Status | Gap Analysis |
Status: [V]Matched, [!]Divergent, [X]Missing, [+]DocOnly
Gap: No Change / Modify / New / Remove

## §6 Generate metadata.yaml
type: "change-request"

## §7 Generate proposal.md
Load context from artifact_context_modular.yml → section proposal
Include: why CR needed (from code scan), impact analysis, risk, scope

## Guardrails
- MUST analyze ACTUAL codebase — !guess
- MUST create ALL 4 artifacts
- Order: current-code-logic → compare-logic → proposal
- !implement code — only analyze and document
