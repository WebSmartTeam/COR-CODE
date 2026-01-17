# Output Structure

## Folder Layout

```
/scraped-data/[site-name]/
├── manifest.json              # Master index
├── [site-name]-theme.md       # THEME SKILL - use during rebuild!
├── url-discovery.json         # All URL sources compared
├── design-tokens.json         # CSS variables, colours, typography
├── component-styles.json      # EXHAUSTIVE component catalogue
├── branding.json              # Firecrawl branding extraction
├── pages/
│   ├── index.md
│   ├── index.json
│   └── [slug].md
├── screenshots/
│   ├── homepage-desktop.png
│   ├── homepage-tablet.png
│   ├── homepage-mobile.png
│   ├── header-desktop.png
│   ├── header-mobile.png
│   ├── footer.png
│   └── dividers/
│       ├── wave-top.svg       # Actual SVG files!
│       ├── wave-bottom.svg
│       └── angle-divider.svg
├── media/
│   └── [images]
├── assets/
│   ├── styles/
│   │   └── [all CSS files]
│   ├── scripts/
│   │   └── [all JS files]
│   ├── fonts/
│   │   └── [font files]
│   └── icons/
│       └── [exact SVG files]  # Not substitutes!
└── comparison/                 # Only if rebuild comparison done
    ├── comparison-report.md
    └── [diff screenshots]
```

## Manifest JSON Example

```json
{
  "harvest": {
    "url": "https://example.com",
    "date": "2025-01-14T10:30:00Z",
    "tool": "site-harvest v2.0"
  },
  "urlDiscovery": {
    "sitemap": {
      "found": true,
      "location": "/sitemap.xml",
      "urls": 47,
      "freshness": { "fresh": 12, "stale": 20, "veryStale": 8, "unknown": 7 }
    },
    "firecrawl": { "urls": 52 },
    "screamingFrog": { "urls": 48 },
    "merged": { "total": 55, "unique": ["list of URLs only in one source"] }
  },
  "pages": [
    { "url": "/", "slug": "index", "title": "Home", "file": "pages/index.md" }
  ],
  "design": {
    "tokens": "design-tokens.json",
    "components": "component-styles.json",
    "branding": "branding.json"
  },
  "assets": {
    "stylesheets": ["assets/styles/main.css"],
    "scripts": ["assets/scripts/main.js"],
    "fonts": ["assets/fonts/inter.woff2"],
    "icons": ["assets/icons/phone.svg"],
    "images": 42
  },
  "screenshots": {
    "pages": ["screenshots/homepage-desktop.png"],
    "components": ["screenshots/header-desktop.png", "screenshots/dividers/wave-top.png"]
  },
  "warnings": [
    "3 URLs in sitemap returned 404",
    "Wave divider SVGs captured - verify on rebuild"
  ]
}
```
