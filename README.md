# COR-CODE

**Claude Code Enhancement Framework** - Production-ready skills, agents, and hooks for Claude Code.

Developed by [COR Solutions](https://msp.corsolutions.co.uk) - Professional AI-enhanced development tools.

## What's Included

| Folder | Contents |
|--------|----------|
| `global-claude/` | Global CLAUDE.md template and documentation |
| `skills/` | User-invocable skills for common workflows |
| `agents/` | Specialist personas for domain expertise |
| `hooks/` | Automation hooks for quality gates |
| `output-styles/` | Custom output styles for behaviour modification |

## Understanding the Components

| Component | What It Does | Scope |
|-----------|--------------|-------|
| **Output Styles** | *Replaces* Claude's system prompt | Fundamental behaviour change |
| **CLAUDE.md** | *Adds* context after system prompt | Project rules and standards |
| **Skills** | Add knowledge to current conversation | Guidance and patterns |
| **Agents** | Run in separate isolated context | Domain expertise with tool restrictions |
| **MCP** | Provides external tools | Database, browser, API connections |

**The relationship:**
- **Output Styles** change *how Claude thinks* at the system level
- **CLAUDE.md** adds *project context* without changing core behaviour
- **Skills** teach Claude *how* to follow standards and patterns
- **Agents** run in *isolation* with domain expertise
- **MCP** *provides* the tools themselves (Context7, Playwright, etc.)

**When to use which:**
- Use **Output Styles** to fundamentally change Claude's behaviour
- Use **CLAUDE.md** for project-specific rules and context
- Use **Skills** for reusable guidance and workflows
- Use **Agents** when you need isolation or different tool access
- Use **MCP** to connect Claude to external systems

## Global vs Local Configuration

Claude Code supports configuration at two levels:

| Level | Location | Scope |
|-------|----------|-------|
| **Global** | `~/.claude/` | All projects, all sessions |
| **Local** | `<project>/.claude/` | Single project only |

**Global** = Personal preferences that follow you everywhere
**Local** = Project-specific rules committed to git and shared with team

Each folder in COR-CODE explains how to install globally or locally. See the README in each folder for details.

## Quick Start

### Install All Skills

```bash
# Clone the repo
git clone https://github.com/webSmartTeam/COR-CODE.git

# Copy skills to your Claude config
cp -r COR-CODE/skills/* ~/.claude/skills/

# Copy agents
cp -r COR-CODE/agents/* ~/.claude/agents/

# Copy hooks
cp -r COR-CODE/hooks/* ~/.claude/hooks/

# Copy output styles
cp -r COR-CODE/output-styles/* ~/.claude/output-styles/

# Copy global CLAUDE.md (customise placeholders after copying)
cp COR-CODE/global-claude/CLAUDE.md ~/.claude/CLAUDE.md
```

### Install Specific Skill

```bash
cp -r COR-CODE/skills/feature-dev ~/.claude/skills/
```

## Skills Overview

| Skill | Description | Chrome Required |
|-------|-------------|-----------------|
| `feature-dev` | 7-phase feature development workflow | Optional |
| `contact-form-builder` | AWS SES contact forms with reCAPTCHA | No |
| `site-harvest` | Extract website content and design | For comparison |
| `web-frontend` | Frontend preferences and standards | For colour picker |
| `seo-skill` | Technical SEO patterns | No |
| `non-stop` | Autonomous development mode | Yes |
| `vercel-deployment` | UK-first Vercel deployment | No |
| `programmatic-claude` | Run Claude via CLI/SDK for automation | No |
| `supabase-vercel-shop` | Complete e-commerce platform with CMS | No |
| `stripe-shop-integration` | Stripe payment integration patterns | No |
| `new-and-imported-projects` | Project setup for new or cloned repos | No |

## Agents Overview

| Agent | Expertise |
|-------|-----------|
| `frontend` | UI/UX, accessibility, responsive design |
| `backend` | APIs, reliability, server-side systems |
| `security` | Threat modeling, vulnerabilities |
| `performance` | Optimisation, bottlenecks |
| `architect` | Systems design, scalability |
| `qa` | Testing, quality assurance |
| `refactorer` | Code quality, technical debt |
| `scribe` | Documentation, UK English |
| `ecommerce-builder` | E-commerce platforms with Supabase/Stripe |

## Requirements

- Claude Code CLI
- For Chrome-dependent features: `claude --chrome` or `claude --chrome --resume`

## Configuration

Skills and agents use placeholders for user-specific values:

| Placeholder | Replace With |
|-------------|--------------|
| `{{USERNAME}}` | Your system username |
| `your-email@example.com` | Your actual email |
| `your-api-key-here` | Your actual API key |
| `your-project` | Your project name |

## Development Workflow

**COR-CODE is a distribution repository** - not a development environment.

### The Correct Workflow

```
~/.claude/skills/       →  COR-CODE/skills/
(develop & test here)      (copy for distribution)
```

1. **Develop in Global** (`~/.claude/skills/`): Create and test skills where they actually run
2. **Copy to COR-CODE**: Once working, copy to distribution repo
3. **Commit COR-CODE**: Push the distribution package

### Syncing Skills

```bash
# After fixing a skill in global:
cp -r ~/.claude/skills/feature-dev/* COR-CODE/skills/feature-dev/

# Or sync all skills:
rsync -av --exclude='.DS_Store' ~/.claude/skills/ COR-CODE/skills/

# Then commit COR-CODE
git -C COR-CODE add -A && git -C COR-CODE commit -m "sync: Update skills from global"
```

### Location-Specific Skills

Some skills only make sense in one location:

| Skill | Location | Reason |
|-------|----------|--------|
| `global-config-audit` | Global only | Audits YOUR personal config |
| `programmatic-claude` | COR-CODE only | Documentation about distributing Claude setups |

## UK Standards

This framework follows UK conventions:

- UK English spelling (colour, organisation, realise)
- London deployment region (lhr1)
- British date format (DD/MM/YYYY)
- GBP currency where applicable

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Licence

**COR Solutions Proprietary Licence** - This software is the intellectual property of COR Solutions Ltd.

- Internal use permitted for authorised team members
- Client use permitted under active service agreement
- Redistribution, resale, and derivative works prohibited
- See [LICENCE](LICENCE) for full terms

---

**COR Solutions** | [Website](https://msp.corsolutions.co.uk) | Professional Claude Code Enhancement
