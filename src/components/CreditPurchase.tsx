'use client';

import { useState } from 'react';
import { createCheckoutSession } from '@/app/actions/stripe';
import { useLocale } from 'next-intl';

export default function CreditPurchase({ dict }: { dict: any }) {
  const [loading, setLoading] = useState(false);
  const locale = useLocale();

  // Mocking price IDs. In production these should match live Stripe Product Price IDs.
  // For the sake of the MVP, we use hardcoded IDs that will need to be configured in Stripe.
  const packages = [
    {
      id: 'price_10k_credits', // Replace with real ID
      name: dict.package10k,
      credits: 10000,
      price: '$10.00',
    },
    {
      id: 'price_50k_credits', // Replace with real ID
      name: dict.package50k,
      credits: 50000,
      price: '$45.00',
      popular: true,
    },
  ];

  const handlePurchase = async (priceId: string, credits: number) => {
    setLoading(true);
    try {
      const res = await createCheckoutSession(priceId, credits, locale);
      if (res.url) {
        window.location.href = res.url;
      }
    } catch (e) {
      console.error(e);
      // fallback or toast error
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-5 grid grid-cols-1 gap-4 sm:grid-cols-2">
      {packages.map((pkg) => (
        <div 
          key={pkg.id} 
          className={`relative flex flex-col items-center justify-between rounded-lg border p-4 shadow-sm bg-[var(--pz-canvas)] ${pkg.popular ? 'border-[var(--pz-cipher)] ring-1 ring-[var(--pz-cipher)]' : 'border-[var(--pz-border)]'}`}
        >
          {pkg.popular && (
            <span className="absolute -top-3 bg-[var(--pz-cipher)] text-[var(--pz-ink)] px-2 py-0.5 rounded-full text-xs font-semibold tracking-wide">
              {dict.mostPopular}
            </span>
          )}
          <div className="text-center mt-2">
            <h4 className="text-lg font-bold text-[var(--pz-text)]">{pkg.name}</h4>
            <p className="text-sm text-[var(--pz-text-secondary)] mt-1">{pkg.credits.toLocaleString()} {dict.creditsLabel}</p>
            <p className="text-xl font-bold text-[var(--pz-text)] mt-3">{pkg.price}</p>
          </div>
          <button
            onClick={() => handlePurchase(pkg.id, pkg.credits)}
            disabled={loading}
            className={`mt-6 w-full inline-flex justify-center rounded-md px-3 py-2 text-sm font-semibold shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50 transition-colors ${pkg.popular ? 'bg-[var(--pz-cipher)] text-[var(--pz-ink)] hover:bg-[var(--pz-cipher-hover)] focus-visible:outline-[var(--pz-cipher)]' : 'bg-[var(--pz-surface)] text-[var(--pz-text)] ring-1 ring-inset ring-[var(--pz-border-strong)] hover:bg-[var(--pz-surface-inset)]'}`}
          >
            {loading ? dict.redirecting : dict.buyCredits}
          </button>
        </div>
      ))}
    </div>
  );
}