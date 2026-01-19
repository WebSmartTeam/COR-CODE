# Next.js Stripe Integration Specifics

## Key Differences from Vite

| Aspect | Vite + Vercel | Next.js |
|--------|---------------|---------|
| Environment Variables | `import.meta.env.VITE_*` | `process.env.*` |
| API Routes | `api/*.ts` | `app/api/*/route.ts` (App Router) or `pages/api/*.ts` (Pages Router) |
| Client Directive | Not needed | `'use client'` for components using hooks |
| Server Components | N/A | Default in App Router |

## Environment Variables

```bash
# .env.local (Next.js)
# Client-side variables need NEXT_PUBLIC_ prefix
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key

# Server-side only (no prefix)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

## Client Library (Next.js)

```typescript
// lib/stripe.ts
import { loadStripe } from '@stripe/stripe-js'

const stripePublishableKey = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY

if (!stripePublishableKey) {
  throw new Error('NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY is required')
}

export const stripePromise = loadStripe(stripePublishableKey)

// UK configuration
export const stripeConfig = {
  currency: 'GBP',
  country: 'GB',
  appearance: {
    theme: 'stripe' as const,
    variables: {
      colorPrimary: '#your-brand-color',
      borderRadius: '8px',
    },
  },
}

export const formatPriceForStripe = (pounds: number): number => Math.round(pounds * 100)
export const formatPriceForDisplay = (pence: number): number => pence / 100
```

## API Routes (App Router)

### Create Payment Intent

```typescript
// app/api/stripe/create-payment-intent/route.ts
import { NextRequest, NextResponse } from 'next/server'
import Stripe from 'stripe'
import { createClient } from '@supabase/supabase-js'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-06-30.basil',
})

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY! // Use service role for server-side
)

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { order_id, amount, currency = 'gbp', customer_email, description } = body

    // Validate required fields
    if (!order_id || !amount) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      )
    }

    // Verify order exists and amount matches
    const { data: order, error: orderError } = await supabase
      .from('orders')
      .select('id, total_amount')
      .eq('id', order_id)
      .single()

    if (orderError || !order) {
      return NextResponse.json(
        { error: 'Order not found' },
        { status: 404 }
      )
    }

    // Verify amount matches
    if (Math.abs(Number(amount) - Number(order.total_amount)) > 0.01) {
      return NextResponse.json(
        { error: 'Amount mismatch' },
        { status: 400 }
      )
    }

    // Create payment intent
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(amount * 100), // Convert to pence
      currency,
      description,
      metadata: { order_id, customer_email: customer_email || '' },
      automatic_payment_methods: {
        enabled: true,
        allow_redirects: 'never',
      },
    })

    // Save to database
    await supabase.from('stripe_payment_intents').insert({
      order_id,
      stripe_payment_intent_id: paymentIntent.id,
      amount: paymentIntent.amount,
      currency: paymentIntent.currency,
      status: paymentIntent.status,
      client_secret: paymentIntent.client_secret,
    })

    // Update order
    await supabase
      .from('orders')
      .update({
        payment_reference: paymentIntent.id,
        payment_status: 'pending',
        updated_at: new Date().toISOString(),
      })
      .eq('id', order_id)

    return NextResponse.json({
      client_secret: paymentIntent.client_secret,
      payment_intent_id: paymentIntent.id,
      amount: paymentIntent.amount,
      currency: paymentIntent.currency,
    })
  } catch (error) {
    console.error('Error creating payment intent:', error)
    return NextResponse.json(
      { error: 'Failed to create payment intent' },
      { status: 500 }
    )
  }
}
```

### Webhook Handler

```typescript
// app/api/stripe/webhook/route.ts
import { NextResponse } from 'next/server'
import { headers } from 'next/headers'
import Stripe from 'stripe'
import { createClient } from '@supabase/supabase-js'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-06-30.basil',
})

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

export async function POST(request: Request) {
  const body = await request.text() // Raw body for signature
  const signature = headers().get('stripe-signature')!

  try {
    const event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )

    // Log event for idempotency
    const { error: logError } = await supabase
      .from('stripe_webhook_events')
      .insert({
        stripe_event_id: event.id,
        event_type: event.type,
        processed: false,
        event_data: event.data,
      })

    if (logError?.code === '23505') {
      // Duplicate - already processed
      return NextResponse.json({ received: true, duplicate: true })
    }

    // Process event
    switch (event.type) {
      case 'payment_intent.succeeded':
        await handlePaymentSuccess(event.data.object as Stripe.PaymentIntent)
        break
      case 'payment_intent.payment_failed':
        await handlePaymentFailed(event.data.object as Stripe.PaymentIntent)
        break
    }

    // Mark processed
    await supabase
      .from('stripe_webhook_events')
      .update({ processed: true, processed_at: new Date().toISOString() })
      .eq('stripe_event_id', event.id)

    return NextResponse.json({ received: true })
  } catch (error) {
    console.error('Webhook error:', error)
    return NextResponse.json(
      { error: 'Webhook verification failed' },
      { status: 400 }
    )
  }
}

async function handlePaymentSuccess(paymentIntent: Stripe.PaymentIntent) {
  const { data: order } = await supabase
    .from('orders')
    .select('id')
    .eq('payment_reference', paymentIntent.id)
    .single()

  if (!order) return

  await supabase
    .from('orders')
    .update({
      payment_status: 'succeeded',
      payment_method: 'card',
      payment_date: new Date().toISOString(),
      status: 'processing',
    })
    .eq('id', order.id)
}

async function handlePaymentFailed(paymentIntent: Stripe.PaymentIntent) {
  const { data: order } = await supabase
    .from('orders')
    .select('id')
    .eq('payment_reference', paymentIntent.id)
    .single()

  if (!order) return

  await supabase
    .from('orders')
    .update({
      payment_status: 'failed',
      status: 'cancelled',
    })
    .eq('id', order.id)
}
```

## Client Components

### Payment Page (App Router)

```typescript
// app/payment/[orderId]/page.tsx
'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter, useSearchParams } from 'next/navigation'
import { Elements } from '@stripe/react-stripe-js'
import { stripePromise } from '@/lib/stripe'
import StripeCheckout from '@/components/StripeCheckout'
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

export default function PaymentPage() {
  const params = useParams()
  const router = useRouter()
  const orderId = params.orderId as string

  const [clientSecret, setClientSecret] = useState<string | null>(null)
  const [orderData, setOrderData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (orderId) {
      fetchOrderAndCreatePayment()
    }
  }, [orderId])

  const fetchOrderAndCreatePayment = async () => {
    try {
      // Fetch order details
      const { data: order, error: orderError } = await supabase
        .from('orders')
        .select(`
          id, order_number, total_amount,
          customers (email, first_name, last_name)
        `)
        .eq('id', orderId)
        .single()

      if (orderError || !order) {
        throw new Error('Order not found')
      }

      setOrderData(order)

      // Create payment intent
      const response = await fetch('/api/stripe/create-payment-intent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          order_id: orderId,
          amount: order.total_amount,
          currency: 'gbp',
          customer_email: order.customers?.email,
          description: `Order ${order.order_number}`,
        }),
      })

      const data = await response.json()
      if (!response.ok) throw new Error(data.error)

      setClientSecret(data.client_secret)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load payment')
    } finally {
      setLoading(false)
    }
  }

  const handleSuccess = (paymentIntentId: string) => {
    router.push(`/order-confirmation/${orderId}`)
  }

  if (loading) return <div>Loading payment...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div className="max-w-lg mx-auto py-12">
      <h1 className="text-2xl font-bold mb-4">Complete Payment</h1>
      <p className="mb-6">Order: {orderData?.order_number} - £{orderData?.total_amount?.toFixed(2)}</p>

      {clientSecret && (
        <Elements
          stripe={stripePromise}
          options={{
            clientSecret,
            appearance: { theme: 'stripe' }
          }}
        >
          <StripeCheckout
            clientSecret={clientSecret}
            onSuccess={handleSuccess}
            onError={setError}
            customerData={{
              email: orderData?.customers?.email || '',
              firstName: orderData?.customers?.first_name || '',
              lastName: orderData?.customers?.last_name || '',
            }}
          />
        </Elements>
      )}
    </div>
  )
}
```

## Deployment Configuration

### vercel.json (for both Vite and Next.js on Vercel)

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "regions": ["lhr1"],
  "functions": {
    "api/stripe/webhook.ts": {
      "maxDuration": 30
    }
  }
}
```

### next.config.js

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    // Required for webhook raw body handling
    serverActions: true,
  },
}

module.exports = nextConfig
```
