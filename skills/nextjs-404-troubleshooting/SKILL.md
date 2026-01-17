# Next.js 404 Troubleshooting - Lessons Learned
**Status:** ✅ WORKING

## Common Issues & Solutions

### 1. Next.js 15/16 Async Params
**Problem:** Pages not generating during build - all 404s.

**Fix:**
```typescript
// OLD (broken)
export default function Page({ params }: { params: { slug: string } }) {
  const post = posts.find(p => p.slug === params.slug);
}

// NEW (working)
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = posts.find(p => p.slug === slug);
}
```

Must do in BOTH `generateMetadata()` AND page component.

### 2. localStorage SSR Error
**Problem:** `TypeError: localStorage.getItem is not a function` during build - even in 'use client' components.

**Fix:**
```typescript
if (typeof window === 'undefined') return; // Guard all localStorage calls
localStorage.setItem('key', 'value');
```

### 3. Domain Split
**Problem:** `domain.config.ts` uses apex domain (example.com), `site.ts` uses subdomain (www.example.com).

**Fix:** Unify to a single canonical domain across all config files.

### 4. Duplicate Canonical Helpers
**What we found:** Multiple canonical URL functions across files causing inconsistency.

**Fix:** Consolidated to single `getCanonicalUrl()` in `domain.config.ts`.

## Result
100 pages generated successfully. All dynamic routes returning HTTP/2 200 with `x-vercel-cache: PRERENDER`.
