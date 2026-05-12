---
name: learn-zmp-sdk
description: Learn ZMP SDK & ZMP UI — Zalo Mini App platform APIs, UI components, theme, deployment
tag: "@AI-ONLY"
allowed-tools: [Read, Write, Grep, Glob]
context: fork
version: 4.0
---

# Learn ZMP SDK & ZMP UI

> Output: `knowledge_zmp_sdk.md` → PROPOSE_DIR
> Replaces learn-thirdparty-call — platform SDK instead of HTTP service wrappers

## §1 ZMP SDK API
- grepFor imports from `zmp-sdk` across ALL files
- catalog each SDK function used:
  - `getSystemInfo()` → device info, zaloTheme, platform
  - `openMiniApp({ appId })` → open other mini apps
  - `getUserInfo()` → user profile (if used)
  - `getPhoneNumber()` → phone auth (if used)
  - `openChat()`, `shareContent()` → social features (if used)
  - `payment()` → payment integration (if used)
- for each: parameters, return type, usage context, error handling

## §2 ZMP UI Component Library
- grepFor imports from `zmp-ui` across ALL files
- catalog each UI component:

| Component | Source | Purpose |
|-----------|--------|---------|
| App | `zmp-ui` | Root app wrapper, theme provider |
| ZMPRouter | `zmp-ui` | Router wrapper for ZMP navigation |
| AnimationRoutes | `zmp-ui` | Animated route transitions |
| Route | `zmp-ui` | Route definition |
| SnackbarProvider | `zmp-ui` | Toast/snackbar notifications |
| Page | `zmp-ui` | Page container with scroll |
| Box | `zmp-ui` | Flex container (like div) |
| Text | `zmp-ui` | Typography (Text.Title, Text.Header) |
| Button | `zmp-ui` | Button with variants + icons |
| Icon | `zmp-ui` | Icon set (zi-* icon names) |
| Input | `zmp-ui` | Form input field |
| Select | `zmp-ui` | Dropdown select |
| Modal | `zmp-ui` | Dialog/modal |
| Sheet | `zmp-ui` | Bottom sheet |
| Tabs | `zmp-ui` | Tab navigation |
| List | `zmp-ui` | List layout |
| Avatar | `zmp-ui` | User avatar |
| ImageViewer | `zmp-ui` | Image gallery |
| Spinner | `zmp-ui` | Loading spinner |
| Switch | `zmp-ui` | Toggle switch |
| Checkbox | `zmp-ui` | Checkbox input |
| Radio | `zmp-ui` | Radio button |
| DatePicker | `zmp-ui` | Date picker |
| Picker | `zmp-ui` | General picker |

- for each used: props documented, real usage examples from source

## §3 Theme & Styling Integration
- `getSystemInfo().zaloTheme` → `"light" | "dark"` → App theme prop
- `AppProps["theme"]` type from `zmp-ui/app`
- Tailwind dark mode: `[zaui-theme="dark"]` selector
- theme-color meta tag integration

## §4 Platform-Specific Behavior
- `app-config.json` settings: actionBarHidden, safeArea, statusBar
- `zmp-cli.json`: framework detection, theming config
- mobile-specific: viewport-fit cover, user-scalable no
- CSP (Content-Security-Policy) in index.html

## §5 Deployment & CLI
- `zmp login` → authenticate with Zalo
- `zmp start` → dev server (localhost:3000 via Vite)
- `zmp deploy` → deploy to Zalo platform
- scan `zmp-cli.json` → project metadata for deployment

## §6 Write Output — Structured NL Format
Output format: **Structured NL** (@AI-ONLY, pipeline context)
- Tables for structured data (SDK functions, UI components, config keys)
- Code blocks: keep 100% unchanged (real samples, templates)
- !verbose prose | bullets + shorthand | use cos_convention.md operators
- ALL function/component names = REAL from source — !placeholders

## Guardrails
- !assume web browser APIs always available — check ZMP SDK alternatives first
- !use React Router directly — use ZMPRouter wrapper from `zmp-ui`
- !hardcode app IDs — use constants or config — scan verified: `appId: "1070750904448149704"` in index.tsx 🔴
- SDK calls: ALWAYS wrap in try/catch — scan verified: `getSystemInfo()` unprotected in layout.tsx 🟠
- `openMiniApp()` calls: extract appId to `src/constants/app.ts`
- xref: react_architecture, react_component
