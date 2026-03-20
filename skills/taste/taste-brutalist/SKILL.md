---
name: taste-brutalist
description: Industrial brutalism and tactical telemetry design paradigm for plan-phase injection. Swiss typographic print fused with military terminal aesthetics. Rigid grids, extreme type scale contrast, utilitarian color, analog degradation effects. For data-heavy dashboards, portfolios, or editorial sites that need to feel like declassified blueprints.
---

# Industrial Brutalism & Tactical Telemetry Design Paradigm

This skill is a **plan-phase** design paradigm. When injected into a planner/architect agent, it informs the Design Specification section of plan.md with brutalist design decisions. The implementation agent then follows the plan using taste-core guardrails.

## 1. Visual Archetypes

Pick ONE paradigm per project. Do not mix within the same interface.

### Swiss Industrial Print
Derived from 1960s corporate identity systems and heavy machinery blueprints.
* High-contrast light modes (newsprint/off-white substrates). Monolithic heavy sans-serif typography. Unforgiving structural grids with visible dividing lines. Aggressive asymmetric negative space punctuated by oversized viewport-bleeding numerals. Heavy use of primary red as accent.

### Tactical Telemetry & CRT Terminal
Derived from classified military databases, legacy mainframes, and aerospace HUDs.
* Dark mode exclusivity. High-density tabular data. Absolute dominance of monospaced typography. Technical framing devices (ASCII brackets, crosshairs). Simulated hardware limitations (phosphor glow, scanlines, low bit-depth).

## 2. Typographic Architecture

Typography is the primary structural and decorative infrastructure. Imagery is secondary.

### Macro-Typography (Structural Headers)
* **Fonts:** Neue Haas Grotesk (Black), Archivo Black, Roboto Flex (Heavy), Monument Extended.
* **Scale:** Massive, fluid: `clamp(4rem, 10vw, 15rem)`.
* **Tracking:** Extremely tight, often negative (`-0.03em` to `-0.06em`), forcing glyphs to form solid blocks.
* **Leading:** Highly compressed (`0.85` to `0.95`). Exclusively uppercase.

### Micro-Typography (Data & Telemetry)
* **Fonts:** JetBrains Mono, IBM Plex Mono, Space Mono, VT323, Courier Prime.
* **Scale:** Fixed small (`10px`-`14px`). Generous tracking (`0.05em`-`0.1em`). Exclusively uppercase.

### Textural Contrast (Artistic Disruption)
* **Fonts:** Playfair Display, EB Garamond. Used sparingly with heavy post-processing (halftone, 1-bit dithering).

## 3. Color System

Gradients, soft drop shadows, and translucency are strictly prohibited. Choose ONE substrate per project.

### Swiss Industrial Print (Light)
* Background: `#F4F4F0` or `#EAE8E3` (matte unbleached paper)
* Foreground: `#050505` to `#111111` (carbon ink)
* Accent: `#E61919` or `#FF2A2A` (aviation/hazard red) — the ONLY accent color

### Tactical Telemetry (Dark)
* Background: `#0A0A0A` or `#121212` (deactivated CRT, avoid pure `#000000`)
* Foreground: `#EAEAEA` (white phosphor)
* Accent: `#E61919` or `#FF2A2A` (same red)
* Terminal Green (`#4AF626`): Optional, for a single specific UI element only

## 4. Layout & Spatial Engineering

* **Blueprint Grid:** Strict CSS Grid. Elements anchored to grid tracks, not floating.
* **Visible Compartmentalization:** Solid borders (`1px`-`2px solid`) delineate zones. Horizontal rules span full width.
* **Bimodal Density:** Oscillate between extreme data density (packed monospace) and vast negative space framing macro-typography.
* **Geometry:** Zero `border-radius`. All corners exactly 90 degrees.

## 5. UI Components & Symbology

* **ASCII Framing:** `[ DELIVERY SYSTEMS ]`, `< RE-IND >`, `>>>`, `///`
* **Industrial Markers:** Registration `®`, copyright `©`, trademark `™` as structural geometric elements.
* **Technical Assets:** Crosshairs `+` at grid intersections, barcodes, warning stripes, randomized IDs (`REV 2.6`, `UNIT / D-01`).

## 6. Textural & Post-Processing Effects

* **Halftone/1-Bit Dithering:** Dot-matrix patterns via `mix-blend-mode: multiply` + SVG radial dot overlays.
* **CRT Scanlines:** `repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px)`.
* **Mechanical Noise:** Global low-opacity SVG noise filter on DOM root.

## 7. Web Engineering Directives

* Grid Determinism: `display: grid; gap: 1px` with contrasting parent/child backgrounds for razor-thin dividers.
* Semantic Rigidity: Use `<data>`, `<samp>`, `<kbd>`, `<output>`, `<dl>` for technical content.
* Typography Clamping: CSS `clamp()` exclusively for macro-typography.

## Plan Output Directive

When writing the Design Specification section of plan.md, include:
1. **Chosen paradigm:** Swiss Industrial Print OR Tactical Telemetry
2. **Substrate palette:** Exact background, foreground, accent hex values
3. **Typography system:** Specific font stack for macro/micro/textural roles
4. **Grid architecture:** Column structure, compartmentalization strategy
5. **Textural effects:** Which post-processing effects to apply
6. **Component inventory:** ASCII framing patterns, industrial markers planned
