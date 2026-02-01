---
name: start
description: Start the ElevenLabs voice system with mode selection. Choose between Instruction mode (text only) or Conversation mode (text + voice).
---

# Start Voice System

Start both STT and TTS daemons with mode selection.

## Usage

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/voice-manager.py start
```

## What Happens

1. Starts TTS daemon (voice output)
2. Starts STT daemon (voice input)
3. Asks you to choose a mode:
   - **1. Instruction Mode**: You speak, Claude responds in text only
   - **2. Conversation Mode**: You speak, Claude responds in text AND voice
4. Announces the selected mode via voice
5. Ready to use!

## Hotkeys After Starting

- **Ctrl+Shift+Space** - Start/stop voice recording
- **Ctrl+Shift+T** - Toggle TTS on/off
- **Ctrl+Shift+P** - Pause/resume playback
- **Ctrl+Shift+S** - Skip current playback
