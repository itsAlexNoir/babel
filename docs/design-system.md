# Frontend design system

The frontend follows an **editorial** direction: warm paper neutrals, hairline
rules instead of card boxes, a serif voice for titles, and one spot color
(navy) carrying links, focus and selection. Everything lives in one file,
[`frontend/src/app.css`](../frontend/src/app.css), as CSS custom properties.

## Why two sets of token names

`app.css` defines a set of **core tokens** (`--color-paper`, `--color-ink`,
`--color-spot`, …) and a set of **legacy aliases** (`--color-bg`,
`--color-text`, `--color-primary`, …) that point at them:

```css
--color-bg: var(--color-paper);
--color-text: var(--color-ink);
--color-primary: var(--color-ink);
```

The legacy names are what the app's components were actually written
against before this palette existed, and most of them (`BookForm`, the
Stats/Data/Scan pages) were never touched during the redesign — they still
reference `--color-border`, `--color-text-secondary`, and so on. Because
those are aliases rather than duplicated values, repointing the ten core
tokens repaints the entire app, dark mode included, without editing a
single one of those components.

**When touching CSS:** new code should use the core token names directly
(`var(--color-ink)`, not `var(--color-text)`) — the aliases exist for
backward compatibility with pre-redesign components, not as a second
naming convention to keep extending.

## Core tokens

| Token | Light | Dark | Use |
| --- | --- | --- | --- |
| `--color-paper` | `#ffffff` | `#100b08` | Page background |
| `--color-paper-2` | `#fdfbf8` | `#1f1916` | Subtle fills (hover rows) |
| `--color-rule-faint` | `#ece9e4` | `#2c2521` | Row dividers |
| `--color-rule` | `#ddd8d3` | `#3b3430` | Borders, input underlines |
| `--color-rule-strong` | `#c2bdb6` | `#544b46` | Hover borders |
| `--color-faint` | `#98918a` | `#7b736d` | Placeholders, disabled — **not body text** (~3.1:1) |
| `--color-muted` | `#69625b` | `#a49d97` | Secondary text (~6:1) |
| `--color-sub` | `#423c36` | `#d5d0cc` | Body text (~11:1) |
| `--color-ink` | `#16100b` | `#f4f1ee` | Primary text, primary-button fill |
| `--color-spot` | `#254974` | `#67a7f7` | Links, focus, selection |
| `--color-danger` | `#8a3028` | `#e67a73` | Destructive actions |
| `--color-avail` | `#2b5f39` | `#69ba7c` | "On shelf" status |
| `--color-out` | `#7a511f` | `#e29e47` | "On loan" status |

Each status color also has a `--color-tint-*` / `--color-ink-*` pair (e.g.
`--color-tint-avail` / `--color-ink-avail`) for badge and toast backgrounds —
a low-saturation ground with a matching high-contrast ink, ≥7:1 in both
themes.

All of the above were generated in [oklch](https://oklch.com) and
gamut-fitted to sRGB rather than picked by eye: the four status hues
(`spot`/`danger`/`avail`/`out`) share one lightness and chroma in each
theme and differ only in hue, which is why they read as a coherent set
rather than four unrelated colors.

## Typography

- **`--font-serif`** (Instrument Serif) — book titles, page headings (`h1`–`h3`).
- **`--font-body`** (Instrument Sans) — everything else.
- **`--font-mono`** (JetBrains Mono) — figures that should align: years,
  counts, shelf marks (`.mono` class, `font-variant-numeric: tabular-nums`).

## Dark mode

Two mechanisms redefine the core tokens (never the aliases — see above):

```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme='light']) { /* ... */ }
}
:root[data-theme='dark'] { /* ... */ }
```

The media query follows the OS setting by default. An explicit choice —
made via the sun/moon toggle in the masthead
([`+layout.svelte`](../frontend/src/routes/+layout.svelte)) — sets
`data-theme` on `<html>` and is persisted to `localStorage` under
`babel-theme`. A small blocking `<script>` in
[`app.html`](../frontend/src/app.html) applies a stored preference before
first paint, so there's no flash of the wrong theme on load.

**Known browser gotcha:** Chrome's UA stylesheet sets `color: black`
directly on `<dialog>` elements (not just as an inherited default), which
blocks normal CSS inheritance from `<body>`. This was invisible in light
mode — black is nearly identical to `--color-ink` there — but made every
dialog heading render pure black on a dark background. Both dialogs
(`BorrowDialog.svelte` and the delete-confirmation dialog in
`routes/books/[id]/+page.svelte`) set `color: var(--color-ink)` explicitly
on the `dialog` element itself to work around it. Any new `<dialog>` needs
the same explicit `color`.

## Generated covers

Books with no `cover_image_path` get a placeholder built from their own
data rather than a blank box: title, author and publisher rendered on a
tinted card, colored by a deterministic hash of the title (see
[`coverPalette.ts`](../frontend/src/lib/coverPalette.ts)). The eight
ground/ink pairs are fixed regardless of theme — a book's generated cover
looks the same in light and dark mode, the way a real dust jacket would.
`BookCover.svelte` renders this, or the real image when one exists, at
three sizes (`s` for list-row thumbnails — text is dropped entirely at
that size since it doesn't fit legibly, `m` for grid cards, `l` for the
detail page).

## Known limitations / left for later

- **Tag vocabulary has case-split duplicates** in the underlying data
  (e.g. "Literatura norteamericana" vs "Literatura Norteamericana" count
  as different tags) — a one-off data migration, not a styling or
  frontend-architecture problem, and intentionally out of scope here.
- **No decade filter.** Publisher and language are exposed as filters;
  decade was judged lower-value relative to the parsing complexity of the
  catalogue's free-text date fields and was left out.
- **List view on very narrow screens** collapses to a stacked layout via
  CSS rather than a true responsive redesign of the table — functional,
  not polished.
