---
description: Verification checkpoint between build phases - confirms before proceeding
allowed_tools:
  - Read
  - Bash
  - TodoWrite
---

# Phase Checkpoint

**Purpose**: Pause for human verification before proceeding to next phase. Quality gate.

## When to Use

Call this skill at the end of each major phase:
- After Foundation setup
- After Auth implementation
- After Core features
- After Payments integration
- Before deployment

## Checkpoint Process

### 1. Summary of Completed Work
List what was built this phase:
- Features implemented
- Files created/modified
- Commits made
- Tests passing

### 2. Verification Steps
Guide human through testing:
```bash
# Start dev server
npm run dev

# Check these URLs:
# - http://localhost:3000 (or 3001)
# - http://localhost:3000/auth/login
# - http://localhost:3000/dashboard
```

### 3. Checklist
Present verification checklist:
- [ ] UI renders correctly
- [ ] No console errors
- [ ] Core functionality works
- [ ] Auth flow complete (if applicable)
- [ ] Data persists to database (if applicable)
- [ ] Responsive on mobile

### 4. Decision Point
Ask human:
> **Phase [X] Complete. Ready to proceed to Phase [X+1]?**
>
> Options:
> 1. ✅ Approved - Continue to next phase
> 2. 🔧 Fix issues - [describe what's wrong]
> 3. ⏸️ Pause - Save state, continue later

### 5. State Update
Based on response:
- **Approved**: Update TodoWrite, proceed
- **Fix issues**: Address problems, re-verify
- **Pause**: Update STATE.md with current position

## Example Checkpoint Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 PHASE 2 CHECKPOINT: Database & Auth
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Completed:
   • Supabase project connected
   • User profiles table created
   • RLS policies applied
   • Sign up / Sign in / Sign out working
   • Protected dashboard route

🧪 Verify:
   1. Go to http://localhost:3000
   2. Click "Sign Up" - create test account
   3. Check email for confirmation
   4. Confirm and verify redirect to dashboard
   5. Check Supabase → Auth → Users (should see new user)
   6. Click "Sign Out" - verify redirect to home

📝 Commits:
   • feat: Add Supabase auth configuration
   • feat: Create user profiles schema
   • feat: Implement auth UI components

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ready to proceed to Phase 3: Core Features?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Why Checkpoints Matter

From GSD methodology:
> "You can't screw this part up. We have to make sure payments work properly. That's why we're taking so much time here."

Verification prevents:
- Building on broken foundations
- Deploying broken functionality
- Wasting time on features that don't work
- Context rot from debugging old issues
