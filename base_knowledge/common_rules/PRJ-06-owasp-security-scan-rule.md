---
description: Security Compliance Scan Rules (OWASP) — React/Zalo Mini App
tag: "@AI-ONLY"
---

# Security Compliance Scan Rules

## §0 Dynamic Rule Extraction (MANDATORY FIRST)

### §0a askUser for Excel path
- !assume filename || format — askUser("Provide OWASP Excel file path")

### §0b Extract rules
```bash
python base_knowledge/standards/security-compliance-checker/scripts/extract-owasp-rules.py "<path>" --output ./owasp_checklist.md
```
- script auto-detects column structure — Excel format may vary
- filter PIC = All || FE (via `--pic`)
- output: `owasp_checklist.md`
- debug: `--preview` || `--list-sheets` on error

### §0c yieldToUser(checklist) → wait(approval) before scan
- !hardcode_rules — !assume_filename — everything dynamic

## §1 Path Resolution
- `${FE_ROOT}` = dir containing `package.json` with `zmp-ui` dependency
- scan React/Zalo Mini App scope only

## §2 Scan Scope

### React FE — IN SCOPE:
| Directory | Content | Priority |
|-----------|---------|----------|
| `${FE_ROOT}/src/pages/` | Page components | 🔴 |
| `${FE_ROOT}/src/components/` | Shared components | 🔴 |
| `${FE_ROOT}/src/services/` | API service functions | 🔴 |
| `${FE_ROOT}/src/hooks/` | Custom hooks (auth, data) | 🔴 |
| `${FE_ROOT}/src/stores/` | Jotai atoms (state) | 🟠 |
| `${FE_ROOT}/src/utils/` | Utility functions | 🟠 |
| `${FE_ROOT}/index.html` | CSP, meta tags | 🟠 |
| `${FE_ROOT}/app-config.json` | App configuration | 🟡 |
| `${FE_ROOT}/.env` | Environment variables | 🔴 |

- files: `.ts`, `.tsx`, `.html`, `.json`, `.env`
- !scan: `node_modules/`, `dist/`, `.git/`, `.agent/`, `*.spec.ts`

### Key Security Checks for React/ZMP:
| Check | Category | Priority |
|-------|----------|----------|
| XSS via dangerouslySetInnerHTML | Injection | 🔴 |
| Hardcoded secrets in source | Secrets | 🔴 |
| API keys in client code | Secrets | 🔴 |
| Missing CSP headers | HTTP Security | 🟠 |
| localStorage sensitive data | Data Storage | 🟠 |
| Unvalidated user input | Input Validation | 🔴 |
| Missing error boundary | Error Handling | 🟠 |
| ZMP SDK auth token exposure | Auth | 🔴 |
| Insecure fetch/API calls | Transport | 🟠 |
| eval() or Function() usage | Code Injection | 🔴 |

## §3 Severity

| Level | Icon | OWASP Mapping |
|-------|------|---------------|
| CRITICAL | 🔴 | L1 (Essential) — XSS, hardcoded secrets, eval(), exposed tokens |
| WARNING | 🟠 | L2 (Standard) — missing input validation, insecure storage |
| INFO | 🟡 | L3 (Advanced) — missing CSP fine-tuning, no subresource integrity |
| PASS | ✅ | fully compliant |

## §4 Output Format
- Per-Chapter summary table (by OWASP section)
- Per-Finding detail: File, Status, Detail, Rule (OWASP req_id)
- Overall summary + Mermaid pie chart

## §5 Behavioral Rules

| # | Rule | Description |
|---|------|-------------|
| R1 | READ-ONLY | !modify source — read && report only |
| R2 | EXHAUSTIVE | check ALL rules in owasp_checklist.md — !skip |
| R3 | TRACEABLE | each finding MUST ref OWASP req_id AND file |
| R4 | STRUCTURED | output per §4 format |
| R5 | NO FALSE POSITIVES | readFile(actual code) — !grep_only |
| R6 | PRIORITIZED | order: CRITICAL → WARNING → INFO |
| R7 | DYNAMIC RULES | rules from Excel (§0) — !hardcode |
| R8 | USER APPROVAL | askUser(Excel path) + yieldToUser(checklist) before scan |

## §6 Anti-Patterns
- !scan_without_extract_script
- !assume_excel_filename
- !hardcode_rule_list
- !scan_before_user_approval
- !scan_without_report
- !report_without_owasp_req_id
- !modify_code
- !skip_file
- !report_without_severity
