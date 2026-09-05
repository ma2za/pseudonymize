'use server';

import { stripe } from '@/lib/stripe';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';

export async function createCheckoutSession(priceId: string, creditsAmount: number, locale: string) {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session) {
    throw new Error('Unauthorized');
  }

  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';

  try {
    // Create Stripe checkout session
    const checkoutSession = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'payment',
      customer_email: session.user.email,
      client_reference_id: session.user.id,
      metadata: {
        userId: session.user.id,
        credits: creditsAmount.toString(),
      },
      line_items: [
        {
          price: priceId, // The Stripe Price ID passed from the client
          quantity: 1,
        },
      ],
      success_url: `${baseUrl}/${locale}/dashboard?session_id={CHECKOUT_SESSION_ID}&success=true`,
      cancel_url: `${baseUrl}/${locale}/dashboard?canceled=true`,
    });

    return { sessionId: checkoutSession.id, url: checkoutSession.url };
  } catch (error: any) {
    console.error('Error creating checkout session:', error);
    throw new Error(error.message);
  }
}