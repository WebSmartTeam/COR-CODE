# COR-CODE

**Claude Code Enhancement Framework** - Production-ready skills, agents, and hooks for Claude Code.

Developed by [COR Solutions](https://msp.corsolutions.co.uk) - Professional AI-enhanced development tools.

## What's Included

| Folder | Contents |
|--------|----------|
| `skills/` | User-invocable skills for common workflows |
| `agents/` | Specialist personas for domain expertise |
| `hooks/` | Automation hooks for quality gates |
| `context/` | Context files for project standards |
| `scripts/` | Utility scripts for installation/setup |

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Ensure NO personal data or credentials
4. Submit a pull request

### Security Checklist

Before submitting, verify:

- [ ] No hardcoded usernames or paths
- [ ] No API keys or credentials
- [ ] No personal email addresses
- [ ] No client-specific domains
- [ ] Placeholders used for all user-specific values

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Licence

MIT Licence - See [LICENCE](LICENCE) for details.

---

**COR Solutions** | [Website](https://msp.corsolutions.co.uk) | Professional Claude Code Enhancement
