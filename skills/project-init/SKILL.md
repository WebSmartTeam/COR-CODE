---
name: project-init
description: Initialise new or imported projects. New projects get a private git repo created in the website/app subfolder. Imported projects are cloned into that subfolder. Project root contains Claude config (CLAUDE.md, STYLE_GUIDE.md) - git repo lives in subfolder only. Triggers: init project, new project, import project, clone project, take over project.
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

# Project Init Skill

**Purpose**: Initialise new or imported projects with correct folder structure and UK standards.

## Two Workflows

| Type | What happens |
|------|--------------|
| **New project** | Create private git repo (`webSmartTeam/name`) IN the `website/` subfolder |
| **Imported project** | Clone existing repo INTO the `website/` subfolder |

**Key point**: Git repo lives in subfolder. Project root is Claude config only (not tracked by git).

## Project Structure Pattern

```
project-root/                    ← Claude config + workspace wrapper
├── .claude/settings.local.json  ← Permissions
├── CLAUDE.md                    ← Project identity + rules
├── STYLE_GUIDE.md               ← Brand colours, typography
├── DELETED_CODE.md              ← Track removed code
├── .env.local                   ← Secrets (gitignored)
├── .gitignore
└── website/                     ← Deployable (pushed to git)
    ├── package.json
    ├── vercel.json              ← regions: ["lhr1"]
    ├── src/
    └── public/
```

**Subfolder naming**: `website/`, `app/`, `platform/`, `dashboard/` depending on project type.

## Anti-Patterns (NEVER DO)

- ❌ CLAUDE.md inside website/ subfolder
- ❌ .claude/ inside website/ subfolder
- ❌ vercel.json in project root (goes WITH package.json)
- ❌ localhost testing - always Vercel preview URLs
- ❌ Creating public git repos without explicit permission

## What to Create

### 1. CLAUDE.md (project root)
Include:
- Project name, client, type (website/app/platform)
- UK Standards block (UK English, lhr1, GBP, DD/MM/YYYY)
- SuperClaude capabilities note
- Workspace boundary (this folder only)
- Git: push to main unless told otherwise

### 2. STYLE_GUIDE.md (project root)
- Brand colours table (Primary, Secondary, Accent, Background, Text)
- Typography (headings, body)
- Change log table

### 3. DELETED_CODE.md (project root)
- Table: Date | File | Reason | Code Block
- Track before deleting

### 4. .claude/settings.local.json (project root)
```json
{
  "permissions": {
    "allow": ["Bash(npm:*)", "Bash(npx:*)", "Bash(git:*)"]
  }
}
```

### 5. vercel.json (inside website/app subfolder)
```json
{
  "regions": ["lhr1"]
}
```

### 6. .gitignore (project root)
```
.env
.env.local
.env*.local
node_modules/
.DS_Store
```

## UK Standards (Always Apply)

- UK English: colour, organisation, realise
- Region: London (lhr1)
- Currency: GBP (£)
- Date: DD/MM/YYYY
- Phone: +44 format

## Git Setup (New Projects)

```bash
# In website/app subfolder (where package.json lives)
git init
git add .
git commit -m "feat: Initial project setup

Developed by COR Solutions MSP Platform
https://msp.corsolutions.co.uk

Co-Authored-By: COR Solutions AI <enquiries@corsolutions.co.uk>"

# Create private repo under webSmartTeam org
gh repo create webSmartTeam/{{PROJECT_NAME}} --private --source=. --remote=origin --push
```

## Import Workflow (Existing Projects)

When importing a project from git (taking over someone else's work):

```bash
# 1. Create project root folder with config
mkdir -p {{PROJECT_NAME}}
cd {{PROJECT_NAME}}

# 2. Create wrapper config files (CLAUDE.md, STYLE_GUIDE.md, DELETED_CODE.md, .gitignore)
# [Use templates from this skill]

# 3. Clone existing repo into website/app subfolder
git clone {{REPO_URL}} website/
# OR for other project types:
git clone {{REPO_URL}} app/
git clone {{REPO_URL}} platform/

# 4. Add .claude/settings.local.json in project root

# 5. Add vercel.json with regions: ["lhr1"] if missing
```

**Key difference**: Imported projects already have git history - don't re-init, just wrap with our config structure.

## After Setup

Tell user:
1. Config created in project root
2. Deployable code goes in website/ (or app/, platform/)
3. Update STYLE_GUIDE.md as design decisions made
4. Git repo created under webSmartTeam (private)
