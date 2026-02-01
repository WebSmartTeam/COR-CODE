#!/usr/bin/env python3
"""Send text to the TTS daemon for speech output.

Usage:
    python3 speak.py "Hello, this is a test"
    echo "Pipe input" | python3 speak.py
    python3 speak.py  # Interactive mode

COR Solutions - ElevenLabs Voice Suite
"""

import json
import socket
import sys
from pathlib import Path


def get_socket_path() -> Path:
    """Get the TTS daemon socket path."""
    return Path.home() / ".claude" / "plugins" / "elevenlabs-tts" / "daemon.sock"


def speak(text: str) -> bool:
    """Send text to TTS daemon.

    Args:
        text: Text to speak.

    Returns:
        True if successful, False otherwise.
    """
    socket_path = get_socket_path()

    if not socket_path.exists():
        print(f"Error: TTS daemon not running (socket not found: {socket_path})")
        print("Start the daemon with:")
        print("  python3 ~/.claude/plugins/cache/elevenlabs/elevenlabs-tts/*/scripts/exec.py -m elevenlabs_tts.daemon start --background")
        return False

    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(str(socket_path))

        message = {"type": "speak", "text": text}
        client.sendall(json.dumps(message).encode() + b"\n")
        client.close()

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    # Check for command line argument
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        if speak(text):
            print(f"Speaking: {text[:50]}..." if len(text) > 50 else f"Speaking: {text}")
        return

    # Check for piped input
    if not sys.stdin.isatty():
        text = sys.stdin.read().strip()
        if text:
            if speak(text):
                print(f"Speaking: {text[:50]}..." if len(text) > 50 else f"Speaking: {text}")
        return

    # Interactive mode
    print("ElevenLabs TTS - Interactive Mode")
    print("Type text to speak, Ctrl+C to exit")
    print("-" * 40)

    try:
        while True:
            text = input("> ").strip()
            if text:
                speak(text)
    except KeyboardInterrupt:
        print("\nBye!")
    except EOFError:
        pass


if __name__ == "__main__":
    main()
