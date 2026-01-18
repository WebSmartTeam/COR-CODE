/**
 * DOMPurify Sanitisation Helpers
 * Copy to: src/lib/sanitize.ts
 * 
 * PLACEHOLDERS TO REPLACE: None - this is ready to use
 */

import DOMPurify from 'isomorphic-dompurify'

// Sanitise a single string (removes all HTML)
export function sanitizeString(input: string): string {
  if (!input) return ''
  return DOMPurify.sanitize(input, {
    ALLOWED_TAGS: [],
    ALLOWED_ATTR: [],
  }).trim()
}

// Sanitise contact form data
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
    email: sanitizeString(data.email),
    phone: data.phone ? sanitizeString(data.phone) : undefined,
    subject: sanitizeString(data.subject),
    message: sanitizeString(data.message),
  }
}
