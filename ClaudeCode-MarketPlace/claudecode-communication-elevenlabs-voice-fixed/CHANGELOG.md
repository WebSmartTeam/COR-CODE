# Changelog

All notable changes to Claude Code Communication: ElevenLabs Voice (Fixed) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-31

### Fixed (Issues with Official ElevenLabs Plugins)

- **TTS Buffering Latency**: Official plugin buffers ALL audio before playing (~3s delay). Our patch streams directly to mpv for ~500ms latency - a 6x improvement.
- **Unclear Installation Scope**: Official plugins don't explain Global vs Local. We ask explicitly and warn about implications.
- **Unsafe Auto-Read Default**: Official may default to auto_read=true causing ALL Claude instances to speak. We default to OFF.

### Added (New Features Not in Official)

- **Interactive Setup Wizard**: Step-by-step configuration with clear choices
- **Two Voice Modes**: Instruction (text only) and Conversation (text + voice)
- **Voice Manager**: Spoken confirmations when starting, stopping, switching modes
- **5 Claude Code Skills**: `/elevenlabs-voice-enhanced:setup`, `:start`, `:stop`, `:status`, `:mode`
- **Config Templates**: Ready-to-use configs without API keys

### Security

- No API keys included in package
- Clear warnings about Global + Auto-read implications
- `.gitignore` excludes sensitive config files
- **Voice Safety Rules**: Automatic blocking of dangerous voice commands:
  - File deletion (delete all, rm -rf, wipe)
  - Database operations (drop database, truncate table)
  - Git destructive ops (push --force, reset --hard)
  - Permission confirmations (yes execute, permission approved)
  - Infrastructure destruction (terraform destroy, kubectl delete --all)
- Configurable safety filter with strict mode option
- Custom block/allow patterns for enterprise needs
- Audit logging of blocked commands

### Documentation

- Comprehensive README with comparison table vs official
- Troubleshooting guide for common issues
- Clear explanation of Global vs Local installation
