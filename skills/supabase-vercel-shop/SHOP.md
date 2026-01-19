# E-Commerce Integration

UK-focused e-commerce with cart, wishlist, and order management. For Stripe payments, see the dedicated **stripe-shop-integration** skill.

## UK Configuration

**Currency**: GBP (£) - amounts in pence for Stripe API
**Locale**: en-GB
**Region**: Vercel London (lhr1)

```typescript
// Currency formatting
function formatPrice(pounds: number): string {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP'
  }).format(pounds);
}
```

## Stripe Integration

**Use the global skill**: `stripe-shop-integration`

This skill covers:
- Client/server library setup
- Payment Intent & Checkout Session flows
- Webhook handling
- UK GBP configuration
- Stripe CLI & MCP integration

**Location**: `~/.claude/skills/stripe-shop-integration/`

## Cart System

### Cart Context (Client-Side)

```typescript
// src/context/CartContext.tsx
'use client';

import { createContext, useContext, useState, useEffect } from 'react';

interface CartItem {
  productId: string;
  variantId?: string;
  name: string;
  price: number;
  quantity: number;
  image?: string;
  size?: string;
  colour?: string;
}

interface CartContext {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (productId: string, variantId?: string) => void;
  updateQuantity: (productId: string, quantity: number, variantId?: string) => void;
  clearCart: () => void;
  subtotal: number;
  itemCount: number;
}

const CartContext = createContext<CartContext | undefined>(undefined);

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([]);

  // Persist to localStorage
  useEffect(() => {
    const stored = localStorage.getItem('cart');
    if (stored) setItems(JSON.parse(stored));
  }, []);

  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(items));
  }, [items]);

  const addItem = (item: CartItem) => {
    setItems(prev => {
      const existing = prev.find(
        i => i.productId === item.productId && i.variantId === item.variantId
      );
      if (existing) {
        return prev.map(i =>
          i.productId === item.productId && i.variantId === item.variantId
            ? { ...i, quantity: i.quantity + item.quantity }
            : i
        );
      }
      return [...prev, item];
    });
  };

  const removeItem = (productId: string, variantId?: string) => {
    setItems(prev => prev.filter(
      i => !(i.productId === productId && i.variantId === variantId)
    ));
  };

  const updateQuantity = (productId: string, quantity: number, variantId?: string) => {
    if (quantity < 1) return removeItem(productId, variantId);
    setItems(prev => prev.map(i =>
      i.productId === productId && i.variantId === variantId
        ? { ...i, quantity }
        : i
    ));
  };

  const clearCart = () => setItems([]);

  const subtotal = items.reduce((sum, i) => sum + i.price * i.quantity, 0);
  const itemCount = items.reduce((sum, i) => sum + i.quantity, 0);

  return (
    <CartContext.Provider value={{
      items, addItem, removeItem, updateQuantity, clearCart, subtotal, itemCount
    }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used within CartProvider');
  return context;
}
```

## Wishlist

```typescript
// src/app/api/wishlist/route.ts
import { requireAuth } from '@/lib/auth';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function GET() {
  const user = await requireAuth();
  const supabase = await createServerSupabaseClient();

  const { data } = await supabase
    .from('wishlist')
    .select('*, product:products(*)')
    .eq('user_id', user.id);

  return NextResponse.json(data);
}

export async function POST(request: Request) {
  const user = await requireAuth();
  const { productId } = await request.json();
  const supabase = await createServerSupabaseClient();

  const { data, error } = await supabase
    .from('wishlist')
    .insert({ user_id: user.id, product_id: productId })
    .select()
    .single();

  if (error?.code === '23505') {
    return NextResponse.json({ error: 'Already in wishlist' }, { status: 409 });
  }

  return NextResponse.json(data);
}

export async function DELETE(request: Request) {
  const user = await requireAuth();
  const { productId } = await request.json();
  const supabase = await createServerSupabaseClient();

  await supabase
    .from('wishlist')
    .delete()
    .eq('user_id', user.id)
    .eq('product_id', productId);

  return NextResponse.json({ success: true });
}
```

## Discount Validation

```typescript
// src/app/api/discount/validate/route.ts
export async function POST(request: Request) {
  const { code, subtotal } = await request.json();
  const supabase = await createServerSupabaseClient();

  const { data: discount } = await supabase
    .from('discount_codes')
    .select('*')
    .eq('code', code.toUpperCase())
    .eq('is_active', true)
    .gte('valid_until', new Date().toISOString())
    .single();

  if (!discount) {
    return NextResponse.json({ valid: false, error: 'Invalid or expired code' });
  }

  if (discount.max_uses && discount.current_uses >= discount.max_uses) {
    return NextResponse.json({ valid: false, error: 'Code usage limit reached' });
  }

  if (subtotal < discount.minimum_order) {
    return NextResponse.json({
      valid: false,
      error: `Minimum order £${discount.minimum_order} required`
    });
  }

  const discountAmount = discount.discount_type === 'percentage'
    ? subtotal * (discount.discount_value / 100)
    : discount.discount_value;

  return NextResponse.json({
    valid: true,
    discountType: discount.discount_type,
    discountValue: discount.discount_value,
    discountAmount,
    description: discount.description
  });
}
```

## Order Status Emails

```typescript
// src/lib/order-emails.ts
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function sendOrderConfirmationEmail(order: Order) {
  const brandName = await getSetting('brand_name');

  await resend.emails.send({
    from: `${brandName} <orders@{{DOMAIN}}>`,
    to: order.email,
    subject: `Order Confirmed - ${order.order_number}`,
    html: `
      <h1>Thank you for your order!</h1>
      <p>Order number: ${order.order_number}</p>
      <p>Total: £${order.total.toFixed(2)}</p>
    `
  });
}

export async function sendShippingEmail(order: Order) {
  const brandName = await getSetting('brand_name');

  await resend.emails.send({
    from: `${brandName} <orders@{{DOMAIN}}>`,
    to: order.email,
    subject: `Your order has shipped - ${order.order_number}`,
    html: `
      <h1>Your order is on its way!</h1>
      <p>Tracking number: ${order.tracking_number}</p>
    `
  });
}
```

## UK Icon Standards for E-Commerce

**ALL shop icons MUST be UK-appropriate. NO American symbols.**

### Financial Icons - Pound (£) ONLY

```tsx
// ✅ CORRECT - UK Pound Icon for all price displays
const PoundIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
    <path d="M6 20h12M6 12h8M10 20V10c0-4 5-6 9-3" />
  </svg>
);

// Price display component
function PriceDisplay({ price }: { price: number }) {
  return (
    <span className="flex items-center gap-1">
      <PoundIcon className="w-4 h-4" />
      {price.toFixed(2)}
    </span>
  );
}

// ❌ BANNED - Dollar icon
// Never use DollarSign, CircleDollarSign, BadgeDollarSign
```

### Cart & Checkout Icons

```tsx
// ✅ CORRECT - UK appropriate icons
import { ShoppingBag, CreditCard, Truck, Package, Heart } from 'lucide-react';

// Cart icon - generic shopping bag
<ShoppingBag />

// Payment icon - generic credit card (NOT dollar)
<CreditCard />

// Shipping icon - generic truck
<Truck />

// Order icon - generic package
<Package />

// Wishlist icon - generic heart
<Heart />
```

### Currency Symbol Rules

```tsx
// ✅ CORRECT - Always £ prefix
<span>£{price.toFixed(2)}</span>
<span>£99.99</span>
<span>Total: £{total.toLocaleString('en-GB')}</span>

// ❌ WRONG - Dollar signs BANNED
<span>${price}</span>
<span>$99.99</span>
```

### Order Status Icons

```tsx
// ✅ CORRECT - UK standard icons for order status
const OrderStatusIcons = {
  pending: ClockIcon,           // ✅ Generic
  paid: CheckCircleIcon,        // ✅ Generic
  processing: PackageIcon,      // ✅ Generic
  shipped: TruckIcon,           // ✅ Generic
  delivered: HomeIcon,          // ✅ Generic
  cancelled: XCircleIcon,       // ✅ Generic
  refunded: RefreshCwIcon,      // ✅ Generic - NOT RefundDollarIcon!
};
```

### Icon Checklist

Before deploying shop features:

- [ ] All price displays show £ symbol
- [ ] No dollar icons ($) in cart or checkout
- [ ] Payment icons are generic (CreditCard, Wallet)
- [ ] Order status icons are generic/universal
- [ ] Email templates use £ for all amounts
- [ ] Currency formatted with en-GB locale

## Pre-Deployment Validation

```bash
# Check for American currency references
grep -r "DollarSign\|dollar\|Dollar\|\\\$[0-9]" src/ --include="*.tsx" && exit 1
grep -r "USD\|usd" src/ --include="*.tsx" && exit 1

# Verify GBP usage
grep -r "GBP\|gbp\|£" src/ --include="*.tsx" && echo "✅ UK currency found"
```
