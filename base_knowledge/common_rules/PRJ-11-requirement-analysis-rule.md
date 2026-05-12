---
description: Business Requirement Analysis Rules
tag: "@AI-ONLY"
---

# Business Requirement Analysis Rules

## §1 Requirement Classification (FR/NFR/BR/DR)
All input requirement docs MUST decompose into 4 independent groups:

- **FR** (Functional): system capabilities — CRUD, validation, state workflow
- **NFR** (Non-Functional): performance, security, audit log, auth, SLA
- **BR** (Business Rules): rules controlling function flow — limits, conditions, formulas
- **DR** (Data Requirements): data storage constraints, table relationships, lookup info

## §2 Hidden Knowledge Extraction
Devs cannot code without lifecycle info. BA MUST clarify:

- **State & Lifecycle:** how many states? transition triggers? soft delete || hard delete?
- **Auth & Audit:** which Role can operate? audit trail required?
- **Integration:** calls external system? (Core, SMS, Email) — retry mechanism?
- **Exceptions:** validation fail, logic fail → how to handle?

## §3 Traceability
- every requirement MUST have ID for tracing: `FR-01`, `BR-02`, ...
- ensures no logic dropped during design phase transition
