---
title: Error Handling & Debugging Knowledge
tag: "@AI-ONLY"
generated: "2026-04-15"
source_skill: learn-error-debug
---

# Error Handling & Debugging — pretty-little-shop-vn

## §1 Error Boundary

### Current State: 🔴 MISSING
No ErrorBoundary component found in source code.

### Recommended Implementation
```tsx
// src/components/ErrorBoundary.tsx
import React from "react";
import { Box, Text, Button } from "zmp-ui";

interface Props { children: React.ReactNode; fallback?: React.ReactNode; }
interface State { hasError: boolean; error?: Error; }

class ErrorBoundary extends React.Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error("[ErrorBoundary]", error, info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <Box className="flex flex-col items-center justify-center min-h-screen p-4">
          <Text.Title>Đã xảy ra lỗi</Text.Title>
          <Text className="text-gray-500 mt-2">Vui lòng thử lại sau</Text>
          <Button className="mt-4" onClick={() => this.setState({ hasError: false })}>
            Thử lại
          </Button>
        </Box>
      );
    }
    return this.props.children;
  }
}
export default ErrorBoundary;
```

### Integration Point (layout.tsx)
```tsx
<App theme={...}>
  <SnackbarProvider>
    <ErrorBoundary>       {/* ← ADD HERE */}
      <ZMPRouter>
        <AnimationRoutes>
          <Route ... />
        </AnimationRoutes>
      </ZMPRouter>
    </ErrorBoundary>
  </SnackbarProvider>
</App>
```

## §2 Error Handling Patterns

### Current Coverage
| Pattern | Found | Files |
|---------|-------|-------|
| try/catch | ❌ None | — |
| .catch() | ❌ None | — |
| Error state | ❌ None | — |
| useEffect cleanup | ✅ | clock.tsx |

### Expected Patterns
```tsx
// API error handling
try {
  const data = await fetchProducts();
  setProducts(data);
} catch (error) {
  console.error("[ProductPage] fetch failed:", error);
  setError(error instanceof Error ? error : new Error("Unknown error"));
}

// ZMP SDK error handling
try {
  const info = getSystemInfo();
  setTheme(info.zaloTheme);
} catch (error) {
  console.warn("[Layout] getSystemInfo failed, using light theme:", error);
  setTheme("light"); // fallback
}
```

## §3 Common Errors & Solutions

| Error | Cause | Fix |
|-------|-------|-----|
| `Invalid hook call` | Hook called outside component | Move hook to component body top-level |
| `Objects are not valid as React child` | Rendering object | Use `.toString()` or extract property |
| `Cannot read property of undefined` | Missing null check | Optional chaining `?.` or loading guard |
| `Module not found` | Wrong import path | Check `@/` alias, verify file exists |
| `zmp-sdk not available` | Running outside Zalo | try/catch with fallback |
| `CORS error` | API call from dev | Configure Vite proxy |
| `Tailwind classes not applied` | File not in purge paths | Check `tailwind.config.js` content |
| `Dark mode not working` | Wrong selector | Use `[zaui-theme="dark"]` |

## §4 Debug Tools

| Tool | Usage |
|------|-------|
| Vite HMR | Auto-reload on save, error overlay in browser |
| React DevTools | Component tree, hooks inspector, profiler |
| Zalo DevTools | Mini app testing in Zalo environment |
| Console | `console.log/warn/error` with component prefix `[ComponentName]` |
| Network tab | API call inspection, response validation |

## §5 Vite Troubleshooting

| Issue | Fix |
|-------|-----|
| Port conflict | Kill existing process on port, restart `zmp start` |
| HMR not working | Clear `.vite` cache, restart dev server |
| Build TypeScript error | Check strict mode settings in tsconfig |
| Asset not loading | Verify `assetsInlineLimit: 0` in vite.config |
| Path alias error | Ensure `@/` configured in both tsconfig + vite.config |

xref: react_architecture, zmp_sdk
