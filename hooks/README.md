# Hooks

Hooks run shell commands at specific points in Claude Code's workflow. They extend behaviour without modifying Claude itself.

## Global vs Local Hooks

| Aspect | Global (`~/.claude/settings.json`) | Local (`<project>/.claude/settings.json`) |
|--------|------------------------------------|--------------------------------------------|
| **Scope** | All projects, all sessions | Single project only |
| **Purpose** | Personal automation everywhere | Project-specific quality gates |
| **Git** | Not in any repo (personal) | Committed to project repo (shared with team) |
| **Examples** | Skill detection, logging | Project-specific validation, client rules |

**Note:** Hook scripts live in `~/.claude/hooks/` (global) or `<project>/.claude/hooks/` (local). The `settings.json` references them.

## Current Setup

**One hook active** - skill-detector on prompt submit:

```json
// ~/.claude/settings.json
"hooks": {
  "UserPromptSubmit": [
    {
      "matcher": "",
      "hooks": [{"type": "command", "command": "bash ~/.claude/hooks/skill-detector.sh"}]
    }
  ]
}
```

## Hook Events

| Event | When | Use For |
|-------|------|---------|
| `UserPromptSubmit` | User sends message | Skill reminders, context injection |
| `PreToolUse` | Before tool runs | Validation, logging, blocking |
| `PostToolUse` | After tool runs | Quality checks, notifications |
| `Notification` | Claude outputs text | Filtering, routing |
| `Stop` | Main agent stops | Cleanup, reporting |
| `SubagentStop` | Subagent stops | Aggregation, validation |
| `PreCompact` | Before context compaction | Saving critical context |

## Format

```json
"hooks": {
  "EventName": [
    {
      "matcher": "ToolName",
      "hooks": [
        { "type": "command", "command": "your-script.sh" }
      ]
    }
  ]
}
```

- **matcher**: Tool name to filter (empty string = all tools)
- **type**: `command` (shell) or `url` (webhook - coming soon)
- **command**: Script path or inline command

## Environment Variables Available

Scripts receive context via env vars:
- `CLAUDE_USER_PROMPT` - User's message
- `CLAUDE_TOOL_NAME` - Tool being used
- `CLAUDE_TOOL_INPUT` - Tool arguments (JSON)
- `CLAUDE_TOOL_OUTPUT` - Tool result (PostToolUse only)

## Tips

- Keep hooks fast (<100ms) - they block execution
- Use stdout for messages Claude sees
- Use stderr for logging (doesn't reach Claude)
- Exit 0 = continue, exit 2 = block tool (PreToolUse only)
- Hooks run in order listed

## Archive

Old experimental hooks in `./archive/` - not active.

## Docs

https://code.claude.com/docs/en/hooks-guide
