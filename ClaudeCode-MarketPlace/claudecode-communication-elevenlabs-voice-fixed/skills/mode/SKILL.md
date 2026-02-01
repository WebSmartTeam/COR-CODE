---
name: mode
description: Switch between Instruction mode (text only) and Conversation mode (text + voice). Use "conv" or "inst" as argument.
---

# Switch Voice Mode

Change between Instruction and Conversation modes.

## Usage

```bash
# Switch to Conversation mode (Claude speaks responses)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/voice-manager.py mode conv

# Switch to Instruction mode (text only)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/voice-manager.py mode inst
```

## Mode Options

| Argument | Mode | Behaviour |
|----------|------|-----------|
| `conv`, `conversation`, `chat`, `2` | Conversation | Claude responds in text AND voice |
| `inst`, `instruction`, `text`, `1` | Instruction | Claude responds in text only |

## When to Use Each Mode

### Instruction Mode (Default)
Best for:
- Giving complex instructions
- Code reviews
- Tasks where you need to read the response

### Conversation Mode
Best for:
- Natural back-and-forth chat
- Hands-free interaction
- When you're away from keyboard

The mode switch is announced via voice when changed.
