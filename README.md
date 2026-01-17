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

## Skills vs Agents vs MCP

Understanding how these three concepts work together:

| Component | What It Does | Example |
|-----------|--------------|---------|
| **Skills** | Add knowledge to the current conversation | "Always use UK English", "Follow this deployment pattern" |
| **Agents** | Run in separate context with specific tools | Security specialist with threat modeling focus |
| **MCP** | Provides tools Claude can use | Database connections, browser automation |

**The relationship:**
- **Skills** tell Claude *how* to use tools and follow standards
- **Agents** run in *isolation* with their own tool access and domain expertise
- **MCP** *provides* the tools themselves (Context7, Playwright, etc.)

**When to use which:**
- Use **Skills** for guidance, patterns, and standards
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
