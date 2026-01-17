# Rebuild Success Pattern (Proven Workflow)

**What makes rebuilds actually match the original:**

## Visual Verification Loop (Critical!)

```
Deploy to Vercel → get real URL
Screenshot deployed result via Chrome
Compare to original (not assumptions!)
Fix differences → redeploy → verify again
```

- ❌ NEVER: Assume it looks right without seeing it
- ✅ ALWAYS: Screenshot actual deployed page

## Theme Skill as Reference

- Keep [project]-theme.md open
- Check colours against spec
- Check typography against spec
- Check section patterns against spec

## Original Site in Browser Tab

- Have original open for visual reference
- Compare sections side-by-side
- Catch subtle differences (link colours, hover states, spacing)

## Incremental Commit → Deploy → Verify

- Small focused changes
- Push to trigger Vercel deploy
- Screenshot to confirm
- Don't batch multiple changes

## Read Before Edit

- Always read the component file first
- Understand existing structure
- Make targeted changes

## Practical Fallbacks

- Missing images? Use styled placeholders, not broken `<img>`
- Complex animation? Simple transition that works > broken fancy one
- Edge case content? Handle gracefully

---

## Side-by-Side Comparison (Phase 9)

**This phase only runs when BOTH old and new sites exist.**

### 1. Open Both Sites

- Tab 1: Original site (source URL)
- Tab 2: New build (Vercel preview URL)

### 2. Homepage Comparison

- Screenshot both at same viewport
- Visual diff overlay
- Check:
  - □ Header matches (logo, nav, colours)
  - □ Hero matches (layout, typography, CTA)
  - □ Sections match (order, styling, dividers!)
  - □ Footer matches (columns, links, colours)
  - □ Dividers match (waves, angles, borders)
  - □ Icons match (exact same SVGs)

### 3. Page-by-Page Comparison

For each key page:
- Navigate both tabs
- Screenshot both
- Flag differences:

```
"MISMATCH: Footer link colour - Original: #666, New: #333"
"MISMATCH: Section divider missing wave SVG"
"MISMATCH: Icon substituted - Original: custom SVG, New: Lucide icon"
```

### 4. Component Checklist

- □ Navigation hover states
- □ Button hover states
- □ Link underlines
- □ Card hover effects
- □ Mobile menu animation
- □ Form focus states

### 5. Output

- /comparison-report.md
- /comparison-screenshots/
- List of issues to fix
