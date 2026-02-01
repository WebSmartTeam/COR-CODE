---
name: status
description: Show current status of ElevenLabs voice system - daemon status, current mode, and configuration.
---

# Voice System Status

Check the status of STT and TTS daemons and current mode.

## Usage

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/voice-manager.py status
```

## Output Shows

- **STT (voice input)**: Running or Stopped
- **TTS (voice output)**: Running or Stopped
- **Mode**: Instruction or Conversation

If TTS is running, it will also announce the current mode via voice.
