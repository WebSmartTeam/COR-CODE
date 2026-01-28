---
name: skill-building
description: Create effective Claude Code skills and agents. Covers official frontmatter spec, global vs project scope, and the formula - references activate dormant knowledge, pet hates stop bad defaults, post-training fills gaps. Triggers: create skill, build skill, write skill, make agent, skill template, how to write skills.
updated: 2025-01-18
---

# Skill & Agent Building

## Global vs Project Skills

| Scope | Location | Use For |
|-------|----------|---------|
| **Global (User)** | `~/.claude/skills/` | Personal workflows across ALL projects |
| **Project (Local)** | `<project>/.claude/skills/` | Project-specific, committed to git |

**Default**: Create project skills unless explicitly asked for global.

## Official Frontmatter Spec

```yaml
---
name: skill-name
description: What + When + Triggers (for Claude to match requests)
updated: 2025-01-18
allowed-tools:              # NOTE: hyphen, not underscore!
  - Read
  - Write
  - Bash
model: haiku|sonnet|opus    # Optional: override model
context: fork               # Optional: isolated 200k context
user-invocable: true        # Can user call directly?
---
```

**Key fields:**
- `allowed-tools` - Restricts which tools the skill can use (hyphenated!)
- `context: fork` - Runs in isolated subagent with fresh context
- `user-invocable: true` - User can trigger via `/skill-name`
- `model` - Override for specific model needs

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

```yaml
---
name: skill-name
description: What it does + When to use + Triggers (comma-separated keywords)
updated: 2025-01-18
user-invocable: true        # If user can call via /skill-name
allowed-tools:              # Optional: restrict available tools
  - Read
  - Write
  - Bash
---

# Skill Title

[Core principle - 1-2 sentences]

## Preferences
- "We do X, not Y"

## Anti-Patterns
- Things Claude defaults to that we don't want

## Resources
- Where to look for post-training knowledge
```

## Agent Structure

Agents live in `~/.claude/agents/` (global) or `<project>/.claude/agents/` (local).

```yaml
---
name: agent-name
description: When this agent activates + domain expertise
updated: 2025-01-18
allowed-tools:
  - Read
  - Grep
  - Bash
---

# Agent Role

[One sentence identity]

## Focus
- What this agent prioritises

## Approach
- How this agent differs from default Claude

## Boundaries
- What this agent defers to others
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

## Documenting Discoveries

When you discover something worth sharing (installation methods, gotchas, tips), add it to `knowledge/` in COR-CODE:

```bash
COR-CODE/knowledge/
├── README.md                 # Index of all notes
├── installation-methods.md   # Native vs Homebrew vs npm
└── [your-discovery].md       # New findings
```

Knowledge notes are curated research - verified, useful information that helps other Claude instances avoid rediscovering the same things.

## COR-CODE Commits Checklist

**Every time you commit to COR-CODE, you MUST:**

1. **Update CHANGELOG.md** - Add entry under current version or create new version
2. **Update version table** at bottom of CHANGELOG.md
3. **Sync to global** if skill/agent was updated (`cp -r COR-CODE/skills/x ~/.claude/skills/`)

Format:
```markdown
## [1.0.X] - YYYY-MM-DD

### Added/Changed/Removed
- What you added or changed
```
