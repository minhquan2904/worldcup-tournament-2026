---
name: learn-react-hook-helper
description: Learn React custom hooks & helpers — custom hooks, utility functions, formatters, validators, data transformations
tag: "@AI-ONLY"
allowed-tools: [Read, Write, Grep, Glob]
context: fork
version: 4.0
---

# Learn React Custom Hooks & Helpers

> Output: `knowledge_react_hook_helper.md` → PROPOSE_DIR
> Consolidates Angular directive + helper + pipe equivalents into React patterns

## §1 Custom Hooks
- scan `src/hooks/` (if exist)
- grepFor(`function use`, `src/`) → catalog ALL custom hooks
- for each hook:
  - name, parameters, return value
  - internal hooks used (useState, useEffect, useRef, useMemo, useCallback)
  - cleanup logic (useEffect return)
  - dependencies array analysis

## §2 Helper Functions
- scan `src/utils/` || `src/helpers/` (if exist)
- for each: function name, parameters, return type, purpose
- categorize: format, validate, transform, calculate

## §3 Format Utilities (replaces Angular pipes)
- scan for formatting functions: number, currency, date, string
- pattern: pure functions (input → formatted output)
- i18n: `toLocaleString("vi-VN", ...)` patterns
- example from source: Clock component uses `Date.toLocaleString("vi-VN", {...})`

## §4 Validation Helpers (replaces Angular CustomValidatorService)
- scan for validation functions
- patterns: form validation, input masks, regex validators
- integration: React Hook Form validators || custom validation

## §5 Data Transformation Helpers (replaces Angular directives)
- scan for data manipulation utilities
- patterns: array sort/filter, object mapping, type guards
- TypeScript utility types usage

## §6 Template — Custom Hook
```typescript
// hooks/useFeature.ts
import { useState, useEffect, useCallback } from "react";

interface UseFeatureOptions {
  initialValue?: string;
}

export function useFeature(options?: UseFeatureOptions) {
  const [value, setValue] = useState(options?.initialValue ?? "");
  const [loading, setLoading] = useState(false);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      // fetch data
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
    return () => {
      // cleanup
    };
  }, [refresh]);

  return { value, loading, refresh };
}
```

```typescript
// utils/format.ts
export const formatCurrency = (amount: number): string =>
  amount.toLocaleString("vi-VN", { style: "currency", currency: "VND" });

export const formatDate = (date: Date): string =>
  date.toLocaleString("vi-VN", {
    hour: "2-digit",
    minute: "2-digit",
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
```

## §7 Write Output — Structured NL Format
Output format: **Structured NL** (@AI-ONLY, pipeline context)
- Tables for structured data (hook inventory, helper catalog, formatter list)
- Code blocks: keep 100% unchanged (real samples, templates)
- !verbose prose | bullets + shorthand | use cos_convention.md operators

## Guardrails
- !Angular directive patterns — use custom hooks for reusable behavior
- !Angular pipe patterns — use pure format functions
- Custom hooks: MUST start with `use` prefix
- Hooks Rules: !call in loops, !call in conditions, !call in nested functions
- Pure functions for formatters — !side effects in formatters
- xref: react_component, react_util
