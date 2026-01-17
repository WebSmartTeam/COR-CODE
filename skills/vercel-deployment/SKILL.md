---
name: vercel-deployment
description: Deploy UK projects to Vercel using git-based workflow (never CLI deploy). Always London region (lhr1), dynamic version checking via Context7. Includes security headers and pre-deployment checklist. Triggers: deploy, vercel, publish, go live, push to production, hosting, deploy to vercel, vercel deployment.
---

# Vercel Deployment - UK Standards

**Trigger**: "deploy to vercel", "vercel deployment", "setup vercel"

## 🚨 CRITICAL: NO HARDCODED VERSIONS

**This skill contains PRINCIPLES and PROCESSES, not specific versions.**

Before ANY deployment work:
1. **Use Context7 MCP** to check latest compatible versions of Next.js, React, Tailwind
2. **Use WebSearch** to check for recent security patches and CVEs
3. **Check Vercel Dashboard** for platform defaults (Node.js version, regions)
4. **NEVER use version numbers from memory** - always verify current state

```
# Example Context7 usage
"Use Context7 to check latest stable Next.js version and React compatibility"
"Use Context7 to check Tailwind CSS compatibility with current Next.js version"
```

## 🚀 CORE PRINCIPLE: Git-Based Deployment ONLY

**Vercel pulls from git. We NEVER deploy direct.**

```
Push to git → Vercel detects → Vercel builds → Vercel deploys

❌ NEVER use: vercel deploy, vercel --prod, vercel CLI for deployment
✅ ALWAYS use: git push (Vercel auto-deploys)
```

### Why Git-Based?
- **Source of truth**: Git history = deployment history
- **Reproducible**: Any commit can be redeployed
- **Preview deployments**: PRs get automatic preview URLs
- **Rollback**: Revert commit = rollback deployment
- **Team workflow**: Standard git flow, no special CLI knowledge needed

## 🇬🇧 UK Standards (Mandatory)

- **Language**: UK English throughout (realise, colour, centre)
- **Date format**: DD/MM/YYYY in UI
- **Timezone**: GMT/BST
- **Currency**: GBP (£) where applicable
- **Region preference**: London (lhr1) - but check Vercel dashboard for how to set this

### Region Configuration
**⚠️ CHECK VERCEL DOCUMENTATION** for current best practice on region configuration:
- Vercel may set region at project level in dashboard
- Or may use vercel.json - verify current approach
- Use Context7 or WebSearch: "Vercel region configuration 2026"

## 🔒 Security Headers (Principles)

These security header PATTERNS are relatively stable, but verify current best practices:

```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
Content-Security-Policy: [project-specific - don't copy blindly]
```

**⚠️ CSP must be tailored per project** - depends on what external resources you use.

## 📦 Package Setup Process

### Step 1: Check Current Versions
```bash
# Use Context7 to find latest compatible versions
"What are the latest stable versions of Next.js, React, and their compatibility?"

# Or WebSearch
"Latest stable Next.js React Tailwind versions January 2026"
```

### Step 2: Check for Security Patches
```bash
# WebSearch for recent CVEs
"React Next.js security vulnerabilities 2026"
"Next.js CVE patches latest"
```

### Step 3: Check Vercel Platform Defaults
- Go to Vercel Dashboard → Project Settings
- Check default Node.js version
- Check default build settings
- Check region settings

### Step 4: Create package.json
Use versions discovered in Steps 1-3, NOT from memory or this skill.

## 🚀 Deployment Workflow

### First Time Setup (Vercel Dashboard) - User Completes This Step
1. Go to vercel.com/new
2. Import Git Repository (webSmartTeam organisation)
3. Select the repository
4. Configure:
   - Framework: Auto-detected
   - Root Directory: ./ (or subdirectory if monorepo)
   - Build Command: Usually default is fine
   - Output Directory: Usually default is fine
5. Set region preference in project settings if needed
6. Add Environment Variables
7. Deploy

### Ongoing Deployments
```bash
# Make changes
git add .
git commit -m "feat: Add new feature"
git push origin main

# Vercel automatically:
# 1. Detects the push
# 2. Pulls the code
# 3. Runs build
# 4. Deploys to production (main branch) or preview (other branches)
```

## ✅ Pre-Deployment Checklist

### Version Verification (USE CONTEXT7/WEBSEARCH)
- [ ] Check latest stable framework versions
- [ ] Check for recent security patches
- [ ] Verify version compatibility (Next.js ↔ React ↔ Tailwind)
- [ ] Check Vercel platform defaults

### Security
- [ ] Security headers configured
- [ ] CSP tailored to project needs
- [ ] No secrets in code
- [ ] Environment variables in Vercel dashboard

### UK Standards
- [ ] UK English throughout
- [ ] Date format: DD/MM/YYYY
- [ ] Region set to London (via Vercel dashboard or config)

## 🚨 Security Patch Process

When security vulnerabilities are discovered:

1. **WebSearch** for current CVE information and patched versions
2. **Verify** which versions are affected
3. **Update** to patched versions (use Context7 to check compatibility)
4. **Test locally** before pushing
5. **Push to git** (Vercel auto-deploys)
6. **Verify** deployment succeeded

## ⚠️ WHAT THIS SKILL DOES NOT CONTAIN

This skill intentionally does NOT include:
- ❌ Specific version numbers (they become outdated)
- ❌ Hardcoded Node.js versions
- ❌ Hardcoded framework versions
- ❌ Specific CVE numbers (check current state instead)
- ❌ IP addresses or URLs that might change

**WHY**: Hardcoded values in skills cause Claude to use outdated information even when told otherwise. Always check current state using Context7, WebSearch, or Vercel dashboard.

## 📚 Dynamic References

Instead of hardcoded links, search for:
- "Vercel documentation deployment"
- "Next.js security advisories"
- "React security patches"
- "Tailwind CSS compatibility Next.js"
