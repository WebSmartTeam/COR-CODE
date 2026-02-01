#!/bin/bash
# ElevenLabs Voice Suite Installer for Claude Code
# COR Solutions - True Streaming Edition

set -e

echo "================================================"
echo "ElevenLabs Voice Suite Installer"
echo "With True Streaming Patch for minimal latency"
echo "================================================"
echo ""

# Check for mpv
echo "Checking prerequisites..."
if ! command -v mpv &> /dev/null; then
    echo "⚠️  mpv not found - required for true streaming"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "   Install with: brew install mpv"
    else
        echo "   Install with: apt install mpv (or your package manager)"
    fi
    echo ""
    read -p "Continue without mpv? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ mpv installed"
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found - required"
    exit 1
fi
echo "✅ Python 3 installed"

# Check for Claude Code
if ! command -v claude &> /dev/null; then
    echo "❌ Claude Code CLI not found"
    echo "   Install from: https://claude.ai/code"
    exit 1
fi
echo "✅ Claude Code installed"

echo ""
echo "Installing plugins..."

# Install STT plugin
echo "Installing STT (voice input)..."
claude plugin install elevenlabs/stt || echo "STT may already be installed"

# Install TTS plugin
echo "Installing TTS (voice output)..."
claude plugin install elevenlabs/tts || echo "TTS may already be installed"

echo ""
echo "Applying true streaming patch..."

# Find TTS daemon
TTS_DAEMON=$(find ~/.claude/plugins -name "daemon.py" -path "*elevenlabs-tts*" 2>/dev/null | head -1)

if [ -z "$TTS_DAEMON" ]; then
    echo "⚠️  TTS daemon.py not found - you may need to run the TTS plugin first"
    echo "   Then re-run this script to apply the patch"
else
    # Backup original
    if [ ! -f "${TTS_DAEMON}.backup" ]; then
        cp "$TTS_DAEMON" "${TTS_DAEMON}.backup"
        echo "✅ Backed up original daemon.py"
    fi

    # Get script directory
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PATCH_FILE="$SCRIPT_DIR/../tts-patch/daemon_streaming.py"

    if [ -f "$PATCH_FILE" ]; then
        cp "$PATCH_FILE" "$TTS_DAEMON"
        echo "✅ Applied true streaming patch"
    else
        echo "⚠️  Patch file not found: $PATCH_FILE"
    fi
fi

echo ""
echo "Setting up config directories..."

mkdir -p ~/.claude/plugins/elevenlabs-stt
mkdir -p ~/.claude/plugins/elevenlabs-tts

# Copy config templates if configs don't exist
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -f ~/.claude/plugins/elevenlabs-stt/config.toml ]; then
    cp "$SCRIPT_DIR/../config-templates/stt-config.toml" ~/.claude/plugins/elevenlabs-stt/config.toml
    echo "✅ Created STT config template"
else
    echo "ℹ️  STT config already exists"
fi

if [ ! -f ~/.claude/plugins/elevenlabs-tts/config.toml ]; then
    cp "$SCRIPT_DIR/../config-templates/tts-config.toml" ~/.claude/plugins/elevenlabs-tts/config.toml
    echo "✅ Created TTS config template"
else
    echo "ℹ️  TTS config already exists"
fi

echo ""
echo "================================================"
echo "Installation complete!"
echo "================================================"
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. Add your ElevenLabs API key to both configs:"
echo "   nano ~/.claude/plugins/elevenlabs-stt/config.toml"
echo "   nano ~/.claude/plugins/elevenlabs-tts/config.toml"
echo ""
echo "2. (Optional) Set your voice ID in TTS config"
echo "   Find voice IDs at: https://elevenlabs.io/app/voice-library"
echo ""
echo "3. Start the daemons:"
echo "   # Start STT (voice input)"
echo "   python3 ~/.claude/plugins/cache/elevenlabs/elevenlabs-stt/*/scripts/exec.py -m elevenlabs_stt.daemon start --background"
echo ""
echo "   # Start TTS (voice output)"
echo "   python3 ~/.claude/plugins/cache/elevenlabs/elevenlabs-tts/*/scripts/exec.py -m elevenlabs_tts.daemon start --background"
echo ""
echo "4. Grant Accessibility permissions (macOS):"
echo "   System Settings > Privacy & Security > Accessibility"
echo "   Enable your terminal app"
echo ""
echo "HOTKEYS:"
echo "  Ctrl+Shift+Space - Toggle voice input"
echo "  Ctrl+Shift+T     - Toggle voice output"
echo "  Ctrl+Shift+P     - Pause/resume playback"
echo "  Ctrl+Shift+S     - Skip current playback"
echo ""
