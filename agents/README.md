# Agents

Specialist AI agents for domain-specific expertise in Claude Code.

## Understanding Agents (Subagents)

In Claude Code's official terminology, these are called **subagents**. They run in their own context window with:
- Custom system prompts
- Specific tool access
- Independent permissions

**Key distinction from Skills:**
- **Skills** add knowledge to the current conversation (guidance, patterns)
- **Subagents** run in a *separate context* with isolation

Subagents cannot spawn other subagents. If you need nested delegation, use Skills or chain subagents from the main conversation.

## Built-in Subagents

Claude Code includes these built-in subagents that activate automatically:

| Subagent | Model | Tools | Purpose |
|----------|-------|-------|---------|
| **Explore** | Haiku | Read-only | File discovery, code search, codebase exploration |
| **Plan** | Inherits | Read-only | Research for planning mode |
| **general-purpose** | Inherits | All tools | Complex research, multi-step operations |
| **Bash** | Inherits | Terminal | Running commands in separate context |
| **Claude Code Guide** | Haiku | Read-only | Answering questions about Claude Code |

**Explore** has thoroughness levels: `quick`, `medium`, `very thorough`

## Global vs Local Agents

| Aspect | Global (`~/.claude/agents/`) | Local (`<project>/.claude/agents/`) |
|--------|------------------------------|-------------------------------------|
| **Scope** | All projects, all sessions | Single project only |
| **Purpose** | Domain expertise used everywhere | Project-specific specialists |
| **Git** | Not in any repo (personal) | Committed to project repo (shared with team) |
| **Examples** | Security, performance, frontend | CMS specialist, client billing agent |

**Local agents override global:** If you have `frontend.md` in both locations, the local version takes precedence for that project.

## Installation

```bash
# Global (personal, all projects)
cp -r agents/* ~/.claude/agents/

# Local (one project only)
cp -r agents/* <project>/.claude/agents/
```

## Available Agents

| Agent | Description |
|-------|-------------|
| `web-frontend` | UI/UX specialist with accessibility focus and production checklist |
| `backend` | Reliability engineer and API specialist |
| `security` | Threat modeling and vulnerability assessment |
| `performance` | Optimisation and bottleneck elimination |
| `architect` | Systems design and scalability |
| `qa` | Quality assurance and testing |
| `refactorer` | Code quality and technical debt |
| `scribe` | Documentation with UK English standards |
| `mentor` | Educational guidance and knowledge transfer |
| `devops` | Infrastructure and deployment automation |
| `analyzer` | Root cause analysis and investigation |
| `design-reviewer` | Visual UI assessment using Playwright |
| `aws` | AWS services, cloud infrastructure, serverless architecture |
| `aws-alb` | AWS Application Load Balancer with ECS Fargate integration |
| `mobile-app` | Cross-platform mobile development (Flutter, React Native, SwiftUI) |
| `project-setup` | New project scaffolding with folder structure and UK standards |
| `content-migration` | Hardcoded content to database migration specialist |
| `mcp-specialist` | MCP server configuration and integration expert |
| `harvester` | Web scraping, content extraction, design system harvesting |
| `ecommerce-builder` | Supabase + Vercel e-commerce platforms with CMS |
| `xero` | Xero accounting integration and invoicing automation |

## Agent File Format

Agents are Markdown files with YAML frontmatter:

```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. Analyze code and provide specific,
actionable feedback on quality, security, and best practices.
```

### Supported Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase with hyphens |
| `description` | Yes | When Claude should delegate to this agent |
| `tools` | No | Allowed tools (inherits all if omitted) |
| `disallowedTools` | No | Tools to deny |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `skills` | No | Skills to load into agent's context |
| `hooks` | No | Lifecycle hooks for this agent |

## Usage

Agents auto-activate based on context keywords, or request explicitly:

```bash
# Explicit request
Use the code-reviewer agent to review my changes

# Or use flags
--agent-frontend      # UI/UX work
--agent-backend       # API development
--agent-security      # Security audit
--agent-performance   # Optimisation
```

## Common Patterns

### Isolate High-Volume Operations
Delegate verbose tasks (running tests, processing logs) to keep your main context clean.

### Run Parallel Research
Spawn multiple agents to investigate independent areas simultaneously.

### Chain Agents
Use agents in sequence - each completes and returns results for the next.

## When to Use Agents vs Main Conversation

**Use agents when:**
- Task produces verbose output you don't need in main context
- You want specific tool restrictions or permissions
- Work is self-contained and can return a summary

**Use main conversation when:**
- Task needs frequent back-and-forth
- Multiple phases share significant context
- Making a quick, targeted change

## Customisation

Edit any agent file to adjust:

- Priority hierarchies
- Quality standards
- MCP server preferences
- Auto-activation keywords

## UK English

The `scribe` agent enforces UK English standards for documentation.
All agents follow professional British communication conventions.

## Docs

https://code.claude.com/docs/en/sub-agents

---

Part of COR-CODE v1.2.0
