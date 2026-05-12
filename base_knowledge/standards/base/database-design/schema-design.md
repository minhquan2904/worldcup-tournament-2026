# Schema Design Principles

> Normalization, primary keys, timestamps, relationships — Oracle context.

## Normalization Decision

```
When to normalize (separate tables):
├── Data is repeated across rows
├── Updates would need multiple changes
├── Relationships are clear
└── Query patterns benefit

When to denormalize (embed/duplicate):
├── Read performance critical
├── Data rarely changes
├── Always fetched together
└── Simpler queries needed
```

## Primary Key Selection

| Type | Use When | Oracle Implementation |
|------|----------|----------------------|
| **Sequence + Trigger** | Standard approach for banking tables | `CREATE SEQUENCE`, `BEFORE INSERT` trigger |
| **Composite PK** | Junction tables, multi-tenant | `PRIMARY KEY (col1, col2)` |
| **Natural key** | Reference/lookup tables with business codes | `PRIMARY KEY (BRANCH_CODE)` |

> ⚠️ **Note:** Project convention uses `NUMBER` type for PKs with Oracle sequences, NOT UUID/GUID.

## Audit Columns (MANDATORY for Banking)

```sql
-- Every table MUST include:
RECORD_STAT       CHAR(1) DEFAULT 'O',          -- Record status
AUTH_STAT          CHAR(1) DEFAULT 'U',          -- Authorization status
MAKER_ID           VARCHAR2(30),                  -- Creator
MAKER_DT_STAMP    DATE DEFAULT SYSDATE,          -- Created at
CHECKER_ID         VARCHAR2(30),                  -- Approver
CHECKER_DT_STAMP  DATE,                           -- Approved at
MOD_NO             NUMBER(6) DEFAULT 1,           -- Modification number
ONCE_AUTH          CHAR(1) DEFAULT 'N'            -- Once authorized flag
```

## Timestamp Strategy

```
For every table:
├── MAKER_DT_STAMP  → When created (DATE DEFAULT SYSDATE)
├── CHECKER_DT_STAMP → When approved (DATE)
└── Use DATE type (includes time in Oracle)

Oracle DATE includes time component — no need for TIMESTAMP unless sub-second precision needed.
```

## Relationship Types

| Type | When | Implementation |
|------|------|----------------|
| **One-to-One** | Extension data | Separate table with FK |
| **One-to-Many** | Parent-children | FK on child table |
| **Many-to-Many** | Both sides have many | Junction table |

## Foreign Key ON DELETE

```
├── CASCADE    → Delete children with parent (RARE in banking)
├── SET NULL   → Children become orphans
├── RESTRICT   → Prevent delete if children exist (DEFAULT for banking)
└── NO ACTION  → Similar to RESTRICT (Oracle default)
```

> ⚠️ **Banking rule:** Prefer `RESTRICT` or soft-delete (`RECORD_STAT = 'C'`) over `CASCADE`. Financial records should never be hard-deleted.
