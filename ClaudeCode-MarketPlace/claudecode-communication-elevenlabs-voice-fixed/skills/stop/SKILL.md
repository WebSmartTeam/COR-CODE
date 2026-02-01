---
name: stop
description: Stop all ElevenLabs voice daemons (STT and TTS). Announces shutdown before stopping.
---

# Stop Voice System

Stop both STT and TTS daemons.

## Usage

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/voice-manager.py stop
```

## What Happens

1. Announces "Voice system shutting down" (if TTS running)
2. Stops STT daemon (voice input)
3. Stops TTS daemon (voice output)
4. Cleans up mode file

## Manual Stop

If needed, you can also stop daemons manually:

```bash
pkill -f "elevenlabs_stt.daemon"
pkill -f "elevenlabs_tts.daemon"
```
