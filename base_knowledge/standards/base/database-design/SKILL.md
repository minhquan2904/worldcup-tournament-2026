---
name: database-design
when_to_use: Database design for Oracle — schema, normalization, indexing, optimization.
paths: [base_knowledge/standards/base/database-design/]
---

# Database Design

> Oracle banking systems. Related: oracle-ddl-generation, oracle-package-crud-generation, oracle-package-report-generation

## Sub-Files
| File | When |
|------|------|
| schema-design.md | Designing schema (normalization, PKs, relationships, Oracle types) |
| indexing.md | Performance tuning (index types, composite, partitioning) |
| optimization.md | Query optimization (EXPLAIN PLAN, hints, N+1) |

## Core Principles
- Follow PRJ-10-database-naming-convention, PRJ-12-logical-data-modeling-rule
- Oracle ONLY (!PostgreSQL, !MySQL)
- No ORM — PL/SQL packages for data access
- Financial tables MUST have audit columns (RECORD_STAT, AUTH_STAT, MAKER_ID, CHECKER_ID)

## Anti-Patterns
❌ ORM instead of PL/SQL | ❌ Skip FK indexing | ❌ SELECT * in production
❌ JSON when structured columns fit | ❌ Ignore N+1 | ❌ Tables without audit columns
