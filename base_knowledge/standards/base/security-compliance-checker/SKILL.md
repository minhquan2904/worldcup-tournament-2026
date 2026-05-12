---
name: security-compliance-checker
when_to_use: Security compliance scan — extract rules from Excel, scan BE+FE code against OWASP checklist.
paths: [base_knowledge/standards/base/security-compliance-checker/]
---

# Security Compliance Checker

> Scan source code vs user-provided Excel rules. Script auto-detects column structure.

## 8 Phases
0. Get File Path (ASK user)
1. Rule Extraction: `python scripts/extract-owasp-rules.py "<path>" --output ./owasp_checklist.md`
2. User Approval (🔴 MANDATORY GATE — !scan without approval)
3. Init (load checklist + methodology)
4. Backend Scan (controllers, services, config, middleware)
5. Frontend Scan (components, services, guards, templates)
6. Cross-cutting (session, token, file, error, libs)
7. Report (classify findings, generate report)

## Methodology Sub-Files
| File | Chapters | Focus |
|------|----------|-------|
| methodology-injection-sanitization.md | V1 | Injection, deserialization |
| methodology-web-api-security.md | V3-V4 | CORS, CSP, HSTS |
| methodology-auth-session-token.md | V6-V9 | Auth, session, JWT, RBAC |
| methodology-file-crypto-infra.md | V5,V11-V14 | File, TLS, data protection |
| methodology-coding-error.md | V15-V16 | Libs, error handling |

## Dependencies
Python 3.x + openpyxl. Debug: --list-sheets, --preview
