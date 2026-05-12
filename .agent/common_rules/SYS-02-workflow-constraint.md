---
description: Workflow Constraint — Plan→Act→Reflect loop, Fail Fast, Approval Gate, Context Efficiency
tag: "@AI-ONLY"
---

# Workflow Constraints

## §1 Reasoning Loop
Plan → Act → Reflect (mandatory cycle)

1. **Plan:** declare approach, intended tools, expected output
2. **Act:** execute using specific Skills/Tools
3. **Reflect:** evaluate results vs plan → restart if incorrect

## §2 Fail Fast & Recovery
- tool_error → retry(max: 2, adjust_params: true)
- after 2 failures → haltIf(true) — report error + askUser for guidance
- !substitute(dummy_data) to continue workflow — NEVER

## §3 Approval Gate (Human-In-The-Loop)
- structural_changes (DB scripts, API interfaces) → yieldToUser(plan) && wait(approval)
- !auto_execute(shell_commands) on Prod || Staging

## §4 Context Efficiency
- handoff between steps: pass final output/findings only
- !pass(raw_logs || full_page_text || unprocessed_data) to next step
