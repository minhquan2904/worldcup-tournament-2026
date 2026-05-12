---
name: archive
description: Archive completed change — code-vs-docs sync check, optional changelog, knowledge export advisory.
arguments: ["${change_name}"]
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
context: inline
version: 3.0
---

# Archive

Output: Synced documentation + archive move. CR variant: changelog.md + updated compare-logic.md.
Input: Change name (kebab-case). All pipeline steps must be complete.

## §1 ⛔ MANDATORY COMPLIANCE (HALT if failed)
Read artifact_context_modular.yml → section archive → load required_rules + required_skills

## §2 Verify Completion
`openspec status --change "<name>"` → check all artifacts + impl done

## §3 Detect Variant
metadata.yaml → type: new-feature | change-request

## §4 Code-vs-Documentation Sync
Compare source code against: proposal.md, design.md, specs/**
- MATCH → display [OK]
- MISMATCH → auto-edit docs to match code + add `> [!WARNING]` markers + display report

Rule: MUST only edit docs → !edit code to match docs

## §5 CR Variant: compare-logic.md + changelog.md
Update comparison table (Before→After), generate changelog (Added/Modified/Removed/Fixed)

## §6 Archive Move
`openspec/changes/<name>/ → openspec/archive/<name>/`
Verify all files included

## §7 Knowledge Export Advisory
Check if change affects base_knowledge → warn but !auto-update

## Guardrails
- MUST sync BEFORE archiving
- MUST only edit docs not code
- !auto-update base_knowledge — only advise
