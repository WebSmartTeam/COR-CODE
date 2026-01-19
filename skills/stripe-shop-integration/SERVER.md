# Server-Side Stripe Setup

## Installation

```bash
npm install stripe
```

## src/lib/stripe-server.ts

Server-side Stripe configuration:

```typescript
import Stripe from 'stripe';

// Initialize Stripe with secret key
const stripe = new Stripe(import.meta.env.STRIPE_SECRET_KEY || process.env.STRIPE_SECRET_KEY || '', {
  apiVersion: '2025-06-30.basil', // Use latest API version
});

export { stripe };

// Stripe server-side configuration for UK market
export const stripeServerConfig = {
  currency: 'gbp',
  country: 'GB',
  supportedPaymentMethods: ['card', 'apple_pay', 'google_pay', 'link'],
  automaticPaymentMethods: {
    enabled: true,
    allow_redirects: 'never',
  },
  paymentIntentConfig: {
    automatic_payment_methods: {
      enabled: true,
      allow_redirects: 'never' as const,
    },
  },
  checkoutSessionConfig: {
    mode: 'payment' as const,
    currency: 'gbp',
    billing_address_collection: 'required' as const,
    shipping_address_collection: {
      allowed_countries: ['GB' as const],
    },
    phone_number_collection: {
      enabled: true,
    },
  },
};

// Helper function to validate webhook signature
export const validateStripeWebhook = (
  payload: string,
  signature: string,
  webhookSecret: string
): Stripe.Event => {
  try {
    return stripe.webhooks.constructEvent(payload, signature, webhookSecret);
  } catch (error) {
    console.error('Stripe webhook validation failed:', error);
    throw new Error('Invalid webhook signature');
  }
};

// Helper function to format price for Stripe (pounds to pence)
export const formatPriceForStripe = (pounds: number): number => {
  return Math.round(pounds * 100);
};

// Create a Stripe customer
export const createStripeCustomer = async (customerData: {
  email: string;
  name: string;
  phone?: string;
  address?: Stripe.AddressParam;
}): Promise<Stripe.Customer> => {
  try {
    const customer = await stripe.customers.create({
      email: customerData.email,
      name: customerData.name,
      phone: customerData.phone,
      address: customerData.address,
      metadata: {
        source: 'your-shop-name',
      },
    });
    return customer;
  } catch (error) {
    console.error('Error creating Stripe customer:', error);
    throw new Error('Failed to create Stripe customer');
  }
};

// Create a payment intent
export const createPaymentIntent = async (params: {
  amount: number; // in pence
  currency?: string;
  customer_id?: string;
  description?: string;
  metadata?: Record<string, string>;
}): Promise<Stripe.PaymentIntent> => {
  try {
    const paymentIntent = await stripe.paymentIntents.create({
      amount: params.amount,
      currency: params.currency || 'gbp',
      customer: params.customer_id,
      description: params.description,
      metadata: {
        integration: 'your-shop-name',
        ...params.metadata,
      },
      automatic_payment_methods: stripeServerConfig.paymentIntentConfig.automatic_payment_methods,
    });
    return paymentIntent;
  } catch (error) {
    console.error('Error creating payment intent:', error);
    throw new Error('Failed to create payment intent');
  }
};

// Create a checkout session
export const createCheckoutSession = async (params: {
  line_items: Stripe.Checkout.SessionCreateParams.LineItem[];
  success_url: string;
  cancel_url: string;
  customer_email?: string;
  customer_id?: string;
  collect_shipping_address?: boolean;
  metadata?: Record<string, string>;
}): Promise<Stripe.Checkout.Session> => {
  try {
    const session = await stripe.checkout.sessions.create({
      mode: stripeServerConfig.checkoutSessionConfig.mode,
      currency: stripeServerConfig.checkoutSessionConfig.currency,
      billing_address_collection: stripeServerConfig.checkoutSessionConfig.billing_address_collection,
      shipping_address_collection: params.collect_shipping_address
        ? stripeServerConfig.checkoutSessionConfig.shipping_address_collection
        : undefined,
      phone_number_collection: stripeServerConfig.checkoutSessionConfig.phone_number_collection,
      line_items: params.line_items,
      success_url: params.success_url,
      cancel_url: params.cancel_url,
      customer_email: params.customer_email,
      customer: params.customer_id,
      metadata: {
        integration: 'your-shop-name',
        ...params.metadata,
      },
    });
    return session;
  } catch (error) {
    console.error('Error creating checkout session:', error);
    throw new Error('Failed to create checkout session');
  }
};

// Retrieve a payment intent
export const retrievePaymentIntent = async (
  paymentIntentId: string
): Promise<Stripe.PaymentIntent> => {
  try {
    return await stripe.paymentIntents.retrieve(paymentIntentId);
  } catch (error) {
    console.error('Error retrieving payment intent:', error);
    throw new Error('Failed to retrieve payment intent');
  }
};

// Create a refund
export const createRefund = async (params: {
  payment_intent: string;
  amount?: number; // in pence, omit for full refund
  reason?: 'duplicate' | 'fraudulent' | 'requested_by_customer';
}): Promise<Stripe.Refund> => {
  try {
    return await stripe.refunds.create({
      payment_intent: params.payment_intent,
      amount: params.amount,
      reason: params.reason,
    });
  } catch (error) {
    console.error('Error creating refund:', error);
    throw new Error('Failed to create refund');
  }
};

export default stripe;
```

## API Endpoint: Create Payment Intent

`api/stripe/create-payment-intent.ts` (Vercel):

```typescript
import type { VercelRequest, VercelResponse } from '@vercel/node'
import { createClient } from '@supabase/supabase-js'
import Stripe from 'stripe'

// Initialize Supabase client
const supabase = createClient(
  process.env.VITE_SUPABASE_URL || '',
  process.env.VITE_SUPABASE_ANON_KEY || ''
)

// Initialize Stripe
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || '', {
  apiVersion: '2025-06-30.basil',
})

export default async function handler(req: VercelRequest, res: VercelResponse) {
  // Add CORS headers
  const allowedOrigins = [
    'https://www.yoursite.com',
    'https://yoursite.com',
    'https://your-project.vercel.app'
  ]
  const origin = req.headers.origin || ''
  if (allowedOrigins.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin)
  }
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS')
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type')

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    return res.status(200).end()
  }

  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const { order_id, amount, currency = 'gbp', customer_email, description } = req.body

    // Validate required fields
    if (!order_id || !amount) {
      return res.status(400).json({ error: 'Missing required fields: order_id, amount' })
    }

    // CRITICAL: Verify the order exists and amount matches database
    const { data: order, error: orderError } = await supabase
      .from('orders')
      .select('id, total_amount, customer_id')
      .eq('id', order_id)
      .single()

    if (orderError || !order) {
      return res.status(404).json({ error: 'Order not found' })
    }

    // Verify the amount matches the order total
    const orderTotal = Number(order.total_amount)
    const requestAmount = Number(amount)

    if (Math.abs(requestAmount - orderTotal) > 0.01) {
      return res.status(400).json({
        error: 'Amount mismatch with order total',
        details: { requested: requestAmount, expected: orderTotal }
      })
    }

    // Create Stripe payment intent
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(amount * 100), // Convert to pence
      currency,
      description: description || `Order ${order_id}`,
      metadata: {
        order_id,
        customer_email: customer_email || '',
      },
      automatic_payment_methods: {
        enabled: true,
        allow_redirects: 'never',
      },
    })

    // Save payment intent to database
    await supabase
      .from('stripe_payment_intents')
      .insert({
        order_id,
        stripe_payment_intent_id: paymentIntent.id,
        amount: paymentIntent.amount,
        currency: paymentIntent.currency,
        status: paymentIntent.status,
        client_secret: paymentIntent.client_secret,
      })

    // Update order with payment reference
    await supabase
      .from('orders')
      .update({
        payment_reference: paymentIntent.id,
        payment_status: 'pending',
        updated_at: new Date().toISOString(),
      })
      .eq('id', order_id)

    return res.status(200).json({
      client_secret: paymentIntent.client_secret,
      payment_intent_id: paymentIntent.id,
      amount: paymentIntent.amount,
      currency: paymentIntent.currency,
      status: paymentIntent.status,
    })
  } catch (error) {
    console.error('Error creating payment intent:', error)
    return res.status(500).json({
      error: 'Failed to create payment intent',
      details: error instanceof Error ? error.message : 'Unknown error',
    })
  }
}
```

## API Endpoint: Create Checkout Session

`api/stripe/create-checkout-session.ts`:

```typescript
import type { VercelRequest, VercelResponse } from '@vercel/node'
import { supabase } from '../../src/lib/supabase'
import { createCheckoutSession } from '../../src/lib/stripe-server'

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const { order_id, success_url, cancel_url, customer_email } = req.body

    if (!order_id || !success_url || !cancel_url) {
      return res.status(400).json({
        error: 'Missing required fields: order_id, success_url, cancel_url'
      })
    }

    // Get order details with items
    const { data: order, error: orderError } = await supabase
      .from('orders')
      .select(`
        id,
        order_number,
        total_amount,
        customers (email, first_name, last_name)
      `)
      .eq('id', order_id)
      .single()

    if (orderError || !order) {
      return res.status(404).json({ error: 'Order not found' })
    }

    // Get order items
    const { data: orderItems } = await supabase
      .from('order_items')
      .select('quantity, price, product_name, products (short_description, featured_image)')
      .eq('order_id', order_id)

    if (!orderItems || orderItems.length === 0) {
      return res.status(400).json({ error: 'No order items found' })
    }

    // Convert to Stripe line items
    const lineItems = orderItems.map((item: any) => ({
      price_data: {
        currency: 'gbp',
        product_data: {
          name: item.product_name,
          description: item.products?.short_description || '',
          images: item.products?.featured_image ? [item.products.featured_image] : [],
        },
        unit_amount: Math.round((item.price / item.quantity) * 100), // Unit price in pence
      },
      quantity: item.quantity,
    }))

    const session = await createCheckoutSession({
      line_items: lineItems,
      success_url: `${success_url}?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url,
      customer_email: customer_email || order.customers?.email,
      collect_shipping_address: true,
      metadata: {
        order_id,
        order_number: order.order_number,
      },
    })

    // Save checkout session to database
    await supabase
      .from('stripe_payment_sessions')
      .insert({
        order_id,
        stripe_session_id: session.id,
        session_status: session.status,
        amount_total: session.amount_total || 0,
        currency: session.currency || 'gbp',
        customer_email: session.customer_email,
        expires_at: session.expires_at
          ? new Date(session.expires_at * 1000).toISOString()
          : null,
      })

    return res.status(200).json({
      url: session.url,
      session_id: session.id,
      payment_status: session.payment_status,
      amount_total: session.amount_total,
    })
  } catch (error) {
    console.error('Error creating checkout session:', error)
    return res.status(500).json({ error: 'Failed to create checkout session' })
  }
}
```
