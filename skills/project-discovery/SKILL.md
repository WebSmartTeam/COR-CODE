---
description: Guided project discovery before implementation - understand what you're building
context: fork
allowed_tools:
  - Read
  - Write
  - WebSearch
  - TodoWrite
---

# Project Discovery Skill

**Purpose**: Guide through understanding what we're building BEFORE writing code. Creates PROJECT.md with full requirements.

## Discovery Framework

### Phase 1: Vision & Problem
- What problem does this solve?
- Who experiences this problem?
- Why does this matter to them?
- What happens if we don't solve it?

### Phase 2: Users & Context
- Who are the primary users?
- What's their technical level?
- How will they access this (web, mobile, desktop)?
- What's their workflow/journey?

### Phase 3: Core Features (Must-Haves)
- What are the 3-5 essential features?
- What's the MVP (Minimum Viable Product)?
- What can wait for v2?
- What's explicitly OUT of scope?

### Phase 4: Technical Decisions

**Stack baseline** (always, not a choice):
- Next.js + React + TypeScript
- Tailwind CSS
- Vercel (London lhr1)

**THE KEY QUESTION: Does this project need a database?**

**NO DATABASE** → Simple build
- Just Next.js + Vercel
- Contact forms via edge function or Formspree
- No auth needed (public site)
- Examples: marketing sites, portfolios, brochures, landing pages

**YES DATABASE** → Full build (DB + Auth always go together)
- Supabase (PostgreSQL) - Pete's preference
- Supabase Auth with proper commercial implementation
- RLS policies, proper security
- Examples: platforms, dashboards, apps with user data

**Payments**: Only if actually charging money
- Stripe when needed

### Phase 5: Constraints & Requirements
- Budget constraints?
- Timeline expectations?
- Existing systems to integrate with?
- Compliance requirements (GDPR, etc.)?
- Performance requirements?

### Phase 6: Success Criteria
- How do we know this is working?
- What metrics matter?
- What does "done" look like for MVP?

## Output: PROJECT.md

Create `PROJECT.md` in project root with:

```markdown
# [Project Name]

## Vision
[One paragraph summary of what this is and why it matters]

## Problem Statement
[The specific problem being solved]

## Target Users
[Who uses this and their characteristics]

## Core Features (MVP)
1. [Feature 1] - [Brief description]
2. [Feature 2] - [Brief description]
3. [Feature 3] - [Brief description]

## Out of Scope (v1)
- [Thing we're NOT building yet]
- [Another thing for later]

## Technical Stack
- **Frontend**: [Choice] - [Reason]
- **Backend**: [Choice] - [Reason]
- **Database**: [Choice] - [Reason]
- **Auth**: [Choice] - [Reason]
- **Hosting**: [Choice] - [Reason]
- **Payments**: [Choice if applicable] - [Reason]

## Key Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [Decision 1] | [Choice] | [Why] |

## Constraints
- [Budget/timeline/technical constraints]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Phase Roadmap
### Phase 1: Foundation
- [What we build first]

### Phase 2: Core Features
- [Main functionality]

### Phase 3: Polish & Launch
- [Final touches]
```

## Workflow

1. **Ask questions conversationally** - Don't interrogate, have a dialogue
2. **Explain technical concepts** - User may not know what "database" means
3. **Make recommendations** - Suggest sensible defaults for their use case
4. **Challenge assumptions** - "Do you really need X for MVP?"
5. **Document decisions** - Write PROJECT.md as we go
6. **Confirm understanding** - Summarise back before finalising

## Key Philosophy

> "You aren't a coder and you probably never will be. But you still need to view yourself as a software engineer, as an app architect. You need to understand the fundamentals."

This skill helps users understand WHAT they're building and WHY, so implementation has clear direction.
