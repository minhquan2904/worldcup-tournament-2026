# Standards Catalog

```
standards/
├── base/                        # Tech-agnostic (any project)
│   └── <skill>/SKILL.md
├── <skill>/                     # Project-level domain-specific
│   └── <extension>.md
└── _standards-catalog.md
```

## Project-Level Skills

| Folder | Type | xref |
|--------|------|------|
| api-patterns/ | Override | REST API (extends base/) |
| fixbug/ | Override | Debug (extends base/) |

## Base Skills (Tech-agnostic)

| Folder | Type | Description |
|--------|------|-------------|
| clean-code/ | Methodology | SRP, DRY, KISS, YAGNI, naming |
| code-review-checklist/ | Methodology | Correctness, security, perf |
| tdd-workflow/ | Methodology | RED-GREEN-REFACTOR, AAA |
| testing-patterns/ | Dev Practice | Testing pyramid, AAA, mocking |
| security-compliance-checker/ | Dev Practice | OWASP scan rules |
| api-patterns/ | Dev Practice | REST design, response |
| database-design/ | Knowledge | Schema, normalization |
| requirement-analysis/ | Knowledge | BA requirement analysis |

> Note: Project uses React 18 / TypeScript / Vite / Jotai / ZMP SDK / ZMP UI / Tailwind CSS.
> Angular/dotnet/Oracle-specific standards removed — not applicable.
