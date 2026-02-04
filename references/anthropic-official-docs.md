# Anthropic Official Documentation Reference

**Source of truth for Claude Code features.**

All documentation available as clean markdown at `https://code.claude.com/docs/en/*.md`

## Documentation URLs

### Claude Code CLI Documentation
| Topic | URL | Last Verified |
|-------|-----|---------------|
| **Skills** | https://code.claude.com/docs/en/skills.md | 2025-02-04 |
| **Output Styles** | https://code.claude.com/docs/en/output-styles.md | 2025-01-17 |
| **Hooks Guide** | https://code.claude.com/docs/en/hooks-guide.md | 2025-01-17 |
| **Sub-Agents** | https://code.claude.com/docs/en/sub-agents.md | 2025-02-04 |
| **Headless/Programmatic** | https://code.claude.com/docs/en/headless.md | 2025-01-17 |
| **MCP Servers** | https://code.claude.com/docs/en/mcp.md | 2025-01-19 |
| **Plugins** | https://code.claude.com/docs/en/plugins.md | 2025-01-17 |
| **Discover Plugins** | https://code.claude.com/docs/en/discover-plugins.md | 2025-01-17 |
| **Troubleshooting** | https://code.claude.com/docs/en/troubleshooting.md | 2025-01-17 |
| **CLI Reference** | https://code.claude.com/docs/en/cli-reference.md | 2025-01-17 |
| **Settings** | https://code.claude.com/docs/en/settings.md | 2025-01-17 |
| **Slash Commands** | https://code.claude.com/docs/en/slash-commands.md | 2025-01-17 |
| **Memory (CLAUDE.md)** | https://code.claude.com/docs/en/memory.md | 2025-01-17 |

### Claude API & Agent SDK Documentation (Advanced)
| Topic | URL | Last Verified |
|-------|-----|---------------|
| **MCP Connector (API)** | https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md | 2025-01-19 |
| **Remote MCP Servers** | https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers.md | 2025-01-19 |
| **Agent SDK MCP** | https://platform.claude.com/docs/en/agent-sdk/mcp.md | 2025-01-19 |

**Note**: The API/SDK docs above are for server-side and programmatic usage, not CLI configuration.

## GitHub Repository

| Resource | URL | Purpose |
|----------|-----|---------|
| **Changelog** | https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md | Track new features, breaking changes, updates |
| **Issues** | https://github.com/anthropics/claude-code/issues | Bug reports, feature requests |
| **Discussions** | https://github.com/anthropics/claude-code/discussions | Community Q&A |

**Check the changelog** when Claude Code updates to see what's new or changed.

## Engineering Blog (Advanced Patterns)

| Topic | URL | Published | Key Insight |
|-------|-----|-----------|-------------|
| **Code Execution with MCP** | https://www.anthropic.com/engineering/code-execution-with-mcp | 2025-11-04 | "Code Mode" - 98.7% token savings |
| **Cloudflare Code Mode** | https://blog.cloudflare.com/code-mode/ | 2025-09-26 | Original "Code Mode" implementation |

### Code Mode Pattern (2025-11-04)

**The Problem**: Direct tool calls consume excessive tokens:
- Tool definitions overload context (150K+ tokens for thousands of tools)
- Intermediate results flow through model multiple times

**The Solution**: Present MCP servers as code APIs, not direct tool calls:
```
servers/
├── google-drive/
│   ├── getDocument.ts
│   └── index.ts
├── salesforce/
│   ├── updateRecord.ts
│   └── index.ts
```

**Benefits**:
- **Progressive disclosure**: Load tools on-demand via filesystem exploration
- **Context efficiency**: Filter/transform data in execution environment before returning
- **Better control flow**: Loops, conditionals, error handling in code
- **Privacy-preserving**: Intermediate results stay in execution environment
- **State persistence**: Write intermediate results to files for resumption
- **Skills integration**: Save reusable functions with SKILL.md files

**Cloudflare Reference**: https://blog.cloudflare.com/code-mode/ (original implementation, September 2025)

**Why Code Mode Works** (Cloudflare insight):
> "Making an LLM perform tasks with tool calling is like putting Shakespeare through a month-long class in Mandarin and then asking him to write a play in it."

LLMs have seen millions of real TypeScript/code examples in training, but only contrived synthetic examples of tool calls.

**Key Quote** (Anthropic): "LLMs are adept at writing code and developers should take advantage of this strength to build agents that interact with MCP servers more efficiently."

**Cloudflare Implementation**:
- `codemode` helper in Cloudflare Agents SDK
- Converts MCP tools → TypeScript API definitions
- Runs in V8 isolates (not containers) - millisecond startup
- Bindings hide API keys from sandbox
- Docs: https://github.com/cloudflare/agents/blob/main/docs/codemode.md

---

## Key Findings (2025-02-04 Audit)

### New Since Last Audit (2025-01-19 → 2025-02-04)

**Sub-Agents (New Features)**:
- `/agents` slash command — lists all available agents in current session
- `--agents` CLI flag — start Claude Code in agent-only mode
- Background agents with `run_in_background` parameter on Task tool
- Agent resume capability — resume a previous agent by ID
- `SubagentStart` / `SubagentStop` hook events for lifecycle management
- `auto-compaction` — agents handle context limits with automatic summarisation
- Agents can preload skills via `skills` field in frontmatter

**Skills (New Features)**:
- `context: fork` with `agent` field — runs skill as isolated subagent
- `disable-model-invocation: true` — prevents Claude auto-triggering the skill
- `argument-hint` — placeholder text shown when skill is invoked
- Supporting files pattern — `skills/my-skill/SKILL.md` + `skills/my-skill/*.md` (all loaded)
- Dynamic context injection — `!`command`` syntax executes shell and injects output
- Skills can reference agent files for fork execution

---

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
- `auto` (default): Activates when tools exceed 10% of context window
- `auto:N`: Custom threshold (e.g., `auto:50` for 50 tools)
- `true`: Always enabled
- `false`: Disabled

### MCP Registry API (2025-01-19)

**Endpoint**: `https://api.anthropic.com/mcp-registry/docs`

Browse and discover MCP servers from the official Anthropic registry. Useful for finding community MCP servers.

### Claude Code as MCP Server (2025-01-19)

Run Claude Code itself as an MCP server for other applications:

```bash
claude mcp serve
```

This exposes Claude Code's capabilities to external MCP clients.

### Managed MCP Configuration (2025-01-19)

Claude Code supports managed MCP configuration for enterprise deployments:
- Centralised server definitions
- Organisation-wide tool policies
- Automatic server provisioning

### MCP Tool Naming & Wildcards (2025-01-19)

**Tool Naming Convention**:
```
mcp__<server-name>__<tool-name>
```

**Wildcard Patterns for allowedTools**:
```json
{
  "autoApproveTools": [
    "mcp__context7__*",      // All context7 tools
    "mcp__magic__*",         // All magic tools
    "mcp__supabase__*"       // All supabase tools
  ]
}
```

**Best Practices**:
- Use wildcards to auto-approve trusted MCP servers
- Place in `~/.claude/settings.json` for global approval
- Tool search auto-activates when tools exceed 10% of context window

### MCP API Integration (Advanced - Not CLI)

**MCP Connector** (for API/SDK, not CLI):
- Beta header: `mcp-client-2025-11-20`
- Toolset configuration in `tools` array
- Supports allowlist/denylist patterns per tool

**Remote MCP Servers**:
- HTTP transport required (no local stdio)
- Third-party hosted MCP servers
- Authentication via headers

**Agent SDK MCP**:
- For programmatic claude-agent-sdk usage
- `permissionMode`: bypassPermissions, acceptEdits, plan, fullAutoMcp, none
- Supports in-process SDK MCP servers

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

**Last full audit**: 2025-02-04
