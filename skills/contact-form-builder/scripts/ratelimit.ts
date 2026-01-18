/**
 * Upstash Rate Limiting
 * Copy to: src/lib/ratelimit.ts
 * 
 * PLACEHOLDERS TO REPLACE: None - this is ready to use
 * REQUIRES: UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN env vars
 */

import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'
import { NextRequest, NextResponse } from 'next/server'

// Create Redis client (returns null if not configured)
function createRedisClient(): Redis | null {
  const url = process.env.UPSTASH_REDIS_REST_URL
  const token = process.env.UPSTASH_REDIS_REST_TOKEN
  if (!url || !token) return null
  return new Redis({ url, token })
}

const redis = createRedisClient()

// Email form: 5 requests per hour per IP
export const emailRatelimit = redis
  ? new Ratelimit({
      redis,
      limiter: Ratelimit.slidingWindow(5, '1 h'),
      prefix: 'ratelimit:email',
    })
  : null

// Get client IP from request
function getClientIP(request: NextRequest): string {
  const forwardedFor = request.headers.get('x-forwarded-for')
  if (forwardedFor) return forwardedFor.split(',')[0].trim()
  return request.headers.get('x-real-ip') || '127.0.0.1'
}

// Apply rate limiting
export async function applyRateLimit(
  request: NextRequest,
  ratelimit: Ratelimit | null
): Promise<{
  success: boolean
  remaining?: number
  response?: NextResponse
}> {
  if (!ratelimit) return { success: true }

  const ip = getClientIP(request)
  const { success, remaining, reset } = await ratelimit.limit(ip)

  if (!success) {
    const retryAfter = Math.ceil((reset - Date.now()) / 1000)
    return {
      success: false,
      remaining: 0,
      response: NextResponse.json(
        { error: 'Too many requests. Please try again later.', retryAfter },
        { status: 429, headers: { 'Retry-After': String(retryAfter) } }
      ),
    }
  }

  return { success: true, remaining }
}
