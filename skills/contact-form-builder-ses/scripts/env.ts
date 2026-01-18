/**
 * Environment Variable Validation
 * Copy to: src/lib/env.ts
 * 
 * PLACEHOLDERS TO REPLACE:
 * - {{COMPANY_NAME}} - Your company name for default sender
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

  // Email
  EMAIL_FROM: getEnvVar('EMAIL_FROM'),
  EMAIL_FROM_NAME: getEnvVar('EMAIL_FROM_NAME', false) || '{{COMPANY_NAME}}',
  EMAIL_TO: getEnvVar('EMAIL_TO'),

  // reCAPTCHA
  RECAPTCHA_SECRET_KEY: getEnvVar('RECAPTCHA_SECRET_KEY'),

  // Rate limiting (optional in dev)
  UPSTASH_REDIS_REST_URL: getEnvVar('UPSTASH_REDIS_REST_URL', false),
  UPSTASH_REDIS_REST_TOKEN: getEnvVar('UPSTASH_REDIS_REST_TOKEN', false),
}

export function getEmailFrom(): string { return env.EMAIL_FROM }
export function getEmailFromName(): string { return env.EMAIL_FROM_NAME }
export function getEmailTo(): string { return env.EMAIL_TO }
