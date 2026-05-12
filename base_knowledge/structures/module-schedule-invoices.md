---
title: Module — Schedule & Invoices (Lịch khám & Hóa đơn)
tag: "@AI-ONLY"
generated: "2026-04-16"
---

# Module: Schedule & Invoices

## §1 Schedule Routes

| Path | Component | Handle |
|------|-----------|--------|
| `/schedule` | `ScheduleHistoryPage` | — (footer visible) |
| `/schedule/:id` | `ScheduleDetailPage` | `back:true, title:"Chi tiết"` |

## §2 Invoices Route

| Path | Component | Handle |
|------|-----------|--------|
| `/invoices` | `InvoicesPage` | `back:true, title:"Hóa đơn"` |

> Accessed from: Profile page → Action "Hóa đơn của tôi" (badge: 3)

## §3 Component Trees

### Schedule History
```mermaid
graph TD
    SHP[ScheduleHistoryPage] --> TABS[Tabs - upcoming/past]
    TABS --> ONGOING[Ongoing Bookings - schedulesState filter]
    TABS --> PAST[Past Bookings - schedulesState filter]
    ONGOING --> BK[Booking items - PolarizedList]
    PAST --> BK2[Booking items - PolarizedList]
    BK -- click --> SDT["/schedule/:id"]
```

### Schedule Detail
```mermaid
graph TD
    SDP[ScheduleDetailPage] --> DETAIL[Booking detail layout]
    DETAIL --> INFO[Doctor + Department info]
    DETAIL --> SLOT[Time slot display]
    DETAIL --> STATUS[Booking status]
    DETAIL --> ACTIONS[Action buttons - Call, Cancel]
```

## §4 State Flow

```
schedulesState (atom<Promise<Booking[]>>)
  ↓
ScheduleHistoryPage → filter by status (upcoming/past)
scheduleByIdState(id) (atomFamily)
  ↓
ScheduleDetailPage → full booking detail
invoicesState (atom<Promise<Invoice[]>>)
  ↓
InvoicesPage → invoice list
  → Invoice.booking.id links to schedule detail
```

## §5 Booking Status Pattern

```typescript
// Booking.status: "upcoming" | "completed" | "cancelled" | etc.
const upcoming = schedules.filter(s => s.status === "upcoming");
const past = schedules.filter(s => s.status !== "upcoming");
```

## §6 Invoice Structure

```typescript
interface Invoice {
  id: number;
  booking: Booking;  // embedded booking reference
}
// InvoicesPage renders Invoice.booking summary
// Click → navigate to booking detail or separate invoice detail
```

## §7 Files

| File | Purpose |
|------|---------|
| `src/pages/schedule/history.tsx` | ScheduleHistoryPage |
| `src/pages/schedule/detail.tsx` | ScheduleDetailPage |
| `src/pages/invoices/index.tsx` | InvoicesPage |

xref: state.ts (schedulesState, scheduleByIdState, invoicesState), components/polarized-list
