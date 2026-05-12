---
description: Archive completed change - code-vs-doc sync, changelog, archive move.
---

## Dispatch
Follow .agent/skills/archive/SKILL.md

## Input
Change name. All implementation + review complete.

## Performs
A. Code-vs-docs sync check (MATCH->OK, MISMATCH->auto-edit docs)
B. CR-specific: update compare-logic.md + generate changelog.md
C. Move to openspec/archive/<name>/
D. Knowledge export advisory (warn only, !auto-update base_knowledge)

## Guardrails
- MUST sync-check before archive
- MUST only edit docs->match code (!reverse)
- !auto-update base_knowledge
