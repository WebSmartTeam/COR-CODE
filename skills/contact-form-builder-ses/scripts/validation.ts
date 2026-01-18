/**
 * Zod Validation Schemas
 * Copy to: src/lib/validation.ts
 * 
 * PLACEHOLDERS TO REPLACE: None - this is ready to use
 */

import { z } from 'zod'

// Contact form schema
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
