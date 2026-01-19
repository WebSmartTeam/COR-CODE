# Project Setup & Discovery

**CRITICAL: Never assume infrastructure exists. Always ask the user first.**

## 🚨 MANDATORY: Project Discovery Before ANY Code

Before writing a single line of code, you MUST complete this discovery process with the user.

### Step 1: Supabase Discovery

**ASK THE USER:**
```
Do you have an existing Supabase project for this shop, or should we create a new one?

1. I have an existing Supabase project (provide URL and project ID)
2. I need to create a new Supabase project
3. I'm not sure
```

**If existing project:**
- Get the project URL (e.g., `https://xxxxx.supabase.co`)
- Get the project ID (the `xxxxx` part)
- Get the anon key from Project Settings > API
- Verify they have admin access to run migrations

**If new project needed:**
- Guide user to create at https://supabase.com/dashboard
- Wait for them to provide the URL and project ID
- DO NOT proceed until you have real credentials

### Step 2: Git Repository Discovery

**ASK THE USER:**
```
Do you have a Git repository set up for this project?

1. Yes, I have a GitHub repo (provide URL)
2. Yes, I have a different Git provider (provide details)
3. No, I need to create one
4. I don't want version control
```

**If GitHub exists:**
- Verify the repo URL
- Check if it's the correct organisation/account
- Confirm push access

**If needs creating:**
- Confirm which GitHub account/organisation
- Confirm repository name
- Create with: `gh repo create [org]/[name] --private --source=. --remote=origin --push`

### Step 3: Vercel Discovery

**ASK THE USER:**
```
Do you have a Vercel project for deployment?

1. Yes, I have an existing Vercel project (provide project name/URL)
2. No, but I have a Vercel account (I'll link it)
3. No Vercel account yet
4. I want to deploy elsewhere
```

**If Vercel exists:**
- Get project name
- Verify London (lhr1) region is set
- Check environment variables are configured

**If needs creating:**
- Guide through Vercel project creation
- ALWAYS set region to London (lhr1)
- Wait for confirmation before proceeding

### Step 4: Stripe Discovery

**ASK THE USER:**
```
Do you have Stripe set up for payments?

1. Yes, I have Stripe keys (test and/or live)
2. No, I need to set up Stripe
3. I don't need payments yet
```

**If Stripe exists:**
- Get publishable key and secret key
- Confirm if test or live mode
- Get webhook secret if available

## 📝 Recording in CLAUDE.md

**MANDATORY: After discovery, add this section to the project's CLAUDE.md:**

```markdown
## Project Configuration

### Supabase
| Key | Value |
|-----|-------|
| **Project URL** | https://[PROJECT_ID].supabase.co |
| **Project ID** | [PROJECT_ID] |
| **Region** | [REGION] |

### GitHub
| Key | Value |
|-----|-------|
| **Repository** | [ORG]/[REPO_NAME] |
| **URL** | https://github.com/[ORG]/[REPO_NAME] |
| **Branch** | main |

### Vercel
| Key | Value |
|-----|-------|
| **Project** | [PROJECT_NAME] |
| **Team** | [TEAM_NAME] |
| **Region** | London (lhr1) |
| **URL** | https://[PROJECT].vercel.app |

### Stripe
| Key | Value |
|-----|-------|
| **Mode** | Test / Live |
| **Account** | [ACCOUNT_ID] |
```

## 🔌 Supabase MCP Configuration

**CRITICAL: Supabase MCP must be project-specific, not global.**

### Why Project-Specific?
- Each shop has its own Supabase project
- Global MCP would connect to wrong database
- Security: isolate projects from each other
- Prevents accidental data access across projects

### Setting Up Supabase MCP

**Step 1: Create project-scoped .mcp.json**

Create `.mcp.json` in the project root (NOT global):

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server-supabase@latest",
        "--supabase-url",
        "https://[PROJECT_ID].supabase.co",
        "--supabase-service-role-key",
        "[SERVICE_ROLE_KEY]"
      ]
    }
  }
}
```

**Step 2: Get the service role key**
1. Go to Supabase Dashboard > Project Settings > API
2. Copy the `service_role` key (NOT the anon key)
3. This key bypasses RLS - use only for admin operations

**Step 3: Restart Claude Code**
After creating `.mcp.json`, exit and resume Claude Code for the MCP to load.

### Security Considerations

```markdown
⚠️ NEVER commit .mcp.json with real keys to git!

Add to .gitignore:
```
.mcp.json
```

For team sharing, use environment variables:
```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server-supabase@latest",
        "--supabase-url",
        "${SUPABASE_URL}",
        "--supabase-service-role-key",
        "${SUPABASE_SERVICE_ROLE_KEY}"
      ]
    }
  }
}
```

## 🌍 Environment Variables

### Required Variables

Create `.env.local` (gitignored):

```bash
# Supabase (PUBLIC - safe for client)
NEXT_PUBLIC_SUPABASE_URL=https://[PROJECT_ID].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=[ANON_KEY]

# Supabase (PRIVATE - server only)
SUPABASE_SERVICE_ROLE_KEY=[SERVICE_ROLE_KEY]

# Stripe (PUBLIC - safe for client)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...

# Stripe (PRIVATE - server only)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Site URL (for callbacks)
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

### Vercel Environment Variables

Set these in Vercel Dashboard > Project > Settings > Environment Variables:

| Variable | Environment | Notes |
|----------|-------------|-------|
| `NEXT_PUBLIC_SUPABASE_URL` | All | Public, safe |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | All | Public, safe |
| `SUPABASE_SERVICE_ROLE_KEY` | Production, Preview | Server only |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | All | Public, safe |
| `STRIPE_SECRET_KEY` | Production, Preview | Server only |
| `STRIPE_WEBHOOK_SECRET` | Production | Webhook verification |
| `NEXT_PUBLIC_SITE_URL` | Production | Your domain |

### Environment Variable Verification

Before proceeding with development, verify all variables are set:

```typescript
// src/lib/env.ts
const requiredEnvVars = [
  'NEXT_PUBLIC_SUPABASE_URL',
  'NEXT_PUBLIC_SUPABASE_ANON_KEY',
] as const;

const requiredServerEnvVars = [
  'SUPABASE_SERVICE_ROLE_KEY',
  'STRIPE_SECRET_KEY',
] as const;

export function validateEnv() {
  const missing: string[] = [];

  for (const key of requiredEnvVars) {
    if (!process.env[key]) {
      missing.push(key);
    }
  }

  if (typeof window === 'undefined') {
    for (const key of requiredServerEnvVars) {
      if (!process.env[key]) {
        missing.push(key);
      }
    }
  }

  if (missing.length > 0) {
    throw new Error(`Missing environment variables: ${missing.join(', ')}`);
  }
}
```

## 📋 Setup Checklist

Before writing any component code, verify:

```markdown
## Pre-Development Checklist

### Infrastructure Discovery
- [ ] Asked user about Supabase project
- [ ] Asked user about Git repository
- [ ] Asked user about Vercel project
- [ ] Asked user about Stripe setup
- [ ] Recorded all IDs in CLAUDE.md

### Supabase Setup
- [ ] Project exists or created
- [ ] Project ID recorded
- [ ] Anon key obtained
- [ ] Service role key obtained (for MCP)
- [ ] .mcp.json created with project-specific config
- [ ] .mcp.json added to .gitignore
- [ ] Claude Code restarted to load MCP

### Environment Variables
- [ ] .env.local created with all required vars
- [ ] .env.local added to .gitignore
- [ ] Vercel env vars configured (for deployment)

### Git Setup
- [ ] Repository exists or created
- [ ] Remote configured
- [ ] Initial commit made
- [ ] .gitignore includes sensitive files

### Vercel Setup
- [ ] Project exists or created
- [ ] Region set to London (lhr1)
- [ ] Connected to Git repository
- [ ] Environment variables configured
```

## 🚫 Anti-Patterns

### NEVER Do This:

```typescript
// ❌ WRONG - Hardcoded project ID
const supabaseUrl = 'https://abcdefghijklmnop.supabase.co';

// ❌ WRONG - Assuming project exists
// Just start coding without asking user

// ❌ WRONG - Global MCP for project-specific database
// ~/.claude.json with Supabase MCP

// ❌ WRONG - Committing keys
// .mcp.json with real service role key in git
```

### ALWAYS Do This:

```typescript
// ✅ CORRECT - Environment variable
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;

// ✅ CORRECT - Ask user first
// "Do you have a Supabase project set up?"

// ✅ CORRECT - Project-scoped MCP
// .mcp.json in project root, gitignored

// ✅ CORRECT - Document in CLAUDE.md
// Record project ID after user confirms
```

## 🔄 Database Migration Order

After Supabase is set up, run migrations in this order:

1. **Core Tables** (DATABASE.md)
   - products, categories, page_content, site_settings, navigation

2. **Auth & RBAC** (AUTH.md)
   - roles, user_roles, role_permissions

3. **Shop Tables** (SHOP.md)
   - orders, order_items, cart (if server-side)

4. **CMS Seed Data** (CMS.md)
   - Initial page_content, site_settings, navigation

5. **RLS Policies** (AUTH.md)
   - Apply after tables exist

### Verification After Migrations

```sql
-- Check all tables exist
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';

-- Check RLS is enabled
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';

-- Verify initial data
SELECT COUNT(*) FROM site_settings;
SELECT COUNT(*) FROM navigation;
```

## 🎯 First Development Steps

After setup is complete:

1. **Verify Connection**
   ```typescript
   // Quick test in a page
   const { data } = await supabase.from('site_settings').select('*');
   console.log('Connection test:', data);
   ```

2. **Seed CMS Data**
   - Run CMS.md seed queries
   - Verify content loads

3. **Build Header/Footer**
   - Navigation from database
   - No hardcoded links

4. **Build Homepage**
   - Hero from page_content
   - Products from products table

5. **Continue with other pages**
   - All content from CMS
   - Zero hardcoding
