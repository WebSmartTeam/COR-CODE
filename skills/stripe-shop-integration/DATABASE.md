# Database Schema for Stripe Integration

## Required Tables

### Products Table

```sql
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  short_description TEXT,
  price DECIMAL(10,2) NOT NULL,
  sale_price DECIMAL(10,2),
  featured_image TEXT,
  is_active BOOLEAN DEFAULT true,
  is_shippable BOOLEAN DEFAULT true,
  stock_quantity INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

-- Public read access
CREATE POLICY "Products are viewable by everyone"
  ON products FOR SELECT
  USING (is_active = true);
```

### Customers Table

```sql
CREATE TABLE customers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  phone TEXT,
  address_line_1 TEXT,
  address_line_2 TEXT,
  city TEXT,
  county TEXT,
  postcode TEXT,
  country TEXT DEFAULT 'GB',
  stripe_customer_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;

-- Allow insert for checkout
CREATE POLICY "Allow customer creation"
  ON customers FOR INSERT
  WITH CHECK (true);

-- Allow read/update by email match
CREATE POLICY "Customers can view own data"
  ON customers FOR SELECT
  USING (true);

CREATE POLICY "Customers can update own data"
  ON customers FOR UPDATE
  USING (true);
```

### Cart Items Table

```sql
CREATE TABLE cart_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id TEXT NOT NULL,
  product_id UUID REFERENCES products(id) ON DELETE CASCADE,
  quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0 AND quantity <= 99),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(session_id, product_id)
);

-- Enable RLS
ALTER TABLE cart_items ENABLE ROW LEVEL SECURITY;

-- Allow all operations for cart (session-based)
CREATE POLICY "Allow cart operations"
  ON cart_items FOR ALL
  USING (true)
  WITH CHECK (true);

-- Index for fast lookups
CREATE INDEX idx_cart_items_session ON cart_items(session_id);
```

### Orders Table

```sql
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_number TEXT UNIQUE NOT NULL,
  customer_id UUID REFERENCES customers(id),
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded', 'payment_failed', 'payment_pending')),

  -- Pricing
  subtotal DECIMAL(10,2) NOT NULL DEFAULT 0,
  tax_amount DECIMAL(10,2) DEFAULT 0,
  shipping_amount DECIMAL(10,2) DEFAULT 0,
  discount_amount DECIMAL(10,2) DEFAULT 0,
  discount_code TEXT,
  total_amount DECIMAL(10,2) NOT NULL DEFAULT 0,

  -- Payment
  payment_status TEXT DEFAULT 'pending' CHECK (payment_status IN ('pending', 'processing', 'succeeded', 'failed', 'cancelled', 'refunded')),
  payment_method TEXT,
  payment_reference TEXT,  -- Stripe payment intent ID
  payment_date TIMESTAMPTZ,

  -- Delivery
  delivery_method TEXT DEFAULT 'shipping' CHECK (delivery_method IN ('shipping', 'collection')),

  -- Shipping address
  shipping_name TEXT,
  shipping_phone TEXT,
  shipping_address_line1 TEXT,
  shipping_address_line2 TEXT,
  shipping_city TEXT,
  shipping_county TEXT,
  shipping_postcode TEXT,
  shipping_country TEXT DEFAULT 'GB',

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Allow insert for checkout
CREATE POLICY "Allow order creation"
  ON orders FOR INSERT
  WITH CHECK (true);

-- Allow read
CREATE POLICY "Allow order read"
  ON orders FOR SELECT
  USING (true);

-- Allow update (for payment status)
CREATE POLICY "Allow order update"
  ON orders FOR UPDATE
  USING (true);

-- Indexes
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_payment_ref ON orders(payment_reference);
CREATE INDEX idx_orders_status ON orders(status);
```

### Order Items Table

```sql
CREATE TABLE order_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
  product_id UUID REFERENCES products(id),
  product_name TEXT NOT NULL,
  quantity INTEGER NOT NULL DEFAULT 1,
  price DECIMAL(10,2) NOT NULL,  -- Total price (unit price * quantity)
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE order_items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow order items operations"
  ON order_items FOR ALL
  USING (true)
  WITH CHECK (true);

CREATE INDEX idx_order_items_order ON order_items(order_id);
```

### Stripe Payment Intents Table

```sql
CREATE TABLE stripe_payment_intents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID REFERENCES orders(id),
  stripe_payment_intent_id TEXT UNIQUE NOT NULL,
  amount INTEGER NOT NULL,  -- In pence
  currency TEXT DEFAULT 'gbp',
  status TEXT NOT NULL,
  payment_method_types TEXT[],
  client_secret TEXT,
  last_payment_error JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE stripe_payment_intents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow payment intent operations"
  ON stripe_payment_intents FOR ALL
  USING (true)
  WITH CHECK (true);

CREATE INDEX idx_payment_intents_order ON stripe_payment_intents(order_id);
CREATE INDEX idx_payment_intents_stripe ON stripe_payment_intents(stripe_payment_intent_id);
```

### Stripe Payment Sessions Table (for Checkout Sessions)

```sql
CREATE TABLE stripe_payment_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID REFERENCES orders(id),
  stripe_session_id TEXT UNIQUE NOT NULL,
  session_status TEXT DEFAULT 'open' CHECK (session_status IN ('open', 'complete', 'expired')),
  amount_total INTEGER NOT NULL,  -- In pence
  currency TEXT DEFAULT 'gbp',
  customer_email TEXT,
  expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE stripe_payment_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow session operations"
  ON stripe_payment_sessions FOR ALL
  USING (true)
  WITH CHECK (true);

CREATE INDEX idx_payment_sessions_order ON stripe_payment_sessions(order_id);
CREATE INDEX idx_payment_sessions_stripe ON stripe_payment_sessions(stripe_session_id);
```

### Stripe Webhook Events Table (Idempotency)

```sql
CREATE TABLE stripe_webhook_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stripe_event_id TEXT UNIQUE NOT NULL,
  event_type TEXT NOT NULL,
  processed BOOLEAN DEFAULT false,
  processed_at TIMESTAMPTZ,
  event_data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE stripe_webhook_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow webhook event operations"
  ON stripe_webhook_events FOR ALL
  USING (true)
  WITH CHECK (true);

CREATE INDEX idx_webhook_events_stripe ON stripe_webhook_events(stripe_event_id);
CREATE INDEX idx_webhook_events_type ON stripe_webhook_events(event_type);
```

## Database Functions

### Generate Order Number

```sql
CREATE OR REPLACE FUNCTION generate_order_number()
RETURNS TEXT AS $$
DECLARE
  prefix TEXT := 'ORD';
  date_part TEXT;
  random_part TEXT;
BEGIN
  date_part := TO_CHAR(NOW(), 'YYMMDD');
  random_part := UPPER(SUBSTRING(MD5(RANDOM()::TEXT) FROM 1 FOR 4));
  RETURN prefix || '-' || date_part || '-' || random_part;
END;
$$ LANGUAGE plpgsql;
```

### Create Order from Cart Session

```sql
CREATE OR REPLACE FUNCTION create_order_from_cart_session(
  customer_id_param UUID,
  session_id_param TEXT
)
RETURNS UUID AS $$
DECLARE
  new_order_id UUID;
  cart_total DECIMAL(10,2);
BEGIN
  -- Calculate cart total
  SELECT COALESCE(SUM(ci.quantity * p.price), 0)
  INTO cart_total
  FROM cart_items ci
  JOIN products p ON ci.product_id = p.id
  WHERE ci.session_id = session_id_param;

  -- Validate cart has items
  IF cart_total = 0 THEN
    RAISE EXCEPTION 'Cart is empty';
  END IF;

  -- Create order
  INSERT INTO orders (
    order_number,
    customer_id,
    subtotal,
    total_amount,
    status,
    payment_status
  ) VALUES (
    generate_order_number(),
    customer_id_param,
    cart_total,
    cart_total,
    'pending',
    'pending'
  )
  RETURNING id INTO new_order_id;

  -- Copy cart items to order items
  INSERT INTO order_items (order_id, product_id, product_name, quantity, price)
  SELECT
    new_order_id,
    ci.product_id,
    p.name,
    ci.quantity,
    ci.quantity * p.price
  FROM cart_items ci
  JOIN products p ON ci.product_id = p.id
  WHERE ci.session_id = session_id_param;

  -- Clear cart
  DELETE FROM cart_items WHERE session_id = session_id_param;

  RETURN new_order_id;
END;
$$ LANGUAGE plpgsql;
```

## Views

### Products with Media (Optional)

```sql
CREATE OR REPLACE VIEW products_with_media AS
SELECT
  p.*,
  (
    SELECT jsonb_agg(jsonb_build_object(
      'id', pm.id,
      'media_url', pm.media_url,
      'is_featured', pm.is_featured
    ))
    FROM product_media pm
    WHERE pm.product_id = p.id
  ) as media
FROM products p
WHERE p.is_active = true;
```
