---
name: ultraplan
description: Deep architectural planning with --ultrathink (32K tokens) followed by phased creation with fresh context. Two-stage workflow - UltraPlan creates comprehensive PHASES.md, then Create builds each phase with pristine 200K context. Use for any complex build requiring multiple phases. Use phase-checkpoint skill between phases for human verification. Delegates to architect/frontend/backend agents during execution. Triggers: ultraplan, plan and create, plan phases, deep plan, strategic plan, architect plan.
updated: 2025-01-23
context: fork
allowed-tools:
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

# UltraPlan & Create

**Purpose**: Two-stage workflow for complex builds - deep planning with maximum thinking, then clean creation with pristine context per phase.

## The Problem This Solves

Complex projects fail because:
1. **Shallow planning** → Missed requirements surface mid-build
2. **Context rot** → Quality degrades as conversation grows
3. **No structure** → Ad-hoc decisions without architectural thinking

## The UltraPlan Solution

### Stage 1: UltraPlan (Deep Thinking)
```
--ultrathink (32K tokens of analysis)
```
- Comprehensive requirement analysis
- Architecture decisions BEFORE code
- Phase breakdown with clear boundaries
- Risk identification upfront
- Output: **PHASES.md** - the complete build plan

### Stage 2: Create (Clean Context)
```
context: fork (fresh 200K per phase)
```
- Each phase runs with pristine context
- No accumulated garbage from previous work
- Maximum quality per phase
- Follows PHASES.md exactly

## Usage

### Step 1: Create the Plan
```
"UltraPlan this project" or "Create phases for [project description]"
```

This triggers --ultrathink analysis and produces PHASES.md with:
- Project overview and goals
- Technical architecture decisions
- Phase-by-phase breakdown
- Dependencies and risks
- Success criteria per phase

### Step 2: Create Phases
```
"Create Phase 1" or "Run ultraplan phase 2"
```

Each execution:
1. Reads PHASES.md for context
2. Runs with forked 200K context
3. Completes phase tasks
4. Updates STATE.md with decisions
5. Verifies before marking complete

## PHASES.md Template

```markdown
# [Project Name] - UltraPlan

## Overview
[What we're building and why]

## Architecture Decisions
- Framework: [choice and rationale]
- Database: [choice and rationale]
- Auth: [choice and rationale]
- Hosting: [choice and rationale]

## Phase Breakdown

### Phase 1: Foundation
**Goal**: [Clear objective]
**Delivers**: [Concrete outputs]
**Tasks**:
- [ ] Task 1
- [ ] Task 2
**Verification**: [How we know it's done]
**Estimated effort**: [Simple/Medium/Complex]

### Phase 2: [Name]
[Same structure...]

## Dependencies
- Phase 2 requires Phase 1 complete
- Phase 4 requires Stripe account setup

## Risks
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

## Success Criteria
[How we know the project is complete]
```

## When to Use UltraPlan

**Use for anything that:**
- Needs a database
- Has user authentication
- Requires multiple distinct features
- Would take more than a day to build properly
- Benefits from architectural decisions upfront

**Example project types** (not exhaustive):
- SaaS platforms
- E-commerce shops
- Booking/scheduling systems
- Membership sites
- Client portals
- Multi-tenant platforms
- API services
- Admin dashboards
- CMS-driven sites

**Common phase pattern** (adapt to your project):
1. Foundation (scaffolding, design system)
2. Database & Auth (schema, RLS, auth flow)
3. Core Features (primary functionality)
4. Secondary Features (nice-to-haves)
5. Polish (UI refinements, error handling)
6. Launch (deploy, go live)

Add or remove phases based on what the project actually needs. Payments? Add a payments phase. Admin panel? Add that. Keep it specific to the build.

## Key Principles

> **Plan deep, create clean.**

- --ultrathink ensures nothing is missed
- Forked context ensures maximum quality
- PHASES.md is the single source of truth
- Each phase is independently verifiable

## ⚠️ CRITICAL: No Cost-Based Decisions

**NEVER factor cost or affordability into recommendations.**

When planning, you must:
- **Assume subscriptions exist** - User likely has Vercel Pro, Supabase Pro, Stripe, etc.
- **Recommend the RIGHT solution** - Not the cheapest or free alternative
- **Never downgrade for budget** - Don't suggest free tiers "to save money"
- **Ignore pricing entirely** - It's not your concern; user handles that
- **Skip the cost disclaimers** - No "this has fees" or "paid feature" warnings

**Wrong approach:**
> "We could use Supabase free tier to keep costs down..."
> "Stripe has transaction fees, so consider alternatives..."
> "Vercel hobby plan should be sufficient..."

**Right approach:**
> "Use Supabase with RLS policies..."
> "Stripe for payments with webhooks..."
> "Deploy to Vercel with proper configuration..."

The user decides what they can afford. Your job is to recommend what's technically correct.

## When NOT to Use

- Simple websites (just build them directly)
- Single-page apps with no backend
- Quick prototypes or experiments
- Projects under ~4 hours of work

Use ultraplan for projects that genuinely need architectural thinking and phased execution.

## 🔗 Workflow Integration

```
project-discovery (if requirements unclear)
        ↓
    ultraplan → PHASES.md
        ↓
    For each phase:
      Create Phase N → phase-checkpoint → Next
        ↓
    Project complete
```

**Related**: `phase-checkpoint` (between phases), `architect`/`frontend`/`backend` agents (during execution), `non-stop` skill (autonomous mode).
