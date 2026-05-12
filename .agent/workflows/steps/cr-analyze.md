---
description: Analyze existing code for CR - generate current-code-logic, compare-logic, proposal.
---

## Dispatch
Follow .agent/skills/cr-analyze/SKILL.md

## Input
CR name + description. User may specify affected modules.

## Performs
- Scaffold change directory
- Scan all layers: Controller -> Service/Handler -> Factory -> Model -> Repository -> Infra
- Generate current-code-logic.md (processing flow, config, message codes, integrations)
- Map code vs docs -> compare-logic.md ([V] Matched / [!] Divergent / [X] Missing)
- Generate metadata.yaml (type: change-request)
- Generate proposal.md (CR-specific with impact + risk)

Output: metadata.yaml, current-code-logic.md, compare-logic.md, proposal.md
Next: /srs <name>
