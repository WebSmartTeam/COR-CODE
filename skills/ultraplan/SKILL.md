---
name: ultraplan
description: Deep architectural planning with --ultrathink (32K tokens) followed by phased execution with fresh context. Two-stage workflow - UltraPlan creates comprehensive PHASES.md, then Execute runs each phase with pristine 200K context. Use for any complex build requiring multiple phases. Triggers: ultraplan, plan phases, phase planning, architect plan, deep plan, strategic plan.
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

# UltraPlan & Execute

**Purpose**: Two-stage workflow for complex builds - deep planning with maximum thinking, then clean execution with pristine context per phase.

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

### Stage 2: Execute (Clean Context)
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

### Step 2: Execute Phases
```
"Execute Phase 1" or "Run ultraplan phase 2"
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

## Project Type Templates

### SaaS Platform
1. Foundation (scaffolding, design system)
2. Database & Auth (Supabase, RLS, auth flow)
3. Core Features (primary functionality)
4. Payments (Stripe, subscriptions)
5. Dashboard (user area, analytics)
6. Polish (UI refinements, error handling)
7. Launch (deploy, go live)

### E-commerce
1. Foundation (Next.js, design system)
2. Database & Products (catalogue, inventory)
3. Cart & Checkout (Stripe, order flow)
4. User Accounts (auth, order history)
5. Admin Panel (management interface)
6. Polish & SEO
7. Launch

### Multi-tenant Platform
1. Foundation (architecture for tenancy)
2. Tenant Management (onboarding, isolation)
3. Core Features (shared functionality)
4. Tenant Customisation (branding, settings)
5. Billing (per-tenant payments)
6. Admin & Monitoring
7. Launch

### API/Backend Service
1. Foundation (framework, structure)
2. Database & Models (schema, migrations)
3. API Endpoints (routes, validation)
4. Auth & Security (JWT, rate limiting)
5. Documentation (OpenAPI, examples)
6. Testing & Monitoring
7. Deploy

## Key Principles

> **Plan deep, execute clean.**

- --ultrathink ensures nothing is missed
- Forked context ensures maximum quality
- PHASES.md is the single source of truth
- Each phase is independently verifiable

## When NOT to Use

- Simple websites (just build them directly)
- Single-page apps with no backend
- Quick prototypes or experiments
- Projects under ~4 hours of work

Use ultraplan for projects that genuinely need architectural thinking and phased execution.
