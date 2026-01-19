# Stripe CLI Configuration Guide

## Installation

```bash
# macOS (Homebrew)
brew install stripe/stripe-cli/stripe

# Verify installation
stripe --version
```

## Authentication

```bash
# Login to Stripe (opens browser)
stripe login

# Check current account
stripe config --list
```

## Dashboard Configuration via CLI

### Products & Prices

```bash
# Create a product
stripe products create \
  --name="Pilates Session" \
  --description="1-hour studio Pilates session" \
  --metadata[category]="services"

# List products
stripe products list --limit=10

# Create a price for a product
stripe prices create \
  --product=prod_xxxxx \
  --unit-amount=4500 \
  --currency=gbp

# Create product with price in one command
stripe products create \
  --name="Mat Pilates Course" \
  --default-price-data[unit_amount]=12000 \
  --default-price-data[currency]=gbp
```

### Customers

```bash
# Create a customer
stripe customers create \
  --email="client@example.com" \
  --name="John Smith" \
  --metadata[source]="website"

# List customers
stripe customers list --limit=20

# Retrieve a customer
stripe customers retrieve cus_xxxxx
```

### Payment Links (Quick Checkout)

```bash
# Create a payment link for a price
stripe payment_links create \
  --line-items[0][price]=price_xxxxx \
  --line-items[0][quantity]=1

# List payment links
stripe payment_links list
```

### Coupons & Discounts

```bash
# Create percentage discount
stripe coupons create \
  --percent-off=10 \
  --duration=once \
  --name="10% Off First Session"

# Create fixed amount discount (in pence)
stripe coupons create \
  --amount-off=500 \
  --currency=gbp \
  --duration=once \
  --name="£5 Off"

# List coupons
stripe coupons list
```

## Webhook Management

### Local Testing

```bash
# Forward webhooks to local server
stripe listen --forward-to localhost:3000/api/stripe/webhook

# Forward to specific events only
stripe listen \
  --forward-to localhost:3000/api/stripe/webhook \
  --events payment_intent.succeeded,payment_intent.payment_failed

# Get webhook signing secret (shown when listen starts)
# Use this for STRIPE_WEBHOOK_SECRET in .env.local
```

### Trigger Test Events

```bash
# Trigger a successful payment
stripe trigger payment_intent.succeeded

# Trigger a failed payment
stripe trigger payment_intent.payment_failed

# Trigger checkout session completed
stripe trigger checkout.session.completed

# List available triggers
stripe trigger --help
```

### Production Webhooks

```bash
# List webhook endpoints
stripe webhook_endpoints list

# Create a webhook endpoint
stripe webhook_endpoints create \
  --url="https://yoursite.com/api/stripe/webhook" \
  --enabled-events[0]="payment_intent.succeeded" \
  --enabled-events[1]="payment_intent.payment_failed" \
  --enabled-events[2]="checkout.session.completed"
```

## Testing & Debugging

### Test Mode vs Live Mode

```bash
# Check current mode
stripe config --list

# Use test mode explicitly
stripe --api-key sk_test_xxxxx products list

# Use live mode (be careful!)
stripe --api-key sk_live_xxxxx products list
```

### Logs & Events

```bash
# Stream real-time logs
stripe logs tail

# Filter logs by status
stripe logs tail --filter-status-code=400

# List recent events
stripe events list --limit=10

# Retrieve specific event
stripe events retrieve evt_xxxxx
```

### Payment Intents

```bash
# Create a payment intent (for testing)
stripe payment_intents create \
  --amount=2500 \
  --currency=gbp \
  --payment-method-types[0]=card

# List recent payment intents
stripe payment_intents list --limit=5

# Retrieve a payment intent
stripe payment_intents retrieve pi_xxxxx
```

## Fixtures (Bulk Operations)

Create a `stripe-fixtures.json` for repeatable setup:

```json
{
  "_meta": {
    "template_version": 0
  },
  "fixtures": [
    {
      "name": "product_pilates",
      "path": "/v1/products",
      "method": "post",
      "params": {
        "name": "1-2-1 Pilates Session",
        "description": "Private studio Pilates session"
      }
    },
    {
      "name": "price_pilates",
      "path": "/v1/prices",
      "method": "post",
      "params": {
        "product": "${product_pilates:id}",
        "unit_amount": 4500,
        "currency": "gbp"
      }
    }
  ]
}
```

Run fixtures:
```bash
stripe fixtures stripe-fixtures.json
```

## Environment Setup

### Required Environment Variables

```bash
# .env.local (development)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...  # From 'stripe listen'
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...

# .env.production (production)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...  # From dashboard webhook
VITE_STRIPE_PUBLISHABLE_KEY=pk_live_...
```

### Get Keys via CLI

```bash
# This opens Stripe Dashboard - keys are in Developers > API keys
stripe open

# Open specific dashboard section
stripe open webhooks
stripe open products
stripe open customers
stripe open logs
```

## Useful Aliases

Add to your shell profile (`.zshrc` or `.bashrc`):

```bash
# Stripe shortcuts
alias sl='stripe listen --forward-to localhost:3000/api/stripe/webhook'
alias st='stripe trigger'
alias sp='stripe products list'
alias sc='stripe customers list'
alias slog='stripe logs tail'
```

## Common Workflows

### New Product Setup

```bash
# 1. Create product
stripe products create --name="New Service" --description="Description"

# 2. Note the product ID (prod_xxxxx)

# 3. Create price
stripe prices create --product=prod_xxxxx --unit-amount=5000 --currency=gbp

# 4. Note the price ID (price_xxxxx) for your database/code
```

### Test Full Payment Flow

```bash
# Terminal 1: Start webhook listener
stripe listen --forward-to localhost:3000/api/stripe/webhook

# Terminal 2: Trigger test payment
stripe trigger payment_intent.succeeded

# Check logs for confirmation
stripe logs tail
```

### Debug Failed Payments

```bash
# Check recent failed intents
stripe payment_intents list --limit=10 | grep -A5 "status.*failed"

# Get details of specific intent
stripe payment_intents retrieve pi_xxxxx --expand[0]=latest_charge

# Check webhook delivery
stripe events list --type=payment_intent.payment_failed --limit=5
```
