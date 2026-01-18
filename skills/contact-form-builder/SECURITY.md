# Security Implementation

Critical security components for email-sending features. **NEVER skip these**.

---

## Validation (Zod)

**File**: `src/lib/validation.ts`

```typescript
/**
 * Zod validation schemas for form inputs
 * Validates BEFORE sanitisation
 */

import { z } from 'zod'

/**
 * Contact form validation schema
 * Customise fields based on user requirements
 */
export const contactFormSchema = z.object({
  name: z
    .string()
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name must be under 100 characters')
    .regex(/^[a-zA-Z\s\-']+$/, 'Name contains invalid characters'),

  email: z
    .string()
    .email('Please enter a valid email address')
    .max(254, 'Email must be under 254 characters'),

  phone: z
    .string()
    .max(20, 'Phone number must be under 20 characters')
    .regex(/^[\d\s\+\-\(\)]*$/, 'Phone contains invalid characters')
    .optional()
    .or(z.literal('')),

  subject: z
    .string()
    .min(3, 'Subject must be at least 3 characters')
    .max(200, 'Subject must be under 200 characters'),

  message: z
    .string()
    .min(10, 'Message must be at least 10 characters')
    .max(5000, 'Message must be under 5000 characters'),

  recaptchaToken: z
    .string()
    .min(1, 'reCAPTCHA verification required'),
})

export type ContactFormData = z.infer<typeof contactFormSchema>

/**
 * Newsletter signup schema (simpler form)
 */
export const newsletterSchema = z.object({
  email: z
    .string()
    .email('Please enter a valid email address')
    .max(254, 'Email must be under 254 characters'),

  recaptchaToken: z
    .string()
    .min(1, 'reCAPTCHA verification required'),
})

export type NewsletterFormData = z.infer<typeof newsletterSchema>

/**
 * Callback request schema
 */
export const callbackSchema = z.object({
  name: z
    .string()
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name must be under 100 characters'),

  phone: z
    .string()
    .min(10, 'Please enter a valid phone number')
    .max(20, 'Phone number must be under 20 characters')
    .regex(/^[\d\s\+\-\(\)]+$/, 'Phone contains invalid characters'),

  preferredTime: z
    .enum(['morning', 'afternoon', 'evening'])
    .optional(),

  recaptchaToken: z
    .string()
    .min(1, 'reCAPTCHA verification required'),
})

export type CallbackFormData = z.infer<typeof callbackSchema>
```

---

## Sanitisation (DOMPurify)

**File**: `src/lib/sanitize.ts`

```typescript
/**
 * HTML sanitisation using DOMPurify
 * Prevents XSS attacks in user input
 * 
 * IMPORTANT: Always sanitise AFTER Zod validation
 */

import DOMPurify from 'isomorphic-dompurify'

/**
 * Sanitise a single string value
 * Removes all HTML tags and dangerous content
 */
export function sanitizeString(input: string): string {
  if (!input) return ''
  
  // Remove all HTML tags - we want plain text only
  return DOMPurify.sanitize(input, {
    ALLOWED_TAGS: [], // No HTML allowed
    ALLOWED_ATTR: [], // No attributes allowed
  }).trim()
}

/**
 * Sanitise contact form data
 * Call this AFTER Zod validation passes
 */
export function sanitizeContactData(data: {
  name: string
  email: string
  phone?: string
  subject: string
  message: string
}): {
  name: string
  email: string
  phone?: string
  subject: string
  message: string
} {
  return {
    name: sanitizeString(data.name),
    email: sanitizeString(data.email), // Email already validated by Zod
    phone: data.phone ? sanitizeString(data.phone) : undefined,
    subject: sanitizeString(data.subject),
    message: sanitizeString(data.message),
  }
}

/**
 * Sanitise newsletter signup data
 */
export function sanitizeNewsletterData(data: {
  email: string
}): {
  email: string
} {
  return {
    email: sanitizeString(data.email),
  }
}

/**
 * Sanitise callback request data
 */
export function sanitizeCallbackData(data: {
  name: string
  phone: string
  preferredTime?: string
}): {
  name: string
  phone: string
  preferredTime?: string
} {
  return {
    name: sanitizeString(data.name),
    phone: sanitizeString(data.phone),
    preferredTime: data.preferredTime ? sanitizeString(data.preferredTime) : undefined,
  }
}

/**
 * Test if a string contains potentially dangerous content
 * Use for logging/monitoring suspicious submissions
 */
export function containsSuspiciousContent(input: string): boolean {
  const suspiciousPatterns = [
    /<script/i,
    /javascript:/i,
    /on\w+=/i, // onclick=, onerror=, etc.
    /<iframe/i,
    /<object/i,
    /<embed/i,
    /data:/i,
    /vbscript:/i,
  ]

  return suspiciousPatterns.some(pattern => pattern.test(input))
}
```

---

## Rate Limiting (Upstash)

**File**: `src/lib/ratelimit.ts`

```typescript
/**
 * Rate limiting using Upstash Redis
 * Prevents spam and DDoS attacks
 */

import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'
import { NextRequest, NextResponse } from 'next/server'

/**
 * Create Redis client from environment
 * Returns null if not configured (dev mode fallback)
 */
function createRedisClient(): Redis | null {
  const url = process.env.UPSTASH_REDIS_REST_URL
  const token = process.env.UPSTASH_REDIS_REST_TOKEN

  if (!url || !token) {
    console.warn('Rate limiting disabled: UPSTASH_REDIS credentials not configured')
    return null
  }

  return new Redis({ url, token })
}

const redis = createRedisClient()

/**
 * Email form rate limiter
 * 5 requests per hour per IP (prevents spam)
 */
export const emailRatelimit = redis
  ? new Ratelimit({
      redis,
      limiter: Ratelimit.slidingWindow(5, '1 h'),
      analytics: true,
      prefix: 'ratelimit:email',
    })
  : null

/**
 * General API rate limiter
 * 60 requests per minute per IP
 */
export const apiRatelimit = redis
  ? new Ratelimit({
      redis,
      limiter: Ratelimit.slidingWindow(60, '1 m'),
      analytics: true,
      prefix: 'ratelimit:api',
    })
  : null

/**
 * Newsletter signup rate limiter
 * 3 requests per day per IP
 */
export const newsletterRatelimit = redis
  ? new Ratelimit({
      redis,
      limiter: Ratelimit.slidingWindow(3, '1 d'),
      analytics: true,
      prefix: 'ratelimit:newsletter',
    })
  : null

/**
 * Get client IP from request
 */
function getClientIP(request: NextRequest): string {
  // Check common headers for real IP (behind proxy/CDN)
  const forwardedFor = request.headers.get('x-forwarded-for')
  if (forwardedFor) {
    return forwardedFor.split(',')[0].trim()
  }

  const realIP = request.headers.get('x-real-ip')
  if (realIP) {
    return realIP
  }

  // Fallback
  return '127.0.0.1'
}

/**
 * Apply rate limiting to a request
 * Returns success: true if allowed, or a 429 response if blocked
 */
export async function applyRateLimit(
  request: NextRequest,
  ratelimit: Ratelimit | null
): Promise<{
  success: boolean
  remaining?: number
  response?: NextResponse
}> {
  // Skip rate limiting if not configured
  if (!ratelimit) {
    return { success: true }
  }

  const ip = getClientIP(request)
  const { success, remaining, reset } = await ratelimit.limit(ip)

  if (!success) {
    const retryAfter = Math.ceil((reset - Date.now()) / 1000)
    
    return {
      success: false,
      remaining: 0,
      response: NextResponse.json(
        {
          error: 'Too many requests. Please try again later.',
          retryAfter,
        },
        {
          status: 429,
          headers: {
            'Retry-After': String(retryAfter),
            'X-RateLimit-Remaining': '0',
          },
        }
      ),
    }
  }

  return {
    success: true,
    remaining,
  }
}

/**
 * Rate limit configuration guide:
 * 
 * - Contact forms: 5/hour (prevents spam while allowing genuine retries)
 * - Newsletter: 3/day (one signup per day is plenty)
 * - Callback requests: 3/hour (similar to contact)
 * - General API: 60/minute (standard API protection)
 * 
 * Adjust these based on expected legitimate usage patterns.
 */
```

---

## Security Headers (Middleware)

**File**: `src/middleware.ts`

```typescript
/**
 * Security middleware
 * Adds CSP and other security headers
 */

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()

  // Content Security Policy
  const csp = [
    "default-src 'self'",
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.google.com https://www.gstatic.com",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: https:",
    "font-src 'self' data:",
    "frame-src https://www.google.com",
    "connect-src 'self' https://www.google.com",
  ].join('; ')

  response.headers.set('Content-Security-Policy', csp)
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-XSS-Protection', '1; mode=block')
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  response.headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')

  return response
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
}
```

---

## Security Checklist

Before deploying any email feature:

### Validation
- [ ] Zod schema validates ALL user inputs
- [ ] Email format validated
- [ ] String lengths limited (prevent DoS)
- [ ] Regex patterns prevent injection

### Sanitisation
- [ ] DOMPurify sanitises ALL user inputs
- [ ] No HTML allowed in plain text fields
- [ ] Sanitisation happens AFTER validation

### Rate Limiting
- [ ] Upstash Redis configured
- [ ] Appropriate limits per endpoint
- [ ] 429 responses include Retry-After

### reCAPTCHA
- [ ] v3 with score threshold >= 0.5
- [ ] Token verified server-side
- [ ] Secret key never exposed to client

### Email Security
- [ ] SES sender domain verified with DKIM
- [ ] Reply-To set to customer (not spoofable)
- [ ] No user input in From address
- [ ] Production SES access (not sandbox)

### Headers
- [ ] CSP configured
- [ ] X-Frame-Options: DENY
- [ ] X-Content-Type-Options: nosniff
- [ ] HTTPS enforced
