---
name: learn-react-state-service
description: Learn React state management — Jotai atoms, API services, data fetching, constants, type definitions
tag: "@AI-ONLY"
allowed-tools: [Read, Write, Grep, Glob]
context: fork
version: 4.0
---

# Learn React State & Service

> Output: `knowledge_react_state_service.md` → PROPOSE_DIR

## §1 Jotai State Management
- scan `src/stores/` || `src/atoms/` || `src/state/` (if exist)
- for each atom file: atom name, type, initial value, derived atoms
- patterns:
  - `atom()` — primitive state
  - `atom((get) => ...)` — derived/computed state
  - `atomWithStorage()` — persisted state
  - async atoms — data fetching atoms
- grepFor(`atom(`, `src/`) → catalog ALL atoms

## §2 API Services
- scan `src/services/` || `src/api/` (if exist)
- pattern: fetch/axios wrapper functions
- for each service: function name, endpoint, method, request/response types
- error handling: try/catch, error state management
- authentication: token handling, ZMP SDK auth

## §3 Data Fetching Patterns
- scan for `fetch(`, `axios.`, custom hooks with data fetching
- pattern: loading → data → error state management
- caching: Jotai atom caching, SWR-like patterns
- scan for `useEffect` + fetch combinations

## §4 Constants & Config
- scan `src/constants/` (if exist)
- scan `app-config.json` → runtime config, expose via `window.APP_CONFIG`
- route paths, API endpoints, feature flags
- enums / string constants

## §5 Type Definitions
- scan `src/types/` || `src/interfaces/` || `src/models/` (if exist)
- shared types: API response types, entity types, form types
- grepFor(`interface `, `src/`) + grepFor(`type `, `src/`) → catalog

## §6 Template — Atom + Service
```typescript
// stores/feature.ts
import { atom } from "jotai";

interface FeatureItem {
  id: string;
  name: string;
}

// Primitive atom
export const featureListAtom = atom<FeatureItem[]>([]);

// Derived atom
export const featureCountAtom = atom((get) => get(featureListAtom).length);

// Async atom (data fetching)
export const fetchFeatureAtom = atom(async () => {
  const response = await fetch("/api/features");
  return response.json() as Promise<FeatureItem[]>;
});
```

```typescript
// services/feature.service.ts
const API_BASE = "/api/v1";

export const featureService = {
  getAll: async (): Promise<FeatureItem[]> => {
    const res = await fetch(`${API_BASE}/features`);
    if (!res.ok) throw new Error("Failed to fetch");
    return res.json();
  },
  create: async (data: Partial<FeatureItem>): Promise<FeatureItem> => {
    const res = await fetch(`${API_BASE}/features`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to create");
    return res.json();
  },
};
```

## §7 Write Output — Structured NL Format
Output format: **Structured NL** (@AI-ONLY, pipeline context)
- Tables for structured data (atom inventory, service methods, types)
- Code blocks: keep 100% unchanged (real samples, templates)
- !verbose prose | bullets + shorthand | use cos_convention.md operators

## Guardrails
- Jotai = primary state management — !Redux, !Zustand, !Context API for global state
- !Angular services/DI — use plain functions or Jotai atoms
- !BehaviorSubject, !Observable — use Jotai atoms for reactive state
- async atoms for server state — !manual useEffect + setState
- TypeScript strict types — !`any`
- xref: react_component, react_util, zmp_sdk
