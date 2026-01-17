# Anthropic Official Documentation Reference

**Source of truth for Claude Code features.**

All documentation available as clean markdown at `https://code.claude.com/docs/en/*.md`

## Documentation URLs

| Topic | URL | Last Verified |
|-------|-----|---------------|
| **Skills** | https://code.claude.com/docs/en/skills.md | 2025-01-17 |
| **Output Styles** | https://code.claude.com/docs/en/output-styles.md | 2025-01-17 |
| **Hooks Guide** | https://code.claude.com/docs/en/hooks-guide.md | 2025-01-17 |
| **Sub-Agents** | https://code.claude.com/docs/en/sub-agents.md | 2025-01-17 |
| **Headless Mode** | https://code.claude.com/docs/en/headless.md | 2025-01-17 |
| **MCP Servers** | https://code.claude.com/docs/en/mcp.md | 2025-01-17 |
| **Plugins** | https://code.claude.com/docs/en/plugins.md | 2025-01-17 |
| **Discover Plugins** | https://code.claude.com/docs/en/discover-plugins.md | 2025-01-17 |
| **Troubleshooting** | https://code.claude.com/docs/en/troubleshooting.md | 2025-01-17 |

## How to Use

**Fetch fresh docs**:
```
WebFetch https://code.claude.com/docs/en/skills.md
```

**Compare against COR-CODE**:
1. Fetch official .md
2. Compare with our skills/output-styles/hooks
3. Update if Anthropic added new features
4. Update "Last Verified" date

## Why This Matters

- Anthropic updates documentation when features change
- Our skills/agents should align with official capabilities
- Timestamps help track when we last verified alignment
- .md format = clean content, no HTML parsing needed

## Mapping to COR-CODE

| Official Doc | COR-CODE Location |
|--------------|-------------------|
| skills.md | `skills/` folder |
| output-styles.md | `output-styles/` folder |
| hooks-guide.md | `hooks/` folder |
| sub-agents.md | `agents/` folder |
| headless.md | `skills/programmatic-claude/` |

## Maintenance Schedule

**Recommended**: Check monthly or when Claude Code updates

**Process**:
1. Fetch each URL
2. Diff against previous version (if cached)
3. Update COR-CODE if new features discovered
4. Update timestamps in this file
