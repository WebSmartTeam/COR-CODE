# Frontend Implementation

Public-facing storefront patterns using CMS content, products from database, and zero hardcoding.

## 🚨 MANDATORY: Test After EVERY Component

**YOU MUST run these tests after creating or modifying ANY frontend component.**

Claude defaults to hardcoding. Catch it immediately.

### After Creating/Editing ANY Component:

```bash
# 1. Check THIS specific file for hardcoded content
grep -n "|| '\||| \"\|Welcome\|Lorem\|£[0-9]\|Our \|My " src/components/[YOUR_FILE].tsx

# 2. Check for fallback patterns (BANNED)
grep -n "?? '\||| '\||| \"\|: '" src/components/[YOUR_FILE].tsx

# 3. Check entire components folder
grep -rn "|| '\||| \"" src/components/ --include="*.tsx"

# 4. Check pages folder
grep -rn "|| '\||| \"" src/app/ --include="*.tsx"
```

### If ANY Test Finds Results:
1. **STOP** - Do not continue to next component
2. **FIX** - Remove the hardcoded content or fallback
3. **REPLACE** - Use conditional render pattern
4. **VERIFY** - Run test again, must be clean

### Example Fix:

```typescript
// ❌ TEST FOUND THIS
<h1>{content?.title || 'Welcome'}</h1>

// ✅ REPLACE WITH THIS
{content?.title && <h1>{content.title}</h1>}
```

## Page Structure

```
src/app/
├── page.tsx                    # Homepage (CMS-driven)
├── products/
│   ├── page.tsx               # Product listing
│   └── [slug]/page.tsx        # Product detail
├── categories/
│   └── [slug]/page.tsx        # Category listing
├── about/page.tsx             # About page (CMS)
├── contact/page.tsx           # Contact page (CMS)
├── cart/page.tsx              # Shopping cart
├── checkout/page.tsx          # Checkout flow
└── order-confirmation/page.tsx # Post-purchase
```

## Homepage (CMS-Driven)

```typescript
// src/app/page.tsx
import { getPageContent, getSetting } from '@/lib/cms';
import { getProducts } from '@/lib/products';
import { Hero } from '@/components/sections/Hero';
import { FeaturedProducts } from '@/components/sections/FeaturedProducts';
import { Features } from '@/components/sections/Features';
import { Newsletter } from '@/components/sections/Newsletter';

export default async function HomePage() {
  const [content, featuredProducts, brandName] = await Promise.all([
    getPageContent('home'),
    getProducts({ featured: true, limit: 4 }),
    getSetting('brand_name')
  ]);

  return (
    <main>
      {/* Hero - from CMS */}
      {content.hero && <Hero content={content.hero} />}

      {/* Featured Products - from products table */}
      {featuredProducts.length > 0 && (
        <FeaturedProducts products={featuredProducts} />
      )}

      {/* Features - from CMS */}
      {content.features && <Features content={content.features} />}

      {/* Brand Story - from CMS */}
      {content.story && <BrandStory content={content.story} />}

      {/* Newsletter - from CMS */}
      {content.newsletter && <Newsletter content={content.newsletter} />}
    </main>
  );
}

// Metadata from CMS
export async function generateMetadata() {
  const [brandName, seoContent] = await Promise.all([
    getSetting('brand_name'),
    getPageSection('home', 'seo')
  ]);

  return {
    title: seoContent?.title || brandName,
    description: seoContent?.description
  };
}
```

## Hero Component

```typescript
// src/components/sections/Hero.tsx
import Image from 'next/image';
import Link from 'next/link';

interface HeroContent {
  title: string;
  subtitle?: string;
  description?: string;
  primaryCta?: { text: string; href: string };
  secondaryCta?: { text: string; href: string };
  image?: string;
  videoUrl?: string;
}

export function Hero({ content }: { content: HeroContent }) {
  // NO FALLBACKS - if no title, don't render
  if (!content.title) return null;

  return (
    <section className="relative min-h-[80vh] flex items-center">
      {/* Background */}
      {content.image && (
        <Image
          src={content.image}
          alt=""
          fill
          className="object-cover"
          priority
        />
      )}
      <div className="absolute inset-0 bg-black/40" />

      {/* Content */}
      <div className="relative z-10 container mx-auto px-6">
        <h1 className="text-5xl md:text-7xl font-serif text-white max-w-3xl">
          {content.title}
        </h1>

        {content.subtitle && (
          <p className="text-xl md:text-2xl text-white/90 mt-4 max-w-2xl">
            {content.subtitle}
          </p>
        )}

        {content.description && (
          <p className="text-lg text-white/80 mt-6 max-w-xl">
            {content.description}
          </p>
        )}

        {/* CTAs */}
        <div className="flex gap-4 mt-8">
          {content.primaryCta && (
            <Link
              href={content.primaryCta.href}
              className="btn-primary"
            >
              {content.primaryCta.text}
            </Link>
          )}
          {content.secondaryCta && (
            <Link
              href={content.secondaryCta.href}
              className="btn-secondary"
            >
              {content.secondaryCta.text}
            </Link>
          )}
        </div>
      </div>
    </section>
  );
}
```

## Product Listing Page

```typescript
// src/app/products/page.tsx
import { getProducts, getCategories } from '@/lib/products';
import { getPageContent } from '@/lib/cms';
import { ProductGrid } from '@/components/products/ProductGrid';
import { CategoryFilter } from '@/components/products/CategoryFilter';

interface Props {
  searchParams: Promise<{ category?: string; sort?: string }>;
}

export default async function ProductsPage({ searchParams }: Props) {
  const params = await searchParams;

  const [products, categories, content] = await Promise.all([
    getProducts({
      category: params.category,
      sort: params.sort || 'newest'
    }),
    getCategories(),
    getPageContent('products')
  ]);

  return (
    <main className="container mx-auto px-6 py-12">
      {/* Page Header - from CMS */}
      {content.header && (
        <header className="text-center mb-12">
          <h1 className="text-4xl font-serif">{content.header.title}</h1>
          {content.header.description && (
            <p className="text-lg text-gray-600 mt-4 max-w-2xl mx-auto">
              {content.header.description}
            </p>
          )}
        </header>
      )}

      <div className="flex gap-8">
        {/* Filters */}
        <aside className="w-64 shrink-0">
          <CategoryFilter
            categories={categories}
            activeCategory={params.category}
          />
        </aside>

        {/* Products */}
        <div className="flex-1">
          {products.length > 0 ? (
            <ProductGrid products={products} />
          ) : (
            <p className="text-center text-gray-500 py-12">
              No products found
            </p>
          )}
        </div>
      </div>
    </main>
  );
}
```

## Product Card Component

```typescript
// src/components/products/ProductCard.tsx
import Image from 'next/image';
import Link from 'next/link';
import { Heart } from 'lucide-react';

interface Product {
  id: string;
  name: string;
  slug: string;
  price: number;
  compareAtPrice?: number;
  images: string[];
  category?: { name: string; slug: string };
}

export function ProductCard({ product }: { product: Product }) {
  const hasDiscount = product.compareAtPrice && product.compareAtPrice > product.price;
  const discountPercent = hasDiscount
    ? Math.round((1 - product.price / product.compareAtPrice!) * 100)
    : 0;

  return (
    <article className="group">
      {/* Image */}
      <Link href={`/products/${product.slug}`} className="block relative aspect-[3/4] overflow-hidden bg-gray-100">
        {product.images[0] && (
          <Image
            src={product.images[0]}
            alt={product.name}
            fill
            className="object-cover transition-transform duration-500 group-hover:scale-105"
          />
        )}

        {/* Discount Badge */}
        {hasDiscount && (
          <span className="absolute top-3 left-3 bg-black text-white text-xs px-2 py-1">
            -{discountPercent}%
          </span>
        )}

        {/* Wishlist Button */}
        <button
          className="absolute top-3 right-3 p-2 bg-white/90 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
          aria-label="Add to wishlist"
        >
          <Heart className="w-5 h-5" />
        </button>
      </Link>

      {/* Info */}
      <div className="mt-4">
        {product.category && (
          <p className="text-sm text-gray-500">{product.category.name}</p>
        )}

        <Link href={`/products/${product.slug}`}>
          <h3 className="font-medium mt-1 group-hover:underline">
            {product.name}
          </h3>
        </Link>

        {/* Price - ALWAYS £ */}
        <div className="flex items-center gap-2 mt-2">
          <span className="font-medium">£{product.price.toFixed(2)}</span>
          {hasDiscount && (
            <span className="text-gray-400 line-through text-sm">
              £{product.compareAtPrice!.toFixed(2)}
            </span>
          )}
        </div>
      </div>
    </article>
  );
}
```

## Product Detail Page

```typescript
// src/app/products/[slug]/page.tsx
import { notFound } from 'next/navigation';
import { getProductBySlug, getRelatedProducts } from '@/lib/products';
import { ProductGallery } from '@/components/products/ProductGallery';
import { ProductInfo } from '@/components/products/ProductInfo';
import { AddToCartForm } from '@/components/products/AddToCartForm';
import { RelatedProducts } from '@/components/products/RelatedProducts';

interface Props {
  params: Promise<{ slug: string }>;
}

export default async function ProductPage({ params }: Props) {
  const { slug } = await params;
  const product = await getProductBySlug(slug);

  if (!product) notFound();

  const relatedProducts = await getRelatedProducts(product.id, product.category_id);

  return (
    <main className="container mx-auto px-6 py-12">
      <div className="grid md:grid-cols-2 gap-12">
        {/* Gallery */}
        <ProductGallery images={product.images} name={product.name} />

        {/* Info & Add to Cart */}
        <div>
          <ProductInfo product={product} />
          <AddToCartForm product={product} />
        </div>
      </div>

      {/* Description */}
      {product.description && (
        <section className="mt-16 max-w-3xl">
          <h2 className="text-2xl font-serif mb-6">Details</h2>
          <div
            className="prose prose-lg"
            dangerouslySetInnerHTML={{ __html: product.description }}
          />
        </section>
      )}

      {/* Related Products */}
      {relatedProducts.length > 0 && (
        <section className="mt-20">
          <h2 className="text-2xl font-serif mb-8">You May Also Like</h2>
          <RelatedProducts products={relatedProducts} />
        </section>
      )}
    </main>
  );
}

// Generate static params for build
export async function generateStaticParams() {
  const { data } = await supabase
    .from('products')
    .select('slug')
    .eq('is_active', true);

  return (data || []).map(p => ({ slug: p.slug }));
}

// Metadata
export async function generateMetadata({ params }: Props) {
  const { slug } = await params;
  const product = await getProductBySlug(slug);

  if (!product) return {};

  return {
    title: product.seo_title || product.name,
    description: product.seo_description || product.short_description,
    openGraph: {
      images: product.images[0] ? [product.images[0]] : []
    }
  };
}
```

## Add to Cart Form

```typescript
// src/components/products/AddToCartForm.tsx
'use client';

import { useState } from 'react';
import { useCart } from '@/context/CartContext';
import { ShoppingBag } from 'lucide-react';

interface Product {
  id: string;
  name: string;
  price: number;
  images: string[];
  sizes?: string[];
  colours?: string[];
  variants?: Array<{
    id: string;
    size?: string;
    colour?: string;
    stock_quantity: number;
  }>;
}

export function AddToCartForm({ product }: { product: Product }) {
  const { addItem } = useCart();
  const [selectedSize, setSelectedSize] = useState<string | null>(null);
  const [selectedColour, setSelectedColour] = useState<string | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(false);

  const handleAddToCart = () => {
    const variant = product.variants?.find(
      v => v.size === selectedSize && v.colour === selectedColour
    );

    addItem({
      productId: product.id,
      variantId: variant?.id,
      name: product.name,
      price: product.price,
      quantity,
      image: product.images[0],
      size: selectedSize || undefined,
      colour: selectedColour || undefined
    });

    setAdded(true);
    setTimeout(() => setAdded(false), 2000);
  };

  const canAddToCart =
    (!product.sizes?.length || selectedSize) &&
    (!product.colours?.length || selectedColour);

  return (
    <div className="space-y-6 mt-8">
      {/* Size Selector */}
      {product.sizes && product.sizes.length > 0 && (
        <div>
          <label className="block text-sm font-medium mb-3">Size</label>
          <div className="flex flex-wrap gap-2">
            {product.sizes.map(size => (
              <button
                key={size}
                onClick={() => setSelectedSize(size)}
                className={`px-4 py-2 border transition-colors ${
                  selectedSize === size
                    ? 'border-black bg-black text-white'
                    : 'border-gray-300 hover:border-black'
                }`}
              >
                {size}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Colour Selector */}
      {product.colours && product.colours.length > 0 && (
        <div>
          <label className="block text-sm font-medium mb-3">Colour</label>
          <div className="flex flex-wrap gap-2">
            {product.colours.map(colour => (
              <button
                key={colour}
                onClick={() => setSelectedColour(colour)}
                className={`px-4 py-2 border transition-colors ${
                  selectedColour === colour
                    ? 'border-black bg-black text-white'
                    : 'border-gray-300 hover:border-black'
                }`}
              >
                {colour}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Quantity */}
      <div>
        <label className="block text-sm font-medium mb-3">Quantity</label>
        <div className="flex items-center gap-3">
          <button
            onClick={() => setQuantity(q => Math.max(1, q - 1))}
            className="w-10 h-10 border border-gray-300 flex items-center justify-center"
          >
            -
          </button>
          <span className="w-12 text-center">{quantity}</span>
          <button
            onClick={() => setQuantity(q => q + 1)}
            className="w-10 h-10 border border-gray-300 flex items-center justify-center"
          >
            +
          </button>
        </div>
      </div>

      {/* Add to Cart Button */}
      <button
        onClick={handleAddToCart}
        disabled={!canAddToCart}
        className="w-full btn-primary flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <ShoppingBag className="w-5 h-5" />
        {added ? 'Added to Basket!' : 'Add to Basket'}
      </button>
    </div>
  );
}
```

## Products Library

```typescript
// src/lib/products.ts
import { supabase } from './supabase';

interface ProductFilters {
  category?: string;
  featured?: boolean;
  limit?: number;
  sort?: 'newest' | 'price-asc' | 'price-desc' | 'name';
}

export async function getProducts(filters: ProductFilters = {}) {
  let query = supabase
    .from('products')
    .select('*, category:categories(name, slug)')
    .eq('is_active', true);

  if (filters.category) {
    query = query.eq('categories.slug', filters.category);
  }

  if (filters.featured) {
    query = query.eq('is_featured', true);
  }

  // Sorting
  switch (filters.sort) {
    case 'price-asc':
      query = query.order('price', { ascending: true });
      break;
    case 'price-desc':
      query = query.order('price', { ascending: false });
      break;
    case 'name':
      query = query.order('name');
      break;
    default:
      query = query.order('created_at', { ascending: false });
  }

  if (filters.limit) {
    query = query.limit(filters.limit);
  }

  const { data, error } = await query;

  if (error) {
    console.error('Error fetching products:', error);
    return [];
  }

  return data || [];
}

export async function getProductBySlug(slug: string) {
  const { data, error } = await supabase
    .from('products')
    .select(`
      *,
      category:categories(name, slug),
      variants:product_variants(*)
    `)
    .eq('slug', slug)
    .eq('is_active', true)
    .single();

  if (error) return null;
  return data;
}

export async function getRelatedProducts(productId: string, categoryId?: string) {
  let query = supabase
    .from('products')
    .select('*, category:categories(name, slug)')
    .eq('is_active', true)
    .neq('id', productId)
    .limit(4);

  if (categoryId) {
    query = query.eq('category_id', categoryId);
  }

  const { data } = await query;
  return data || [];
}

export async function getCategories() {
  const { data } = await supabase
    .from('categories')
    .select('*')
    .eq('is_active', true)
    .order('display_order');

  return data || [];
}
```

## Navigation Component

```typescript
// src/components/layout/Header.tsx
import Link from 'next/link';
import { getNavigation, getSetting } from '@/lib/cms';
import { CartButton } from '@/components/cart/CartButton';
import { UserMenu } from '@/components/auth/UserMenu';

export async function Header() {
  const [navigation, brandName, logo] = await Promise.all([
    getNavigation('header'),
    getSetting('brand_name'),
    getSetting('logo_url')
  ]);

  return (
    <header className="sticky top-0 z-50 bg-white border-b">
      <div className="container mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="font-serif text-xl">
            {logo ? (
              <img src={logo as string} alt={brandName as string} className="h-8" />
            ) : (
              brandName
            )}
          </Link>

          {/* Navigation - from database */}
          <nav className="hidden md:flex items-center gap-8">
            {navigation.map(item => (
              <Link
                key={item.id}
                href={item.href}
                className="text-sm hover:text-gray-600 transition-colors"
              >
                {item.label}
              </Link>
            ))}
          </nav>

          {/* Actions */}
          <div className="flex items-center gap-4">
            <UserMenu />
            <CartButton />
          </div>
        </div>
      </div>
    </header>
  );
}
```

## Footer Component

```typescript
// src/components/layout/Footer.tsx
import Link from 'next/link';
import { getNavigation, getSetting, getSiteSettings } from '@/lib/cms';

export async function Footer() {
  const [footerNav, settings] = await Promise.all([
    getNavigation('footer'),
    getSiteSettings()
  ]);

  const brandName = settings.brand_name as string;
  const contactEmail = settings.contact_email as string;
  const socialInstagram = settings.social_instagram as string;

  return (
    <footer className="bg-black text-white py-16">
      <div className="container mx-auto px-6">
        <div className="grid md:grid-cols-4 gap-12">
          {/* Brand */}
          <div>
            <h3 className="font-serif text-xl mb-4">{brandName}</h3>
            {settings.brand_tagline && (
              <p className="text-gray-400 text-sm">{settings.brand_tagline as string}</p>
            )}
          </div>

          {/* Navigation */}
          <div>
            <h4 className="font-medium mb-4">Shop</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              {footerNav
                .filter(item => item.menu_location === 'footer')
                .map(item => (
                  <li key={item.id}>
                    <Link href={item.href} className="hover:text-white transition-colors">
                      {item.label}
                    </Link>
                  </li>
                ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-medium mb-4">Contact</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              {contactEmail && (
                <li>
                  <a href={`mailto:${contactEmail}`} className="hover:text-white">
                    {contactEmail}
                  </a>
                </li>
              )}
            </ul>
          </div>

          {/* Social */}
          <div>
            <h4 className="font-medium mb-4">Follow Us</h4>
            <div className="flex gap-4">
              {socialInstagram && (
                <a
                  href={socialInstagram}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white"
                >
                  Instagram
                </a>
              )}
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-12 pt-8 text-center text-sm text-gray-500">
          © {new Date().getFullYear()} {brandName}. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
```

## Button Styles

```css
/* src/app/globals.css - Add to your Tailwind config */

.btn-primary {
  @apply bg-black text-white px-6 py-3 text-sm font-medium
         hover:bg-gray-900 transition-colors;
}

.btn-secondary {
  @apply border border-white text-white px-6 py-3 text-sm font-medium
         hover:bg-white hover:text-black transition-colors;
}

.btn-outline {
  @apply border border-black text-black px-6 py-3 text-sm font-medium
         hover:bg-black hover:text-white transition-colors;
}
```

## Root Layout

```typescript
// src/app/layout.tsx
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';
import { CartProvider } from '@/context/CartContext';
import './globals.css';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en-GB">
      <body>
        <CartProvider>
          <Header />
          {children}
          <Footer />
        </CartProvider>
      </body>
    </html>
  );
}
```

## 🚫 Anti-Patterns (CRITICAL - Claude Defaults to These)

**Claude's training data is full of these patterns. YOU MUST FIGHT THESE INSTINCTS.**

### BANNED: Fallback Patterns

```tsx
// ❌ BANNED - String fallbacks
{content?.title || 'Shop Our Collection'}
{settings?.brandName ?? 'Brand Name'}
{product.description || 'No description'}

// ❌ BANNED - Ternary fallbacks
{title ? title : 'Default Title'}

// ❌ BANNED - Default function params
function Hero({ title = 'Welcome' }) {}

// ❌ BANNED - Nullish coalescing for content
const displayName = name ?? 'Unknown';

// ✅ CORRECT - Conditional render ONLY
{content?.title && <h1>{content.title}</h1>}
{product.description && <p>{product.description}</p>}

// ✅ CORRECT - Early return for required
if (!content) return null;
```

### BANNED: Hardcoded Content

```tsx
// ❌ BANNED - Any user-visible text
<h1>Welcome to Our Store</h1>
<p>Shop the latest collection</p>
<button>Add to Cart</button>  // Even button text!

// ✅ CORRECT - All from CMS/database
{content.heading && <h1>{content.heading}</h1>}
{settings.ctaText && <button>{settings.ctaText}</button>}
```

### BANNED: Hardcoded Prices

```tsx
// ❌ BANNED - Any hardcoded price
<span>£49.99</span>
<span>From £25</span>
{price || 29.99}

// ✅ CORRECT - Always from database
<span>£{product.price.toFixed(2)}</span>
```

### BANNED: Dollar Signs

```tsx
// ❌ BANNED - American currency
<span>${product.price}</span>
import { DollarSign } from 'lucide-react';

// ✅ CORRECT - UK currency only
<span>£{product.price.toFixed(2)}</span>
import { PoundSterling } from 'lucide-react';
```

### BANNED: Placeholder Text

```tsx
// ❌ BANNED - Lorem ipsum
<p>Lorem ipsum dolor sit amet...</p>

// ❌ BANNED - Generic placeholders
<p>Description goes here</p>
<img alt="Product image" />

// ✅ CORRECT - From CMS or nothing
{product.description && <p>{product.description}</p>}
```

## 🧹 Legacy Cleanup (MANDATORY After Migration)

**When migrating components from hardcoded to CMS, DELETE all old code.**

### What MUST Be Deleted After Migration:

```typescript
// ❌ DELETE - Old constants imports
import { HERO_TITLE, BRAND_NAME } from '@/lib/constants';

// ❌ DELETE - Commented "for reference" code
// Old hardcoded version:
// const title = 'Welcome to Our Store';

// ❌ DELETE - Unused interfaces
interface OldHardcodedProps {
  title?: string;  // DELETE if not used
}

// ❌ DELETE - Migration TODO comments
// TODO: Remove after CMS working

// ❌ DELETE - Temporary fallback code
const temp = content || { title: 'Temp' };  // DELETE
```

### Component Migration Checklist:

```markdown
## Migration: [ComponentName]

### Before
- [ ] Identified ALL hardcoded strings
- [ ] Created CMS entries for each
- [ ] Verified CMS data loads

### After (MANDATORY CLEANUP)
- [ ] Removed ALL hardcoded strings
- [ ] Removed ALL fallback patterns
- [ ] Removed ALL unused imports
- [ ] Removed ALL commented old code
- [ ] Removed ALL TODO comments
- [ ] Deleted unused constants files
- [ ] Ran hardcode detection test
- [ ] Test returns ZERO results
```

### Post-Migration Verification:

```bash
# Must return NOTHING
grep -rn "|| '\||| \"" src/components/[COMPONENT].tsx

# Must return NOTHING
grep -rn "TODO\|FIXME\|for reference" src/components/[COMPONENT].tsx

# Check no orphaned imports
grep -rn "from.*constants" src/components/[COMPONENT].tsx
```

## Component Creation Workflow

**Every new component MUST follow this workflow:**

```markdown
1. CREATE component file
2. IMPLEMENT with CMS data fetching
3. TEST for hardcoding: grep -n "|| '\||| \"" [file]
4. FIX any hardcoded content found
5. TEST again until clean
6. COMMIT only when tests pass
```

**This workflow is NON-NEGOTIABLE.**
