import { getTranslations, setRequestLocale } from 'next-intl/server';
import { TrustFacts } from '@/brand/components';
import type { Metadata } from 'next';
import { routing } from '@/i18n/routing';

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({locale, namespace: 'Security'});
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';

  const alternates: Record<string, string> = {
    'x-default': `${baseUrl}/security`,
  };
  routing.locales.forEach((l) => {
      alternates[l] = `${baseUrl}/${l}/security`;
  });

  return {
    title: `${t('title')} | pseudonymize.io`,
    description: t('description'),
    alternates: {
      canonical: `${baseUrl}/${locale}/security`,
      languages: alternates,
    },
  };
}

export default async function SecurityPage({params}: {params: Promise<{locale: string}>}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('Security');

  return (
    <div className="pz-appbody">
      <section className="py-24 sm:py-32">
        <div className="pz-container max-w-3xl text-center">
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-[var(--pz-text)] mb-8 leading-tight">
            {t('title')}
          </h1>
          <p className="text-lg text-[var(--pz-text-secondary)] leading-relaxed">
            {t('description')}
          </p>
        </div>
      </section>

      <section className="py-24 border-t border-[var(--pz-border)] bg-[var(--pz-surface)]">
        <div className="pz-container max-w-4xl">
          <div className="grid md:grid-cols-2 gap-16">
            <TrustFacts facts={[
              { label: 'Data processing', value: 'In-memory stream processing only. No payloads touch disk.' },
              { label: 'Retention', value: '0 bytes of original or pseudonymized payload retained post-request.' },
              { label: 'Encryption', value: 'TLS 1.3 in transit. AES-256 for all stored mapping tables.' },
              { label: 'Infrastructure / region', value: 'Hetzner Cloud (EU-Central, Falkenstein)' },
              { label: 'Access controls', value: 'Strict internal RBAC. No operator access to live payloads.' },
              { label: 'Subprocessors', value: 'Hetzner (Compute), Stripe (Billing), Resend (Email)' }
            ]} />
          </div>
        </div>
      </section>
    </div>
  );
}