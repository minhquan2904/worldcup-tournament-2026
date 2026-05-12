---
description: Post-implementation review - scan frontend React code, generate tracking artifacts.
---

## Dispatch
Follow .agent/skills/review-fe/SKILL.md

## Input
Change name. Frontend implementation must be complete.

## Performs
- Verify prerequisites (FE code exists)
- Load artifact_context_modular.yml section review-fe
- HALT if required rules missing
- Scan TSX, TS source code
- Generate: todo-uncover-fe.md, delta-spec-fe.md

Output: tracking files in openspec/changes/<name>/
Next: /archive <name>
