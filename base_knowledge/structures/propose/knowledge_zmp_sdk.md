---
title: ZMP SDK Knowledge
tag: "@AI-ONLY"
generated: "2026-04-16"
source_skill: learn-zmp-sdk
---

# ZMP SDK & ZMP UI — pretty-little-shop-vn

## §1 ZMP SDK Usage

### Installed version
`zmp-sdk: latest` (from package.json)

### Active API Calls

| API | Call | Location | Error Handling |
|-----|------|----------|----------------|
| `getUserInfo` | `getUserInfo({ avatarType: "normal" })` | `state.ts` — `userState` atom | `.catch(() => throw NotifiableError)` |

### Removed ZMP SDK calls (post-refactor)
- ❌ `getSystemInfo()` — was used for `zaloTheme`. **REMOVED** in current codebase (Tailwind CSS handles theming).

### ZMP SDK Pattern (established)
```typescript
import { getUserInfo } from "zmp-sdk";

// MUST wrap with try/catch or .catch()
const user = await getUserInfo({ avatarType: "normal" })
  .catch(() => {
    throw new NotifiableError("Friendly error message for user");
  });
```

## §2 ZMP UI Usage

### Installed version
`zmp-ui: ^1.11.7` (from package.json)

### CRITICAL: ZMP UI routing components **NOT USED**
| Component | Status | Replacement |
|-----------|--------|-------------|
| `App` | ❌ NOT used | Native `<div>` in `layout.tsx` |
| `SnackbarProvider` | ❌ NOT used | `react-hot-toast` `<Toaster>` |
| `ZMPRouter` | ❌ NOT used | `createBrowserRouter` from react-router-dom |
| `AnimationRoutes` | ❌ NOT used | React Router `<Outlet>` |
| `Route` (zmp-ui) | ❌ NOT used | `Route` from react-router-dom |
| `Page` (zmp-ui) | ❌ NOT used | Custom `page.tsx` with `<Outlet>` |
| `useNavigate` (zmp-ui) | ❌ NOT used | `useNavigate` from react-router-dom |

### ZMP UI components potentially still used (unconfirmed — check individual pages)
> The package `zmp-ui ^1.11.7` is in dependencies but routing/shell components are removed.
> Individual pages may use ZMP UI form/display components — verify per page.
> Stylesheet still imported: `import "zmp-ui/zaui.min.css"` in `app.ts`

### ZMP UI stylesheet
```typescript
// src/app.ts
import "zmp-ui/zaui.min.css";  // CSS custom properties still loaded
```
CSS variables from zaui.min.css may be used by Tailwind theme (`:root {}` vars).

## §3 Zalo Platform Integration

### appId Configuration
```json
// app-config.json
{ "app": { "title": "...", ... } }
```

### App ID pattern (router.tsx)
```typescript
// Zalo injects APP_ID into window
return `/zapps/${window.APP_ID}`;  // production basename
```

### Zalo WebView constraints
- ✅ HTML5 History API available → `createBrowserRouter` works with `basename`
- ✅ No MemoryRouter needed (correct basename is `/zapps/${APP_ID}`)
- Platform sets `window.APP_ID` automatically

## §4 ZMP CLI Configuration

| File | Purpose |
|------|---------|
| `zmp-cli.json` | ZMP app metadata |
| `app-config.json` | App title, color, etc. |
| `zmp-vite-plugin` | Vite plugin for ZMP build |

### Scripts
```json
"login": "zmp login",
"start": "zmp start",      // dev server
"deploy": "zmp deploy"     // publish to Zalo
```

## §5 Rules & Conventions

| # | Rule | Severity |
|---|------|----------|
| RZ1 | ZMP SDK calls: MUST have try/catch or .catch() | 🔴 |
| RZ2 | Use `NotifiableError` for user-facing ZMP SDK errors | 🟠 |
| RZ3 | !hardcode appId — use `window.APP_ID` | 🔴 |
| RZ4 | !import routing/shell components from `zmp-ui` — use `react-router-dom` | 🔴 |
| RZ5 | !import `getSystemInfo()` for theme — use Tailwind CSS vars | 🟠 |
| RZ6 | `zmp-ui/zaui.min.css` MUST be imported in `app.ts` | 🟠 |

xref: react_architecture, react_component, react_util
