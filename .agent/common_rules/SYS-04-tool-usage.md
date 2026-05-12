---
description: Tool Usage Constraint — Precise parameters, token efficiency, judicious tool selection
tag: "@AI-ONLY"
---

# Tool Usage Constraints

## §1 Precise Parameters
- analyze user input → extract exact tool params (Key, URL, ID, Keywords)
- !guess(params) — FORBIDDEN
- if params insufficient → askUser("provide missing info: ...")

## §2 Token Efficiency
- pagination/filtering: limit=5 || limit=10 — !fetch(all_data_at_once)
- readFile: use StartLine/EndLine blocks — !read(entire_file) when unnecessary

## §3 Judicious Tool Selection
- !use(Python scripts) to parse files when readFile + LLM reasoning suffices
- use shell commands only when OS interaction truly needed (compile, test, git)

## §4 Respect Tool Errors
- tool_error → log + retry(adjust_params)
- after 2 failures → haltIf(true) — see SYS-02 §2
