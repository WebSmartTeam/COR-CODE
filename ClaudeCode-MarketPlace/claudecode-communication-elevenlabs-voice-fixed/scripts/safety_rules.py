"""Voice Command Safety Rules - Blocks dangerous commands from voice input.

SECURITY FEATURE: Prevents accidental execution of destructive commands
when someone in your environment says something that sounds like a command.

This module provides a safety filter that checks voice input BEFORE it's
sent to Claude Code, blocking commands that could cause data loss or
system damage.
"""

import re
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

# ============================================================
# DANGEROUS COMMAND PATTERNS
# ============================================================
# These patterns are checked against voice input. If matched,
# the command is BLOCKED and logged for security.

DANGEROUS_PATTERNS = [
    # File/Directory Deletion
    (r'\b(delete|remove|rm)\s+(all|everything|\*|-rf|-r)\b', 'file deletion'),
    (r'\brm\s+-[rf]+\b', 'recursive delete'),
    (r'\brmdir\b.*\b(all|\*)\b', 'directory deletion'),
    (r'\bunlink\b.*\ball\b', 'file unlinking'),
    (r'\bwipe\b', 'data wiping'),
    (r'\bshred\b', 'secure delete'),
    (r'\btruncate\b', 'file truncation'),

    # Database Operations
    (r'\bdrop\s+(database|table|schema|index)\b', 'database drop'),
    (r'\bdelete\s+from\b.*\bwhere\s+1\s*=\s*1\b', 'delete all rows'),
    (r'\btruncate\s+table\b', 'table truncation'),
    (r'\bdrop\s+all\b', 'drop all'),

    # Git Destructive Operations
    (r'\bgit\s+push\s+--force\b', 'force push'),
    (r'\bgit\s+push\s+-f\b', 'force push'),
    (r'\bgit\s+reset\s+--hard\b', 'hard reset'),
    (r'\bgit\s+clean\s+-fd\b', 'git clean'),
    (r'\bgit\s+checkout\s+\.\b', 'discard all changes'),

    # System Commands
    (r'\bsudo\s+rm\b', 'sudo delete'),
    (r'\bchmod\s+777\b', 'insecure permissions'),
    (r'\bchown\s+-R\b.*\b/\b', 'recursive ownership change'),
    (r'\bmkfs\b', 'format filesystem'),
    (r'\bdd\s+if=.*of=/dev\b', 'disk overwrite'),
    (r'\b:()\s*{\s*:\s*\|\s*:\s*&\s*}\s*;\s*:\b', 'fork bomb'),

    # Credential/Secret Operations
    (r'\b(expose|leak|share|post)\s+(credentials?|secrets?|api.?keys?|passwords?)\b', 'credential exposure'),
    (r'\bprint\s+(env|environment|secrets?)\b', 'environment exposure'),

    # Permission Confirmations (prevent accidental approval)
    (r'\b(yes|approve|confirm|allow|permit)\s+(delete|remove|drop|execute|run)\b', 'permission confirmation'),
    (r'\bpermission\s+(approved|granted|given)\b', 'permission grant'),
    (r'\bgo\s+ahead\b', 'execution approval'),
    (r'\bjust\s+do\s+it\b', 'blanket approval'),
    (r'\bexecute\s+(that|it|this)\b', 'execution command'),

    # Cloud/Infrastructure
    (r'\b(destroy|terminate)\s+(all|instance|server|cluster)\b', 'infrastructure destruction'),
    (r'\bterraform\s+destroy\b', 'terraform destroy'),
    (r'\bkubectl\s+delete\b.*\b--all\b', 'kubernetes delete all'),

    # Network/Security
    (r'\bdisable\s+(firewall|security|authentication)\b', 'security disable'),
    (r'\bopen\s+port\s+\d+\b', 'port opening'),
]

# Words that should trigger extra caution (soft warnings, not blocks)
CAUTION_WORDS = [
    'delete', 'remove', 'drop', 'destroy', 'wipe', 'clear', 'reset',
    'force', 'override', 'bypass', 'disable', 'expose', 'public',
    'all', 'everything', 'entire', 'complete',
]


class VoiceSafetyFilter:
    """Filters voice commands for dangerous patterns before execution."""

    def __init__(self, enabled: bool = True, strict_mode: bool = False):
        """Initialize the safety filter.

        Args:
            enabled: Whether safety filtering is active
            strict_mode: If True, also blocks caution words (more restrictive)
        """
        self.enabled = enabled
        self.strict_mode = strict_mode
        self._blocked_count = 0
        self._caution_count = 0

    def check_command(self, text: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """Check if a voice command is safe to execute.

        Args:
            text: The voice command text to check

        Returns:
            Tuple of (is_safe, blocked_reason, warning_message)
            - is_safe: True if command can proceed, False if blocked
            - blocked_reason: Why it was blocked (None if safe)
            - warning_message: Caution warning (None if no concerns)
        """
        if not self.enabled:
            return (True, None, None)

        text_lower = text.lower()

        # Check dangerous patterns (BLOCK)
        for pattern, reason in DANGEROUS_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                self._blocked_count += 1
                logger.warning(
                    "BLOCKED dangerous voice command: '%s' (reason: %s)",
                    text[:100], reason
                )
                return (False, reason, None)

        # Check caution words (WARN)
        warning = None
        caution_found = [w for w in CAUTION_WORDS if w in text_lower]
        if caution_found:
            self._caution_count += 1
            warning = f"Voice command contains caution words: {', '.join(caution_found)}"
            logger.info("Caution in voice command: %s", warning)

            if self.strict_mode:
                return (False, f"strict mode: {warning}", None)

        return (True, None, warning)

    def filter_command(self, text: str) -> Optional[str]:
        """Filter a voice command, returning None if blocked.

        Args:
            text: The voice command text

        Returns:
            The text if safe, None if blocked
        """
        is_safe, reason, warning = self.check_command(text)

        if not is_safe:
            print(f"\n⚠️  VOICE COMMAND BLOCKED: {reason}")
            print(f"    Command was: {text[:80]}...")
            print("    This is a safety feature to prevent accidental destructive actions.")
            print("    Type the command manually if you really mean it.\n")
            return None

        if warning:
            print(f"\n⚡ Caution: {warning}\n")

        return text

    @property
    def stats(self) -> dict:
        """Get safety filter statistics."""
        return {
            'enabled': self.enabled,
            'strict_mode': self.strict_mode,
            'blocked_count': self._blocked_count,
            'caution_count': self._caution_count,
        }


# Global instance for easy access
_safety_filter: Optional[VoiceSafetyFilter] = None


def get_safety_filter() -> VoiceSafetyFilter:
    """Get the global safety filter instance."""
    global _safety_filter
    if _safety_filter is None:
        _safety_filter = VoiceSafetyFilter(enabled=True, strict_mode=False)
    return _safety_filter


def is_safe_command(text: str) -> bool:
    """Quick check if a command is safe.

    Args:
        text: Command text to check

    Returns:
        True if safe, False if dangerous
    """
    is_safe, _, _ = get_safety_filter().check_command(text)
    return is_safe


def filter_voice_input(text: str) -> Optional[str]:
    """Filter voice input, blocking dangerous commands.

    Args:
        text: Voice input text

    Returns:
        Text if safe, None if blocked
    """
    return get_safety_filter().filter_command(text)


# ============================================================
# CUSTOMISATION: Add your own rules
# ============================================================
# Users can add custom patterns to their config:
#
# [safety]
# enabled = true
# strict_mode = false
# custom_blocks = [
#     "deploy to production",
#     "merge to main",
# ]
# custom_allows = [
#     "delete test files",  # Override block for specific safe commands
# ]

def add_custom_pattern(pattern: str, reason: str) -> None:
    """Add a custom dangerous pattern at runtime.

    Args:
        pattern: Regex pattern to match
        reason: Description of why it's dangerous
    """
    DANGEROUS_PATTERNS.append((pattern, reason))
    logger.info("Added custom safety pattern: %s (%s)", pattern, reason)


if __name__ == "__main__":
    # Test the safety filter
    test_commands = [
        "delete all files",
        "rm -rf /",
        "git push --force",
        "drop database production",
        "yes, delete everything",
        "permission approved",
        "create a new file",  # Safe
        "help me write code",  # Safe
        "show me the logs",  # Safe
    ]

    print("Voice Safety Filter Test\n" + "=" * 40)

    for cmd in test_commands:
        is_safe, reason, warning = get_safety_filter().check_command(cmd)
        status = "✅ SAFE" if is_safe else f"❌ BLOCKED ({reason})"
        print(f"{status}: {cmd}")
        if warning:
            print(f"   ⚠️  {warning}")

    print(f"\nStats: {get_safety_filter().stats}")
