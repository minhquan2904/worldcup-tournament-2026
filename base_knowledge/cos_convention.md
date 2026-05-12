---
description: Code-flavored Structured NL Convention — action verbs, abbreviations, operators, and file category tags for AI agent files.
tag: "@AI-ONLY"
version: 1.0
---

# Code-flavored Structured NL Convention

> Convention file cho toàn bộ dự án. Mọi file `@AI-ONLY` và phần instruction trong `@HYBRID` files phải tuân thủ các quy tắc viết tắt dưới đây.

---

## §1 File Category Tags

Every .md file in agent/knowledge system MUST declare tag in frontmatter:

| Tag | Meaning | Conversion |
|-----|---------|------------|
| `@AI-ONLY` | Only agent reads | Full Structured NL — compress all prose |
| `@HYBRID` | Agent instructions + user-facing output | Instructions → Structured NL, output templates → keep NL |
| `@HUMAN` | User reads directly | Keep full NL — no conversion |

---

## §2 Action Verbs (camelCase)

Agent understands these from code training data — use instead of NL phrases.

| Verb | Replaces | Example |
|------|----------|---------|
| `askUser` | "hỏi người dùng", "ask user for confirmation" | `if ambiguous → askUser("clarify X?")` |
| `scanDir` | "scan/list the directory" | `scanDir(${ROOT}/modules/)` |
| `readFile` | "read and parse file" | `readFile(SKILL.md)` |
| `grepFor` | "search for pattern in files" | `grepFor("IScoped", ${ROOT}/src/)` |
| `writeOutput` | "generate/write output file" | `writeOutput("srs.md", changeDir)` |
| `validate` | "check/verify convention compliance" | `validate(entity, [E1..E10])` |
| `mapTo` | "convert/transform/map to" | `Entity.mapTo(DTO)` |
| `loadCtx` | "load context files into memory" | `loadCtx(knowledge_*.md)` |
| `assertRule` | "assert/enforce rule compliance" | `assertRule(E8, base == ApprovableEntity)` |
| `skipIf` | "skip/bypass if condition" | `skipIf(--frontend not set)` |
| `haltIf` | "stop immediately if condition" | `haltIf(required_rule.notFound)` |
| `yieldToUser` | "return control to user, present output" | `yieldToUser(summary)` |
| `dispatch` | "invoke skill/workflow" | `dispatch(skill: "learn-architecture")` |
| `checkExists` | "verify file/dir exists" | `checkExists(srs.md)` |
| `countTokens` | "measure token usage" | `countTokens(before) vs countTokens(after)` |
| `logWarn` | "warn but continue" | `logWarn("directory empty, proceeding")` |
| `logError` | "log error" | `logError("required file missing")` |

---

## §3 Common Abbreviations

| Short | Full | Context |
|-------|------|---------|
| `req` | Request | DTO naming: `CreateBannerReq` |
| `res` | Response | DTO naming: `BannerRes` |
| `cfg` | Config | Configuration class: `AppCfg` |
| `ctx` | Context | Loaded context: `loadCtx(...)` |
| `auth` | Authorization | Permission/auth rules |
| `APV` | Approval | Approval workflow |
| `FK` | Foreign Key | Entity relationships |
| `PK` | Primary Key | Entity key |
| `NL` | Natural Language | Human-readable text |
| `BE` | Backend | .NET/C# scope |
| `FE` | Frontend | Angular/TS scope |
| `DI` | Dependency Injection | Service registration |
| `CRUD` | Create/Read/Update/Delete | Standard operations |
| `RPT` | Report | Report pattern |
| `FSM` | Finite State Machine | Approval state pattern |
| `SRS` | Software Requirement Spec | Business document |
| `DDL` | Data Definition Language | CREATE TABLE, ALTER, etc. |
| `dto` | Data Transfer Object | Request/Response models |
| `svc` | Service | Service layer |
| `ctrl` | Controller | API controller |
| `impl` | Implementation | Concrete class |
| `nav` | Navigation | Entity navigation property |
| `prop` | Property | Class property |

---

## §4 Operators (Code-style)

| Symbol | Meaning | Example |
|--------|---------|---------|
| `→` | Then / leads to / calls | `Controller → Service → Repository` |
| `←` | Returns / comes from | `Response ← Service.Search()` |
| `↔` | Bidirectional / maps both ways | `Entity ↔ DTO (via Mapper)` |
| `&&` | AND (both required) | `PascalCase && suffix("Entity")` |
| `\|\|` | OR (either acceptable) | `BaseFieldEntity \|\| BaseBoEntity` |
| `!` | NOT / forbidden | `!plural`, `!scan(all)` |
| `==` | Equals / must be exactly | `namespace == "BOBase.Domain"` |
| `!=` | Not equals / must not be | `output != placeholder` |
| `=>` | Implies / when...then | `has(APV) => inherit(BaseFieldApprovableEntity)` |
| `?` | Optional / conditional | `DateTime? ConfirmedDate` |
| `...` | et cetera / and more | `audit_fields: CreatedDate, ModifiedDate, ...` |

---

## §4.1 Spec State Transition Symbols (Pure CoS v2)

> Used ONLY in `specs/**/*.md` files for behavioral state machine notation.

### SC Line Format
```
SC{N}: [state_before] →(action) [state_after] | side_effects
```

### Symbol Dictionary

| Symbol | Meaning | Example |
|--------|---------|---------|
| `[...]` | State block (current state) | `[Active]`, `[cache:loaded]`, `[filter:Code="X"]` |
| `[⊘]` | Null/empty state (before creation) | `[⊘] →(save valid) [CFG:Active]` |
| `[X:∅]` | Empty collection/cache | `[list:∅]`, `[cache:∅]` |
| `✗` | Blocked/refused (validation fail) | `[⊘] →(save Code∈DB) ✗` |
| `→(action)` | Trigger with action | `→(save valid)`, `→(Khóa → confirm:OK)` |
| `\|` | Side effect separator | `[Active] →(Khóa) [Inactive] \| msg:"..."` |
| `∋` | Contains (filter match) | `[list:match∋"PROMO"]` |
| `∉` | Does not match pattern | `→(save Code∉regex) ✗` |
| `∈DB` | Exists in database | `→(save Code∈DB) ✗` |
| `↑` / `↓` | Sort ASC / DESC | `sort:Code↑` |
| `∨` | OR (action alternatives) | `→(click:Khóa∨Mở_khóa)` |
| `confirm:OK` / `confirm:Cancel` | User confirmation result | `→(Khóa → confirm:OK)` |

### State Naming Conventions
- Entity state: `[Active]`, `[Inactive]`, `[CFG:Active]`
- UI screen: `[listScreen]`, `[createForm]`, `[updateForm]`
- UI sub-state: `[screen:init]`, `[form:Code=readonly]`
- Collection: `[list:all]`, `[list:∅]`, `[filter:Code="X"]`
- System: `[cache:loaded]`, `[cache:∅]`

---

## §5 Severity & Status Icons

| Icon | Meaning | Usage |
|------|---------|-------|
| 🔴 | CRITICAL — must fix | Convention violations that break system |
| 🟠 | WARNING — should fix | Convention drift, suboptimal patterns |
| 🟡 | INFO — nice to have | Style suggestions |
| ✅ | PASS / correct | Scan results, verification |
| ❌ | FAIL / violation | Scan results, anti-patterns |
| 🔴GATE | Mandatory stop point | Pipeline flow control |

---

## §6 Scan Rule Format

Convention checker rules must follow this format:

```
[RULE_ID] SEVERITY  rule_description_in_shorthand
```

Example:
```
[E1] 🔴  className: PascalCase && suffix("Entity")
[E2] 🔴  className: singular only — !plural
[E3] 🟠  prefix ↔ table: Ad→AD_, Omni→OMNI_, Bo→BO_
[E8] 🔴  has(APV) => base == BaseFieldApprovableEntity
```

---

## §7 Step/Flow Format

Workflow and skill steps — use numbered shorthand:

```
§1 Step Name
  action_verb(args) → expected_result
  if condition → consequence

§2 Next Step  
  depends_on: §1.output
  action_verb(args) → expected_result
```

Example:
```
§1 Find Entry Points
  scanDir(${ROOT}) → find("*.sln", "*.csproj")
  determine: core_layers, feature_modules, api_entry

§2 Trace Request Flow
  depends_on: §1.projects
  grepFor("class BaseController", ${ROOT})
  readFile(BaseController.cs) → document: base_class, Response(), filter_attrs
```

---

## §8 Conversion Rules

### @AI-ONLY files — full conversion:
1. Remove all NL prose paragraphs → replace with structured bullets
2. Tables: keep but compress wording
3. Code blocks: **keep 100% unchanged** — never modify code templates
4. Examples: keep but compress NL explanation around them
5. Frontmatter: add `tag: "@AI-ONLY"`, keep existing fields

### @HYBRID files — partial conversion:
1. Agent instruction sections → convert to Structured NL
2. Output format/template sections → keep full NL (user reads these)
3. Guardrails → convert to `!` / `→` shorthand
4. Mark boundary clearly: `<!-- OUTPUT FORMAT — keep NL below -->`

### @HUMAN files — no conversion:
1. No changes — these are for human consumption
2. Only add `tag: "@HUMAN"` to frontmatter if missing

---

## §9 Anti-patterns

```
! mix NL prose with shorthand in same sentence
! invent new abbreviations not listed in §3
! use math symbols (∀, ∃, ⇒) — use code-style instead (except §4.1 spec symbols: ⊘, ∋, ∉, ∨, ∈)
! convert code blocks or code templates to shorthand
! remove context that helps agent understand WHY a rule exists
! break existing frontmatter fields when adding tag
```
