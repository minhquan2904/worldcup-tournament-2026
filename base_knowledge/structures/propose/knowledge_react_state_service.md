---
title: React State & Service Knowledge
tag: "@AI-ONLY"
generated: "2026-04-16"
source_skill: learn-react-state-service
---

# React State & Services — pretty-little-shop-vn

## §1 State Architecture

**Single file**: `src/state.ts` — all Jotai atoms centralized.
**Providerless mode**: No `<Provider>` wrapper — Jotai 2.x global store.
**Async first**: Most atoms hold `Promise<T>` (async data from mock/API).

### Jotai imports used
```typescript
import { atom } from "jotai";
import {
  atomFamily,        // parametric atoms
  atomWithDefault,   // (unused currently)
  atomWithLazy,      // (unused currently)
  atomWithRefresh,   // re-fetchable atoms
  atomWithReset,     // resettable form atoms
  loadable,          // wrap async atom → { state, data, error }
} from "jotai/utils";
```

## §2 Atom Inventory

### Listing Atoms (async, Promise<T[]>)
| Atom | Type | Mock Source |
|------|------|-------------|
| `servicesState` | `atom<Promise<Service[]>>` | `mockServices` |
| `doctorsState` | `atom<Promise<Doctor[]>>` | `mockDoctors` |
| `availableTimeSlotsState` | `atom<Promise<AvailableTimeSlots[]>>` | `mock7DaysTimeSlots` |
| `articlesState` | `atom<Promise<Article[]>>` | `mockArticles` |
| `departmentGroupsState` | `atom<Promise<DepartmentGroup[]>>` | `mockDepartmentGroups` |
| `departmentsState` | `atom<Promise<Department[]>>` | `mockDepartments` |
| `schedulesState` | `atom<Promise<Booking[]>>` | `mockBookings` |
| `invoicesState` | `atom<Promise<Invoice[]>>` | `mockInvoices` |
| `symptomsState` | `atom<Promise<string[]>>` | `mockSymptoms` |
| `feedbackCategoriesState` | `atom<Promise<string[]>>` | `mockFeedbackCategories` |

### Detail Atoms (atomFamily — parametric by ID)
```typescript
export const serviceByIdState = atomFamily((id: number) =>
  atom(async (get) => {
    const services = await get(servicesState);
    return services.find((service) => service.id === id);
  })
);
// Same pattern: departmentByIdState, scheduleByIdState, newsByIdState
```

### Computed Atoms (derived)
```typescript
export const departmentHierarchyState = atom(async (get) => {
  const [groups, deps] = await Promise.all([
    get(departmentGroupsState),
    get(departmentsState),
  ]);
  return groups.map((group) => ({
    ...group,
    subDepartments: deps.filter((dep) => dep.groupId === group.id),
  }));
});
```

### Search Atom (loadable + simulated delay)
```typescript
export const searchResultState = atomFamily((keyword: string) =>
  loadable(atom(async (get) => {
    await wait(1500);  // simulate network delay
    // filter doctors, departments, news by keyword
    // uses toLowerCaseNonAccentVietnamese for Vietnamese search
  }))
);
// Returns: { state: "loading"|"hasData"|"hasError", data?, error? }
```

### User Atom (ZMP SDK + atomWithRefresh)
```typescript
export const userState = atomWithRefresh(() => {
  return getUserInfo({ avatarType: "normal" }).catch(() => {
    throw new NotifiableError("Vui lòng cho phép truy cập tên và ảnh đại diện!");
  });
});
```
- `atomWithRefresh` → call `useSetAtom(userState)()` to re-fetch
- `NotifiableError` → caught by `ErrorBoundary` → `toast.error(message)`

### Form Atoms (atomWithReset)
| Atom | Type | Initial |
|------|------|---------|
| `symptomFormState` | `SymptomDescription` | `{ symptoms:[], description:"", images:[] }` |
| `bookingFormState` | `{ slot?, doctor?, department?, symptoms, description, images }` | empty |
| `askFormState` | `Inquiry` | `{ symptoms:[], description:"", images:[] }` |
| `feedbackFormState` | `Feedback` | `{ title:"", description:"", images:[], category:"" }` |

### Misc Atoms
| Atom | Type | Purpose |
|------|------|---------|
| `customTitleState` | `atom("")` | Dynamic route title for `handle.title === "custom"` |

## §3 Atom Usage Patterns

### Read sync
```typescript
const services = useAtomValue(servicesState);  // returns Promise<Service[]>
// Must use Suspense or await
```

### Read with loadable
```typescript
const result = useAtomValue(searchResultState(keyword));
if (result.state === "loading") return <Spinner />;
if (result.state === "hasError") return <Error />;
const { doctors, departments, news } = result.data;
```

### Reset form atom
```typescript
const resetBooking = useResetAtom(bookingFormState);
resetBooking();  // back to initial value
```

### Refresh user
```typescript
const refreshUser = useSetAtom(userState);
refreshUser();  // re-runs getUserInfo()
```

## §4 Mock Data (`src/utils/mock.ts`)
All data is mocked — no real API calls yet.

| Mock | Returns |
|------|---------|
| `mockServices` | `Promise<Service[]>` |
| `mockDoctors` | `Promise<Doctor[]>` |
| `mock7DaysTimeSlots` | `Promise<AvailableTimeSlots[]>` |
| `mockBookings` | `Promise<Booking[]>` |
| `mockInvoices` | `Promise<Invoice[]>` |
| `mockArticles` | `Promise<Article[]>` |
| `mockDepartments` | `Promise<Department[]>` |
| `mockDepartmentGroups` | `Promise<DepartmentGroup[]>` |
| `mockSymptoms` | `Promise<string[]>` |
| `mockFeedbackCategories` | `Promise<string[]>` |

> Migration path: Replace `mock*` calls with real API calls (HttpService) in `state.ts`

## §5 TypeScript Interfaces (`src/types.d.ts`)

| Interface | Key Fields |
|-----------|-----------|
| `Service` | `id, name, description, image, price, department` |
| `TimeSlot` | `date: Date, time: { hour, half? }` |
| `AvailableTimeSlots` | `date: Date, slots: [{hour, half?, isAvailable?}]` |
| `Doctor` | `id, name, title, languages, specialties, image, isAvailable` |
| `SymptomDescription` | `symptoms, description, images` |
| `Inquiry extends SymptomDescription` | `+ department?` |
| `Feedback` | `title, description, images, category` |
| `Booking` | `id, status, patientName, schedule: TimeSlot, doctor, department` |
| `Invoice` | `id, booking: Booking` |
| `DepartmentGroup` | `id, name, description` |
| `Department` | `id, name, shortDescription, description, groupId` |
| `Article` | `id, title, description, category, timeAgo, image, content` |

## §6 Global Type Augmentation (`src/global.d.ts`)
```typescript
declare interface Window {
  APP_ID?: string;     // Zalo Mini App ID (set by platform)
  BASE_PATH?: string;  // Base path override for dev
  APP_CONFIG: any;     // app-config.json deep clone
}
```

xref: react_architecture, react_hook_helper, zmp_sdk
