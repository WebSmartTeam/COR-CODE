---
name: non-stop
description: Work autonomously until task is complete with self-correction loop. No questions asked - makes decisions based on evidence (console errors, screenshots, test results). Use when you want continuous uninterrupted work. Triggers: non-stop, don't stop, work until done, autonomous mode, keep going, work autonomously, no questions.
updated: 2025-01-18
compatibility: Requires `claude --chrome` or `claude --chrome --resume` for console errors and screenshots
user-invocable: true
---

# Non-Stop Mode Skill

**Trigger**: User says "non-stop mode", "use non-stop", "work autonomously", "don't stop until done"

**Max Iterations**: 10 (default) - safety net to prevent infinite loops. User can specify: "non-stop mode --max 20"

## What This Mode Does

Fully autonomous development loop with quality validation. Claude works until genuinely complete - not just "todos marked done" but quality-verified complete.

## The Loop

```
1. Create/read todos for the task
2. Work on todos, mark complete as done
3. Quality check with chrome devtools:
   - Check console for errors
   - Take screenshots
   - Verify functionality works
4. If issues found:
   - Create new todos for issues
   - Update existing todos with findings
   - Loop back to step 2
5. Only COMPLETE when:
   - All todos done AND
   - No console errors AND
   - Screenshots show expected result AND
   - Functionality verified
   OR max iterations reached (report status + remaining issues)
```

## Critical Rules

**NEVER ASK HUMAN QUESTIONS IN THIS MODE**

- Don't ask "which approach?" → Pick one based on evidence
- Don't ask "should I continue?" → Continue until quality-verified
- Don't ask "is this acceptable?" → Validate with tools, not questions
- Don't ask "do you want X or Y?" → Decide and execute

**Make autonomous decisions based on:**
- Error messages and logs
- Test results
- Console output (chrome devtools)
- Screenshot evidence
- Code analysis

## Tools Used (existing only - no extra costs)

- **TodoWrite**: Track progress, record findings, manage iterations
- **Chrome DevTools MCP**: Console errors, network issues, screenshots
- **Playwright** (if needed): E2E validation, visual checks
- **Standard Claude tools**: Read, Write, Edit, Bash, Grep, Glob

## Starting Non-Stop Mode

When activated, Claude should:

1. **Understand the task** - Read any provided context
2. **Break into todos** - Create structured task list with TodoWrite
3. **Execute autonomously** - Work through todos without asking
4. **Validate with evidence** - Use chrome devtools to verify quality
5. **Self-correct** - Create new todos for any issues found
6. **Loop until clean** - Only stop when quality-verified complete

## Completion Criteria

Non-stop mode ends when ALL are true:
- [ ] All todos marked complete
- [ ] Console shows no errors (chrome devtools check)
- [ ] Screenshots match expected result
- [ ] Any tests pass (if applicable)
- [ ] No obvious issues in code review

**OR** max iterations (default 10) reached - then report:
- What was completed
- What remains incomplete
- Current blockers/issues
- Recommended next steps

## Example Usage

```
User: "Build a contact form for the website. Use non-stop mode."

Claude activates non-stop:
1. Creates todos: form component, validation, submission, styling, testing
2. Implements form component
3. Marks todo complete
4. Checks chrome devtools - sees console error "undefined handler"
5. Creates new todo: "Fix undefined handler error"
6. Fixes error
7. Checks again - console clean
8. Takes screenshot - form looks broken on mobile
9. Creates new todo: "Fix mobile responsive layout"
10. Fixes layout
11. Final check - console clean, screenshot good, form submits
12. COMPLETE
```

## Escaping Non-Stop Mode

User can interrupt at any time with:
- "stop"
- "pause"
- "wait"
- Any direct question requiring human decision

Otherwise, Claude continues until quality-verified complete.
