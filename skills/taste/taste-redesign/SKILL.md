---
name: taste-redesign
description: Audit and upgrade existing UI to premium quality. Diagnoses generic patterns, applies targeted fixes working with the existing stack. Complements taste-core with redesign-specific checks.
---

# Redesign Skill

## How This Works

1. **Scan** — Read the codebase. Identify the framework, styling method, and current design patterns.
2. **Diagnose** — Run through the audit below. List every generic pattern, weak point, and missing state.
3. **Fix** — Apply targeted upgrades working with the existing stack. Do not rewrite from scratch.

## Design Audit

### Typography (Beyond Basics)
* Only Regular (400) and Bold (700) used — introduce Medium (500) and SemiBold (600) for subtle hierarchy.
* Numbers in proportional font — use monospace or `font-variant-numeric: tabular-nums` for data interfaces.
* Missing letter-spacing adjustments — negative tracking for large headers, positive for small caps/labels.
* All-caps subheaders everywhere — try lowercase italics, sentence case, or small-caps.
* Orphaned words on last line — fix with `text-wrap: balance` or `text-wrap: pretty`.

### Layout (Beyond Basics)
* No max-width container — add 1200-1440px constraint with auto margins.
* Cards of equal height forced by flexbox — allow variable heights or masonry.
* Uniform border-radius on everything — vary: tighter on inner elements, softer on containers.
* No overlap or depth — use negative margins for layering and visual depth.
* Symmetrical vertical padding — adjust optically (bottom often needs slightly more).
* Dashboard always has left sidebar — try top nav, floating command menu, or collapsible panel.
* Missing whitespace — double spacing. Dense layouts for data dashboards, not marketing pages.
* Buttons not bottom-aligned in card groups — pin CTAs to card bottom for clean horizontal lines.
* Inconsistent vertical rhythm — align shared elements across side-by-side items. Apply 1-2px optical adjustments where math centering looks wrong.

### Interactivity and States
* No hover states on buttons — add background shift, slight scale, or translate.
* No active/pressed feedback — add `scale(0.98)` or `translateY(1px)` on press.
* Instant transitions with zero duration — add 200-300ms transitions to interactive elements.
* Missing focus ring — visible focus indicators for keyboard navigation (accessibility requirement).
* Dead links to `#` — link to real destinations or visually disable.
* No active page indicator in navigation.
* Scroll jumping — add `scroll-behavior: smooth`.
* Animations using `top`/`left`/`width`/`height` — switch to `transform` and `opacity`.

### Component Patterns
* Generic card look (border + shadow + white bg) — remove border, or use only background/spacing.
* Accordion FAQ — use side-by-side list or inline progressive disclosure.
* Modals for everything — use inline editing, slide-over panels, or expandable sections.
* Avatar circles exclusively — try squircles or rounded squares.
* Footer link farm — simplify to main paths and legal links.

### Iconography
* Lucide/Feather exclusively — use Phosphor, Heroicons, or custom set.
* Inconsistent stroke widths — standardize to one weight.
* Missing favicon — always include one.

### Code Quality
* Div soup — use semantic HTML (`<nav>`, `<main>`, `<article>`, `<aside>`, `<section>`).
* Hardcoded pixel widths — use relative units (`%`, `rem`, `max-width`).
* Import hallucinations — verify every import exists in `package.json`.

### Strategic Omissions
* No "back" navigation — dead ends in user flows.
* No form validation (client-side).
* No "skip to content" link (keyboard accessibility).

## Upgrade Techniques

### Typography
* Variable font animation: interpolate weight/width on scroll or hover.
* Outlined-to-fill transitions: text starts as stroke outline, fills on scroll entry.

### Layout
* Broken grid / asymmetry: elements overlapping, bleeding off-screen with calculated randomness.
* Parallax card stacks: sections sticking and stacking during scroll.

### Motion
* Staggered entry: cascade with slight delays, Y-axis translation + opacity fade. Never mount all at once.
* Spring physics: replace linear easing with spring-based motion for natural, weighty feel.

### Surface
* True glassmorphism: `backdrop-filter: blur` + 1px inner border + subtle inner shadow for edge refraction.
* Spotlight borders: card borders illuminating dynamically under cursor.

## Fix Priority

Apply changes in this order for maximum impact with minimum risk:

1. **Font swap** — biggest instant improvement, lowest risk
2. **Color palette cleanup** — remove clashing or oversaturated colors
3. **Hover and active states** — makes the interface feel alive
4. **Layout and spacing** — proper grid, max-width, consistent padding
5. **Replace generic components** — swap cliche patterns for modern alternatives
6. **Add loading, empty, error states** — makes it feel finished
7. **Polish typography scale and spacing** — the premium final touch

## Rules

* Work with the existing tech stack. Do not migrate frameworks or styling libraries.
* Do not break existing functionality. Test after every change.
* Before importing any new library, check the project's dependency file first.
* If the project uses Tailwind, check version (v3 vs v4) before modifying config.
* Keep changes reviewable and focused. Small, targeted improvements over big rewrites.
