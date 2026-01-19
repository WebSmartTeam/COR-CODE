# Client-Side Stripe Setup

## Installation

```bash
npm install @stripe/stripe-js @stripe/react-stripe-js
```

## src/lib/stripe.ts

Main client-side Stripe configuration:

```typescript
import { loadStripe } from '@stripe/stripe-js';

// Initialize Stripe with environment variable - NO HARDCODED KEYS!
const stripePublishableKey = import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY;

if (!stripePublishableKey) {
  throw new Error('VITE_STRIPE_PUBLISHABLE_KEY environment variable is required');
}

const stripePromise = loadStripe(stripePublishableKey);

export { stripePromise };

// Stripe configuration for UK market
export const stripeConfig = {
  currency: 'GBP',
  country: 'GB',
  supportedPaymentMethods: ['card'],
  appearance: {
    theme: 'stripe' as const,
    variables: {
      colorPrimary: '#your-brand-color', // Replace with your brand colour (e.g., '#3B82F6')
      colorBackground: '#ffffff',
      colorText: '#1a1a1a',
      colorDanger: '#df1b41',
      fontFamily: 'Inter, system-ui, sans-serif',
      spacingUnit: '4px',
      borderRadius: '8px',
    },
  },
  paymentElementOptions: {
    layout: 'tabs' as const,
    defaultValues: {
      billingDetails: {
        name: '',
        email: '',
        phone: '',
        address: {
          country: 'GB',
        },
      },
    },
  },
};

// Helper function to format price for Stripe (convert pounds to pence)
export const formatPriceForStripe = (pounds: number): number => {
  return Math.round(pounds * 100);
};

// Helper function to format price for display (convert pence to pounds)
export const formatPriceForDisplay = (pence: number): number => {
  return pence / 100;
};

// Stripe API endpoints configuration
export const stripeEndpoints = {
  createPaymentIntent: '/api/stripe/create-payment-intent',
  createCheckoutSession: '/api/stripe/create-checkout-session',
  webhook: '/api/stripe/webhook',
};

// Order status mapping for Stripe events
export const stripeStatusMap = {
  'payment_intent.succeeded': 'processing',
  'payment_intent.payment_failed': 'payment_failed',
  'payment_intent.canceled': 'cancelled',
  'checkout.session.completed': 'processing',
  'checkout.session.expired': 'cancelled',
} as const;

// Supported payment methods for UK market
export const supportedPaymentMethods = [
  'card',
  'apple_pay',
  'google_pay',
  'link',
] as const;

export type SupportedPaymentMethod = typeof supportedPaymentMethods[number];
export type StripeEvent = keyof typeof stripeStatusMap;
```

## StripeCheckout Component

Payment form component using PaymentElement:

```typescript
// src/components/StripeCheckout.tsx
import { useState } from 'react'
import { PaymentElement, useStripe, useElements } from '@stripe/react-stripe-js'
import { CreditCard, AlertCircle } from 'lucide-react'

interface StripeCheckoutProps {
  clientSecret: string
  onSuccess: (paymentIntentId: string) => void
  onError: (error: string) => void
  customerData: {
    email: string
    firstName: string
    lastName: string
  }
}

const StripeCheckout: React.FC<StripeCheckoutProps> = ({
  clientSecret,
  onSuccess,
  onError,
  customerData
}) => {
  const stripe = useStripe()
  const elements = useElements()
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    setError(null)

    if (!stripe || !elements) {
      setError('Stripe has not loaded yet. Please try again.')
      return
    }

    setProcessing(true)

    try {
      // Submit the form and validate fields
      const { error: submitError } = await elements.submit()
      if (submitError) {
        throw new Error(submitError.message)
      }

      // Confirm payment
      const result = await stripe.confirmPayment({
        elements,
        clientSecret,
        confirmParams: {
          return_url: `${window.location.origin}/order-confirmation`,
          payment_method_data: {
            billing_details: {
              name: `${customerData.firstName} ${customerData.lastName}`,
              email: customerData.email,
            },
          },
        },
        redirect: 'if_required' // Stay on page for success handling
      })

      if (result.error) {
        setError(result.error.message || 'Payment failed')
        onError(result.error.message || 'Payment failed')
      } else if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
        onSuccess(result.paymentIntent.id)
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Payment failed'
      setError(errorMessage)
      onError(errorMessage)
    } finally {
      setProcessing(false)
    }
  }

  const paymentElementOptions = {
    layout: 'tabs' as const,
    defaultValues: {
      billingDetails: {
        name: `${customerData.firstName} ${customerData.lastName}`,
        email: customerData.email,
      },
    },
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium mb-2">
          Payment Details
        </label>
        <div className="border border-gray-300 rounded-lg bg-white overflow-hidden">
          <PaymentElement options={paymentElementOptions} />
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
          <div>
            <h3 className="font-medium text-red-800 mb-1">Payment Error</h3>
            <p className="text-sm text-red-700">{error}</p>
          </div>
        </div>
      )}

      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <p className="text-sm text-green-800 mb-2">
          <strong>Secure Payment:</strong> Your payment is protected by 256-bit SSL encryption
        </p>
        <p className="text-xs text-green-700">
          We never store your card details. Powered by Stripe.
        </p>
      </div>

      <button
        type="submit"
        disabled={!stripe || processing}
        className="w-full px-8 py-4 bg-primary text-white rounded-full hover:bg-primary-dark transition-all font-medium text-xl disabled:opacity-50 flex items-center justify-center gap-2"
      >
        <CreditCard className="w-5 h-5" />
        {processing ? 'Processing Payment...' : 'Complete Payment'}
      </button>
    </form>
  )
}

export default StripeCheckout
```

## Using Elements Provider

Wrap your payment page with Elements:

```typescript
import { Elements } from '@stripe/react-stripe-js'
import { stripePromise } from '../lib/stripe'
import StripeCheckout from '../components/StripeCheckout'

const PaymentPage = () => {
  const [clientSecret, setClientSecret] = useState<string | null>(null)

  // Appearance customisation
  const appearance = {
    theme: 'stripe' as const,
    variables: {
      colorPrimary: '#your-brand-color',
      borderRadius: '8px',
    },
  }

  const stripeOptions = {
    clientSecret: clientSecret || '',
    appearance,
  }

  return (
    <div>
      {clientSecret && (
        <Elements stripe={stripePromise} options={stripeOptions}>
          <StripeCheckout
            clientSecret={clientSecret}
            onSuccess={handleSuccess}
            onError={handleError}
            customerData={customerData}
          />
        </Elements>
      )}
    </div>
  )
}
```
