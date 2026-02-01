# Claude Code Communication: ElevenLabs Voice (Fixed)

**FIXED version of the official ElevenLabs voice plugins for Claude Code.**

> The official ElevenLabs plugins have a 2-3 second latency bug and poor setup experience. This version **fixes those issues** and adds new features.

---

## SECURITY: Voice Safety Rules (Built-In Protection)

**Voice commands can trigger destructive actions!**

If someone in your environment says *"Delete all files"* or *"Drop the database"*, Claude Code may interpret this as YOUR instruction and act on it.

### Built-In Safety Filter (NEW!)

This plugin includes **automatic safety rules** that BLOCK dangerous voice commands:

```
✅ BLOCKED: "delete all files"      (file deletion)
✅ BLOCKED: "rm -rf /"              (recursive delete)
✅ BLOCKED: "git push --force"      (force push)
✅ BLOCKED: "drop database"         (database drop)
✅ BLOCKED: "yes, execute that"     (permission confirmation)
✅ BLOCKED: "permission approved"   (blanket approval)
```

When a dangerous command is detected via voice, you'll see:
```
⚠️  VOICE COMMAND BLOCKED: file deletion
    Command was: delete all files...
    This is a safety feature to prevent accidental destructive actions.
    Type the command manually if you really mean it.
```

### Safety Configuration

In your `config.toml`:

```toml
[safety]
enabled = true        # Enable/disable safety filter (KEEP ON!)
strict_mode = false   # Also block caution words like "delete"
log_blocked = true    # Log blocked commands for audit
custom_blocks = []    # Add your own patterns: ["deploy to prod"]
custom_allows = []    # Override blocks: ["delete test files"]
```

### Additional Recommendations

- Use in **private environments only** (not open offices, not public demos)
- Keep **auto_read = false** so Claude doesn't speak in sensitive contexts
- Consider **Instruction Mode** (text responses) for sensitive operations
- Be aware of **who can hear your microphone** when voice input is active

---

## Origin Story

This enhancement suite was born at a live demo.

**[Boris Starkov](https://www.linkedin.com/in/boris-starkov/)**, Growth Engineer at ElevenLabs and co-creator of the viral [GibberLink](https://github.com/anthropics/gibberlink) AI communication protocol, demonstrated the official ElevenLabs voice plugins at **[Brain Station London](https://brainstation.io/london)**, hosted by Olivier Legris.

While watching from the audience, **Pete Gypps (COR Solutions)** noticed the latency issues and used Claude Code on his laptop to:
1. Install and configure both the MCP server and voice plugin in under 10 minutes
2. Identify the buffering issue causing 2-3 second delays
3. Implement the true streaming fix in real-time while the demo was still running
4. Add toggle controls and mode switching for better usability

This suite packages those fixes and improvements for the community.

## What We Fixed & Added

| Issue/Feature | Official Plugin | This Suite |
|---------------|-----------------|------------|
| **TTS Latency** | ~3 seconds (buffers ALL audio first) | **~500ms** (true streaming to mpv) |
| **Setup Experience** | Manual config file editing | **Interactive wizard** with guided choices |
| **Installation Scope** | Not clearly explained | **Asks Global vs Local** with warnings |
| **Auto-Read Default** | Often enabled (all Claudes speak!) | **Defaults to OFF** (manual control) |
| **Voice Modes** | None | **Instruction vs Conversation** modes |
| **Spoken Feedback** | None | **Announces mode changes** and status |
| **Claude Code Skills** | None | **5 skills** for easy `/command` access |
| **Voice Safety Rules** | None | **Blocks dangerous commands** (delete, drop, force push) |

## Features

- **STT (Speech-to-Text)**: Press hotkey, speak, text appears in Claude Code
- **TTS (Text-to-Speech)**: Claude speaks responses using ElevenLabs voices
- **True Streaming**: Audio plays as chunks arrive (~500ms latency vs ~3s buffered)
- **Voice Cloning**: Use your own cloned voice from ElevenLabs
- **Toggle Controls**: Hotkeys to pause, skip, or disable
- **Voice Manager**: Spoken confirmations and mode switching
- **Two Modes**: Instruction (text only) or Conversation (text + voice)
- **Global vs Local**: Choose whether ALL projects or just ONE project can use voice
- **Voice Safety Rules**: Automatic blocking of dangerous commands (delete, drop, force push)

## Prerequisites

1. **ElevenLabs Account**: Get API key from https://elevenlabs.io/app/developers/api-keys
2. **mpv** (for true streaming): `brew install mpv` (macOS) or `apt install mpv` (Linux)
3. **Python 3.10+**: Required for the plugins
4. **Claude Code**: Obviously!

## Quick Start (Interactive Setup)

The easiest way to get started - the setup wizard asks all the right questions:

```bash
python3 scripts/setup.py
```

**The setup asks:**
1. **Global or Local?** - Do you want ALL your Claudes to use voice, or just this project?
2. **Auto-read?** - Should Claude speak automatically, or only when you trigger it?
3. **API Key** - Your ElevenLabs API key
4. **Voice ID** - Which voice to use (default: Rachel)

### Why Global vs Local Matters

| Scope | Config Location | Effect |
|-------|-----------------|--------|
| **LOCAL** | `./.claude/plugins/` | Only THIS project's Claude can use voice |
| **GLOBAL** | `~/.claude/plugins/` | ALL your Claude instances share voice |

**Recommendation**: Use LOCAL unless you specifically want all Claudes to talk.

### Why Auto-Read Matters

| Setting | Behaviour |
|---------|-----------|
| **OFF** (Recommended) | Claude only speaks when YOU trigger voice (Ctrl+Shift+Space) |
| **ON** | Claude speaks ALL responses automatically (can be noisy!) |

**Warning**: If you choose GLOBAL + AUTO-READ ON, every Claude instance will speak!

## Manual Installation

If you prefer manual setup:

### Step 1: Install the Official Plugins

```bash
# Install STT plugin (voice input)
claude plugin install elevenlabs/stt

# Install TTS plugin (voice output)
claude plugin install elevenlabs/tts
```

### Step 2: Apply True Streaming Patch (TTS)

The official TTS plugin buffers ALL audio before playing. Our patch streams directly to mpv for instant playback.

```bash
# Find your TTS daemon.py location
TTS_DAEMON=$(find ~/.claude/plugins -name "daemon.py" -path "*elevenlabs-tts*" | head -1)

# Backup original
cp "$TTS_DAEMON" "${TTS_DAEMON}.backup"

# Apply patch (copy our patched version)
cp tts-patch/daemon_streaming.py "$TTS_DAEMON"
```

### Step 3: Configure (Choose Your Scope!)

**For LOCAL installation (recommended):**
```bash
# Create LOCAL config directories
mkdir -p ./.claude/plugins/elevenlabs-stt
mkdir -p ./.claude/plugins/elevenlabs-tts

# Copy config templates
cp config-templates/stt-config.toml ./.claude/plugins/elevenlabs-stt/config.toml
cp config-templates/tts-config.toml ./.claude/plugins/elevenlabs-tts/config.toml

# Edit and add your API key
nano ./.claude/plugins/elevenlabs-stt/config.toml
nano ./.claude/plugins/elevenlabs-tts/config.toml
```

**For GLOBAL installation (use carefully):**
```bash
# Create GLOBAL config directories
mkdir -p ~/.claude/plugins/elevenlabs-stt
mkdir -p ~/.claude/plugins/elevenlabs-tts

# Copy config templates
cp config-templates/stt-config.toml ~/.claude/plugins/elevenlabs-stt/config.toml
cp config-templates/tts-config.toml ~/.claude/plugins/elevenlabs-tts/config.toml

# Edit and add your API key
nano ~/.claude/plugins/elevenlabs-stt/config.toml
nano ~/.claude/plugins/elevenlabs-tts/config.toml
```

### Step 4: Start the Daemons

```bash
# Start STT daemon (voice input)
python3 ~/.claude/plugins/cache/elevenlabs/elevenlabs-stt/*/scripts/exec.py -m elevenlabs_stt.daemon start --background

# Start TTS daemon (voice output)
python3 ~/.claude/plugins/cache/elevenlabs/elevenlabs-tts/*/scripts/exec.py -m elevenlabs_tts.daemon start --background
```

## Usage

### Voice Input (STT)
- **Ctrl+Shift+Space**: Start/stop recording (toggle mode)
- Speak your message, press again to transcribe
- Text appears in Claude Code input

### Voice Output (TTS)
- **Ctrl+Shift+T**: Toggle TTS on/off
- **Ctrl+Shift+P**: Pause/resume current playback
- **Ctrl+Shift+S**: Skip current playback

## Voice Manager (Recommended)

The Voice Manager provides a better experience with spoken confirmations and mode selection.

### Quick Start with Voice Manager

```bash
# Start with mode selection prompt
python3 scripts/voice-manager.py start

# Or use the shortcut
./scripts/voice start
```

This will:
1. Start both STT and TTS daemons
2. Ask you to choose a mode (1=Instruction, 2=Conversation)
3. Announce the selected mode via voice
4. You're ready to go!

### Voice Manager Commands

```bash
./scripts/voice start          # Start with mode selection
./scripts/voice stop           # Stop all daemons (announces "shutting down")
./scripts/voice status         # Show status (announces current mode)
./scripts/voice mode conv      # Switch to conversation mode
./scripts/voice mode inst      # Switch to instruction mode
./scripts/voice confirm "Hi"   # Speak any confirmation
```

### Spoken Confirmations

The Voice Manager provides audio feedback:
- **Starting**: "Conversation mode activated" or "Instruction mode"
- **Mode switch**: Announces the new mode
- **Stopping**: "Voice system shutting down"
- **Status check**: Announces current mode

## Two Conversation Modes

### Instruction Mode (Default)
You speak commands, Claude responds in text only. Good for:
- Giving complex instructions
- Code reviews
- Tasks where you need to read the response

### Conversation Mode
You speak, Claude responds in text AND voice. Good for:
- Natural back-and-forth chat
- Hands-free interaction
- When you're away from keyboard

**Switching modes**: Say "conversation mode" or "instruction mode", or use:
```bash
./scripts/voice mode conv   # Conversation mode
./scripts/voice mode inst   # Instruction mode
```

**How Claude activates voice**: Claude writes the response (visible in context) AND sends to TTS. Both happen - you see it and hear it.

### Make Claude Speak Programmatically

```python
import socket
import json
from pathlib import Path

socket_path = Path.home() / ".claude" / "plugins" / "elevenlabs-tts" / "daemon.sock"
client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect(str(socket_path))

message = {"type": "speak", "text": "Hello from Claude!"}
client.sendall(json.dumps(message).encode() + b"\n")
client.close()
```

## Configuration Options

### STT Config (`config.toml`)

```toml
[elevenlabs-stt]
api_key = "your-api-key-here"
hotkey = "ctrl+shift+space"
activation_mode = "toggle"        # or "push-to-talk"
transcription_mode = "batch"      # or "streaming"
sound_effects = true
```

### TTS Config (`config.toml`)

```toml
[elevenlabs-tts]
api_key = "your-api-key-here"
voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default: Rachel. Use your cloned voice ID!
model_id = "eleven_multilingual_v2"
speed = 1.0
auto_read = false                  # ⚠️ Set to false to prevent random speaking!
hotkey_toggle = "ctrl+shift+t"
hotkey_pause = "ctrl+shift+p"
hotkey_skip = "ctrl+shift+s"
skip_code_blocks = true
sound_effects = true
```

**⚠️ IMPORTANT**: `auto_read = false` is strongly recommended unless you want Claude to speak every response automatically!

## Finding Your Voice ID

1. Go to https://elevenlabs.io/app/voice-library
2. Click on your voice (or clone one)
3. Voice ID is in the URL or voice settings

## Troubleshooting

### "API key: not configured"
- Ensure config.toml has the `[elevenlabs-stt]` or `[elevenlabs-tts]` section header
- Restart the daemon after config changes

### Hotkey not working
- Check macOS Accessibility permissions: System Settings > Privacy & Security > Accessibility
- Enable your terminal app (iTerm2, Terminal, etc.)

### No audio playing
- Ensure mpv is installed: `which mpv`
- Check daemon is running: `ps aux | grep elevenlabs`

### All my Claudes are talking!
- You probably installed GLOBAL with `auto_read = true`
- Edit `~/.claude/plugins/elevenlabs-tts/config.toml` and set `auto_read = false`
- Restart TTS daemon

### Restart daemons
```bash
# Stop
pkill -f "elevenlabs_stt.daemon"
pkill -f "elevenlabs_tts.daemon"

# Start fresh
python3 ~/.claude/plugins/cache/elevenlabs/elevenlabs-stt/*/scripts/exec.py -m elevenlabs_stt.daemon start --background
python3 ~/.claude/plugins/cache/elevenlabs/elevenlabs-tts/*/scripts/exec.py -m elevenlabs_tts.daemon start --background
```

## Technical Details: How We Fixed It

### The Streaming Latency Fix

**The Problem**: The official ElevenLabs TTS plugin collects ALL audio chunks into memory before playing. For a typical response, this means waiting 2-3 seconds of silence before hearing anything.

**Official Plugin Code** (slow - buffers everything):
```python
# Collects ALL chunks first - user waits in silence
chunks = []
for chunk in client.stream(text):
    chunks.append(chunk)
audio = b"".join(chunks)  # Wait for ENTIRE response
player.play(audio)        # Only THEN play
```

**Our Fix** (fast - true streaming via mpv stdin pipe):
```python
# Pipes chunks directly to mpv as they arrive
process = subprocess.Popen(
    ["mpv", "--no-video", "--really-quiet", "-"],
    stdin=subprocess.PIPE
)
for chunk in client.stream(text):
    process.stdin.write(chunk)  # Play IMMEDIATELY as each chunk arrives!
    process.stdin.flush()
```

**Result**: ~500ms to first audio vs ~2-3 seconds buffered (6x improvement).

**Why This Works**: mpv can play audio from stdin in real-time. By piping chunks directly instead of buffering, audio starts playing as soon as the first chunk arrives from ElevenLabs API.

### The Setup Experience Fix

**The Problem**: Official plugins require manual config file editing with no guidance on Global vs Local implications.

**Our Fix**: Interactive Python wizard (`scripts/setup.py`) that:
1. Checks prerequisites (Python, mpv, Claude Code)
2. Explicitly asks: "Global or Local?" with warnings
3. Explicitly asks: "Auto-read ON or OFF?" with warnings
4. Warns if user chooses Global + Auto-read (all Claudes will speak!)
5. Creates config files in the correct location
6. Applies the streaming patch automatically
7. Starts daemons

### The Auto-Read Default Fix

**The Problem**: If `auto_read = true` in a GLOBAL config, every Claude instance speaks every response - very annoying!

**Our Fix**:
- Default to `auto_read = false` in templates
- Default to LOCAL installation in setup wizard
- Double-warn if user chooses Global + Auto-read ON

## Credits

- **[Boris Starkov](https://www.linkedin.com/in/boris-starkov/)** (ElevenLabs) - Original demo at Brain Station London
- **[Brain Station London](https://brainstation.io/london)** & Olivier Legris - Hosting the event
- **ElevenLabs** - Amazing voice AI platform
- **Anthropic** - Claude Code plugin system
- **Pete Gypps - COR Solutions** - True streaming fix & enhancement suite

## Author

**Pete Gypps** - [COR Solutions](https://msp.corsolutions.co.uk)
- Email: enquiries@corsolutions.co.uk
- GitHub: [webSmartTeam](https://github.com/webSmartTeam)

## Licence

MIT - Use freely, credit appreciated.
