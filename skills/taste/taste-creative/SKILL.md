---
name: taste-creative
description: Advanced creative design patterns and paradigm selection for premium UI. Plan-phase skill that drives design decisions — variance engine with vibe/layout archetypes, haptic micro-aesthetics, motion choreography, bento paradigm, and a comprehensive creative arsenal. Inject into planner/architect agents for frontend tasks requiring creative/premium UI.
---

# Creative Design Paradigm (Plan Phase)

This skill is a **plan-phase** design paradigm. When injected into a planner/architect agent, it drives design decisions and produces a Design Specification section in plan.md. The implementation agent then follows the plan using taste-core guardrails.

**Combination rule:** When injected alongside `taste-brutalist` or `taste-minimalist`, the companion paradigm's constraints take precedence over conflicting patterns in this skill. Ignore Creative Arsenal items that violate the companion's bans (e.g., skip Glassmorphism/Holographic patterns when combined with brutalist's no-gradients rule; skip heavy motion when combined with minimalist's invisible-motion principle). The companion paradigm narrows the creative space — this skill provides the structural framework and remaining compatible options.

## 1. Variance Engine

Before writing the design spec, select ONE combination from each archetype based on the project context. This ensures unique, tailored output.

### A. Vibe & Texture Archetypes (Pick 1)

1. **Ethereal Glass (SaaS / AI / Tech):** OLED black (`#050505`), radial mesh gradients (subtle glowing orbs). Vantablack cards with `backdrop-blur-2xl` and `white/10` hairlines. Wide geometric Grotesk typography.
2. **Editorial Luxury (Lifestyle / Real Estate / Agency):** Warm creams (`#FDFBF7`), muted sage, deep espresso. High-contrast Variable Serif for massive headings. CSS noise/film-grain overlay (`opacity-[0.03]`) for paper feel.
3. **Soft Structuralism (Consumer / Health / Portfolio):** Silver-grey or white backgrounds. Massive bold Grotesk typography. Floating components with highly diffused ambient shadows.

### B. Layout Archetypes (Pick 1)

1. **Asymmetrical Bento:** Masonry-like CSS Grid (`col-span-8 row-span-2` next to stacked `col-span-4`). Mobile: single-column `grid-cols-1` with generous `gap-6`.
2. **Z-Axis Cascade:** Stacked like physical cards, slightly overlapping with varying depth, subtle rotation (`-2deg` / `3deg`). Mobile: remove rotations/overlaps, standard vertical stack.
3. **Editorial Split:** Massive typography left half (`w-1/2`), scrollable interactive cards right half. Mobile: full-width vertical stack.

### C. Design Dials (Tuning Parameters)

* **DESIGN_VARIANCE** (1-10): 1-3 = symmetric grids, equal paddings. 8-10 = masonry, fractional grid units, massive empty zones.
* **MOTION_INTENSITY** (1-10): 1-3 = CSS hover/active only. 8-10 = scroll-triggered choreography, parallax.
* **VISUAL_DENSITY** (1-10): 1-3 = art gallery whitespace. 8-10 = cockpit mode, 1px lines, monospace numbers.

Default: (8, 6, 4). Adapt based on user context.

## 2. Haptic Micro-Aesthetics

### The Double-Bezel (Doppelrand / Nested Architecture)
Premium cards/containers must look like machined hardware — a glass plate in an aluminum tray:
* **Outer Shell:** `bg-black/5` or `bg-white/5`, hairline border (`ring-1 ring-black/5`), `p-1.5`-`p-2`, large radius (`rounded-[2rem]`).
* **Inner Core:** Own background, inner highlight (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`), mathematically smaller radius (`rounded-[calc(2rem-0.375rem)]`).

### Button-in-Button CTA
Primary buttons: rounded pills (`rounded-full`, `px-6 py-3`). Trailing arrow icon nested in its own circular wrapper (`w-8 h-8 rounded-full bg-black/5`) flush with the button's right padding.

### Spatial Rhythm & Tension
* **Macro-Whitespace:** Double standard padding. `py-24` to `py-40` for sections.
* **Eyebrow Tags:** Microscopic pill badges (`rounded-full px-3 py-1 text-[10px] uppercase tracking-[0.2em]`) preceding H1/H2s.

## 3. Motion Choreography

### Fluid Island Navigation
* **Closed:** Floating glass pill, detached from top (`mt-6`, `mx-auto`, `w-max`, `rounded-full`).
* **Hamburger Morph:** Lines fluidly rotate/translate to form `X` (not disappear).
* **Modal Expansion:** Screen-filling overlay with `backdrop-blur-3xl bg-black/80`.
* **Staggered Mask Reveal:** Links slide up from `translate-y-12 opacity-0` with staggered delays.

### Magnetic Button Hover Physics
* Scale down on active (`active:scale-[0.98]`).
* Inner icon translates diagonally (`group-hover:translate-x-1 group-hover:-translate-y-[1px]`) and scales up.

### Scroll Interpolation (Entry Animations)
* Elements enter with heavy fade-up: `translate-y-16 blur-md opacity-0` → `translate-y-0 blur-0 opacity-100` over `800ms+`.
* Use `IntersectionObserver` or Framer Motion `whileInView`. Never `scroll` event listener.

### All transitions use custom cubic-beziers
`transition-all duration-700 ease-[cubic-bezier(0.32,0.72,0,1)]`. No `linear` or `ease-in-out`.

## 4. Creative Arsenal

Pull from this library of advanced concepts to ensure striking, memorable output.

### Navigation & Menus
* Mac OS Dock Magnification: icons scale fluidly on hover
* Magnetic Button: physically pulls toward cursor
* Gooey Menu: sub-items detach like viscous liquid
* Dynamic Island: pill-shaped component morphing for status/alerts
* Contextual Radial Menu: circular menu expanding at click coordinates
* Floating Speed Dial: FAB springing into curved secondary actions
* Mega Menu Reveal: full-screen stagger-fade dropdowns

### Layout & Grids
* Bento Grid: asymmetric tile-based grouping
* Masonry Layout: staggered grid without fixed row heights
* Chroma Grid: borders/tiles with continuously animating color gradients
* Split Screen Scroll: two halves sliding in opposite directions
* Curtain Reveal: hero parting like a curtain on scroll

### Cards & Containers
* Parallax Tilt Card: 3D-tilting tracking mouse coordinates
* Spotlight Border Card: borders illuminate dynamically under cursor
* Glassmorphism Panel: frosted glass with inner refraction borders
* Holographic Foil Card: iridescent rainbow reflections on hover
* Tinder Swipe Stack: physical card stack user can swipe away
* Morphing Modal: button seamlessly expands into full-screen dialog

### Scroll Animations
* Sticky Scroll Stack: cards stick and physically stack over each other
* Horizontal Scroll Hijack: vertical scroll → smooth horizontal gallery pan
* Locomotive Scroll Sequence: video/3D tied directly to scrollbar
* Zoom Parallax: background image zooming in/out with scroll
* Scroll Progress Path: SVG lines drawing themselves on scroll
* Liquid Swipe Transition: viscous liquid page transitions

### Galleries & Media
* Dome Gallery: 3D panoramic dome
* Coverflow Carousel: 3D carousel, center focused, edges angled
* Drag-to-Pan Grid: boundless grid freely draggable
* Accordion Image Slider: strips expanding fully on hover
* Hover Image Trail: popping/fading image trail behind cursor
* Glitch Effect Image: RGB-channel shifting on hover

### Typography & Text
* Kinetic Marquee: endless text bands reversing/speeding on scroll
* Text Mask Reveal: typography as window to video background
* Text Scramble Effect: matrix-style character decoding on load/hover
* Circular Text Path: text curved along spinning circular path
* Gradient Stroke Animation: outlined text with running gradient stroke
* Kinetic Typography Grid: letters dodging/rotating away from cursor

### Micro-Interactions & Effects
* Particle Explosion Button: CTAs shatter into particles on success
* Liquid Pull-to-Refresh: detaching water droplet reload indicator
* Skeleton Shimmer: shifting light reflections on placeholder boxes
* Directional Hover Aware Button: fill entering from the mouse's entry side
* Ripple Click Effect: waves from click coordinates
* Animated SVG Line Drawing: vectors drawing contours in real-time
* Mesh Gradient Background: organic lava-lamp animated color blobs
* Lens Blur Depth: dynamic focus blur on background layers

## 5. Bento Paradigm (Motion-Engine)

For SaaS dashboards or feature sections, use this "Vercel-meets-Dribbble" architecture:

### Design Philosophy
* **Palette:** Background `#f9fafb`. Cards pure white with `border-slate-200/50`.
* **Surfaces:** `rounded-[2.5rem]` for major containers. Diffusion shadow: `shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`.
* **Typography:** Strict `Geist`/`Satoshi`/`Cabinet Grotesk`. `tracking-tight` for headers.
* **Labels:** Titles/descriptions placed **outside and below** cards (gallery-style).

### Animation Engine (Perpetual Motion)
* Spring Physics: `type: "spring", stiffness: 100, damping: 20`.
* Layout Transitions: Heavy use of `layout` and `layoutId`.
* Infinite Loops: Every card has an "Active State" looping infinitely (Pulse, Typewriter, Float, Carousel).

### Card Archetypes
1. **Intelligent List:** Auto-sorting loop with `layoutId` swaps simulating AI prioritization.
2. **Command Input:** Multi-step Typewriter with blinking cursor and shimmering loading gradient.
3. **Live Status:** Breathing indicators with Overshoot spring pop-up badges.
4. **Wide Data Stream:** Infinite Carousel (`x: ["0%", "-100%"]`) with seamless looping.
5. **Contextual UI:** Staggered text highlight followed by float-in action toolbar.

## Plan Output Directive

When writing the Design Specification section of plan.md, include:
1. **Chosen vibe archetype:** Ethereal Glass / Editorial Luxury / Soft Structuralism (or custom)
2. **Chosen layout archetype:** Asymmetrical Bento / Z-Axis Cascade / Editorial Split (or custom)
3. **Dial values:** DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY
4. **Color palette:** Exact hex values for background, surfaces, accents
5. **Typography system:** Font stack, headline/body/mono specifications
6. **Component patterns:** Which creative arsenal items to use (from §4)
7. **Motion strategy:** Entry animations, hover physics, scroll behavior, perpetual animations
8. **Haptic details:** Double-Bezel usage, CTA architecture, spatial rhythm choices
9. **Bento layout:** If applicable, specify card archetypes and grid structure
