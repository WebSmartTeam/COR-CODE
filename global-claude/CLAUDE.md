# SuperClaude Framework Entry Point
**Claude Code Enhancement System - Global Configuration**

## User Context

**About the User**: Describe your technical level, preferences, and working style here.

Example:
```
- Expert-level / Senior / Mid-level / Junior developer
- Frontend, backend, full-stack, infrastructure focus
- Autonomous execution preferences
- Communication preferences (draft-first for external comms, etc.)
```

**Your Name**: {{YOUR_NAME}}

## UK Standards (Adjust for Your Region)

This framework defaults to UK conventions. Modify for your locale:

- **Language**: UK English (colour, organisation, realise)
- **Date Format**: DD/MM/YYYY
- **Currency**: GBP (£)
- **Deployment Region**: London (lhr1)
- **Time Zone**: GMT/BST

## Global Configuration Structure

### Configuration Locations

**Global Configuration** (Available to ALL projects):
```
~/.claude/
├── settings.json               # Claude Code settings
├── settings.local.json         # Personal overrides
├── agents/                     # Global AI agents
├── commands/                   # Global slash commands
├── hooks/                      # Global automation hooks
├── skills/                     # Global skills
├── context/                    # Global context files
└── CLAUDE.md                   # This file
```

**Project Configuration** (Project-specific):
```
<project-root>/.claude/
├── settings.json               # Project settings (committed)
├── settings.local.json         # Personal overrides (gitignored)
├── agents/                     # Project specialists
├── hooks/                      # Project hooks
├── skills/                     # Project skills
└── .mcp.json                   # Project MCP servers
```

### MCP Server Configuration

**Global MCP Config**: `~/.claude.json`
**Project MCP Config**: `.mcp.json` in project root

**Adding Global MCP Servers**:
```bash
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp
```

**After adding MCP servers, restart Claude Code for changes to take effect.**

## Chrome Browser Integration

To access Chrome tools and browser automation:
```bash
claude --chrome
```

Enables:
- `mcp__claude-in-chrome__*` tools
- Access to open browser tabs
- Visual validation and testing
- Console log reading

## No Localhost Development

**NEVER run `npm run dev` or any local development server unless user explicitly requests it.**

- ❌ Don't ask "shall I start the dev server?"
- ❌ Don't run `npm run dev`, `yarn dev`, `pnpm dev`, `next dev`
- ❌ Don't suggest testing on localhost:3000

**Instead:**
- ✅ Build and deploy to preview/production URLs
- ✅ Test on real deployed URLs
- ✅ Push changes and let CI/CD handle deployment

## Skills Configuration

**Local Skills** (Default - Project-specific):
- Location: `<project-root>/.claude/skills/`
- Committed to git, shared with team

**Global Skills** (User-level):
- Location: `~/.claude/skills/`
- Personal workflows across all projects

## Agents vs Specialists

| Concept | Location | Purpose |
|---------|----------|---------|
| **Agent** | `~/.claude/agents/` | Global domain expertise |
| **Specialist** | `<project>/.claude/agents/` | Project-specific expertise |

## Available Framework Components

### Commands
- `/build` - Project builder with framework detection
- `/analyze` - Multi-dimensional code analysis
- `/implement` - Feature implementation
- `/improve` - Evidence-based enhancement
- `/design` - Design orchestration
- `/document` - Documentation generation
- `/troubleshoot` - Problem investigation

### Agents
- `architect` - Systems design, scalability
- `frontend` - UI/UX, accessibility
- `backend` - APIs, reliability
- `security` - Threat modeling
- `performance` - Optimisation
- `qa` - Testing, quality assurance
- `refactorer` - Code quality
- `scribe` - Documentation
- `mentor` - Educational guidance
- `devops` - Infrastructure, CI/CD
- `analyzer` - Root cause analysis

### MCP Servers
- **Context7** - Library documentation lookup
- **Sequential** - Complex multi-step analysis
- **Magic** - UI component generation
- **Playwright** - Browser automation and testing

## Email Notification Systems (Optional)

If you have AWS SES configured for notifications:

```
~/.claude/email-configs/
└── your-project/
    ├── README.md
    ├── project-email-helper.py
    └── .env  # AWS SES credentials
```

## Git Configuration

**Repository Visibility**: Configure your default (private/public)
**Organisation**: your-github-org

**Commit Message Format**:
```
feat: Add feature description

Developed by Your Organisation
https://your-website.com

Co-Authored-By: Your AI <your-email@example.com>
```

## Deployment Configuration

**Vercel Region**: lhr1 (London) - adjust for your location
**Node.js Version**: 22.x (current LTS)

```json
{
  "regions": ["lhr1"],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ]
}
```

## Core Principles

### No Cost-Based Decisions

**NEVER factor cost or affordability into recommendations.**

- **Assume subscriptions exist** - User likely has paid tiers already
- **Recommend the RIGHT solution** - Not the cheapest or free alternative
- **Never downgrade for budget** - Don't suggest free tiers "to save money"
- **Ignore pricing entirely** - User decides what they can afford
- **Skip cost disclaimers** - No "this has fees" warnings

Wrong: "We could use Supabase free tier to keep costs down..."
Right: "Use Supabase with RLS policies..."

## Security Rules

- Never commit secrets, API keys, or credentials
- Use environment variables for sensitive data
- No public repository creation without explicit permission
- Check for vulnerabilities before deploying

## Project Boundary Rules

- Work within project root and child folders only
- Never navigate to parent directories
- Never access files outside project boundary
- Each project is completely isolated

## Customisation Notes

Replace these placeholders throughout:

| Placeholder | Replace With |
|-------------|--------------|
| `{{YOUR_NAME}}` | Your name |
| `{{USERNAME}}` | Your system username |
| `your-email@example.com` | Your actual email |
| `your-github-org` | Your GitHub organisation |
| `your-website.com` | Your website URL |
| `lhr1` | Your preferred deployment region |

---

**Framework**: COR-CODE by [COR Solutions](https://msp.corsolutions.co.uk)
