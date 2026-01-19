# Stripe Webhook Handling

## Overview

Webhooks allow Stripe to notify your server about payment events (success, failure, refunds). This is **critical** for reliable payment processing - don't rely solely on client-side callbacks!

## Setting Up Webhooks

### 1. Create Webhook Endpoint in Stripe Dashboard

1. Go to [Stripe Dashboard → Developers → Webhooks](https://dashboard.stripe.com/webhooks)
2. Click "Add endpoint"
3. Enter your endpoint URL: `https://yoursite.com/api/stripe/webhook`
4. Select events to listen for:
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
   - `checkout.session.completed`
   - `checkout.session.expired`
5. Copy the signing secret (starts with `whsec_`)

### 2. Webhook API Endpoint

**CRITICAL**: Disable body parsing to get raw body for signature validation!

#### Vite + Vercel

```typescript
// api/stripe/webhook.ts
import type { VercelRequest, VercelResponse } from '@vercel/node'
import { supabase } from '../../src/lib/supabase'
import { validateStripeWebhook } from '../../src/lib/stripe-server'
import type Stripe from 'stripe'

// CRITICAL: Disable body parsing for webhook signature validation
export const config = {
  api: {
    bodyParser: false,
  },
}

export default async function handler(req: VercelRequest, res: VercelResponse) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const signature = req.headers['stripe-signature'] as string
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET

  if (!signature || !webhookSecret) {
    return res.status(400).json({ error: 'Missing webhook signature or secret' })
  }

  try {
    // Get raw body as buffer - CRITICAL for signature validation
    const chunks: Buffer[] = []
    for await (const chunk of req as any) {
      chunks.push(typeof chunk === 'string' ? Buffer.from(chunk) : chunk)
    }
    const rawBody = Buffer.concat(chunks).toString('utf8')

    // Validate webhook signature
    const event = validateStripeWebhook(rawBody, signature, webhookSecret)

    // Log webhook event to database (idempotency)
    const { error: logError } = await supabase
      .from('stripe_webhook_events')
      .insert({
        stripe_event_id: event.id,
        event_type: event.type,
        processed: false,
        event_data: event.data,
      })

    if (logError && logError.code === '23505') {
      // Duplicate event - already processed
      return res.status(200).json({ received: true, duplicate: true })
    }

    // Process the event
    switch (event.type) {
      case 'payment_intent.succeeded':
        await handlePaymentIntentSucceeded(event.data.object as Stripe.PaymentIntent)
        break
      case 'payment_intent.payment_failed':
        await handlePaymentIntentFailed(event.data.object as Stripe.PaymentIntent)
        break
      case 'checkout.session.completed':
        await handleCheckoutSessionCompleted(event.data.object as Stripe.Checkout.Session)
        break
      case 'checkout.session.expired':
        await handleCheckoutSessionExpired(event.data.object as Stripe.Checkout.Session)
        break
      default:
        // Unhandled event type
        console.log(`Unhandled event type: ${event.type}`)
    }

    // Mark event as processed
    await supabase
      .from('stripe_webhook_events')
      .update({ processed: true, processed_at: new Date().toISOString() })
      .eq('stripe_event_id', event.id)

    return res.status(200).json({ received: true })
  } catch (error) {
    console.error('Webhook error:', error)
    return res.status(400).json({
      error: 'Webhook processing failed',
      details: error instanceof Error ? error.message : 'Unknown error',
    })
  }
}

// Handle successful payment
async function handlePaymentIntentSucceeded(paymentIntent: Stripe.PaymentIntent) {
  try {
    // Find order by payment reference
    const { data: order, error } = await supabase
      .from('orders')
      .select('id')
      .eq('payment_reference', paymentIntent.id)
      .single()

    if (error || !order) {
      console.error('Order not found for payment intent:', paymentIntent.id)
      return
    }

    // Update order status
    await supabase
      .from('orders')
      .update({
        payment_status: 'succeeded',
        payment_method: 'card',
        payment_date: new Date().toISOString(),
        status: 'processing',
        updated_at: new Date().toISOString(),
      })
      .eq('id', order.id)

    // Update payment intent record
    await supabase
      .from('stripe_payment_intents')
      .update({
        status: paymentIntent.status,
        updated_at: new Date().toISOString(),
      })
      .eq('stripe_payment_intent_id', paymentIntent.id)

    console.log('Payment succeeded for order:', order.id)
  } catch (error) {
    console.error('Error handling payment success:', error)
  }
}

// Handle failed payment
async function handlePaymentIntentFailed(paymentIntent: Stripe.PaymentIntent) {
  try {
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
        updated_at: new Date().toISOString(),
      })
      .eq('id', order.id)

    await supabase
      .from('stripe_payment_intents')
      .update({
        status: paymentIntent.status,
        last_payment_error: paymentIntent.last_payment_error,
        updated_at: new Date().toISOString(),
      })
      .eq('stripe_payment_intent_id', paymentIntent.id)

    console.log('Payment failed for order:', order.id)
  } catch (error) {
    console.error('Error handling payment failure:', error)
  }
}

// Handle completed checkout session
async function handleCheckoutSessionCompleted(session: Stripe.Checkout.Session) {
  try {
    const { data: paymentSession } = await supabase
      .from('stripe_payment_sessions')
      .select('order_id')
      .eq('stripe_session_id', session.id)
      .single()

    if (!paymentSession) return

    // Build update object
    const orderUpdate: any = {
      payment_reference: session.payment_intent as string,
      payment_status: 'succeeded',
      payment_method: 'card',
      payment_date: new Date().toISOString(),
      status: 'processing',
      updated_at: new Date().toISOString(),
    }

    // Add shipping address if collected via Stripe
    if (session.shipping?.address) {
      orderUpdate.shipping_name = session.shipping.name
      orderUpdate.shipping_phone = session.customer_details?.phone
      orderUpdate.shipping_address_line1 = session.shipping.address.line1
      orderUpdate.shipping_address_line2 = session.shipping.address.line2
      orderUpdate.shipping_city = session.shipping.address.city
      orderUpdate.shipping_county = session.shipping.address.state
      orderUpdate.shipping_postcode = session.shipping.address.postal_code
      orderUpdate.shipping_country = session.shipping.address.country || 'GB'
    }

    await supabase
      .from('orders')
      .update(orderUpdate)
      .eq('id', paymentSession.order_id)

    await supabase
      .from('stripe_payment_sessions')
      .update({ session_status: 'complete', updated_at: new Date().toISOString() })
      .eq('stripe_session_id', session.id)

    console.log('Checkout session completed for order:', paymentSession.order_id)
  } catch (error) {
    console.error('Error handling checkout session:', error)
  }
}

// Handle expired checkout session
async function handleCheckoutSessionExpired(session: Stripe.Checkout.Session) {
  try {
    const { data: paymentSession } = await supabase
      .from('stripe_payment_sessions')
      .select('order_id')
      .eq('stripe_session_id', session.id)
      .single()

    if (!paymentSession) return

    await supabase
      .from('stripe_payment_sessions')
      .update({ session_status: 'expired', updated_at: new Date().toISOString() })
      .eq('stripe_session_id', session.id)

    console.log('Checkout session expired:', session.id)
  } catch (error) {
    console.error('Error handling session expiry:', error)
  }
}
```

#### Next.js App Router

```typescript
// app/api/stripe/webhook/route.ts
import { NextResponse } from 'next/server'
import { headers } from 'next/headers'
import Stripe from 'stripe'
import { supabase } from '@/lib/supabase'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-06-30.basil',
})

export async function POST(request: Request) {
  const body = await request.text()
  const signature = headers().get('stripe-signature')!

  try {
    const event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )

    // Process event...
    switch (event.type) {
      case 'payment_intent.succeeded':
        // Handle success
        break
      // ... other cases
    }

    return NextResponse.json({ received: true })
  } catch (error) {
    console.error('Webhook error:', error)
    return NextResponse.json(
      { error: 'Webhook signature verification failed' },
      { status: 400 }
    )
  }
}
```

## Testing Webhooks Locally

### Using Stripe CLI

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:3000/api/stripe/webhook

# In another terminal, trigger test events
stripe trigger payment_intent.succeeded
stripe trigger payment_intent.payment_failed
```

## Best Practices

1. **Always validate signatures** - Never skip webhook signature validation
2. **Idempotency** - Store event IDs to handle duplicate deliveries
3. **Return 200 quickly** - Process asynchronously if needed
4. **Log everything** - Store webhook events for debugging
5. **Handle retries** - Stripe retries failed webhooks for up to 3 days
