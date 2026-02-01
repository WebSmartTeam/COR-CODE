#!/bin/bash
# Quick speak command for Claude to use inline
# Usage: ./claude-speak.sh "Text to speak"
# Or: echo "Text" | ./claude-speak.sh

SOCKET_PATH="$HOME/.claude/plugins/elevenlabs-tts/daemon.sock"

if [ ! -S "$SOCKET_PATH" ]; then
    echo "TTS daemon not running" >&2
    exit 1
fi

# Get text from argument or stdin
if [ -n "$1" ]; then
    TEXT="$*"
else
    TEXT=$(cat)
fi

# Send to daemon via Python (most reliable for JSON)
python3 -c "
import socket, json
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect('$SOCKET_PATH')
s.sendall(json.dumps({'type': 'speak', 'text': '''$TEXT'''}).encode() + b'\n')
s.close()
" 2>/dev/null

echo "Speaking: ${TEXT:0:50}..."
