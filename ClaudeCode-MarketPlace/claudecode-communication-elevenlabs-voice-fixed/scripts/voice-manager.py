#!/usr/bin/env python3
"""
Voice Manager for Claude Code - ElevenLabs Voice Suite

Manages both STT and TTS with spoken confirmations and mode switching.

Features:
- Spoken confirmations: "Listening", "Got it", "Mode changed"
- Two modes: Instruction (text only) / Conversation (text + voice)
- Coordinates both daemons
- Provides status feedback

Usage:
    python3 voice-manager.py start          # Start with mode selection
    python3 voice-manager.py status         # Show current status
    python3 voice-manager.py mode conv      # Switch to conversation mode
    python3 voice-manager.py mode inst      # Switch to instruction mode
    python3 voice-manager.py stop           # Stop all daemons
    python3 voice-manager.py confirm "text" # Speak a confirmation

COR Solutions - ElevenLabs Voice Suite
"""

import argparse
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path


# Paths
HOME = Path.home()
STT_CONFIG_DIR = HOME / ".claude" / "plugins" / "elevenlabs-stt"
TTS_CONFIG_DIR = HOME / ".claude" / "plugins" / "elevenlabs-tts"
TTS_SOCKET = TTS_CONFIG_DIR / "daemon.sock"
STT_PID_FILE = STT_CONFIG_DIR / "daemon.pid"
TTS_PID_FILE = TTS_CONFIG_DIR / "daemon.pid"
MODE_FILE = HOME / ".claude" / "plugins" / "voice-mode.txt"

# Find plugin cache paths
PLUGIN_CACHE = HOME / ".claude" / "plugins" / "cache" / "elevenlabs"


def find_exec_script(plugin_name: str) -> Path | None:
    """Find the exec.py script for a plugin."""
    cache_dir = PLUGIN_CACHE / plugin_name
    if not cache_dir.exists():
        return None

    for version_dir in cache_dir.iterdir():
        exec_script = version_dir / "scripts" / "exec.py"
        if exec_script.exists():
            return exec_script
    return None


def speak(text: str, wait: bool = True) -> bool:
    """Send text to TTS daemon."""
    if not TTS_SOCKET.exists():
        return False

    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.settimeout(5.0)
        client.connect(str(TTS_SOCKET))
        message = {"type": "speak", "text": text}
        client.sendall(json.dumps(message).encode() + b"\n")
        client.close()
        if wait:
            time.sleep(len(text) * 0.05 + 0.5)  # Rough estimate for speech duration
        return True
    except Exception:
        return False


def get_mode() -> str:
    """Get current voice mode."""
    if MODE_FILE.exists():
        return MODE_FILE.read_text().strip()
    return "instruction"  # Default


def set_mode(mode: str) -> None:
    """Set voice mode."""
    MODE_FILE.parent.mkdir(parents=True, exist_ok=True)
    MODE_FILE.write_text(mode)


def is_daemon_running(pid_file: Path) -> bool:
    """Check if a daemon is running."""
    if not pid_file.exists():
        return False

    try:
        content = pid_file.read_text().strip()

        # Handle JSON format (STT uses this)
        if content.startswith("{"):
            data = json.loads(content)
            pid = data.get("pid")
        else:
            # Plain number format (TTS uses this)
            pid = int(content)

        if pid:
            os.kill(pid, 0)
            return True
        return False
    except (ValueError, OSError, json.JSONDecodeError):
        return False


def start_stt_daemon() -> bool:
    """Start STT daemon."""
    exec_script = find_exec_script("elevenlabs-stt")
    if not exec_script:
        print("STT plugin not found. Install with: claude plugin install elevenlabs/stt")
        return False

    try:
        subprocess.Popen(
            [sys.executable, str(exec_script), "-m", "elevenlabs_stt.daemon", "start", "--background"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(2)
        return is_daemon_running(STT_PID_FILE)
    except Exception as e:
        print(f"Failed to start STT: {e}")
        return False


def start_tts_daemon() -> bool:
    """Start TTS daemon."""
    exec_script = find_exec_script("elevenlabs-tts")
    if not exec_script:
        print("TTS plugin not found. Install with: claude plugin install elevenlabs/tts")
        return False

    try:
        subprocess.Popen(
            [sys.executable, str(exec_script), "-m", "elevenlabs_tts.daemon", "start", "--background"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(2)
        return is_daemon_running(TTS_PID_FILE)
    except Exception as e:
        print(f"Failed to start TTS: {e}")
        return False


def stop_daemon(name: str) -> None:
    """Stop a daemon by name."""
    subprocess.run(["pkill", "-f", f"elevenlabs_{name}.daemon"], capture_output=True)


def cmd_start(args):
    """Start voice system with mode selection."""
    print("=" * 50)
    print("ElevenLabs Voice Suite - Starting")
    print("=" * 50)
    print()

    # Start TTS first (needed for confirmations)
    print("Starting TTS daemon...")
    if not start_tts_daemon():
        print("❌ TTS failed to start")
        return 1
    print("✅ TTS running")

    # Start STT
    print("Starting STT daemon...")
    if not start_stt_daemon():
        print("❌ STT failed to start")
        return 1
    print("✅ STT running")

    time.sleep(1)

    # Mode selection
    print()
    print("Select mode:")
    print("  1. Instruction mode (you speak, Claude responds in text)")
    print("  2. Conversation mode (you speak, Claude responds in text AND voice)")
    print()

    choice = input("Enter 1 or 2 [default: 1]: ").strip()

    if choice == "2":
        set_mode("conversation")
        speak("Conversation mode activated. I'll speak my responses.", wait=True)
        print("✅ Conversation mode - Claude will speak responses")
    else:
        set_mode("instruction")
        speak("Instruction mode. I'll respond in text only.", wait=True)
        print("✅ Instruction mode - Claude responds in text only")

    print()
    print("Voice system ready!")
    print("  Ctrl+Shift+Space = Toggle recording")
    print("  Say 'conversation mode' or 'instruction mode' to switch")
    print()

    return 0


def cmd_stop(args):
    """Stop all voice daemons."""
    speak("Voice system shutting down.", wait=False)
    time.sleep(1)

    stop_daemon("stt")
    stop_daemon("tts")

    # Clean up mode file
    if MODE_FILE.exists():
        MODE_FILE.unlink()

    print("Voice system stopped.")
    return 0


def cmd_status(args):
    """Show voice system status."""
    stt_running = is_daemon_running(STT_PID_FILE)
    tts_running = is_daemon_running(TTS_PID_FILE)
    mode = get_mode()

    print("ElevenLabs Voice Suite Status")
    print("-" * 30)
    print(f"STT (voice input):  {'✅ Running' if stt_running else '❌ Stopped'}")
    print(f"TTS (voice output): {'✅ Running' if tts_running else '❌ Stopped'}")
    print(f"Mode:               {mode.title()}")
    print()

    if tts_running:
        speak(f"Voice system active. {mode} mode.", wait=False)

    return 0


def cmd_mode(args):
    """Switch voice mode."""
    mode_input = args.mode_name.lower()

    if mode_input in ("conv", "conversation", "chat", "2"):
        set_mode("conversation")
        speak("Conversation mode. I'll speak my responses now.")
        print("✅ Switched to conversation mode")
    elif mode_input in ("inst", "instruction", "text", "1"):
        set_mode("instruction")
        speak("Instruction mode. Text responses only.")
        print("✅ Switched to instruction mode")
    else:
        print(f"Unknown mode: {mode_input}")
        print("Use: conv/conversation or inst/instruction")
        return 1

    return 0


def cmd_confirm(args):
    """Speak a confirmation message."""
    text = " ".join(args.text) if args.text else "Ready"
    if speak(text):
        print(f"Spoke: {text}")
    else:
        print("TTS daemon not running")
        return 1
    return 0


def cmd_listening(args):
    """Announce listening started."""
    speak("Listening", wait=False)
    return 0


def cmd_got_it(args):
    """Announce recording stopped."""
    speak("Got it", wait=False)
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Voice Manager for Claude Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  voice-manager.py start           Start with mode selection
  voice-manager.py mode conv       Switch to conversation mode
  voice-manager.py mode inst       Switch to instruction mode
  voice-manager.py status          Show current status
  voice-manager.py confirm "Hi"    Speak confirmation
  voice-manager.py stop            Stop all daemons
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Start
    subparsers.add_parser("start", help="Start voice system with mode selection")

    # Stop
    subparsers.add_parser("stop", help="Stop all voice daemons")

    # Status
    subparsers.add_parser("status", help="Show voice system status")

    # Mode
    mode_parser = subparsers.add_parser("mode", help="Switch voice mode")
    mode_parser.add_argument("mode_name", help="Mode: conv/conversation or inst/instruction")

    # Confirm
    confirm_parser = subparsers.add_parser("confirm", help="Speak confirmation")
    confirm_parser.add_argument("text", nargs="*", help="Text to speak")

    # Quick confirmations
    subparsers.add_parser("listening", help="Announce 'Listening'")
    subparsers.add_parser("got-it", help="Announce 'Got it'")

    args = parser.parse_args()

    if args.command == "start":
        return cmd_start(args)
    elif args.command == "stop":
        return cmd_stop(args)
    elif args.command == "status":
        return cmd_status(args)
    elif args.command == "mode":
        return cmd_mode(args)
    elif args.command == "confirm":
        return cmd_confirm(args)
    elif args.command == "listening":
        return cmd_listening(args)
    elif args.command == "got-it":
        return cmd_got_it(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
