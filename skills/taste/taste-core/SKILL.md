---
name: taste-core
description: Core frontend design quality rules. Enforces metric-based design engineering, strict conventions, performance guardrails, and AI-tell avoidance for premium UI output.
---

# Core Design Rules

## 1. Baseline Configuration

* DESIGN_VARIANCE: 8 (1=Perfect Symmetry, 10=Artsy Chaos)
* MOTION_INTENSITY: 6 (1=Static, 10=Cinematic)
* VISUAL_DENSITY: 4 (1=Art Gallery, 10=Cockpit)

Default baseline is strictly (8, 6, 4). If the plan-phase design spec (plan.md) specifies dial values, use those instead. Adapt dynamically based on explicit user requests. These values drive Sections 2-5 logic.

## 2. Architecture & Conventions

* **Dependency Verification [MANDATORY]:** Before importing ANY 3rd party library, check `package.json`. If missing, output the install command first. Never assume a library exists.
* **Framework:** React or Next.js. Default to Server Components (RSC).
  * **RSC Safety:** Global state works ONLY in Client Components. Wrap providers in a `"use client"` component.
  * **Interactivity Isolation:** Interactive UI components MUST be extracted as isolated leaf `'use client'` components. Server Components render static layouts only.
* **State:** `useState`/`useReducer` for isolated UI. Global state strictly for deep prop-drilling avoidance.
* **Styling:** Tailwind CSS (v3/v4) for 90% of styling.
  * **Version Lock:** Check `package.json` first. Do not use v4 syntax in v3 projects.
  * **v4 Config:** Do NOT use `tailwindcss` plugin in `postcss.config.js`. Use `@tailwindcss/postcss` or Vite plugin.
* **Anti-Emoji [CRITICAL]:** NEVER use emojis in code, markup, or text content. Replace with Radix/Phosphor icons or clean SVG.
* **Responsiveness:**
  * Standardize breakpoints (`sm`, `md`, `lg`, `xl`).
  * Contain layouts: `max-w-[1400px] mx-auto` or `max-w-7xl`.
  * **Viewport Stability [CRITICAL]:** NEVER use `h-screen`. ALWAYS use `min-h-[100dvh]`.
  * **Grid over Flex-Math:** NEVER use `w-[calc(33%-1rem)]`. ALWAYS use CSS Grid.
* **Icons:** Use `@phosphor-icons/react` or `@radix-ui/react-icons`. Standardize `strokeWidth` globally.

## 3. Design Engineering Directives

**Rule 1: Deterministic Typography**
* Display/Headlines: `text-4xl md:text-6xl tracking-tighter leading-none`.
* **Anti-Slop:** Ban `Inter` for premium/creative. Use `Geist`, `Outfit`, `Cabinet Grotesk`, or `Satoshi`.
* **Technical UI:** Serif fonts BANNED for Dashboard/Software UIs. Use `Geist` + `Geist Mono` or `Satoshi` + `JetBrains Mono`.
* Body: `text-base text-gray-600 leading-relaxed max-w-[65ch]`.

**Rule 2: Color Calibration**
* Max 1 accent color. Saturation < 80%.
* **Lila Ban:** "AI Purple/Blue" is BANNED. No purple glows, no neon gradients. Use neutral bases (Zinc/Slate) with singular accents (Emerald, Electric Blue, Deep Rose).
* **Consistency:** One palette for the entire output. No warm/cool gray mixing.

**Rule 3: Layout Diversification**
* **Anti-Center Bias:** Centered Hero/H1 BANNED when DESIGN_VARIANCE > 4. Force split-screen, left/right aligned, or asymmetric whitespace.

**Rule 4: Materiality & Anti-Card Overuse**
* For VISUAL_DENSITY > 7: generic card containers BANNED. Use `border-t`, `divide-y`, or negative space.
* Use cards ONLY when elevation communicates hierarchy. Tint shadows to background hue.

**Rule 5: Interactive UI States**
* MUST implement full interaction cycles:
  * **Loading:** Skeletal loaders matching layout sizes (no generic spinners).
  * **Empty States:** Beautifully composed empty states.
  * **Error States:** Clear, inline error reporting.
  * **Tactile Feedback:** On `:active`, use `-translate-y-[1px]` or `scale-[0.98]`.

**Rule 6: Data & Form Patterns**
* Label above input. Helper text optional. Error text below. Standard `gap-2` for input blocks.

## 4. Motion & Animation Implementation Rules

* **Magnetic Hover [CRITICAL]:** NEVER use `useState` for magnetic hover or continuous animations. Use EXCLUSIVELY Framer Motion `useMotionValue` + `useTransform` outside the React render cycle to prevent performance collapse on mobile.
* **Spring Physics:** Apply `type: "spring", stiffness: 100, damping: 20` to all interactive elements. No linear easing.
* **Layout Transitions:** Use Framer Motion `layout` and `layoutId` for smooth re-ordering, resizing, and shared element transitions.
* **Staggered Orchestration:** Never mount lists instantly. Use `staggerChildren` (Framer) or CSS cascade (`animation-delay: calc(var(--index) * 100ms)`). **CRITICAL:** Parent (`variants`) and Children MUST reside in the same Client Component tree.
* **GSAP/ThreeJS Isolation:** Never mix GSAP/ThreeJS with Framer Motion in the same component tree. Default to Framer Motion for UI. Use GSAP/ThreeJS exclusively for isolated full-page scrolltelling or canvas backgrounds in strict `useEffect` cleanup blocks.
* **Liquid Glass:** Beyond `backdrop-blur`: add `border-white/10` inner border + `shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]` inner shadow for physical edge refraction.

## 5. Performance Guardrails

* **DOM Cost:** Grain/noise filters exclusively on `fixed inset-0 z-50 pointer-events-none` pseudo-elements. NEVER on scrolling containers.
* **Hardware Acceleration:** Never animate `top`, `left`, `width`, `height`. Use `transform` and `opacity` only.
* **Z-Index Restraint:** Use z-indexes strictly for systemic layers (Sticky Navbars, Modals, Overlays).
* **Blur Constraints:** Apply `backdrop-blur` only to fixed/sticky elements. Never on scrolling content areas.
* **Perpetual Animation Isolation:** Any perpetual motion or infinite loop MUST be `React.memo`-isolated in its own microscopic Client Component. Never trigger parent re-renders.

## 6. AI Tells (Forbidden Patterns)

### Visual & CSS
* NO neon/outer glows. Use inner borders or subtle tinted shadows.
* NO pure `#000000`. Use Off-Black, Zinc-950, or Charcoal.
* NO oversaturated accents. Desaturate to blend with neutrals.
* NO excessive gradient text. Do not use text-fill gradients for large headers.
* NO custom mouse cursors. They are outdated and ruin performance/accessibility.

### Typography
* NO Inter font. Use `Geist`, `Outfit`, `Cabinet Grotesk`, or `Satoshi`.
* NO oversized H1s. Control hierarchy with weight and color, not massive scale.
* Serif ONLY for creative/editorial. NEVER on dashboards.

### Layout & Spacing
* Padding and margins must be mathematically perfect.
* NO 3-column equal card layouts. Use zig-zag, asymmetric grid, or horizontal scroll.

### Content & Data
* NO generic names ("John Doe", "Sarah Chan"). Use creative, realistic names.
* NO generic avatars. Use creative photo placeholders or specific styling.
* NO fake round numbers (`99.99%`, `50%`). Use organic data (`47.2%`, `+1 (312) 847-1928`).
* NO startup slop names ("Acme", "Nexus"). Invent premium, contextual brands.
* NO filler words ("Elevate", "Seamless", "Unleash", "Next-Gen"). Use concrete verbs.

### External Resources
* NO broken Unsplash links. Use `https://picsum.photos/seed/{random}/800/600` or SVG avatars.
* shadcn/ui: NEVER use in generic default state. MUST customize radii, colors, shadows.
* **Production-Ready Cleanliness:** Code must be extremely clean, visually striking, and meticulously refined.

## 7. Pre-Flight Check

Before outputting, verify:
- [ ] Global state used appropriately (not arbitrarily)?
- [ ] Mobile layout collapse (`w-full`, `px-4`, `max-w-7xl mx-auto`) guaranteed?
- [ ] Full-height sections use `min-h-[100dvh]` (not `h-screen`)?
- [ ] `useEffect` animations have strict cleanup functions?
- [ ] Empty, loading, and error states provided?
- [ ] Cards omitted in favor of spacing where possible?
- [ ] CPU-heavy perpetual animations isolated in own Client Components?
