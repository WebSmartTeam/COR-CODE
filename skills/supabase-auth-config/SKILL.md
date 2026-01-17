# Supabase Auth Configuration

## Trigger
When setting up Supabase authentication, configuring redirect URLs, or handling auth callbacks.

## 🚨 CRITICAL: Redirect URL Configuration

**WRONG** - Adding multiple redirect URLs:
```
https://example.com/auth/callback
https://example.com/auth/reset-password
https://example.com/auth/verify-email
https://example.com/auth/signup-confirm
```

**CORRECT** - Single callback URL handles ALL flows:
```
https://example.com/auth/callback
```

### Why Single Callback?
All auth flows need to exchange the code for a session FIRST. The `/auth/callback` route:
1. Receives the auth code from Supabase
2. Exchanges it for a session
3. THEN routes based on the `type` parameter

Having separate routes is redundant - they'd all need the same code exchange logic.

## Supabase Dashboard Settings

**Authentication → URL Configuration:**
- **Site URL**: `https://yourdomain.com`
- **Redirect URLs**: `https://yourdomain.com/auth/callback`

For local development, add:
- `http://localhost:3000/auth/callback`

## The Callback Route Pattern

```typescript
// app/auth/callback/route.ts (Next.js App Router)
import { createClient } from '@/utils/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url)
  const code = searchParams.get('code')
  const type = searchParams.get('type')
  const next = searchParams.get('next') ?? '/dashboard'

  if (code) {
    const supabase = await createClient()
    const { error } = await supabase.auth.exchangeCodeForSession(code)

    if (!error) {
      // Route based on auth flow type
      switch (type) {
        case 'recovery':
          return NextResponse.redirect(`${origin}/auth/reset-password`)
        case 'signup':
          return NextResponse.redirect(`${origin}/dashboard?welcome=true`)
        case 'email_change':
          return NextResponse.redirect(`${origin}/dashboard/profile?email_updated=true`)
        default:
          // Magic link or other - go to dashboard
          return NextResponse.redirect(`${origin}${next}`)
      }
    }
  }

  // Auth error - redirect to error page
  return NextResponse.redirect(`${origin}/auth/error`)
}
```

## Auth Flow Types

| Type | Trigger | Redirect To |
|------|---------|-------------|
| `recovery` | Password reset email | `/auth/reset-password` |
| `signup` | Email confirmation | `/dashboard?welcome=true` |
| `email_change` | Email change confirmation | `/dashboard/profile?email_updated=true` |
| `magiclink` | Magic link login | `/dashboard` |
| (none) | Regular magic link | `/dashboard` |

## Common Bug: Ignoring Type Parameter

**The bug**: Callback route ignores `type` parameter, sends ALL users to `/dashboard`.

**The problem**: Password reset users never reach `/auth/reset-password` - they can't set their new password!

**The fix**: Always check `type` parameter and route accordingly (see pattern above).

## Reset Password Page

After routing to `/auth/reset-password`, user needs a form to set new password:

```typescript
// app/auth/reset-password/page.tsx
'use client'
import { createClient } from '@/utils/supabase/client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function ResetPasswordPage() {
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const router = useRouter()
  const supabase = createClient()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const { error } = await supabase.auth.updateUser({
      password: password
    })

    if (error) {
      setError(error.message)
    } else {
      router.push('/dashboard?password_updated=true')
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="New password"
        minLength={8}
        required
      />
      {error && <p className="text-red-500">{error}</p>}
      <button type="submit">Update Password</button>
    </form>
  )
}
```

## Email Templates (Supabase Dashboard)

**Authentication → Email Templates**

Ensure redirect URLs use your callback with type:
- **Confirm signup**: `{{ .SiteURL }}/auth/callback?type=signup`
- **Reset password**: `{{ .SiteURL }}/auth/callback?type=recovery`
- **Magic link**: `{{ .SiteURL }}/auth/callback`
- **Change email**: `{{ .SiteURL }}/auth/callback?type=email_change`

## Checklist

- [ ] Single redirect URL in Supabase dashboard: `/auth/callback`
- [ ] Callback route handles `type` parameter
- [ ] Recovery type routes to reset password page
- [ ] Reset password page exists with form
- [ ] Email templates use correct type parameters
- [ ] Local dev URL added if needed
