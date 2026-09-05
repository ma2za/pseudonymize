import Stripe from 'stripe';

if (!process.env.STRIPE_SECRET_KEY) {
  throw new Error('STRIPE_SECRET_KEY is missing. Please set it in your .env.local file.');
}

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2026-08-26.dahlia', // Latest Stripe API version requested by type definitions
  appInfo: {
    name: 'pseudonymize.io',
    version: '0.6.0',
  },
});