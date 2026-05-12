---
name: tdd-workflow
when_to_use: Test-Driven Development — RED-GREEN-REFACTOR cycle, AAA pattern.
paths: [base_knowledge/standards/base/tdd-workflow/]
---

# TDD Workflow

> Write tests first, code second.

## Cycle
🔴 RED (failing test) → 🟢 GREEN (minimal code to pass) → 🔵 REFACTOR (improve quality) → Repeat

## Three Laws
1. Production code only to make failing test pass
2. Only enough test to demonstrate failure
3. Only enough code to make test pass

## Phase Rules
- **RED**: test MUST fail first, name describes behavior, one assertion
- **GREEN**: YAGNI, simplest thing, no optimization
- **REFACTOR**: all tests stay green, small incremental, commit after each

## AAA Pattern
Arrange (setup) → Act (execute) → Assert (verify)

## When to TDD
High value: new feature, bug fix, complex logic | Low value: exploratory, UI layout

## Priority
1. Happy path → 2. Error cases → 3. Edge cases → 4. Performance

## Anti-Patterns
❌ Skip RED phase | ❌ Tests after code | ❌ Over-engineer initial
❌ Multiple asserts | ❌ Test implementation (test behavior instead)
