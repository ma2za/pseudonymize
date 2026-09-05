import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || 'sk_dummy_for_build', {
  apiVersion: '2026-08-26.dahlia', // Latest Stripe API version requested by type definitions
  appInfo: {
    name: 'pseudonymize.io',
    version: '0.6.0',
  },
});