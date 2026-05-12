---
description: Pre-process URD into raw extraction. MCP entry point for Confluence/Jira.
---

§ Dispatch → .agent/skills/preprocess/SKILL.md
Support: confluence-reader (reads Confluence pages when input is URL/ID)

§ Steps
1. IF input = Confluence URL/ID → invoke confluence-reader skill FIRST
2. Invoke preprocess skill → pre_process.md

§ Pipeline: /preprocess →🔴→ /srs →🔴→ /init → /specs →🔴→ (--backend|--frontend) → /archive
> ONLY step that calls MCP. Subsequent steps read pre_process.md.

🔴 GATE → present summary, wait for user review. Next: /srs <name>