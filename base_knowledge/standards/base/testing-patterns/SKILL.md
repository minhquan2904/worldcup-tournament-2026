---
name: testing-patterns
when_to_use: Testing patterns — unit, integration, mocking for .NET/C#, Angular, and Java/Spring.
paths: [base_knowledge/standards/base/testing-patterns/]
---

# Testing Patterns

## Testing Pyramid
Unit (many, fast) → Integration (some, medium) → E2E (few, slow)

## AAA Pattern
Arrange (setup) → Act (execute) → Assert (verify)

## Test Type Selection
| Type | Best For | Tools |
|------|----------|-------|
| Unit | Service logic, validators | xUnit+Moq / Jasmine+Karma |
| Integration | API endpoints, repository | @SpringBootTest, TestRestTemplate |
| E2E | Critical user flows | Selenium, Cypress |

## FIRST Principles
Fast (<100ms) | Isolated (!external deps) | Repeatable (same result) | Self-checking (!manual verify) | Timely (with code)

## What to Test vs Skip
✅ Business logic, edge cases, error handling, validation
❌ Framework internals, getters/setters, third-party libs

## Mocking Rules
✅ Mock: Repository, external APIs, Clock, message queues
❌ !Mock: service under test, simple domain objects, pure utils

## Mock Types (cross-framework)
| Type | Java (Mockito) | .NET (Moq) | Angular (Jasmine) |
|------|----------------|------------|-------------------|
| Stub | when().thenReturn() | Setup().Returns() | spy.and.returnValue() |
| Verify | verify(mock).method() | mock.Verify() | expect(spy).toHaveBeenCalled() |

## Naming Convention
`methodName_StateUnderTest_ExpectedBehavior` or `should_Expected_When_State`

## Anti-Patterns
❌ Test implementation → test behavior | ❌ Duplicate setup → @BeforeEach
❌ Tests after code → TDD | ❌ Ignore flaky → fix root cause | ❌ Skip cleanup → @AfterEach
