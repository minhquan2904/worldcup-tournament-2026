---
title: React Utility Knowledge
tag: "@AI-ONLY"
generated: "2026-04-16"
source_skill: learn-react-util
---

# React Utilities — pretty-little-shop-vn

## §1 ZMP SDK Utilities

| Utility | Source | Usage | Pattern |
|---------|--------|-------|---------|
| `getUserInfo()` | `zmp-sdk` | `userState` atom in state.ts | async + `.catch()` |

> ⚠️ `getSystemInfo()` — **NOT USED** in current codebase (removed with ZMP UI Router)
> ✅ `getUserInfo()` — used in Jotai `atomWithRefresh` with `NotifiableError` error handling

```typescript
// src/state.ts
import { getUserInfo } from "zmp-sdk";

export const userState = atomWithRefresh(() => {
  return getUserInfo({ avatarType: "normal" }).catch(() => {
    throw new NotifiableError("Vui lòng cho phép truy cập tên và ảnh đại diện!");
  });
});
```

## §2 Vite / Build Utilities

| Feature | Config | Details |
|---------|--------|---------|
| Path alias | `@` → `/src` | Both `vite.config.mts` + `tsconfig.json` |
| Base path | `getBasePath()` | Dynamic: `/zapps/${APP_ID}` in PROD, `BASE_PATH` in dev |
| App env | `import.meta.env.PROD` | Vite env flag |
| URL params | `new URLSearchParams(window.location.search).get("env")` | `router.tsx` |

## §3 Window Global (`src/global.d.ts`)
```typescript
declare interface Window {
  APP_ID?: string;     // Zalo Mini App ID (injected by platform)
  BASE_PATH?: string;  // Dev override for router basename
  APP_CONFIG: any;     // app-config.json content
}
```

### App Config Pattern
```typescript
// src/utils/miscellaneous.tsx
import appConfig from '../../app-config.json';

export function getConfig<T>(getter: (config: typeof appConfig) => T): T {
  return getter(appConfig);
}

// Usage:
getConfig((c) => c.app.title)  // app title in header.tsx
```

## §4 Navigation Utilities

```typescript
// react-router-dom — DO NOT use zmp-ui useNavigate
import { useNavigate, NavLink } from "react-router-dom";

// Programmatic navigation with View Transition
const navigate = useNavigate();
navigate(-1 as To, { viewTransition: true });  // go back
navigate("/booking", { viewTransition: true }); // go to route
```

### Base Path for createBrowserRouter
```typescript
// src/router.tsx
export function getBasePath() {
  const urlParams = new URLSearchParams(window.location.search);
  const appEnv = urlParams.get("env");

  if (import.meta.env.PROD || ["TESTING_LOCAL", "TESTING", "DEVELOPMENT"].includes(appEnv)) {
    return `/zapps/${window.APP_ID}`;  // Zalo production path
  }
  return window.BASE_PATH || "";  // dev: empty string
}
```

## §5 Miscellaneous Utilities (`src/utils/miscellaneous.tsx`)

### `wait(ms)` — Promise delay
```typescript
export const wait = (ms: number): Promise<void> =>
  new Promise(resolve => setTimeout(resolve, ms));
// Used in: searchResultState atom (simulate 1500ms search delay)
```

### `startViewTransition(callback)` — View Transition wrapper
```typescript
export const startViewTransition = (callback: () => void) => {
  if (document.startViewTransition) {
    document.startViewTransition(callback);
  } else {
    callback();
  }
};
// Used in: button.tsx + available for manual transitions
```

### `promptJSON(data)` — Dev debug toast
```typescript
export const promptJSON = (data: unknown) =>
  toast(t => <code onClick={() => toast.dismiss(t.id)}>
    {JSON.stringify(data, undefined, 2)}
  </code>, { duration: Infinity });
// For development debugging only
```

### `toLowerCaseNonAccentVietnamese(str)` — Vietnamese search
```typescript
// Removes all Vietnamese diacritics for accent-insensitive search
// Used in: searchResultState atom filter logic
toLowerCaseNonAccentVietnamese("Bác sĩ") // → "bac si"
```

## §6 Format Utilities (`src/utils/format.ts`)

```typescript
import { TimeSlot } from "@/types";  // uses @/ alias

formatPrice(100000)        // → "100.000 VND"
formatDayName(new Date())  // → "Thứ hai" (Vietnamese day names)
formatFullDate(new Date()) // → "25/12/2024"
formatShortDate(new Date())// → "12.25"
formatTimeSlot({ hour: 9, half: true }) // → "09:30"
```

## §7 Error Utilities (`src/utils/errors.ts`)
```typescript
// Minimal — only one class
export class NotifiableError extends Error {}
// Extend if needed: new NotifiableError("user-facing message")
```

## §8 Anti-Patterns — DO NOT
- ❌ `import { useNavigate } from "zmp-ui"` — use `react-router-dom`
- ❌ `window.location.href = "..."` — use `useNavigate()`
- ❌ `import { getSystemInfo } from "zmp-sdk"` for theme — theme handled by Tailwind CSS vars
- ❌ Hardcode route paths — define routes in router.tsx
- ❌ `window.location.reload()` — use `atomWithRefresh` pattern

xref: react_architecture, react_hook_helper, react_state_service
