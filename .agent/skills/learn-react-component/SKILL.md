---
name: learn-react-component
description: Learn React component patterns — function components, props typing, hooks, ZMP UI, page components, layout
tag: "@AI-ONLY"
allowed-tools: [Read, Write, Grep, Glob]
context: fork
version: 4.0
---

# Learn React Component

> Output: `knowledge_react_component.md` → PROPOSE_DIR

## §1 Component Infrastructure
- scan `src/components/` → for each: name, props interface, hooks used, ZMP UI imports
- scan `src/pages/` → for each: name, route path, data dependencies, child components
- determine component hierarchy: Layout → Pages → Components

## §2 Page Components (read ALL)
- pattern: function component, default export
- scan: ZMP UI usage (Page, Box, Text, Button, Icon, etc.)
- scan: data fetching / state management hooks
- scan: navigation / route params
- scan: event handlers + user interactions

## §3 Layout Component
- readFile(`src/components/layout.tsx`)
- pattern: App wrapper → SnackbarProvider → ZMPRouter → AnimationRoutes → Routes
- theme: `getSystemInfo().zaloTheme` → App theme prop
- providers: document provider nesting order

## §4 Reusable Components (read ALL in components/)
- for each: function signature, props interface, return JSX
- categorize: UI (presentational) vs Container (data-connected)
- hooks: useState, useEffect, useRef, useMemo, useCallback usage
- cleanup: useEffect return cleanup functions

## §5 ZMP UI Component Usage
- scan imports from `zmp-ui` across ALL files
- catalog: which ZMP UI components are used where
- common: App, Page, Box, Text, Button, Icon, Route, ZMPRouter, AnimationRoutes, SnackbarProvider
- props: document significant props used

## §6 Component Template
```tsx
// Page component template
import { Page, Box, Text } from "zmp-ui";

function FeaturePage() {
  return (
    <Page className="...tailwind-classes">
      <Box>
        <Text.Title>Title</Text.Title>
      </Box>
    </Page>
  );
}

export default FeaturePage;
```

```tsx
// Reusable component template
import { FC } from "react";

interface FeatureProps {
  title: string;
  className?: string;
}

const Feature: FC<FeatureProps> = ({ title, className }) => {
  return <div className={className}>{title}</div>;
};

export default Feature;
```

## §7 Write Output — Structured NL Format
Output format: **Structured NL** (@AI-ONLY, pipeline context)
- Tables for structured data (component inventory, props, hooks)
- Code blocks: keep 100% unchanged (real samples, templates)
- !verbose prose | bullets + shorthand | use cos_convention.md operators
Include ready-to-copy templates for Page + Reusable component

## Guardrails
- !class components — function components ONLY (exception: ErrorBoundary class component)
- !Angular patterns (NgModule, @Component, etc.)
- default export for page components, named export OK for small utils
- TypeScript interfaces for props — !`any` typing — scan verified: `as any` found in app.ts 🟠
- hooks: follow Rules of Hooks (top-level, conditional-free)
- Layout MUST include ErrorBoundary wrapping routes — scan verified: MISSING 🔴
- xref: react_architecture, react_shared_component, react_hook_helper
