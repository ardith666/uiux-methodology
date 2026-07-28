# Token Architecture

## Three-Layer Structure

```
Primitive (raw values)
       ↓
Semantic (purpose aliases)
       ↓
Component (component-specific)
```

## Primitive Tokens

Raw design values without semantic meaning.

```css
:root {
  /* Colors */
  --color-blue-50: #EFF6FF;
  --color-blue-100: #DBEAFE;
  --color-blue-500: #3B82F6;
  --color-blue-600: #2563EB;
  --color-blue-700: #1D4ED8;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;

  /* Typography */
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}
```

## Semantic Tokens

Purpose-driven aliases referencing primitive tokens.

```css
:root {
  /* Colors */
  --color-primary: var(--color-blue-600);
  --color-primary-light: var(--color-blue-500);
  --color-primary-dark: var(--color-blue-700);

  /* Surfaces */
  --color-background: #FFFFFF;
  --color-surface: var(--color-blue-50);
  --color-surface-alt: var(--color-blue-100);

  /* Text */
  --color-text: #1F2937;
  --color-text-secondary: #6B7280;
  --color-text-muted: #9CA3AF;

  /* Borders */
  --color-border: #E5E7EB;
  --color-border-focus: var(--color-primary);

  /* Status */
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;
}
```

## Component Tokens

Component-specific tokens referencing semantic tokens.

```css
:root {
  /* Button */
  --button-bg: var(--color-primary);
  --button-bg-hover: var(--color-primary-dark);
  --button-text: #FFFFFF;
  --button-radius: var(--radius-md);

  /* Input */
  --input-bg: #FFFFFF;
  --input-border: var(--color-border);
  --input-border-focus: var(--color-border-focus);
  --input-text: var(--color-text);

  /* Card */
  --card-bg: #FFFFFF;
  --card-border: var(--color-border);
  --card-shadow: var(--shadow-sm);
  --card-radius: var(--radius-lg);
  --card-padding: var(--space-6);
}
```

## Naming Convention

```
--{category}-{property}-{variant}-{state}

Examples:
--button-bg-primary-hover
--input-border-focus
--card-shadow-lg
--text-color-secondary
```

## Dark Mode

Override semantic tokens for dark mode.

```css
[data-theme="dark"] {
  --color-background: #0F172A;
  --color-surface: #1E293B;
  --color-surface-alt: #334155;
  --color-text: #F1F5F9;
  --color-text-secondary: #94A3B8;
  --color-border: #334155;
}
```

## Best Practices

1. Never use primitive tokens directly in components
2. Always reference semantic tokens
3. Use HSL format for opacity control
4. Document every token's purpose
5. Keep naming consistent
6. Theme switching via semantic layer only
