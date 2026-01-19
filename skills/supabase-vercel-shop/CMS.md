# Content Management System

Zero-hardcoding CMS architecture using Supabase for all content.

## Core Tables

### page_content

Stores all page sections as structured JSON:

```sql
CREATE TABLE page_content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  page TEXT NOT NULL,           -- 'home', 'about', 'contact'
  section TEXT NOT NULL,        -- 'hero', 'features', 'cta'
  content JSONB NOT NULL,       -- Structured content
  display_label TEXT,           -- Human-readable label for admin
  display_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(page, section)
);
```

### section_types

Defines available section schemas:

```sql
CREATE TABLE section_types (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  category TEXT NOT NULL,       -- 'hero', 'content', 'feature'
  description TEXT,
  schema JSONB NOT NULL,        -- JSON Schema for validation
  default_content JSONB NOT NULL,
  display_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true
);
```

### site_settings

Global key-value configuration:

```sql
CREATE TABLE site_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key TEXT NOT NULL UNIQUE,
  value JSONB NOT NULL,
  description TEXT,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## CMS Library

```typescript
// src/lib/cms.ts
import { supabase } from './supabase';

// Get all content for a page
export async function getPageContent(page: string): Promise<Record<string, unknown>> {
  const { data, error } = await supabase
    .from('page_content')
    .select('section, content')
    .eq('page', page)
    .eq('is_active', true)
    .order('display_order');

  if (error) {
    console.error(`Error fetching ${page} content:`, error);
    return {};
  }

  return (data || []).reduce((acc, item) => {
    acc[item.section] = item.content;
    return acc;
  }, {} as Record<string, unknown>);
}

// Get specific section
export async function getPageSection<T = Record<string, unknown>>(
  page: string,
  section: string
): Promise<T | null> {
  const { data, error } = await supabase
    .from('page_content')
    .select('content')
    .eq('page', page)
    .eq('section', section)
    .eq('is_active', true)
    .single();

  if (error) return null;
  return data?.content as T;
}

// Get site setting
export async function getSetting(key: string): Promise<unknown> {
  const { data } = await supabase
    .from('site_settings')
    .select('value')
    .eq('key', key)
    .single();

  return data?.value;
}

// Get all settings as object
export async function getSiteSettings(): Promise<Record<string, unknown>> {
  const { data } = await supabase
    .from('site_settings')
    .select('key, value');

  return (data || []).reduce((acc, item) => {
    acc[item.key] = item.value;
    return acc;
  }, {} as Record<string, unknown>);
}

// Get navigation
export async function getNavigation(location: 'header' | 'footer' | 'mobile') {
  const { data } = await supabase
    .from('navigation')
    .select('*')
    .eq('menu_location', location)
    .eq('is_active', true)
    .order('display_order');

  return data || [];
}
```

## Content Type Interfaces

```typescript
// src/lib/types.ts

// Hero section content
interface HeroContent {
  title: string;
  subtitle?: string;
  description?: string;
  primaryCta?: { text: string; href: string };
  secondaryCta?: { text: string; href: string };
  image?: string;
  videoUrl?: string;
}

// Feature grid content
interface FeaturesContent {
  title: string;
  subtitle?: string;
  items: Array<{
    title: string;
    description: string;
    icon?: string;
    image?: string;
    href?: string;
  }>;
}

// Testimonials content
interface TestimonialsContent {
  title: string;
  items: Array<{
    quote: string;
    author: string;
    role?: string;
    image?: string;
    rating?: number;
  }>;
}

// CTA section content
interface CtaContent {
  title: string;
  description?: string;
  buttonText: string;
  buttonHref: string;
  backgroundImage?: string;
}

// FAQ content
interface FaqContent {
  title: string;
  items: Array<{
    question: string;
    answer: string;
  }>;
}
```

## Using CMS Content in Pages

### Server Component Pattern

```typescript
// src/app/page.tsx
import { getPageContent, getNavigation, getSetting } from '@/lib/cms';
import { Hero } from '@/components/Hero';
import { Features } from '@/components/Features';

export default async function HomePage() {
  const content = await getPageContent('home');
  const navigation = await getNavigation('header');
  const brandName = await getSetting('brand_name');

  return (
    <main>
      {content.hero && <Hero content={content.hero} />}
      {content.features && <Features content={content.features} />}
      {content.cta && <Cta content={content.cta} />}
    </main>
  );
}
```

### Component Pattern

```typescript
// src/components/Hero.tsx
interface HeroProps {
  content: HeroContent;
}

export function Hero({ content }: HeroProps) {
  // NO FALLBACKS - if content missing, don't render
  if (!content.title) return null;

  return (
    <section className="hero">
      <h1>{content.title}</h1>
      {content.subtitle && <p className="subtitle">{content.subtitle}</p>}
      {content.description && <p>{content.description}</p>}

      <div className="cta-buttons">
        {content.primaryCta && (
          <a href={content.primaryCta.href} className="btn-primary">
            {content.primaryCta.text}
          </a>
        )}
        {content.secondaryCta && (
          <a href={content.secondaryCta.href} className="btn-secondary">
            {content.secondaryCta.text}
          </a>
        )}
      </div>

      {content.image && (
        <Image src={content.image} alt={content.title} fill />
      )}
    </section>
  );
}
```

## Seeding Content

```sql
-- Homepage content
INSERT INTO page_content (page, section, content, display_label, display_order) VALUES
(
  'home',
  'hero',
  '{
    "title": "{{BRAND_TAGLINE}}",
    "subtitle": "Welcome to {{BRAND_NAME}}",
    "description": "Discover our collection",
    "primaryCta": {"text": "Shop Now", "href": "/products"},
    "secondaryCta": {"text": "Our Story", "href": "/about"},
    "image": "/images/hero.jpg"
  }',
  'Homepage Hero',
  1
),
(
  'home',
  'features',
  '{
    "title": "Why Choose Us",
    "items": [
      {"title": "Quality", "description": "Premium materials", "icon": "star"},
      {"title": "Service", "description": "Exceptional care", "icon": "heart"},
      {"title": "Delivery", "description": "Fast UK shipping", "icon": "truck"}
    ]
  }',
  'Features Section',
  2
);

-- About page content
INSERT INTO page_content (page, section, content, display_label, display_order) VALUES
(
  'about',
  'story',
  '{
    "title": "Our Story",
    "paragraphs": [
      "Founded in London...",
      "Our mission is..."
    ],
    "image": "/images/story.jpg"
  }',
  'Brand Story',
  1
);

-- Site settings
INSERT INTO site_settings (key, value, description) VALUES
('brand_name', '"{{BRAND_NAME}}"', 'Brand name'),
('brand_tagline', '"{{TAGLINE}}"', 'Main tagline'),
('contact_email', '"{{CONTACT_EMAIL}}"', 'Contact email'),
('social_instagram', '"{{INSTAGRAM_URL}}"', 'Instagram URL'),
('currency', '{"code": "GBP", "symbol": "£"}', 'Currency');
```

## Admin Content Editor

```typescript
// src/app/admin/content/page.tsx
import { createServerSupabaseClient } from '@/lib/supabase-server';
import ContentEditor from './ContentEditor';

async function getAllPageContent() {
  const supabase = await createServerSupabaseClient();
  const { data } = await supabase
    .from('page_content')
    .select('*')
    .order('page')
    .order('display_order');
  return data || [];
}

async function getSectionTypes() {
  const supabase = await createServerSupabaseClient();
  const { data } = await supabase
    .from('section_types')
    .select('*')
    .eq('is_active', true)
    .order('category')
    .order('display_order');
  return data || [];
}

export default async function ContentPage() {
  const [content, sectionTypes] = await Promise.all([
    getAllPageContent(),
    getSectionTypes()
  ]);

  // Group by page
  const contentByPage = content.reduce((acc, item) => {
    if (!acc[item.page]) acc[item.page] = [];
    acc[item.page].push(item);
    return acc;
  }, {});

  return (
    <div className="space-y-6">
      <h1 className="admin-h1">Content Editor</h1>
      <p className="text-[var(--admin-text-secondary)] mt-1">
        Edit page content, sections, and text across the site
      </p>
      <ContentEditor
        pages={Object.keys(contentByPage).sort()}
        contentByPage={contentByPage}
        sectionTypes={sectionTypes}
      />
    </div>
  );
}
```

## Content Update API

```typescript
// src/app/api/admin/content/route.ts
import { requireAdmin } from '@/lib/auth';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function PATCH(request: Request) {
  await requireAdmin();
  const { id, content } = await request.json();

  const supabase = await createServerSupabaseClient();

  const { data, error } = await supabase
    .from('page_content')
    .update({ content, updated_at: new Date().toISOString() })
    .eq('id', id)
    .select()
    .single();

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 400 });
  }

  return NextResponse.json(data);
}

export async function POST(request: Request) {
  await requireAdmin();
  const body = await request.json();

  const supabase = await createServerSupabaseClient();

  const { data, error } = await supabase
    .from('page_content')
    .insert(body)
    .select()
    .single();

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 400 });
  }

  return NextResponse.json(data);
}
```

## 🚫 Anti-Patterns (CRITICAL)

**Claude defaults to these patterns. YOU MUST catch and fix them.**

### BANNED: Fallback Patterns

```tsx
// ❌ BANNED - String fallbacks
{content?.title || 'Welcome to our store'}
{settings?.name ?? 'Brand'}
{data.description || 'No description'}

// ❌ BANNED - Ternary fallbacks
{title ? title : 'Default'}

// ❌ BANNED - Default params
function Section({ title = 'Section Title' }) {}

// ❌ BANNED - Nullish coalescing
const name = content?.name ?? 'Unknown';

// ✅ CORRECT - Conditional render
{content?.title && <h1>{content.title}</h1>}

// ✅ CORRECT - Early return
if (!content) return null;

// ✅ CORRECT - Explicit error for required
if (!content.hero) {
  throw new Error('Homepage hero content not found in CMS');
}
```

### BANNED: Hardcoded Content

```tsx
// ❌ BANNED - Brand names
<title>Your Brand - Home</title>

// ✅ CORRECT
const brandName = await getSetting('brand_name');
<title>{brandName} - Home</title>

// ❌ BANNED - Any visible text
<p>Welcome to our luxury boutique</p>

// ✅ CORRECT
{content?.welcome && <p>{content.welcome}</p>}
```

### BANNED: Styling in Content

```tsx
// ❌ BANNED - HTML in CMS
content = { text: '<strong>Bold</strong>' }

// ✅ CORRECT - Structured data
content = { text: 'Bold', emphasis: 'strong' }
```

## 🚨 MANDATORY: Hardcode Detection Tests

**Run these after EVERY CMS-related change. Not optional.**

### After Any cms.ts or CMS Component Change:

```bash
# 1. Check for fallback patterns (MUST return nothing)
grep -rn "|| '\||| \"\|?? '" src/lib/cms.ts src/components/ --include="*.tsx" --include="*.ts"

# 2. Check for hardcoded brand/content
grep -rn "Welcome\|Our Store\|My Brand\|Lorem" src/ --include="*.tsx"

# 3. Check for hardcoded prices
grep -rn "£[0-9]\|\$[0-9]" src/ --include="*.tsx"

# 4. Check for default function parameters with content
grep -rn "= '\|= \"" src/components/ --include="*.tsx"
```

### Pre-Commit Hook (Add to .husky/pre-commit):

```bash
#!/bin/bash
# Block commits with CMS anti-patterns

if grep -rq "|| '\||| \"" src/ --include="*.tsx"; then
  echo "❌ BLOCKED: Fallback patterns found"
  grep -rn "|| '\||| \"" src/ --include="*.tsx"
  exit 1
fi

if grep -rq "Welcome to\|Our Store\|Lorem" src/ --include="*.tsx"; then
  echo "❌ BLOCKED: Hardcoded content found"
  exit 1
fi

echo "✅ CMS compliance check passed"
```

## 🧹 Legacy Cleanup Requirements

**After migrating content to CMS, DELETE all traces of old code.**

### Must Delete:

```typescript
// ❌ DELETE - Old constants
export const BRAND_NAME = 'Company';
export const HERO_TEXT = 'Welcome';

// ❌ DELETE - Commented old code
// const oldTitle = 'Welcome'; // keeping for reference

// ❌ DELETE - Migration TODOs
// TODO: Remove after CMS is working

// ❌ DELETE - Temporary fallbacks
const temp = data || defaultData;
```

### Verification:

```bash
# No orphaned constants imports
grep -rn "from.*constants" src/ --include="*.tsx"

# No TODO comments about migration
grep -rn "TODO.*CMS\|TODO.*migration" src/ --include="*.tsx"

# No commented code blocks
grep -rn "^// const\|^// export" src/ --include="*.tsx"
```
