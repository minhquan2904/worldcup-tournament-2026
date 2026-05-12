---
name: api-patterns
when_to_use: REST API design — resource naming, HTTP methods, response format, auth, documentation.
paths: [base_knowledge/standards/base/api-patterns/]
---

# API Patterns — REST Design Principles

> Project-specific conventions → standards/api-patterns/ (rest.md, response.md, auth.md, documentation.md)

## Resource Naming
| Rule | ✅ | ❌ |
|------|---|---|
| Danh từ (not verbs) | POST /api/users | POST /api/createUser |
| Lowercase | /api/backgrounds | /api/Backgrounds |
| Nested cha-con | /categories/{id}/items | /getCategoryItems |
| Max 2 cấp lồng | /modules/{id}/functions | /a/{id}/b/{id}/c/{id}/d |

## HTTP Method → Action
| Method | Action | Purpose |
|--------|--------|---------|
| GET | Search/GetBy | Read |
| POST | Create | Create |
| PUT | Update | Full update |
| PATCH | Partial/Toggle | Partial update |
| DELETE | Delete | Remove |

## Status Codes
200=OK, 201=Created, 400=BadRequest, 401=Unauthorized, 403=Forbidden, 404=NotFound, 500=ServerError

## Core Rules
- Response PHẢI dùng envelope pattern nhất quán
- List API PHẢI có pagination (totalRecords, pageNumber, pageSize)
- Error response PHẢI có structured format
- Mọi endpoint PHẢI có authorization
- Permission sync: DB ↔ BE ↔ FE
- API docs = hợp đồng BE↔FE

## Anti-Patterns
❌ Verbs in URL | ❌ Raw framework responses | ❌ Hardcode permission strings
❌ No API docs | ❌ Expose stack traces | ❌ Business logic in Controller
