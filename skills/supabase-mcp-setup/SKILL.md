---
name: supabase-mcp-setup
description: Configure Supabase MCP server for a specific project using local .mcp.json (NOT global). Each project needs its own config to prevent wrong-database queries. Triggers: setup supabase mcp, install supabase mcp, configure supabase mcp, connect supabase, supabase database access, mcp not loading supabase.
---

# Supabase MCP Local Project Configuration

## Why Local (Not Global)
- Each project has its own Supabase database
- Prevents accidentally running queries on wrong database
- Project ref scopes access to specific project

## Setup Steps

### 1. Add token to project .env.local

Copy `SUPABASE_ACCESS_TOKEN` from `~/.env.local` to your project `.env.local`, or get a new token from https://supabase.com/dashboard/account/tokens

### 2. Create .mcp.json in project root

```json
{
  "mcpServers": {
    "supabase": {
      "type": "http",
      "url": "https://mcp.supabase.com/mcp?project_ref=YOUR_PROJECT_REF",
      "headers": {
        "Authorization": "Bearer ${SUPABASE_ACCESS_TOKEN}"
      }
    }
  }
}
```

### 3. Get your Project Ref from user

**Project Ref (YOUR_PROJECT_REF):**
- Go to Supabase Dashboard → Your Project → Settings → General
- Copy the "Reference ID" (e.g., `xyzexampleref12345678`)
- Replace `YOUR_PROJECT_REF` in the URL above

### 4. Restart Claude Code

After creating/editing .mcp.json, you must:
- Type `exit` in Claude Code
- Run `claude` again (or `claude --resume` to continue conversation)

### 5. Verify it works

Ask Claude to run:
```
mcp__supabase__list_tables
```

If configured correctly, it will return your database tables.


## Troubleshooting

**MCP not loading:**
- Check .mcp.json is in project root
- Verify JSON syntax is valid
- Restart Claude Code (exit + claude)

**Authentication error:**
- Check project .env.local has SUPABASE_ACCESS_TOKEN
- Token must start with `sbp_`

**Wrong database:**
- Verify project_ref matches your project's Reference ID
