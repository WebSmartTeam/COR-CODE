# Hooks Changelog

## 2025-01-23 - UltraPlan & Non-Stop Detection Added

**Updated:** `skill-detector.sh` now detects two additional skills

**UltraPlan triggers:**
- "ultraplan", "plan phases", "phase planning", "deep plan", "strategic plan", "architect plan", "execute phase", "run phase"
- Two-stage workflow: --ultrathink for planning → forked context for execution

**Non-stop triggers:**
- "non-stop", "nonstop", "don't stop", "work until done", "autonomous mode", "work autonomously", "keep going"
- Autonomous work mode with chrome devtools validation

**New skill:** `ultraplan` (renamed from saas-phase-builder)
- Deep architectural planning with --ultrathink (32K tokens)
- Phased execution with fresh 200K context per phase
- Project type templates (SaaS, e-commerce, multi-tenant, API)
- PHASES.md output format for build plans

---

## 2025-01-23 - Setup Hook Added

**New hook:** `setup-detector.sh` for project initialisation

**Trigger:** `claude --init` (uses new Setup event from Claude Code 2.1.10+)

**What it does:**
- Checks if CLAUDE.md exists (project already configured)
- If not, prompts Claude to ask user:
  1. Project type (website/platform/app)
  2. Project name
  3. Existing git repo URL (or new project)
- Then runs `new-and-imported-projects` skill

**Why:**
New `--init` flag in Claude Code triggers Setup hooks. Perfect for zero-friction project setup instead of manually invoking skills.

---

## 2025-01-17 - Skill Detector Rewrite

**What we changed:**
- Rewrote `skill-detector.sh` to use official stdin + jq approach
- Added fallback to env var for compatibility
- Updated skill paths to new folder structure (`skill-name/SKILL.md`)

**Why:**
The original hook used `CLAUDE_USER_PROMPT` env var, but official Anthropic examples pipe JSON to stdin and parse with `jq`. This is more reliable for structured data.

**How it works:**
```bash
# Claude pipes JSON like {"user_prompt": "setup project"} to stdin
# Script extracts with jq, matches keywords, outputs reminder tags
cat | jq -r '.user_prompt' | grep -i "setup"
```

**README rewrite:**
- Reduced from 324 lines to 75 lines
- Old README documented 5 archived hooks that weren't active
- New README shows actual current state + correct format from official docs

**Archive folder:**
Contains old experimental hooks - not active, kept for reference.

---

*Part of SuperClaude framework cleanup - skills and hooks now follow official Anthropic patterns.*
