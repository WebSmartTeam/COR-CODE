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
| **Headless/Programmatic** | https://code.claude.com/docs/en/headless.md | 2025-01-17 |
| **MCP Servers** | https://code.claude.com/docs/en/mcp.md | 2025-01-17 |
| **Plugins** | https://code.claude.com/docs/en/plugins.md | 2025-01-17 |
| **Discover Plugins** | https://code.claude.com/docs/en/discover-plugins.md | 2025-01-17 |
| **Troubleshooting** | https://code.claude.com/docs/en/troubleshooting.md | 2025-01-17 |
| **CLI Reference** | https://code.claude.com/docs/en/cli-reference.md | 2025-01-17 |
| **Settings** | https://code.claude.com/docs/en/settings.md | 2025-01-17 |
| **Slash Commands** | https://code.claude.com/docs/en/slash-commands.md | 2025-01-17 |
| **Memory (CLAUDE.md)** | https://code.claude.com/docs/en/memory.md | 2025-01-17 |

## GitHub Repository

| Resource | URL | Purpose |
|----------|-----|---------|
| **Changelog** | https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md | Track new features, breaking changes, updates |
| **Issues** | https://github.com/anthropics/claude-code/issues | Bug reports, feature requests |
| **Discussions** | https://github.com/anthropics/claude-code/discussions | Community Q&A |

**Check the changelog** when Claude Code updates to see what's new or changed.

---

## Key Findings (2025-01-17 Audit)

### Skills Frontmatter (Official Spec)

```yaml
---
name: skill-name                    # Required: unique identifier
description: What + When + Triggers # Required: max 1024 chars, used for matching
allowed-tools:                      # Optional: restrict tools (NOTE: hyphenated!)
  - Read
  - Write
model: haiku|sonnet|opus           # Optional: override model for this skill
context: fork                       # Optional: run in isolated subagent
agent: agent-name                   # Optional: link to specific agent
hooks:                              # Optional: embed hooks in skill
  PreToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "lint $FILE"
user-invocable: true               # Optional: show in /skill command
disable-model-invocation: false    # Optional: prevent Claude auto-triggering
---
```

**CRITICAL**: Official uses `allowed-tools` (hyphen), not `allowed_tools` (underscore)

### Output Styles

**Location**: `~/.claude/output-styles/` or `.claude/output-styles/`

**Built-in styles**: Default, Explanatory, Learning

**Frontmatter**:
```yaml
---
name: Style Name
description: Shown in UI
keep-coding-instructions: false    # Keep default coding instructions
---
```

**Key insight**: Output styles modify the system prompt directly. Different from CLAUDE.md (user message) and --append-system-prompt.

### Hooks (Official Events)

- `PreToolUse` - Before tool execution
- `PostToolUse` - After tool execution
- `Stop` - When agent stops
- `Notification` - User notifications
- `SubagentStart` - When subagent spawns
- `SubagentStop` - When subagent finishes

### Sub-Agents (Built-in)

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| Explore | Haiku | Read-only | Fast codebase exploration |
| Plan | Inherited | Read-only | Implementation planning |
| general-purpose | Inherited | All | Complex multi-step tasks |

### MCP Configuration

**Scopes** (terminology changed):
- `local` (default) - Current project, private to you
- `project` - Shared via `.mcp.json`, committed to git
- `user` - All projects, private to you (was called `global`)

**Transports**:
- `http` - Recommended for remote servers
- `sse` - **Deprecated**, use http instead
- `stdio` - Local processes

**Tool Search**: `ENABLE_TOOL_SEARCH=auto|true|false|auto:N`

### Programmatic Mode (Agent SDK)

**Note**: "Headless mode" is now called "Agent SDK"

**CLI flags**:
- `-p "prompt"` - Non-interactive mode
- `--allowedTools "Read,Edit,Bash"` - Auto-approve tools
- `--output-format json|text|stream-json`
- `--json-schema '{...}'` - Structured output
- `--continue` - Resume most recent
- `--resume <id>` - Resume specific session
- `--append-system-prompt` - Add to system prompt
- `--system-prompt` - Replace system prompt

**SDK packages**:
- Python: `pip install claude-agent-sdk`
- TypeScript: `npm install @anthropic-ai/claude-agent-sdk`

### Plugins

**Structure**:
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required manifest
├── commands/                # Slash commands
├── agents/                  # Custom agents
├── skills/                  # Agent skills
├── hooks/
│   └── hooks.json          # Hook definitions
├── .mcp.json               # MCP servers
└── .lsp.json               # LSP servers (code intelligence)
```

**Namespace**: Plugin commands are `/plugin-name:command`

### Native Installation

```bash
# macOS/Linux/WSL
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

---

## Mapping to COR-CODE

| Official Doc | COR-CODE Location | Status |
|--------------|-------------------|--------|
| skills.md | `skills/` folder | Implemented |
| output-styles.md | `output-styles/` folder | Implemented |
| hooks-guide.md | `hooks/` folder | Implemented |
| sub-agents.md | `agents/` folder | Implemented |
| headless.md | `skills/programmatic-claude/` | Implemented |
| plugins.md | Not yet | TODO |
| mcp.md | Reference only | Partial |

---

## Maintenance Schedule

**Recommended**: Check monthly or when Claude Code updates

**Process**:
1. Fetch each URL with WebFetch
2. Compare against this reference
3. Update COR-CODE if new features
4. Update timestamps above

**Last full audit**: 2025-01-17
