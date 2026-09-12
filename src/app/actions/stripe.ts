'use server';

import { stripe } from '@/lib/stripe';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';

const SECURE_PACKAGES = {
  starter: {
    name: 'Starter Package (10k Credits)',
    credits: 10000,
    amountInCents: 1000, // $10.00
  },
  pro: {
    name: 'Pro Package (50k Credits)',
    credits: 50000,
    amountInCents: 4500, // $45.00
  }
};

export async function createCheckoutSession(packageId: 'starter' | 'pro', locale: string) {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session) {
    throw new Error('Unauthorized');
  }

  const pkg = SECURE_PACKAGES[packageId];
  if (!pkg) {
    throw new Error('Invalid package selected');
  }

  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';

  try {
    // Create Stripe checkout session with secure dynamic price_data
    const checkoutSession = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'payment',
      customer_email: session.user.email,
      client_reference_id: session.user.id,
      metadata: {
        userId: session.user.id,
        credits: pkg.credits.toString(),
      },
      line_items: [
        {
          price_data: {
            currency: 'usd',
            product_data: {
              name: pkg.name,
            },
            unit_amount: pkg.amountInCents,
          },
          quantity: 1,
        },
      ],
      success_url: `${baseUrl}/${locale}/dashboard?session_id={CHECKOUT_SESSION_ID}&success=true`,
      cancel_url: `${baseUrl}/${locale}/dashboard?canceled=true`,
    });

    return { sessionId: checkoutSession.id, url: checkoutSession.url };
  } catch (error) {
    console.error('Error creating checkout session:', error);
    throw new Error(error instanceof Error ? error.message : 'Unknown error');
  }
}