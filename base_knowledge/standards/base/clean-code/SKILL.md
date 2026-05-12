---
name: clean-code
when_to_use: Pragmatic coding standards — concise, direct, no over-engineering.
paths: [base_knowledge/standards/base/clean-code/]
---

# Clean Code — Pragmatic AI Coding Standards

## Core Principles
SRP (one thing) | DRY (no repeat) | KISS (simplest) | YAGNI (!unused features) | Boy Scout (leave cleaner)

## Naming
| Element | Convention |
|---------|-----------|
| Variables | Reveal intent: `userCount` !`n` |
| Functions | Verb+noun: `getUserById()` !`user()` |
| Booleans | Question: `isActive`, `hasPermission` |
| Constants | SCREAMING_SNAKE: `MAX_RETRY_COUNT` |

## Functions
Max 20 lines (ideal 5-10) | One thing | One abstraction level | Max 3 args | No side effects

## Structure
Guard clauses (early return) | Flat > nested (max 2 levels) | Composition | Colocation

## Anti-Patterns
❌ Comment every line → delete obvious comments
❌ Helper for one-liner → inline
❌ Deep nesting → guard clauses
❌ Magic numbers → named constants
❌ God functions → split by responsibility

## Before Editing ANY File
1. What imports this? (may break) | 2. What does this import? (interface changes)
3. What tests cover this? | 4. Is shared component? (multiple places)
> 🔴 Edit file + ALL dependent files in SAME task. Never leave broken imports.

## Self-Check (MANDATORY)
✅ Goal met? | ✅ All files edited? | ✅ Code works? | ✅ Conventions? | ✅ Nothing forgotten?
