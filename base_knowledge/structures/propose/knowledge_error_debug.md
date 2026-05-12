---
title: Error Handling & Debugging Knowledge
tag: "@AI-ONLY"
generated: "2026-04-16"
source_skill: learn-error-debug
---

# Error Handling & Debugging — pretty-little-shop-vn

## §1 Error Architecture

```
Error Sources
├── Route errors      → React Router ErrorBoundary (useRouteError)
├── ZMP SDK errors    → NotifiableError → toast.error()
├── Async atom errors → Jotai loadable { state: "hasError" }
└── UI errors         → react-hot-toast (toast.error)
```

## §2 Error Boundary (`src/components/error-boundary.tsx`)

```typescript
// React Router v7 functional ErrorBoundary (NOT class-based)
export function ErrorBoundary() {
  const error = useRouteError();          // React Router hook
  const resetUser = useSetAtom(userState); // Jotai

  useEffect(() => {
    if (error instanceof NotifiableError) {
      toast.error(error.message);  // user-facing toast
      resetUser();                 // re-fires getUserInfo()
    } else {
      console.warn({ error });     // dev log for unexpected errors
    }
  }, [error]);

  return <NotFound noToast />;  // navigates back, no extra toast
}
```

### Mounting Pattern
```typescript
// src/router.tsx — root route level
{
  path: "/",
  element: <Layout />,
  ErrorBoundary,   // attached here — catches all child route errors
  children: [...]
}
```

## §3 NotifiableError Pattern

```typescript
// src/utils/errors.ts
export class NotifiableError extends Error {}

// Usage pattern (state.ts):
return getUserInfo(...).catch(() => {
  throw new NotifiableError("Friendly message for user");
});

// Detection (error-boundary.tsx):
if (error instanceof NotifiableError) {
  toast.error(error.message);  // show to user
  resetUser();                 // recover user atom state
} else {
  console.warn({ error });     // unexpected — log only
}
```

## §4 Toast Notifications (`react-hot-toast`)

### Installation
`react-hot-toast: ^2.5.2`

### Toaster setup
```tsx
// src/components/layout.tsx
import { Toaster } from "react-hot-toast";
<Toaster containerClassName="toast-container" position="bottom-center" />
```

### Usage patterns
```typescript
import toast from "react-hot-toast";

toast.error("Error message");          // error toast
toast("Message");                      // default toast
toast(t => <code onClick={...}>...</code>, { duration: Infinity }); // custom JSX toast (dev)
toast.dismiss(id);                     // dismiss by ID
```

## §5 404 / NotFound Page (`src/pages/404.tsx`)

```tsx
export default function NotFound(props: { noToast?: boolean }) {
  const navigate = useNavigate();
  useEffect(() => {
    if (!props.noToast) toast.error("Trang không tồn tại");
    navigate(-1 as To, { viewTransition: true });  // go back
  }, []);
  return <></>;
}
```
- Called by: `ErrorBoundary` (with `noToast`) + catch-all route `*` (with toast)
- Auto-navigates back — does NOT stay on 404 page

## §6 Jotai Async Error Handling

### loadable pattern (non-crashing)
```typescript
export const searchResultState = atomFamily((keyword: string) =>
  loadable(atom(async (get) => {
    // errors caught by loadable — returns { state: "hasError", error }
  }))
);

// In component:
const result = useAtomValue(searchResultState(keyword));
if (result.state === "loading") return <Spinner />;
if (result.state === "hasError") return <ErrorUI error={result.error} />;
```

### Suspense + ErrorBoundary pattern (crashing — let ErrorBoundary handle)
```typescript
// atom throws → propagates to nearest ErrorBoundary
// In component tree: <Suspense> in page.tsx catches loading
// Route ErrorBoundary catches thrown errors
```

## §7 Debug Utilities

### `promptJSON` — dev JSON inspector toast
```typescript
import { promptJSON } from "@/utils/miscellaneous";
promptJSON(someData);  // displays JSON in persistent toast
// Click to dismiss
```

### `console.warn` convention
- Unexpected errors: `console.warn({ error })` in ErrorBoundary
- Do NOT `console.error` — use `toast.error` for user-facing errors

## §8 Verification Checklist

| # | Check | Status |
|---|-------|--------|
| EB1 | Route ErrorBoundary mounted at root | ✅ verified |
| EB2 | NotifiableError class exists | ✅ verified |
| EB3 | ZMP SDK calls have `.catch()` | ✅ userState verified |
| EB4 | Toast system initialized (Toaster in Layout) | ✅ verified |
| EB5 | 404 page navigates back | ✅ verified |
| EB6 | loadable used for non-critical async | ✅ searchResultState |
| EB7 | Suspense wraps Outlet in page.tsx | ✅ verified |

## §9 Known Issues / Gaps

| ID | Issue | Severity |
|----|-------|----------|
| ERR-001 | `console.warn` only for unexpected errors — no error reporting service | 🟡 |
| ERR-002 | Jotai form atoms not validated client-side — can submit empty forms | 🟠 |
| ERR-003 | Mock data never fails — no error states tested in listings | 🟡 |

xref: react_architecture, react_component, react_state_service
