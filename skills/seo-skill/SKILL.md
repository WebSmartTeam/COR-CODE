---
name: seo-skill
description: Technical SEO patterns, structured data, and search optimisation for web projects
---

# SEO Skill

Technical SEO knowledge for web frontend work. Works alongside GMB agent for local SEO.

## Critical: Visible vs Hidden Content

**DO NOT automatically change visible/on-page content.** SEO optimisation should only modify:

| Can Modify | Cannot Modify |
|------------|---------------|
| Meta tags (title, description) | Body text / paragraphs |
| Schema.org JSON-LD | Headings text content |
| Open Graph / Twitter cards | Button labels |
| Canonical URLs | Navigation text |
| robots.txt / sitemap | Any user-visible content |
| Alt text (with care) | |

For visible content improvements, **produce a report with recommendations** - don't apply changes automatically.

## SEO Improvement Report Format

After SEO work, provide summary:

```markdown
## SEO Improvements Applied

### Hidden/Technical Changes Made:
- ✅ Added meta description to /services page
- ✅ Added BreadcrumbList schema to all pages

### Visible Content Recommendations (Requires Review):
| Page | Issue | Recommendation |
|------|-------|----------------|
| /about | Thin content (180 words) | Expand to 400+ words |
| /services | No H1 contains keyword | Consider: "Professional [Service] in [Location]" |

### SEO Score Summary:
- Pages analysed: 12
- Issues fixed: 8
- Recommendations pending: 4
```

## Meta Tag Targets

| Tag | Target Length | Notes |
|-----|---------------|-------|
| Title | 50-60 chars | Primary keyword near start |
| Description | 150-160 chars | Compelling summary with CTA |
| Canonical | Full URL | Prevents duplicate content |

Use Next.js metadata API (static or generateMetadata for dynamic).

## Semantic HTML

- **One H1 per page** - the main topic
- **Logical heading hierarchy** - H2 sections, H3 subsections (don't skip)
- **Landmarks** - `<header>`, `<main>`, `<nav>`, `<footer>`, `<article>`, `<aside>`
- **Strategic `<strong>`** - 2-3 per page for key entities

## Structured Data (Schema.org)

Use JSON-LD in `<head>`. Common types:

| Schema Type | When to Use |
|-------------|-------------|
| BreadcrumbList | Navigation path (enables rich snippets) |
| FAQPage | FAQ sections (expandable results) |
| Article/BlogPosting | Blog content |
| LocalBusiness | Business sites (coordinates with GMB agent) |
| HowTo | Instructional content |

Claude knows Schema.org syntax - just specify which types are needed.

## Content Guidelines

### Length Targets (Total Across Page)

| Content Type | Minimum | Optimal |
|--------------|---------|---------|
| Service page | 300 words | 600+ |
| Blog post | 400 words | 1000+ |
| Product page | 200 words | 400+ |

**Distribute naturally** across hero, features, FAQ, CTA - not one block.

### Keyword Usage
- **Density**: 0.5-2% natural occurrence
- **Placement**: H1, first paragraph, URL, meta description
- **Variations**: Semantic variations naturally

## Image SEO

- **Alt text** - descriptive, keywords natural (not stuffing)
- **File names** - descriptive (`blue-widget-product.jpg` not `IMG_1234.jpg`)
- **Dimensions** - always specify (prevents CLS)
- **Format** - WebP/AVIF with fallbacks
- **Lazy loading** - use Next.js Image component

## Technical SEO

- **robots.txt** - control crawler access
- **sitemap.xml** - all indexable URLs with lastmod
- **Canonical URLs** - prevent duplicate content
- **HTTPS** - required
- **Mobile-friendly** - Google indexes mobile-first
- **Core Web Vitals** - LCP <2.5s, FID <100ms, CLS <0.1

### AI Crawlers (Modern Consideration)

Don't block AI crawlers unless specific reason:
- GPTBot (ChatGPT)
- Google-Extended (Gemini/AI Overviews)
- anthropic-ai (Claude)
- PerplexityBot

Being cited by AI systems is increasingly valuable.

## Site-Wide Audit Checklist

When reviewing a site, check and **advise** (don't auto-implement):

### Images
- [ ] Modern formats (WebP/AVIF)?
- [ ] Properly sized (not 4000px displayed at 400px)?
- [ ] Lazy loading?
- [ ] Alt text present?

### Navigation
- [ ] Breadcrumbs (Schema + visible)?
- [ ] Logical URLs (/services/web-design not /page?id=47)?
- [ ] Internal linking between related pages?
- [ ] 404 page helpful?

### Technical
- [ ] robots.txt reviewed?
- [ ] sitemap.xml submitted?
- [ ] HTTPS everywhere?
- [ ] Mobile responsive?

### Content
- [ ] No thin pages (<300 words)?
- [ ] No duplicate content?
- [ ] Dates on blog posts?
- [ ] Contact/about pages exist?

### Local SEO (if applicable)
- [ ] LocalBusiness schema?
- [ ] NAP consistent?
- [ ] GMB linked? (GMB agent)

**Output findings as recommendations, not changes.**

## UK Considerations

- **UK English** - British spellings throughout
- **Local keywords** - include town/region names
- **hreflang** - if multi-region: `hreflang="en-GB"`
- **LocalBusiness** - UK address format, +44 phone
- **Coordinates with GMB agent** - for local business SEO

## Accessibility = SEO

Good accessibility benefits SEO:
- Semantic HTML helps both screen readers and crawlers
- Alt text required for accessibility, used by image search
- Heading hierarchy helps both
- Descriptive link text (not "Read more")
