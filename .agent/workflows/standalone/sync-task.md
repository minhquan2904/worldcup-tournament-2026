---
description: Sync documentation artifacts with current source code. Detects drift, auto-corrects docs.
version: 3.0
---

# /sync-task

Input: Task name (kebab-case) or metadata ID.

## Steps

1. **Invoke sync-task skill**
   - ⛔ Load artifact_context_modular.yml → section sync-task → HALT if missing
   - Follow .agent/skills/sync-task/SKILL.md

Performs:
- Find change by name or id (active + archived)
- Compare docs vs source code
- In sync → report + exit
- Drifted → auto-correct docs + `> [!WARNING]` markers
- Archived → unarchive → sync → prompt re-archive
- Update metadata.yaml last-sync

## Guardrails
- MUST only edit docs → !edit code
- MUST handle archived changes
- MUST update last-sync
