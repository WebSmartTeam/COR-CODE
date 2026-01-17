# Global CLAUDE.md

## What Is Global CLAUDE.md?

The global `CLAUDE.md` file lives at `~/.claude/CLAUDE.md` and applies to **every Claude Code session**, regardless of which project you're working in.

Think of it as your personal AI configuration that follows you everywhere.

## Global vs Local CLAUDE.md

| Aspect | Global (`~/.claude/CLAUDE.md`) | Local (`<project>/CLAUDE.md`) |
|--------|--------------------------------|-------------------------------|
| **Location** | `~/.claude/CLAUDE.md` | Project root or `<project>/.claude/` folder |
| **Scope** | All projects, all sessions | Single project only |
| **Purpose** | Personal preferences, standards, tools | Project-specific rules, context, boundaries |
| **Git** | Not in any repo (personal) | Committed to project repo (shared with team) |
| **Examples** | UK English preference, MCP servers, email config | Tech stack, deployment URLs, project boundaries |

## When to Use Which

**Global CLAUDE.md** - Things that apply everywhere:
- Your language preferences (UK English, date formats)
- Your working style (autonomous execution, approval preferences)
- MCP server configuration instructions
- Personal tools and email notification systems
- Security rules you always want enforced

**Local CLAUDE.md** - Things specific to one project:
- Project tech stack and deployment details
- Client-specific requirements
- Project boundaries (what folders Claude can access)
- Team conventions for that codebase
- API endpoints, database details for that project

## Installation

```bash
cp CLAUDE.md ~/.claude/CLAUDE.md
```

Then customise the placeholders:

| Placeholder | Replace With |
|-------------|--------------|
| `{{YOUR_NAME}}` | Your name |
| `{{USERNAME}}` | Your system username |
| `your-email@example.com` | Your actual email |
| `your-github-org` | Your GitHub organisation |

## Regional Settings

The template defaults to UK standards. Adjust for your region:

- **Spelling**: UK (colour) vs US (color)
- **Date Format**: DD/MM/YYYY vs MM/DD/YYYY
- **Deployment Region**: lhr1 (London) vs iad1 (Washington DC)

## Creating a Local CLAUDE.md

For project-specific configuration, create a `CLAUDE.md` in your project root:

```bash
# In your project root
touch CLAUDE.md

# Or in .claude folder
mkdir -p .claude && touch .claude/CLAUDE.md
```

Local files add to (and can override) global settings for that project.

---

Part of COR-CODE v1.0.0 by [COR Solutions](https://msp.corsolutions.co.uk)
