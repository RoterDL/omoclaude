---
name: taste-redesign
description: Audit and upgrade existing UI to premium quality. Diagnoses generic patterns across 11 categories, applies targeted fixes working with the existing stack. Complements taste-core with redesign-specific checks. Works with any CSS framework or vanilla CSS.
---

# Redesign Skill

## How This Works

1. **Scan** — Read the codebase. Identify the framework, styling method, and current design patterns.
2. **Diagnose** — Run through the audit below. List every generic pattern, weak point, and missing state.
3. **Fix** — Apply targeted upgrades working with the existing stack. Do not rewrite from scratch.

## Design Audit

### Typography

- **Browser default fonts or Inter everywhere.** Replace with a font that has character: `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`. For editorial projects, pair serif header with sans body.
- **Headlines lack presence.** Increase display text size, tighten letter-spacing, reduce line-height. Headlines should feel heavy and intentional.
- **Body text too wide.** Limit paragraph width to ~65 characters. Increase line-height for readability.
- **Only Regular (400) and Bold (700) weights.** Introduce Medium (500) and SemiBold (600) for subtle hierarchy.
- **Numbers in proportional font.** Use monospace or `font-variant-numeric: tabular-nums` for data interfaces.
- **Missing letter-spacing adjustments.** Negative tracking for large headers, positive for small caps/labels.
- **All-caps subheaders everywhere.** Try lowercase italics, sentence case, or small-caps.
- **Orphaned words.** Fix with `text-wrap: balance` or `text-wrap: pretty`.

### Color and Surfaces

- **Pure `#000000` background.** Replace with off-black (`#0a0a0a`, `#121212`, or tinted dark).
- **Oversaturated accent colors.** Keep saturation below 80%. Desaturate to blend with neutrals.
- **More than one accent color.** Pick one. Remove the rest.
- **Mixing warm and cool grays.** Stick to one gray family with consistent hue tinting.
- **Purple/blue "AI gradient" aesthetic.** The most common AI fingerprint. Replace with neutral bases + single accent.
- **Generic `box-shadow`.** Tint shadows to match background hue. Use colored shadows.
- **Flat design with zero texture.** Add subtle noise, grain, or micro-patterns to backgrounds.
- **Perfectly even gradients.** Break with radial gradients, noise overlays, or mesh gradients.
- **Inconsistent lighting direction.** Audit all shadows for single consistent light source.
- **Random dark sections in a light mode page.** Either commit to full dark mode or keep consistent background tone. Use slightly darker shade, not a sudden jump.
- **Empty flat sections.** Add background imagery at low opacity, subtle patterns, or ambient gradients. Use `picsum.photos/seed/{name}/1920/1080` for placeholders.

### Layout

- **Everything centered and symmetrical.** Break with offset margins, mixed aspect ratios, or left-aligned headers.
- **Three equal card columns as feature row.** Replace with 2-column zig-zag, asymmetric grid, horizontal scroll, or masonry.
- **`height: 100vh` for full-screen sections.** Replace with `min-height: 100dvh`.
- **Complex flexbox percentage math.** Replace with CSS Grid.
- **No max-width container.** Add 1200-1440px constraint with auto margins.
- **Cards of equal height forced by flexbox.** Allow variable heights or masonry.
- **Uniform border-radius on everything.** Vary: tighter on inner elements, softer on containers.
- **No overlap or depth.** Use negative margins for layering and visual depth.
- **Symmetrical vertical padding.** Adjust optically (bottom often needs slightly more).
- **Dashboard always has left sidebar.** Try top nav, floating command menu, or collapsible panel.
- **Missing whitespace.** Double spacing. Dense layouts for data dashboards, not marketing pages.
- **Buttons not bottom-aligned in card groups.** Pin CTAs to card bottom for clean horizontal lines.
- **Feature lists starting at different vertical positions.** Consistent spacing above lists or fixed-height title blocks.
- **Inconsistent vertical rhythm in side-by-side elements.** Align shared elements (titles, descriptions, buttons) across items.
- **Mathematical alignment that looks optically wrong.** Icons/text/buttons often need 1-2px optical adjustments.

### Interactivity and States

- **No hover states on buttons.** Add background shift, slight scale, or translate.
- **No active/pressed feedback.** `scale(0.98)` or `translateY(1px)` on press.
- **Instant transitions with zero duration.** Add 200-300ms transitions to interactive elements.
- **Missing focus ring.** Visible focus indicators for keyboard navigation (accessibility requirement).
- **No loading states.** Skeleton loaders matching layout shape, not generic spinners.
- **No empty states.** Design a composed "getting started" view.
- **No error states.** Clear inline error messages. No `window.alert()`.
- **Dead links to `#`.** Link to real destinations or visually disable.
- **No active page indicator in navigation.**
- **Scroll jumping.** Add `scroll-behavior: smooth`.
- **Animations using `top`/`left`/`width`/`height`.** Switch to `transform` and `opacity`.

### Content

- **Generic names "John Doe", "Jane Smith".** Use diverse, realistic names.
- **Fake round numbers `99.99%`, `50%`, `$100.00`.** Use organic data: `47.2%`, `$99.00`.
- **Placeholder companies "Acme Corp", "Nexus".** Invent contextual brand names.
- **AI copywriting clichés.** Never: "Elevate", "Seamless", "Unleash", "Next-Gen", "Delve", "Tapestry".
- **Exclamation marks in success messages.** Be confident, not loud.
- **"Oops!" error messages.** Be direct: "Connection failed. Please try again."
- **Passive voice.** Active: "We couldn't save your changes" not "Mistakes were made."
- **All blog post dates identical.** Randomize to appear real.
- **Same avatar for multiple users.** Unique assets per person.
- **Lorem Ipsum.** Write real draft copy.
- **Title Case On Every Header.** Use sentence case.

### Component Patterns

- **Generic card (border + shadow + white bg).** Remove border, or use only background, or only spacing.
- **Always one filled button + one ghost button.** Add text links or tertiary styles.
- **Pill-shaped "New" and "Beta" badges.** Try square badges, flags, or plain text.
- **Accordion FAQ sections.** Use side-by-side list, searchable help, or inline progressive disclosure.
- **3-card carousel testimonials with dots.** Replace with masonry wall, social posts, or single rotating quote.
- **Pricing table with 3 towers.** Highlight recommended tier with color/emphasis, not extra height.
- **Modals for everything.** Use inline editing, slide-over panels, or expandable sections.
- **Avatar circles exclusively.** Try squircles or rounded squares.
- **Light/dark toggle always sun/moon.** Use dropdown, system preference, or settings integration.
- **Footer link farm with 4 columns.** Simplify to main paths and legal links.

### Iconography

- **Lucide/Feather exclusively.** Use Phosphor, Heroicons, or custom set.
- **Rocketship for "Launch", shield for "Security".** Replace cliché metaphors with less obvious icons.
- **Inconsistent stroke widths.** Standardize to one weight.
- **Missing favicon.** Always include one.
- **Stock "diverse team" photos.** Use real photos, candid shots, or consistent illustration style.

### Code Quality

- **Div soup.** Use semantic HTML: `<nav>`, `<main>`, `<article>`, `<aside>`, `<section>`.
- **Inline styles mixed with CSS classes.** Move all styling to the project's system.
- **Hardcoded pixel widths.** Use relative units (`%`, `rem`, `max-width`).
- **Missing alt text.** Describe image content. Never `alt=""` on meaningful images.
- **Arbitrary z-index `9999`.** Establish a clean z-index scale.
- **Commented-out dead code.** Remove debug artifacts.
- **Import hallucinations.** Verify every import in `package.json`.
- **Missing meta tags.** Add `<title>`, `description`, `og:image`, social sharing tags.

### Strategic Omissions

- **No legal links.** Privacy policy and terms of service in footer.
- **No "back" navigation.** Dead ends in user flows.
- **No custom 404 page.** Design a helpful branded experience.
- **No form validation.** Client-side validation for emails, required fields, formats.
- **No "skip to content" link.** Essential for keyboard users.
- **No cookie consent.** If required by jurisdiction, add compliant banner.

## Upgrade Techniques

### Typography
* Variable font animation: interpolate weight/width on scroll or hover.
* Outlined-to-fill transitions: text starts as stroke outline, fills on scroll entry.
* Text mask reveals: large typography as window to video/animated imagery.

### Layout
* Broken grid / asymmetry: elements overlapping, bleeding off-screen with calculated randomness.
* Whitespace maximization: aggressive negative space forcing focus on single elements.
* Parallax card stacks: sections sticking and stacking during scroll.
* Split-screen scroll: two halves sliding in opposite directions.

### Motion
* Smooth scroll with inertia: decouple scrolling from browser defaults for cinematic feel.
* Staggered entry: cascade with slight delays, Y-axis translation + opacity fade.
* Spring physics: replace linear easing with spring-based motion.
* Scroll-driven reveals: expanding masks, wipes, or draw-on SVG paths tied to scroll.

### Surface
* True glassmorphism: `backdrop-filter: blur` + 1px inner border + subtle inner shadow.
* Spotlight borders: card borders illuminating dynamically under cursor.
* Grain and noise overlays: fixed, pointer-events-none overlay for texture.
* Colored, tinted shadows: shadows carrying background hue instead of generic black.

## Fix Priority

1. **Font swap** — biggest instant improvement, lowest risk
2. **Color palette cleanup** — remove clashing or oversaturated colors
3. **Hover and active states** — makes the interface feel alive
4. **Layout and spacing** — proper grid, max-width, consistent padding
5. **Replace generic components** — swap cliché patterns for modern alternatives
6. **Add loading, empty, error states** — makes it feel finished
7. **Polish typography scale and spacing** — the premium final touch

## Rules

* Work with the existing tech stack. Do not migrate frameworks or styling libraries.
* Do not break existing functionality. Test after every change.
* Before importing any new library, check the project's dependency file first.
* If the project uses Tailwind, check version (v3 vs v4) before modifying config.
* If the project has no framework, use vanilla CSS.
* Keep changes reviewable and focused. Small, targeted improvements over big rewrites.
