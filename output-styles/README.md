# Output Styles

Output styles modify Claude Code's system prompt to change how it behaves fundamentally.

## How Output Styles Differ from Other Features

| Feature | What It Does | Effect |
|---------|--------------|--------|
| **Output Styles** | *Replaces* parts of system prompt | Fundamental behaviour change |
| **CLAUDE.md** | *Adds* content after system prompt | Additional context and rules |
| **Agents** | Run in separate context | Isolated task handling |
| **Skills** | Add knowledge to conversation | Guidance and patterns |

Think of it this way:
- **Output Styles** = "stored system prompts" (how Claude thinks)
- **Slash Commands** = "stored prompts" (what you ask Claude)

## Built-in Output Styles

| Style | Description |
|-------|-------------|
| **Default** | Standard software engineering mode |
| **Explanatory** | Adds educational "Insights" while coding |
| **Learning** | Collaborative mode with `TODO(human)` markers for you to implement |

## Global vs Local Output Styles

| Location | Scope |
|----------|-------|
| `~/.claude/output-styles/` | All projects (personal) |
| `.claude/output-styles/` | Single project (shared with team) |

## Installation

```bash
# Global (personal, all projects)
cp -r output-styles/* ~/.claude/output-styles/

# Local (one project only)
cp -r output-styles/* <project>/.claude/output-styles/
```

## Creating Output Styles

Output styles are Markdown files with YAML frontmatter:

```yaml
---
name: My Custom Style
description: A brief description displayed in the UI
keep-coding-instructions: false
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with [specific purpose].

## Specific Behaviours

[Define how Claude should behave in this style...]
```

### Frontmatter Fields

| Field | Purpose | Default |
|-------|---------|---------|
| `name` | Display name | Inherits from filename |
| `description` | Shown in `/output-style` menu | None |
| `keep-coding-instructions` | Keep software engineering instructions | false |

## Changing Output Style

```bash
# Interactive menu
/output-style

# Direct switch
/output-style explanatory
/output-style uk-professional
```

Changes are saved in `.claude/settings.local.json` at project level.

## When to Use Output Styles

**Use output styles when:**
- You want to fundamentally change how Claude operates
- You're using Claude for non-coding tasks
- You need consistent behaviour across entire sessions

**Use CLAUDE.md when:**
- You want to add rules without changing core behaviour
- You need project-specific context
- You want to keep coding capabilities intact

## Docs

https://code.claude.com/docs/en/output-styles

---

Part of COR-CODE v1.0.0
