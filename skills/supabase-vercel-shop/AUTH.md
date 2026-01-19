# Authentication & Roles

Enterprise RBAC (Role-Based Access Control) with Supabase Auth.

## Role Hierarchy

| Role | Access Level | Permissions |
|------|--------------|-------------|
| `super_admin` | Full system | All admin + user management |
| `admin` | Shop + CMS | Products, orders, content |
| `shop_editor` | Shop only | Products, orders, categories |
| `cms_editor` | CMS only | Page content, navigation, settings |
| `customer` | Public | Browse, purchase, own orders |

## Schema

### Roles Table

```sql
CREATE TABLE roles (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  permissions JSONB DEFAULT '{}',
  is_admin_role BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO roles (id, name, description, permissions, is_admin_role) VALUES
  ('super_admin', 'Super Admin', 'Full system access', '{"all": true}', TRUE),
  ('admin', 'Admin', 'Shop and CMS management', '{"shop": true, "cms": true}', TRUE),
  ('shop_editor', 'Shop Editor', 'Products and orders', '{"shop": true}', TRUE),
  ('cms_editor', 'CMS Editor', 'Content and pages', '{"cms": true}', TRUE),
  ('customer', 'Customer', 'Standard customer', '{"shop_browse": true}', FALSE);
```

### User Roles (Many-to-Many)

```sql
CREATE TABLE user_roles (
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  role_id TEXT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
  granted_by UUID REFERENCES auth.users(id),
  granted_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, role_id)
);
```

### Admin Invitations

```sql
CREATE TABLE admin_invitations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL,
  role_id TEXT NOT NULL REFERENCES roles(id),
  invited_by UUID NOT NULL REFERENCES auth.users(id),
  token TEXT UNIQUE NOT NULL DEFAULT encode(gen_random_bytes(32), 'hex'),
  expires_at TIMESTAMPTZ NOT NULL DEFAULT NOW() + INTERVAL '7 days',
  accepted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Auth Library

```typescript
// src/lib/auth.ts
import { createServerSupabaseClient, createServiceRoleClient } from './supabase-server';

export interface AuthUser {
  id: string;
  email: string;
  isAdmin: boolean;
  isSuperAdmin: boolean;
  roles: string[];
}

export async function getCurrentUser(): Promise<AuthUser | null> {
  const supabase = await createServerSupabaseClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) return null;

  // Service role for role queries (bypasses RLS)
  const serviceClient = createServiceRoleClient();

  const { data: userRoles } = await serviceClient
    .from('user_roles')
    .select('role_id')
    .eq('user_id', user.id);

  const roles = userRoles?.map(r => r.role_id) ?? [];

  const { data: adminRoles } = await serviceClient
    .from('roles')
    .select('id')
    .eq('is_admin_role', true);

  const adminRoleIds = adminRoles?.map(r => r.id) ?? [];
  const isAdmin = roles.some(r => adminRoleIds.includes(r));

  return {
    id: user.id,
    email: user.email!,
    isAdmin,
    isSuperAdmin: roles.includes('super_admin'),
    roles
  };
}

export async function requireAuth(): Promise<AuthUser> {
  const user = await getCurrentUser();
  if (!user) throw new Error('UNAUTHORIZED');
  return user;
}

export async function requireAdmin(): Promise<AuthUser> {
  const user = await requireAuth();
  if (!user.isAdmin) throw new Error('FORBIDDEN');
  return user;
}

export async function requireSuperAdmin(): Promise<AuthUser> {
  const user = await requireAuth();
  if (!user.isSuperAdmin) throw new Error('FORBIDDEN');
  return user;
}

export async function getAvailableRoles() {
  const serviceClient = createServiceRoleClient();
  const { data } = await serviceClient
    .from('roles')
    .select('id, name, description, is_admin_role')
    .order('is_admin_role', { ascending: false });
  return data ?? [];
}

export async function hasPermission(permission: string): Promise<boolean> {
  const user = await getCurrentUser();
  if (!user) return false;

  const serviceClient = createServiceRoleClient();
  const { data } = await serviceClient
    .from('user_roles')
    .select('roles:role_id(permissions)')
    .eq('user_id', user.id);

  for (const item of data ?? []) {
    const role = item.roles as { permissions: Record<string, boolean> };
    if (role?.permissions?.all || role?.permissions?.[permission]) return true;
  }
  return false;
}
```

## Middleware Protection

```typescript
// src/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { createServerClient } from '@supabase/ssr';

export async function middleware(request: NextRequest) {
  const response = NextResponse.next();

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => request.cookies.getAll(),
        setAll: (cookies) => cookies.forEach(c => response.cookies.set(c))
      }
    }
  );

  const { data: { session } } = await supabase.auth.getSession();

  // Protect /admin routes
  if (request.nextUrl.pathname.startsWith('/admin')) {
    if (!session) {
      return NextResponse.redirect(new URL('/auth/login?redirect=/admin', request.url));
    }
  }

  return response;
}

export const config = {
  matcher: ['/admin/:path*', '/account/:path*']
};
```

## Admin Layout Guard

```typescript
// src/app/admin/layout.tsx
import { getCurrentUser } from '@/lib/auth';
import { redirect } from 'next/navigation';

export default async function AdminLayout({ children }) {
  const user = await getCurrentUser();

  if (!user || !user.isAdmin) {
    redirect('/auth/login?error=admin_required');
  }

  return (
    <div className="admin-layout">
      <AdminSidebar user={user} />
      <main>{children}</main>
    </div>
  );
}
```

## Invitation Flow

### 1. Create Invitation API

```typescript
// src/app/api/admin/invite/route.ts
export async function POST(request: Request) {
  const user = await requireSuperAdmin();
  const { email, roleId } = await request.json();

  const supabase = await createServerSupabaseClient();

  const { data, error } = await supabase
    .from('admin_invitations')
    .insert({
      email,
      role_id: roleId,
      invited_by: user.id
    })
    .select()
    .single();

  // Send invitation email with token link
  await sendInvitationEmail(email, data.token);

  return NextResponse.json({ success: true });
}
```

### 2. Accept Invitation API

```typescript
// src/app/api/auth/accept-invite/route.ts
export async function POST(request: Request) {
  const { token, password, fullName } = await request.json();

  const serviceClient = createServiceRoleClient();

  // Verify invitation
  const { data: invitation } = await serviceClient
    .from('admin_invitations')
    .select('*')
    .eq('token', token)
    .is('accepted_at', null)
    .gt('expires_at', new Date().toISOString())
    .single();

  if (!invitation) {
    return NextResponse.json({ error: 'Invalid or expired invitation' }, { status: 400 });
  }

  // Create user account
  const { data: authData, error: authError } = await serviceClient.auth.admin.createUser({
    email: invitation.email,
    password,
    email_confirm: true,
    user_metadata: { full_name: fullName }
  });

  if (authError) throw authError;

  // Assign role
  await serviceClient
    .from('user_roles')
    .insert({
      user_id: authData.user.id,
      role_id: invitation.role_id,
      granted_by: invitation.invited_by
    });

  // Mark invitation as accepted
  await serviceClient
    .from('admin_invitations')
    .update({ accepted_at: new Date().toISOString() })
    .eq('id', invitation.id);

  return NextResponse.json({ success: true });
}
```

## User Management (Super Admin)

### Soft Delete Users

```typescript
// Ban user via Supabase Auth (soft delete)
const serviceClient = createServiceRoleClient();

await serviceClient.auth.admin.updateUserById(userId, {
  ban_duration: '87600h', // 10 years
  user_metadata: {
    deleted_at: new Date().toISOString(),
    deleted_by: currentUser.id
  }
});
```

### Restore Users

```typescript
// Unban user to restore
await serviceClient.auth.admin.updateUserById(userId, {
  ban_duration: 'none',
  user_metadata: {
    deleted_at: null,
    deleted_by: null,
    restored_at: new Date().toISOString()
  }
});
```

## Database Functions

```sql
-- Check if user has specific role
CREATE OR REPLACE FUNCTION has_role(user_id UUID, required_role TEXT)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM user_roles
    WHERE user_roles.user_id = $1 AND role_id = $2
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check if user is any admin
CREATE OR REPLACE FUNCTION is_admin(user_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM user_roles ur
    JOIN roles r ON ur.role_id = r.id
    WHERE ur.user_id = $1 AND r.is_admin_role = TRUE
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Get all roles for user
CREATE OR REPLACE FUNCTION get_user_roles(user_id UUID)
RETURNS TEXT[] AS $$
BEGIN
  RETURN ARRAY(
    SELECT role_id FROM user_roles
    WHERE user_roles.user_id = $1
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## Auto-Create Profile Trigger

```sql
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  -- Create profile
  INSERT INTO user_profiles (id, email, full_name)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'full_name', '')
  );

  -- Assign 'customer' role by default
  IF NEW.raw_user_meta_data->>'role' IS NULL THEN
    INSERT INTO user_roles (user_id, role_id)
    VALUES (NEW.id, 'customer');
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();
```
