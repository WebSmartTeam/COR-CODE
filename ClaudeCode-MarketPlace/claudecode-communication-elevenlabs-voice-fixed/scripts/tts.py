#!/usr/bin/env python3
"""
Simple TTS module for Claude Code integration.

This module provides a simple speak() function that Claude can use
to vocalize responses while keeping them in the conversation context.

Usage in Claude's responses:
    The text appears here in conversation AND gets spoken.

COR Solutions - ElevenLabs Voice Suite
"""

import json
import socket
import sys
from pathlib import Path


def get_socket_path() -> Path:
    """Get the TTS daemon socket path."""
    return Path.home() / ".claude" / "plugins" / "elevenlabs-tts" / "daemon.sock"


def is_daemon_running() -> bool:
    """Check if TTS daemon is running."""
    return get_socket_path().exists()


def speak(text: str, block: bool = False) -> bool:
    """Send text to TTS daemon for speech output.

    Args:
        text: Text to speak.
        block: If True, wait for speech to complete (not implemented yet).

    Returns:
        True if message sent successfully, False otherwise.
    """
    socket_path = get_socket_path()

    if not socket_path.exists():
        return False

    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.settimeout(5.0)
        client.connect(str(socket_path))
        message = {"type": "speak", "text": text}
        client.sendall(json.dumps(message).encode() + b"\n")
        client.close()
        return True
    except Exception:
        return False


def speak_or_print(text: str) -> str:
    """Speak text if daemon running, always return text for context.

    This is the recommended function for Claude to use - it ensures
    the text appears in conversation AND gets spoken if TTS is active.

    Args:
        text: Text to speak and return.

    Returns:
        The same text (for inclusion in response).
    """
    speak(text)  # Will silently fail if daemon not running
    return text


# Quick CLI usage
if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        if speak(text):
            print(f"Speaking: {text[:50]}...")
        else:
            print("TTS daemon not running")
    else:
        print("Usage: python3 tts.py 'text to speak'")
