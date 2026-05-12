---
name: specs
description: Generate delta behavioral specs (ADDED/MODIFIED/REMOVED) with scenarios.
arguments: ["${change_name}"]
allowed-tools: [Read, Write, Grep, Glob, Bash]
context: inline
version: 3.0
---

# Specs — Behavioral Specifications

Output: specs/<domain>/spec.md in openspec/changes/<name>/
Input: Change name. proposal.md + srs.md must exist.

## §1 Verify
proposal.md + srs.md exist

## §2 Read Dependencies
proposal.md → scope, services | srs.md → requirements, API, flow type

## §3 ⛔ MANDATORY COMPLIANCE (HALT if failed)
artifact_context_modular.yml → section specs → load required_rules + required_skills + context

## §4 Generate Spec Files — Pure CoS v2 (State Transition)
Per affected domain → specs/<domain>/spec.md
- Delta only: ADDED / MODIFIED / REMOVED

Output format: **Pure CoS v2** — State Transition Notation (cos_convention.md §4.1)
```
### REQ: requirement_name (FR-xxx)
Fields/Filters/Controls declaration (if applicable)

SC1: [state_before] →(action)         [state_after] | side_effects
SC2: [state_before] →(action_invalid) ✗             | msg:"error_message"
```

Rules:
- Each SC = state machine transition: `[S_before] →(action) [S_after]`
- `[⊘]` = null state (creation from nothing)
- `✗` = blocked/refused (validation fail, system error)
- `|` separates side effects: msg, reload, clearForm
- State naming: entity(`[Active]`), UI(`[listScreen]`), collection(`[list:∅]`)
- !GIVEN/WHEN/THEN | !semi-CoS long chains | use column-aligned transitions
- Map each REQ to source: `(FR-xxx)` suffix

## §5 Cross-Check
- ✓ all requirements covered
- ✓ no duplicates
- ✓ no implementation details
- ✓ every req has ≥1 scenario

## Guardrails
- MUST read proposal + srs first
- MUST apply PRJ-rule_planing_feature.md
- !implementation details in specs
- !lose any requirement
