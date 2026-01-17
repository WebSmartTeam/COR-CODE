#!/bin/bash
# Skill Detector Hook - Reminds Claude about available skills
# Uses stdin (official approach) with jq fallback to env var

# Read JSON from stdin, extract user_prompt field
# Fallback to env var if jq fails or field missing
if command -v jq &> /dev/null; then
    PROMPT=$(cat | jq -r '.user_prompt // empty' 2>/dev/null)
fi
PROMPT="${PROMPT:-$CLAUDE_USER_PROMPT}"

# Exit silently if no prompt
[ -z "$PROMPT" ] && exit 0

# Convert to lowercase for matching
PROMPT_LOWER=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

# Check for setup/project triggers
if [[ "$PROMPT_LOWER" == *"setup claude"* ]] || \
   [[ "$PROMPT_LOWER" == *"setup project"* ]] || \
   [[ "$PROMPT_LOWER" == *"initialise claude"* ]] || \
   [[ "$PROMPT_LOWER" == *"initialize claude"* ]] || \
   [[ "$PROMPT_LOWER" == *"new project"* ]]; then
    echo "<skill-reminder>"
    echo "SKILL DETECTED: setup-uk-project"
    echo "Location: ~/.claude/skills/setup-uk-project/ OR .claude/skills/setup-uk-project/"
    echo "READ AND FOLLOW the SKILL.md instructions before proceeding."
    echo "</skill-reminder>"
fi

# Check for design review triggers
if [[ "$PROMPT_LOWER" == *"design review"* ]] || \
   [[ "$PROMPT_LOWER" == *"visual review"* ]] || \
   [[ "$PROMPT_LOWER" == *"ui review"* ]]; then
    echo "<skill-reminder>"
    echo "SKILL DETECTED: design-review"
    echo "Use the design-reviewer agent with Playwright screenshots."
    echo "</skill-reminder>"
fi
