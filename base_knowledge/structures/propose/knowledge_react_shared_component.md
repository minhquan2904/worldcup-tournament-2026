---
title: React Shared Component Knowledge
tag: "@AI-ONLY"
generated: "2026-04-16"
source_skill: learn-react-shared-component
---

# React Shared Components — pretty-little-shop-vn

## §1 Shared Component Inventory

| Component | File | Category | Props Interface |
|-----------|------|----------|--------------------|
| Button | `components/button.tsx` | UI (interactive) | `ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement>` |
| Section | `components/section.tsx` | Layout | `SectionProps` |
| Tabs | `components/tabs.tsx` | UI (navigation) | TBD |
| PolarizedList | `components/polarized-list.tsx` | Layout | TBD |
| MarkedTitleSection | `components/marked-title-section.tsx` | Layout | TBD |
| RemoteDiagnosisItem | `components/remote-diagnosis-item.tsx` | Data | TBD |
| DashedDivider | `components/dashed-divider.tsx` | UI | none |
| HorizontalDivider | `components/horizontal-divider.tsx` | UI | none |
| TransitionLink | `components/transition-link.tsx` | Navigation | `TransitionLinkProps extends NavLinkProps` |
| ArticleItem | `components/items/article.tsx` | Data | `Article` |
| DepartmentItem | `components/items/department.tsx` | Data | `Department` |
| DoctorItem | `components/items/doctor.tsx` | Data | `Doctor` |
| ServiceItem | `components/items/service.tsx` | Data | `Service` |

## §2 Component Details

### Button — `src/components/button.tsx`
```tsx
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  loading?: boolean;
  onDisabledClick?: () => void;
}
export const Button: FC<ButtonProps>
```
- Full-width (`w-full h-12 rounded-full`)
- Gradient: `bg-gradient-to-br from-primary to-primary-gradient`
- Shadow: `shadow shadow-highlight`
- Loading: spinner overlay (`animate-spin`) + content hidden
- Disabled: `#E1E1E1CC` overlay
- `onDisabledClick`: called when button is disabled (for UX feedback)
- `startViewTransition` NOT called here — only on navigation

### Section — `src/components/section.tsx`
```tsx
interface SectionProps {
  children: ReactNode;
  className?: string;
  title?: string;
  viewMore?: To;     // react-router-dom To
  isCard?: boolean;
}
```
- `isCard=true`: white card `bg-white rounded-xl p-3.5`
- `isCard=false`: plain with optional title header
- `viewMore`: TransitionLink → ArrowRightIcon

### TransitionLink — `src/components/transition-link.tsx`
```tsx
interface TransitionLinkProps extends NavLinkProps {}
export default function TransitionLink(props: TransitionLinkProps) {
  return <NavLink {...props} viewTransition />;
}
```
- Wraps `NavLink` from react-router-dom
- Enables CSS View Transition API on navigation
- Children render prop: `children({ isActive })`

## §3 Icon Components (`src/components/icons/`)

All SVG components, pattern:
```tsx
// Pattern A: plain SVG (no props)
export function ArrowRightIcon({ className }: { className?: string }) {}

// Pattern B: active state (footer icons)
interface IconProps { active?: boolean; }
export function HomeIcon({ active }: IconProps) {}  // fill changes on active
```

| Icon | `active` prop | Notes |
|------|---------------|-------|
| ArrowRight | no | Chevron right |
| Back | no | Back arrow |
| BigPlus | no | FAB center button with shadow |
| Call | no | Phone icon |
| Cart | ✅ | Schedule/calendar icon (footer) |
| Check | no | Checkmark |
| ChevronDown | no | Dropdown chevron |
| Explore | ✅ | Explore/compass (footer) |
| FooterWave | no | SVG wave decoration |
| HeaderShield | no | Header decoration |
| Home | ✅ | Home (footer) |
| PlusIcon | no | Small plus |
| Profile | ✅ | Person (footer) |
| Search | no | Magnifier |
| Ship | no | Hospital/ship icon |
| Success | no | Success checkmark (large) |

## §4 Design Principles Observed

1. **Props extend HTML attributes** — `Button extends ButtonHTMLAttributes` (spread safe)
2. **Render prop pattern** — `TransitionLink children({ isActive })`
3. **Tailwind only** — NO ZMP UI components, NO inline styles (except dynamic)
4. **No default export for named exports** — `export const Button`, `export function ErrorBoundary`
5. **Default export for page/layout components** — `export default Section`, `export default TransitionLink`
6. **TypeScript `To` type** for navigation destinations — `import { To } from "react-router-dom"`
7. **SVG as TSX** — all icons are inline SVG React components (no external SVG files for icons)
8. **`active?: boolean`** on footer icons — drives fill/stroke toggling

## §5 Shared Component Template

```tsx
// Named UI component
interface FeatureComponentProps {
  className?: string;
  children?: ReactNode;
  // ... specific props
}

export const FeatureComponent: FC<FeatureComponentProps> = ({
  className,
  children,
  ...rest
}) => {
  return <div className={`base-classes ${className || ""}`}>{children}</div>;
};
```

```tsx
// Icon SVG component
interface IconProps {
  active?: boolean;
  className?: string;
}

export function FeatureIcon({ active, className }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" className={className}>
      <path fill={active ? "currentColor" : "#9CA3AF"} d="..." />
    </svg>
  );
}
```

xref: react_component, react_hook_helper
