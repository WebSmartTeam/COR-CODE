# COR-CODE Agents

Specialist AI agents for domain-specific expertise in Claude Code.

## Installation

Copy to your global Claude config:

```bash
cp -r agents/* ~/.claude/agents/
```

## Available Agents

| Agent | Description |
|-------|-------------|
| `frontend` | UI/UX specialist with accessibility focus |
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

## Usage

Agents auto-activate based on context keywords, or use explicit flags:

```bash
--agent-frontend      # UI/UX work
--agent-backend       # API development
--agent-security      # Security audit
--agent-performance   # Optimisation
```

## Agent Features

Each agent includes:

- **Tools**: Specific tool combinations for the domain
- **Priorities**: Clear decision framework
- **MCP Preferences**: Recommended MCP servers
- **Auto-Activation**: Context keywords that trigger the agent
- **Commands**: Optimised command suggestions

## Customisation

Edit any agent file to adjust:

- Priority hierarchies
- Quality standards
- MCP server preferences
- Auto-activation keywords

## UK English

The `scribe` agent enforces UK English standards for documentation.
All agents follow professional British communication conventions.

---

Part of COR-CODE v1.0.0
