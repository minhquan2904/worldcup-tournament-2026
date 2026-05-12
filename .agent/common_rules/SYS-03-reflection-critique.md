---
description: Reflection & Critique — Mandatory Generator-Critic pattern for all code/script output
tag: "@AI-ONLY"
---

# Reflection & Critique

## §1 Generator-Critic Pattern
Every code/script output: !end_at_first_draft

1. **Generator:** create draft from requirements
2. **Critic:** switch to Senior Reviewer role → list 3-5 specific issues
   - missing audit fields? naming violations? runtime risks?
3. **Refine:** incorporate Critic feedback → produce final version

## §2 Critique Criteria (allowed evaluation targets)
- naming_convention compliance (per PRJ rules)
- syntax compatibility with target system
- completeness of input requirements (missing columns? APIs? fields?)
- security && runtime risk assessment
- !subjective_comments ("inelegant", "ugly") — FORBIDDEN, must target Data/Logic

## §3 Pre-Submit Verification
- before output → cross-check vs relevant PRJ rules
- tag output: `[CRITIQUE-PASSED]` || include 1-2 sentence self-review confirmation
