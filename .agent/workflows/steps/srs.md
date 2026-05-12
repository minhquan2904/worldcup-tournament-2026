---
description: Generate SRS — consolidate pre_process.md into shared business specification.
---

§ Dispatch → .agent/skills/srs/SKILL.md
Agent: ba-specialist

§ Input: Change name. Requires pre_process.md.
> !MCP calls. All content from /preprocess.

§ Performs
- Consolidate + refine requirements (dedup, normalize, conflicts)
- Elaborate use case flows (Mermaid)
- Enrich with banking domain (idempotency, retry, security, logging)
- Data requirements at LOGICAL level (!physical DB)
- Authorization + error handling at BUSINESS level
- Quality scoring

§ Boundary: SRS = BUSINESS doc (WHAT, !HOW)
!class names, !file paths, !API endpoints, !HTTP methods, !SQL, !DI patterns

Output: openspec/changes/<name>/srs.md
🔴 GATE → BA/Dev/Tester review. Next: /init <name>
