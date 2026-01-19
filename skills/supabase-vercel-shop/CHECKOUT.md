# Checkout & Order Flow

Complete checkout implementation with Stripe, order creation, and stock management.

## Architecture Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Cart     │ →  │  Checkout   │ →  │   Stripe    │ →  │ Confirmation│
│    Page     │    │    Page     │    │   Payment   │    │    Page     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      ↓                  ↓                  ↓                  ↓
  Local State      Create Session     Webhook Event      Order Display
  (or Supabase)    Stripe Redirect    Order Creation     Thank You
                                      Stock Decrement
```

## Cart Implementation

### Cart State Management

**Option 1: Client-Side Cart (Recommended for most shops)**

```typescript
// src/lib/cart.ts
'use client';

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface CartItem {
  id: string;
  productId: string;
  name: string;
  price: number;  // In pence
  quantity: number;
  image: string;
  variant?: {
    id: string;
    name: string;
    options: Record<string, string>;
  };
}

interface CartStore {
  items: CartItem[];
  addItem: (item: Omit<CartItem, 'id'>) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
  getTotal: () => number;
  getItemCount: () => number;
}

export const useCart = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (item) => {
        const id = `${item.productId}-${item.variant?.id || 'default'}`;
        const existing = get().items.find((i) => i.id === id);

        if (existing) {
          set({
            items: get().items.map((i) =>
              i.id === id ? { ...i, quantity: i.quantity + item.quantity } : i
            ),
          });
        } else {
          set({ items: [...get().items, { ...item, id }] });
        }
      },

      removeItem: (id) => {
        set({ items: get().items.filter((i) => i.id !== id) });
      },

      updateQuantity: (id, quantity) => {
        if (quantity <= 0) {
          get().removeItem(id);
          return;
        }
        set({
          items: get().items.map((i) =>
            i.id === id ? { ...i, quantity } : i
          ),
        });
      },

      clearCart: () => set({ items: [] }),

      getTotal: () => {
        return get().items.reduce((sum, item) => sum + item.price * item.quantity, 0);
      },

      getItemCount: () => {
        return get().items.reduce((sum, item) => sum + item.quantity, 0);
      },
    }),
    {
      name: 'cart-storage',
    }
  )
);
```

### Cart Page Component

```typescript
// src/app/cart/page.tsx
import { Metadata } from 'next';
import { getSetting } from '@/lib/cms';
import CartPageClient from './CartPageClient';

export async function generateMetadata(): Promise<Metadata> {
  const brandName = await getSetting('brand_name');
  return {
    title: brandName ? `Shopping Bag | ${brandName}` : undefined,
  };
}

export default async function CartPage() {
  const brandName = await getSetting('brand_name');

  return <CartPageClient brandName={brandName as string} />;
}
```

```typescript
// src/app/cart/CartPageClient.tsx
'use client';

import { useCart } from '@/lib/cart';
import { formatPrice } from '@/lib/utils';
import Image from 'next/image';
import Link from 'next/link';

interface CartPageClientProps {
  brandName: string;
}

export default function CartPageClient({ brandName }: CartPageClientProps) {
  const { items, removeItem, updateQuantity, getTotal, getItemCount } = useCart();

  // NO FALLBACKS - if cart is empty, show empty state from CMS or nothing
  if (items.length === 0) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        {/* Empty cart message should come from CMS */}
        <Link href="/products" className="btn-primary">
          Continue Shopping
        </Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-serif mb-8">Shopping Bag</h1>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Cart Items */}
        <div className="lg:col-span-2 space-y-4">
          {items.map((item) => (
            <div key={item.id} className="flex gap-4 border-b pb-4">
              {item.image && (
                <div className="relative w-24 h-24 flex-shrink-0">
                  <Image
                    src={item.image}
                    alt={item.name}
                    fill
                    className="object-cover"
                  />
                </div>
              )}

              <div className="flex-1">
                <h3 className="font-medium">{item.name}</h3>
                {item.variant && (
                  <p className="text-sm text-gray-600">
                    {Object.values(item.variant.options).join(' / ')}
                  </p>
                )}
                <p className="font-semibold">{formatPrice(item.price)}</p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => updateQuantity(item.id, item.quantity - 1)}
                  className="w-8 h-8 border rounded"
                  aria-label="Decrease quantity"
                >
                  -
                </button>
                <span className="w-8 text-center">{item.quantity}</span>
                <button
                  onClick={() => updateQuantity(item.id, item.quantity + 1)}
                  className="w-8 h-8 border rounded"
                  aria-label="Increase quantity"
                >
                  +
                </button>
              </div>

              <button
                onClick={() => removeItem(item.id)}
                className="text-gray-400 hover:text-red-500"
                aria-label="Remove item"
              >
                ×
              </button>
            </div>
          ))}
        </div>

        {/* Order Summary */}
        <div className="lg:col-span-1">
          <div className="bg-gray-50 p-6 rounded-lg">
            <h2 className="text-lg font-semibold mb-4">Order Summary</h2>

            <div className="space-y-2 mb-4">
              <div className="flex justify-between">
                <span>Subtotal ({getItemCount()} items)</span>
                <span>{formatPrice(getTotal())}</span>
              </div>
              <div className="flex justify-between">
                <span>Delivery</span>
                <span>Calculated at checkout</span>
              </div>
            </div>

            <div className="border-t pt-4 mb-6">
              <div className="flex justify-between font-semibold">
                <span>Total</span>
                <span>{formatPrice(getTotal())}</span>
              </div>
            </div>

            <Link
              href="/checkout"
              className="block w-full bg-black text-white text-center py-3 hover:bg-gray-800 transition"
            >
              Proceed to Checkout
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
```

### Price Formatting Utility

```typescript
// src/lib/utils.ts
export function formatPrice(pence: number): string {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP',
  }).format(pence / 100);
}
```

## Checkout Flow

### Checkout Page

```typescript
// src/app/checkout/page.tsx
import { Metadata } from 'next';
import { getSetting } from '@/lib/cms';
import CheckoutClient from './CheckoutClient';

export async function generateMetadata(): Promise<Metadata> {
  const brandName = await getSetting('brand_name');
  return {
    title: brandName ? `Checkout | ${brandName}` : undefined,
  };
}

export default async function CheckoutPage() {
  return <CheckoutClient />;
}
```

```typescript
// src/app/checkout/CheckoutClient.tsx
'use client';

import { useState } from 'react';
import { useCart } from '@/lib/cart';
import { formatPrice } from '@/lib/utils';
import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
);

export default function CheckoutClient() {
  const { items, getTotal } = useCart();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCheckout = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          items: items.map((item) => ({
            productId: item.productId,
            variantId: item.variant?.id,
            quantity: item.quantity,
          })),
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Checkout failed');
      }

      const { sessionId } = await response.json();

      const stripe = await stripePromise;
      if (!stripe) throw new Error('Stripe failed to load');

      const { error: stripeError } = await stripe.redirectToCheckout({
        sessionId,
      });

      if (stripeError) {
        throw new Error(stripeError.message);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <p>Your bag is empty</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <h1 className="text-3xl font-serif mb-8">Checkout</h1>

      {/* Order Review */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-4">Order Review</h2>
        {items.map((item) => (
          <div key={item.id} className="flex justify-between py-2 border-b">
            <span>
              {item.name} × {item.quantity}
            </span>
            <span>{formatPrice(item.price * item.quantity)}</span>
          </div>
        ))}
        <div className="flex justify-between py-4 font-semibold">
          <span>Total</span>
          <span>{formatPrice(getTotal())}</span>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 text-red-700 p-4 rounded mb-4">
          {error}
        </div>
      )}

      <button
        onClick={handleCheckout}
        disabled={loading}
        className="w-full bg-black text-white py-4 hover:bg-gray-800 transition disabled:opacity-50"
      >
        {loading ? 'Processing...' : 'Pay with Stripe'}
      </button>

      <p className="text-sm text-gray-500 text-center mt-4">
        You will be redirected to Stripe to complete your payment securely.
      </p>
    </div>
  );
}
```

### Checkout API Route

```typescript
// src/app/api/checkout/route.ts
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { createServiceRoleClient } from '@/lib/supabase-server';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
});

interface CheckoutItem {
  productId: string;
  variantId?: string;
  quantity: number;
}

export async function POST(request: NextRequest) {
  try {
    const { items } = (await request.json()) as { items: CheckoutItem[] };

    if (!items || items.length === 0) {
      return NextResponse.json(
        { error: 'No items provided' },
        { status: 400 }
      );
    }

    const supabase = createServiceRoleClient();

    // Fetch product details from database
    const productIds = items.map((item) => item.productId);
    const { data: products, error: dbError } = await supabase
      .from('products')
      .select('id, name, price, images, stock_quantity')
      .in('id', productIds);

    if (dbError || !products) {
      return NextResponse.json(
        { error: 'Failed to fetch products' },
        { status: 500 }
      );
    }

    // Validate stock and build line items
    const lineItems: Stripe.Checkout.SessionCreateParams.LineItem[] = [];

    for (const item of items) {
      const product = products.find((p) => p.id === item.productId);

      if (!product) {
        return NextResponse.json(
          { error: `Product not found: ${item.productId}` },
          { status: 400 }
        );
      }

      // Check stock
      if (product.stock_quantity !== null && product.stock_quantity < item.quantity) {
        return NextResponse.json(
          { error: `Insufficient stock for ${product.name}` },
          { status: 400 }
        );
      }

      lineItems.push({
        price_data: {
          currency: 'gbp',
          product_data: {
            name: product.name,
            images: product.images?.slice(0, 1) || [],
          },
          unit_amount: product.price, // Already in pence
        },
        quantity: item.quantity,
      });
    }

    // Create Stripe checkout session
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: lineItems,
      mode: 'payment',
      success_url: `${process.env.NEXT_PUBLIC_SITE_URL}/order/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.NEXT_PUBLIC_SITE_URL}/cart`,
      metadata: {
        items: JSON.stringify(items),
      },
      shipping_address_collection: {
        allowed_countries: ['GB'],
      },
      shipping_options: [
        {
          shipping_rate_data: {
            type: 'fixed_amount',
            fixed_amount: { amount: 500, currency: 'gbp' },
            display_name: 'Standard Delivery',
            delivery_estimate: {
              minimum: { unit: 'business_day', value: 3 },
              maximum: { unit: 'business_day', value: 5 },
            },
          },
        },
        {
          shipping_rate_data: {
            type: 'fixed_amount',
            fixed_amount: { amount: 1000, currency: 'gbp' },
            display_name: 'Express Delivery',
            delivery_estimate: {
              minimum: { unit: 'business_day', value: 1 },
              maximum: { unit: 'business_day', value: 2 },
            },
          },
        },
      ],
    });

    return NextResponse.json({ sessionId: session.id });
  } catch (error) {
    console.error('Checkout error:', error);
    return NextResponse.json(
      { error: 'Checkout failed' },
      { status: 500 }
    );
  }
}
```

## Stripe Webhook Handler

### Webhook Route

```typescript
// src/app/api/webhooks/stripe/route.ts
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { createServiceRoleClient } from '@/lib/supabase-server';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
});

const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

export async function POST(request: NextRequest) {
  const body = await request.text();
  const signature = request.headers.get('stripe-signature');

  if (!signature) {
    return NextResponse.json(
      { error: 'No signature' },
      { status: 400 }
    );
  }

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
  } catch (err) {
    console.error('Webhook signature verification failed:', err);
    return NextResponse.json(
      { error: 'Invalid signature' },
      { status: 400 }
    );
  }

  try {
    switch (event.type) {
      case 'checkout.session.completed':
        await handleCheckoutComplete(event.data.object as Stripe.Checkout.Session);
        break;

      case 'payment_intent.payment_failed':
        await handlePaymentFailed(event.data.object as Stripe.PaymentIntent);
        break;
    }

    return NextResponse.json({ received: true });
  } catch (error) {
    console.error('Webhook handler error:', error);
    return NextResponse.json(
      { error: 'Webhook handler failed' },
      { status: 500 }
    );
  }
}

async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
  const supabase = createServiceRoleClient();

  // Parse items from metadata
  const items = JSON.parse(session.metadata?.items || '[]') as Array<{
    productId: string;
    variantId?: string;
    quantity: number;
  }>;

  // Get full session with line items
  const fullSession = await stripe.checkout.sessions.retrieve(session.id, {
    expand: ['line_items', 'customer_details'],
  });

  // Create order in database
  const { data: order, error: orderError } = await supabase
    .from('orders')
    .insert({
      stripe_session_id: session.id,
      stripe_payment_intent: session.payment_intent as string,
      customer_email: fullSession.customer_details?.email,
      customer_name: fullSession.customer_details?.name,
      shipping_address: fullSession.shipping_details?.address,
      total_amount: session.amount_total,
      currency: session.currency?.toUpperCase() || 'GBP',
      status: 'paid',
    })
    .select()
    .single();

  if (orderError || !order) {
    console.error('Failed to create order:', orderError);
    throw new Error('Order creation failed');
  }

  // Create order items
  const orderItems = items.map((item, index) => ({
    order_id: order.id,
    product_id: item.productId,
    variant_id: item.variantId || null,
    quantity: item.quantity,
    unit_price: fullSession.line_items?.data[index]?.amount_total || 0,
  }));

  const { error: itemsError } = await supabase
    .from('order_items')
    .insert(orderItems);

  if (itemsError) {
    console.error('Failed to create order items:', itemsError);
  }

  // Decrement stock
  for (const item of items) {
    const { error: stockError } = await supabase.rpc('decrement_stock', {
      p_product_id: item.productId,
      p_quantity: item.quantity,
    });

    if (stockError) {
      console.error('Failed to decrement stock:', stockError);
    }
  }

  console.log('Order created:', order.id);
}

async function handlePaymentFailed(paymentIntent: Stripe.PaymentIntent) {
  console.error('Payment failed:', paymentIntent.id);
  // Could update order status, send notification, etc.
}
```

### Stock Decrement Function (Database)

```sql
-- Create stock decrement function
CREATE OR REPLACE FUNCTION decrement_stock(
  p_product_id UUID,
  p_quantity INT
)
RETURNS VOID AS $$
BEGIN
  UPDATE products
  SET stock_quantity = GREATEST(0, stock_quantity - p_quantity),
      updated_at = NOW()
  WHERE id = p_product_id
    AND stock_quantity IS NOT NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## Order Confirmation Page

### Success Page

```typescript
// src/app/order/success/page.tsx
import { Suspense } from 'react';
import { getSetting } from '@/lib/cms';
import OrderSuccessClient from './OrderSuccessClient';

export async function generateMetadata() {
  const brandName = await getSetting('brand_name');
  return {
    title: brandName ? `Order Confirmed | ${brandName}` : undefined,
  };
}

export default async function OrderSuccessPage() {
  return (
    <Suspense fallback={<OrderSuccessLoading />}>
      <OrderSuccessClient />
    </Suspense>
  );
}

function OrderSuccessLoading() {
  return (
    <div className="container mx-auto px-4 py-16 text-center">
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-64 mx-auto mb-4" />
        <div className="h-4 bg-gray-200 rounded w-48 mx-auto" />
      </div>
    </div>
  );
}
```

```typescript
// src/app/order/success/OrderSuccessClient.tsx
'use client';

import { useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { useCart } from '@/lib/cart';
import Link from 'next/link';

export default function OrderSuccessClient() {
  const searchParams = useSearchParams();
  const sessionId = searchParams.get('session_id');
  const { clearCart } = useCart();

  // Clear cart on successful order
  useEffect(() => {
    if (sessionId) {
      clearCart();
    }
  }, [sessionId, clearCart]);

  return (
    <div className="container mx-auto px-4 py-16 text-center max-w-lg">
      <div className="mb-8">
        <svg
          className="w-16 h-16 text-green-500 mx-auto"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M5 13l4 4L19 7"
          />
        </svg>
      </div>

      <h1 className="text-3xl font-serif mb-4">Thank You for Your Order</h1>

      <p className="text-gray-600 mb-8">
        Your order has been confirmed. You will receive an email confirmation shortly.
      </p>

      {sessionId && (
        <p className="text-sm text-gray-500 mb-8">
          Order reference: {sessionId.slice(-8).toUpperCase()}
        </p>
      )}

      <Link
        href="/products"
        className="inline-block bg-black text-white px-8 py-3 hover:bg-gray-800 transition"
      >
        Continue Shopping
      </Link>
    </div>
  );
}
```

## Order Database Schema

```sql
-- Orders table
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  stripe_session_id TEXT UNIQUE,
  stripe_payment_intent TEXT,
  customer_email TEXT NOT NULL,
  customer_name TEXT,
  shipping_address JSONB,
  total_amount INT NOT NULL,  -- In pence
  currency TEXT DEFAULT 'GBP',
  status TEXT DEFAULT 'pending' CHECK (status IN (
    'pending', 'paid', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded'
  )),
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Order items table
CREATE TABLE order_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id UUID NOT NULL REFERENCES products(id),
  variant_id UUID REFERENCES product_variants(id),
  quantity INT NOT NULL CHECK (quantity > 0),
  unit_price INT NOT NULL,  -- In pence at time of purchase
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_stripe_session ON orders(stripe_session_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);

-- RLS policies
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE order_items ENABLE ROW LEVEL SECURITY;

-- Users can view their own orders
CREATE POLICY "Users view own orders"
  ON orders FOR SELECT
  USING (
    auth.uid() = user_id
    OR customer_email = auth.jwt()->>'email'
  );

-- Admins can view all orders
CREATE POLICY "Admins view all orders"
  ON orders FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_id = auth.uid()
      AND role_id IN ('super_admin', 'admin', 'shop_editor')
    )
  );

-- Admins can update orders
CREATE POLICY "Admins update orders"
  ON orders FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_id = auth.uid()
      AND role_id IN ('super_admin', 'admin', 'shop_editor')
    )
  );

-- Order items follow order access
CREATE POLICY "View order items with order access"
  ON order_items FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM orders
      WHERE orders.id = order_items.order_id
      AND (
        orders.user_id = auth.uid()
        OR orders.customer_email = auth.jwt()->>'email'
        OR EXISTS (
          SELECT 1 FROM user_roles
          WHERE user_id = auth.uid()
          AND role_id IN ('super_admin', 'admin', 'shop_editor')
        )
      )
    )
  );
```

## Admin Order Management

```typescript
// src/app/admin/orders/page.tsx
import { createServerSupabaseClient } from '@/lib/supabase-server';
import { formatPrice } from '@/lib/utils';

async function getOrders() {
  const supabase = await createServerSupabaseClient();
  const { data } = await supabase
    .from('orders')
    .select(`
      *,
      order_items (
        id,
        quantity,
        unit_price,
        product:products (name)
      )
    `)
    .order('created_at', { ascending: false })
    .limit(50);
  return data || [];
}

export default async function AdminOrdersPage() {
  const orders = await getOrders();

  return (
    <div className="space-y-6">
      <h1 className="admin-h1">Orders</h1>

      <div className="admin-card overflow-hidden">
        <table className="admin-table">
          <thead>
            <tr>
              <th>Order</th>
              <th>Customer</th>
              <th>Items</th>
              <th>Total</th>
              <th>Status</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td className="font-mono text-sm">
                  {order.stripe_session_id?.slice(-8).toUpperCase()}
                </td>
                <td>
                  <div>{order.customer_name}</div>
                  <div className="text-sm text-gray-500">{order.customer_email}</div>
                </td>
                <td>{order.order_items?.length || 0} items</td>
                <td className="font-semibold">{formatPrice(order.total_amount)}</td>
                <td>
                  <span className={`admin-badge admin-badge-${order.status}`}>
                    {order.status}
                  </span>
                </td>
                <td className="text-sm text-gray-500">
                  {new Date(order.created_at).toLocaleDateString('en-GB')}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

## Testing Checklist

```markdown
## Checkout Flow Testing

### Cart
- [ ] Add item to cart
- [ ] Update quantity
- [ ] Remove item
- [ ] Cart persists on page refresh
- [ ] Cart total calculates correctly
- [ ] Empty cart shows appropriate state

### Checkout
- [ ] Checkout redirects to Stripe
- [ ] Stock validation before checkout
- [ ] Invalid items rejected
- [ ] Shipping options display correctly

### Stripe
- [ ] Test card (4242424242424242) works
- [ ] Payment failure handled (4000000000000002)
- [ ] Webhook receives events
- [ ] Order created on success

### Order Confirmation
- [ ] Success page displays
- [ ] Cart cleared on success
- [ ] Order reference shown
- [ ] Email confirmation sent

### Stock Management
- [ ] Stock decremented on successful order
- [ ] Cannot order more than stock
- [ ] Admin can view stock levels

### Admin
- [ ] Orders list displays
- [ ] Order details accessible
- [ ] Status updates work
- [ ] Order items visible
```

## 🚫 Anti-Patterns

```typescript
// ❌ WRONG - Hardcoded shipping prices
const shipping = 5.00;

// ✅ CORRECT - From database or Stripe shipping rates
const shipping = await getShippingRate(address);

// ❌ WRONG - Storing prices client-side for checkout
// Cart stores product prices, used for payment

// ✅ CORRECT - Always fetch prices from database at checkout
// Cart stores product IDs, prices fetched fresh at checkout

// ❌ WRONG - Creating order before payment confirmed
// Order created on checkout initiation

// ✅ CORRECT - Create order only on webhook confirmation
// Order created in webhook handler after Stripe confirms payment

// ❌ WRONG - Trusting client-side total
const total = cartTotal; // From client

// ✅ CORRECT - Calculate total server-side
const total = await calculateOrderTotal(items); // From database prices
```
