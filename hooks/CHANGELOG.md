# Hooks Changelog

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
