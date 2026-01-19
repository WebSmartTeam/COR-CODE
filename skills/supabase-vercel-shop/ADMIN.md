# Admin Dashboard

Professional admin panel architecture with CSS design system and role-based navigation.

## Directory Structure

```
src/app/admin/
├── layout.tsx           # Auth guard + sidebar
├── page.tsx             # Dashboard with analytics
├── products/
│   ├── page.tsx         # Product list
│   ├── new/page.tsx     # Create product
│   └── [id]/page.tsx    # Edit product
├── categories/
│   └── page.tsx         # Category management
├── orders/
│   ├── page.tsx         # Order list
│   └── [id]/page.tsx    # Order detail
├── content/
│   └── page.tsx         # CMS editor
├── marketing/
│   ├── page.tsx         # Marketing overview
│   ├── newsletter/page.tsx
│   └── discounts/page.tsx
├── settings/
│   └── page.tsx         # Site settings
└── users/
    ├── page.tsx         # User management (super_admin only)
    ├── InviteUserForm.tsx
    └── UsersTable.tsx
```

## CSS Design System

Create `src/app/admin/admin.css` with consistent styling:

```css
/* Admin Design System Variables */
:root {
  --admin-bg-primary: #0a0a0a;
  --admin-bg-secondary: #141414;
  --admin-bg-card: #1a1a1a;
  --admin-bg-hover: #242424;
  --admin-border: #2a2a2a;
  --admin-border-hover: #3a3a3a;
  --admin-text-primary: #ffffff;
  --admin-text-secondary: #a0a0a0;
  --admin-text-muted: #666666;
  --admin-accent: #d4af37;       /* Gold accent */
  --admin-accent-hover: #e5c04b;
  --admin-success: #22c55e;
  --admin-warning: #f59e0b;
  --admin-danger: #ef4444;
  --admin-info: #3b82f6;
}

/* Typography */
.admin-h1 { font-size: 1.75rem; font-weight: 600; color: var(--admin-text-primary); }
.admin-h2 { font-size: 1.5rem; font-weight: 600; color: var(--admin-text-primary); }
.admin-h3 { font-size: 1.125rem; font-weight: 500; color: var(--admin-text-primary); }
.admin-label { font-size: 0.875rem; font-weight: 500; color: var(--admin-text-secondary); }

/* Cards */
.admin-card {
  background: var(--admin-bg-card);
  border: 1px solid var(--admin-border);
  border-radius: 0.75rem;
  overflow: hidden;
}
.admin-card-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--admin-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.admin-card-title { font-size: 1rem; font-weight: 500; }
.admin-card-body { padding: 1.5rem; }

/* Buttons */
.admin-btn {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
}
.admin-btn-primary {
  background: var(--admin-accent);
  color: #000;
}
.admin-btn-primary:hover { background: var(--admin-accent-hover); }
.admin-btn-secondary {
  background: transparent;
  border: 1px solid var(--admin-border);
  color: var(--admin-text-primary);
}
.admin-btn-secondary:hover { border-color: var(--admin-border-hover); }
.admin-btn-danger { background: var(--admin-danger); color: white; }
.admin-btn-danger:hover { opacity: 0.9; }

/* Badges */
.admin-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}
.admin-badge-success { background: rgba(34, 197, 94, 0.15); color: var(--admin-success); }
.admin-badge-warning { background: rgba(245, 158, 11, 0.15); color: var(--admin-warning); }
.admin-badge-danger { background: rgba(239, 68, 68, 0.15); color: var(--admin-danger); }
.admin-badge-info { background: rgba(59, 130, 246, 0.15); color: var(--admin-info); }

/* Inputs */
.admin-input {
  width: 100%;
  padding: 0.625rem 0.875rem;
  background: var(--admin-bg-secondary);
  border: 1px solid var(--admin-border);
  border-radius: 0.5rem;
  color: var(--admin-text-primary);
}
.admin-input:focus {
  outline: none;
  border-color: var(--admin-accent);
}

/* Tables */
.admin-table { width: 100%; }
.admin-table th {
  text-align: left;
  padding: 0.75rem 1rem;
  font-weight: 500;
  color: var(--admin-text-secondary);
  border-bottom: 1px solid var(--admin-border);
}
.admin-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--admin-border);
}
.admin-table tr:hover { background: var(--admin-bg-hover); }
```

## Sidebar Component

```typescript
// src/components/admin/layout/AdminSidebar.tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { AuthUser } from '@/lib/auth';

interface NavItem {
  label: string;
  href: string;
  icon: React.ReactNode;
  permission?: 'super_admin' | 'admin' | 'shop_editor' | 'cms_editor';
}

interface NavSection {
  title: string;
  items: NavItem[];
  defaultOpen?: boolean;
}

export function AdminSidebar({ user }: { user: AuthUser }) {
  const pathname = usePathname();

  const sections: NavSection[] = [
    {
      title: 'Overview',
      defaultOpen: true,
      items: [
        { label: 'Dashboard', href: '/admin', icon: <DashboardIcon /> }
      ]
    },
    {
      title: 'Shop',
      defaultOpen: true,
      items: [
        { label: 'Products', href: '/admin/products', icon: <ProductsIcon /> },
        { label: 'Categories', href: '/admin/categories', icon: <CategoriesIcon /> },
        { label: 'Orders', href: '/admin/orders', icon: <OrdersIcon /> }
      ]
    },
    {
      title: 'Content',
      defaultOpen: true,
      items: [
        { label: 'Pages', href: '/admin/content', icon: <PagesIcon /> },
        { label: 'Media', href: '/admin/media', icon: <MediaIcon /> }
      ]
    },
    {
      title: 'Marketing',
      defaultOpen: true,
      items: [
        { label: 'Newsletter', href: '/admin/marketing/newsletter', icon: <NewsletterIcon /> },
        { label: 'Discounts', href: '/admin/marketing/discounts', icon: <DiscountsIcon /> }
      ]
    },
    {
      title: 'Settings',
      defaultOpen: true,
      items: [
        { label: 'Site Settings', href: '/admin/settings', icon: <SettingsIcon /> },
        { label: 'Users', href: '/admin/users', icon: <UsersIcon />, permission: 'super_admin' }
      ]
    }
  ];

  const filteredSections = sections.map(section => ({
    ...section,
    items: section.items.filter(item =>
      !item.permission || user.roles.includes(item.permission)
    )
  })).filter(section => section.items.length > 0);

  return (
    <aside className="admin-sidebar">
      <div className="p-4 border-b border-[var(--admin-border)]">
        <Link href="/admin" className="text-lg font-semibold">
          Admin Panel
        </Link>
      </div>
      <nav className="p-4 space-y-6">
        {filteredSections.map(section => (
          <SidebarSection
            key={section.title}
            section={section}
            pathname={pathname}
          />
        ))}
      </nav>
    </aside>
  );
}
```

## Dashboard Page

```typescript
// src/app/admin/page.tsx
import { getCurrentUser } from '@/lib/auth';
import { createServerSupabaseClient } from '@/lib/supabase-server';

async function getDashboardStats() {
  const supabase = await createServerSupabaseClient();

  const [orders, products, customers, revenue] = await Promise.all([
    supabase.from('orders').select('id', { count: 'exact', head: true }),
    supabase.from('products').select('id', { count: 'exact', head: true }).eq('is_active', true),
    supabase.from('user_profiles').select('id', { count: 'exact', head: true }),
    supabase.from('orders').select('total').eq('status', 'paid')
  ]);

  const totalRevenue = revenue.data?.reduce((sum, o) => sum + Number(o.total), 0) ?? 0;

  return {
    totalOrders: orders.count ?? 0,
    totalProducts: products.count ?? 0,
    totalCustomers: customers.count ?? 0,
    totalRevenue
  };
}

export default async function AdminDashboard() {
  const user = await getCurrentUser();
  const stats = await getDashboardStats();

  return (
    <div className="space-y-6">
      <h1 className="admin-h1">Dashboard</h1>

      <div className="grid grid-cols-4 gap-4">
        <StatCard
          title="Total Revenue"
          value={`£${stats.totalRevenue.toLocaleString()}`}
          icon={<PoundIcon />}  {/* NOT dollar! */}
        />
        <StatCard
          title="Orders"
          value={stats.totalOrders}
          icon={<OrdersIcon />}
        />
        <StatCard
          title="Products"
          value={stats.totalProducts}
          icon={<ProductsIcon />}
        />
        <StatCard
          title="Customers"
          value={stats.totalCustomers}
          icon={<CustomersIcon />}
        />
      </div>

      <div className="grid grid-cols-2 gap-6">
        <RecentOrdersCard />
        <LowStockAlertCard />
      </div>
    </div>
  );
}
```

## Important Rules

### Typography

**ALWAYS use design system classes:**
```tsx
// CORRECT
<h1 className="admin-h1">Page Title</h1>
<h2 className="admin-h2">Section Title</h2>
<h3 className="admin-h3">Card Title</h3>

// WRONG - Don't use arbitrary classes
<h1 className="text-2xl font-bold">Page Title</h1>
```

### UK Icon Standards (CRITICAL)

**ALL icons MUST be UK-appropriate. This is NON-NEGOTIABLE.**

#### Financial Icons - Pound (£) ONLY

```tsx
// ✅ CORRECT - UK Pound Sterling Icon
const PoundIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
    <path d="M6 20h12M6 12h8M10 20V10c0-4 5-6 9-3" />
  </svg>
);

// ❌ WRONG - Dollar sign (BANNED)
const DollarIcon = () => (
  <svg>
    <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
  </svg>
);
```

#### Required Admin Icons (UK Standard)

```tsx
// Admin sidebar & dashboard icons - ALL UK appropriate
const AdminIcons = {
  // Financial - ALWAYS pound symbol
  revenue: PoundIcon,           // ✅ For revenue stats
  earnings: PoundIcon,          // ✅ For earnings displays
  payments: CreditCardIcon,     // ✅ Generic payment icon

  // Navigation - Generic/UK appropriate
  dashboard: LayoutDashboardIcon,
  products: PackageIcon,
  orders: ShoppingBagIcon,
  customers: UsersIcon,
  content: FileTextIcon,
  settings: SettingsIcon,
  media: ImageIcon,

  // Status - Universal symbols
  success: CheckCircleIcon,
  warning: AlertTriangleIcon,
  error: XCircleIcon,
  info: InfoIcon
};
```

#### Dashboard Stat Cards - Pound Icon Mandatory

```tsx
// ✅ CORRECT - All financial stats use PoundIcon
<StatCard
  title="Total Revenue"
  value={`£${stats.totalRevenue.toLocaleString('en-GB')}`}
  icon={<PoundIcon />}  // MANDATORY for financial
/>

<StatCard
  title="Average Order"
  value={`£${stats.avgOrder.toFixed(2)}`}
  icon={<PoundIcon />}  // MANDATORY for financial
/>

// ❌ NEVER DO THIS
<StatCard
  title="Revenue"
  value={`$${stats.revenue}`}  // WRONG - Dollar sign
  icon={<DollarIcon />}        // WRONG - Dollar icon
/>
```

#### Icon Import Guidelines

```tsx
// When using Lucide React or similar:

// ✅ ALLOWED - Generic or UK-appropriate
import {
  PoundSterling,    // ✅ UK currency
  CreditCard,       // ✅ Generic payment
  Wallet,           // ✅ Generic financial
  Banknote,         // ✅ Generic currency
  ShoppingBag,      // ✅ Generic commerce
  Package,          // ✅ Generic products
  Users,            // ✅ Generic customers
  Settings,         // ✅ Generic settings
  LayoutDashboard   // ✅ Generic dashboard
} from 'lucide-react';

// ❌ BANNED - US-specific icons
import {
  DollarSign,       // ❌ BANNED - American
  CircleDollarSign, // ❌ BANNED - American
  BadgeDollarSign,  // ❌ BANNED - American
} from 'lucide-react';
```

#### Pre-Commit Icon Validation

```bash
# Run before any commit - fail if American icons found
grep -r "DollarSign\|dollar\|Dollar" src/ --include="*.tsx" && echo "❌ FAIL: Dollar icons found!" && exit 1
grep -r "\\\$[0-9]" src/ --include="*.tsx" && echo "❌ FAIL: Dollar amounts found!" && exit 1
echo "✅ PASS: No American currency icons found"
```

### No Hardcoding

**All content from database:**
```tsx
// WRONG - Hardcoded brand name
<h1>{{BRAND_NAME}} Admin</h1>

// CORRECT - From site_settings
const brandName = await getSetting('brand_name');
<h1>{brandName} Admin</h1>
```

### Role Permissions

```tsx
// CORRECT - Check permissions before rendering
{user.isSuperAdmin && (
  <Link href="/admin/users">User Management</Link>
)}

// CORRECT - API route protection
export async function POST(request: Request) {
  const user = await requireSuperAdmin();
  // ...
}
```

## Admin API Routes

### Products CRUD

```typescript
// src/app/api/admin/products/route.ts
import { requireAdmin } from '@/lib/auth';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function GET() {
  await requireAdmin();
  const supabase = await createServerSupabaseClient();

  const { data } = await supabase
    .from('products')
    .select('*, category:categories(*)')
    .order('created_at', { ascending: false });

  return NextResponse.json(data);
}

export async function POST(request: Request) {
  await requireAdmin();
  const body = await request.json();
  const supabase = await createServerSupabaseClient();

  const { data, error } = await supabase
    .from('products')
    .insert(body)
    .select()
    .single();

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 400 });
  }

  return NextResponse.json(data);
}
```

### Orders Management

```typescript
// src/app/api/admin/orders/route.ts
export async function PATCH(request: Request) {
  await requireAdmin();
  const { orderId, status, trackingNumber } = await request.json();

  const supabase = await createServerSupabaseClient();

  const { data, error } = await supabase
    .from('orders')
    .update({ status, tracking_number: trackingNumber })
    .eq('id', orderId)
    .select()
    .single();

  // Send status email if status changed
  if (status === 'shipped' && trackingNumber) {
    await sendShippingEmail(data);
  }

  return NextResponse.json(data);
}
```
