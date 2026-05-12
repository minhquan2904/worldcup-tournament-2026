---
name: learn-react-shared-component
description: Learn React shared components — reusable UI components, props interfaces, ZMP UI wrappers, SVG components
tag: "@AI-ONLY"
allowed-tools: [Read, Write, Grep, Glob]
context: fork
version: 4.0
---

# Learn React Shared Components

> Output: `knowledge_react_shared_component.md` → PROPOSE_DIR

## §1 List All
```
scanDir: src/components/
```
- exclude: `layout.tsx` (documented in react_architecture)
- for each: filename, component name, category (UI/container/SVG)

## §2 Component Deep-Read (each component)
For each component in `src/components/`:
- function signature + props interface
- internal state (useState, useRef)
- side effects (useEffect)
- ZMP UI imports + usage
- Tailwind classes used
- event handlers
- children/composition pattern

## §3 SVG / Icon Components
- scan for inline SVG components (like `logo.tsx`)
- pattern: `SVGProps<SVGSVGElement>` spread
- usage: `<Logo className="..." />`

## §4 ZMP UI Wrapper Components
- scan for components that wrap/extend ZMP UI components
- document: original ZMP UI component → wrapper → added behavior
- common wrappings: styled Box, custom Button, themed Page

## §5 Component Composition Patterns
- scan for children prop usage
- scan for render prop / compound component patterns
- scan for forwardRef usage
- scan for HOC patterns (if any)

## §6 Usage Examples
- grepFor each shared component name across `src/pages/` → usage patterns
- document: where used, what props passed, context

## §7 Write Output — Structured NL Format
Output format: **Structured NL** (@AI-ONLY, pipeline context)
- Tables for structured data (component inventory, props, usage)
- Code blocks: keep 100% unchanged (real samples, templates)
- !verbose prose | bullets + shorthand | use cos_convention.md operators

## Guardrails
- !create duplicate components — check existing inventory first
- !inline complex SVG — extract to separate component file
- TypeScript interfaces for ALL props — !`any`
- !Angular component patterns (selector, NgModule, etc.)
- Tailwind for styling — !inline style objects (except dynamic values)
- xref: react_component, react_hook_helper
