---
name: web-frontend
description: Apply frontend development standards for React/Next.js/Tailwind projects. Covers colour extraction from logos, avoiding AI-slop aesthetics, performance targets (LCP <2.5s), and modern CSS patterns. Triggers: component, responsive, accessibility, styling, UI, colours, Tailwind, layout, hover states, buttons, frontend.
compatibility: Requires `claude --chrome` or `claude --chrome --resume` for colour picker and console access
---

# Web Frontend Skill

## Pet Hates (Never Do These)

### AI Slop Aesthetic
- Predictable primary + ghost button combos
- Always-blue or purple-gradient-on-white schemes
- Weak hover states (just opacity changes)
- Cookie-cutter layouts (endless full-width rows)
- Labels everywhere ("NEW", "FEATURED", "POPULAR")

### Template Garbage
- Progress bar "skills" (Web Design 85%)
- Circular percentage ratings (9/10 Customer Satisfaction)
- Counter animations (500+ counting up on scroll)
- Star ratings without actual reviews
- Arbitrary statistics (95% Success Rate)
- "Years of Experience" counters
- Skill percentage bars

If there's no real proof point, leave it out. Don't fabricate metrics.

### Layout Laziness
- Full-width everything - vary the rhythm
- Ignoring card alignment (use flex-1 + mt-auto)
- Fixed breakpoints instead of content-based ones
- Hamburger menus when bottom nav works better on mobile
- **Flat rectangles everywhere** - no section dividers, no decorative shapes. Use waves, angles, curves, blobs. Pick a shape theme and use it consistently throughout the site (waves at section tops/bottoms, blob behind hero image, angled cards)

## Colour Selection (Claude's Weakness)

### The Problem
Claude defaults to safe blue/purple. Fight it.

### Extraction Methods (Use Both to Verify)
1. **Script extraction** - run `./scripts/extract-colours.sh path/to/logo.png` → precise hex codes
2. **Vision verification** - `Read logo.png` → visually confirm which colour is primary/accent/background
3. **Chrome tabs** - colour picker in Elements panel (requires `claude --chrome` session)
4. **Ask the user** - they might have brand guidelines

**Workflow**: Script gives hex codes → Vision confirms context ("the orange is the logo mark, grey is the tagline")

### Expansion Process
1. **If only 1-2 colours**: use colour theory (complementary, split-complementary, analogous)
2. **Use oklch** - better for generating tints/shades than hex (`oklch(65% 0.15 250)`)
3. **Test contrast** - WCAG AA minimum (4.5:1 text, 3:1 large text)

### Pet Hates
- Defaulting to blue (#3B82F6) or purple (#8B5CF6)
- Low-contrast pastels
- Gradients that clash (purple-to-orange syndrome)
- Ignoring the logo colours entirely
- Guessing when you could just look at the image
- **Industry stereotyping** - "developer site = black background", "restaurant = warm oranges", "law firm = navy/gold". Design for the CLIENT's brand, not the industry template

### Safe Fallback
If genuinely nothing to go on: **slate/zinc + one accent**. At least it's neutral.

## References (Use These)

### Modern CSS (Tailwind v4 has these)
Container queries (`@container`, `@md:`), `:has()` (`has-[]:`), `clamp()`, subgrid (`grid-cols-subgrid`), `text-balance`, `text-pretty`, scroll-driven animations, view transitions, oklch colours.

### Design Variety
Sidebar widgets, asymmetric layouts, alternating backgrounds, glassmorphism where appropriate, micro-interactions on hover.

### Section Shapes & Dividers (Ideas, Not Rules)
Don't just stack flat rectangles. Pick a shape theme - but these are IDEAS to offer, not rules. If user says "I don't like it", try a different one.

**Shape themes to try:**
- Waves (SVG at section top AND bottom, matching angle/count, padding adjusted so content clears the curve)
- Angles/diagonals (`clip-path: polygon()` - ensure content padding accounts for the cut)
- Blobs behind images (organic SVG shapes, z-indexed behind)
- Rounded corners on sections (soft, friendly)
- Geometric cutouts (modern, bold)

**Waves implementation detail**: Wave SVGs attach to top and bottom of a section. Match the wave count, angle, and amplitude. Adjust section padding so text/content doesn't overlap the wave. Validate in browser (requires `claude --chrome` or `claude --chrome --resume`).

**Image corner ideas:**
- All corners rounded (safe)
- Diagonal corners only (top-left + bottom-right)
- One dramatic corner (large radius on one)
- Blob mask (organic shape)
- No rounding (sharp, editorial)

**Implementation**: SVG for complex, `clip-path` for simple, `border-radius` for soft. Generate at shapedivider.app or getwaves.io.

**When user says "I don't like it"**: Try the NEXT idea on the list, don't repeat the same approach.

### Typography
Fluid scales with clamp(). Semantic hierarchy (h1, h2) doesn't have to match visual hierarchy - style for design, tag for accessibility.

### Components
shadcn/ui for accessible primitives. Radix UI + Tailwind.

## Performance Targets

| Metric | Target |
|--------|--------|
| LCP | <2.5s |
| FID | <100ms |
| CLS | <0.1 |
| Initial bundle | <500KB |
| 3G load | <3s |
| WCAG | AA minimum |

## Tools

- **Screenshots**: Firecrawl scrape with screenshot format, or Playwright
- **UI components**: Magic MCP (21st.dev library)
- **Console/network/colour picker**: Chrome tabs integration (user must start session with `claude --chrome` or `claude --chrome --resume`)
- **E2E testing**: Playwright direct (`npx playwright test --browser=webkit`)
- **Colour extraction**: `./scripts/extract-colours.sh` (this skill)

## Post-Training

Check Context7 or web.dev/blog for latest CSS features and syntax changes.
