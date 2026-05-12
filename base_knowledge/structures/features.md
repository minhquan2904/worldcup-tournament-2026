---
title: Features Registry
tag: "@AI-ONLY"
generated: "2026-04-15"
updated: "2026-04-16"
changelog: "2026-04-16 — Full rewrite: starter → full healthcare SPA (15 routes, ~22 atoms, 18+ components)"
---

# Features Registry — pretty-little-shop-vn

## §1 Page Features (Route-Level)

| # | Feature | Route | Page Component | File |
|---|---------|-------|----------------|------|
| 1 | Trang chủ | `/` | `HomePage` | `src/pages/home/index.tsx` |
| 2 | Tìm kiếm | `/search` | `SearchResultPage` | `src/pages/search/index.tsx` |
| 3 | Danh mục | `/categories` | `CategoriesPage` | `src/pages/categories/index.tsx` |
| 4 | Khám phá | `/explore` | `ExplorePage` | `src/pages/explore/index.tsx` |
| 5 | Tất cả dịch vụ | `/services` | `ServicesPage` | `src/pages/services/index.tsx` |
| 6 | Chi tiết dịch vụ | `/service/:id` | `ServiceDetailPage` | `src/pages/detail/service.tsx` |
| 7 | Chi tiết khoa | `/department/:id` | `DepartmentDetailPage` | `src/pages/detail/department.tsx` |
| 8 | Đặt lịch khám | `/booking/:step?` | `BookingPage` | `src/pages/booking/index.tsx` |
| 9 | Gửi câu hỏi | `/ask` | `AskPage` | `src/pages/ask/index.tsx` |
| 10 | Gửi phản ảnh | `/feedback` | `FeedbackPage` | `src/pages/feedback/index.tsx` |
| 11 | Lịch sử khám | `/schedule` | `ScheduleHistoryPage` | `src/pages/schedule/history.tsx` |
| 12 | Chi tiết lịch | `/schedule/:id` | `ScheduleDetailPage` | `src/pages/schedule/detail.tsx` |
| 13 | Hồ sơ cá nhân | `/profile` | `ProfilePage` | `src/pages/profile/index.tsx` |
| 14 | Tin tức | `/news/:id` | `NewsPage` | `src/pages/news/index.tsx` |
| 15 | Hóa đơn | `/invoices` | `InvoicesPage` | `src/pages/invoices/index.tsx` |
| 16 | 404 / Not Found | `*` | `NotFound` | `src/pages/404.tsx` |

## §2 Shared Components

| # | Component | File | Used By |
|---|-----------|------|---------|
| 1 | Layout | `src/components/layout.tsx` | App shell |
| 2 | Header | `src/components/header.tsx` | Layout |
| 3 | Footer | `src/components/footer.tsx` | Layout |
| 4 | Page | `src/components/page.tsx` | Layout (Outlet wrapper) |
| 5 | ErrorBoundary | `src/components/error-boundary.tsx` | router.tsx root route |
| 6 | ScrollRestoration | `src/components/scroll-restoration.tsx` | Layout |
| 7 | TransitionLink | `src/components/transition-link.tsx` | Footer, Section, many pages |
| 8 | Button | `src/components/button.tsx` | Booking, Ask, Feedback |
| 9 | Section | `src/components/section.tsx` | Home, Profile |
| 10 | Tabs | `src/components/tabs.tsx` | Detail pages |
| 11 | PolarizedList | `src/components/polarized-list.tsx` | Schedule, Invoices |
| 12 | MarkedTitleSection | `src/components/marked-title-section.tsx` | Home sections |
| 13 | RemoteDiagnosisItem | `src/components/remote-diagnosis-item.tsx` | Home |
| 14 | DashedDivider | `src/components/dashed-divider.tsx` | various |
| 15 | HorizontalDivider | `src/components/horizontal-divider.tsx` | various |

### Icon Components (`src/components/icons/`) — 16 total
`ArrowRightIcon, BackIcon, BigPlusIcon, CallIcon, CartIcon (schedule), CheckIcon, ChevronDownIcon, ExploreIcon, FooterWaveIcon, HeaderShieldIcon, HomeIcon, PlusIcon, ProfileIcon, SearchIcon, ShipIcon, SuccessIcon`

### Item Components (`src/components/items/`) — 4 total
`ArticleItem, DepartmentItem, DoctorItem, ServiceItem`

### Form Components (`src/components/form/`) — 8 total
`DateTimePicker, DepartmentPicker, DoctorSelector, FabForm, FormItem, SearchInput, SymptomInquiry, TextareaWithImageUpload`

## §3 State Stores (`src/state.ts`)

| # | Atom | Type | Category |
|---|------|------|----------|
| 1 | `servicesState` | `atom<Promise<Service[]>>` | Listing |
| 2 | `doctorsState` | `atom<Promise<Doctor[]>>` | Listing |
| 3 | `availableTimeSlotsState` | `atom<Promise<AvailableTimeSlots[]>>` | Listing |
| 4 | `articlesState` | `atom<Promise<Article[]>>` | Listing |
| 5 | `departmentGroupsState` | `atom<Promise<DepartmentGroup[]>>` | Listing |
| 6 | `departmentsState` | `atom<Promise<Department[]>>` | Listing |
| 7 | `schedulesState` | `atom<Promise<Booking[]>>` | Listing |
| 8 | `invoicesState` | `atom<Promise<Invoice[]>>` | Listing |
| 9 | `symptomsState` | `atom<Promise<string[]>>` | Listing |
| 10 | `feedbackCategoriesState` | `atom<Promise<string[]>>` | Listing |
| 11 | `serviceByIdState` | `atomFamily(id)` | Detail |
| 12 | `departmentByIdState` | `atomFamily(id)` | Detail |
| 13 | `scheduleByIdState` | `atomFamily(id)` | Detail |
| 14 | `newsByIdState` | `atomFamily(id)` | Detail |
| 15 | `departmentHierarchyState` | `atom(async)` | Computed |
| 16 | `searchResultState` | `atomFamily(keyword) + loadable` | Computed |
| 17 | `userState` | `atomWithRefresh` | ZMP SDK |
| 18 | `symptomFormState` | `atomWithReset<SymptomDescription>` | Form |
| 19 | `bookingFormState` | `atomWithReset<BookingForm>` | Form |
| 20 | `askFormState` | `atomWithReset<Inquiry>` | Form |
| 21 | `feedbackFormState` | `atomWithReset<Feedback>` | Form |
| 22 | `customTitleState` | `atom("")` | Misc |

## §4 Services

| # | Service | File | Endpoints |
|---|---------|------|-----------|
| — | (mock only) | `src/utils/mock.ts` | 10 mock factories |

> ⚠️ No real API service layer yet — all data is mocked. Migration needed.

## §5 Custom Hooks (`src/hooks.ts`)

| # | Hook | File | Purpose |
|---|------|------|---------|
| 1 | `useRouteHandle` | `src/hooks.ts` | Read route `handle` metadata |
| 2 | `useRealHeight` | `src/hooks.ts` | ResizeObserver height tracking |

## §6 Types (`src/types.d.ts`)

`Service, TimeSlot, AvailableTimeSlots, Doctor, SymptomDescription, Inquiry, Feedback, Booking, Invoice, DepartmentGroup, Department, Article` — 12 interfaces

## §7 Feature Summary
```
Total Pages:        16 (15 routes + 404)
Total Components:   18 shell/shared + 16 icons + 4 items + 8 form = 46
Total Atoms:        22
Total Hooks:        2
Total Utils:        12
Total Types:        12
Total Mock Factories: 10
Project Status:     FULL HEALTHCARE SPA (mock data, no real API)
```
