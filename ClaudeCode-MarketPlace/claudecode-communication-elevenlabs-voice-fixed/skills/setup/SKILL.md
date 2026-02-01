---
name: setup
description: Set up ElevenLabs voice system for Claude Code with STT and TTS. Run this first to configure voice input and output.
---

# ElevenLabs Voice Suite Setup

Run the interactive setup wizard to configure voice for Claude Code.

## What This Does

1. **Checks prerequisites** - Python 3.10+, mpv, Claude Code CLI
2. **Asks installation scope** - LOCAL (this project only) or GLOBAL (all projects)
3. **Asks auto-read preference** - OFF (manual control) or ON (Claude speaks all responses)
4. **Configures API key** - Your ElevenLabs API key
5. **Configures voice** - Default Rachel or your cloned voice ID
6. **Applies true streaming patch** - Reduces latency from ~3s to ~500ms
7. **Starts daemons** - Launches STT and TTS background services

## Run Setup

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/setup.py
```

## Prerequisites

Before running setup, ensure you have:

1. **ElevenLabs API Key** - Get from https://elevenlabs.io/app/developers/api-keys
2. **mpv installed** - `brew install mpv` (macOS) or `apt install mpv` (Linux)
3. **Python 3.10+** - Check with `python3 --version`

## Important Choices

### Global vs Local

- **LOCAL** (Recommended): Only THIS project's Claude can use voice
- **GLOBAL**: ALL your Claude instances share voice settings

### Auto-Read

- **OFF** (Recommended): Claude only speaks when you trigger voice (Ctrl+Shift+Space)
- **ON**: Claude speaks ALL responses automatically (can be noisy!)

**Warning**: GLOBAL + AUTO-READ ON = every Claude instance will speak!
