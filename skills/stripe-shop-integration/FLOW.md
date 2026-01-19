# Complete Checkout Flow

## Flow Overview

```
Cart → Checkout → Create Order → Payment Page → Stripe Payment → Success
```

### Step 1: Cart Context (State Management)

```typescript
// src/context/CartContext.tsx (Vite) or app/context/CartContext.tsx (Next.js)
import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { supabase } from '../lib/supabase'

interface CartContextType {
  cart: { [key: string]: number }  // productId -> quantity
  addToCart: (productId: string, quantity?: number) => void
  removeFromCart: (productId: string) => void
  clearCart: () => void
  getTotalItems: () => number
  loading: boolean
}

const CartContext = createContext<CartContextType | undefined>(undefined)

export const CartProvider = ({ children }: { children: ReactNode }) => {
  const [cart, setCart] = useState<{ [key: string]: number }>({})
  const [loading, setLoading] = useState(true)
  const [sessionId] = useState(() => {
    // Generate or retrieve session ID for anonymous users
    if (typeof window === 'undefined') return '' // SSR guard
    let sid = localStorage.getItem('cart_session_id')
    if (!sid) {
      sid = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      localStorage.setItem('cart_session_id', sid)
    }
    return sid
  })

  // Load cart from database on mount
  useEffect(() => {
    loadCartFromDatabase()
  }, [])

  const loadCartFromDatabase = async () => {
    try {
      setLoading(true)
      const { data: cartItems, error } = await supabase
        .from('cart_items')
        .select('product_id, quantity')
        .eq('session_id', sessionId)

      if (error) {
        console.error('Cart database error:', error.message)
        setCart({})
        return
      }

      const cartData: { [key: string]: number } = {}
      cartItems?.forEach((item: any) => {
        cartData[item.product_id] = item.quantity
      })
      setCart(cartData)
    } catch (err) {
      console.error('Database connection failed:', err)
      setCart({})
    } finally {
      setLoading(false)
    }
  }

  const saveCartToDatabase = async (newCart: { [key: string]: number }) => {
    // Clear existing and insert new items
    await supabase.from('cart_items').delete().eq('session_id', sessionId)

    const cartItems = Object.entries(newCart)
      .filter(([_, quantity]) => quantity > 0)
      .map(([productId, quantity]) => ({
        session_id: sessionId,
        product_id: productId,
        quantity: quantity
      }))

    if (cartItems.length > 0) {
      await supabase.from('cart_items').insert(cartItems)
    }
  }

  const addToCart = async (productId: string, quantity: number = 1) => {
    // Validate UUID format
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(productId)) {
      throw new Error('Invalid product ID format')
    }

    const currentQuantity = cart[productId] || 0
    const newQuantity = Math.min(currentQuantity + quantity, 99) // Max 99

    const newCart = { ...cart, [productId]: newQuantity }
    setCart(newCart)
    await saveCartToDatabase(newCart)
  }

  const removeFromCart = async (productId: string) => {
    const newCart = { ...cart }
    if (newCart[productId] > 1) {
      newCart[productId]--
    } else {
      delete newCart[productId]
    }
    setCart(newCart)
    await saveCartToDatabase(newCart)
  }

  const clearCart = async () => {
    setCart({})
    await saveCartToDatabase({})
  }

  const getTotalItems = () => {
    return Object.values(cart).reduce((total, quantity) => total + quantity, 0)
  }

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart, clearCart, getTotalItems, loading }}>
      {children}
    </CartContext.Provider>
  )
}

export const useCart = () => {
  const context = useContext(CartContext)
  if (!context) throw new Error('useCart must be used within a CartProvider')
  return context
}
```

### Step 2: Checkout Page (Create Order)

```typescript
// src/pages/Checkout.tsx (Vite) or app/checkout/page.tsx (Next.js)
import { useState } from 'react'
import { useNavigate } from 'react-router-dom' // Vite
// import { useRouter } from 'next/navigation' // Next.js
import { useCart } from '../context/CartContext'
import { supabase } from '../lib/supabase'

const Checkout = () => {
  const { cart, clearCart, getTotalItems } = useCart()
  const navigate = useNavigate() // or useRouter() for Next.js
  const [customerData, setCustomerData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    addressLine1: '',
    city: '',
    postcode: '',
    country: 'GB'
  })
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (getTotalItems() === 0) {
      setError('Your cart is empty')
      return
    }

    try {
      setSubmitting(true)
      setError(null)

      // 1. Create or get customer
      const { data: existingCustomer } = await supabase
        .from('customers')
        .select('id')
        .eq('email', customerData.email)
        .maybeSingle()

      let customerId: string

      if (existingCustomer) {
        // Update existing customer
        const { data: updated } = await supabase
          .from('customers')
          .update({
            first_name: customerData.firstName,
            last_name: customerData.lastName,
            phone: customerData.phone,
            address_line_1: customerData.addressLine1,
            city: customerData.city,
            postcode: customerData.postcode,
            country: customerData.country,
          })
          .eq('id', existingCustomer.id)
          .select()
          .single()
        customerId = updated!.id
      } else {
        // Create new customer
        const { data: newCustomer } = await supabase
          .from('customers')
          .insert({
            email: customerData.email.toLowerCase().trim(),
            first_name: customerData.firstName.trim(),
            last_name: customerData.lastName.trim(),
            phone: customerData.phone,
            address_line_1: customerData.addressLine1,
            city: customerData.city,
            postcode: customerData.postcode,
            country: customerData.country,
          })
          .select()
          .single()
        customerId = newCustomer!.id
      }

      // 2. Create order using database function
      const sessionId = localStorage.getItem('cart_session_id')
      const { data: orderId, error: orderError } = await supabase
        .rpc('create_order_from_cart_session', {
          customer_id_param: customerId,
          session_id_param: sessionId
        })

      if (orderError) throw orderError

      // 3. Get order details
      const { data: order } = await supabase
        .from('orders')
        .select('*')
        .eq('id', orderId)
        .single()

      // 4. Clear cart ONLY after success
      await clearCart()

      // 5. Navigate to payment page
      navigate(`/payment/${order!.id}`, {
        state: {
          orderId: order!.id,
          orderNumber: order!.order_number,
          totalAmount: order!.total_amount,
          customerData: {
            email: customerData.email,
            firstName: customerData.firstName,
            lastName: customerData.lastName
          }
        }
      })

    } catch (err) {
      console.error('Order creation failed:', err)
      setError(err instanceof Error ? err.message : 'Failed to create order')
    } finally {
      setSubmitting(false)
    }
  }

  // ... render form
}
```

### Step 3: Payment Page (Stripe Integration)

```typescript
// src/pages/Payment.tsx (Vite) or app/payment/[orderId]/page.tsx (Next.js)
import { useState, useEffect } from 'react'
import { useParams, useLocation, useNavigate } from 'react-router-dom'
import { Elements } from '@stripe/react-stripe-js'
import { stripePromise } from '../lib/stripe'
import StripeCheckout from '../components/StripeCheckout'

const Payment = () => {
  const { orderId } = useParams<{ orderId: string }>()
  const location = useLocation()
  const navigate = useNavigate()
  const [clientSecret, setClientSecret] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const state = location.state as {
    orderNumber: string
    totalAmount: number
    customerData: { email: string; firstName: string; lastName: string }
  }

  useEffect(() => {
    if (!orderId || !state) {
      navigate('/shop')
      return
    }
    createPaymentIntent()
  }, [orderId])

  const createPaymentIntent = async () => {
    try {
      setLoading(true)

      const response = await fetch('/api/stripe/create-payment-intent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          order_id: orderId,
          amount: state.totalAmount,
          currency: 'gbp',
          customer_email: state.customerData.email,
          description: `Order ${state.orderNumber}`,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Failed to create payment intent')
      }

      setClientSecret(data.client_secret)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to initialize payment')
    } finally {
      setLoading(false)
    }
  }

  const handlePaymentSuccess = async (paymentIntentId: string) => {
    // Navigate to confirmation
    navigate(`/order-confirmation/${orderId}`, {
      state: {
        orderNumber: state.orderNumber,
        totalAmount: state.totalAmount,
        paymentIntentId
      }
    })
  }

  const appearance = {
    theme: 'stripe' as const,
    variables: {
      colorPrimary: '#your-brand-color',
      borderRadius: '8px',
    },
  }

  return (
    <div>
      {loading && <div>Loading payment...</div>}
      {error && <div className="error">{error}</div>}

      {clientSecret && !loading && (
        <Elements
          stripe={stripePromise}
          options={{ clientSecret, appearance }}
        >
          <StripeCheckout
            clientSecret={clientSecret}
            onSuccess={handlePaymentSuccess}
            onError={setError}
            customerData={state.customerData}
          />
        </Elements>
      )}
    </div>
  )
}

export default Payment
```

### Step 4: Order Confirmation

```typescript
// src/pages/OrderConfirmation.tsx
import { useParams, useLocation } from 'react-router-dom'

const OrderConfirmation = () => {
  const { orderId } = useParams()
  const location = useLocation()
  const state = location.state as {
    orderNumber: string
    totalAmount: number
    paymentIntentId: string
  }

  return (
    <div className="text-center py-20">
      <h1 className="text-3xl font-bold mb-4">Thank You!</h1>
      <p className="text-xl mb-2">Order #{state?.orderNumber}</p>
      <p className="text-lg">Total: £{state?.totalAmount?.toFixed(2)}</p>
      <p className="mt-4 text-gray-600">
        A confirmation email has been sent to your email address.
      </p>
    </div>
  )
}

export default OrderConfirmation
```

## Key Points

1. **Create Order BEFORE Payment** - Order exists in database before Stripe is involved
2. **Validate Server-Side** - Always verify amounts match database
3. **Clear Cart ONLY on Success** - Don't clear if order creation fails
4. **Use Database Functions** - `create_order_from_cart_session` handles atomicity
5. **Session-Based Cart** - Works for anonymous users
