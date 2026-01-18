# Implementation Templates

Full code templates for email-sending features. Replace all `{{PLACEHOLDER}}` values with user-provided details.

---

## API Route Template

**File**: `src/app/api/contact/route.ts`

```typescript
/**
 * Contact Form API Route
 * Handles form submissions with validation, sanitisation, and dual email delivery
 */

import { NextRequest, NextResponse } from 'next/server'
import { contactFormSchema } from '@/lib/validation'
import { sanitizeContactData } from '@/lib/sanitize'
import { env, getEmailFrom, getEmailFromName, getEmailTo } from '@/lib/env'
import { applyRateLimit, emailRatelimit } from '@/lib/ratelimit'

interface SafeEmailData {
  name: string
  email: string
  phone?: string
  subject: string
  message: string
}

/**
 * Send notification email to owner
 * ALL user input is sanitised to prevent XSS
 */
async function sendOwnerNotification(data: SafeEmailData) {
  const { SESClient, SendEmailCommand } = await import('@aws-sdk/client-ses')

  const client = new SESClient({
    region: env.AWS_REGION,
    credentials: {
      accessKeyId: env.AWS_ACCESS_KEY_ID,
      secretAccessKey: env.AWS_SECRET_ACCESS_KEY,
    },
  })

  const command = new SendEmailCommand({
    Source: `${getEmailFromName()} <${getEmailFrom()}>`,
    Destination: {
      ToAddresses: [getEmailTo()],
    },
    ReplyToAddresses: [data.email], // Reply goes to customer
    Message: {
      Subject: {
        Data: `New Enquiry: ${data.subject}`,
        Charset: 'UTF-8',
      },
      Body: {
        Html: {
          Data: generateOwnerEmailHtml(data),
          Charset: 'UTF-8',
        },
        Text: {
          Data: generateOwnerEmailText(data),
          Charset: 'UTF-8',
        },
      },
    },
  })

  return client.send(command)
}

/**
 * Send confirmation email to customer
 */
async function sendCustomerConfirmation(data: SafeEmailData) {
  const { SESClient, SendEmailCommand } = await import('@aws-sdk/client-ses')

  const client = new SESClient({
    region: env.AWS_REGION,
    credentials: {
      accessKeyId: env.AWS_ACCESS_KEY_ID,
      secretAccessKey: env.AWS_SECRET_ACCESS_KEY,
    },
  })

  const command = new SendEmailCommand({
    Source: `${getEmailFromName()} <${getEmailFrom()}>`,
    Destination: {
      ToAddresses: [data.email],
    },
    Message: {
      Subject: {
        Data: `Thank you for contacting {{COMPANY_NAME}}`,
        Charset: 'UTF-8',
      },
      Body: {
        Html: {
          Data: generateCustomerEmailHtml(data),
          Charset: 'UTF-8',
        },
        Text: {
          Data: generateCustomerEmailText(data),
          Charset: 'UTF-8',
        },
      },
    },
  })

  return client.send(command)
}

/**
 * Verify reCAPTCHA v3 token
 */
async function verifyRecaptcha(token: string): Promise<boolean> {
  try {
    const response = await fetch('https://www.google.com/recaptcha/api/siteverify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `secret=${env.RECAPTCHA_SECRET_KEY}&response=${token}`,
    })

    const data = await response.json()
    return data.success && data.score >= 0.5
  } catch {
    return false
  }
}

/**
 * POST handler
 */
export async function POST(request: NextRequest) {
  try {
    // 1. Rate limiting
    const rateLimitResult = await applyRateLimit(request, emailRatelimit)
    if (!rateLimitResult.success) {
      return rateLimitResult.response!
    }

    // 2. Parse and validate
    const body = await request.json()
    const validationResult = contactFormSchema.safeParse(body)

    if (!validationResult.success) {
      return NextResponse.json(
        { error: 'Invalid input', details: validationResult.error.issues },
        { status: 400 }
      )
    }

    // 3. Sanitise (XSS protection)
    const sanitizedData = sanitizeContactData(validationResult.data)

    // 4. Verify reCAPTCHA
    const isValidRecaptcha = await verifyRecaptcha(validationResult.data.recaptchaToken)
    if (!isValidRecaptcha) {
      return NextResponse.json(
        { error: 'reCAPTCHA verification failed' },
        { status: 400 }
      )
    }

    // 5. Send DUAL emails (BOTH are required)
    await sendOwnerNotification(sanitizedData)
    
    try {
      await sendCustomerConfirmation(sanitizedData)
    } catch (confirmError) {
      // Log but don't fail if confirmation fails
      console.error('Customer confirmation failed:', confirmError)
    }

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error('Contact form error:', error)
    return NextResponse.json(
      { error: 'Failed to send. Please call {{COMPANY_PHONE}}.' },
      { status: 500 }
    )
  }
}

// ============================================
// EMAIL TEMPLATES (Table-based for Outlook)
// ============================================

function generateOwnerEmailHtml(data: SafeEmailData): string {
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto;">
    <!-- Header -->
    <tr>
      <td style="background-color: {{PRIMARY_COLOR}}; padding: 40px; text-align: center;">
        <h1 style="color: #ffffff; margin: 0; font-size: 28px;">{{COMPANY_NAME}}</h1>
        <p style="color: {{SECONDARY_COLOR}}; margin: 10px 0 0 0;">New Enquiry Received</p>
      </td>
    </tr>
    
    <!-- Content -->
    <tr>
      <td style="background-color: #f7f7f7; padding: 30px;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px;">
          <tr>
            <td style="padding: 20px;">
              <h2 style="color: {{PRIMARY_COLOR}}; margin: 0 0 20px 0;">Contact Details</h2>
              <p style="margin: 8px 0;"><strong>Name:</strong> ${data.name}</p>
              <p style="margin: 8px 0;"><strong>Email:</strong> <a href="mailto:${data.email}" style="color: {{ACCENT_COLOR}};">${data.email}</a></p>
              <p style="margin: 8px 0;"><strong>Phone:</strong> ${data.phone || 'Not provided'}</p>
              <p style="margin: 8px 0;"><strong>Subject:</strong> ${data.subject}</p>
            </td>
          </tr>
        </table>
        
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; margin-top: 20px;">
          <tr>
            <td style="padding: 20px;">
              <h2 style="color: {{PRIMARY_COLOR}}; margin: 0 0 20px 0;">Message</h2>
              <div style="background-color: #f7f7f7; padding: 15px; border-left: 4px solid {{SECONDARY_COLOR}}; border-radius: 4px;">
                <p style="margin: 0; line-height: 1.6; white-space: pre-line;">${data.message.replace(/\n/g, '<br>')}</p>
              </div>
            </td>
          </tr>
        </table>
      </td>
    </tr>
    
    <!-- Footer -->
    <tr>
      <td style="background-color: {{PRIMARY_COLOR}}; padding: 20px; text-align: center;">
        <p style="color: #ffffff; margin: 0; font-size: 12px;">
          Reply directly to: <a href="mailto:${data.email}" style="color: {{SECONDARY_COLOR}};">${data.email}</a>
        </p>
      </td>
    </tr>
  </table>
</body>
</html>
  `
}

function generateOwnerEmailText(data: SafeEmailData): string {
  return `
New Enquiry from {{COMPANY_NAME}} Website

Name: ${data.name}
Email: ${data.email}
Phone: ${data.phone || 'Not provided'}
Subject: ${data.subject}

Message:
${data.message}

---
Reply directly to: ${data.email}
  `.trim()
}

function generateCustomerEmailHtml(data: SafeEmailData): string {
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto;">
    <!-- Header -->
    <tr>
      <td style="background-color: {{PRIMARY_COLOR}}; padding: 40px; text-align: center;">
        <h1 style="color: #ffffff; margin: 0; font-size: 28px;">{{COMPANY_NAME}}</h1>
      </td>
    </tr>
    
    <!-- Content -->
    <tr>
      <td style="background-color: #f7f7f7; padding: 30px;">
        <h2 style="color: {{PRIMARY_COLOR}}; margin: 0 0 20px 0;">Thank you for your enquiry, ${data.name}!</h2>
        <p style="color: #333; line-height: 1.6;">
          We've received your message and will respond within one business day.
        </p>
        <p style="color: #333; line-height: 1.6;">
          For urgent matters, please call us on <strong style="color: {{ACCENT_COLOR}};">{{COMPANY_PHONE}}</strong>.
        </p>
        
        <!-- Message Summary -->
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; margin-top: 20px; border-left: 4px solid {{SECONDARY_COLOR}};">
          <tr>
            <td style="padding: 20px;">
              <h3 style="color: {{PRIMARY_COLOR}}; margin: 0 0 15px 0;">Your message:</h3>
              <p style="margin: 5px 0;"><strong>Subject:</strong> ${data.subject}</p>
              <div style="background-color: #f7f7f7; padding: 15px; border-radius: 4px; margin-top: 10px;">
                <p style="margin: 0; line-height: 1.6; white-space: pre-line;">${data.message.replace(/\n/g, '<br>')}</p>
              </div>
            </td>
          </tr>
        </table>
      </td>
    </tr>
    
    <!-- Footer -->
    <tr>
      <td style="background-color: {{PRIMARY_COLOR}}; padding: 25px; text-align: center;">
        <p style="color: #ffffff; margin: 5px 0; font-size: 14px;">{{COMPANY_NAME}}</p>
        <p style="color: {{SECONDARY_COLOR}}; margin: 5px 0; font-size: 13px;">{{COMPANY_ADDRESS}}</p>
        <p style="margin: 15px 0;">
          <a href="{{WEBSITE_URL}}" style="color: {{ACCENT_COLOR}}; text-decoration: none; font-weight: bold;">
            {{WEBSITE_URL}}
          </a>
        </p>
      </td>
    </tr>
  </table>
</body>
</html>
  `
}

function generateCustomerEmailText(data: SafeEmailData): string {
  return `
Thank you for contacting {{COMPANY_NAME}}, ${data.name}!

We've received your message and will respond within one business day.

For urgent matters, please call us on {{COMPANY_PHONE}}.

Your message:
Subject: ${data.subject}
${data.message}

---
{{COMPANY_NAME}}
{{COMPANY_ADDRESS}}
{{WEBSITE_URL}}
  `.trim()
}
```

---

## Form Component Template

**File**: `src/components/ContactForm.tsx`

```typescript
'use client'

import { useState, useCallback } from 'react'
import Script from 'next/script'

const RECAPTCHA_SITE_KEY = process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY || ''

interface FormData {
  name: string
  email: string
  phone: string
  subject: string
  message: string
}

export default function ContactForm() {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: '',
  })
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')
  const [errorMessage, setErrorMessage] = useState('')

  const handleChange = useCallback((
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setStatus('loading')
    setErrorMessage('')

    try {
      // Get reCAPTCHA token
      const token = await new Promise<string>((resolve, reject) => {
        if (typeof window !== 'undefined' && window.grecaptcha) {
          window.grecaptcha.ready(() => {
            window.grecaptcha
              .execute(RECAPTCHA_SITE_KEY, { action: 'contact_form' })
              .then(resolve)
              .catch(reject)
          })
        } else {
          reject(new Error('reCAPTCHA not loaded'))
        }
      })

      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          recaptchaToken: token,
        }),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.error || 'Failed to send message')
      }

      setStatus('success')
      setFormData({ name: '', email: '', phone: '', subject: '', message: '' })
    } catch (error) {
      setStatus('error')
      setErrorMessage(error instanceof Error ? error.message : 'Something went wrong')
    }
  }

  return (
    <>
      {/* reCAPTCHA v3 - MUST use afterInteractive */}
      <Script
        src={`https://www.google.com/recaptcha/api.js?render=${RECAPTCHA_SITE_KEY}`}
        strategy="afterInteractive"
      />

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Name */}
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700">
            Name *
          </label>
          <input
            type="text"
            id="name"
            name="name"
            required
            value={formData.name}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-[{{PRIMARY_COLOR}}] focus:ring-[{{PRIMARY_COLOR}}]"
          />
        </div>

        {/* Email */}
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">
            Email *
          </label>
          <input
            type="email"
            id="email"
            name="email"
            required
            value={formData.email}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-[{{PRIMARY_COLOR}}] focus:ring-[{{PRIMARY_COLOR}}]"
          />
        </div>

        {/* Phone */}
        <div>
          <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
            Phone
          </label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-[{{PRIMARY_COLOR}}] focus:ring-[{{PRIMARY_COLOR}}]"
          />
        </div>

        {/* Subject */}
        <div>
          <label htmlFor="subject" className="block text-sm font-medium text-gray-700">
            Subject *
          </label>
          <input
            type="text"
            id="subject"
            name="subject"
            required
            value={formData.subject}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-[{{PRIMARY_COLOR}}] focus:ring-[{{PRIMARY_COLOR}}]"
          />
        </div>

        {/* Message */}
        <div>
          <label htmlFor="message" className="block text-sm font-medium text-gray-700">
            Message *
          </label>
          <textarea
            id="message"
            name="message"
            rows={5}
            required
            minLength={10}
            value={formData.message}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-[{{PRIMARY_COLOR}}] focus:ring-[{{PRIMARY_COLOR}}]"
          />
        </div>

        {/* Error Message */}
        {status === 'error' && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-800">{errorMessage}</p>
          </div>
        )}

        {/* Success Message */}
        {status === 'success' && (
          <div className="p-4 bg-green-50 border border-green-200 rounded-md">
            <p className="text-green-800">
              Thank you! We&apos;ve received your message and will respond shortly.
            </p>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={status === 'loading'}
          className="w-full py-3 px-6 rounded-md text-white font-medium transition-colors disabled:opacity-50"
          style={{ backgroundColor: '{{ACCENT_COLOR}}' }}
        >
          {status === 'loading' ? 'Sending...' : 'Send Message'}
        </button>

        {/* reCAPTCHA Notice */}
        <p className="text-xs text-gray-500 text-center">
          Protected by reCAPTCHA. Google{' '}
          <a href="https://policies.google.com/privacy" className="underline">Privacy</a> &{' '}
          <a href="https://policies.google.com/terms" className="underline">Terms</a>.
        </p>
      </form>
    </>
  )
}

// TypeScript declaration for grecaptcha
declare global {
  interface Window {
    grecaptcha: {
      ready: (callback: () => void) => void
      execute: (siteKey: string, options: { action: string }) => Promise<string>
    }
  }
}
```

---

## Environment Validation Template

**File**: `src/lib/env.ts`

```typescript
/**
 * Environment variable validation and access
 * Ensures all required variables are present at runtime
 */

function getEnvVar(key: string, required = true): string {
  const value = process.env[key]
  if (required && !value) {
    throw new Error(`Missing required environment variable: ${key}`)
  }
  return value || ''
}

export const env = {
  // AWS SES
  AWS_REGION: getEnvVar('AWS_REGION'),
  AWS_ACCESS_KEY_ID: getEnvVar('AWS_ACCESS_KEY_ID'),
  AWS_SECRET_ACCESS_KEY: getEnvVar('AWS_SECRET_ACCESS_KEY'),

  // Email addresses
  EMAIL_FROM: getEnvVar('EMAIL_FROM'),
  EMAIL_FROM_NAME: getEnvVar('EMAIL_FROM_NAME', false) || '{{COMPANY_NAME}}',
  EMAIL_TO: getEnvVar('EMAIL_TO'),

  // reCAPTCHA
  RECAPTCHA_SECRET_KEY: getEnvVar('RECAPTCHA_SECRET_KEY'),

  // Rate limiting (optional in dev)
  UPSTASH_REDIS_REST_URL: getEnvVar('UPSTASH_REDIS_REST_URL', false),
  UPSTASH_REDIS_REST_TOKEN: getEnvVar('UPSTASH_REDIS_REST_TOKEN', false),
}

// Helper functions for email config
export function getEmailFrom(): string {
  return env.EMAIL_FROM
}

export function getEmailFromName(): string {
  return env.EMAIL_FROM_NAME
}

export function getEmailTo(): string {
  return env.EMAIL_TO
}
```

---

## Dependencies to Install

```bash
# Required packages
npm install @aws-sdk/client-ses zod isomorphic-dompurify @upstash/ratelimit @upstash/redis

# TypeScript types
npm install -D @types/dompurify
```

---

## Package.json Scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  }
}
```
