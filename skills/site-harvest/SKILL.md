---
name: site-harvest
description: Extract complete website content, design system, and assets for rebuilding or migration. Uses Firecrawl for content/CSS extraction, Chrome for visual comparison. Generates theme skill file for rebuild. Triggers: harvest site, scrape website, extract design, clone website, migrate site, copy website design, grab design tokens.
updated: 2025-01-18
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - TodoWrite
  - WebFetch
  - mcp__firecrawl__firecrawl_scrape
  - mcp__firecrawl__firecrawl_map
  - mcp__firecrawl__firecrawl_crawl
  - mcp__firecrawl__firecrawl_extract
---

# Site Harvest Skill

**Purpose**: Extract complete website content, design system, and assets for rebuilding or migration.

**Trigger**: `/site-harvest [url]` or "harvest [url]"

## Architecture: Token-Efficient Hybrid

| Task | Tool | Why |
|------|------|-----|
| URL Discovery | Firecrawl `map` | Their tokens, instant, free 500 pages |
| Bulk Content | Firecrawl `crawl` | Their tokens, parallel extraction |
| Structured Data | Firecrawl `extract` | Schema-based, accurate |
| Sitemap Analysis | Claude + WebFetch | Quick XML parse, freshness check |
| Screaming Frog | CSV import | Pre-crawled, comprehensive |
| Design Screenshots | Firecrawl `scrape` | Branding format extracts design |
| Side-by-Side Compare | Chrome Tab | Only for old vs new comparison |

**Token Strategy**: Firecrawl does heavy lifting (their tokens) → Chrome only for visual comparison (our tokens)

## Prerequisites

1. **Firecrawl MCP** - Primary extraction engine
2. **Chrome Tab MCP** - Only for side-by-side comparison phase
3. **URL sources** (one or more):
   - Site URL (Firecrawl discovers pages)
   - Screaming Frog export (CSV)
   - sitemap.xml (auto-detected)

## Quick Start

```
/site-harvest https://example.com
```

## 9-Phase Workflow

### Phase 1: URL Discovery & Site Structure (FOUNDATION)

**⚠️ THIS IS THE BASIS FOR EVERYTHING. Get this wrong = rebuild has gaps.**

1. Ask for Screaming Frog export first (most comprehensive)
2. Analyse sitemap.xml via WebFetch (freshness, coverage)
3. Run Firecrawl map (live discoverable pages)
4. **Check AJAX/Pagination** (load more, infinite scroll, WordPress API)
5. Four-way comparison: Sitemap vs Firecrawl vs SF vs AJAX
6. Document site structure (page types, navigation, hierarchy)
7. Report findings and **wait for confirmation**

**Detailed instructions**: See `references/url-discovery.md`

Save: /url-discovery.json

### Phase 2: Content Extraction (Firecrawl)

```javascript
firecrawl_crawl({
  url: "https://example.com",
  limit: [merged URL count],
  scrapeOptions: {
    formats: ["markdown", "html", "links"],
    onlyMainContent: true
  }
})
```

For each page, save:
- /pages/[slug].md (clean markdown)
- /pages/[slug].json (structured: title, meta, headings)

Extract media references (images, videos, documents).

Save: /content-manifest.json

### Phase 3: Design System Extraction

```javascript
// Branding extraction
firecrawl_scrape({
  url: "https://example.com",
  formats: ["branding"]
})

// Full CSS capture
firecrawl_scrape({
  url: "https://example.com",
  formats: ["html", "rawHtml"]
})
```

- Parse all stylesheet URLs and download CSS files
- Extract CSS variables (--color-*, --font-*, --spacing-*)
- Capture typography scale (h1-h6, p, small)

Save: /design-tokens.json

### Phase 4: Component Style Catalogue (EXHAUSTIVE)

**Capture EVERY visual pattern** - this prevents "footer links unstyled" problems.

Extract computed styles for:
- Navigation (header, links, mobile menu, dropdowns)
- Footer (container, columns, links, social icons)
- Typography (headings, paragraphs, lists, blockquotes)
- Buttons & CTAs (primary, secondary, ghost, hover states)
- Sections (padding, backgrounds, alternating patterns)
- **Dividers** (hr, borders, SVG waves, clip-path angles)
- Cards (container, hover, image, content)
- Icons (download exact SVGs, don't substitute!)
- Forms (inputs, labels, error states)

**Detailed element list**: See `references/component-styles.md`

Save: /component-styles.json

### Phase 5: Visual Capture (Screenshots)

```javascript
firecrawl_scrape({
  url: "https://example.com",
  formats: [
    { type: "screenshot", fullPage: true, viewport: { width: 1920, height: 1080 } },
    { type: "screenshot", fullPage: true, viewport: { width: 768, height: 1024 } },
    { type: "screenshot", fullPage: true, viewport: { width: 375, height: 812 } }
  ]
})
```

Screenshot key pages (homepage, about, services, blog, contact) and components (header, footer, hero, cards, dividers).

Save to: /screenshots/

### Phase 6: Asset Download

1. **Images**: Download all, maintain folder structure → /media/
2. **Fonts**: Parse @font-face, download all formats → /assets/fonts/
3. **Icons**: Extract inline SVGs exactly, download external SVGs → /assets/icons/
4. **JavaScript**: Download external JS, note inline scripts → /assets/scripts/

### Phase 7: Theme Skill Generation

Generate: /[project-name]-theme.md

Document:
1. Brand identity (colours with hex + Tailwind classes)
2. Typography (fonts, sizes, weights)
3. Section patterns (padding, backgrounds, dividers)
4. Component specs (buttons, cards, links)
5. Layout patterns (grids, flexbox)
6. Special elements (wave SVGs, icons)
7. Tailwind classes reference

**Template**: See `references/theme-generation.md`

**This is the single source of truth during rebuild.**

### Phase 8: Manifest Generation

Generate comprehensive manifest.json with:
- Harvest metadata (URL, date, tool version)
- URL discovery results (all sources compared)
- Pages list with files
- Design assets references
- Screenshots index
- Warnings and flags

**Example manifest**: See `references/output-structure.md`

### Phase 9: Side-by-Side Comparison (Chrome Tab)

**Only runs when BOTH old and new sites exist.**

1. Open both sites in Chrome tabs
2. Screenshot both at same viewport
3. Compare: header, hero, sections, footer, dividers, icons
4. Flag mismatches with specifics
5. Generate comparison report

**Detailed workflow**: See `references/rebuild-workflow.md`

## Critical Rules

### ❌ DON'T
- Substitute icons with similar ones from icon libraries
- Ignore wave/angle dividers
- Skip footer link styling
- Assume section spacing without measuring
- Miss hover/active/focus states

### ✅ DO
- Extract EXACT SVG markup for all custom icons
- Capture ALL divider types (hr, border, SVG, clip-path)
- Document EVERY link style (nav, footer, inline, CTA)
- Measure actual padding/margin values
- Screenshot unusual patterns for reference

## Error Handling

| Error | Action |
|-------|--------|
| Firecrawl rate limit | Wait, retry with smaller batch |
| sitemap.xml missing | Continue with Firecrawl + Screaming Frog |
| CSS file 404 | Log warning, check for inline styles |
| Font file blocked | Note in manifest, may need manual download |
| SVG divider complex | Screenshot + extract raw HTML |

## Example Usage

```bash
# Basic harvest
/site-harvest https://client-site.co.uk

# With Screaming Frog export
/site-harvest https://example.com --urls screaming-frog-export.csv

# Comparison mode (after rebuild)
/site-harvest compare https://old-site.com https://new-site.vercel.app
```

## Output Structure

See `references/output-structure.md` for complete folder layout and manifest example.

```
/scraped-data/[site-name]/
├── manifest.json
├── [site-name]-theme.md
├── url-discovery.json
├── design-tokens.json
├── component-styles.json
├── pages/
├── screenshots/
├── media/
├── assets/
└── comparison/
```
