---
description: Run security compliance scan. READ-ONLY.
version: 4.0
---

# /security-scan

$ARGUMENTS

⚠️ READ-ONLY — !modify source code

## Steps

0. **Checklist Extraction** — find .xlsx security rules (auto-search or from $ARGUMENTS)
   - ⛔ Load PRJ-06-owasp-security-scan-rule.md
   - Run extract-owasp-rules.py → owasp_checklist.md
   - 🛑 Approval Gate

1. **Security Scan** — scan React/TypeScript code vs checklist, classify issues
   - Scope: src/pages/, src/components/, src/hooks/, src/services/, src/stores/, src/utils/
   - Key checks: XSS (dangerouslySetInnerHTML), hardcoded secrets, eval(), exposed tokens, insecure storage
2. **Report** — statistics, severity (🔴🟠), Mermaid Pie, detail (req_id, file, line)
   - Pipeline → openspec/changes/<name>/security-report.md
   - Standalone → display on chat

## Usage
```
/security-scan
/security-scan "OWASP_checklist.xlsx"
```
