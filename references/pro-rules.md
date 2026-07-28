# Pro Rules & Pre-Delivery Checklist

## Icon & Visual Element Discipline

- Use SVG icons from Heroicons or Lucide
- Never use emoji as functional icons
- Icons must have visible labels or aria-labels
- Consistent icon style throughout project
- Minimum icon size 16px for inline 24px for standalone

## Interaction Feedback

- All clickable elements have cursor-pointer
- Hover states with smooth transitions 150-300ms
- Active/pressed states for buttons
- Loading states for async actions
- Success/error feedback for user actions
- Focus rings visible for keyboard navigation

## Light/Dark Mode Contrast

- Test all text in both light and dark modes
- Minimum 4.5:1 contrast ratio in both modes
- Avoid pure black (#000) on pure white (#FFF)
- Use slightly muted backgrounds in dark mode
- Ensure shadows work in both themes

## Safe Area Layout

- Account for notch on mobile devices
- Respect safe-area-inset-* CSS properties
- Test on actual devices not just browser resize
- Consider landscape orientation on tablets

## Accessibility

- Screen reader test for critical flows
- ARIA labels on all interactive elements
- Focus management for modals and overlays
- Skip navigation link for keyboard users
- Form error announcements via aria-live

## Performance Budget

- First Contentful Paint < 1.5s
- Largest Contentful Paint < 2.5s
- Cumulative Layout Shift < 0.1
- Total bundle size < 200KB initial
- Image formats: WebP/AVIF with fallbacks

## Code Quality

- No hardcoded colors use design tokens
- Consistent naming conventions
- TypeScript for new projects
- Component props properly typed
- No unused imports or variables

## Pre-Delivery Checklist

- [ ] cursor-pointer on all clickable elements
- [ ] Hover states with smooth transitions 150-300ms
- [ ] Text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard nav
- [ ] prefers-reduced-motion respected
- [ ] Responsive: 375px 768px 1024px 1440px
- [ ] No hardcoded colors use design tokens
- [ ] SVG icons no emoji as icons
- [ ] Min touch target 44×44px
- [ ] Error messages near relevant fields
- [ ] Back button works correctly
- [ ] Images optimized WebP/AVIF
- [ ] CLS < 0.1 no layout shift
- [ ] Font loading optimized font-display swap
- [ ] Screen reader tested for critical flows
