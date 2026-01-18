---
name: feature-dev
description: Implement new features in existing projects using 7-phase workflow (Discovery → Explore → Clarify → Design → Implement → Review → Summary). Use when adding functionality, building new components, creating API endpoints, or extending existing systems. Triggers: new feature, implement, add functionality, build feature, extend, create endpoint, add component.
updated: 2025-01-18
user-invocable: true
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
  - AskUserQuestion
  - mcp__supabase__*
  - mcp__context7__*
  - mcp__sequential-thinking__*
  - mcp__firecrawl__*
  - mcp__magic__*
---

# Feature Development for Existing Projects

**Purpose**: Add new features to established projects using a structured workflow. No tech stack assumptions - reads from CLAUDE.md and existing code.

## Why No `context: fork`

This skill deliberately keeps the main conversation context because:
- You already know the codebase from previous work
- Forking loses that accumulated understanding
- Sub-agents via Task tool can explore and report back
- Main conversation retains decision history

## 7-Phase Workflow

### Phase 1: Discovery
**Goal**: Understand what the user wants to build

- Listen to the feature request
- Identify core requirements vs nice-to-haves
- Note any constraints mentioned (performance, security, but timeline is nonsense,usual developer cost for this work to charge client)
- Tech stack will be discovered in Phase 2 from CLAUDE.md and codebase

**Output**: Clear feature scope statement

### Phase 2: Codebase Exploration
**Goal**: Understand the existing system and its tech stack

**First**: Read CLAUDE.md and discover the project's actual setup:
- Framework (Next.js, Remix, Nuxt, plain React, etc.)
- Database (Supabase, Prisma, Drizzle, raw SQL, etc.)
- Hosting (Vercel, AWS, Netlify, etc.)
- Auth provider (Supabase Auth, NextAuth, Clerk, etc.)
- Styling (Tailwind, CSS modules, styled-components, etc.)

**Then**: Use Task tool sub-agents in parallel to explore relevant areas:
```
Task (Explore): "Find authentication patterns - how does this project handle auth?"
Task (Explore): "Identify database schema - what ORM/client, what tables exist?"
Task (Explore): "Map API routes - REST, tRPC, Server Actions, GraphQL?"
Task (Explore): "Find UI patterns - component library, design tokens, layouts"
```

**Understand**:
- How existing features are structured
- Naming conventions and file organisation
- Error handling patterns
- State management approach

**Output**: Clear picture of project tech stack and patterns to follow

### Phase 3: Clarifying Questions
**Goal**: Fill gaps before designing

Ask only what you genuinely don't know:
- Business logic ambiguities
- Edge cases and error handling preferences
- Integration priorities
- Performance requirements

**Rule**: Don't ask about tech choices already in CLAUDE.md or codebase

**Output**: Complete understanding to design solution

### Phase 4: Architecture Design
**Goal**: Design the implementation approach

Document in TodoWrite:
- Database changes (if any)
- API endpoints needed
- UI components to create/modify
- Integration points with existing code
- Migration strategy (if schema changes)

Consider:
- Follows existing patterns in codebase
- Maintains consistency with current architecture
- Handles errors like existing code does
- Security model matches project standards

**Output**: Clear implementation plan in todos

### Phase 5: Implementation
**Goal**: Build the feature

Execute todos systematically:
1. Database/schema changes first (if any)
2. Backend/API layer
3. Frontend/UI layer
4. Integration and wiring
5. Tests (matching project's test patterns)

**Rules**:
- One logical change at a time
- Commit after each working milestone
- Follow existing code patterns exactly
- Use project's established libraries

### Phase 6: Quality Review
**Goal**: Verify the implementation

Check against:
- Original requirements from Phase 1
- Existing patterns (does it match the codebase style?)
- Error handling (does it follow project conventions?)
- Security (authentication, authorisation, input validation)
- Performance (no obvious N+1 queries, proper caching)

If visual changes, use available tools:
- **Firecrawl**: scrape with screenshot format for quick captures
- **Playwright**: E2E testing and detailed visual regression
- **Chrome tabs**: colour picker, console, network (requires `claude --chrome` session)

**Output**: Verified, working feature

### Phase 7: Summary
**Goal**: Document what was done

Provide:
- What was built (feature summary)
- Files created/modified
- Database changes made
- Any new environment variables needed
- Testing instructions
- Follow-up improvements (if any)

## Usage

Invoke with feature description:
```
/feature-dev Add a user notification system with email and in-app alerts
```

Or naturally:
```
"I need to add a new dashboard section for analytics - can you use the feature-dev workflow?"
```

## Key Principles

1. **Discover, don't assume** - Read CLAUDE.md and explore codebase to understand actual tech stack
2. **Adapt to project** - Use whatever framework, database, styling the project already has
3. **Keep context** - Main conversation remembers everything, sub-agents report back
4. **Follow patterns** - New code should look like it belongs in the existing codebase
5. **Ask smart questions** - Only what you can't determine from existing code
6. **Incremental commits** - Working milestones, not one big commit
