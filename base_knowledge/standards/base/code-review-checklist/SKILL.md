---
name: code-review-checklist
when_to_use: Code review — correctness, security, performance, quality, testing, documentation.
paths: [base_knowledge/standards/base/code-review-checklist/]
---

# Code Review Checklist

## Quick Review
- **Correctness**: does what expected, edge cases, error handling, no bugs
- **Security**: input validated, no injection/XSS/CSRF, no hardcoded secrets, AI prompt injection protection
- **Performance**: no N+1, no unnecessary loops, caching, bundle size
- **Quality**: clear naming, DRY, SOLID, appropriate abstraction
- **Testing**: unit tests, edge cases, readable
- **Documentation**: complex logic commented, public APIs documented

## Review Comment Severity
🔴 BLOCKING | 🟡 SUGGESTION | 🟢 NIT | ❓ QUESTION

## Anti-Patterns to Flag
❌ Magic numbers → named constants
❌ Deep nesting → early returns
❌ `any` type → proper types
❌ Long functions → small focused functions
