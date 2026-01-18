---
name: contact-form-builder-ses
description: Build AWS SES email features with reCAPTCHA v3, Zod validation, XSS sanitisation, and rate limiting. Uses placeholders until env vars added to Vercel. Dual emails (owner + customer confirmation). Triggers: contact form, email form, enquiry form, ses email, newsletter signup, booking form, callback request.
updated: 2025-01-18
---

# AWS SES Contact Form Builder

**Purpose**: Contact forms and email features using AWS SES. Works with placeholders during development - add env vars to Vercel when ready to go live.

## When to Use

- "create a contact form"
- "add email functionality"
- "build enquiry form"
- "newsletter signup"
- "callback request form"
- "booking request with email"
- Any feature sending email from website

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  React Form     │────▶│  API Route      │────▶│  AWS SES        │
│  + reCAPTCHA v3 │     │  + Validation   │     │  (eu-west-1)    │
└─────────────────┘     │  + Sanitisation │     └────────┬────────┘
                        │  + Rate Limit   │              │
                        └─────────────────┘              ▼
                                                 ┌──────────────┐
                                                 │ DUAL EMAILS  │
                                                 │ 1. Owner     │
                                                 │ 2. Customer  │
                                                 └──────────────┘
```

## Placeholder Reference

Use these placeholders throughout - Claude MUST ask user to provide values:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{COMPANY_NAME}}` | Business name | "Acme Solutions Ltd" |
| `{{COMPANY_PHONE}}` | Phone number | "01234 567890" |
| `{{COMPANY_ADDRESS}}` | Full address | "123 High Street, London, SW1A 1AA" |
| `{{COMPANY_NUMBER}}` | Company registration | "12345678" |
| `{{WEBSITE_URL}}` | Main website URL | "https://example.co.uk" |
| `{{OWNER_EMAIL}}` | Where notifications go | "enquiries@example.co.uk" |
| `{{FROM_EMAIL}}` | SES verified sender | "noreply@example.co.uk" |
| `{{FROM_NAME}}` | Sender display name | "Acme Solutions" |
| `{{PRIMARY_COLOR}}` | Brand primary colour | "#192a37" |
| `{{SECONDARY_COLOR}}` | Brand secondary colour | "#899759" |
| `{{ACCENT_COLOR}}` | Accent/CTA colour | "#ff5101" |
| `{{LOGO_URL}}` | Logo image URL (optional) | "/images/logo.png" |

## What to Ask User

**MANDATORY before building:**

1. **Company Details**
   - Company name
   - Phone number
   - Address
   - Company number (if displaying)
   - Website URL

2. **Email Configuration**
   - Owner notification email (where enquiries go)
   - From email (must be SES verified)
   - From display name

3. **Brand Colours**
   - Primary colour (headers, backgrounds)
   - Secondary colour (accents, highlights)
   - Accent colour (CTAs, links)

4. **Form Fields Needed**
   - Which fields? (name, email, phone, subject, message, etc.)
   - Which are required?
   - Any special validation? (min length, formats)

5. **Personality/Tone**
   - Formal, friendly, or witty?
   - This affects email greetings and copy

## Technology Stack (Non-Negotiable)

| Component | Technology | Why |
|-----------|------------|-----|
| Email delivery | AWS SES | Reliable, GDPR compliant (eu-west-1) |
| Spam protection | reCAPTCHA v3 | Invisible, score-based |
| Input validation | Zod | Type-safe, comprehensive |
| XSS prevention | DOMPurify | Industry standard sanitisation |
| Rate limiting | @upstash/ratelimit | Redis-based, serverless |
| Form state | React Hook Form | Performance, validation integration |

## Critical Implementation Rules

### 1. reCAPTCHA v3 Loading (MUST USE)
```typescript
// ✅ CORRECT - loads before form submit
<Script
  src={`https://www.google.com/recaptcha/api.js?render=${siteKey}`}
  strategy="afterInteractive"
/>

// ❌ WRONG - causes timeout errors
strategy="lazyOnload"  // NEVER use this
```

### 2. Dual Email (ALWAYS SEND BOTH)
Every form submission MUST send TWO emails:
1. **Owner notification** - Full details with reply-to set to customer
2. **Customer confirmation** - Thank you with summary of their message

Never send just one. This is enterprise standard.

### 3. Email Template Rules
```html
<!-- ✅ CORRECT - table layout for Outlook -->
<table style="background-color: {{PRIMARY_COLOR}};">

<!-- ❌ WRONG - breaks in Outlook -->
<div style="display: flex;">
```

- Use TABLE layouts (not flexbox/grid)
- Inline ALL CSS (no external stylesheets)
- Add solid colour BEFORE gradients (fallback)
- Test in Gmail, Outlook, Apple Mail

### 4. Validation Chain
```
User Input → Zod Schema → DOMPurify Sanitise → Safe Data → Send Email
```

Never skip any step. See SECURITY.md for full implementation.

### 5. Rate Limiting
```typescript
// Default: 5 requests per hour per IP
const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(5, '1 h'),
})
```

## File Structure to Create

```
src/
├── app/
│   ├── contact/
│   │   ├── page.tsx              # Contact page with form
│   │   └── metadata.ts           # SEO metadata
│   └── api/
│       └── contact/
│           └── route.ts          # API handler
├── components/
│   └── ContactForm.tsx           # Reusable form component
└── lib/
    ├── validation.ts             # Zod schemas
    ├── sanitize.ts               # DOMPurify helpers
    ├── ratelimit.ts              # Rate limiting setup
    └── env.ts                    # Environment validation
```

## Environment Variables

```bash
# AWS SES (REQUIRED)
AWS_REGION=eu-west-1
AWS_ACCESS_KEY_ID={{ASK_USER}}
AWS_SECRET_ACCESS_KEY={{ASK_USER}}

# Email addresses (REQUIRED)
EMAIL_FROM={{FROM_EMAIL}}
EMAIL_FROM_NAME={{FROM_NAME}}
EMAIL_TO={{OWNER_EMAIL}}

# reCAPTCHA v3 (REQUIRED)
NEXT_PUBLIC_RECAPTCHA_SITE_KEY={{ASK_USER}}
RECAPTCHA_SECRET_KEY={{ASK_USER}}

# Rate limiting (REQUIRED for production)
UPSTASH_REDIS_REST_URL={{ASK_USER}}
UPSTASH_REDIS_REST_TOKEN={{ASK_USER}}
```

## Testing Checklist

- [ ] Submit with valid data → success
- [ ] Submit with missing required fields → validation error
- [ ] Submit with XSS payload `<script>alert('xss')</script>` → sanitised
- [ ] Submit 6 times quickly → rate limited on 6th
- [ ] Check owner receives notification email
- [ ] Check customer receives confirmation email
- [ ] Test reply-to works (reply goes to customer)
- [ ] Test emails render correctly in Gmail
- [ ] Test emails render correctly in Outlook
- [ ] Test mobile responsiveness of form

## Common Failures & Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| reCAPTCHA timeout | Wrong script strategy | Use `afterInteractive` |
| White text on white bg | Email gradient stripped | Add solid colour fallback |
| Form accepts `<script>` | No sanitisation | Add DOMPurify |
| 500 error on submit | No validation | Add Zod schema |
| Spam submissions | No rate limiting | Add Upstash ratelimit |
| Only owner OR customer gets email | Forgot dual email | Send BOTH always |
| SES rejects email | Sandbox mode | Request production access |
| Outlook breaks layout | Using flexbox | Use table layout |

## Additional Resources

- **IMPLEMENTATION.md** - Full code templates with placeholders
- **SECURITY.md** - Validation, sanitisation, rate limiting code
- **scripts/** - Copyable code files

## UK Standards (Always Apply)

- UK English spelling (colour, enquiry, organisation)
- eu-west-1 region for GDPR compliance
- British date format (DD/MM/YYYY)
- British phone format (+44)
- Professional business tone
