---
name: srs
description: Generate SRS — shared business document for BA, Dev, Tester. Consolidates pre_process.md into enriched specification.
arguments: ["${change_name}"]
allowed-tools: [Read, Write, Grep, Glob]
context: inline
version: 3.0
---

# SRS — Software Requirements Specification

Output: srs.md in openspec/changes/<name>/
Input: Change name. pre_process.md must exist (from /preprocess).
Nature: BUSINESS document — WHAT, not HOW.

## §1 Verify
pre_process.md exists → if not, /preprocess first

## §2 Read pre_process.md
Feature type, raw FRs, actors, integrations, assumptions, open questions
!call Confluence/Jira MCP — content already collected

## §3 ⛔ MANDATORY COMPLIANCE (HALT if failed)
artifact_context_modular.yml → section srs → load required_rules + required_skills + context

## §4 Consolidate Requirements
- Deduplicate, normalize wording, detect conflicts (→ Issues, !silently remove)
- Refine FR quality: clear, testable, no duplicates, consistent language
- Mandatory="phải", Recommended="nên", Optional="có thể"

## §5 Elaborate Use Cases
Basic Flow (happy path), Alternative Flows, Exception Flows, Mermaid for complex flows
Business language only: "Hệ thống xác thực" ✅ → !"Gọi API /auth/verify" ❌

## §6 Enrich Banking Domain (only if missing)
Constraints (idempotency, logging, timeout, retry), NFR (response time, HA), Security (auth, encryption)
Mark [Enriched]. !override existing.

## §7 Data Requirements (LOGICAL only)
Business entities + attributes + relationships
✅ "Mỗi tham số có: tên, giá trị, mô tả" → ❌ "VARCHAR2(2000)", "BaseFieldEntity"

## §8 Authorization (BUSINESS level)
✅ "Người dùng BO có quyền xem" → ❌ "FuncRleSystemParameter..."

## §9 Error Handling (BUSINESS level)
✅ "Nếu tên đã tồn tại → thông báo lỗi" → ❌ "ERR_NAME_EXISTS, HTTP 400"

## §10 Quality Score + Issues
Clarity(0-25) + Completeness(0-25) + Consistency(0-25) + Testability(0-25)
<70 → populate Open Questions. <50 → ask user.
Issues: Conflict, Missing, Ambiguity, Risk → ISSUE-XXX entries

## §11 Finalize
Follow template from openspec/schemas/modular_feature/templates/srs.md

## Guardrails
- !generate code or technical design
- !include: class names, file paths, API endpoints, HTTP methods, DB types, DI patterns
- !invent business logic, !remove original intent
- !discard conflicts silently
- !call Confluence/Jira MCP
- Vietnamese language (except IDs + tech terms)
- [Enriched] clearly distinguishable
- ⚠️ BOUNDARY: NO implementation details
