---
description: Scan React/TypeScript source code for convention violations, structure issues, and anti-patterns. READ-ONLY.
version: 4.0
---

# /react-scan

$ARGUMENTS

⚠️ READ-ONLY — !modify source code

## Steps

0. **Plan** — parse scope (default: full scan src/pages/, src/components/, src/hooks/, src/stores/, src/services/)
   - ⛔ Load PRJ-07-react-scan-rule.md → HALT if missing
   - 🛑 Approval Gate

1. **Scan** — load conventions, scan source, classify (🔴🟠🟡✅)
2. **Report** — statistics, Mermaid Pie, Top 10 violations
3. **Recommendations** — prioritized actions (CRITICAL→WARNING)

## Usage
```
/react-scan
/react-scan pages product
/react-scan hooks
/react-scan components shared
```
