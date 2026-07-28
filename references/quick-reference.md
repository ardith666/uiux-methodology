# UX Quick Reference

## 1. Accessibility (Priority: CRITICAL)

- Contrast ratio 4.5:1 for normal text 3:1 for large text
- Alt text on all meaningful images
- Keyboard navigation for all interactive elements
- Visible focus indicators
- Semantic HTML (header nav main article section)
- ARIA labels on icon buttons
- Never use color alone to convey information
- Form labels always visible or via aria-label
- Respect prefers-reduced-motion
- Logical heading hierarchy

## 2. Touch & Interaction (Priority: CRITICAL)

- Minimum touch target 44×44px
- 8px+ spacing between touch targets
- Loading indicators for 300ms+ actions
- Button alternatives for gesture-only features
- Hover states but never hover-only critical info
- Subtle haptic feedback for confirmations

## 3. Performance (Priority: HIGH)

- WebP/AVIF images with responsive srcset
- Lazy loading below-fold content
- CLS < 0.1 reserve space for dynamic content
- font-display:swap for web fonts
- Code splitting and dynamic imports
- Debounce scroll/resize handlers
- Virtualize lists > 100 items

## 4. Style Selection (Priority: HIGH)

- Match style to product type
- Consistent design language
- SVG icons from Heroicons/Lucide never emoji
- Design tokens for all values
- Clear visual hierarchy

## 5. Layout & Responsive (Priority: HIGH)

- Mobile-first CSS
- No horizontal scroll
- Viewport meta with user-scalable=yes
- Breakpoints: 375px 768px 1024px 1440px
- max-width containers with responsive padding
- Sticky navigation for quick access

## 6. Typography & Color (Priority: MEDIUM)

- Base font size 16px minimum
- Line height 1.5 for body 1.2 for headings
- Line length 50-75 characters
- Max 2 font families
- Semantic color tokens not raw hex
- Test both light and dark modes
- Color-blind friendly combinations

## 7. Animation (Priority: MEDIUM)

- Duration 150-300ms
- ease-out for entering ease-in for exiting
- Always provide prefers-reduced-motion alternative
- Animate with purpose not decoration
- Exit animations faster than enter
- Spatial continuity in motion

## 8. Forms & Feedback (Priority: MEDIUM)

- Visible labels not placeholder-only
- Errors near relevant fields
- Helper text for complex inputs
- Progressive disclosure
- Correct input types (email tel url)
- Auto-focus first input on form pages

## 9. Navigation (Priority: HIGH)

- Back button always works
- Bottom nav max 5 items
- Deep linking for all important pages
- Breadcrumbs for nested navigation > 2 levels
- Active state clearly indicated
- Search for content-heavy sites

## 10. Charts & Data (Priority: LOW)

- Legends for multi-series charts
- Interactive tooltips with values
- Color-blind friendly palettes
- Data labels for key points
- Responsive charts for all screens
