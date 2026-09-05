import { NextResponse } from 'next/server';
import { stripe } from '@/lib/stripe';
import { prisma } from '@/db';
import { headers } from 'next/headers';
import Stripe from 'stripe';

const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

export async function POST(req: Request) {
  try {
    const body = await req.text();
    const signatureList = (await headers()).get('stripe-signature');
    
    if (!signatureList || !webhookSecret) {
      return NextResponse.json({ error: 'Missing stripe signature or webhook secret' }, { status: 400 });
    }

    let event: Stripe.Event;

    try {
      event = stripe.webhooks.constructEvent(body, signatureList, webhookSecret);
    } catch (err: any) {
      console.error(`Webhook signature verification failed.`, err.message);
      return NextResponse.json({ error: err.message }, { status: 400 });
    }

    // Handle the event
    switch (event.type) {
      case 'checkout.session.completed':
        const session = event.data.object as Stripe.Checkout.Session;
        
        const userId = session.metadata?.userId;
        const credits = parseInt(session.metadata?.credits || '0', 10);

        if (userId && credits > 0) {
          // Add credits to the user
          await prisma.user.update({
            where: { id: userId },
            data: {
              credits: { increment: credits }
            }
          });
            
          console.log(`Successfully added ${credits} credits to user ${userId}`);
        } else {
          console.warn('Checkout completed but missing metadata.', session.id);
        }
        break;
      default:
        // Unhandled event type
        break;
    }

    return NextResponse.json({ received: true });
  } catch (error) {
    console.error('Webhook error:', error);
    return NextResponse.json({ error: 'Internal webhook error' }, { status: 500 });
  }
}