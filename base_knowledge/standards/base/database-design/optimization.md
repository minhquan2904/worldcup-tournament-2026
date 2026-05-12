# Query Optimization

> N+1 problem, EXPLAIN PLAN, Oracle optimizer hints, optimization priorities.

## N+1 Problem

```
What is N+1?
├── 1 query to get parent records
├── N queries to get related records
└── Very slow!

Solutions:
├── JOIN         → Single query with all data
├── Bulk collect → PL/SQL BULK COLLECT INTO
├── Subquery     → Fetch related in one query
└── Cursor       → Explicit cursor with JOIN
```

## Query Analysis (Oracle EXPLAIN PLAN)

```sql
-- Analyze query execution plan
EXPLAIN PLAN FOR
SELECT c.CUSTOMER_NAME, a.ACCOUNT_NO
FROM BO_CUSTOMER c
JOIN BO_ACCOUNT a ON a.CUSTOMER_ID = c.ID
WHERE c.BRANCH_CODE = 'HCM';

-- View the plan
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- Look for:
-- ├── TABLE ACCESS FULL (full table scan — needs index?)
-- ├── Cost and cardinality estimates
-- ├── INDEX RANGE SCAN (good — using index)
-- └── HASH JOIN vs NESTED LOOPS (join strategy)
```

## Oracle Optimizer Hints

| Hint | When to Use |
|------|-------------|
| `/*+ INDEX(t idx_name) */` | Force specific index |
| `/*+ FULL(t) */` | Force full table scan (small tables) |
| `/*+ PARALLEL(t, 4) */` | Parallel execution for large queries |
| `/*+ FIRST_ROWS(n) */` | Optimize for first N rows (pagination) |
| `/*+ USE_HASH(t1 t2) */` | Force hash join |
| `/*+ LEADING(t1 t2) */` | Force join order |

> ⚠️ **Hints should be last resort.** Fix schema/indexes first. Hints bypass the optimizer's intelligence.

## Optimization Priorities

1. **Add missing indexes** (most common issue)
2. **Select only needed columns** (not `SELECT *`)
3. **Use proper JOINs** (avoid correlated subqueries when possible)
4. **Limit early** (pagination at database level with ROWNUM / ROW_NUMBER)
5. **Use BULK COLLECT** (for PL/SQL loops processing multiple rows)
6. **Bind variables** (avoid hard parsing — use `:p_param` not concatenation)
7. **Gather statistics** (`DBMS_STATS.GATHER_TABLE_STATS`) after large data changes

## Pagination Pattern (Oracle)

```sql
-- Standard Oracle pagination for backoffice reports
SELECT * FROM (
    SELECT t.*, ROW_NUMBER() OVER (ORDER BY t.MAKER_DT_STAMP DESC) AS RN
    FROM BO_CUSTOMER t
    WHERE t.RECORD_STAT = 'O'
)
WHERE RN BETWEEN :p_start AND :p_end;
```
