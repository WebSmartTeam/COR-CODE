# Database Schema

Complete Supabase schema for luxury CMS shop platform. Run migrations in numbered order.

## Core Tables

### Categories

```sql
CREATE TABLE categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  description TEXT,
  image_url TEXT,
  display_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_categories_slug ON categories(slug);
```

### Products

```sql
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
  name TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  description TEXT,
  short_description TEXT,
  price DECIMAL(10,2) NOT NULL,
  compare_at_price DECIMAL(10,2),  -- For showing discounts
  images TEXT[] DEFAULT '{}',
  sizes TEXT[] DEFAULT '{}',
  colours TEXT[] DEFAULT '{}',
  stock_quantity INT DEFAULT 0,
  is_featured BOOLEAN DEFAULT false,
  is_active BOOLEAN DEFAULT true,
  seo_title TEXT,
  seo_description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_slug ON products(slug);
CREATE INDEX idx_products_featured ON products(is_featured) WHERE is_featured = true;
```

### Product Variants

```sql
CREATE TABLE product_variants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID REFERENCES products(id) ON DELETE CASCADE,
  size TEXT,
  colour TEXT,
  sku TEXT UNIQUE,
  price_adjustment DECIMAL(10,2) DEFAULT 0,
  stock_quantity INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Page Content (CMS)

```sql
CREATE TABLE page_content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  page TEXT NOT NULL,
  section TEXT NOT NULL,
  content JSONB NOT NULL DEFAULT '{}',
  display_label TEXT,  -- Human-readable label for admin
  display_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(page, section)
);

CREATE INDEX idx_page_content_page ON page_content(page);
```

### Section Types (CMS Schema)

```sql
CREATE TABLE section_types (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  category TEXT NOT NULL,  -- 'hero', 'content', 'feature', etc.
  description TEXT,
  schema JSONB NOT NULL,   -- JSON Schema for content validation
  default_content JSONB NOT NULL,
  display_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Site Settings

```sql
CREATE TABLE site_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key TEXT NOT NULL UNIQUE,
  value JSONB NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Essential settings to seed:**

```sql
INSERT INTO site_settings (key, value, description) VALUES
('brand_name', '"{{BRAND_NAME}}"', 'Brand name'),
('brand_tagline', '"{{TAGLINE}}"', 'Main tagline'),
('contact_email', '"{{CONTACT_EMAIL}}"', 'Contact email'),
('contact_phone', '"{{CONTACT_PHONE}}"', 'Contact phone'),
('social_instagram', '"{{INSTAGRAM_URL}}"', 'Instagram URL'),
('social_facebook', '"{{FACEBOOK_URL}}"', 'Facebook URL'),
('currency', '{"code": "GBP", "symbol": "£"}', 'Currency settings'),
('shipping_threshold', '100', 'Free shipping threshold in GBP');
```

### Navigation

```sql
CREATE TABLE navigation (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  menu_location TEXT NOT NULL,  -- 'header', 'footer', 'mobile'
  label TEXT NOT NULL,
  href TEXT NOT NULL,
  display_order INT DEFAULT 0,
  is_active BOOLEAN DEFAULT true,
  parent_id UUID REFERENCES navigation(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_navigation_location ON navigation(menu_location);
```

### Orders

```sql
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_number TEXT UNIQUE,  -- Human-readable: ORD-2024-00001
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  email TEXT NOT NULL,
  status TEXT DEFAULT 'pending',
  subtotal DECIMAL(10,2) NOT NULL,
  discount_amount DECIMAL(10,2) DEFAULT 0,
  shipping_cost DECIMAL(10,2) DEFAULT 0,
  total DECIMAL(10,2) NOT NULL,
  shipping_address JSONB,
  billing_address JSONB,
  stripe_payment_intent_id TEXT,
  stripe_session_id TEXT,
  tracking_number TEXT,
  notes TEXT,
  admin_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Order statuses: pending, paid, processing, shipped, delivered, cancelled, refunded
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_number ON orders(order_number);
```

### Order Items

```sql
CREATE TABLE order_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
  product_id UUID REFERENCES products(id) ON DELETE SET NULL,
  variant_id UUID REFERENCES product_variants(id) ON DELETE SET NULL,
  product_name TEXT NOT NULL,
  variant_info TEXT,
  quantity INT NOT NULL DEFAULT 1,
  unit_price DECIMAL(10,2) NOT NULL,
  total_price DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Wishlist

```sql
CREATE TABLE wishlist (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  product_id UUID REFERENCES products(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, product_id)
);

CREATE INDEX idx_wishlist_user ON wishlist(user_id);
```

### Newsletter Subscribers

```sql
CREATE TABLE newsletter_subscribers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL UNIQUE,
  is_active BOOLEAN DEFAULT true,
  source TEXT DEFAULT 'website',
  subscribed_at TIMESTAMPTZ DEFAULT NOW(),
  unsubscribed_at TIMESTAMPTZ
);
```

### Contact Messages

```sql
CREATE TABLE contact_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  subject TEXT NOT NULL,
  message TEXT NOT NULL,
  status TEXT DEFAULT 'new',  -- new, read, replied, archived
  admin_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_contact_messages_status ON contact_messages(status);
```

### Discount Codes

```sql
CREATE TABLE discount_codes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code TEXT NOT NULL UNIQUE,
  description TEXT,
  discount_type TEXT NOT NULL,  -- 'percentage', 'fixed'
  discount_value DECIMAL(10,2) NOT NULL,
  minimum_order DECIMAL(10,2) DEFAULT 0,
  max_uses INT,
  current_uses INT DEFAULT 0,
  valid_from TIMESTAMPTZ DEFAULT NOW(),
  valid_until TIMESTAMPTZ,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Row Level Security

Enable RLS on all tables and create policies:

```sql
-- Enable RLS
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE page_content ENABLE ROW LEVEL SECURITY;
ALTER TABLE site_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE navigation ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE wishlist ENABLE ROW LEVEL SECURITY;

-- Public read for CMS content
CREATE POLICY "Public read categories" ON categories
  FOR SELECT USING (is_active = true);

CREATE POLICY "Public read products" ON products
  FOR SELECT USING (is_active = true);

CREATE POLICY "Public read page_content" ON page_content
  FOR SELECT USING (is_active = true);

CREATE POLICY "Public read site_settings" ON site_settings
  FOR SELECT USING (true);

CREATE POLICY "Public read navigation" ON navigation
  FOR SELECT USING (is_active = true);

-- User-specific policies
CREATE POLICY "Users read own orders" ON orders
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users manage own wishlist" ON wishlist
  FOR ALL USING (auth.uid() = user_id);
```

## Triggers

```sql
-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to relevant tables
CREATE TRIGGER update_products_updated_at
  BEFORE UPDATE ON products
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_orders_updated_at
  BEFORE UPDATE ON orders
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

## Migration Order

1. `001_auth_and_roles.sql` - User profiles, roles, user_roles, invitations
2. `002_storage_buckets.sql` - Supabase storage configuration
3. `003_init.sql` - Core CMS and shop tables
4. `004_rls_security.sql` - Row level security policies
5. `005_seed_data.sql` - Initial content (categories, navigation, settings)
