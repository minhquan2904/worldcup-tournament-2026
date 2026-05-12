---
name: init
description: Initialize new feature — scaffold change directory, generate metadata.yaml and proposal.md.
arguments: ["${change_name}"]
allowed-tools: [Read, Write, Grep, Glob, Bash]
context: inline
version: 4.0
---

# Init Feature

Output: metadata.yaml + proposal.md in openspec/changes/<name>/
Input: Feature name (kebab-case). srs.md must exist (from /srs).

## §1 Verify
openspec/changes/<name>/srs.md exists → if not, notify /srs first

## §2 Read srs.md
Feature scope, actors, business context, FR-xxx, use cases, business rules, authorization, quality scoring
!call Confluence/Jira MCP — all content already in srs.md

## §3 Scaffold
`openspec new change "<name>"`

## §4 Generate metadata.yaml
```yaml
id: "UPPERCASE(rootProject)+YYMMDD+5random"
name: "<name>"
type: "new-feature"
created: "ISO timestamp +07:00"
summary: "Vietnamese summary"
service: []
path: []
confluence: []
jira: []
schema: []
```

## §5 Load Context
artifact_context_modular.yml → section proposal → read knowledge files

## §6 Feature Profile
Lock:
- Mode: LIST | DETAIL | FORM | DASHBOARD
- State: Jotai atoms (global) | useState (local) | mixed
- Data: API service | static | ZMP SDK
- Type: NEWBUILD | MAINTENANCE
Show locked profile.

## §7 Generate proposal.md — Structured NL Format
`openspec instructions proposal --change "<name>" --json`
Fill template with srs.md + Feature Profile + knowledge

Output format: **Structured NL** (AI-optimized, human-reviewable)
- Why: 2-3 lines max | What Changes: numbered 1-liners | Capabilities: `name`: 1-line
- Impact: bullet list (Routes/Components/State/API/Config) | Feature Profile: code block
- !verbose prose | !paragraphs | use tables where >3 items

## Guardrails
- MUST verify srs.md exists
- !call Confluence/Jira MCP
- MUST generate metadata.yaml BEFORE proposal.md
- context/rules from openspec = constraints, !copy into output
