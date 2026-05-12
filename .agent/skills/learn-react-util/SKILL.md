---
name: learn-react-util
description: Learn React utility services — ZMP SDK helpers, storage, navigation, loading patterns, environment config
tag: "@AI-ONLY"
allowed-tools: [Read, Write, Grep, Glob]
context: fork
version: 4.0
---

# Learn React Utility Services

> Output: `knowledge_react_util.md` → PROPOSE_DIR

## §1 Storage Utilities
- scan for localStorage/sessionStorage usage
- scan for Jotai `atomWithStorage` patterns
- scan `window.APP_CONFIG` usage → runtime config access
- pattern: get/set/remove with JSON serialization

## §2 Navigation Utilities
- scan for `useNavigate` || ZMP navigation functions
- scan for programmatic route changes
- scan for route parameter extraction
- ZMP-specific: `openMiniApp()`, `openChat()`, etc.

## §3 Loading & Error UI
- scan for loading state patterns: `useState(false)` + `setLoading(true/false)`
- scan for error boundary components
- scan for skeleton/placeholder UI
- ZMP UI: SnackbarProvider usage for notifications

## §4 Environment & Config
- `app-config.json` → `window.APP_CONFIG` flow
- `import.meta.env` → Vite env variables
- scan for `.env` file → environment-specific config
- scan for conditional logic based on environment

## §5 Platform Utilities
- `getSystemInfo()` from `zmp-sdk` → device info, theme, platform
- dark mode detection: `getSystemInfo().zaloTheme`
- viewport/safe area handling
- device-specific adjustments

## §6 Template — Utility Pattern
```typescript
// utils/storage.ts
const STORAGE_PREFIX = "pls_";

export const storage = {
  get: <T>(key: string): T | null => {
    try {
      const item = localStorage.getItem(`${STORAGE_PREFIX}${key}`);
      return item ? JSON.parse(item) : null;
    } catch {
      return null;
    }
  },
  set: <T>(key: string, value: T): void => {
    localStorage.setItem(`${STORAGE_PREFIX}${key}`, JSON.stringify(value));
  },
  remove: (key: string): void => {
    localStorage.removeItem(`${STORAGE_PREFIX}${key}`);
  },
};
```

```typescript
// utils/config.ts
export const getAppConfig = () =>
  (window as any).APP_CONFIG as {
    app: { title: string; textColor: Record<string, string> };
  };
```

## §7 Write Output — Structured NL Format
Output format: **Structured NL** (@AI-ONLY, pipeline context)
- Tables for structured data (utility inventory, config keys, storage keys)
- Code blocks: keep 100% unchanged (real samples, templates)
- !verbose prose | bullets + shorthand | use cos_convention.md operators

## Guardrails
- !Angular utility service patterns (providedIn: 'root', injectable)
- !browser confirm()/alert() — use ZMP UI SnackbarProvider or custom dialog
- storage: always JSON serialize/deserialize — !raw string storage
- config: access via `window.APP_CONFIG` or `import.meta.env` — !hardcode values
- xref: react_component, zmp_sdk
