---
name: preprocess
description: Pre-process URD into structured raw extraction ready for SRS generation.
arguments: []
allowed-tools: [Read, Write, Grep, Glob, Bash, MCP]
context: inline
version: 3.0
---

# Preprocess URD

Output: pre_process.md in openspec/changes/<feature>/
Language: Vietnamese (except IDs + technical terms)

## §1 ⛔ MANDATORY COMPLIANCE
artifact_context_modular.yml → section preprocess → load required_rules + required_skills

## §2 Identify URD Source + Feature Name + Scaffold

### Source Detection
| Source | How |
|--------|-----|
| Confluence (--confluence or URL detected) | MCP get_page |
| Jira (--confluence or key detected) | MCP get_issue |
| SRS document | read directly |
| Plain text/file | read directly |
| External URL | read_url_content |

MCP RULE: only when --confluence flag OR auto-detected URL/key pattern

### Classify Feature Type
Signal 1: grep features.md for keywords → candidate MAINTENANCE
Signal 2: grep module/ for related handlers → confirmed MAINTENANCE
Decision: match+code=MAINTENANCE, match+!code=NEWBUILD, !match=NEWBUILD
Fallback: if !features.md → warn + default NEWBUILD

### Scaffold
`openspec new change "<name>"`

## §3 Extract Raw Data (!interpretation)
Feature name, Actors, Raw requirements (use case flows, business rules), Integrations
- !infer missing logic, !rewrite meaning
- preserve ~~strikethrough~~ as deprecated

## §4 Normalize → Structured FR
Actor → Action → Object → Condition → Result
→ Vietnamese: "Hệ thống phải <action> khi <condition>."
Assign FR-001..N, short Vietnamese title, split compounds, extract validations
- !enrich with banking domain (that's /srs)
- !score quality (that's /srs)

## §5 Detect Obvious Issues (surface only)
Conflict (different values), Missing (referenced but undefined), Ambiguity (vague words)
!flag missing banking domain requirements

## §6 Finalize Output — CoS Format
Output format: **Chain of Symbol (CoS)**

### Structure:
```
## Symbols
- **ND**: Actor description (mapped from URD actors)
- **BO**: System/BackOffice
- **<ENTITY>**: Domain entity abbreviation

## FR (Functional Requirements)
FR-001: ND → BO.action(params) | constraint1 | constraint2
FR-002: BO.validate → condition → msg("message") | alt_condition → alt_result

## NFR / Constraints / Integrations / Assumptions / Resolved Questions / Deprecated
```

### CoS Rules:
- Actors from URD → Symbols (2-4 char abbreviation)
- Each FR = one symbol chain: `Actor → System.action(params) | constraints | results`
- Validation flows: `BO.validate → condition → msg("...")`
- Use `|` for alternative branches, `→` for flow, `!` for negation
- Open Questions resolved inline: `OQ-001: question ===> Resolve: answer`

## Guardrails
- !generate code, !invent business logic
- !remove original intent, !discard conflicts silently
- ~~strikethrough~~ → Deprecated Items (!active FRs)
- !enrich with banking domain — /srs responsibility
- !score quality — /srs responsibility
