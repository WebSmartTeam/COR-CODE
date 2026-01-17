# Global Context Files

This folder contains template context files for your global Claude Code configuration.

## Installation

Copy to your global Claude config:

```bash
cp CLAUDE.md ~/.claude/CLAUDE.md
```

## Configuration

After copying, customise the placeholders:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{YOUR_NAME}}` | Your name | John Smith |
| `{{USERNAME}}` | System username | johnsmith |
| `your-email@example.com` | Your email | john@example.com |
| `your-github-org` | GitHub organisation | my-company |
| `your-website.com` | Your website | example.com |

## Regional Settings

The template defaults to UK standards. Adjust for your region:

**UK (Default)**:
- Spelling: colour, organisation, realise
- Date: DD/MM/YYYY
- Region: lhr1 (London)

**US**:
- Spelling: color, organization, realize
- Date: MM/DD/YYYY
- Region: iad1 (Washington DC)

**EU**:
- Region: cdg1 (Paris) or fra1 (Frankfurt)

## What This File Does

The global `CLAUDE.md` provides:

1. **User Context** - Your preferences and working style
2. **Framework Structure** - Where config files live
3. **Available Commands** - What SuperClaude commands exist
4. **Agent List** - Domain specialist agents
5. **Security Rules** - Standard security practices
6. **Project Boundaries** - Isolation rules

## Extending

Add your own sections for:

- Team-specific workflows
- Project naming conventions
- Deployment checklists
- Code review standards

## Version

This template is part of COR-CODE v1.0.0
