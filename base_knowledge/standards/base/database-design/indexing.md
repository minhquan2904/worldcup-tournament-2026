# Indexing Principles

> When and how to create indexes effectively in Oracle.

## When to Create Indexes

```
Index these:
├── Columns in WHERE clauses
├── Columns in JOIN conditions
├── Columns in ORDER BY
├── Foreign key columns
└── Unique constraints

Don't over-index:
├── Write-heavy tables (slower inserts)
├── Low-cardinality columns (unless bitmap)
├── Columns rarely queried
```

## Oracle Index Type Selection

| Type | Use For | Oracle Syntax |
|------|---------|---------------|
| **B-tree** | General purpose, equality & range queries | `CREATE INDEX idx_name ON table(col)` |
| **Bitmap** | Low-cardinality columns (status flags, Y/N) | `CREATE BITMAP INDEX idx_name ON table(col)` |
| **Function-based** | Queries on expressions/functions | `CREATE INDEX idx_name ON table(UPPER(col))` |
| **Reverse key** | Sequence-generated PKs (reduce contention) | `CREATE INDEX idx_name ON table(col) REVERSE` |
| **Composite** | Multi-column WHERE/JOIN conditions | `CREATE INDEX idx_name ON table(col1, col2)` |

> ⚠️ **Bitmap indexes** are excellent for OLAP/reporting but dangerous for OLTP with high concurrency — use B-tree for frequently updated columns.

## Composite Index Principles

```
Order matters for composite indexes:
├── Equality columns first
├── Range columns last
├── Most selective column first
└── Match query pattern

Example:
  Query: WHERE BRANCH_CODE = 'HCM' AND TXN_DATE > SYSDATE - 30
  Index: CREATE INDEX idx_txn ON BO_TRANSACTION(BRANCH_CODE, TXN_DATE)
```

## Partitioning (Large Tables)

```
When to partition:
├── Table > 10M rows
├── Date-range queries are common
├── Historical data archival needed
└── Parallel query performance required

Partition types:
├── RANGE  → Date-based (most common for banking)
├── LIST   → Category-based (branch, region)
├── HASH   → Even distribution
└── COMPOSITE → Range + List combined
```

## Index Naming Convention

```
Pattern: IDX_<TABLE_NAME>_<COLUMN(S)>
Examples:
├── IDX_BO_CUSTOMER_NAME
├── IDX_BO_TRANSACTION_DATE
├── IDX_BO_ACCOUNT_BRANCH_STATUS
└── UQ_BO_CUSTOMER_CIF (for unique indexes)
```
