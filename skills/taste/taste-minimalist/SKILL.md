---
name: taste-minimalist
description: Premium utilitarian minimalism design paradigm for plan-phase injection. Clean editorial-style interfaces with warm monochrome palette, typographic contrast, flat bento grids, muted pastels. Notion/Linear aesthetic. No gradients, no heavy shadows.
---

# Premium Utilitarian Minimalism Design Paradigm

This skill is a **plan-phase** design paradigm. When injected into a planner/architect agent, it informs the Design Specification section of plan.md with minimalist design decisions. The implementation agent then follows the plan using taste-core guardrails.

## 1. Negative Constraints (Banned Elements)

* NO Inter, Roboto, or Open Sans typefaces.
* NO generic thin-line icon libraries (Lucide, Feather, standard Heroicons).
* NO Tailwind default heavy shadows (`shadow-md`, `shadow-lg`, `shadow-xl`). Shadows must be ultra-diffuse, opacity < 0.05.
* NO primary-colored backgrounds for large sections.
* NO gradients, neon colors, or 3D glassmorphism (beyond subtle navbar blurs).
* NO `rounded-full` for large containers, cards, or primary buttons.
* NO emojis anywhere.
* NO generic placeholder names or AI copywriting clichés.

## 2. Typographic Architecture

Extreme typographic contrast establishes the editorial feel.

* **Primary Sans-Serif (Body, UI):** `'SF Pro Display', 'Geist Sans', 'Helvetica Neue', 'Switzer', sans-serif`.
* **Editorial Serif (Hero Headings & Quotes):** `'Lyon Text', 'Newsreader', 'Playfair Display', 'Instrument Serif', serif`. Tight tracking (`-0.02em` to `-0.04em`), tight line-height (`1.1`).
* **Monospace (Code, Keystrokes, Meta-data):** `'Geist Mono', 'SF Mono', 'JetBrains Mono', monospace`.
* **Text Colors:** Body never pure black. Use off-black (`#111111` or `#2F3437`), line-height `1.6`. Secondary: muted gray (`#787774`).

## 3. Color Palette (Warm Monochrome + Spot Pastels)

Color is a scarce resource, used only for semantic meaning or subtle accents.

* **Canvas:** Pure White `#FFFFFF` or Warm Bone `#F7F6F3` / `#FBFBFA`.
* **Primary Surface (Cards):** `#FFFFFF` or `#F9F9F8`.
* **Borders/Dividers:** Ultra-light gray `#EAEAEA` or `rgba(0,0,0,0.06)`.
* **Accent Colors (muted pastels only):**
  - Pale Red: `#FDEBEC` (Text: `#9F2F2D`)
  - Pale Blue: `#E1F3FE` (Text: `#1F6C9F`)
  - Pale Green: `#EDF3EC` (Text: `#346538`)
  - Pale Yellow: `#FBF3DB` (Text: `#956400`)

## 4. Component Specifications

* **Bento Grids:** Asymmetrical CSS Grid. Cards: `border: 1px solid #EAEAEA`, radius `8px`-`12px` max, padding `24px`-`40px`.
* **CTA Buttons:** Solid `#111111` bg, `#FFFFFF` text. Radius `4px`-`6px`. No box-shadow. Hover: `#333333` or `scale(0.98)`.
* **Tags/Badges:** Pill-shaped, `text-xs`, uppercase, tracking `0.05em`. Background uses muted pastels.
* **Accordions:** Strip container boxes. Separate only with `border-bottom: 1px solid #EAEAEA`. Clean `+`/`-` toggle.
* **Keystrokes:** `<kbd>` tags with `border: 1px solid #EAEAEA`, `radius: 4px`, `bg: #F7F6F3`, monospace font.
* **Faux-OS Chrome:** Minimalist container with white top bar + three small gray circles (macOS controls).

## 5. Iconography & Imagery

* **Icons:** Phosphor Icons (Bold/Fill) or Radix UI Icons. Standardize stroke width.
* **Illustrations:** Monochromatic continuous-line ink sketches + single offset pastel geometric shape.
* **Photography:** High-quality, desaturated, warm tone. Subtle warm grain overlay (`opacity: 0.04`). Use `picsum.photos/seed/{context}` when no real assets.
* **Section Backgrounds:** Never empty flat. Use subtle imagery at low opacity, soft radial light spots (`opacity: 0.03`), or minimal geometric line patterns.

## 6. Motion Guidelines

Motion should feel invisible — present but never distracting.

* **Scroll Entry:** `translateY(12px)` + `opacity: 0` → resolved over `600ms` with `cubic-bezier(0.16, 1, 0.3, 1)`. Use `IntersectionObserver`, never `scroll` listener.
* **Hover:** Cards lift with ultra-subtle shadow shift (`0 2px 8px rgba(0,0,0,0.04)` over `200ms`). Buttons `scale(0.98)` on `:active`.
* **Staggered Reveals:** `animation-delay: calc(var(--index) * 80ms)`. Never mount everything at once.
* **Ambient (Optional):** Single slow radial gradient blob (`20s+`, `opacity: 0.02-0.04`), `position: fixed; pointer-events: none`. Never on scrolling containers.

## Plan Output Directive

When writing the Design Specification section of plan.md, include:
1. **Canvas choice:** Pure white or warm bone background
2. **Typography system:** Specific serif/sans/mono stack with sizes and weights
3. **Color tokens:** Exact hex values for canvas, surfaces, borders, and chosen pastel accents
4. **Component palette:** Which component patterns to use (bento grid, kbd, faux-OS chrome, etc.)
5. **Iconography:** Specific icon library and stroke weight
6. **Motion profile:** Entry animation style, hover behavior, stagger timing
