---
name: sync-task
description: Sync documentation with current source code — detect drift, auto-correct docs to match implementation.
arguments: ["${change_name_or_id}"]
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
context: inline
version: 4.0
---

# Sync Task — Documentation ↔ Code Sync

Input: Task name (kebab-case) or metadata ID.

## §1 Locate Change
1a. Search active: openspec/changes/ → match name or metadata.yaml id
1b. Search archived: openspec/changes/archive/ → match name or id
1c. Not found → list all + stop | Multiple → ask user

## §2 Read Documentation Artifacts
Feature: proposal, design, tasks, specs, srs, metadata
CR: + current-code-logic, compare-logic
Extract: page routes, component props, hook signatures, atom definitions, API service functions, type interfaces, configs

## §3 Analyze Current Source Code
Scan documented items in actual codebase: pages, components, hooks, atoms, services, types, utils, routes, configs

## §4 Compare → Sync Status
```
[V] In Sync | [!] Drifted | [NEW] Code Only | [DEL] Docs Only
```
Detailed table: Item, Document, Doc Description, Code Reality, Status

## §5 Handle Results
All sync → update metadata last-sync → stop
Drift detected → step 6
Archived + drifted → move back to active → step 6

## §6 Auto-Correct Documentation
- [!] Drifted → update doc section + `> [!WARNING]` marker with before/after
- [NEW] Code Only → add section + `> [!NOTE]` marker
- [DEL] Docs Only → !remove, add `> [!CAUTION]` marker
Generate sync report table

## §7 Update metadata.yaml
```yaml
last-sync: "ISO timestamp +07:00"
```

## Guardrails
- MUST only edit docs → !edit code to match docs
- MUST add [!WARNING] on every correction with timestamp + before/after
- MUST search BOTH active + archived
- MUST unarchive before modifying
- !remove documented items missing from code — only [!CAUTION]
- !auto-archive — let user decide
- !guess code behavior — scan actual source
