---
description: Execute a single SaaS/platform build phase with fresh 200k token context (prevents context rot). Runs in forked context for maximum quality. Only for projects with database/auth/payments - not simple sites. Triggers: build phase, execute phase, SaaS phase, platform phase, run phase 2, fresh context build.
context: fork
allowed_tools:
  - Read
  - Write
  - Edit
  - MultiEdit
  - Bash
  - Glob
  - Grep
  - TodoWrite
  - Task
---

# SaaS Phase Builder

**Purpose**: Execute a single build phase with pristine 200k token context. No accumulated garbage from previous work.

**⚠️ ONLY USE FOR ACTUAL SaaS/PLATFORM PROJECTS**
- This skill assumes database, auth, possibly payments
- Do NOT use for static sites, brochure sites, or simple marketing pages
- For simple websites: just build them directly, no phases needed

## How This Works

This skill runs with `context: fork` - meaning:
- Fresh 200k token context window
- Isolated from main conversation
- No context rot from previous phases
- Maximum quality for this phase

## Pre-Execution Checklist

Before starting, verify:
1. **PROJECT.md exists** - Run `/project-discovery` first if not
2. **Phase is defined** - Know exactly what we're building this phase
3. **Dependencies ready** - Previous phases complete

## Phase Execution Pattern

### 1. Read Context
```
Read PROJECT.md for vision and requirements
Read STATE.md for decisions and constraints
Check TodoWrite for current phase tasks
```

### 2. Execute Phase Tasks
Work through each task atomically:
- One feature at a time
- Commit after each completion
- Validate before moving on

### 3. Verification Checkpoint
Before completing phase:
- Run dev server and test functionality
- Check for console errors
- Verify against PROJECT.md requirements
- Get human confirmation

### 4. Update State
- Mark phase complete in TodoWrite
- Update STATE.md with decisions made
- Document any deviations
- Note what's ready for next phase

## Standard SaaS Phases

### Phase 1: Foundation
- Project scaffolding (Next.js, Tailwind, TypeScript)
- Design system / component library
- Layout and navigation structure
- Development environment

### Phase 2: Database & Auth
- Supabase project setup
- Database schema and migrations
- RLS policies
- Authentication flow (signup, login, logout)
- Protected routes

### Phase 3: Core Features
- Primary feature implementation
- API routes
- Data fetching and mutations
- User-specific data handling

### Phase 4: Payments (if applicable)
- Stripe integration
- Subscription tiers
- Checkout flow
- Webhook handling
- Usage limits per tier

### Phase 5: Dashboard & Analytics
- User dashboard
- Usage metrics
- Data visualisation
- Settings/profile pages

### Phase 6: Polish & Deploy
- UI refinements (use frontend persona)
- Landing page
- Error handling
- Loading states
- SEO metadata

### Phase 7: Launch
- Vercel deployment
- Environment variables
- Domain configuration
- Stripe live mode
- Final testing

## Usage

Invoke for specific phase:
```
"Run saas-phase-builder for Phase 2: Database & Auth"
```

Or chain with Task tool:
```
"Use Task tool to run saas-phase-builder for each phase sequentially"
```

## Key Principle

> Each phase gets pristine context. No accumulated garbage. Maximum quality.

This is GSD's methodology without the manual session management - `context: fork` handles it automatically.
