import { getTranslations, setRequestLocale } from 'next-intl/server';
import type { Metadata } from 'next';
import { routing } from '@/i18n/routing';

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';

  const alternates: Record<string, string> = {
    'x-default': `${baseUrl}/docs`,
  };
  routing.locales.forEach((l) => {
      alternates[l] = `${baseUrl}/${l}/docs`;
  });

  return {
    title: 'Documentation | pseudonymize.io',
    description: 'Documentation for integrating the pseudonymize.io API.',
    alternates: {
      canonical: `${baseUrl}/${locale}/docs`,
      languages: alternates,
    },
  };
}

export default async function DocsPage({params}: {params: Promise<{locale: string}>}) {
  const { locale } = await params;
  setRequestLocale(locale);

  return (
    <div className="pz-appbody">
      <section className="py-24 sm:py-32 text-center">
        <div className="pz-container">
          <h1 className="text-4xl sm:text-6xl font-bold tracking-tight text-[var(--pz-text)] mb-6 max-w-3xl mx-auto leading-tight">
            Documentation
          </h1>
          <p className="text-lg text-[var(--pz-text-secondary)] max-w-2xl mx-auto mb-4">
            API Documentation coming soon in Release 1.5.
          </p>
        </div>
      </section>
    </div>
  );
}