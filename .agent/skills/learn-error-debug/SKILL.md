---
name: learn-error-debug
description: Learn Error Handling & Debugging — React error boundaries, console debugging, Zalo DevTools, common errors, Vite troubleshooting
tag: "@AI-ONLY"
allowed-tools: [Read, Write, Grep, Glob]
context: fork
version: 4.0
---

# Learn Error Handling & Debugging

> Output: `knowledge_error_debug.md` → APPLY_DIR

## §1 React Error Boundaries
- scan for ErrorBoundary components in `src/`
- pattern: class component with `componentDidCatch` + `getDerivedStateFromError`
- fallback UI: what shows when error caught
- if !exist → document recommendation pattern:
```tsx
class ErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback?: React.ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error("ErrorBoundary caught:", error, info);
  }
  render() {
    if (this.state.hasError) return this.props.fallback ?? <div>Something went wrong</div>;
    return this.props.children;
  }
}
```

## §2 Error Handling Patterns
- scan for `try/catch` blocks across `src/`
- scan for `.catch()` on promises
- scan for error state: `useState<Error | null>(null)`
- patterns:
  - API errors: fetch → check `res.ok` → throw
  - ZMP SDK errors: callback error params
  - Form validation errors: inline error messages

## §3 Console & DevTools Debugging
- `console.log/warn/error` usage patterns
- Vite HMR (Hot Module Replacement) error overlay
- React DevTools: component tree, hooks inspector
- Zalo DevTools: mini app testing environment

## §4 Common Errors & Solutions

| Error | Cause | Fix |
|-------|-------|-----|
| `Invalid hook call` | Hook called outside component/custom hook | Move hook to component body top-level |
| `Objects are not valid as a React child` | Rendering object instead of string/JSX | Use `.toString()` or extract property |
| `Cannot read property of undefined` | Missing null check on async data | Optional chaining `?.` or loading guard |
| `Module not found` | Wrong import path or missing dep | Check `@/` alias, run `npm install` |
| `zmp-sdk not available` | Running outside Zalo environment | Use `getSystemInfo()` with try/catch |
| `CORS error` | API call from dev server | Configure Vite proxy or use ZMP backend |
| `Tailwind classes not applied` | File not in purge content paths | Check `tailwind.config.js` content array |
| `Dark mode not working` | Wrong dark mode selector | Use `[zaui-theme="dark"]` selector |

## §5 Vite Dev Server Troubleshooting
- port conflicts: `zmp start` default port
- HMR failures: clear `.vite` cache, restart dev server
- build errors: TypeScript strict mode violations
- asset loading: `assetsInlineLimit: 0` in vite.config
- path alias: `@/` → `./src/` in both tsconfig + vite.config

## §6 Write Output — Structured NL Format
Output format: **Structured NL** (@AI-ONLY, pipeline context)
- Tables for structured data (error types, solutions)
- Code blocks: keep 100% unchanged (real samples, templates)
- !verbose prose | bullets + shorthand | use cos_convention.md operators
- ALL class names = REAL from source — !placeholders

## Self-Verify
- [ ] Error boundary pattern documented
- [ ] API error handling patterns
- [ ] Common React errors table
- [ ] ZMP SDK error handling
- [ ] Vite troubleshooting guide
- [ ] Debugging tools listed

## Guardrails
- !.NET exception patterns (BadRequestException, etc.)
- !Angular ErrorHandler — use React ErrorBoundary
- !swallow errors silently — always log + show user feedback
- ErrorBoundary component: MUST exist in project — scan verified: MISSING 🔴 → create as first priority
- ZMP SDK error handling: ALL calls require try/catch — scan verified: partial 🟠
- xref: react_architecture, zmp_sdk
