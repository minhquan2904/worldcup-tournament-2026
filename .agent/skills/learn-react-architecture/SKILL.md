---
name: learn-react-architecture
description: Learn React/Zalo Mini App architecture — project structure, Vite config, routing, entry point, styling, folder conventions
tag: "@AI-ONLY"
allowed-tools: [Read, Write, Grep, Glob]
context: fork
version: 4.0
---

# Learn React Architecture

> Output: `knowledge_react_architecture.md` → PROPOSE_DIR

## §1 Project Structure
- scan root: `src/`, `src/components/`, `src/pages/`, `src/css/`, `src/static/`
- scan future dirs (if exist): `src/hooks/`, `src/stores/`, `src/utils/`, `src/services/`, `src/types/`, `src/constants/`
- scan config files: `package.json`, `tsconfig.json`, `vite.config.mts`, `app-config.json`, `zmp-cli.json`
- scan styling: `tailwind.config.js`, `postcss.config.js`

## §2 Entry Point Flow
- readFile(`src/app.ts`) → CSS import order → React createRoot → Layout mount
- readFile(`index.html`) → meta tags, viewport, CSP, script entry
- flow: `index.html` → `src/app.ts` → CSS imports → `Layout` → `ZMPRouter` → Pages

## §3 Build & Config
- `vite.config.mts`: root, base, plugins (zaloMiniApp + react), resolve alias
- `tsconfig.json`: target, jsx, paths (`@/*` → `./src/*`), strict mode
- `app-config.json`: title, textColor, statusBar, actionBarHidden, safeArea
- `zmp-cli.json`: framework, cssPreProcessor, stateManagement, template, theming
- `package.json`: scripts (login, start, deploy via `zmp` CLI), dependencies

## §4 Routing
- ZMPRouter (from `zmp-ui`) → AnimationRoutes → Route
- pattern: `<Route path="/" element={<Component />} />`
- scan ALL Route definitions across components → route map
- !React Router directly — use ZMP wrapping layer

## §5 Styling System
- Tailwind CSS 3 + SCSS preprocessor
- darkMode: `["selector", '[zaui-theme="dark"]']` — Zalo theme integration
- CSS import order in `app.ts`: zaui.css → tailwind.scss → app.scss
- scan `tailwind.config.js`: purge paths, theme extensions, custom fonts

## §6 Folder Convention
```
src/
├── app.ts                    # Entry point
├── components/               # Shared/reusable components
│   ├── layout.tsx           # App shell (ZMPRouter, providers)
│   └── *.tsx                # Shared components
├── pages/                    # Route-level page components
│   └── index.tsx            # Home page
├── hooks/                    # Custom React hooks (if exists)
├── stores/                   # Jotai atom definitions (if exists)
├── services/                 # API service functions (if exists)
├── utils/                    # Utility/helper functions (if exists)
├── types/                    # TypeScript type definitions (if exists)
├── constants/                # App constants (if exists)
├── css/
│   ├── tailwind.scss        # Tailwind directives
│   └── app.scss             # Custom app styles
└── static/                   # Static assets (images, SVGs)
```

## §7 Write Output — Structured NL Format
Output format: **Structured NL** (@AI-ONLY, pipeline context)
- Tables for structured data (config keys, route mapping, alias paths)
- Code blocks: keep 100% unchanged (real samples, templates)
- !verbose prose | bullets + shorthand | use cos_convention.md operators

## Guardrails
- !Angular patterns — project uses React 18 function components
- !class components — function components ONLY
- ZMP UI = UI library — document common imports from `zmp-ui`
- Jotai = state management — !Redux, !Zustand, !Context API for global state
- Tailwind CSS = styling — !CSS modules, !styled-components
- Error Boundary MUST wrap AnimationRoutes in layout — scan verified: MISSING 🔴
- `src/constants/` MUST exist for app IDs + config values — scan verified: MISSING 🔴
- SCSS: migrate hardcoded colors (#ffffff) to Tailwind utilities (bg-white) — scan verified: DRIFT 🟠
- xref: react_component, react_state_service, zmp_sdk
