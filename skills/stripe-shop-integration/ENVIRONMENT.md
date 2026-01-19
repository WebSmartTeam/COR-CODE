# Environment Variables Configuration

## Required Environment Variables

Create a `.env` file in your project root:

```bash
# Stripe API Keys - NEVER commit these to git!
# Get from: https://dashboard.stripe.com/apikeys

# Publishable key (starts with pk_) - safe for client-side
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here

# Secret key (starts with sk_) - server-side only
STRIPE_SECRET_KEY=sk_test_your_secret_key_here

# Webhook secret (starts with whsec_) - for webhook signature validation
# Get from: https://dashboard.stripe.com/webhooks
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Supabase (if using for database)
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key_here
```

## Environment Variable Rules

### Client-Side (VITE_ prefix)
- `VITE_STRIPE_PUBLISHABLE_KEY` - Exposed to browser, starts with `pk_`
- `VITE_SUPABASE_URL` - Public URL
- `VITE_SUPABASE_ANON_KEY` - Public key with RLS protection

### Server-Side (no prefix)
- `STRIPE_SECRET_KEY` - **NEVER** expose to client
- `STRIPE_WEBHOOK_SECRET` - **NEVER** expose to client

## Vercel Environment Variables

Add these in Vercel Dashboard → Settings → Environment Variables:

1. `VITE_STRIPE_PUBLISHABLE_KEY` (all environments)
2. `STRIPE_SECRET_KEY` (all environments)
3. `STRIPE_WEBHOOK_SECRET` (production only - different for each environment)

## .gitignore

Ensure these are in your `.gitignore`:

```gitignore
# Environment files
.env
.env.local
.env.*.local
.env.production

# Never commit keys
*.pem
*.key
```

## Test vs Live Keys

| Environment | Publishable Key | Secret Key |
|------------|-----------------|------------|
| Development | `pk_test_...` | `sk_test_...` |
| Production | `pk_live_...` | `sk_live_...` |

**Important**: Always use test keys during development. Live keys process real payments!
