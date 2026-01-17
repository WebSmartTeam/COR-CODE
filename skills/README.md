# Skills

Skills teach Claude specific capabilities. Claude auto-discovers and applies them when your request matches their description.

## Global vs Local Skills

| Aspect | Global (`~/.claude/skills/`) | Local (`<project>/.claude/skills/`) |
|--------|------------------------------|-------------------------------------|
| **Scope** | All projects, all sessions | Single project only |
| **Purpose** | Personal workflows used everywhere | Project-specific automation |
| **Git** | Not in any repo (personal) | Committed to project repo (shared with team) |
| **Examples** | Deployment skills, email notifications | Project build scripts, client-specific workflows |

**Installation:**
```bash
# Global (personal, all projects)
cp -r skills/* ~/.claude/skills/

# Local (one project only)
cp -r skills/* <project>/.claude/skills/
```

## Structure

```
skills/
├── skill-name/
│   ├── SKILL.md          # Required
│   ├── reference.md      # Optional - loaded when needed
│   └── scripts/          # Optional - executed, not loaded
```

## SKILL.md Format

```yaml
---
name: skill-name
description: What it does and when to use it. Include trigger keywords.
allowed-tools: Read, Grep, Glob  # Optional - restrict tools
---

Instructions for Claude in Markdown.
```

## Metadata Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase, hyphens, max 64 chars. Match folder name. |
| `description` | Yes | What + when. Max 1024 chars. Claude uses this to decide activation. |
| `allowed-tools` | No | Comma-separated list of permitted tools. |
| `model` | No | Override model for this skill. |
| `context` | No | `fork` to run in isolated subagent. |
| `user-invocable` | No | `false` hides from `/` menu. |

## Locations

| Path | Scope |
|------|-------|
| `~/.claude/skills/` | Personal - all your projects |
| `.claude/skills/` | Project - this repo only |

## Writing Effective Skills

**The Formula:**
1. **References** - "Use X" activates dormant knowledge
2. **Pet hates** - "Never do Y" stops bad defaults
3. **Post-training** - "Look here for Z" fills genuine gaps

**Don't teach Claude what Claude knows.** Keep under 500 lines.

## Tips

- Description is everything - include trigger keywords
- Scripts execute without loading into context
- Use `allowed-tools` for read-only skills
- Supporting files use progressive disclosure

## Docs

https://code.claude.com/docs/en/skills
