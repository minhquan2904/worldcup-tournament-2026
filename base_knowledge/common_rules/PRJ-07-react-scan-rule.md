---
description: React/TypeScript Source Code Scan Rules
tag: "@AI-ONLY"
updated: "2026-04-16"
---

# React/TypeScript Scan Rules

## §1 Scan Scope

### IN SCOPE:
| Directory | Content | Priority |
|-----------|---------|----------|
| `src/pages/` | Page components (route-level) | 🔴 |
| `src/components/` | Shared/reusable components | 🔴 |
| `src/hooks.ts` | Custom React hooks | 🔴 |
| `src/state.ts` | Jotai atom definitions | 🔴 |
| `src/router.tsx` | Route configuration | 🔴 |
| `src/utils/` | Utility/helper functions | 🟠 |
| `src/types.d.ts` | TypeScript type definitions | 🟠 |
| `src/global.d.ts` | Window augmentation types | 🟠 |
| `src/css/` | Stylesheets (SCSS + Tailwind) | 🟡 |

- files: `.ts`, `.tsx`, `.scss`
- !scan: `node_modules/`, `dist/`, `.git/`, `.agent/`, `base_knowledge/`
- out_of_scope: `*.json`, `*.config.js`, `*.config.mts`, `*.svg`, generated code

## §2 Convention Baseline

### Component Convention
| # | Rule | Severity | Scan Status |
|---|------|----------|-------------|
| RC1 | Function components ONLY — !class components | 🔴 | ✅ verified |
| RC2 | Default export for page + layout components | 🔴 | ✅ verified |
| RC3 | Named export for shared UI components (`export const Button`, `export function ErrorBoundary`) | 🔴 | ✅ verified |
| RC4 | TypeScript interfaces for ALL props — !`any` (except `APP_CONFIG: any` known exception) | 🔴 | 🟠 `APP_CONFIG: any` |
| RC5 | Hooks at top-level ONLY — !conditional hooks | 🔴 | ✅ verified |
| RC6 | useEffect cleanup for subscriptions/timers (ResizeObserver) | 🟠 | ✅ verified (hooks.ts) |
| RC7 | Suspense MUST wrap all async atom reads via Outlet | 🔴 | ✅ verified (page.tsx) |

### State Management Convention
| # | Rule | Severity | Scan Status |
|---|------|----------|-------------|
| RS1 | Jotai atoms in `src/state.ts` — !Redux, !Context API, !Zustand | 🔴 | ✅ verified |
| RS2 | useState for component-local state | 🔴 | ✅ verified |
| RS3 | `atomFamily` for parametric state (by ID) | 🟠 | ✅ verified |
| RS4 | `loadable` for non-critical async (no crash on error) | 🟠 | ✅ verified (searchResultState) |
| RS5 | `atomWithReset` for form atoms | 🟠 | ✅ verified |
| RS6 | `atomWithRefresh` for re-fetchable SDK data | 🟠 | ✅ verified (userState) |
| RS7 | !prop drilling > 2 levels — use atoms | 🟠 | N/A |
| RS8 | No `<Provider>` needed — Jotai 2.x providerless mode | 🟡 | ✅ verified |

### Routing Convention
| # | Rule | Severity | Scan Status |
|---|------|----------|-------------|
| RR1 | Use `createBrowserRouter` from `react-router-dom` — !MemoryRouter, !HashRouter, !ZMPRouter | 🔴 | ✅ verified |
| RR2 | Route config in `src/router.tsx` ONLY — !inline route definitions | 🔴 | ✅ verified |
| RR3 | `basename = getBasePath()` — dynamic per environment | 🔴 | ✅ verified |
| RR4 | Route metadata via `handle` object — `{ back, title, noScroll, profile }` | 🟠 | ✅ verified |
| RR5 | Navigation via `useNavigate()` from react-router-dom — !`window.location.href`, !`ZMPRouter.navigate` | 🔴 | ✅ verified |
| RR6 | `ErrorBoundary` MUST be set on root route — `route.ErrorBoundary = ErrorBoundary` | 🔴 | ✅ verified |
| RR7 | Lazy loading for feature pages (future) | 🟡 | Not yet implemented |
| RR8 | `TransitionLink` (NavLink + viewTransition) for tab nav | 🟡 | ✅ verified |

### Styling Convention
| # | Rule | Severity | Scan Status |
|---|------|----------|-------------|
| RT1 | Tailwind CSS classes for styling — !inline style objects (except dynamic values like `filter:`) | 🟠 | 🟠 dynamic filter in footer.tsx (acceptable) |
| RT2 | CSS vars from `zaui.min.css` + Tailwind config for theming — !ZMP UI `getSystemInfo()` | 🟠 | ✅ verified |
| RT3 | SCSS for complex/custom global styles only | 🟡 | ✅ |
| RT4 | !CSS modules — use Tailwind | 🟡 | ✅ verified |

### Naming Convention
| # | Rule | Severity |
|---|------|----------|
| RN1 | Components: PascalCase (FileName.tsx + export name) | 🔴 |
| RN2 | Hooks: `use` prefix (useRouteHandle, useRealHeight) | 🔴 |
| RN3 | Utils: camelCase functions | 🟠 |
| RN4 | Types/Interfaces: PascalCase with descriptive names | 🟠 |
| RN5 | Constants: UPPER_SNAKE_CASE for true constants | 🟡 |
| RN6 | Atoms: `camelCase + State` suffix (servicesState, userState) | 🟠 |
| RN7 | Pages: `index.tsx` per folder, or descriptive name (`404.tsx`, `history.tsx`) | 🟠 |

### ZMP SDK Convention
| # | Rule | Severity | Scan Status |
|---|------|----------|-------------|
| RZ1 | ZMP SDK calls: MUST have try/catch or .catch() | 🔴 | ✅ verified (userState) |
| RZ2 | Use `NotifiableError` for user-facing SDK errors | 🟠 | ✅ verified |
| RZ3 | !hardcode appId — use `window.APP_ID` | 🔴 | ✅ verified (router.tsx getBasePath) |
| RZ4 | !import routing/shell from `zmp-ui` (`App`, `ZMPRouter`, `AnimationRoutes`, `SnackbarProvider`, `Page`) | 🔴 | ✅ verified (removed) |
| RZ5 | Toast via `react-hot-toast` — !ZMP UI SnackbarProvider | 🔴 | ✅ verified |

### Error Handling Convention
| # | Rule | Severity | Scan Status |
|---|------|----------|-------------|
| RE1 | Route-level ErrorBoundary using `useRouteError()` (functional, NOT class) | 🔴 | ✅ verified |
| RE2 | `NotifiableError` class for user-visible error messages | 🟠 | ✅ verified |
| RE3 | `loadable()` for non-critical async — prevents ErrorBoundary cascade | 🟠 | ✅ verified |
| RE4 | `console.warn` for unexpected errors — !`console.error` alone | 🟡 | ✅ verified |
| RE5 | 404 page navigates back + shows toast — !stays on 404 | 🟡 | ✅ verified |

## §3 Severity

| Level | Icon | Description |
|-------|------|-------------|
| CRITICAL | 🔴 | runtime error \|\| data integrity — missing types, broken routing, hook violations |
| WARNING | 🟠 | clear violation, no crash — naming, missing optimization, wrong pattern |
| INFO | 🟡 | minor \|\| recommendation — style preference, optional optimization |
| PASS | ✅ | fully compliant |

## §4 Output Format
- Per-Component/File summary table
- Per-File detail: `| # | Check | Status | Detail | Rule |`
- Overall summary + Mermaid pie chart

## §5 Behavioral Rules

| # | Rule | Description |
|---|------|-------------|
| R1 | READ-ONLY | !modify source — read && report only |
| R2 | EXHAUSTIVE | scan ALL files in scope — !skip |
| R3 | TRACEABLE | each finding MUST ref convention rule ID |
| R4 | STRUCTURED | output per §4 format |
| R5 | NO FALSE POSITIVES | verify Expected vs Actual |
| R6 | PRIORITIZED | order: CRITICAL → WARNING → INFO |

## §6 Anti-Patterns — CRITICAL
- !`import { ZMPRouter, AnimationRoutes } from "zmp-ui"` — removed
- !`import { useNavigate } from "zmp-ui"` — use react-router-dom
- !`import { App, SnackbarProvider } from "zmp-ui"` in layout — removed
- !`getSystemInfo()` for theme — Tailwind CSS vars handle theming
- !class-based ErrorBoundary — use React Router `useRouteError()` functional pattern
- !`window.location.href = "..."` for navigation — use `useNavigate()`
- !hardcode `APP_ID` or route basenames — use `getBasePath()`
