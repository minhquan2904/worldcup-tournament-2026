---
description: System Scope & Boundaries — Security boundaries, least privilege, goal drift prevention
tag: "@AI-ONLY"
---

# System Scope & Boundaries

## §1 Least Privilege
- access: min(data_for_current_task) only
- !scan(entire_codebase) — unless user explicitly approves
- !fetch(all_system_data) — unless user explicitly approves
- scope: all scanDir/grepFor ops must stay within ${PROJECT_ROOT}
- !traverse("..") && !access(adjacent_projects)
- data_access: only Jira/Confluence within granted Project Key || Keyword scope

## §2 Rule of Two — Security Framework
Agent must NOT hold >2 of these 3 capabilities simultaneously:
1. Read untrusted inputs (user-provided data)
2. Access sensitive systems (private codebase, production DB)
3. Modify system state (write/deploy)

Consequence:
- analysis_agent → !execute(DB inserts)
- ddl_agent → yieldToUser(output) before execution

## §3 Goal Drift Prevention
- self_check: every 3-5 sub-tasks, compare current actions vs original objective
- !invent_tasks beyond specified requirements
- !expand_scope beyond what user requested
