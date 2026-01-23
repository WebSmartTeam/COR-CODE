#!/bin/bash
# Setup hook - detects if project needs initialisation
# Triggered by: claude --init

if [ -f "CLAUDE.md" ]; then
    echo "✓ Project already configured (CLAUDE.md exists)"
    exit 0
fi

# No CLAUDE.md - needs setup
echo "=========================================="
echo "PROJECT SETUP REQUIRED"
echo "=========================================="
echo ""
echo "ASK USER:"
echo "1. Project type? (website / platform / app)"
echo "2. Project name?"
echo "3. Existing git repo URL to import? (or 'no' for new project)"
echo ""
echo "Then run 'new-and-imported-projects' skill:"
echo "- If git URL provided: clone into subfolder, wrap with config"
echo "- If no git URL: create new repo under webSmartTeam"
echo "=========================================="
exit 0
