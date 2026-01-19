---
name: cor-code-manager
description: Manage COR-CODE distribution repo - sync from global, security validation, and changelog versioning. Single skill for all distribution maintenance. Triggers: cor-code, sync cor-code, update distribution, check cor-code, release cor-code.
updated: 2025-01-18
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - TodoWrite
---

# COR-CODE Manager Skill

**Purpose**: Single skill for COR-CODE distribution - sync from global, security scan, version, and push.

## Core Workflow

```
~/.claude/skills/  →  COR-CODE/skills/
(develop here)        (distribution)
```

1. **Sync from global** - Copy updated skills
2. **Security scan** - Check for personal data
3. **Commit & push** - Update distribution

## Repository Information

- **Local Path**: `{{PROJECT_ROOT}}/COR-CODE/` (your SuperClaudecode workspace)
- **GitHub Repo**: `webSmartTeam/COR-CODE` (private)
- **GitHub URL**: `https://github.com/webSmartTeam/COR-CODE`

## Repository Structure (DO NOT DELETE)

```
COR-CODE/
├── skills/           # Synced from ~/.claude/skills/
├── agents/           # Synced from ~/.claude/agents/
├── hooks/            # Synced from ~/.claude/hooks/
├── output-styles/    # Synced from ~/.claude/output-styles/
├── global-claude/    # Template CLAUDE.md for distribution
├── references/       # NEVER DELETE - Official Anthropic docs links
├── README.md
├── CHANGELOG.md
└── LICENCE
```

**CRITICAL**: The `references/` folder contains official Anthropic documentation URLs. Do NOT delete this folder - it's essential reference material, not synced content.

## Commands

- `/cor-code sync` - Sync all skills from global to COR-CODE
- `/cor-code check` - Run security validation on entire repo
- `/cor-code release [major|minor|patch]` - Update version and changelog
- `/cor-code push` - Commit and push to GitHub

## Sync from Global

```bash
# Sync all shared skills (excludes global-only skills)
COR_CODE="{{PROJECT_ROOT}}/COR-CODE"  # Set to your COR-CODE local path

# Copy each skill (excluding global-only)
for skill in ~/.claude/skills/*/; do
  name=$(basename "$skill")
  # Skip global-only skills
  [[ "$name" == "global-config-audit" ]] && continue
  cp -r "$skill" "$COR_CODE/skills/"
done
```

**Global-only skills (don't sync):**
- `global-config-audit` - Audits YOUR personal config

## Timestamp Tracking

Each skill should have `updated: YYYY-MM-DD` in frontmatter:

```yaml
---
name: skill-name
description: ...
updated: 2025-01-18
---
```

### Check which skills need syncing

```bash
# Compare updated dates between global and COR-CODE
for skill in ~/.claude/skills/*/SKILL.md; do
  name=$(basename $(dirname "$skill"))
  [[ "$name" == "global-config-audit" ]] && continue

  global_date=$(grep "^updated:" "$skill" 2>/dev/null | cut -d' ' -f2)
  cor_date=$(grep "^updated:" "$COR_CODE/skills/$name/SKILL.md" 2>/dev/null | cut -d' ' -f2)

  if [[ "$global_date" != "$cor_date" ]]; then
    echo "⚠️  $name: global=$global_date cor-code=$cor_date"
  fi
done
```

### When updating a skill

1. Make changes in global (`~/.claude/skills/`)
2. Update the `updated:` field to today's date
3. Run `/cor-code sync` to copy to distribution

## Security Validation (MANDATORY)

**Before ANY skill is added to COR-CODE, check for client/project-specific data.**

Skills often get created during client work - they may contain real company names, domains, emails, or credentials that must be replaced with placeholders before distribution.

### Pre-Sync Checklist

**Ask yourself before syncing any skill:**

1. **Company names** - Is there a real company name? Replace with `{{COMPANY_NAME}}` or `Acme Ltd`
2. **Domains** - Any real `.co.uk`, `.com` domains? Replace with `example.com` or `your-domain.co.uk`
3. **Emails** - Any real email addresses? Replace with `your-email@example.com`
4. **Paths** - Any `/Users/username/` paths? Replace with `~/.claude/` or `{{HOME}}`
5. **API keys** - Any real keys? Replace with `your-api-key-here` or `{{API_KEY}}`
6. **URLs** - Any real website URLs? Replace with `https://example.com`
7. **Phone numbers** - Any real numbers? Replace with `+44 1234 567890`
8. **Addresses** - Any real addresses? Replace with `123 Example Street, London`

### Forbidden Patterns (Auto-Reject)

```bash
# Absolute user paths (ANY username)
/Users/[a-z]+/              # macOS
/home/[a-z]+/               # Linux
C:\\Users\\                 # Windows

# API Keys & Secrets (pattern-based)
sk-[a-zA-Z0-9]{20,}         # OpenAI
sb[a-z]_[a-zA-Z0-9]{20,}    # Supabase
ghp_[a-zA-Z0-9]{36}         # GitHub PAT
AKIA[A-Z0-9]{16}            # AWS access key
xoxb-                       # Slack bot token
sk_live_                    # Stripe live key
pk_live_                    # Stripe publishable live
rk_live_                    # Stripe restricted live

# Hardcoded credentials
password\s*[:=]\s*["'][^"']+
secret\s*[:=]\s*["'][^"']+
api[_-]?key\s*[:=]\s*["'][^"']+

# Personal email domains (not business)
@gmail\.com
@hotmail\.com
@outlook\.com
@yahoo\.com
```

### Allowed (COR Solutions Attribution Only)

```
enquiries@corsolutions.co.uk     # Git co-author
msp.corsolutions.co.uk           # Company credit URL
COR Solutions                    # Company name in credits
```

### Required Placeholders

| Real Data | Placeholder |
|-----------|-------------|
| Company name | `{{COMPANY_NAME}}` or `Acme Ltd` |
| Domain | `example.com` or `your-domain.co.uk` |
| Email | `your-email@example.com` or `{{EMAIL}}` |
| Home path | `~/.claude/` or `{{HOME}}/.claude/` |
| Project path | `{{PROJECT_ROOT}}` or `your-project/` |
| API key | `your-api-key-here` or `{{API_KEY}}` |
| Phone | `+44 1234 567890` or `{{PHONE}}` |
| Username | `{{USERNAME}}` or `your-username` |

## Validation Process

```bash
# 1. Check for absolute paths (any user)
grep -rEn "/Users/[a-z]+/|/home/[a-z]+/" COR-CODE/ --include="*.md"

# 2. Check for API key patterns
grep -rEn "sk-[a-zA-Z0-9]{20}|sb[a-z]_|ghp_|AKIA|sk_live_|pk_live_" COR-CODE/

# 3. Check for personal email domains
grep -rEn "@gmail\.|@hotmail\.|@outlook\.|@yahoo\." COR-CODE/

# 4. Check for real UK domains (manually review these)
grep -rEn "\.co\.uk" COR-CODE/ --include="*.md" | grep -v "example\|your-"

# 5. Verify placeholders exist where data is needed
grep -rn "{{.*}}\|your-\|example\.com" COR-CODE/
```

## Changelog Format

File: `COR-CODE/CHANGELOG.md`

```markdown
# COR-CODE Changelog

All notable changes documented here. Format: [Semantic Versioning](https://semver.org/)

## [Unreleased]

### Added
-

### Changed
-

### Fixed
-

---

## [1.0.0] - 2025-01-17

### Added
- Initial release
- Skills: feature-dev, contact-form-builder, seo-skill, site-harvest, web-frontend
- Agents: frontend, backend, security, performance, architect
- Hooks: pre-tool validation, post-tool quality checks
```

## Version Bump Rules

| Type | When | Example |
|------|------|---------|
| **major** | Breaking changes, major rewrites | 1.0.0 → 2.0.0 |
| **minor** | New skills/agents, new features | 1.0.0 → 1.1.0 |
| **patch** | Bug fixes, docs updates, tweaks | 1.0.0 → 1.0.1 |

## Release Workflow

```bash
# 1. Run security check
/cor-code check

# 2. If clean, update version
/cor-code release minor

# 3. Review changelog entry
# 4. Commit and push
/cor-code sync
```

## Adding Content Workflow

```bash
# 1. Specify source
/cor-code add ~/.claude/skills/feature-dev

# 2. Skill automatically:
#    - Copies to COR-CODE/skills/feature-dev/
#    - Scans for forbidden patterns
#    - Reports any issues
#    - If clean, confirms addition

# 3. If issues found:
#    - Lists each problem with line numbers
#    - Suggests replacements
#    - Does NOT copy until fixed
```

## Git Workflow

```bash
# Standard commit message format
git commit -m "feat: Add feature-dev skill

- 7-phase development workflow
- Visual validation support
- MCP integration patterns

COR-CODE v1.1.0"

# Push to private repo
git push origin main
```

## Team Access

Repository has two permission levels:
- **Senior Dev**: Write access (can push, merge)
- **Junior Dev**: Read access (can clone, pull)

Configure via GitHub repo settings → Collaborators and teams.
