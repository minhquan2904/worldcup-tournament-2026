---
description: Logging Rules — React/Zalo Mini App
tag: "@AI-ONLY"
---

# Logging Standards

## §1 Framework
`console` — browser built-in (dev) + ZMP DevTools (production debugging)

## §2 Log Levels

### console.error() — errors requiring handling
| When | Pattern |
|------|---------|
| exception in catch | `console.error("[ComponentName] failed:", error)` |
| API call failure | `console.error("[ServiceName] API error:", status, response)` |
| ZMP SDK error | `console.error("[ZMP] SDK call failed:", error)` |

### console.warn() — attention needed
| When | Pattern |
|------|---------|
| fallback to default | `console.warn("[Config] not found, using default:", key)` |
| deprecated usage | `console.warn("[Deprecation] useOldHook → useNewHook")` |
| missing optional data | `console.warn("[Feature] optional data missing:", field)` |

### console.log() — dev-only flow tracking
| When | Pattern |
|------|---------|
| debug flow | `console.log("[Feature] state changed:", newState)` |
| component lifecycle | `console.log("[Component] mounted with props:", props)` |

> ⚠️ console.log() SHOULD be removed before production deploy

## §3 Context Rules
- component: `[ComponentName]` prefix for all logs
- hook: `[useHookName]` prefix
- service: `[ServiceName]` prefix
- atom: `[AtomName]` prefix for async atom errors

## §4 Forbidden Patterns

| ❌ Forbidden | Reason |
|-------------|--------|
| log(PIN, password, token, OTP) | data leak — client-side logs visible |
| `alert()` / `confirm()` | use ZMP UI SnackbarProvider |
| empty catch blocks | always log error |
| console.log in production code | use console.error/warn for real issues, remove console.log |
| log entire objects without filtering | sensitive fields exposure |
| log inside render/return | performance + infinite re-render risk |
