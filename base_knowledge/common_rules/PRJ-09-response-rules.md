---
description: Response Standards — React/Zalo Mini App
tag: "@AI-ONLY"
---

# Response Standards

## §1 API Response Handling — handle data correctly on client

| ❌ Forbidden | ✅ Correct |
|-------------|-----------|
| expose raw API response to UI | mapTo(typed DTO) with required fields only |
| store sensitive fields (password, token) in state | remove completely from client state |
| trust client-side data for auth decisions | always validate server-side |
| render unvalidated external data | sanitize before rendering |

Rules:
- API responses MUST be typed with TypeScript interfaces
- each API endpoint: own response type — !use `any`
- null/undefined handling: optional chaining `?.` + nullish coalescing `??`
- loading/error/success states for ALL async operations

## §2 API Response Structure (expected from backend)

| Field | Type | Required |
|-------|------|:--------:|
| `code` | number | ✅ — HTTP-like (200 = success) |
| `message` | string | ✅ — user-friendly |
| `data` | T \| null | per API — null if error |

```typescript
// types/api.ts
interface ApiResponse<T> {
  code: number;
  message: string;
  data: T | null;
}

interface PaginatedData<T> {
  items: T[];
  totalCount: number;
  pageNumber: number;
  pageSize: number;
}
```

## §3 Error Handling — !expose raw errors to user

| ❌ Forbidden | ✅ Correct |
|-------------|-----------|
| show raw error.message to user | user-friendly Vietnamese message |
| show stack trace | generic "Đã xảy ra lỗi" + console.error internally |
| show HTTP status code to user | mapped to friendly message |
| leave failed state without recovery UI | provide retry/back action |

```typescript
// services/api.ts — error handling pattern
async function fetchData<T>(url: string): Promise<ApiResponse<T>> {
  try {
    const res = await fetch(url);
    if (!res.ok) {
      console.error(`[API] ${url} failed: ${res.status}`);
      return { code: res.status, message: "Yêu cầu không thể xử lý", data: null };
    }
    return await res.json();
  } catch (error) {
    console.error(`[API] ${url} error:`, error);
    return { code: 500, message: "Lỗi kết nối. Vui lòng thử lại sau.", data: null };
  }
}
```

## §4 Error Codes

Default unknown error message: "Yêu cầu không thể xử lý. Vui lòng thử lại sau."
- !return(empty response) || !missing(code/message)

| Code | Category | UI Message |
|:----:|----------|-----------|
| 200 | Success | — (render data) |
| 400 | Client input error | "Dữ liệu không hợp lệ" |
| 401 | Not authenticated | Redirect to login / re-auth via ZMP SDK |
| 403 | Not authorized | "Bạn không có quyền thực hiện" |
| 404 | Resource not found | "Không tìm thấy dữ liệu" |
| 422 | Business rule violation | Show specific validation message |
| 500 | System error | "Đã xảy ra lỗi. Vui lòng thử lại sau." |

## §5 UI State Management for API Calls

```typescript
// Pattern: loading → data → error
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
const [data, setData] = useState<T | null>(null);

const fetchAndSet = async () => {
  setLoading(true);
  setError(null);
  try {
    const result = await fetchData<T>(url);
    if (result.code === 200) {
      setData(result.data);
    } else {
      setError(result.message);
    }
  } catch {
    setError("Lỗi kết nối");
  } finally {
    setLoading(false);
  }
};
```
