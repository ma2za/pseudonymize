import { getTranslations, setRequestLocale } from 'next-intl/server';
import type { Metadata } from 'next';
import { routing } from '@/i18n/routing';

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({locale, namespace: 'About'});
  const baseUrl = process.env.NEXT_PUBLIC_APP_URL || 'https://pseudonymize.io';

  const alternates: Record<string, string> = {
    'x-default': `${baseUrl}/about`,
  };
  routing.locales.forEach((l) => {
      alternates[l] = `${baseUrl}/${l}/about`;
  });

  return {
    title: `${t('title')} | pseudonymize.io`,
    description: t('description'),
    alternates: {
      canonical: `${baseUrl}/${locale}/about`,
      languages: alternates,
    },
  };
}

export default async function AboutPage({params}: {params: Promise<{locale: string}>}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations('About');

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
    </div>
  );
}