#!/usr/bin/env python3
"""
ElevenLabs Voice Suite - Interactive Setup

Guides users through configuration with clear choices:
1. Global vs Local installation
2. Auto-read behavior
3. API key configuration
4. Voice selection

COR Solutions - ElevenLabs Voice Suite
"""

import shutil
import subprocess
import sys
from pathlib import Path


# Paths
HOME = Path.home()
SCRIPT_DIR = Path(__file__).parent.parent
CONFIG_TEMPLATES = SCRIPT_DIR / "config-templates"
TTS_PATCH = SCRIPT_DIR / "tts-patch" / "daemon_streaming.py"

# Installation locations
GLOBAL_PLUGIN_DIR = HOME / ".claude" / "plugins"
LOCAL_PLUGIN_DIR = Path.cwd() / ".claude" / "plugins"


def print_header(text: str) -> None:
    """Print a formatted header."""
    print()
    print("=" * 60)
    print(f"  {text}")
    print("=" * 60)
    print()


def print_section(text: str) -> None:
    """Print a section header."""
    print()
    print(f"--- {text} ---")
    print()


def ask_choice(question: str, options: list[tuple[str, str]], default: int = 1) -> int:
    """Ask user to choose from options. Returns 1-indexed choice."""
    print(question)
    print()
    for i, (label, desc) in enumerate(options, 1):
        marker = "(default)" if i == default else ""
        print(f"  {i}. {label} {marker}")
        if desc:
            print(f"     {desc}")
    print()

    while True:
        choice = input(f"Enter choice [1-{len(options)}, default={default}]: ").strip()
        if not choice:
            return default
        try:
            val = int(choice)
            if 1 <= val <= len(options):
                return val
        except ValueError:
            pass
        print(f"Please enter a number between 1 and {len(options)}")


def ask_yes_no(question: str, default: bool = True) -> bool:
    """Ask a yes/no question."""
    default_str = "Y/n" if default else "y/N"
    while True:
        answer = input(f"{question} [{default_str}]: ").strip().lower()
        if not answer:
            return default
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'")


def ask_input(prompt: str, default: str = "", required: bool = False) -> str:
    """Ask for text input."""
    if default:
        full_prompt = f"{prompt} [default: {default}]: "
    else:
        full_prompt = f"{prompt}: "

    while True:
        value = input(full_prompt).strip()
        if not value and default:
            return default
        if not value and required:
            print("This field is required.")
            continue
        return value


def check_prerequisites() -> bool:
    """Check if prerequisites are installed."""
    print_section("Checking Prerequisites")

    issues = []

    # Check Python version
    if sys.version_info < (3, 10):
        issues.append(f"Python 3.10+ required (you have {sys.version_info.major}.{sys.version_info.minor})")
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")

    # Check mpv
    if shutil.which("mpv"):
        print("✅ mpv installed")
    else:
        issues.append("mpv not installed - run: brew install mpv (macOS) or apt install mpv (Linux)")

    # Check Claude Code
    if shutil.which("claude"):
        print("✅ Claude Code CLI installed")
    else:
        issues.append("Claude Code CLI not found")

    if issues:
        print()
        print("❌ Missing prerequisites:")
        for issue in issues:
            print(f"   - {issue}")
        print()
        return False

    return True


def install_official_plugins() -> bool:
    """Install official ElevenLabs plugins."""
    print_section("Installing Official Plugins")

    try:
        print("Installing elevenlabs/stt...")
        result = subprocess.run(
            ["claude", "plugin", "install", "elevenlabs/stt"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0 and "already installed" not in result.stderr.lower():
            print(f"Warning: {result.stderr}")
        else:
            print("✅ STT plugin installed")

        print("Installing elevenlabs/tts...")
        result = subprocess.run(
            ["claude", "plugin", "install", "elevenlabs/tts"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0 and "already installed" not in result.stderr.lower():
            print(f"Warning: {result.stderr}")
        else:
            print("✅ TTS plugin installed")

        return True
    except Exception as e:
        print(f"❌ Failed to install plugins: {e}")
        return False


def apply_streaming_patch() -> bool:
    """Apply the true streaming patch to TTS daemon."""
    print_section("Applying True Streaming Patch")

    # Find daemon.py
    cache_dir = HOME / ".claude" / "plugins" / "cache" / "elevenlabs" / "elevenlabs-tts"

    if not cache_dir.exists():
        print("❌ TTS plugin cache not found. Install the plugin first.")
        return False

    daemon_path = None
    for version_dir in cache_dir.iterdir():
        candidate = version_dir / "src" / "elevenlabs_tts" / "daemon.py"
        if candidate.exists():
            daemon_path = candidate
            break

    if not daemon_path:
        print("❌ Could not find daemon.py in TTS plugin")
        return False

    # Backup original
    backup_path = daemon_path.with_suffix(".py.original")
    if not backup_path.exists():
        shutil.copy(daemon_path, backup_path)
        print(f"✅ Backed up original to {backup_path.name}")

    # Apply patch
    if TTS_PATCH.exists():
        shutil.copy(TTS_PATCH, daemon_path)
        print("✅ True streaming patch applied")
        print("   Audio now plays as chunks arrive (~500ms latency)")
        return True
    else:
        print(f"❌ Patch file not found: {TTS_PATCH}")
        return False


def configure_plugins(
    install_scope: str,
    api_key: str,
    voice_id: str,
    auto_read: bool
) -> bool:
    """Create configuration files."""
    print_section("Configuring Plugins")

    # Determine config directory
    if install_scope == "global":
        config_dir = GLOBAL_PLUGIN_DIR
        scope_desc = "Global (~/.claude/plugins/)"
    else:
        config_dir = LOCAL_PLUGIN_DIR
        scope_desc = f"Local ({LOCAL_PLUGIN_DIR})"

    print(f"Installing to: {scope_desc}")

    # Create directories
    stt_dir = config_dir / "elevenlabs-stt"
    tts_dir = config_dir / "elevenlabs-tts"
    stt_dir.mkdir(parents=True, exist_ok=True)
    tts_dir.mkdir(parents=True, exist_ok=True)

    # STT config
    stt_config = f"""[elevenlabs-stt]
api_key = "{api_key}"
hotkey = "ctrl+shift+space"
activation_mode = "toggle"
transcription_mode = "batch"
sound_effects = true
"""

    stt_config_path = stt_dir / "config.toml"
    stt_config_path.write_text(stt_config)
    print(f"✅ STT config: {stt_config_path}")

    # TTS config
    auto_read_str = "true" if auto_read else "false"
    tts_config = f"""[elevenlabs-tts]
api_key = "{api_key}"
voice_id = "{voice_id}"
model_id = "eleven_multilingual_v2"
output_format = "mp3_44100_128"
speed = 1.0
stability = 0.5
similarity_boost = 0.75
auto_read = {auto_read_str}
hotkey_toggle = "ctrl+shift+t"
hotkey_pause = "ctrl+shift+p"
hotkey_skip = "ctrl+shift+s"
skip_code_blocks = true
max_text_length = 5000
sound_effects = true
"""

    tts_config_path = tts_dir / "config.toml"
    tts_config_path.write_text(tts_config)
    print(f"✅ TTS config: {tts_config_path}")

    return True


def start_daemons() -> bool:
    """Start the STT and TTS daemons."""
    print_section("Starting Daemons")

    # Find exec scripts
    cache_dir = HOME / ".claude" / "plugins" / "cache" / "elevenlabs"

    stt_exec = None
    tts_exec = None

    for plugin_dir in cache_dir.iterdir():
        if "stt" in plugin_dir.name:
            for version_dir in plugin_dir.iterdir():
                candidate = version_dir / "scripts" / "exec.py"
                if candidate.exists():
                    stt_exec = candidate
        elif "tts" in plugin_dir.name:
            for version_dir in plugin_dir.iterdir():
                candidate = version_dir / "scripts" / "exec.py"
                if candidate.exists():
                    tts_exec = candidate

    if stt_exec:
        print("Starting STT daemon...")
        subprocess.Popen(
            [sys.executable, str(stt_exec), "-m", "elevenlabs_stt.daemon", "start", "--background"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✅ STT daemon started")
    else:
        print("⚠️ STT exec script not found")

    if tts_exec:
        print("Starting TTS daemon...")
        subprocess.Popen(
            [sys.executable, str(tts_exec), "-m", "elevenlabs_tts.daemon", "start", "--background"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✅ TTS daemon started")
    else:
        print("⚠️ TTS exec script not found")

    return True


def main():
    print_header("ElevenLabs Voice Suite - Setup")

    print("This wizard will help you set up voice input (STT) and output (TTS)")
    print("for Claude Code with true streaming for minimal latency.")
    print()

    # Check prerequisites
    if not check_prerequisites():
        print()
        print("Please install missing prerequisites and run setup again.")
        return 1

    # Question 1: Global vs Local
    print_section("Installation Scope")
    print("Where should the voice configuration be installed?")
    print()
    print("⚠️  IMPORTANT: This affects which Claude instances can use voice!")
    print()

    scope_choice = ask_choice(
        "Choose installation scope:",
        [
            ("LOCAL (This Project Only)",
             "Config saved to ./.claude/plugins/ - ONLY this project's Claude can use voice"),
            ("GLOBAL (All Projects)",
             "Config saved to ~/.claude/plugins/ - ALL your Claude instances share voice settings"),
        ],
        default=1  # Default to LOCAL to avoid the mistake I made
    )

    install_scope = "local" if scope_choice == 1 else "global"

    if install_scope == "global":
        print()
        print("⚠️  Warning: Global installation means ALL your Claude instances")
        print("   will have access to voice. If auto_read is ON, they may all speak!")
        if not ask_yes_no("Are you sure you want global installation?", default=False):
            install_scope = "local"
            print("Changed to local installation.")

    # Question 2: Auto-read behavior
    print_section("Auto-Read Behaviour")
    print("Should Claude automatically speak its responses?")
    print()

    auto_read_choice = ask_choice(
        "Choose auto-read behaviour:",
        [
            ("OFF - Manual Control (Recommended)",
             "Claude only speaks when you trigger voice mode (Ctrl+Shift+Space)"),
            ("ON - Always Speak",
             "Claude automatically speaks all responses (can be noisy!)"),
        ],
        default=1  # Default OFF to avoid random speaking
    )

    auto_read = (auto_read_choice == 2)

    if auto_read and install_scope == "global":
        print()
        print("🚨 CAUTION: You've chosen Global + Auto-Read ON")
        print("   This means ALL your Claude instances will speak automatically!")
        if not ask_yes_no("Are you absolutely sure?", default=False):
            auto_read = False
            print("Changed auto_read to OFF.")

    # Question 3: API Key
    print_section("ElevenLabs API Key")
    print("Get your API key from: https://elevenlabs.io/app/developers/api-keys")
    print()

    api_key = ask_input("Enter your ElevenLabs API key", required=True)

    # Question 4: Voice ID
    print_section("Voice Selection")
    print("Find voice IDs at: https://elevenlabs.io/app/voice-library")
    print("Or use a cloned voice from your account.")
    print()

    voice_id = ask_input(
        "Enter voice ID",
        default="21m00Tcm4TlvDq8ikWAM",  # Rachel (default)
        required=False
    )

    if not voice_id:
        voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel fallback

    # Summary before installation
    print_header("Installation Summary")
    print(f"  Scope:      {'LOCAL (this project only)' if install_scope == 'local' else 'GLOBAL (all projects)'}")
    print(f"  Auto-read:  {'ON (Claude speaks automatically)' if auto_read else 'OFF (manual control)'}")
    print(f"  API Key:    {api_key[:10]}...{api_key[-4:]}")
    print(f"  Voice ID:   {voice_id}")
    print()

    if not ask_yes_no("Proceed with installation?", default=True):
        print("Setup cancelled.")
        return 0

    # Install official plugins
    if not install_official_plugins():
        print("⚠️ Plugin installation had issues, continuing anyway...")

    # Apply streaming patch
    if not apply_streaming_patch():
        print("⚠️ Streaming patch failed, continuing with buffered playback...")

    # Configure plugins
    if not configure_plugins(install_scope, api_key, voice_id, auto_read):
        print("❌ Configuration failed")
        return 1

    # Start daemons
    if not start_daemons():
        print("⚠️ Daemon startup had issues")

    # Success
    print_header("Setup Complete!")

    print("Voice system is ready to use:")
    print()
    print("  Voice Input (STT):")
    print("    Ctrl+Shift+Space  - Start/stop recording")
    print()
    print("  Voice Output (TTS):")
    print("    Ctrl+Shift+T      - Toggle TTS on/off")
    print("    Ctrl+Shift+P      - Pause/resume playback")
    print("    Ctrl+Shift+S      - Skip current playback")
    print()

    if not auto_read:
        print("  📝 Auto-read is OFF:")
        print("     Claude will only speak when you use voice input (Ctrl+Shift+Space)")
        print("     Or use the voice manager: python3 scripts/voice-manager.py")
    else:
        print("  🔊 Auto-read is ON:")
        print("     Claude will speak all responses automatically")

    print()
    print("  Configuration saved to:")
    if install_scope == "local":
        print(f"    {LOCAL_PLUGIN_DIR}/elevenlabs-stt/config.toml")
        print(f"    {LOCAL_PLUGIN_DIR}/elevenlabs-tts/config.toml")
    else:
        print(f"    {GLOBAL_PLUGIN_DIR}/elevenlabs-stt/config.toml")
        print(f"    {GLOBAL_PLUGIN_DIR}/elevenlabs-tts/config.toml")

    print()
    print("Enjoy talking with Claude! 🎤")

    return 0


if __name__ == "__main__":
    sys.exit(main())
