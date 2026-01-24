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

# Check for ultraplan/phase planning triggers
if [[ "$PROMPT_LOWER" == *"ultraplan"* ]] || \
   [[ "$PROMPT_LOWER" == *"plan phases"* ]] || \
   [[ "$PROMPT_LOWER" == *"phase planning"* ]] || \
   [[ "$PROMPT_LOWER" == *"deep plan"* ]] || \
   [[ "$PROMPT_LOWER" == *"strategic plan"* ]] || \
   [[ "$PROMPT_LOWER" == *"architect plan"* ]] || \
   [[ "$PROMPT_LOWER" == *"create phase"* ]] || \
   [[ "$PROMPT_LOWER" == *"run phase"* ]]; then
    echo "<skill-reminder>"
    echo "SKILL DETECTED: ultraplan"
    echo "Location: ~/.claude/skills/ultraplan/SKILL.md"
    echo "TWO-STAGE WORKFLOW:"
    echo "1. UltraPlan: --ultrathink (32K) for deep planning → PHASES.md"
    echo "2. Create: Fresh 200K context per phase → Maximum quality"
    echo "Use for complex builds needing architectural thinking."
    echo "</skill-reminder>"
fi

# Check for non-stop/autonomous mode triggers
if [[ "$PROMPT_LOWER" == *"non-stop"* ]] || \
   [[ "$PROMPT_LOWER" == *"nonstop"* ]] || \
   [[ "$PROMPT_LOWER" == *"don't stop"* ]] || \
   [[ "$PROMPT_LOWER" == *"dont stop"* ]] || \
   [[ "$PROMPT_LOWER" == *"work until done"* ]] || \
   [[ "$PROMPT_LOWER" == *"autonomous mode"* ]] || \
   [[ "$PROMPT_LOWER" == *"work autonomously"* ]] || \
   [[ "$PROMPT_LOWER" == *"keep going"* ]]; then
    echo "<skill-reminder>"
    echo "SKILL DETECTED: non-stop"
    echo "Location: ~/.claude/skills/non-stop/SKILL.md"
    echo "CRITICAL RULES:"
    echo "- NEVER ask questions - make autonomous decisions"
    echo "- Use TodoWrite to track progress"
    echo "- Validate with chrome devtools (console errors, screenshots)"
    echo "- Loop until quality-verified complete (max 10 iterations)"
    echo "- Only stop when: todos done + no errors + screenshots good"
    echo "</skill-reminder>"
fi
