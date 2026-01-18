---
name: skill-building
description: Create effective Claude Code skills and agents. Covers the formula - references activate dormant knowledge, pet hates stop bad defaults, post-training fills gaps. Don't teach Claude what Claude knows. Triggers: create skill, build skill, write skill, make agent, skill template, agent template, how to write skills.
updated: 2025-01-18
---

# Skill & Agent Building

## The Core Principle

> "its funny ..you didnt realise that if you knew it without research so would any other claude so why stipulate when you can speculate ..i mean ..claude code is you and is it ...so seriously if its in your training data then skills dont need anything but a reference ..where as if you didnt know it without research then it needs the update of info or where to look"

**Translation**: Claude is Claude. If you know it, every Claude knows it. Don't teach Claude what Claude already knows.

**But**: Knowing something exists and remembering to use it are different. A reference triggers recall - "use modern CSS" reminds Claude to reach for container queries instead of defaulting to media queries. The reference activates knowledge that might otherwise stay dormant.

**The Formula**:
1. **References** - "Use X" activates dormant knowledge
2. **Pet hates** - "Never do Y" stops Claude's bad defaults
3. **Post-training** - "Look here for Z" fills genuine gaps

Pet hates are critical. Claude has default tendencies (AI slop, template patterns, over-engineering) that need explicit blocking. You can't assume Claude won't do something annoying - call it out.

## What Skills Should Contain

### ✅ Include

- **Preferences** - "We prefer X over Y" (nudges behaviour)
- **Project-specific patterns** - Custom scales, naming conventions, file structures
- **Anti-patterns** - Things to avoid that Claude might default to
- **External resources** - Where to look for post-training knowledge
- **Decisions already made** - Tech stack choices, architectural decisions
- **Context Claude can't infer** - Client requirements, business rules, user preferences

### ❌ Don't Include

- **Tutorials** - Claude knows how container queries work
- **Syntax examples** - Claude knows the syntax
- **Concept explanations** - Claude knows what `:has()` does
- **Standard best practices** - Claude knows about accessibility, security, performance

## The Test

Before adding content to a skill, ask:

1. **"Would Claude know this without the skill?"**
   - Yes → Reference only (or omit entirely)
   - No → Include the detail

2. **"Is this a preference or a fact?"**
   - Preference → Include (Claude can't guess your preferences)
   - Fact → Omit (Claude knows facts)

3. **"Is this post-training data?"**
   - Yes → Include or point to Context7/docs
   - No → Reference at most

## Examples

### ❌ Bad (Teaching Claude what it knows)
```markdown
## Container Queries
Container queries allow you to style elements based on their
container's size rather than the viewport. Use @container to
define a containment context, then use @container queries to
apply styles based on the container's dimensions.

Example:
.card-container { container-type: inline-size; }
@container (min-width: 400px) { .card { display: grid; } }
```

### ✅ Good (Preference + reference)
```markdown
## Modern CSS
Prefer native CSS over JavaScript workarounds. Use container
queries, :has(), clamp(), subgrid, text-wrap: balance.

For post-training syntax, check Context7 or web.dev/blog.
```

### ❌ Bad (Explaining the obvious)
```markdown
## Git Commits
Git commits should have a clear message explaining what changed.
Use imperative mood ("Add feature" not "Added feature").
Keep the subject line under 50 characters.
```

### ✅ Good (Project-specific preference)
```markdown
## Git Commits
Include "Co-Authored-By: COR Solutions AI <enquiries@corsolutions.co.uk>"
Never use Anthropic branding in commits.
```

## Skill Structure

```markdown
---
name: skill-name
description: One line explaining when this activates
updated: 2025-01-18
---

# Skill Title

[Core principle or key decision - 1-2 sentences max]

## Preferences
- Bullet points of "we do X, not Y"

## Anti-Patterns
- Things to avoid that Claude might default to

## Resources
- Where to look for things not in training data
```

## Agent Structure

Agents are skills with a persona. Same rules apply - don't teach, guide.

```markdown
---
name: agent-name
description: When this agent activates
updated: 2025-01-18
tools: [Tool1, Tool2]
---

# Agent Role

[One sentence identity]

## Focus
- What this agent prioritises

## Approach
- How this agent thinks differently from default Claude

## Boundaries
- What this agent defers to other agents
```

## Signs You're Over-Documenting

- Skill file is over 100 lines
- You're explaining concepts rather than stating preferences
- You're writing "how to" instead of "we prefer"
- Content could apply to any project (not project-specific)
- You're duplicating official documentation

## The Goal

Skills and agents should be **thin wrappers** around Claude's existing knowledge that:
1. Nudge behaviour in preferred directions
2. Provide context Claude can't infer
3. Point to resources for unknowns

They're configuration, not education.
