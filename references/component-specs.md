# Component Specifications

## Button

| Property | Default | Hover | Active | Disabled |
|----------|---------|-------|--------|----------|
| Background | primary | primary-dark | primary-darker | muted |
| Text | white | white | white | muted-fg |
| Border | none | none | none | muted-border |
| Shadow | sm | md | none | none |
| Cursor | pointer | pointer | pointer | not-allowed |
| Transition | 150ms | 150ms | 150ms | none |

## Input

| Property | Default | Focus | Error | Disabled |
|----------|---------|-------|-------|----------|
| Background | white | white | white | surface-alt |
| Border | border | border-focus | error | muted-border |
| Text | text | text | text | muted-fg |
| Label | text-secondary | text | error | muted-fg |
| Helper | text-muted | text-muted | error | muted-fg |
| Shadow | none | sm | none | none |

## Card

| Property | Default | Hover | Elevated |
|----------|---------|-------|----------|
| Background | white | white | white |
| Border | border | border-focus | border |
| Shadow | none | md | lg |
| Radius | lg | lg | xl |
| Padding | lg | lg | lg |

## Modal

| Property | Value |
|----------|-------|
| Overlay | bg-black/50 |
| Background | white |
| Shadow | xl |
| Radius | xl |
| Max Width | 32rem |
| Padding | xl |
| Animation | fade-in + scale |
| Focus Trap | yes |

## Toast

| Property | Value |
|----------|-------|
| Background | white |
| Shadow | lg |
| Radius | lg |
| Padding | md lg |
| Duration | 3000ms auto-dismiss |
| Position | bottom-right |
| Animation | slide-in-right |

## Navigation

| Property | Value |
|----------|-------|
| Height | 64px |
| Background | white/80 blur |
| Shadow | sm on scroll |
| Active | primary text + bottom border |
| Hover | text-secondary |
| Transition | 150ms |

## Table

| Property | Value |
|----------|-------|
| Header BG | surface |
| Header Text | text-secondary |
| Row Hover | surface-alt |
| Border | border |
| Cell Padding | md |
| Font Size | sm |
