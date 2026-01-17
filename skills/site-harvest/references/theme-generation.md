# Theme Skill Generation

**This is what made recent rebuilds successful. Creates a "discovery dock" for consistent styling.**

## Generate: /[project-name]-theme.md

### 1. Brand Identity

- Primary colour (hex + Tailwind class)
- Secondary colour
- Accent colour
- Text colours (headings, body, muted)
- Background colours (sections, cards, alternating)

### 2. Typography

- Heading font (font-family, Google Fonts link if applicable)
- Body font
- Font sizes (h1-h6 with responsive variants)
- Line heights
- Font weights used

### 3. Section Patterns

- Standard section padding (py-16, py-20, etc.)
- Alternating background pattern
- Container max-width
- Section dividers (with SVG code if waves/angles!)

### 4. Component Specs

- Primary button (colours, padding, radius, hover)
- Secondary button
- Card styling (shadow, radius, padding)
- Link colours (normal, hover, in-footer)

### 5. Layout Patterns

- Grid columns for cards (md:grid-cols-2, lg:grid-cols-3)
- Flexbox patterns used (flex-col + flex-grow + mt-auto for alignment)
- Sidebar width if applicable

### 6. Special Elements

- Wave dividers (exact SVG markup!)
- Icon style (outline, solid, size)
- Image aspect ratios
- Any unique brand elements

### 7. Tailwind Classes Reference

- Most-used utility combinations
- Custom classes if any

## Why This Works

- Single source of truth during rebuild
- Claude can reference it constantly
- Catches drift from original design
- Works with visual verification loop

**Save to**: /[project-name]-theme.md (copy to project .claude/skills/ when building)
