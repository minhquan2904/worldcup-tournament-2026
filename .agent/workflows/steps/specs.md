---
description: Generate behavioral specs - delta format with ADDED/MODIFIED/REMOVED.
---

# Dispatch -> .agent/skills/specs/SKILL.md
Input: Change name. Requires proposal.md + srs.md.

## Performs
- Read proposal.md + srs.md
- Load Spec Rules from PRJ-rule_planing_feature.md
- Generate specs/<domain>/spec.md for each domain
- Cross-check: all requirements covered, RFC 2119 keywords

Output: openspec/changes/<name>/specs/**/*.md
GATE -> review. Next: /design <name>
