import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Link } from '@/i18n/routing';
import { BrandButton } from '@/brand/components';
import type { Metadata } from 'next';
import { routing } from '@/i18n/routing';

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({locale, namespace: 'Pricing'});
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';

  const alternates: Record<string, string> = {
    'x-default': `${baseUrl}/pricing`,
  };
  routing.locales.forEach((l) => {
      alternates[l] = `${baseUrl}/${l}/pricing`;
  });

  return {
    title: t('title'),
    description: t('description'),
    alternates: {
      canonical: `${baseUrl}/${locale}/pricing`,
      languages: alternates,
    },
    openGraph: {
      title: t('title'),
      description: t('description'),
      url: `${baseUrl}/${locale}/pricing`,
      type: 'website',
    }
  };
}

export default async function PricingPage({params}: {params: Promise<{locale: string}>}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('Pricing');

  return (
    <div className="pz-appbody">
      {/* Hero Section */}
      <section className="py-24 sm:py-32 text-center">
        <div className="pz-container px-4 sm:px-6">
          <h1 className="text-4xl sm:text-6xl font-bold tracking-tight text-[var(--pz-text)] mb-6 max-w-3xl mx-auto leading-tight">
            {t('title')}
          </h1>
          <p className="text-lg text-[var(--pz-text-secondary)] max-w-2xl mx-auto mb-4">
            {t('description')}
          </p>
          <p className="font-mono text-sm text-[var(--pz-cipher)] bg-[var(--pz-cipher-soft)] inline-block px-3 py-1 rounded-md">
            {t('unitExplanation')}
          </p>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="pb-32">
        <div className="pz-container px-4 sm:px-6 max-w-5xl">
          <div className="grid md:grid-cols-2 gap-8">
            
            {/* Starter Plan */}
            <div className="bg-[var(--pz-surface)] border border-[var(--pz-border)] rounded-2xl p-8 flex flex-col relative">
              <h3 className="text-2xl font-semibold text-[var(--pz-text)] mb-2">{t('starterName')}</h3>
              <p className="text-[var(--pz-text-secondary)] mb-6">{t('starterTokens')}</p>
              <div className="mb-8">
                <span className="text-5xl font-bold text-[var(--pz-text)]">{t('starterPrice')}</span>
              </div>
              <ul className="space-y-4 mb-8 flex-1 text-sm text-[var(--pz-text-secondary)] font-mono">
                <li className="flex items-center gap-3">
                  <span className="w-2 h-2 rounded-full bg-[var(--pz-cipher)]"></span>
                  {t('starterCredits')}
                </li>
                <li className="flex items-center gap-3">
                  <span className="w-2 h-2 rounded-full bg-[var(--pz-cipher)]"></span>
                  {t('noExpiration')}
                </li>
              </ul>
              <Link href="/login" style={{ textDecoration: 'none', width: '100%' }}>
                <BrandButton variant="secondary" className="w-full justify-center">{t('cta')}</BrandButton>
              </Link>
            </div>

            {/* Pro Plan */}
            <div className="bg-[var(--pz-surface)] border-2 border-[var(--pz-cipher)] rounded-2xl p-8 flex flex-col relative shadow-2xl shadow-[var(--pz-cipher-dark)]">
              <div className="absolute top-0 right-8 -translate-y-1/2 bg-[var(--pz-cipher)] text-[var(--pz-ink)] text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full">
                {t('mostPopular')}
              </div>
              <h3 className="text-2xl font-semibold text-[var(--pz-text)] mb-2">{t('proName')}</h3>
              <p className="text-[var(--pz-text-secondary)] mb-6">{t('proTokens')}</p>
              <div className="mb-8">
                <span className="text-5xl font-bold text-[var(--pz-text)]">{t('proPrice')}</span>
              </div>
              <ul className="space-y-4 mb-8 flex-1 text-sm text-[var(--pz-text-secondary)] font-mono">
                <li className="flex items-center gap-3">
                  <span className="w-2 h-2 rounded-full bg-[var(--pz-cipher)]"></span>
                  {t('proCredits')}
                </li>
                <li className="flex items-center gap-3">
                  <span className="w-2 h-2 rounded-full bg-[var(--pz-cipher)]"></span>
                  {t('noExpiration')}
                </li>
                <li className="flex items-center gap-3">
                  <span className="w-2 h-2 rounded-full bg-[var(--pz-cipher)]"></span>
                  {t('prioritySupport')}
                </li>
              </ul>
              <Link href="/login" style={{ textDecoration: 'none', width: '100%' }}>
                <BrandButton className="w-full justify-center">{t('cta')}</BrandButton>
              </Link>
            </div>

          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-24 bg-[var(--pz-surface-inset)] border-t border-[var(--pz-border)]">
        <div className="pz-container px-4 sm:px-6 max-w-3xl">
          <h2 className="text-3xl font-bold mb-12 text-center text-[var(--pz-text)]">{t('faqTitle')}</h2>
          <div className="space-y-8">
            <div>
              <h4 className="text-lg font-semibold text-[var(--pz-text)] mb-2">{t('faq1Q')}</h4>
              <p className="text-[var(--pz-text-secondary)]">{t('faq1A')}</p>
            </div>
            <div>
              <h4 className="text-lg font-semibold text-[var(--pz-text)] mb-2">{t('faq2Q')}</h4>
              <p className="text-[var(--pz-text-secondary)]">{t('faq2A')}</p>
            </div>
            <div>
              <h4 className="text-lg font-semibold text-[var(--pz-text)] mb-2">{t('faq3Q')}</h4>
              <p className="text-[var(--pz-text-secondary)]">{t('faq3A')}</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}