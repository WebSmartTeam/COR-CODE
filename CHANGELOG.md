# COR-CODE Changelog

All notable changes to this project are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).

---

## [1.0.6] - 2025-01-23

### Added

**Skills:**
- `ultraplan/` - Deep architectural planning with --ultrathink (32K tokens) + phased execution with fresh 200K context
  - Two-stage workflow: UltraPlan creates PHASES.md, then Execute runs each phase cleanly
  - Project type agnostic - works for any complex build needing phases
  - Replaced deprecated `saas-phase-builder`

**Hooks:**
- `setup-detector.sh` - Project initialisation via `claude --init` (Claude Code 2.1.10+)
  - Detects if CLAUDE.md exists
  - Prompts for project type, name, and existing git URL
  - Triggers `new-and-imported-projects` skill

**Skill Detection:**
- Added ultraplan triggers: "ultraplan", "plan phases", "deep plan", "execute phase"
- Added non-stop triggers: "non-stop", "autonomous mode", "keep going"

### Changed

**Core Principles:**
- Added "No Cost-Based Decisions" principle to `global-claude/CLAUDE.md`
- Claude must never factor pricing/affordability into recommendations
- Assume user has subscriptions, recommend RIGHT solution not cheapest

### Removed

- `saas-phase-builder/` skill (replaced by `ultraplan`)

---

## [1.0.5] - 2025-01-17

### Added

**References:**
- `references/anthropic-official-docs.md` - Tracked URLs for official Anthropic documentation
- All docs available as .md at `https://code.claude.com/docs/en/*.md`
- Timestamped for tracking when last verified

### Improved

**All Skills** - Updated descriptions with "What + When + Triggers" formula:
- Proper frontmatter on all SKILL.md files
- Trigger terms for better Claude matching
- Consistent naming (fixed mismatches)

---

## [1.0.4] - 2025-01-17

### Added

**Skills:**
- `programmatic-claude/` - Run Claude Code via CLI, Python SDK, or TypeScript SDK
- `harvest-and-build.md` - Website cloning automation pipeline (Firecrawl → Analyse → Build → Validate)
- Session chaining patterns with `--resume` for multi-phase orchestration
- Custom tools, MCP integration, and structured JSON output examples

---

## [1.0.3] - 2025-01-17

### Added

**Output Styles:**
- `ai-first-builder.md` - Autonomous AI-first development with evidence-based execution
- `autonomous-executor.md` - Self-directed execution mode, work until complete
- Both include "Banned Patterns" section (no fallbacks, no hedging, no legacy)

---

## [1.0.2] - 2025-01-17

### Added

**Output Styles:**
- `output-styles/` folder with README and documentation
- `uk-professional.md` - British English, formal communication, enterprise standards
- Comprehensive comparison of Output Styles vs CLAUDE.md vs Agents vs Skills

**Documentation:**
- Updated main README with all five component types
- "Understanding the Components" section with clear distinctions
- Added output-styles to Quick Start installation

---

## [1.0.1] - 2025-01-17

### Added

**Documentation:**
- Skills vs Agents vs MCP explanation in main README
- Clarified relationship between the three core concepts
- Added comparison table to skills/README.md

### Changed

- Renamed `context/` folder to `global-claude/` for clarity
- Updated all READMEs with global vs local configuration guidance

---

## [1.0.0] - 2025-01-17

### Added

**Global Claude:**
- `CLAUDE.md` - Global configuration template with placeholders
- `README.md` - Installation and customisation instructions

**Skills:**
- `feature-dev` - 7-phase feature development workflow with visual validation
- `contact-form-builder` - AWS SES contact forms with reCAPTCHA v3
- `site-harvest` - Website content and design extraction using Firecrawl
- `web-frontend` - Frontend preferences, pet hates, and performance targets
- `seo-skill` - Technical SEO patterns and structured data
- `non-stop` - Autonomous development mode with Chrome DevTools validation
- `vercel-deployment` - UK-first Vercel deployment with security patches
- `phase-checkpoint` - Verification checkpoint between build phases
- `project-discovery` - Guided project discovery before implementation
- `skill-building` - Meta-skill for creating effective skills

**Agents:**
- `frontend` - UI/UX specialist with accessibility focus
- `backend` - Reliability engineer and API specialist
- `security` - Threat modeling and vulnerability assessment
- `performance` - Optimisation and bottleneck elimination
- `architect` - Systems design and scalability
- `qa` - Quality assurance and testing
- `refactorer` - Code quality and technical debt
- `scribe` - Documentation with UK English standards
- `mentor` - Educational guidance and knowledge transfer
- `devops` - Infrastructure and deployment automation
- `analyzer` - Root cause analysis and investigation
- `design-reviewer` - Visual UI assessment using Playwright

**Hooks:**
- Pre-tool validation for security and quality
- Post-tool quality checks and UK compliance

**Documentation:**
- Comprehensive README with installation instructions
- Skill-specific README files
- Agent capability documentation

### Security
- All personal data replaced with placeholders
- Security validation checklist for contributions
- No hardcoded credentials or API keys

---

## Version History

| Version | Date | Summary |
|---------|------|---------|
| 1.0.6 | 2025-01-23 | UltraPlan skill, setup hook, no-cost-decisions principle |
| 1.0.5 | 2025-01-17 | References folder, improved skill descriptions |
| 1.0.4 | 2025-01-17 | Programmatic Claude skill for CLI/SDK automation |
| 1.0.3 | 2025-01-17 | AI-first and autonomous executor output styles |
| 1.0.2 | 2025-01-17 | Added output-styles folder with UK professional style |
| 1.0.1 | 2025-01-17 | Documentation improvements: Skills vs Agents vs MCP |
| 1.0.0 | 2025-01-17 | Initial release with skills, agents, and hooks |
