# Claude Code Installation Methods

**Verified**: January 2025

## Recommended: Native Installer

The native installer is Anthropic's recommended method.

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**What you get:**
- Self-contained Bun-compiled binary (~180MB)
- No Node.js dependency
- Background auto-updates that just work
- Apple-notarized and signed by Anthropic
- Installs to `~/.local/bin/claude`
- Versions stored in `~/.local/share/claude/versions/`

**Update command:**
```bash
claude update
```

**Verify installation:**
```bash
claude doctor
```

## Not Recommended: Homebrew

```bash
brew install --cask claude-code
```

**Problems:**
- No auto-updates (must manually run `brew upgrade claude-code`)
- Cask often lags behind releases (can be 7+ versions behind)
- Installs to `/opt/homebrew/bin/claude`

## Not Recommended: npm

```bash
npm install -g @anthropic-ai/claude-code
```

**Problems:**
- Requires Node.js dependency
- No auto-updates
- Can conflict with other global packages

## Switching to Native

If you have Homebrew or npm installed:

```bash
# Uninstall Homebrew
brew uninstall --cask claude-code

# OR uninstall npm
npm uninstall -g @anthropic-ai/claude-code

# Install native
curl -fsSL https://claude.ai/install.sh | bash

# Verify
claude doctor
```

## How to Check Your Installation

```bash
# Check path - should be ~/.local/bin/claude
which claude

# Check if native (look for symlink to versions folder)
ls -la ~/.local/bin/claude

# Should show: ~/.local/bin/claude -> ~/.local/share/claude/versions/X.X.X
```

## Release Channels

Configure via `/config` in Claude Code:
- `latest` - Most recent release
- `stable` - Stable releases only
