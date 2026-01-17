# URL Discovery Phase (Detailed)

**Phase 1 is the foundation - get this wrong and the rebuild has gaps.**

## Step-by-Step Process

### 1. Ask for Screaming Frog First

```
"Do you have a Screaming Frog export for this site?"
```

If YES:
- Get CSV path
- Parse Address column (URLs)
- Parse Status Code (filter to 200s)
- Parse Content Type (filter text/html for pages)
- Parse Crawl Depth (understand site hierarchy)
- Parse Inlinks/Outlinks (understand page relationships)
- Note: This is the MOST comprehensive source

If NO:
- Proceed with Firecrawl + Sitemap only
- Warn: "Without Screaming Frog, may miss orphan pages"

### 2. Sitemap.xml Analysis (WebFetch)

- Fetch /sitemap.xml
- Fetch /sitemap_index.xml (multiple sitemaps?)
- Check robots.txt for Sitemap: directive
- Parse XML structure:
  - Extract all `<loc>` URLs
  - Extract `<lastmod>` dates
  - Extract `<changefreq>` if present
  - Extract `<priority>` if present

**Freshness Analysis:**
- Fresh: modified <30 days ago
- Stale: 30-90 days ago
- Very stale: >90 days ago
- Unknown: no lastmod (flag as concern!)

### 3. Firecrawl Map (their tokens)

```javascript
firecrawl_map({
  url: "https://example.com",
  includeSubdomains: false,
  limit: 500
})
```

Shows what's ACTUALLY discoverable by following links.

### 4. AJAX/Pagination Check (CRITICAL - Often Missed!)

Many sites hide content behind:
- "Load more" buttons (AJAX)
- Infinite scroll
- Pagination (/page/2, ?page=2, etc.)
- WordPress REST API

#### a) Check for Pagination Patterns
- /blog/page/2, /blog/page/3, etc.
- /news?page=2
- /posts?offset=10
- Detect pattern, crawl ALL pages

#### b) Check for "Load More" Buttons

```javascript
firecrawl_scrape({
  url: "https://example.com/news",
  actions: [
    { type: "click", selector: ".load-more, [data-load-more], button:contains('Load')" },
    { type: "wait", milliseconds: 2000 },
    { type: "click", selector: ".load-more" },
    { type: "wait", milliseconds: 2000 },
    { type: "scrape" }
  ]
})
```

#### c) Check for Infinite Scroll

```javascript
firecrawl_scrape({
  url: "https://example.com/portfolio",
  actions: [
    { type: "scroll", direction: "down" },
    { type: "wait", milliseconds: 2000 },
    { type: "scroll", direction: "down" },
    { type: "wait", milliseconds: 2000 },
    { type: "scroll", direction: "down" },
    { type: "scrape" }
  ]
})
```

#### d) WordPress Specific

If WordPress detected, also check:
- /wp-json/wp/v2/posts?per_page=100 (all posts via API)
- /wp-json/wp/v2/pages?per_page=100 (all pages via API)
- /wp-json/wp/v2/categories (category structure)
- This bypasses pagination entirely!

#### e) Common AJAX Sections to Check
- /news, /blog, /articles (posts)
- /portfolio, /projects, /work (case studies)
- /team, /staff (people)
- /testimonials, /reviews
- /events, /calendar
- /products, /shop (if not full e-commerce)

### 5. Four-Way Comparison (CRITICAL)

Create comparison matrix:

| URL | Sitemap | Firecrawl | SF | AJAX/Pagination | Status |
|-----|---------|-----------|----|-----------------| -------|
| / | ✓ | ✓ | ✓ | - | OK |
| /about | ✓ | ✓ | ✓ | - | OK |
| /old-page | ✓ | ✗ | ✗ | ✗ | ORPHAN? |
| /hidden | ✗ | ✗ | ✓ | ✗ | JS-RENDERED? |
| /news/old-article | ✗ | ✗ | ✗ | ✓ (load more) | AJAX ONLY! |

**Analyse the Differences:**

A) In Sitemap but NOT in Firecrawl:
   - Could be orphan pages (no internal links)
   - Could be sitemap out of date (pages deleted)
   - CHECK: Do these pages actually exist? (fetch each)

B) In Firecrawl but NOT in Sitemap:
   - Sitemap incomplete (common!)
   - New pages not added to sitemap
   - These ARE real pages, include them

C) In Screaming Frog but NOT in others:
   - Pages found via external links
   - Redirects resolved differently
   - JavaScript-rendered content SF captured
   - Investigate each one

D) AJAX/Pagination ONLY (would have been missed!):
   - Items behind "load more" buttons
   - Paginated blog/news posts
   - Infinite scroll content
   - CRITICAL: These are real content, must include!

### 6. Site Structure Understanding

Document:

**Page Types Identified:**
- Homepage
- About/Company pages
- Service/Product pages
- Blog listing + posts
- Contact
- Legal (privacy, terms)
- Other (portfolios, case studies, etc.)

**Navigation Structure:**
- Main nav items
- Footer nav items
- Sidebar if present
- How do page types map to nav?

**Hierarchy:**
- Flat structure or nested?
- Parent-child relationships
- Category/tag structures (blog)

**Concerns/Flags:**
- Orphan pages to investigate
- Missing from sitemap
- Stale content to review
- Broken links detected

### 7. Report & Confirm

```
URL DISCOVERY ANALYSIS COMPLETE
═══════════════════════════════════════

SOURCES:
• Sitemap.xml: X URLs (Y fresh, Z stale, W very stale)
• Firecrawl:   X URLs (live discoverable)
• Screaming Frog: X URLs (comprehensive crawl)

COMPARISON:
• All sources agree: X pages ✓
• In sitemap only: X pages (orphans?)
• In Firecrawl only: X pages (missing from sitemap)
• In SF only: X pages (investigate)

SITE STRUCTURE:
• Page types: [list]
• Hierarchy: [flat/nested]
• Nav structure: [main items]

CONCERNS:
• [List any flags]

MERGED TOTAL: X unique URLs

Proceed with harvest?
```

**WAIT FOR CONFIRMATION before Phase 2.**

Save: /url-discovery.json (complete analysis)
