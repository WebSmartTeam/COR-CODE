# TypeScript Types for Stripe Integration

## src/types/stripe.ts

Complete type definitions for Stripe integration:

```typescript
// Stripe-related TypeScript interfaces and types

export interface StripePaymentIntent {
  id: string;
  amount: number;
  currency: string;
  status: 'requires_payment_method' | 'requires_confirmation' | 'requires_action' | 'processing' | 'succeeded' | 'canceled';
  client_secret: string;
  payment_method_types: string[];
  last_payment_error?: {
    message: string;
    type: string;
    code?: string;
  };
}

export interface StripeCheckoutSession {
  id: string;
  url: string;
  payment_status: 'paid' | 'unpaid' | 'no_payment_required';
  status: 'open' | 'complete' | 'expired';
  amount_total: number;
  currency: string;
  customer_email?: string;
  expires_at: number;
}

export interface StripeWebhookEvent {
  id: string;
  type: string;
  data: {
    object: any;
  };
  created: number;
  livemode: boolean;
  pending_webhooks: number;
  request: {
    id: string;
    idempotency_key?: string;
  };
}

export interface PaymentSession {
  id: string;
  order_id: string;
  stripe_session_id: string;
  session_status: 'open' | 'complete' | 'expired';
  amount_total: number;
  currency: string;
  customer_email?: string;
  expires_at: string;
  created_at: string;
  updated_at: string;
}

export interface PaymentIntentRecord {
  id: string;
  order_id: string;
  stripe_payment_intent_id: string;
  amount: number;
  currency: string;
  status: string;
  payment_method_types: string[];
  client_secret?: string;
  last_payment_error?: any;
  created_at: string;
  updated_at: string;
}

export interface StripeWebhookEventRecord {
  id: string;
  stripe_event_id: string;
  event_type: string;
  processed: boolean;
  processed_at?: string;
  event_data: any;
  created_at: string;
  updated_at: string;
}

export interface CreatePaymentIntentRequest {
  amount: number;
  currency?: string;
  order_id: string;
  customer_email?: string;
  description?: string;
}

export interface CreateCheckoutSessionRequest {
  order_id: string;
  success_url: string;
  cancel_url: string;
  customer_email?: string;
  line_items: Array<{
    price_data: {
      currency: string;
      product_data: {
        name: string;
        description?: string;
        images?: string[];
      };
      unit_amount: number;
    };
    quantity: number;
  }>;
}

export interface StripeError {
  type: 'card_error' | 'invalid_request_error' | 'api_error' | 'authentication_error' | 'rate_limit_error';
  code?: string;
  message: string;
  param?: string;
  decline_code?: string;
}

export interface PaymentFormData {
  amount: number;
  currency: string;
  customer_email: string;
  customer_name: string;
  billing_address: {
    line1: string;
    line2?: string;
    city: string;
    postal_code: string;
    country: string;
  };
  shipping_address?: {
    line1: string;
    line2?: string;
    city: string;
    postal_code: string;
    country: string;
  };
}

export interface StripeConfig {
  publishableKey: string;
  webhookSecret: string;
  currency: string;
  country: string;
  supportedPaymentMethods: string[];
}

// Union types for status tracking
export type PaymentStatus = 'pending' | 'processing' | 'succeeded' | 'failed' | 'cancelled' | 'refunded';
export type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled' | 'refunded' | 'payment_failed' | 'payment_pending';

// Helper type for order updates from Stripe
export interface OrderUpdateFromStripe {
  id: string;
  stripe_payment_intent_id?: string;
  stripe_payment_status?: PaymentStatus;
  payment_method?: string;
  status?: OrderStatus;
  paid_at?: string;
}

// Cart item type
export interface CartItem {
  product_id: string;
  quantity: number;
  price?: number;
  name?: string;
}

// Customer data for checkout
export interface CustomerData {
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  addressLine1: string;
  addressLine2?: string;
  city: string;
  county?: string;
  postcode: string;
  country: string;
}

// Shipping address type
export interface ShippingAddress {
  name: string;
  addressLine1: string;
  addressLine2?: string;
  city: string;
  county?: string;
  postcode: string;
  country: string;
  phone?: string;
}
```

## Using with Supabase Generated Types

If using Supabase, you can extend the generated types:

```typescript
import type { Database } from './supabase'

// Extend Supabase types with Stripe-specific fields
export type Order = Database['public']['Tables']['orders']['Row'] & {
  stripe_payment_intent_id?: string;
  stripe_payment_status?: PaymentStatus;
}

export type OrderInsert = Database['public']['Tables']['orders']['Insert']
export type OrderUpdate = Database['public']['Tables']['orders']['Update']
```
