# Programmatic Claude Code

Run Claude Code programmatically via CLI, Python, or TypeScript for automated workflows.

## Three Interfaces

| Interface | Use Case | Install |
|-----------|----------|---------|
| **CLI** (`-p` flag) | Scripts, CI/CD, quick automation | Built into Claude Code |
| **Python SDK** | Full programmatic control, custom tools | `pip install claude-agent-sdk` |
| **TypeScript SDK** | Type-safe applications, Node.js integration | `npm install @anthropic-ai/claude-agent-sdk` |

## Quick Examples

### CLI: One-Shot Task
```bash
claude -p "Fix all TypeScript errors in src/" \
  --allowedTools "Read,Edit,Bash" \
  --output-format json
```

### CLI: Structured Output
```bash
claude -p "Extract all API endpoints from this codebase" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"endpoints":{"type":"array","items":{"type":"object","properties":{"path":{"type":"string"},"method":{"type":"string"},"description":{"type":"string"}}}}}}'
```

### Python: Simple Query
```python
from claude_agent_sdk import query, ClaudeAgentOptions
import asyncio

async def analyze_code():
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Grep", "Glob"],
        cwd="/path/to/project"
    )

    async for message in query(
        prompt="Analyze the architecture of this codebase",
        options=options
    ):
        print(message)

asyncio.run(analyze_code())
```

### TypeScript: With Custom Tools
```typescript
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const fetchUrl = tool(
  "fetch_url",
  "Fetch content from a URL",
  { url: z.string().url() },
  async ({ url }) => ({
    content: [{ type: "text", text: await fetch(url).then(r => r.text()) }]
  })
);

const server = createSdkMcpServer({
  name: "custom-tools",
  tools: [fetchUrl]
});

for await (const msg of query({
  prompt: "Fetch and summarize https://example.com",
  options: {
    mcpServers: { custom: server },
    allowedTools: ["mcp__custom__fetch_url"]
  }
})) {
  console.log(msg);
}
```

## Key Capabilities

### Automation Features
- **Unattended execution**: `--allowedTools` auto-approves specified tools
- **Structured output**: `--json-schema` enforces response format
- **Session continuity**: `--continue` / `--resume` for multi-step workflows
- **Custom system prompts**: `--append-system-prompt` for behaviour modification
- **Permission bypass**: `permissionMode: 'bypassPermissions'` (use carefully)

### SDK Features
- **Custom tools**: Define your own tools with type-safe schemas
- **In-process MCP servers**: Run MCP servers in the same process
- **Hooks**: Intercept and modify behaviour at key points
- **Interrupts**: Stop long-running operations mid-execution
- **File checkpointing**: Rewind file changes to specific points

## Files in This Skill

| File | Purpose |
|------|---------|
| `cli-reference.md` | Complete CLI flag documentation |
| `python-patterns.md` | Python SDK patterns and examples |
| `typescript-patterns.md` | TypeScript SDK patterns and examples |
| `harvest-and-build.md` | Website cloning automation workflow |

## When to Use Programmatic Mode

**Use CLI (`-p`):**
- Shell scripts and automation
- CI/CD pipelines (GitHub Actions, GitLab CI)
- Quick one-off tasks
- Simple structured data extraction

**Use Python SDK:**
- Custom agent applications
- Complex multi-turn workflows
- Integration with Python tooling
- When you need hooks and custom tools

**Use TypeScript SDK:**
- Node.js applications
- Type-safe development
- Web service integrations
- When you need streaming and interrupts

## Integration with COR-CODE

Programmatic mode works with all COR-CODE components:

```bash
# Use with output styles
claude -p "Build a component" \
  --system-prompt "$(cat ~/.claude/output-styles/ai-first-builder.md)"

# Use with agents (via system prompt)
claude -p "Security audit this code" \
  --append-system-prompt "$(cat ~/.claude/agents/security.md)"
```

## CI/CD Examples

See the official documentation for:
- [GitHub Actions integration](https://code.claude.com/docs/en/github-actions)
- [GitLab CI/CD integration](https://code.claude.com/docs/en/gitlab-ci-cd)
