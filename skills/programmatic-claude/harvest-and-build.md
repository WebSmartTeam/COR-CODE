# Website Harvest and Build Automation

Automated pipeline for cloning websites using programmatic Claude Code.

## The Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   HARVEST   │ -> │   ANALYSE   │ -> │    BUILD    │ -> │  VALIDATE   │
│  Firecrawl  │    │  Claude -p  │    │ Claude SDK  │    │  Playwright │
│  + Chrome   │    │  JSON out   │    │  Full tools │    │  Compare    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Phase 1: Harvest (Data Collection)

Scrape the source website for content, structure, and design.

### Using Firecrawl MCP
```bash
# Map all URLs on the site
claude -p "Map all URLs on https://example.com" \
  --allowedTools "mcp__firecrawl__firecrawl_map" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"urls":{"type":"array","items":{"type":"string"}}}}'
```

### Using Chrome for Screenshots
```bash
# Capture visual reference (requires claude --chrome)
claude -p "Navigate to https://example.com and take a full-page screenshot, save to ./harvest/homepage.png" \
  --allowedTools "mcp__puppeteer__*,Write"
```

### Harvest Script (Node.js)
```javascript
import { query } from "@anthropic-ai/claude-agent-sdk";
import { writeFileSync } from "fs";

async function harvestSite(url) {
  const harvest = {
    url,
    pages: [],
    assets: [],
    designTokens: {}
  };

  // Step 1: Map all pages
  for await (const msg of query({
    prompt: `Map all URLs on ${url} and return as JSON`,
    options: {
      allowedTools: ["mcp__firecrawl__firecrawl_map"],
      outputFormat: {
        type: "json_schema",
        schema: {
          type: "object",
          properties: {
            urls: { type: "array", items: { type: "string" } }
          }
        }
      }
    }
  })) {
    if (msg.type === "result" && msg.structured_output) {
      harvest.pages = msg.structured_output.urls;
    }
  }

  // Step 2: Scrape each page
  for (const pageUrl of harvest.pages.slice(0, 10)) {
    for await (const msg of query({
      prompt: `Scrape ${pageUrl} and extract: title, meta description, headings, main content, navigation links`,
      options: {
        allowedTools: ["mcp__firecrawl__firecrawl_scrape"],
        outputFormat: {
          type: "json_schema",
          schema: {
            type: "object",
            properties: {
              title: { type: "string" },
              description: { type: "string" },
              headings: { type: "array", items: { type: "string" } },
              content: { type: "string" },
              navLinks: { type: "array", items: { type: "object" } }
            }
          }
        }
      }
    })) {
      if (msg.type === "result" && msg.structured_output) {
        harvest.assets.push({
          url: pageUrl,
          ...msg.structured_output
        });
      }
    }
  }

  // Step 3: Extract design tokens
  for await (const msg of query({
    prompt: `Scrape ${url} with 'branding' format to extract colours, fonts, and spacing`,
    options: {
      allowedTools: ["mcp__firecrawl__firecrawl_scrape"]
    }
  })) {
    // Parse branding data
  }

  writeFileSync("./harvest/site-data.json", JSON.stringify(harvest, null, 2));
  return harvest;
}
```

## Phase 2: Analyse (AI Processing)

Process harvested data into build specifications.

### Generate Component Specs
```bash
claude -p "Analyse ./harvest/site-data.json and create component specifications for a Next.js rebuild. Include: component names, props, styling requirements, content slots." \
  --allowedTools "Read" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"components":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"props":{"type":"array"},"styling":{"type":"object"},"content":{"type":"string"}}}}}}'
```

### Create Content Inventory
```bash
claude -p "Create a content inventory from ./harvest/site-data.json. List all pages with their: title, URL slug, content sections, images needed, CTAs." \
  --allowedTools "Read" \
  --output-format json > ./harvest/content-inventory.json
```

### Design Token Extraction
```bash
claude -p "Extract design tokens from the harvested branding data. Output as CSS custom properties and Tailwind config." \
  --allowedTools "Read" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"cssVariables":{"type":"object"},"tailwindColors":{"type":"object"},"tailwindFonts":{"type":"object"}}}'
```

## Phase 3: Build (Code Generation)

Generate the new site using Claude with full tool access.

### Python SDK Build Script
```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
import asyncio
import json

async def build_site():
    # Load specifications
    with open("./harvest/component-specs.json") as f:
        specs = json.load(f)

    with open("./harvest/content-inventory.json") as f:
        content = json.load(f)

    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Edit", "Bash", "Glob"],
        permission_mode="acceptEdits",
        cwd="./new-site",
        system_prompt={
            "type": "preset",
            "preset": "claude_code",
            "append": """You are building a Next.js 15 website.
Use Tailwind CSS for styling.
Follow UK English standards.
Deploy to Vercel London region (lhr1).
Create production-ready, accessible code."""
        }
    )

    async with ClaudeSDKClient(options=options) as client:
        # Step 1: Create project structure
        await client.query("""
Create a Next.js 15 project with:
- App Router
- TypeScript
- Tailwind CSS
- UK standards

Run: npx create-next-app@latest . --typescript --tailwind --app --no-eslint
Then configure for UK deployment.
""")
        async for msg in client.receive_response():
            print(f"Setup: {msg}")

        # Step 2: Apply design tokens
        await client.query(f"""
Apply these design tokens to tailwind.config.ts:
{json.dumps(specs.get('designTokens', {}))}

Create a globals.css with CSS custom properties.
""")
        async for msg in client.receive_response():
            print(f"Tokens: {msg}")

        # Step 3: Generate components
        for component in specs.get('components', []):
            await client.query(f"""
Create component: {component['name']}
Props: {json.dumps(component.get('props', []))}
Styling: {json.dumps(component.get('styling', {}))}

Save to src/components/{component['name']}.tsx
Include TypeScript types and accessibility attributes.
""")
            async for msg in client.receive_response():
                print(f"Component {component['name']}: created")

        # Step 4: Generate pages
        for page in content.get('pages', []):
            await client.query(f"""
Create page: {page['title']}
Route: /app/{page['slug']}/page.tsx
Content sections: {json.dumps(page.get('sections', []))}

Use the components we created. Include proper metadata for SEO.
""")
            async for msg in client.receive_response():
                print(f"Page {page['title']}: created")

asyncio.run(build_site())
```

### CLI Build Alternative
```bash
# Chain commands with session continuity
session_id=$(claude -p "Create Next.js 15 project in ./new-site with TypeScript and Tailwind" \
  --allowedTools "Bash,Write" \
  --output-format json | jq -r '.session_id')

claude -p "Apply design tokens from ./harvest/design-tokens.json to tailwind.config.ts" \
  --resume "$session_id" \
  --allowedTools "Read,Write,Edit"

claude -p "Generate all components from ./harvest/component-specs.json" \
  --resume "$session_id" \
  --allowedTools "Read,Write"

claude -p "Generate all pages from ./harvest/content-inventory.json" \
  --resume "$session_id" \
  --allowedTools "Read,Write"
```

## Phase 4: Validate (Quality Check)

Compare the new build against the original.

### Visual Comparison
```bash
# Start dev server in background
cd ./new-site && npm run dev &

# Screenshot new build
claude -p "Navigate to http://localhost:3000 and take full-page screenshot, save to ./validation/new-homepage.png" \
  --allowedTools "mcp__puppeteer__*,Write"

# Compare with original
claude -p "Compare ./harvest/homepage.png with ./validation/new-homepage.png. Identify visual differences in: layout, colours, typography, spacing. Rate similarity 0-100." \
  --allowedTools "Read" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"similarity":{"type":"number"},"differences":{"type":"array","items":{"type":"string"}},"recommendations":{"type":"array","items":{"type":"string"}}}}'
```

### Accessibility Audit
```bash
claude -p "Run accessibility audit on http://localhost:3000 using Playwright. Check WCAG 2.1 AA compliance." \
  --allowedTools "Bash,Read,Write" \
  --output-format json
```

### Self-Correction Loop
```python
async def validate_and_correct():
    async with ClaudeSDKClient(options) as client:
        max_iterations = 5

        for i in range(max_iterations):
            # Take screenshot and compare
            await client.query("""
1. Screenshot http://localhost:3000
2. Compare with ./harvest/homepage.png
3. If similarity < 90%, identify top 3 differences
4. Fix the most impactful difference
5. Report what was changed
""")
            async for msg in client.receive_response():
                if "similarity" in str(msg) and "100" in str(msg):
                    print("Validation complete - sites match!")
                    return
                print(f"Iteration {i+1}: {msg}")

        print("Max iterations reached")
```

## Complete Orchestration Script

```python
#!/usr/bin/env python3
"""
Website Harvest and Build Pipeline
Usage: python harvest_and_build.py https://example.com ./output-dir
"""

import asyncio
import sys
from pathlib import Path

async def main():
    source_url = sys.argv[1]
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"🌐 Harvesting: {source_url}")
    harvest_data = await harvest_site(source_url, output_dir / "harvest")

    print("📊 Analysing content and design...")
    specs = await analyse_harvest(output_dir / "harvest")

    print("🔨 Building new site...")
    await build_site(specs, output_dir / "new-site")

    print("✅ Validating build...")
    result = await validate_build(
        original_url=source_url,
        new_site_dir=output_dir / "new-site"
    )

    print(f"Similarity: {result['similarity']}%")
    if result['similarity'] >= 90:
        print("🎉 Build successful!")
    else:
        print("⚠️ Manual review recommended")
        print("Differences:", result['differences'])

if __name__ == "__main__":
    asyncio.run(main())
```

## Integration with COR-CODE Skills

This workflow integrates with existing skills:

- **site-harvest**: Use for the harvest phase with Firecrawl
- **web-frontend**: Apply frontend standards during build
- **design-reviewer**: Use for visual validation
- **vercel-deployment**: Deploy the final build

## Output Structure

```
output-dir/
├── harvest/
│   ├── site-data.json          # Raw scraped content
│   ├── component-specs.json    # Generated component specs
│   ├── content-inventory.json  # Page content mapping
│   ├── design-tokens.json      # Extracted design system
│   └── screenshots/            # Visual references
├── new-site/
│   ├── src/
│   │   ├── components/         # Generated components
│   │   └── app/                # Generated pages
│   ├── tailwind.config.ts      # Design tokens applied
│   └── package.json
└── validation/
    ├── comparison-report.json  # Visual diff results
    └── screenshots/            # New site screenshots
```

## Best Practices

1. **Rate limiting**: Add delays between Firecrawl requests
2. **Error handling**: Wrap each phase in try/catch
3. **Incremental saves**: Save progress after each step
4. **Manual review points**: Add human checkpoints for critical decisions
5. **Version control**: Commit after each successful phase
6. **Logging**: Track all Claude interactions for debugging
