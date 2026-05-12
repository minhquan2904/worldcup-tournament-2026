---
title: React Hook & Helper Knowledge
tag: "@AI-ONLY"
generated: "2026-04-16"
source_skill: learn-react-hook-helper
---

# React Custom Hooks & Helpers — pretty-little-shop-vn

## §1 Custom Hooks (`src/hooks.ts`)

### `useRealHeight(element, defaultValue?)`
```typescript
export function useRealHeight(
  element: MutableRefObject<HTMLDivElement | null>,
  defaultValue?: number
): number
```
- Uses `ResizeObserver` to track element height dynamically
- Cleanup: `ro.disconnect()` on unmount
- Fallback: returns `-1` if `ResizeObserver` unavailable (SSR safe)
- Returns: `defaultValue ?? 0` initially, then actual height

### `useRouteHandle()`
```typescript
export function useRouteHandle() {
  const matches = useMatches() as UIMatch<undefined, {
    title?: string;
    back?: boolean;
    scrollRestoration?: number;
    noScroll?: boolean;
    profile?: boolean;
  }>[];
  const lastMatch = matches[matches.length - 1];
  return [lastMatch.handle ?? {}, lastMatch, matches] as const;
}
```
- Returns: `[handle, lastMatch, allMatches]`
- Used in: `Header`, `Footer`, `Page`, `ScrollRestoration`
- Handle fields:
  - `back`: show back button, hide footer
  - `title`: header title string (or `"custom"` → reads `customTitleState` atom)
  - `noScroll`: disable scroll on page container
  - `profile`: show profile header variant
  - `scrollRestoration`: force scroll to specific position

## §2 Hook Usage Map

| Hook | Used In | Purpose |
|------|---------|---------|
| `useRouteHandle` | header.tsx, footer.tsx, page.tsx, scroll-restoration.tsx | Route metadata |
| `useRealHeight` | (available for dynamic layout calculations) | Element height tracking |
| `useAtomValue` | header.tsx, most pages | Read Jotai atoms |
| `useSetAtom` | error-boundary.tsx | Trigger atom refresh |
| `useResetAtom` | form pages (booking, ask, feedback) | Reset form state |
| `useNavigate` | header.tsx, 404.tsx | Programmatic navigation |
| `useLocation` | header.tsx, scroll-restoration.tsx | Current route info |
| `useMatches` | hooks.ts → useRouteHandle | All matched routes |
| `useRouteError` | error-boundary.tsx | Route-level errors |
| `useParams` | detail pages (service/:id, department/:id) | URL parameters |
| `useState` | form components, UI state | Local component state |
| `useEffect` | error-boundary.tsx, scroll-restoration.tsx, 404.tsx | Side effects |
| `useLayoutEffect` | scroll-restoration.tsx (via hooks.ts) | Layout measurements |
| `Suspense` | page.tsx | Async atom loading boundaries |

## §3 Helper Functions (`src/utils/`)

### `src/utils/format.ts`
| Function | Signature | Returns |
|----------|-----------|---------|
| `formatPrice` | `(price: number) => string` | `"100.000 VND"` (vi-VN, code style) |
| `formatDayName` | `(date: Date) => string` | `"Thứ hai"` … `"Chủ nhật"` |
| `formatFullDate` | `(date: Date) => string` | `"25/12/2024"` |
| `formatShortDate` | `(date: Date) => string` | `"12.25"` |
| `formatTimeSlot` | `({ hour, half }: TimeSlot["time"]) => string` | `"09:30"` |

### `src/utils/miscellaneous.tsx`
| Function | Signature | Returns |
|----------|-----------|---------|
| `getConfig<T>` | `(getter: (config) => T) => T` | Config value from `app-config.json` |
| `wait` | `(ms: number) => Promise<void>` | Delay promise |
| `startViewTransition` | `(callback: () => void) => void` | View Transition API wrapper |
| `promptJSON` | `(data: unknown) => void` | Dev: toast JSON debug output |
| `toLowerCaseNonAccentVietnamese` | `(str: string) => string` | Vietnamese accent removal |

### `src/utils/errors.ts`
```typescript
export class NotifiableError extends Error {}
```
- Thrown by: `userState` atom when `getUserInfo()` fails
- Caught by: `ErrorBoundary` → `toast.error(error.message)`
- Pattern: custom error class for user-facing messages

### `src/utils/mock.ts`
- Mock data source for all entities (see knowledge_react_state_service.md §4)
- Returns `Promise<T[]>` for async atom compatibility

## §4 Custom Hook Templates (Established Patterns)

### atomFamily Read Hook
```typescript
// Pattern used in detail pages
function useService(id: number) {
  return useAtomValue(serviceByIdState(id));
  // Wrap in Suspense — returns T | undefined (not Promise)
}
```

### Form Reset Hook
```typescript
// Used in booking flow
const resetBooking = useResetAtom(bookingFormState);  // from jotai/utils
// Call resetBooking() to clear form
```

### Route Params Hook
```typescript
// Used in service/:id, department/:id, schedule/:id, news/:id
const { id } = useParams<{ id: string }>();
const numericId = Number(id);
```

xref: react_architecture, react_component, react_state_service
