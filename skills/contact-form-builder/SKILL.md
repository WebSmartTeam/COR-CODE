---
name: ses-contact-form
description: Build contact forms with AWS SES email delivery, reCAPTCHA v3, and branded HTML templates
---

# AWS SES Contact Form Builder

**Purpose**: Professional contact forms with spam protection and dual email delivery (owner notification + customer confirmation).

## When to Use

- "create a contact form"
- "build a contact form with email"
- "add contact form to website"
- Form needing spam protection + email delivery

## Architecture (What We Build)

| Component | Purpose |
|-----------|---------|
| Frontend form | React component with reCAPTCHA v3 |
| Backend API route | Next.js Route Handler |
| Owner notification | Branded HTML email to business |
| Customer confirmation | Branded HTML email to submitter |

**Key decisions already made:**
- AWS SES for email (eu-west-1 for UK/GDPR)
- reCAPTCHA v3 (invisible, score-based)
- Dual emails (always send to BOTH owner AND customer)
- Table-based HTML emails (not CSS Grid/Flexbox - for email client compatibility)

## What to Ask User

1. **Brand colours** (primary, secondary, accent)
2. **Owner email** (notifications go here)
3. **From email** (verified SES sender)
4. **Reply email** (where customer replies go)
5. **Personality** (formal, friendly, witty)
6. **Fields needed** (name, email, phone, subject, message, etc.)

## Implementation Notes

### reCAPTCHA v3
- Load script with `afterInteractive` (NOT `lazyOnload` - must load before form submit)
- Use score threshold 0.5+
- Keep site key in env var but also hardcode in form (timing issues)

### AWS SES
- Use IAM user with SES-only permissions
- Verify sender domain with DKIM
- Request production access (sandbox limits recipients)

### Email Templates
- Always provide solid colour before gradient (email client compatibility)
- Use table layouts (outlook compatibility)
- Inline all CSS
- Test in Gmail, Outlook, Apple Mail

### Dual Emails (CRITICAL)
Every form submission sends TWO emails:
1. **Owner notification** - Full form details + reply-to customer
2. **Customer confirmation** - Thank you + summary of their message

### Validation
- Minimum message length (10 chars typical)
- Email format validation
- Sanitise inputs (XSS/SQL prevention)
- Rate limiting (5/min per IP typical)

## Personality Examples

### Formal
- Badge: "NEW ENQUIRY"
- Greeting: "Dear [Name]"
- Sign-off: "Best regards"

### Friendly
- Badge: "DING DONG!"
- Greeting: "Hey [Name]! 👋"
- Sign-off: "Speak soon"

### Witty
- Badge: "✨ CHEERS!"
- Greeting: "Hey [Name]! 🎉"
- Sign-off: "Chat soon"

## Environment Variables

```bash
# AWS SES
AWS_REGION=eu-west-1
AWS_ACCESS_KEY_ID=[ask user]
AWS_SECRET_ACCESS_KEY=[ask user]
SES_FROM_EMAIL=[verified sender]
SES_TO_EMAIL=[owner notification]

# reCAPTCHA v3
RECAPTCHA_SECRET_KEY=[server key]
NEXT_PUBLIC_RECAPTCHA_SITE_KEY=[client key]
```

## Testing Checklist

- [ ] Submit with valid data (should succeed)
- [ ] Submit with short message (validation should catch)
- [ ] Check owner email received
- [ ] Check customer confirmation received
- [ ] Test gradient rendering in email clients
- [ ] Test reply-to works correctly

## Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| White text on white | Gradient stripped | Add solid colour before gradient |
| reCAPTCHA timeout | Script not loaded | Use `afterInteractive` strategy |
| SES rejected | Sandbox/unverified | Verify domain, request production |

## UK Standards
- Use UK English in all email copy
- eu-west-1 region for GDPR compliance
- British spellings (colour, favourite)
