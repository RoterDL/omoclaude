---
name: taste-creative
description: Advanced creative design patterns for premium UI. Includes liquid glass, magnetic physics, perpetual micro-interactions, bento paradigm, and creative arsenal concepts.
---

# Creative Design Patterns

## 1. Creative Proactivity (Anti-Slop Implementation)

* **Liquid Glass Refraction:** Beyond `backdrop-blur`. Add `border-white/10` inner border + `shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]` inner shadow for physical edge refraction.
* **Magnetic Micro-physics (MOTION_INTENSITY > 5):** Buttons pull toward cursor. **CRITICAL:** NEVER use `useState` for magnetic hover or continuous animations. Use EXCLUSIVELY Framer Motion `useMotionValue` + `useTransform` outside React render cycle.
* **Perpetual Micro-Interactions (MOTION_INTENSITY > 5):** Embed continuous infinite animations (Pulse, Typewriter, Float, Shimmer, Carousel) in standard components. Apply Spring Physics (`type: "spring", stiffness: 100, damping: 20`) to all interactive elements — no linear easing.
* **Layout Transitions:** Always use Framer Motion `layout` and `layoutId` for smooth re-ordering, resizing, and shared element transitions.
* **Staggered Orchestration:** Never mount lists instantly. Use `staggerChildren` (Framer) or CSS cascade (`animation-delay: calc(var(--index) * 100ms)`). **CRITICAL:** Parent (`variants`) and Children MUST reside in the identical Client Component tree.

## 2. Technical Reference (Dials — Extreme Values)

### DESIGN_VARIANCE
* **1-3 (Predictable):** Flexbox `justify-center`, strict 12-column symmetrical grids, equal paddings.
* **8-10 (Asymmetric):** Masonry layouts, CSS Grid fractional units (`grid-template-columns: 2fr 1fr 1fr`), massive empty zones (`padding-left: 20vw`).
* **Mobile Override (4-10):** Asymmetric layouts above `md:` MUST fall back to single-column (`w-full`, `px-4`, `py-8`) on `< 768px`.

### MOTION_INTENSITY
* **1-3 (Static):** No auto-animations. CSS `:hover`/`:active` only.
* **8-10 (Choreography):** Complex scroll-triggered reveals or parallax. Use Framer Motion hooks. NEVER use `window.addEventListener('scroll')`.

### VISUAL_DENSITY
* **1-3 (Art Gallery):** Lots of whitespace. Huge section gaps. Expensive and clean.
* **8-10 (Cockpit):** Tiny paddings. No card boxes; 1px lines to separate data. **Mandatory:** Monospace (`font-mono`) for all numbers.

## 3. Creative Arsenal

When appropriate, leverage **GSAP (ScrollTrigger/Parallax)** for scrolltelling or **ThreeJS/WebGL** for 3D/Canvas animations. **CRITICAL:** Never mix GSAP/ThreeJS with Framer Motion in the same component tree. Default to Framer Motion for UI. Use GSAP/ThreeJS exclusively for isolated full-page scrolltelling or canvas backgrounds in strict `useEffect` cleanup blocks.

### Hero Paradigm
* Asymmetric hero sections: text aligned left/right, high-quality background with subtle stylistic fade into background color.

### Navigation
* Mac OS Dock Magnification: icons scale fluidly on hover.
* Magnetic Button: physically pulls toward cursor.

### Layout & Grids
* Bento Grid: asymmetric tile-based grouping.
* Masonry Layout: staggered grid without fixed row heights.

### Cards & Containers
* Parallax Tilt Card: 3D-tilting tracking mouse coordinates.
* Spotlight Border Card: borders illuminate dynamically under cursor.

### Scroll-Animations
* Sticky Scroll Stack: cards stick and physically stack on scroll.
* Horizontal Scroll Hijack: vertical scroll translates into horizontal gallery pan.

### Typography & Text
* Kinetic Marquee: endless text bands reversing/speeding on scroll.
* Text Mask Reveal: typography as transparent window to video background.

### Micro-Interactions
* Particle Explosion Button: CTAs shatter into particles on success.
* Skeleton Shimmer: shifting light reflections across placeholder boxes.

## 4. Bento Paradigm (Motion-Engine)

### A. Design Philosophy
* **Aesthetic:** High-end, minimal, functional.
* **Palette:** Background `#f9fafb`. Cards pure white with `border-slate-200/50`.
* **Surfaces:** `rounded-[2.5rem]` for major containers. Diffusion shadow: `shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`.
* **Typography:** Strict `Geist`/`Satoshi`/`Cabinet Grotesk`. `tracking-tight` for headers.
* **Labels:** Titles/descriptions placed outside and below cards (gallery-style).

### B. Animation Engine (Perpetual Motion)
* **Spring Physics:** No linear easing. `type: "spring", stiffness: 100, damping: 20`.
* **Layout Transitions:** Heavy use of `layout` and `layoutId` for smooth transitions.
* **Infinite Loops:** Every card has an "Active State" looping infinitely (Pulse, Typewriter, Float, Carousel).
* **Performance:** Wrap in `<AnimatePresence>`, 60fps. Perpetual motion MUST be `React.memo`-isolated in microscopic Client Components. Never trigger parent re-renders.

### C. Card Archetypes
1. **Intelligent List:** Auto-sorting loop with `layoutId` swaps simulating AI prioritization.
2. **Command Input:** Multi-step Typewriter Effect with blinking cursor and shimmering loading gradient.
3. **Live Status:** Breathing status indicators with Overshoot spring pop-up badges.
4. **Wide Data Stream:** Infinite Carousel (`x: ["0%", "-100%"]`) with seamless looping.
5. **Contextual UI:** Staggered text highlight followed by float-in action toolbar.
